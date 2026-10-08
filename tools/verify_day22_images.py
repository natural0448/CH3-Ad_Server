"""Verify image-ad HTTP relay and Pygame frames using isolated fixture databases."""
import argparse
import hashlib
import http.cookiejar
import json
import os
import socket
import subprocess
import sys
import time
import uuid
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
REPORT = ROOT / "docs/server-routing/verification/day22-images"


def child(component, owned):
    """Run only a fixture web server or render fixture HTTP results."""
    if component == "render":
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
        sys.path.insert(0, str(WORKSPACE / "Game-client"))
        import pygame
        from client.application.controller import Controller
        from client.configuration import load_config
        from client.ui.layout import build_layout
        from client.ui.renderer import ScreenRenderer

        class Network:
            def submit(self, request):
                return True

        pygame.display.init()
        pygame.font.init()
        pygame.display.set_mode((1100, 880))
        controller = Controller(Network())
        controller.game.apply_identity({"type": "state", "player_id": 12, "room_id": "room-01",
                                        "x": 0, "y": 0, "coins": 0, "version": 0})
        controller.app.phase = "connected"
        renderer = ScreenRenderer(pygame.display.get_surface(), load_config())
        frames = json.loads((owned / "frames.json").read_text(encoding="utf-8"))
        for index, frame in enumerate(frames):
            controller.ads.reset()
            for name, decision in frame.items():
                request = controller.ads.slots[name].request(12, 0)
                png = (owned / Path(decision["creative_path"]).name).read_bytes()
                controller.ads.slots[name].accept({**request, "status": 200, "decision": decision,
                                                  "image_bytes": png, "message": "ready"}, 12)
            receipts = renderer.render(controller.screen_model(), build_layout((1100, 880)), 60)
            assert receipts == {name: data["decision_id"] for name, data in frame.items()}
            controller.ads.mark_displayed(receipts)
            assert all(slot.displayed for slot in controller.ads.slots.values())
            pygame.image.save(renderer.canvas, str(REPORT / f"game-frame-{index + 1}.png"))
        pygame.quit()
        return

    project = ROOT if component == "ad" else WORKSPACE / "Game-server"
    sys.path[:0] = [str(project), str(project / ("ad_config" if component == "ad" else "server"))]
    os.environ["DJANGO_SETTINGS_MODULE"] = "ad_config.settings" if component == "ad" else "config.settings"
    from django.conf import settings
    settings.DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": str(owned / f"{component}.sqlite3")}}
    settings.SECRET_KEY = "isolated-image-validation-only"
    settings.DEBUG = True
    settings.ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
    fixture_key = "isolated-image-validation-only"
    if component == "ad":
        settings.MONGO_URI = "mongodb://127.0.0.1:27109/?replicaSet=ads-image-validation"
        settings.MONGO_DB = "image_validation"
        settings.MEDIA_KEYS = {"village-game": fixture_key}
    else:
        settings.ADS_BASE_URL = "http://127.0.0.1:18001"
        settings.ADS_MEDIA_ID = "village-game"
        settings.ADS_MEDIA_KEY = fixture_key
    import django
    django.setup()
    from django.core.management import call_command
    from django.contrib.auth import get_user_model
    call_command("migrate", verbosity=0, interactive=False)
    user = get_user_model().objects.create_user(
        id=101 if component == "ad" else 202, username=component + "-validation",
        password=os.environ["DAY22_IMAGE_TEST_PASSWORD"])
    if component == "game":
        from game.models import Player
        Player.objects.create(id=12, user=user)
    call_command("runserver", "127.0.0.1:" + ("18001" if component == "ad" else "18000"),
                 use_reloader=False, verbosity=0)


class Web:
    def __init__(self, base, csrf_name="csrftoken"):
        self.base = base
        self.csrf_name = csrf_name
        self.jar = http.cookiejar.CookieJar()
        self.opener = build_opener(HTTPCookieProcessor(self.jar))

    def get(self, path):
        with self.opener.open(self.base + path, timeout=5) as response:
            return response.read()

    def csrf(self):
        return next(cookie.value for cookie in self.jar if cookie.name == self.csrf_name)

    def post(self, path, fields, json_body=False):
        body = json.dumps(fields).encode() if json_body else urlencode(fields).encode()
        request = Request(self.base + path, data=body, headers={
            "Content-Type": "application/json" if json_body else "application/x-www-form-urlencoded",
            "X-CSRFToken": self.csrf(), "Referer": self.base + path})
        with self.opener.open(request, timeout=5) as response:
            return response.read()


