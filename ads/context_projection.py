import hashlib
import json
import os
import tempfile
from pathlib import Path

from .exporting import write_ndjson
from .snapshot_intake import (
    PUBLIC_FIELDS,
    SNAPSHOT_FIELDS,
    SCHEMA_VERSION,
    SOURCE_KIND,
    _check_public_state,
    _read_snapshot,
    inspect_snapshot,
)
from .timestamps import parse_utc


def read_snapshot_package(source, contract_path):
    """24일차의 동결된 원문·수신 계약을 소비하기 직전에 대조한다."""
    source = Path(source)
    contract_path = Path(contract_path)
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    if not isinstance(contract, dict):
        raise ValueError("계약은 JSON 객체여야 합니다.")
    inspected = inspect_snapshot(source)
    expected = {
        **inspected,
        "artifact_id": "data/exports/player-cdc.ndjson",
        "artifact_version": "v2",
        "collector": "game.export_player_snapshot",
        "binlog_cdc_status": "not-configured",
        "position_kind": "file-line",
        "kafka_position": None,
        "public_fields": list(PUBLIC_FIELDS),
    }
    for field, value in expected.items():
        if (field not in contract
                or json.dumps(contract[field], sort_keys=True)
                != json.dumps(value, sort_keys=True)):
            raise ValueError(f"계약과 원본이 다릅니다: {field}")
    parse_utc(contract.get("created_at"))
    declared_path = contract.get("source_path")
    if not isinstance(declared_path, str) or not declared_path:
        raise ValueError("계약 source_path가 없습니다.")
    if Path(declared_path).resolve() != source.resolve():
        raise ValueError("계약 source_path와 --source가 다릅니다.")
    # 같은 bytes에서 얻은 행·SHA를 사용한다. 검사 후 변경도 거절한다.
    rows, checksum = _read_snapshot(source)
    if checksum != inspected["sha256"]:
        raise ValueError("검사 후 원본이 변경됐습니다.")
    return rows, inspected

def normalize_snapshot(row, media_id="village-game"):
    if not isinstance(row, dict) or set(row) != SNAPSHOT_FIELDS:
        raise ValueError("공개 snapshot의 정확한 8개 필드가 필요합니다.")
    if row["schema_version"] != SCHEMA_VERSION or row["source_kind"] != SOURCE_KIND:
        raise ValueError("player-snapshot/v1 공개 입력이 필요합니다.")
    if not isinstance(media_id, str) or not media_id.strip():
        raise ValueError("media_id는 비어 있지 않은 문자열이어야 합니다.")

    _check_public_state({field: row[field] for field in PUBLIC_FIELDS})
    parse_utc(row["captured_at"])

    subject_id = str(row["id"])
    updated_at = parse_utc(row["updated_at"]).isoformat()    
    context = {"player_id": subject_id, "room_id": row["room_id"], "coins": row["coins"],
               "version": row["version"], "updated_at": updated_at}

    change = {"schema_version": "player-context-change/v1",
            "source_kind": SOURCE_KIND, "media_id": media_id, 
            "subject_id" : subject_id, "op": "upsert", "version": row["version"],
            "event_time" : updated_at, "context": context}
    canonical = json.dumps(change, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    change["change_id"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return change


def normalize_snapshot_file(source, contract_path, output, media_id="village-game"):
    if not isinstance(media_id, str) or not media_id.strip():
        raise ValueError("media_id는 비어 있지 않은 문자열이어야 합니다.")
    target = Path(output)
    if target.resolve() in {Path(source).resolve(), Path(contract_path).resolve()}:
        raise ValueError("출력은 원본·계약과 다른 경로여야 합니다.")
    rows, inspected = read_snapshot_package(source, contract_path)
    changes = [normalize_snapshot(row, media_id=media_id) for row in rows]
    unique_ids = len({change["change_id"] for change in changes})
    if unique_ids != len(changes):
        raise ValueError("정규화 change_id가 중복됐습니다.")
    target.parent.mkdir(parents=True, exist_ok=True)
    # 모두 변환한 뒤 임시 파일에 쓰고, 완성된 파일만 최종 경로로 옮긴다.
    with tempfile.TemporaryDirectory(prefix=".normalize-", dir=target.parent) as folder:
        staged = Path(folder) / "changes.ndjson"
        checksum = write_ndjson(staged, changes)
        os.replace(staged, target)
    return {"path": str(target), "rows": len(changes), "sha256": checksum,
            "schema_version": "player-context-change/v1", "source_kind": SOURCE_KIND,
            "source_sha256": inspected["sha256"], "media_id": media_id,
            "op_counts": {"upsert": len(changes)}, "unique_change_ids": unique_ids,
            "preview": changes[:1]}