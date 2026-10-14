import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from .context_projection import make_context_document
from .exporting import read_ndjson
from .timestamps import parse_utc


def stable_json(row):
    return json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def build_history(rows):
    """검증한 고유 변경을 시각·ID 순서로 반환한다. 입력·DB를 수정하지 않는다."""
    unique = {}
    for row in rows:
        # 25일차의 필드·공개 상태·출처·change_id 검사를 그대로 재사용한다.
        make_context_document(row)
        old = unique.get(row["change_id"])
        if old is not None and stable_json(old) != stable_json(row):
            raise ValueError("same change_id has conflicting content")
        unique[row["change_id"]] = row
    return sorted(unique.values(), key=lambda row: (
        parse_utc(row["event_time"]), row["change_id"]))


def build_current(history):
    """수신자별 최대 version을 고른다. 삭제 상태도 최신 후보에 남긴다."""
    current = {}
    ordered = sorted(build_history(history), key=lambda row: (
        row["media_id"], row["subject_id"], row["version"], row["change_id"]))
    for row in ordered:
        document = make_context_document(row)
        key = document["_id"]
        candidate = {"schema_version": "player-current/v1", **document}
        old = current.get(key)
        if old is None or candidate["version"] > old["version"]:
            current[key] = candidate
        elif candidate["version"] == old["version"] and (
                candidate["deleted"] != old["deleted"] or candidate["context"] != old["context"]):
            raise ValueError("same subject/version has conflicting content")
    return [current[key] for key in sorted(current)]