def wait_http(url, process):
    opener = build_opener()
    for attempt in range(100):
        if process.poll() is not None:
            raise RuntimeError("Fixture server exited; inspect its runtime log")
        try:
            with opener.open(url, timeout=1):
                return
        except OSError:
            time.sleep(0.15)
    raise RuntimeError("Fixture HTTP server did not start")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mongod")
    parser.add_argument("--component", choices=["ad", "game", "render"])
    parser.add_argument("--owned", type=Path)
    args = parser.parse_args()
    if args.component:
        child(args.component, args.owned)
        return 0
    if not args.mongod:
        parser.error("--mongod is required")
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
    for port in (27109, 18000, 18001):
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", port))
    owned = ROOT / "infra/runtime" / ("day22-images-" + uuid.uuid4().hex)
    owned.mkdir(parents=True)
    assert owned.resolve().is_relative_to((ROOT / "infra/runtime").resolve())
    REPORT.mkdir(parents=True, exist_ok=True)
    processes, logs = [], []
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    env = dict(os.environ, DAY22_IMAGE_TEST_PASSWORD=uuid.uuid4().hex, PYTHONUTF8="1")

    def start(command, name, cwd):
        log = (owned / (name + ".log")).open("w", encoding="utf-8")
        logs.append(log)
        process = subprocess.Popen(command, cwd=cwd, env=env, stdout=log,
                                   stderr=subprocess.STDOUT, creationflags=flags)
        processes.append(process)
        return process

    direct = MongoClient("mongodb://127.0.0.1:27109/?directConnection=true", serverSelectionTimeoutMS=400)
    try:
        mongo = start([args.mongod, "--replSet", "ads-image-validation", "--port", "27109",
                       "--bind_ip", "127.0.0.1", "--dbpath", str(owned)], "mongo", ROOT)
        for attempt in range(100):
            try:
                direct.admin.command("ping")
                break
            except PyMongoError:
                if mongo.poll() is not None:
                    raise RuntimeError("Fixture MongoDB exited")
                time.sleep(0.15)
        else:
            raise RuntimeError("Fixture MongoDB did not start")
        direct.admin.command("replSetInitiate", {"_id": "ads-image-validation", "members": [{"_id": 0, "host": "127.0.0.1:27109"}]})
        for attempt in range(100):
            if direct.admin.command("hello").get("isWritablePrimary"):
                break
            time.sleep(0.15)
        else:
            raise RuntimeError("Fixture MongoDB primary did not become ready")
        ad = start([sys.executable, "-B", __file__, "--component", "ad", "--owned", str(owned)], "ad", ROOT)
        game_root = WORKSPACE / "Game-server"
        game = start([str(game_root / "server/.venv/Scripts/python.exe"), "-B", __file__,
                      "--component", "game", "--owned", str(owned)], "game", game_root)
        wait_http("http://127.0.0.1:18001/accounts/login/", ad)
        wait_http("http://127.0.0.1:18000/api/auth/csrf/", game)
        advertiser, recipient = Web("http://127.0.0.1:18001", "ads_csrftoken"), Web("http://127.0.0.1:18000")
        advertiser.get("/accounts/login/")
        advertiser.post("/accounts/login/", {"username": "ad-validation", "password": env["DAY22_IMAGE_TEST_PASSWORD"]})
        for cid, title, path, slot, amount in (
                ("forest-tools", "숲 도구점", "forest-tools", "village-board", 10),
                ("camp-tea", "모닥불 찻집", "camp-tea", "village-board", 20),
                ("lobby-tea", "모닥불 찻집", "camp-tea", "lobby-banner", 18)):
            advertiser.post("/advertiser/campaigns/", {"campaign_id": cid, "title": title, "body": "마을에서 만나요",
                "creative_path": f"/static/ads/creatives/{path}.png", "slot_id": slot, "active": "on"})
            advertiser.post("/advertiser/bids/", {"campaign_id": cid, "bid_amount": amount})
        recipient.get("/api/auth/csrf/")
        recipient.post("/api/auth/login/", {"username": "game-validation", "password": env["DAY22_IMAGE_TEST_PASSWORD"]}, True)
        frames = []
        for index in range(2):
            if index:
                advertiser.post("/advertiser/bids/", {"campaign_id": "forest-tools", "bid_amount": 30})
            frame = {slot: json.loads(recipient.post("/api/ads/decision/", {"slot_id": slot, "player_id": 999}, True))
                     for slot in ("village-board", "lobby-banner")}
            assert frame["village-board"]["campaign_id"] == ("forest-tools" if index else "camp-tea")
            assert frame["lobby-banner"]["campaign_id"] == "lobby-tea"
            for decision in frame.values():
                png = recipient.get(decision["creative_path"])
                assert png.startswith(b"\x89PNG\r\n\x1a\n")
                (owned / Path(decision["creative_path"]).name).write_bytes(png)
            frames.append(frame)
        db = direct.image_validation
        earlier = db.decisions.find_one({"decision_id": frames[0]["village-board"]["decision_id"]})
        assert earlier["chosen_campaign_id"] == "camp-tea" and earlier["chosen_bid_amount"] == 20
        assert earlier["creative"]["creative_path"].endswith("camp-tea.png")
        assert all(row["subject"]["subject_id"] == "12" for row in db.decisions.find())
        assert all(row["owner_user_id"] == 101 for row in db.campaigns.find())
        (owned / "frames.json").write_text(json.dumps(frames, ensure_ascii=False), encoding="utf-8")
        subprocess.run([str(WORKSPACE / "Game-client/.venv/Scripts/python.exe"), "-B", __file__,
                        "--component", "render", "--owned", str(owned)], cwd=WORKSPACE / "Game-client",
                       env=env, creationflags=flags, check=True, timeout=30)
        browser_script = owned / "browser.cjs"
        browser_script.write_text("""const { chromium } = require(process.env.DAY22_PLAYWRIGHT);
(async () => { const browser = await chromium.launch({channel:'chrome',headless:true});
const page = await browser.newPage({viewport:{width:1360,height:1050}});
await page.goto('http://127.0.0.1:18001/accounts/login/');
await page.locator('input[name=username]').fill('ad-validation');
await page.locator('input[name=password]').fill(process.env.DAY22_IMAGE_TEST_PASSWORD);
await Promise.all([page.waitForURL('**/advertiser/campaigns/'), page.locator('button').click()]);
await page.goto('http://127.0.0.1:18001/advertiser/campaigns/?edit=camp-tea');
await page.locator('[data-preview-image]').evaluate(img => img.decode());
await page.screenshot({path:process.env.DAY22_WEB_SCREENSHOT,fullPage:true});
const game = await browser.newPage({viewport:{width:900,height:820}});
const api = game.context().request;
const csrf = await (await api.get('http://127.0.0.1:18000/api/auth/csrf/')).json();
const login = await api.post('http://127.0.0.1:18000/api/auth/login/', {
  headers:{'X-CSRFToken':csrf.csrfToken},
  data:{username:'game-validation',password:process.env.DAY22_IMAGE_TEST_PASSWORD}});
if (!login.ok()) throw new Error('Fixture login failed');
await game.goto('http://127.0.0.1:18000/ads/preview/');
await game.locator('#request-ad').click();
await game.locator('#ad').waitFor({state:'visible'});
if (await game.locator('#title').innerText() !== '숲 도구점') throw new Error('Wrong first creative');
await game.locator('#slot').selectOption('lobby-banner');
await game.locator('#request-ad').click();
await game.waitForFunction(() => document.querySelector('#title').textContent === '모닥불 찻집');
await game.locator('#creative').evaluate(img => img.decode());
await game.screenshot({path:process.env.DAY22_PREVIEW_SCREENSHOT,fullPage:true});
await browser.close(); })().catch(() => { console.error('Browser verification failed');process.exit(1); });
""", encoding="utf-8")
        runtime = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies"
        node = runtime / "node/bin/node.exe"
        browser_env = dict(env, DAY22_PLAYWRIGHT=str(runtime / "node/node_modules/playwright"),
                           DAY22_WEB_SCREENSHOT=str(REPORT / "advertiser-campaigns.png"),
                           DAY22_PREVIEW_SCREENSHOT=str(REPORT / "game-browser-preview.png"))
        subprocess.run([str(node), str(browser_script)], env=browser_env, creationflags=flags, check=True, timeout=40)
        report = {"scope": "isolated fixture MongoDB, SQLite, HTTP servers and SDL dummy frames",
                  "classroom_databases_modified": False, "actual_student_game_observation": "not_run",
                  "media_key": "synthetic fixture only; no transfer of classroom secret",
                  "checks": {"image_campaign_form": True, "session_player_not_payload": True,
                             "bid_change_switches_image": True, "earlier_snapshot_unchanged": True,
                             "game_origin_png": True, "two_slots_pygame_present": True, "web_browser_render": True},
                  "decisions": frames,
                  "assets": {name: hashlib.sha256((owned / name).read_bytes()).hexdigest()
                             for name in ("forest-tools.png", "camp-tea.png")}}
        (REPORT / "integration.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print("PASS: image campaign -> media API -> authenticated game relay -> PNG -> two Pygame frames")
        print("Report:", REPORT.relative_to(ROOT))
        return 0
    finally:
        for process in reversed(processes):
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=10)
        direct.close()
        for log in logs:
            log.close()
        print("Fixture processes stopped; classroom services unchanged")


if __name__ == "__main__":
    raise SystemExit(main())
