"""광고 서버 작업 폴더에서 python check_day24_period5.py로 실행합니다."""
import hashlib
import json
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ads.snapshot_intake import build_snapshot_contract


# 실제 export 파일 대신 임시 폴더에만 별도 검사 입력을 씁니다.
row = {"schema_version": "player-snapshot/v1", "source_kind": "player-snapshot",
       "captured_at": "2026-10-08T01:00:00+00:00", "id": 2, "room_id": "room-01",
       "coins": 30, "version": 1, "updated_at": "2026-10-08T00:00:00+00:00"}


def write_rows(path, rows):
    path.write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in rows),
                    encoding="utf-8")
    return path


with tempfile.TemporaryDirectory(prefix="day24-period5-") as folder:
    root = Path(folder)
    source = write_rows(root / "snapshot.ndjson", [row, {**row, "id": 1}])
    saved = source.read_bytes()
    started = datetime.now(timezone.utc)
    contract = build_snapshot_contract(source)
    finished = datetime.now(timezone.utc)
    expected = {"rows": 2, "public_ids": [1, 2], "captured_at": row["captured_at"],
                "sha256": hashlib.sha256(saved).hexdigest(),
                "source_kind": "player-snapshot", "schema_version": "player-snapshot/v1"}
    for field, value in expected.items():
        assert contract[field] == value, f"{field}: 기대 {value}, 실제 {contract[field]}"
    metadata = {"artifact_id": "data/exports/player-cdc.ndjson", "artifact_version": "v2",
                "source_path": str(source), "collector": "game.export_player_snapshot",
                "binlog_cdc_status": "not-configured", "position_kind": "file-line",
                "kafka_position": None,
                "public_fields": ["id", "room_id", "coins", "version", "updated_at"]}
    for field, value in metadata.items():
        assert contract[field] == value, f"계약 메타데이터가 다릅니다: {field}"
    created = datetime.fromisoformat(contract["created_at"])
    captured = datetime.fromisoformat(contract["captured_at"])
    assert created.utcoffset() == timedelta(0), "created_at은 aware UTC 시각이어야 합니다."
    assert captured.utcoffset() == timedelta(0), "검사 입력의 captured_at을 보존하세요."
    assert started <= created <= finished, "created_at은 이번 계약 생성 시각이어야 합니다."
    assert source.read_bytes() == saved, "정상 계약 생성이 입력 파일을 변경했습니다."
    print("PASS: 실제 rows·정렬 ID·SHA-256·수집/계약 시각·메타데이터")

    empty = write_rows(root / "empty.ndjson", [])
    result = build_snapshot_contract(empty)
    assert result["rows"] == 0 and result["public_ids"] == []
    assert result["captured_at"] is None
    assert result["sha256"] == hashlib.sha256(b"").hexdigest()
    assert empty.read_bytes() == b"", "빈 입력을 변경했습니다."
    print("PASS: 0행 계약과 빈 bytes의 SHA-256")

    invalid = [
        ("중복 ID", [row, row]),
        ("비공개 필드 혼입", [{**row, "user_id": 1}]),
        ("필수 필드 누락", [{key: value for key, value in row.items() if key != "coins"}]),
        ("잘못된 출처", [{**row, "source_kind": "teaching-fixture"}]),
        ("시간대 없는 수집 시각", [{**row, "captured_at": "2026-10-08T01:00:00"}]),
    ]
    for number, (name, rows) in enumerate(invalid):
        path = write_rows(root / f"invalid-{number}.ndjson", rows)
        before = path.read_bytes()
        try:
            build_snapshot_contract(path)
        except ValueError:
            pass
        else:
            raise AssertionError(f"거절하지 않았습니다: {name}")
        assert path.read_bytes() == before, f"실패 호출이 입력을 변경했습니다: {name}"
        print(f"PASS: {name} 거절·입력 보존")
    assert source.read_bytes() == saved, "검사 중 정상 원본이 변경됐습니다."

print("PASS: 5교시 함수 검사 완료 (실제 DB·export·계약 파일 변경 없음)")