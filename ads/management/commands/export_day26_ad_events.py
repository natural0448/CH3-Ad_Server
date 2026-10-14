import json
import hashlib
import tempfile
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from pymongo.errors import PyMongoError

from ads.exporting import EVENT_FIELDS, export_ad_events, read_ndjson



class Command(BaseCommand):
    help = '광고 사건을 새 고정 파일로 내보내고 ID·schema·SHA를 확인합니다.'

    def add_arguments(self, parser):
        parser.add_argument("--output", required=True)
        parser.add_argument("--since")
        parser.add_argument("--until")

    def handle(self, *args, **options):
        try:
            path = Path(options["output"])
            if path.exists():
                raise ValueError("고정 원본을 보존하려면 새 export 경로를 지정하세요.")
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix=".ad-export-", dir=path.parent) as folder:
                staged = Path(folder) / "events.ndjson"
                exported = export_ad_events(staged, options["since"], options["until"])
                rows = read_ndjson(staged)
                if any(set(row) != set(EVENT_FIELDS) or row["schema_version"] != "ad-event/v1" for row in rows):
                    raise ValueError("ad-event/v1의 정확한 공개 필드가 필요합니다.")
                ids = [row["event_id"] for row in rows]
                if len(ids) != len(set(ids)):
                    raise ValueError("duplicate event_id")
                checksum = hashlib.sha256(staged.read_bytes()).hexdigest()
                if checksum != exported["sha256"]:
                    raise ValueError("export 결과의 SHA가 다릅니다.")
                staged.rename(path)
            result = {"path": str(path), "rows": len(rows), "unique_events": len(set(ids)),
                      "sha256": checksum, "schema_version": "ad-event/v1",
                      "source_kind": "ad-events", "since": exported["since"], "until": exported["until"],
                      "preview": rows[:1]}
        except (OSError, ValueError, KeyError, TypeError, PyMongoError) as error:
            raise CommandError(str(error)) from error
        self.stdout.write(json.dumps(result, ensure_ascii=False))