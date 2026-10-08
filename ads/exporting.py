import hashlib
import json
from pathlib import Path
from .mongo import get_db
from .timestamps import parse_utc

EVENT_FIELDS = (
    "schema_version", "event_id", "decision_id", "event_type", "event_time", "impression_time",
    "media_id", "subject", "slot_id", "campaign_id", "owner_user_id", "bid_amount",
)

def read_ndjson(path):
    rows = []
    with Path(path).open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                raise ValueError(f"빈 행 {number}")
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"문서가 아닌 행 {number}")
            rows.append(row)
    return rows

def write_ndjson(path, rows):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return hashlib.sha256(target.read_bytes()).hexdigest()


def export_ad_events(output_path, since=None, until=None):
    start = parse_utc(since) if since else None
    end = parse_utc(until) if until else None
    if start and end and start >= end:
        raise ValueError("since는 until보다 작아야 합니다.")
    rows = []
    for event in get_db().ad_events.find().sort([("event_time", 1), ("event_id", 1)]):
        instant = parse_utc(event["impression_time"])
        if start and instant < start:
           continue
        if end and instant >= end:
            continue
        rows.append({field: event[field] for field in EVENT_FIELDS})
    rows.sort(key=lambda row: (parse_utc(row["event_time"]), row["event_id"]))
    checksum = write_ndjson(output_path, rows)
    return {"path": str(output_path), "rows": len(rows), "sha256": checksum,
            "schema_version": "ad-event/v1", "source_kind": "ad-events",
            "since": start.isoformat() if start else None,
            "until": end.isoformat() if end else None}