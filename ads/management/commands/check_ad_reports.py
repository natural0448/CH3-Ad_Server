import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from ads.exporting import read_ndjson
from ads.mongo import get_db
from ads.reporting import build_daily_reports


class Command(BaseCommand):
    help = "전체 보관 사건의 고정 입력과 게시 보고서를 대조합니다."

    def add_arguments(self, parser):
        parser.add_argument("--source", required=True)
        parser.add_argument("--output", required=True)

    def handle(self, *args, **options):
        source = Path(options["source"])
        events = read_ndjson(source)
        expected = {row["_id"]: row for row in build_daily_reports(events)}
        actual = {row["_id"]: row for row in get_db().ad_daily_reports.find()}
        fields = ("impressions", "clicks", "ctr", "bid_units_sum", "source_max_event_time")

        missing = sorted(expected.keys() - actual.keys())
        extra = sorted(actual.keys() - expected.keys())
        different = sorted(key for key in expected.keys() & actual.keys()
            if any(expected[key][field] != actual[key][field] for field in fields))
        result = {
            "artifact_id": "village-lab.ads-analytics", "artifact_version": "v2",
            "source_kind": "ad-events", "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "source_rows": len(events), "unique_events": len({row["event_id"] for row in events}),
            "missing_report_keys": missing, "extra_report_keys": extra,
            "different_report_keys": different, "ok": not (missing or extra or different),
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "transport": "file", "spark_ad_job_status": "not-configured",
            "gui_status": "separate-manual-observation",
        }

        target = Path(options["output"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False) + "\n", encoding="utf-8")
        if not result["ok"]:
            raise CommandError("검사 결과를 확인하세요.")