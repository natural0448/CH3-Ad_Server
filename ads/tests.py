import json
import os
import uuid
from unittest import skipUnless
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from . import mongo, repository, services


class AuthenticationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "test-advertiser"
        cls.password = "test-only-password"
        get_user_model().objects.create_user(
            username=cls.username, password=cls.password,
        )

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True, HTTP_HOST="localhost")

    def csrf_headers(self):
        response = self.client.get("/api/auth/csrf/")
        self.assertEqual(response.status_code, 200)
        return {"HTTP_X_CSRFTOKEN": response.json()["csrfToken"]}

    def test_csrf_cookie_and_get_only_endpoint(self):
        headers = self.csrf_headers()
        self.assertIn("ads_csrftoken", self.client.cookies)
        response = self.client.post("/api/auth/csrf/", **headers)
        self.assertEqual(response.status_code, 405)

    def test_login_requires_csrf(self):
        response = self.client.post(
            "/api/auth/login/",
            data=json.dumps({"username": self.username, "password": self.password}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_invalid_login_bodies_are_rejected(self):
        headers = self.csrf_headers()
        for body, error in [("{", "invalid_json"), ("[]", "invalid_json"),
                            ("{}", "missing_credentials"),
                            ('{"username": 1, "password": "x"}', "missing_credentials")]:
            with self.subTest(body=body):
                response = self.client.post(
                    "/api/auth/login/", data=body,
                    content_type="application/json", **headers,
                )
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json(), {"error": error})

    def test_incorrect_password_is_rejected(self):
        response = self.client.post(
            "/api/auth/login/",
            data=json.dumps({"username": self.username, "password": "incorrect"}),
            content_type="application/json", **self.csrf_headers(),
        )
        self.assertEqual(response.status_code, 401)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_and_logout_use_advertiser_session(self):
        response = self.client.post(
            "/api/auth/login/",
            data=json.dumps({"username": self.username, "password": self.password}),
            content_type="application/json", **self.csrf_headers(),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"authenticated": True})
        self.assertIn("ads_sessionid", self.client.cookies)
        self.assertIn("_auth_user_id", self.client.session)
        response = self.client.post("/api/auth/logout/", **self.csrf_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"authenticated": False})
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_admin_route_is_available(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)

    def test_browser_login_and_protected_pages(self):
        response = self.client.get("/advertiser/campaigns/")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        response = self.client.post("/accounts/login/", {
            "username": self.username, "password": self.password,
        }, **self.csrf_headers())
        self.assertRedirects(response, "/advertiser/campaigns/", fetch_redirect_response=False)

    def test_database_outage_is_a_rendered_503(self):
        self.client.force_login(get_user_model().objects.get(username=self.username))
        with patch("ads.views.list_campaigns", side_effect=PyMongoError("test outage")):
            response = self.client.get("/advertiser/campaigns/")
        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "MongoDB", status_code=503)

    def test_media_authentication_precedes_selection(self):
        with override_settings(MEDIA_KEYS={"village-game": "test-media-key"}), \
                patch("ads.views.choose_ad") as choose:
            response = self.client.post("/api/media/decision/", data=json.dumps({
                "media_id": "village-game", "subject": {"media_id": "village-game", "subject_id": "1"},
                "slot_id": "village-board",
            }), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        choose.assert_not_called()


@skipUnless(os.environ.get("ADS_TEST_MONGO_URI"), "Set ADS_TEST_MONGO_URI for isolated MongoDB integration tests")
class ServingIntegrationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.connection = MongoClient(os.environ["ADS_TEST_MONGO_URI"], serverSelectionTimeoutMS=3000)
        cls.connection.admin.command("ping")
        cls.database = cls.connection["ads_sync_test_" + uuid.uuid4().hex]

    @classmethod
    def tearDownClass(cls):
        try:
            cls.connection.drop_database(cls.database.name)
            cls.connection.close()
        finally:
            super().tearDownClass()

    def setUp(self):
        for name in self.database.list_collection_names():
            self.database[name].delete_many({})
        for target in ["ads.repository.get_db", "ads.services.get_db"]:
            patcher = patch(target, return_value=self.database)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.user = get_user_model().objects.create_user(username="owner")
        self.client = Client(enforce_csrf_checks=True, HTTP_HOST="localhost")
        self.client.force_login(self.user)

    def campaign(self, campaign_id, slot_id="village-board", active="on"):
        repository.save_campaign(self.user.id, {
            "campaign_id": campaign_id, "title": "제목 " + campaign_id,
            "body": "본문", "slot_id": slot_id, "active": active,
        })

    def test_owner_collision_keeps_original_document(self):
        self.campaign("forest-tools")
        original = repository.get_campaign("forest-tools")
        with self.assertRaises(ValueError):
            repository.save_campaign(self.user.id + 1, {
                "campaign_id": "forest-tools", "title": "변조", "body": "변조",
                "slot_id": "village-board", "active": "on",
            })
        self.assertEqual(repository.get_campaign("forest-tools"), original)

    def test_invalid_campaign_fields_do_not_write(self):
        for changes in [{"title": 1}, {"title": " "}, {"body": "x" * 301}, {"slot_id": "other"}, {"slot_id": []}]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                repository.save_campaign(self.user.id, {
                    "campaign_id": "test", "title": "title", "body": "body",
                    "slot_id": "village-board", **changes,
                })
        self.assertEqual(self.database.campaigns.count_documents({}), 0)

    def test_bid_updates_one_document_and_rejects_bad_values(self):
        self.campaign("forest-tools")
        repository.save_bid(self.user.id, "forest-tools", "10")
        saved = repository.save_bid(self.user.id, "forest-tools", "30")
        self.assertEqual(saved, self.database.bids.find_one({"_id": "forest-tools"}))
        self.assertEqual(saved["bid_amount"], 30)
        for amount in ["0", "10001", "1.5", "-1", True, "２０"]:
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                repository.save_bid(self.user.id, "forest-tools", amount)
        self.assertEqual(self.database.bids.count_documents({}), 1)
        self.assertEqual(repository.list_bids(self.user.id)[0]["bid_amount"], 30)

    def test_bid_checks_owner_existence_and_active_status(self):
        self.campaign("inactive", active="")
        self.campaign("active")
        for owner, campaign_id in [(self.user.id, "missing"), (self.user.id, "inactive"),
                                    (self.user.id + 1, "active")]:
            with self.subTest(campaign_id=campaign_id), self.assertRaises(ValueError):
                repository.save_bid(owner, campaign_id, "20")
        self.assertEqual(self.database.bids.count_documents({}), 0)

    def test_bid_owner_collision_is_not_overwritten(self):
        self.campaign("active")
        self.database.bids.insert_one({"_id": "active", "owner_user_id": self.user.id + 1, "bid_amount": 90})
        with self.assertRaises(ValueError):
            repository.save_bid(self.user.id, "active", "20")
        self.assertEqual(self.database.bids.find_one({"_id": "active"})["bid_amount"], 90)

    def test_changed_bid_does_not_change_past_decision(self):
        for campaign_id, amount in [("forest-tools", "10"), ("camp-tea", "20")]:
            self.campaign(campaign_id)
            repository.save_bid(self.user.id, campaign_id, amount)
        first = services.choose_ad("village-game", "viewer-001", "village-board", {})
        repository.save_bid(self.user.id, "forest-tools", "30")
        second = services.choose_ad("village-game", "viewer-001", "village-board", {})
        self.assertEqual((first["chosen_campaign_id"], first["chosen_bid_amount"]), ("camp-tea", 20))
        self.assertEqual((second["chosen_campaign_id"], second["chosen_bid_amount"]), ("forest-tools", 30))
        self.assertNotEqual(first["decision_id"], second["decision_id"])
        stored = self.database.decisions.find_one({"_id": first["decision_id"]})
        self.assertEqual(stored["owner_user_id"], self.user.id)
        self.assertEqual(stored["event_time"], first["event_time"])
        self.assertEqual(stored["selected_at"].isoformat(timespec="milliseconds"),
                         first["selected_at"].replace(tzinfo=None).isoformat(timespec="milliseconds"))
        self.assertEqual({k: v for k, v in stored.items() if k != "selected_at"},
                         {k: v for k, v in first.items() if k != "selected_at"})

    def test_tie_slot_and_invalid_candidate_filtering(self):
        for campaign_id in ["camp-tea", "forest-tools"]:
            self.campaign(campaign_id)
            repository.save_bid(self.user.id, campaign_id, "20")
        self.campaign("lobby", slot_id="lobby-banner")
        repository.save_bid(self.user.id, "lobby", "100")
        self.campaign("malformed")
        self.database.bids.insert_one({"_id": "malformed", "owner_user_id": self.user.id, "bid_amount": True})
        row = services.choose_ad("village-game", "1", "village-board", {})
        self.assertEqual(row["chosen_campaign_id"], "camp-tea")
        self.assertEqual([c["campaign_id"] for c in row["candidates"]], ["camp-tea", "forest-tools"])
        self.assertEqual(services.choose_ad("village-game", "1", "lobby-banner", {})["chosen_campaign_id"], "lobby")

    def test_empty_selection_and_nested_context_snapshot(self):
        context = {"public": {"level": 1}}
        row = services.choose_ad("village-game", "1", "village-board", context)
        context["public"]["level"] = 2
        self.assertIsNone(row["chosen_campaign_id"])
        self.assertEqual(row["context"]["public"]["level"], 1)
        self.assertEqual(self.database.decisions.count_documents({}), 1)
        with self.assertRaises(ValueError):
            services.choose_ad("village-game", "1", "bad-slot", {})
        with self.assertRaises(ValueError):
            services.choose_ad("village-game", "1", [], {})

    def test_web_forms_render_and_save_with_csrf(self):
        response = self.client.get("/advertiser/campaigns/")
        self.assertEqual(response.status_code, 200)
        headers = {"HTTP_X_CSRFTOKEN": self.client.cookies["ads_csrftoken"].value}
        response = self.client.post("/advertiser/campaigns/", {
            "campaign_id": "web", "title": "웹 광고", "body": "내용",
            "slot_id": "village-board", "active": "on",
        }, **headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/advertiser/bids/", {"campaign_id": "web", "bid_amount": "30"}, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "30 포인트")
        self.assertEqual(repository.get_campaign("web")["owner_user_id"], self.user.id)

    def test_media_api_subject_validation_and_response(self):
        self.campaign("selected")
        repository.save_bid(self.user.id, "selected", "30")
        payload = {"media_id": "village-game", "subject": {"media_id": "village-game", "subject_id": "12"},
                   "slot_id": "village-board", "context": {}}
        with override_settings(MEDIA_KEYS={"village-game": "test-media-key"}):
            response = self.client.post("/api/media/decision/", data=json.dumps(payload),
                                        content_type="application/json", HTTP_X_MEDIA_ID="village-game", HTTP_X_MEDIA_KEY="test-media-key")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["campaign_id"], "selected")
            self.assertEqual(response.json()["bid_amount"], 30)
            payload["subject"]["media_id"] = "other"
            response = self.client.post("/api/media/decision/", data=json.dumps(payload),
                                        content_type="application/json", HTTP_X_MEDIA_ID="village-game", HTTP_X_MEDIA_KEY="test-media-key")
            self.assertEqual(response.status_code, 400)
        self.assertEqual(self.database.decisions.count_documents({}), 1)

    def test_media_api_empty_candidate_response(self):
        with override_settings(MEDIA_KEYS={"village-game": "test-media-key"}):
            response = self.client.post("/api/media/decision/", data=json.dumps({
                "media_id": "village-game", "subject": {"media_id": "village-game", "subject_id": "1"},
                "slot_id": "village-board",
            }), content_type="application/json", HTTP_X_MEDIA_ID="village-game", HTTP_X_MEDIA_KEY="test-media-key")
        self.assertEqual(response.json(), {"ad": None, "empty": True, "policy_version": "highest-bid/v1"})
        self.assertEqual(self.database.decisions.count_documents({}), 1)

    def test_shared_mongo_client_connects_and_closes(self):
        mongo.close_client()
        with override_settings(MONGO_URI=os.environ["ADS_TEST_MONGO_URI"], MONGO_DB=self.database.name):
            self.assertIs(mongo.get_client(), mongo.get_client())
            self.assertEqual(mongo.get_db().command("ping")["ok"], 1)
            mongo.close_client()
            self.assertEqual(mongo.get_client.cache_info().currsize, 0)

    def test_image_campaign_and_decision_keep_original_creative(self):
        path = "/static/ads/creatives/forest-tools.png"
        repository.save_campaign(self.user.id, {
            "campaign_id": "image-tools", "title": "숲 도구점", "body": "",
            "slot_id": "village-board", "active": "on", "creative_path": path,
        })
        repository.save_bid(self.user.id, "image-tools", "30")
        decision = services.choose_ad("village-game", "12", "village-board", {})
        repository.save_campaign(self.user.id, {
            "campaign_id": "image-tools", "title": "새 제목", "body": "새 문구",
            "slot_id": "village-board", "active": "on",
            "creative_path": "/static/ads/creatives/camp-tea.png",
        })
        stored = self.database.decisions.find_one({"_id": decision["decision_id"]})
        self.assertEqual(stored["creative"]["creative_path"], path)
        self.assertEqual(stored["creative"]["title"], "숲 도구점")
        with override_settings(MEDIA_KEYS={"village-game": "test-media-key"}):
            response = self.client.post("/api/media/decision/", data=json.dumps({
                "media_id": "village-game", "subject": {"media_id": "village-game", "subject_id": "12"},
                "slot_id": "village-board", "context": {},
            }), content_type="application/json", HTTP_X_MEDIA_ID="village-game", HTTP_X_MEDIA_KEY="test-media-key")
        self.assertEqual(response.json()["creative_path"], "/static/ads/creatives/camp-tea.png")
        self.assertEqual(response.json()["bid_units"], 30)

    def test_image_paths_reject_remote_traversal_and_missing_files(self):
        for path in ["https://example.com/image.png", "/static/ads/creatives/../image.png",
                     "/static/ads/creatives/missing.png", "\\image.png", []]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                repository.save_campaign(self.user.id, {
                    "campaign_id": "invalid-image", "title": "제목", "body": "본문",
                    "slot_id": "village-board", "creative_path": path,
                })
        self.assertEqual(self.database.campaigns.count_documents({}), 0)

    def test_campaign_edit_form_is_owner_scoped_and_contains_preview(self):
        self.campaign("mine")
        repository.save_campaign(self.user.id + 1, {
            "campaign_id": "other", "title": "다른 광고주", "body": "본문",
            "slot_id": "village-board", "active": "on",
        })
        response = self.client.get("/advertiser/campaigns/?edit=mine")
        self.assertContains(response, 'name="creative_path"')
        self.assertContains(response, 'value="mine"')
        self.assertContains(response, 'data-preview-image')
        self.assertNotContains(response, "다른 광고주")
