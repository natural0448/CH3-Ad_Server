from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from pymongo.errors import PyMongoError

from .repository import list_bids, list_campaigns, save_bid, save_campaign
from .services import choose_ad
from .creatives import CREATIVES
from .events import record_ad_event
from .media_auth import media_api_methods
from .mongo import get_db


@login_required
@require_http_methods(["GET", "POST"])
def campaign_view(request):
    message, status, campaigns = "", 200, []
    try:
        if request.method == "POST":
            save_campaign(request.user.id, request.POST)
            message = "캠페인을 저장했습니다."
        campaigns = list_campaigns(request.user.id)
    except ValueError as exc:
        message, status = str(exc), 400
    except PyMongoError:
        message, status = "MongoDB에 연결할 수 없습니다.", 503
    form_campaign = next((row for row in campaigns if row["campaign_id"] == request.GET.get("edit")), None)
    if request.method == "POST" and status != 200:
        form_campaign = {name: request.POST.get(name, "") for name in
                         ("campaign_id", "title", "body", "slot_id", "creative_path")}
        form_campaign["active"] = request.POST.get("active") == "on"
    return render(request, "ads/campaigns.html",
                  {"campaigns": campaigns, "message": message,
                   "form_campaign": form_campaign, "creatives": CREATIVES}, status=status)


@login_required
@require_http_methods(["GET", "POST"])
def bid_view(request):
    message, status, bids = "", 200, []
    try:
        if request.method == "POST":
            save_bid(request.user.id, request.POST.get("campaign_id", ""),
                     request.POST.get("bid_amount", ""))
            message = "입찰을 저장했습니다."
        bids = list_bids(request.user.id)
    except ValueError as exc:
        message, status = str(exc), 400
    except PyMongoError:
        message, status = "MongoDB에 연결할 수 없습니다.", 503
    return render(request, "ads/bids.html",
                  {"bids": bids, "message": message}, status=status)


@media_api_methods("POST")
def decision_view(request):
    try:
        payload, subject = request.media_body, request.subject
        media_id = subject["media_id"]
        decision = choose_ad(media_id, subject.get("subject_id"),
                             payload.get("slot_id"), payload.get("context", {}))
        if decision["chosen_campaign_id"] is None:
            return JsonResponse({"ad": None, "empty": True,
                                 "policy_version": decision["policy_version"]})
        return JsonResponse({
            "empty": False,
            "decision_id": decision["decision_id"],
            "campaign_id": decision["chosen_campaign_id"],
            "title": decision["creative"]["title"], "body": decision["creative"]["body"],
            "slot_id": decision["slot_id"], "bid_amount": decision["chosen_bid_amount"],
            "bid_units": decision["chosen_bid_amount"],
            "creative_path": decision["creative"].get("creative_path", ""),
            "policy_version": decision["policy_version"],
        })
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error": "JSON 입력과 필드 값을 확인하세요."}, status=400)
    except PyMongoError:
        return JsonResponse({"error": "MongoDB에 연결할 수 없습니다."}, status=503)


@media_api_methods("POST")
def event_view(request):
    result = record_ad_event(
        request.subject,
        request.media_body.get("decision_id"),
        request.media_body.get("event_type"),
    )
    response = JsonResponse(result)
    response["Cache-Control"] = "no-store"
    return response


@login_required(login_url="/accounts/login/")
@require_http_methods(["GET"])
def advertiser_event_view(request):
    try:
        decisions = list(get_db().decisions.find(
            {"owner_user_id": request.user.pk}
        ).sort("selected_at", -1).limit(30))
        rows = []
        for decision in decisions:
            decision_id = decision["_id"]
            rows.append({
                "decision_id": decision_id,
                "campaign_id": decision.get("chosen_campaign_id", decision.get("campaign_id")),
                "bid_amount": decision.get("chosen_bid_amount", decision.get("bid_units")),
                "selected_at": decision.get("selected_at"),
                "snapshot_ready": bool(decision.get("chosen_campaign_id")),
                "impression": get_db().ad_events.find_one({"_id": decision_id + ":impression"}),
                "click": get_db().ad_events.find_one({"_id": decision_id + ":click"}),
            })
        return render(request, "ads/events.html", {"rows": rows})
    except PyMongoError:
        return render(request, "ads/events.html", {
            "rows": [], "message": "광고 실적 저장소에 연결할 수 없습니다."}, status=503)
