import hashlib
import io
import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

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
        parse_utc

        if captured_at is None:
            captured_at = row["captured_at"]
        elif row["captured_at"] != captured_at:
            raise ValueError("같은 수집이 아님")
    return {"rows": len(rows), "public_ids": sorted(seen),
            "source_kind": SOURCE_KIND, "schema_version": SCHEMA_VERSION,
            "captured_at": captured_at, "sha256": checksum}