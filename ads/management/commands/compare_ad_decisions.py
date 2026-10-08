import json

from django.core.management.base import BaseCommand, CommandError
from pymongo.errors import PyMongoError

from ads.mongo import get_db


class Command(BaseCommand):
    help = "Read two stored decision snapshots without recomputing current bids."

    def add_arguments(self, parser):
        parser.add_argument("first_id")
        parser.add_argument("second_id")

    def handle(self, *args, **options):
        try:
            for decision_id in [options["first_id"], options["second_id"]]:
                row = get_db().decisions.find_one({"_id": decision_id})
                if row is None:
                    raise CommandError("결정을 찾을 수 없습니다: " + decision_id)
                self.stdout.write(json.dumps({
                    "decision_id": row["decision_id"],
                    "campaign_id": row["chosen_campaign_id"],
                    "bid_amount": row["chosen_bid_amount"],
                    "candidates": row["candidates"], "subject": row["subject"],
                    "policy_version": row["policy_version"],
                }, ensure_ascii=False))
        except PyMongoError as exc:
            raise CommandError("MongoDB에 연결할 수 없습니다.") from exc
