from ads.mongo import get_db
from ads.events import record_ad_event
from pprint import pprint

db = get_db()

# 최근 광고 결정 10건을 출력한다.
decisions = list(
    db.decisions.find(
        {"chosen_campaign_id": {"$nin": [None, ""]}}
    ).sort("_id", -1).limit(10)
)

for number, row in enumerate(decisions):
    pprint({
        "번호": number,
        "decision_id": row["_id"],
        "subject": row["subject"],
        "campaign_id": row["chosen_campaign_id"],
        "slot_id": row["slot_id"],
        "event_time": row.get("event_time"),
    })

# Pygame에 실제 표시된 광고의 결정 ID와 일치하는 번호를 입력한다.
# 화면에서 ID를 확인할 수 없다면 여기서 중단한다.
number = int(input("실제 표시된 decision_id와 일치하는 번호: "))
decision = decisions[number]

decision_id = decision["_id"]
subject = decision["subject"]

print("decision_id:", decision_id)
print("subject:", subject)

print(record_ad_event(subject, decision_id, "impression"))
print(record_ad_event(subject, decision_id, "impression"))