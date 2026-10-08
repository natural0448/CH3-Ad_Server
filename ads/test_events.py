"""Real isolated MongoDB event uniqueness, snapshot and media-auth tests."""
import json
import os
import uuid
from io import StringIO
from concurrent.futures import ThreadPoolExecutor
from unittest import skipUnless
from unittest.mock import patch

from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.test import Client, SimpleTestCase, TestCase, override_settings
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from ads.events import record_ad_event
from ads.services import choose_ad


@override_settings(MEDIA_KEYS={"village-game": "test-event-key"})
class EventAuthTests(SimpleTestCase):
    def test_both_media_headers_must_match_the_authenticated_body(self):
        body = {"media_id": "village-game", "subject": {"media_id": "village-game", "subject_id": "7"},
                "decision_id": "d1", "event_type": "impression"}
        for headers in ({"HTTP_X_MEDIA_KEY": "test-event-key"},
                        {"HTTP_X_MEDIA_ID": "village-game"},
                        {"HTTP_X_MEDIA_ID": "other", "HTTP_X_MEDIA_KEY": "test-event-key"}):
            with self.subTest(headers=list(headers)), patch("ads.views.record_ad_event") as record:
                response = self.client.post("/api/media/events/", data=json.dumps(body),
                                            content_type="application/json", **headers)
                self.assertEqual(response.status_code, 401)
                self.assertEqual(response.json(), {"error": "media_auth_required"})
                record.assert_not_called()

    def test_public_snapshot_error_keeps_only_the_allowed_error_code(self):
        with patch("ads.views.record_ad_event", side_effect=ValueError("decision_snapshot_missing: detail")):
            response = self.client.post("/api/media/events/", content_type="application/json",
                data=json.dumps({"media_id": "village-game", "subject": {"media_id": "village-game", "subject_id": "7"},
                                 "decision_id": "d1", "event_type": "impression"}),
                HTTP_X_MEDIA_ID="village-game", HTTP_X_MEDIA_KEY="test-event-key")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "decision_snapshot_missing"})

    def test_media_key_json_subject_and_post_are_required(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.get("/api/media/events/").status_code, 405)
        body = {"media_id": "village-game", "subject": {"media_id": "village-game", "subject_id": "7"},
                "decision_id": "d1", "event_type": "impression"}
        self.assertEqual(client.post("/api/media/events/", data=json.dumps(body), content_type="application/json").status_code, 401)
        for bad, content_type in [("{", "application/json"), ("[]", "application/json"),
                                 (json.dumps(body), "text/plain"),
                                 (json.dumps({**body, "subject": {"media_id": "other", "subject_id": "7"}}), "application/json")]:
            with self.subTest(bad=bad), patch("ads.views.record_ad_event") as record:
                response = client.post("/api/media/events/", data=bad, content_type=content_type,
                                       HTTP_X_MEDIA_ID="village-game", HTTP_X_MEDIA_KEY="test-event-key")
                self.assertEqual(response.status_code, 400)
                record.assert_not_called()

    def test_store_outage_is_503_and_no_private_exception_is_exposed(self):
        with patch("ads.views.record_ad_event", side_effect=PyMongoError("internal fixture")):
            response = self.client.post("/api/media/events/", content_type="application/json",
                data=json.dumps({"media_id": "village-game", "subject": {"media_id": "village-game", "subject_id": "7"},
                                 "decision_id": "d1", "event_type": "impression"}), HTTP_X_MEDIA_ID="village-game", HTTP_X_MEDIA_KEY="test-event-key")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"error": "ads_unavailable"})


