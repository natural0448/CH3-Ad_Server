from .mongo import get_db
from .context_projection import make_context_document

COMPARE_FIELDS = ("media_id", "subject_id", "version", "deleted", "context")


def _index_context_rows(rows):
    fields = {"_id", "media_id", "subject_id", "version", "deleted", "context",
              "source_kind", "change_id", "event_time"}
    indexed = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) not in (fields, fields | {"schema_version"}):
            raise ValueError("대조 문서의 공개 필드 계약이 다릅니다.")
        if "schema_version" in row and row["schema_version"] != "player-current/v1":
            raise ValueError("player-current/v1 문서가 필요합니다.")
        if type(row["deleted"]) is not bool:
            raise ValueError("deleted는 bool이어야 합니다.")
        document = {name: row[name] for name in fields}
        change = {"schema_version": "player-context-change/v1",
                  "op": "delete" if row["deleted"] else "upsert",
                  **{name: row[name] for name in fields - {"_id", "deleted"}}}
        if make_context_document(change) != document:
            raise ValueError("대조 문서의 키·공개 상태·변경 ID가 다릅니다.")
        if row["_id"] in indexed:
            raise ValueError("duplicate subject key")
        indexed[row["_id"]] = row
    return indexed


def compare_rows(expected_rows, actual_rows):
    expected = _index_context_rows(expected_rows)
    actual = _index_context_rows(actual_rows)

    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    mismatched = []

    for key in sorted(set(expected) & set(actual)):
        fields = [name for name in COMPARE_FIELDS if expected[key][name] != actual[key][name]]
        if fields:
            mismatched.append({"_id": key, "fields": fields,
                               "values": {name: {"lake": expected[key][name], "mongo": actual[key][name]}
                                          for name in fields}})
    matched = len(expected) - len(missing) - len(mismatched)
    return {"expected_keys": len(expected), "missing": missing, "extra_keys": extra,
            "mismatched": mismatched, "matched": matched,
            "input_scope_matches": not missing and not mismatched}

def compare_context_to_current(current_rows, media_id="village-game"):
    # 동일 입력의 키만 일치 기준이며 이전 입력의 추가 키는 따로 기록한다.
    if any(row.get("media_id") != media_id for row in current_rows):
        raise ValueError("current와 지정 매체가 다릅니다.")
    actual = list(get_db()["player_context"].find({"media_id": media_id}))
    return compare_rows(current_rows, actual)