"""Install the unique decision/event index without editing records."""
from django.core.management.base import BaseCommand, CommandError
from pymongo.errors import PyMongoError
from ads.mongo import get_db


class Command(BaseCommand):
    help = "Create decision_event_once on ad_events; never delete or rewrite events."

    def handle(self, *args, **options):
        try:
            name = get_db().ad_events.create_index(
                [("decision_id", 1), ("event_type", 1)], unique=True, name="decision_event_once")
        except PyMongoError as exc:
            raise CommandError("사건 인덱스를 만들 수 없습니다. 연결 또는 기존 중복 문서를 확인하세요.") from exc
        self.stdout.write(self.style.SUCCESS("Ready: " + name))