@skipUnless(os.environ.get("ADS_TEST_MONGO_URI"), "Requires isolated ADS_TEST_MONGO_URI")
class EventIntegrationTests(TestCase):
    def test_subject_field_order_does_not_change_recipient_identity(self):
        did = self.decision["decision_id"]
        self.database.decisions.update_one({"_id": did}, {"$set": {
            "subject": {"subject_id": "7", "media_id": "village-game"}}})
        self.assertTrue(record_ad_event(self.subject, did, "impression")["created"])

    def test_old_incomplete_snapshot_is_rejected_without_backfilling(self):
        did = self.decision["decision_id"]
        self.database.decisions.update_one({"_id": did}, {"$unset": {"candidates": ""}})
        before = self.database.decisions.find_one({"_id": did})
        with self.assertRaisesRegex(ValueError, "decision_snapshot_missing"):
            record_ad_event(self.subject, did, "impression")
        self.assertEqual(self.database.decisions.find_one({"_id": did}), before)
        self.assertEqual(self.database.ad_events.count_documents({}), 0)

    def test_index_command_is_repeatable_and_prints_the_lesson_name(self):
        for _ in range(2):
            output = StringIO()
            call_command("create_ad_indexes", stdout=output)
            self.assertEqual(output.getvalue().strip(), "decision_event_once")
        self.assertTrue(self.database.ad_events.index_information()["decision_event_once"]["unique"])

    def test_advertiser_page_lists_only_owner_decisions_latest_first_without_events(self):
        user = get_user_model().objects.create_user(pk=101, username="event-owner")
        self.assertEqual(self.client.get("/advertiser/events/").status_code, 302)
        self.client.force_login(user)
        self.database.decisions.insert_one({"_id": "other-owner", "owner_user_id": 202})
        second = choose_ad("village-game", "7", "village-board", {})
        before = self.database.ad_events.count_documents({})
        response = self.client.get("/advertiser/events/")
        self.assertEqual(response.status_code, 200)
        rows = response.context["rows"]
        self.assertEqual([r["decision_id"] for r in rows], [second["decision_id"], self.decision["decision_id"]])
        self.assertContains(response, "forest-tools")
        self.assertContains(response, "미기록")
        self.assertNotContains(response, "other-owner")
        self.assertEqual(self.database.ad_events.count_documents({}), before)
        self.assertEqual(self.client.post("/advertiser/events/").status_code, 405)
        record_ad_event(self.subject, second["decision_id"], "impression")
        record_ad_event(self.subject, second["decision_id"], "click")
        rows = self.client.get("/advertiser/events/").context["rows"]
        self.assertEqual(rows[0]["impression"]["event_type"], "impression")
        self.assertEqual(rows[0]["click"]["event_type"], "click")
        with patch("ads.views.get_db", side_effect=PyMongoError("private failure")):
            response = self.client.get("/advertiser/events/")
        self.assertContains(response, "광고 실적 저장소에 연결할 수 없습니다.", status_code=503)
        self.assertNotContains(response, "private failure", status_code=503)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.connection = MongoClient(os.environ["ADS_TEST_MONGO_URI"], serverSelectionTimeoutMS=3000)
        cls.database = cls.connection["ads_events_test_" + uuid.uuid4().hex]

    @classmethod
    def tearDownClass(cls):
        cls.connection.drop_database(cls.database.name)
        cls.connection.close()
        super().tearDownClass()

    def setUp(self):
        for name in ("campaigns", "bids", "decisions", "ad_events"):
            self.database[name].delete_many({})
        for target in ("ads.events.get_db", "ads.services.get_db", "ads.management.commands.ensure_ad_event_indexes.get_db", "ads.management.commands.create_ad_indexes.get_db", "ads.views.get_db"):
            fixture = patch(target, return_value=self.database)
            fixture.start()
            self.addCleanup(fixture.stop)
        call_command("ensure_ad_event_indexes", verbosity=0)
        self.database.campaigns.insert_one({"_id": "forest-tools", "campaign_id": "forest-tools",
            "owner_user_id": 101, "slot_id": "village-board", "title": "숲 도구점", "body": "도구",
            "active": True, "creative_path": "/static/ads/creatives/forest-tools.png"})
        self.database.bids.insert_one({"_id": "forest-tools", "owner_user_id": 101, "bid_amount": 20})
        self.subject = {"media_id": "village-game", "subject_id": "7"}
        self.decision = choose_ad("village-game", "7", "village-board", {})

    def test_first_duplicate_click_and_snapshot_amount(self):
        did = self.decision["decision_id"]
        self.database.bids.update_one({"_id": "forest-tools"}, {"$set": {"bid_amount": 30}})
        self.assertEqual(self.database.ad_events.count_documents({}), 0)
        first = record_ad_event(self.subject, did, "impression")
        saved = self.database.ad_events.find_one({"_id": first["event_id"]})
        duplicate = record_ad_event(self.subject, did, "impression")
        self.assertTrue(first["created"]);self.assertFalse(duplicate["created"])
        self.assertEqual(first["event_id"], duplicate["event_id"])
        self.assertEqual(saved, self.database.ad_events.find_one({"_id": first["event_id"]}))
        click = record_ad_event(self.subject, did, "click")
        self.assertTrue(click["created"])
        self.assertFalse(record_ad_event(self.subject, did, "click")["created"])
        row = self.database.ad_events.find_one({"_id": click["event_id"]})
        self.assertEqual(row["impression_time"], saved["event_time"])
        self.assertEqual(row["bid_amount"], 20)
        self.assertEqual(row["owner_user_id"], 101)
        self.assertEqual(row["schema_version"], "ad-event/v1")
        self.assertEqual(self.database.ad_events.count_documents({"decision_id": did}), 2)

    def test_click_before_impression_wrong_subject_and_empty_decision(self):
        did = self.decision["decision_id"]
        for subject, decision_id, kind in [(self.subject, did, "click"),
                ({**self.subject, "subject_id": "other"}, did, "impression"),
                (self.subject, "not-found", "impression")]:
            with self.subTest(kind=kind, decision_id=decision_id), self.assertRaises(ValueError):
                record_ad_event(subject, decision_id, kind)
        empty = choose_ad("village-game", "7", "lobby-banner", {})
        with self.assertRaises(ValueError):record_ad_event(self.subject, empty["decision_id"], "impression")
        self.assertEqual(self.database.ad_events.count_documents({}), 0)

    def test_concurrent_duplicates_have_one_first_write(self):
        did = self.decision["decision_id"]
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda _: record_ad_event(self.subject, did, "impression"), range(12)))
        self.assertEqual(sum(row["created"] for row in results), 1)
        self.assertEqual(self.database.ad_events.count_documents({"decision_id": did}), 1)
        self.assertTrue(self.database.ad_events.index_information()["decision_event_once"]["unique"])

    def test_invalid_types_and_missing_candidate_are_input_errors(self):
        did = self.decision["decision_id"]
        for subject, decision_id, kind in [(None, did, "impression"), ({**self.subject, "extra": True}, did, "impression"),
                ({**self.subject, "subject_id": 7}, did, "impression"), (self.subject, None, "impression"),
                (self.subject, did, []), (self.subject, did, "conversion")]:
            with self.subTest(kind=kind), self.assertRaises(ValueError):record_ad_event(subject, decision_id, kind)
        self.database.decisions.update_one({"_id": did}, {"$set": {"candidates": []}})
        with self.assertRaises(ValueError):record_ad_event(self.subject, did, "impression")

    @override_settings(MEDIA_KEYS={"village-game": "test-event-key"})
    def test_real_media_event_endpoint_duplicate_and_nonhashable_type(self):
        body = {"media_id": "village-game", "subject": self.subject,
                "decision_id": self.decision["decision_id"], "event_type": "impression"}
        client = Client(enforce_csrf_checks=True)
        first = client.post("/api/media/events/", data=json.dumps(body), content_type="application/json", HTTP_X_MEDIA_ID="village-game", HTTP_X_MEDIA_KEY="test-event-key")
        duplicate = client.post("/api/media/events/", data=json.dumps(body), content_type="application/json", HTTP_X_MEDIA_ID="village-game", HTTP_X_MEDIA_KEY="test-event-key")
        self.assertTrue(first.json()["created"]);self.assertFalse(duplicate.json()["created"])
        invalid = client.post("/api/media/events/", data=json.dumps({**body, "event_type": []}), content_type="application/json", HTTP_X_MEDIA_ID="village-game", HTTP_X_MEDIA_KEY="test-event-key")
        self.assertEqual(invalid.status_code, 400)
