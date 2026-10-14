"""Real isolated MongoDB event uniqueness, snapshot and media-auth tests."""
import json
import hashlib
import copy
import os
import tempfile
import uuid
from pathlib import Path
from io import StringIO
from concurrent.futures import ThreadPoolExecutor
from unittest import skipUnless
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import resolve
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from ads import views
from ads.events import record_ad_event
from ads.services import choose_ad
from ads.context_projection import (
    _read_handoff_context, _save_context_checkpoint, export_context_handoff,
    make_context_document, normalize_snapshot, project_context_file,
)
from ads.exporting import write_ndjson
from ads.lake_files import build_current, build_history, stable_json
from ads.management.commands.demo_player_lake import fixture_change


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


@override_settings(MEDIA_KEYS={"village-game": "test-only-key"})
class ContextApiTests(SimpleTestCase):
    def post_context(self, body=None, **headers):
        payload = body if body is not None else {
            "subject": {"media_id": "village-game", "subject_id": "12"}}
        auth = {"HTTP_X_MEDIA_ID": "village-game", "HTTP_X_MEDIA_KEY": "test-only-key"}
        auth.update(headers)
        return self.client.post("/api/media/context/", data=json.dumps(payload),
                                content_type="application/json", **auth)

    def test_subject_only_payload_and_all_media_routes(self):
        for path, view in (("context", views.context_view),
                           ("decision", views.decision_view), ("events", views.event_view)):
            self.assertIs(resolve(f"/api/media/{path}/").func, view)
        context = {"player_id": "12", "room_id": "room-01", "coins": 26,
                   "version": 461, "updated_at": "2026-10-13T06:36:55+00:00"}
        with patch("ads.views.get_context", return_value=context) as lookup:
            response = self.post_context()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["context"], context)
        self.assertEqual(response.json()["subject"]["subject_id"], "12")
        self.assertEqual(response["Cache-Control"], "no-store")
        lookup.assert_called_once_with("village-game", "12")

    def test_invalid_headers_and_cross_media_subject_never_lookup(self):
        for headers in ({"HTTP_X_MEDIA_KEY": ""}, {"HTTP_X_MEDIA_ID": ""},
                        {"HTTP_X_MEDIA_ID": "other"}, {"HTTP_X_MEDIA_KEY": "wrong"}):
            with self.subTest(headers=headers), patch("ads.views.get_context") as lookup:
                self.assertEqual(self.post_context(**headers).status_code, 401)
                lookup.assert_not_called()
        with patch("ads.views.get_context") as lookup:
            response = self.post_context({"subject": {"media_id": "other", "subject_id": "12"}})
        self.assertEqual(response.status_code, 400)
        lookup.assert_not_called()

    def test_legacy_top_level_media_id_remains_checked(self):
        body = {"media_id": "village-game",
                "subject": {"media_id": "village-game", "subject_id": "12"}}
        with patch("ads.views.get_context", return_value={}):
            self.assertEqual(self.post_context(body).status_code, 200)
        body["media_id"] = "other"
        with patch("ads.views.get_context") as lookup:
            self.assertEqual(self.post_context(body).status_code, 401)
            lookup.assert_not_called()

    def test_method_rejection_is_json_and_has_allow(self):
        response = self.client.get("/api/media/context/")
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response["Allow"], "POST")
        self.assertEqual(response.json(), {"error": "method_not_allowed"})

    def test_empty_context_and_store_outage_are_distinct(self):
        with patch("ads.views.get_context", return_value={}):
            response = self.post_context()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["context"], {})
        with patch("ads.views.get_context", side_effect=PyMongoError("private failure")):
            response = self.post_context()
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"error": "ads_unavailable"})


