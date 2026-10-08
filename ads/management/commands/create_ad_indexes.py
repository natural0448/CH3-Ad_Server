from django.core.management.base import BaseCommand
from ads.mongo import get_db


class Command(BaseCommand):
    help = "광고 실적의 결정·종류 고유 색인을 생성합니다."

    def handle(self, *args, **options):
        name = get_db().ad_events.create_index(
            [("decision_id", 1), ("event_type", 1)], unique=True,
            name="decision_event_once")
        self.stdout.write(name)
