import hashlib
import io
import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest import result

from .exporting import read_ndjson, write_ndjson
from .timestamps import parse_utc


SCHEMA_VERSION = "player-snapshot/v1"
SOURCE_KIND = "player-snapshot"
PUBLIC_FIELDS = ("id", "room_id", "coins", "version", "updated_at")
SNAPSHOT_FIELDS = set(PUBLIC_FIELDS) | {"schema_version", "source_kind", "captured_at"}


def _read_snapshot(path):
    """검증할 행과 체크섬을 같은 한 번의 bytes 읽기에서 얻는다."""
    payload = Path(path).read_bytes()
    rows = []
    for number, line in enumerate(io.StringIO(payload.decode("utf-8")), 1):
        if not line.strip():
            raise ValueError(f"빈 행 {number}")
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"문서가 아닌 행 {number}")
        rows.append(row)
    return rows, hashlib.sha256(payload).hexdigest()


def _check_public_state(row):
    """게임 계정·좌표를 받지 않는 공개 상태의 형식 검사."""
    if not isinstance(row, dict) or set(row) != set(PUBLIC_FIELDS):
        raise ValueError("공개 상태는 id, room_id, coins, version, updated_at만 받습니다.")
    if type(row["id"]) is not int or row["id"] <= 0:
        raise ValueError("id는 양의 정수여야 합니다.")
    if not isinstance(row["room_id"], str):
        raise ValueError("room_id는 문자열이어야 합니다.")
    if type(row["coins"]) is not int:
        raise ValueError("coins는 정수여야 합니다.")
    if type(row["version"]) is not int or row["version"] < 0:
        raise ValueError("version은 0 이상의 정수여야 합니다.")
    parse_utc(row["updated_at"])


def inspect_snapshot(path):
    rows, checksum = _read_snapshot(path)
    seen = set()
    captured_at = None
    for row in rows:
        if set(row) != SNAPSHOT_FIELDS:
            raise ValueError("스냅샷 필드 오류")
        if row["schema_version"] != SCHEMA_VERSION or row["source_kind"] != SOURCE_KIND:
            raise ValueError("스냅샷 출처 오류")

        _check_public_state({field: row[field] for field in PUBLIC_FIELDS})

        if row["id"] in seen:
            raise ValueError("중복 ID")
        seen.add(row["id"])
        parse_utc(row["captured_at"])

        if captured_at is None:
            captured_at = row["captured_at"]
        elif row["captured_at"] != captured_at:
            raise ValueError("같은 수집이 아님")
    return {"rows": len(rows), "public_ids": sorted(seen),
            "source_kind": SOURCE_KIND, "schema_version": SCHEMA_VERSION,
            "captured_at": captured_at, "sha256": checksum}

def readiness(mysql_config=None, connect_home=None, debezium_dir=None):
    supplied_paths = {
        "mysql_config": mysql_config,
        "connect_home": connect_home,
        "debezium_dir": debezium_dir
    }
    paths = {name: {"supplied": bool(value), "exists": Path(value).exists()
        if value else False} for name, value in supplied_paths.items()}
    return {"schema_version": "cdc-readiness/v1", "paths": paths,
            "mysql_binlog": "not-verified", "cdc_reader": "not-configured",
            "connect_worker": "not-configured", "debezium_connector": "not-configured",
            "player_change_topic": "not-configured", "common_input": SCHEMA_VERSION,
            "binlog_cdc_observed": False}

def change_player(event):
    if event.get("source_kind") != "teaching-fixture":
        raise ValueError("이 함수에는 teaching-fixture만 넣습니다.")
    op = event.get("op")
    before, after = event.get("before"), event.get("after")
    if op == "r":
        if before is not None or not isinstance(after, dict):
            raise ValueError("r은 before=None과 after 공개 상태가 필요합니다.")
        _check_public_state(after)
    elif op == "u":
        _check_public_state(before)
        _check_public_state(after)
        if before["id"] != after["id"]:
            raise ValueError("u의 before와 after id가 다릅니다.")
    elif op == "d":
        if not isinstance(before, dict) or after is not None:
            raise ValueError("d는 before 공개 상태와 after=None이 필요합니다.")
        _check_public_state(before)
    else:
        raise ValueError("op는 r, u, d만 받습니다.")
    state = before if op == "d" else after
    return {"op": op, "player_id": state["id"], "coins": state["coins"],
            "version": state["version"], "deleted": op == "d"}


