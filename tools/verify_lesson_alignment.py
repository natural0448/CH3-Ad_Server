"""Compare classroom source with day 22 and day 23 period 1/2 code blocks."""
import argparse
import ast
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
DEFAULT_DAY22 = Path.home() / "Desktop/22일차 · 광고 플랫폼이 광고주의 광고를 게임 유저에게 집행한다.html"
DEFAULT_DAY23 = Path.home() / "Desktop/현재 ad_server에서 노출·클릭과 광고주 보고서 완성하기.html"


class CodeBlocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_pre = False
        self.current = []
        self.blocks = []

    def handle_starttag(self, tag, attrs):
        if tag == "pre":
            self.in_pre = True
            self.current = []

    def handle_endtag(self, tag):
        if tag == "pre":
            self.in_pre = False
            self.blocks.append("".join(self.current))

    def handle_data(self, data):
        if self.in_pre:
            self.current.append(data)


def read_blocks(path):
    parser = CodeBlocks()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.blocks


def function_ast(code, name):
    tree = ast.parse(code)
    node = next(n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name)
    return ast.dump(node, include_attributes=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day22", type=Path, default=DEFAULT_DAY22)
    parser.add_argument("--day23", type=Path, default=DEFAULT_DAY23)
    parser.add_argument("--output", type=Path, default=ROOT / "docs/server-routing/verification/lesson-alignment/source-comparison.json")
    args = parser.parse_args()
    day22, day23 = read_blocks(args.day22), read_blocks(args.day23)
    results = []

    def compare(day, block, project, relative, name, expected=None, adaptation="none"):
        reference = (day22 if day == 22 else day23)[block]
        actual = (WORKSPACE / project / relative).read_text(encoding="utf-8")
        results.append({"day": day, "code_block": block, "file": project + "/" + relative,
                        "function": name, "adaptation": adaptation,
                        "ok": function_ast(actual, name) == function_ast(expected or reference, name)})

    for name in ("validate_id", "get_campaign", "list_campaigns"):
        compare(22, 50, "ad_server", "ads/repository.py", name)
    compare(22, 59, "ad_server", "ads/repository.py", "list_bids")
    bid = day22[59].rstrip() + '\n    return get_db()["bids"].find_one({"_id": campaign_id, "owner_user_id": owner_user_id})\n'
    compare(22, 59, "ad_server", "ads/repository.py", "save_bid", bid,
            "revised day23 period1 returns the saved bids document using the existing owner filter")
    for name in ("csrf_token", "logout_view"):
        compare(22, 38, "ad_server", "ads/auth_views.py", name)
    compare(22, 37, "ad_server", "ads/mongo.py", "get_db")
    compare(22, 60, "ad_server", "ads/views.py", "bid_view")
    compare(22, 80, "Game-server", "server/game/ad_views.py", "ad_decision")

    # Keep only declared corrections required for the current input/DB boundary.
    events = day23[15].replace('if event_type not in {"impression", "click"}:',
        'if not isinstance(event_type, str) or event_type not in {"impression", "click"}:')
    compare(23, 15, "ad_server", "ads/events.py", "record_ad_event", events,
            "reject non-string JSON type without a 500; all other function statements match v2.3")
    media_view = day23[16].replace('def event(request):', 'def event_view(request):')
    compare(23, 16, "ad_server", "ads/views.py", "event_view", media_view,
            "retain the current media handler name and combined views.py")
    web_view = day23[21].replace('def event_view(request):', 'def advertiser_event_view(request):')
    compare(23, 21, "ad_server", "ads/views.py", "advertiser_event_view", web_view,
            "combined views.py uses a distinct name for the advertiser GET handler")
    service = day22[67].replace('if slot_id not in VALID_SLOTS or',
        'if not isinstance(slot_id, str) or slot_id not in VALID_SLOTS or')
    service = service.replace('creatives[campaign_id] = {"title": campaign["title"], "body": campaign["body"]}',
        'creatives[campaign_id] = {"title": campaign["title"], "body": campaign.get("body", ""), "creative_path": campaign.get("creative_path", "")}')
    service = service.replace('"context": dict(context)', '"context": deepcopy(context)')
    service = service.replace('decision_id = str(uuid.uuid4())',
        'decision_id = str(uuid.uuid4())\n    selected_at = datetime.now(timezone.utc)')
    service = service.replace('"event_time": datetime.now(timezone.utc).isoformat(),',
        '"event_time": selected_at.isoformat(), "selected_at": selected_at,\n        "owner_user_id": chosen["owner_user_id"] if chosen else None,')
    compare(22, 67, "ad_server", "ads/services.py", "choose_ad", service,
            "revised day23 snapshot owner/time; preserve four arguments, image fields and bid_amount schema")
    compare(23, 19, "Game-server", "server/game/ad_views.py", "ad_event", adaptation=
            "retain the current ad_views.py handler and existing game/urls.py route")
    for relative, block in (("config/day23-subject.py", 2), ("config/day23-period-01.py", 3),
                            ("config/day23-period-02.py", 13),
                            ("ads/management/commands/create_ad_indexes.py", 8)):
        actual = (ROOT / relative).read_text(encoding="utf-8")
        results.append({"day": 23, "code_block": block, "file": "ad_server/" + relative,
                        "adaptation": "none",
                        "ok": ast.dump(ast.parse(actual)) == ast.dump(ast.parse(day23[block]))})
    template = (ROOT / "ads/templates/ads/events.html").read_text(encoding="utf-8")
    reference_table = day23[22].split('<div style="overflow-x:auto">')[1].split('</div>')[0].strip()
    actual_table = template.split('<div style="overflow-x:auto">')[1].split('</div>')[0].strip()
    results.append({"day": 23, "code_block": 22, "file": "ad_server/ads/templates/ads/events.html",
                    "adaptation": "existing base template/navigation; future reports link omitted until implemented",
                    "ok": [line.strip() for line in reference_table.splitlines()] ==
                          [line.strip() for line in actual_table.splitlines()]})
    for relative, block in (("tools/day22_connection.py", 23), ("tools/day22_crud.py", 29)):
        expected = day22[block].replace('import os\n', 'import os\nfrom pathlib import Path\n', 1)
        expected = expected.replace('load_dotenv(".env", override=True)',
            'ROOT = Path(__file__).resolve().parents[1]\nload_dotenv(ROOT / "ads.env", override=True)\nload_dotenv(ROOT / ".env", override=True)')
        expected = expected.replace('os.environ["MONGO_DB"]', 'os.environ.get("MONGO_DB", "village_ads")')
        actual = (ROOT / relative).read_text(encoding="utf-8")
        results.append({"day": 22, "code_block": block, "file": "ad_server/" + relative,
                        "adaptation": "existing ads.env/root .env and existing default village_ads",
                        "ok": ast.dump(ast.parse(actual)) == ast.dump(ast.parse(expected))})
    model = ast.parse((ROOT / "tools/basics/day22_credit_model.py").read_text(encoding="utf-8"))
    body = next(n.body for n in model.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    results.append({"day": 22, "code_block": 95, "file": "ad_server/tools/basics/day22_credit_model.py",
                    "adaptation": "existing main entrypoint", "ok":
                    ast.dump(ast.Module(body=body, type_ignores=[])) == ast.dump(ast.parse(day22[95]))})
    failures = [r for r in results if not r["ok"]]
    report = {"scope": "day22 and revised day23 v2.3 period1/2; event list included; no report/export/delivery implementation",
              "sources": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (args.day22, args.day23)},
              "checks": results, "summary": {"ok": not failures, "check_count": len(results)},
              "preexisting_period3_client_mapping": {"ApiClient.post_ad_event": "client/network/session.py:AuthSession.post_ad_event",
                 "Request/Result": "existing dict queue in client/contracts/messages.py",
                 "AdsPanel.apply_event": "client/application/ads.py:AdSlot.accept_event",
                 "ClientController": "client/application/controller.py:Controller",
                 "present/ad_contains": "client/ui/renderer.py and client/ui/input.py using existing Layout.ad_cards"}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Lesson source comparison:", "PASS" if not failures else "FAIL", len(results), "checks")
    for failure in failures:
        print(failure["file"], failure.get("function", "module"))
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