class ContextHandoffTests(SimpleTestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)
        self.source = self.folder / "input.ndjson"
        self.checkpoint = self.folder / "checkpoint.json"
        self.target = self.folder / "bundle"
        self.public_rows = [
            {"schema_version": "player-snapshot/v1", "source_kind": "player-snapshot",
             "captured_at": "2026-10-14T00:00:00+00:00", "id": player_id,
             "room_id": "room-01", "coins": 26, "version": 461,
             "updated_at": "2026-10-13T06:36:55+00:00"}
            for player_id in (1, 2)
        ]
        self.changes = [normalize_snapshot(row) for row in self.public_rows]
        self.checksum = write_ndjson(self.source, self.changes)
        self.state = _save_context_checkpoint(self.checkpoint, self.checksum, len(self.changes))
        self.fixture = {"schema_version": "player-context-change/v1",
                        "source_kind": "teaching-fixture", "media_id": "village-game",
                        "subject_id": "fixture-handoff", "op": "delete", "version": 3,
                        "event_time": "2026-10-14T00:00:00+00:00", "context": {}}
        canonical = json.dumps(self.fixture, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self.fixture["change_id"] = hashlib.sha256(canonical.encode()).hexdigest()
        self.documents = [make_context_document(row) for row in self.changes + [self.fixture]]
        self.database = Mock()
        self.database.player_context.find.return_value.sort.return_value = self.documents

    def test_four_files_preserve_input_and_replay_has_no_writes(self):
        original_source, original_checkpoint = self.source.read_bytes(), self.checkpoint.read_bytes()
        with patch("ads.context_projection.get_db", return_value=self.database):
            manifest = export_context_handoff(self.source, self.checkpoint, self.target)
        self.assertEqual({p.name for p in self.target.iterdir()}, {
            "player-context-changes.ndjson", "checkpoint.json", "player-context.ndjson", "manifest.json"})
        self.assertEqual(self.source.read_bytes(), original_source)
        self.assertEqual(self.checkpoint.read_bytes(), original_checkpoint)
        self.assertEqual(Path(manifest["input_path"]).read_bytes(), original_source)
        self.assertEqual(manifest["input_sha256"], self.checksum)
        self.assertEqual(manifest["context_sha256"], hashlib.sha256(
            Path(manifest["context_path"]).read_bytes()).hexdigest())
        self.assertEqual(json.loads((self.target / "manifest.json").read_text()), manifest)
        self.assertEqual(manifest["input_rows"], 2)
        self.assertEqual(manifest["context_rows"], 3)
        self.assertEqual(manifest["context_source_kind_counts"], {
            "player-snapshot": 2, "teaching-fixture": 1})
        self.database.player_context.find.assert_called_once_with({"media_id": "village-game"})
        with patch("ads.context_projection.apply_context") as apply:
            replay = project_context_file(manifest["input_path"], manifest["checkpoint_path"])
        self.assertEqual(replay["processed"], 0)
        self.assertTrue(replay["done"])
        apply.assert_not_called()

    def test_existing_destination_is_not_overwritten(self):
        self.target.mkdir()
        sentinel = self.target / "existing.txt"
        sentinel.write_text("keep")
        with patch("ads.context_projection.get_db") as database, self.assertRaisesRegex(ValueError, "새 인계"):
            export_context_handoff(self.source, self.checkpoint, self.target)
        database.assert_not_called()
        self.assertEqual(sentinel.read_text(), "keep")
        self.assertEqual(list(self.target.iterdir()), [sentinel])

    def test_wrong_or_incomplete_checkpoint_never_creates_output(self):
        for state in ({**self.state, "next_line": 1},
                      {**self.state, "source_sha256": "0" * 64},
                      {**self.state, "next_line": True}):
            self.checkpoint.write_text(json.dumps(state))
            with self.subTest(state=state), patch("ads.context_projection.get_db") as database:
                with self.assertRaises(ValueError):
                    export_context_handoff(self.source, self.checkpoint, self.target)
                database.assert_not_called()
                self.assertFalse(self.target.exists())

    def test_only_selected_media_player_snapshot_input_is_exported(self):
        other = normalize_snapshot(self.public_rows[0], media_id="other-media")
        for changes in ([other], [self.fixture]):
            checksum = write_ndjson(self.source, changes)
            _save_context_checkpoint(self.checkpoint, checksum, len(changes))
            with self.subTest(changes=changes), patch("ads.context_projection.get_db") as database:
                with self.assertRaisesRegex(ValueError, "지정 매체"):
                    export_context_handoff(self.source, self.checkpoint, self.target)
                database.assert_not_called()
                self.assertFalse(self.target.exists())

    def test_public_document_key_type_and_digest_are_checked(self):
        original = self.documents[0]
        for row in ({**original, "_id": "wrong"}, {**original, "deleted": 1},
                    {**original, "change_id": "0" * 64}, {**original, "private": "excluded"}):
            self.database.player_context.find.return_value.sort.return_value = [row]
            with self.subTest(row=row), patch("ads.context_projection.get_db", return_value=self.database):
                with self.assertRaises(ValueError):
                    _read_handoff_context("village-game")

    def test_changed_copy_is_rejected_without_publishing_partial_bundle(self):
        def changed_copy(source, destination):
            Path(destination).write_bytes(b"changed\n")
        before = self.source.read_bytes(), self.checkpoint.read_bytes()
        with patch("ads.context_projection.get_db", return_value=self.database), \
                patch("ads.context_projection.shutil.copyfile", side_effect=changed_copy):
            with self.assertRaisesRegex(ValueError, "복사 중"):
                export_context_handoff(self.source, self.checkpoint, self.target)
        self.assertFalse(self.target.exists())
        self.assertEqual(before, (self.source.read_bytes(), self.checkpoint.read_bytes()))
        self.assertFalse(list(self.folder.glob(".handoff-*")))

    def test_command_exports_and_reports_existing_target_as_command_error(self):
        output = StringIO()
        with patch("ads.context_projection.get_db", return_value=self.database):
            call_command("export_context_handoff", source=str(self.source), checkpoint=str(self.checkpoint),
                         output_dir=str(self.target), media_id="village-game", stdout=output)
        self.assertEqual(json.loads(output.getvalue())["checkpoint"]["next_line"], 2)
        from django.core.management.base import CommandError
        with self.assertRaises(CommandError):
            call_command("export_context_handoff", source=str(self.source), checkpoint=str(self.checkpoint),
                         output_dir=str(self.target), media_id="village-game", stdout=StringIO())


class PlayerLakeTests(SimpleTestCase):
    def test_history_repeated_reversed_and_equal_time_rows_are_deterministic(self):
        rows = [fixture_change(4, 40), fixture_change(1), fixture_change(2, 20), fixture_change(2, 21)]
        before = copy.deepcopy(rows)
        history = build_history(rows)
        self.assertEqual(len(history), 4)
        self.assertEqual(history, build_history(list(reversed(rows)) * 2))
        self.assertEqual([row["version"] for row in history], [1, 2, 2, 4])
        self.assertEqual([row["change_id"] for row in history[1:3]],
                         sorted(row["change_id"] for row in history[1:3]))
        self.assertEqual(rows, before)
        self.assertEqual(stable_json({"b": "숲", "a": 1}), stable_json({"a": 1, "b": "숲"}))

    def test_schema_and_content_hash_are_validated_before_results(self):
        original = fixture_change(1)
        wrong_schema = {**original, "schema_version": "ad-event/v1"}
        wrong_hash = fixture_change(1, 99)
        wrong_hash["change_id"] = original["change_id"]
        for row in (wrong_schema, wrong_hash):
            with self.subTest(row=row), self.assertRaises(ValueError):
                build_history([original, row])

    def test_current_chooses_highest_version_and_preserves_input(self):
        rows = [fixture_change(1), fixture_change(4, 40), fixture_change(2, 20)]
        before = copy.deepcopy(rows)
        current = build_current(rows)
        self.assertEqual(len(current), 1)
        self.assertEqual(current[0]["schema_version"], "player-current/v1")
        self.assertEqual(len(current[0]), 10)
        self.assertEqual(current[0]["_id"], "village-game:fixture-lake")
        self.assertEqual(current[0]["version"], 4)
        self.assertEqual(current[0]["context"]["coins"], 40)
        self.assertEqual(current, build_current(list(reversed(rows)) * 2))
        self.assertEqual(rows, before)

    def test_latest_tombstone_cannot_be_revived_by_old_upsert(self):
        current = build_current([fixture_change(4, op="delete"), fixture_change(2, 20)])
        self.assertEqual(current[0]["version"], 4)
        self.assertTrue(current[0]["deleted"])
        self.assertEqual(current[0]["context"], {})

    def test_same_version_conflict_and_next_call_are_isolated(self):
        with self.assertRaisesRegex(ValueError, "same subject/version"):
            build_current([fixture_change(4, 40), fixture_change(4, 99)])
        self.assertEqual(build_current([fixture_change(4, 40)])[0]["context"]["coins"], 40)
        self.assertEqual(build_history([]), [])
        self.assertEqual(build_current([]), [])

    def test_media_are_distinct_and_provenance_ties_are_stable(self):
        first = fixture_change(4, op="delete")
        other = copy.deepcopy(first)
        other["media_id"] = "other-media"
        body = {key: value for key, value in other.items() if key != "change_id"}
        other["change_id"] = hashlib.sha256(stable_json(body).encode()).hexdigest()
        current = build_current([first, other])
        self.assertEqual([row["_id"] for row in current],
                         ["other-media:fixture-lake", "village-game:fixture-lake"])
        later = copy.deepcopy(first)
        later["event_time"] = "2026-10-14T00:01:04+00:00"
        body = {key: value for key, value in later.items() if key != "change_id"}
        later["change_id"] = hashlib.sha256(stable_json(body).encode()).hexdigest()
        self.assertEqual(build_current([first, later]), build_current([later, first]))
        self.assertEqual(build_current([first, later])[0]["change_id"],
                         min(first["change_id"], later["change_id"]))

    def test_preview_command_checks_manifest_checkpoint_and_preserves_files(self):
        from django.core.management.base import CommandError
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, checkpoint, manifest_path = root / "input.ndjson", root / "checkpoint.json", root / "manifest.json"
            row = normalize_snapshot({"schema_version": "player-snapshot/v1", "source_kind": "player-snapshot",
                                      "captured_at": "2026-10-14T00:00:00+00:00", "id": 1,
                                      "room_id": "room-01", "coins": 26, "version": 461,
                                      "updated_at": "2026-10-13T06:36:55+00:00"})
            checksum = write_ndjson(source, [row])
            _save_context_checkpoint(checkpoint, checksum, 1)
            manifest = {"input_sha256": checksum, "input_rows": 1,
                        "input_schema_version": "player-context-change/v1", "source_kind": "player-snapshot",
                        "media_id": "village-game", "checkpoint_path": str(checkpoint)}
            manifest_path.write_text(json.dumps(manifest))
            before = [path.read_bytes() for path in (source, checkpoint, manifest_path)]
            output = StringIO()
            with patch("ads.context_projection.get_db") as database:
                call_command("inspect_player_lake", source=str(source), manifest=str(manifest_path),
                             stage="current", repeat=2, reverse=True, stdout=output)
                database.assert_not_called()
            result = json.loads(output.getvalue())
            self.assertEqual([result[key] for key in ("input_rows", "supplied_rows", "history_rows", "result_rows")],
                             [1, 2, 1, 1])
            self.assertFalse(result["written"])
            self.assertEqual(before, [path.read_bytes() for path in (source, checkpoint, manifest_path)])
            _save_context_checkpoint(checkpoint, checksum, 0)
            with self.assertRaisesRegex(CommandError, "완료되지"):
                call_command("inspect_player_lake", source=str(source), manifest=str(manifest_path), stdout=StringIO())
            _save_context_checkpoint(checkpoint, checksum, 1)
            manifest["input_sha256"] = "0" * 64
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(CommandError, "manifest"):
                call_command("inspect_player_lake", source=str(source), manifest=str(manifest_path), stdout=StringIO())

    def test_demo_observes_duplicates_delete_conflict_and_empty_without_db(self):
        from django.core.management.base import CommandError
        for case, expected_history, expected_current in (("duplicates", 2, 0), ("versions", 3, 1),
                                                        ("delete", 2, 1), ("empty", 0, 0)):
            output = StringIO()
            with self.subTest(case=case), patch("ads.context_projection.get_db") as database:
                call_command("demo_player_lake", case=case, stdout=output)
                database.assert_not_called()
            result = json.loads(output.getvalue())
            self.assertEqual((result["history_rows"], result["current_rows"]), (expected_history, expected_current))
            self.assertFalse(result["written"])
            self.assertFalse(result["database_changed"])
        for case in ("invalid-schema", "change-id-conflict", "version-conflict"):
            output = StringIO()
            with self.subTest(case=case), self.assertRaises(CommandError):
                call_command("demo_player_lake", case=case, stdout=output)
            self.assertEqual(output.getvalue(), "")