# def build_snapshot_contract(source):
#     """검사한 파일의 행 수·ID·체크섬을 인계 계약으로 만든다."""
#     inspected = inspect_snapshot(source)

#     contract = {"artifact_id": "data/exports/player-cdc.ndjson", "artifact_version": "v2",
#         "source_path": str(source), "created_at": datetime.now(timezone.utc).isoformat(),
#         "collector": "game.export_player_snapshot", "binlog_cdc_status": "not-configured",
#         "position_kind": "file-line", "kafka_position": None,
#         "public_fields": list(PUBLIC_FIELDS)}
#     contract.update(inspected)
#     return contract

def build_snapshot_contract(source):
    inspected = inspect_snapshot(source)
    contract = {"artifact_id": "data/exports/player-cdc.ndjson", "artifact_version": "v2",
                "source_path": str(source), "created_at": datetime.now(timezone.utc).isoformat(),
                "collector": "game.export_player_snapshot", "binlog_cdc_status": "not-configured",
                "position_kind": "file-line", "kafka_position": None,
                "public_fields": list(PUBLIC_FIELDS)}
    contract.update(inspected)
    return contract


def load_rows(path):
    inspect_snapshot(path)
    return {row["id"]: row for row in read_ndjson(path)}


def compare(before, after):
    changed = []
    for player_id in sorted(set(before) & set(after)):
        old, new = before[player_id], after[player_id]
        old_state = (old["room_id"], old["coins"], old["version"], parse_utc(old["updated_at"]))
        new_state = (new["room_id"], new["coins"], new["version"], parse_utc(new["updated_at"]))
        if old_state != new_state:
            changed.append({"id": player_id, "before_version": old["version"],
                            "after_version": new["version"], "before_coins": old["coins"],
                            "after_coins": new["coins"]})
    return {"changed": changed, "newly_seen": sorted(set(after) - set(before)),
            "missing_unknown": sorted(set(before) - set(after))}


def missing_summary(before, after):

    missing = sorted(set(before) - set(after))
    result = {"missing_unknown": missing, "source_kind": "snapshot-comparison",
            "delete_events": [], "delete_inference_allowed": False}
    return result


def handoff_snapshot(source, contract_path, target):
    source, target = Path(source), Path(target)
    contract = json.loads(Path(contract_path).read_text(encoding="utf-8"))
    inspected = inspect_snapshot(source)
    expected = {"artifact_id": "data/exports/player-cdc.ndjson", "artifact_version": "v2",
                "public_fields": list(PUBLIC_FIELDS), "position_kind": "file-line",
                "kafka_position": None, "collector": "game.export_player_snapshot",
                "binlog_cdc_status": "not-configured", **inspected}

    for field, value in expected.items():
        if field not in contract or json.dumps(contract[field], sort_keys=True) != json.dumps(value, sort_keys=True):
            raise ValueError(f"다른 값: {field}")
    parse_utc(contract["created_at"])

    if target.exists():
        raise ValueError("새 출력 경로를 지정하세요.")
    
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{target.name}-", dir=target.parent))
    try:
        received = temporary / "player-cdc.ndjson"

        shutil.copyfile(source, received)
        if hashlib.sha256(received.read_bytes()).hexdigest() != inspected["sha256"]:
            raise ValueError("복사 결과가 다릅니다.")
        # [문제 4 · 한 줄] 기존 계약을 복사하되 source_path만 최종 수신 파일 경로로 바꾼다.
        # 예시: copied_metadata = {**metadata, "path": str(output_path)}
        received_contract = {**contract, "source_path": str(target / "player-cdc.ndjson")}
        (temporary / "player-cdc-contract.json").write_text(
            json.dumps(received_contract, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8")
        # [문제 5 · 한 줄] 검증된 파일·계약이 모두 준비된 임시 폴더를 최종 target으로 옮긴다.
        # 예시: staged_folder.rename(final_folder)
        temporary.rename(target)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return {"rows": inspected["rows"], "sha256": inspected["sha256"],
            "source_kind": SOURCE_KIND, "target": str(target)}


