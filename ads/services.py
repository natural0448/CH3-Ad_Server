import uuid
from datetime import datetime, timezone
from copy import deepcopy
from .mongo import get_db
from .repository import VALID_SLOTS, validate_id


def clean_subject(subject):
    if (not isinstance(subject, dict) or set(subject) != {"media_id", "subject_id"}
            or any(not isinstance(subject[name], str) or not subject[name]
                   for name in ("media_id", "subject_id"))):
        raise ValueError("subject_invalid")
    return {"media_id": subject["media_id"], "subject_id": subject["subject_id"]}


def choose_ad(media_id, subject_id, slot_id, context):
    validate_id(media_id, "매체 ID")
    validate_id(subject_id, "대상 ID")
    if not isinstance(slot_id, str) or slot_id not in VALID_SLOTS or not isinstance(context, dict):
        raise ValueError("게시 위치와 맥락을 확인하세요.")
    db = get_db()
    candidates, creatives = [], {}
    # 활성 캠페인과 같은 소유자의 입찰만 후보로 만든다.
    for campaign in db["campaigns"].find({"slot_id": slot_id, "active": True}):
        bid = db["bids"].find_one({"_id": campaign["campaign_id"],
                                    "owner_user_id": campaign["owner_user_id"]})
        if not bid or type(bid.get("bid_amount")) is not int:
            continue
        if not 1 <= bid["bid_amount"] <= 10000:
            continue
        campaign_id = campaign["campaign_id"]
        candidates.append({"campaign_id": campaign_id,
                           "owner_user_id": campaign["owner_user_id"],
                           "bid_amount": bid["bid_amount"]})
        creatives[campaign_id] = {
            "title": campaign["title"], "body": campaign.get("body", ""),
            "creative_path": campaign.get("creative_path", ""),
        }
    candidates.sort(key=lambda row: (-row["bid_amount"], row["campaign_id"]))
    chosen = candidates[0] if candidates else None
    decision_id = str(uuid.uuid4())
    selected_at = datetime.now(timezone.utc)
    # 현재 값을 복사해 선택 당시의 근거를 보존한다.
    decision = {
        "_id": decision_id, "schema_version": "ad-decision/v1",
        "decision_id": decision_id,
        "event_time": selected_at.isoformat(), "selected_at": selected_at,
        "owner_user_id": chosen["owner_user_id"] if chosen else None,
        "media_id": media_id, "subject": {"media_id": media_id, "subject_id": subject_id},
        "slot_id": slot_id, "context": deepcopy(context), "candidates": candidates,
        "chosen_campaign_id": chosen["campaign_id"] if chosen else None,
        "chosen_bid_amount": chosen["bid_amount"] if chosen else None,
        "creative": creatives[chosen["campaign_id"]] if chosen else None,
        "policy_version": "highest-bid/v1",
    }
    db["decisions"].insert_one(decision)
    return decision
