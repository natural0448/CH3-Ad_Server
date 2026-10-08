import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

# 기존 작업 폴더의 .env에서 연습 컬렉션만 선택한다.
# 현재 작업환경: 기존 ads.env를 읽고 루트 .env가 있으면 덮어 읽는다.
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / "ads.env", override=True)
load_dotenv(ROOT / ".env", override=True)
client = MongoClient(os.environ["MONGO_URI"])
database = client[os.environ.get("MONGO_DB", "village_ads")]
collection = database["practice_campaigns"]
print("collection", collection.name)

# 연습 문서 한 건을 생성하고 전체·선택 필드를 조회한다.
document = {
    "_id": "practice-campaign",
    "priority": 1,
    "creative": {
        "headline": "연습용 지도 안내",
        "body": "숲 지도를 살펴보세요.",
    },
}
inserted = collection.insert_one(document)
print("inserted", inserted.inserted_id)
print("whole", collection.find_one({"_id": "practice-campaign"}))
print("selected", collection.find_one(
    {"_id": "practice-campaign"},
    {"_id": 0, "creative.headline": 1, "priority": 1},
))

# 본문 한 필드만 바꾸고 수정 결과를 읽는다.
result = collection.update_one(
    {"_id": "practice-campaign"},
    {"$set": {"creative.body": "지도를 펼쳐 숲 입구를 찾아보세요."}}
)
print("matched", result.matched_count, "modified", result.modified_count)
print("changed", collection.find_one(
    {"_id": "practice-campaign"},
    {"_id": 0, "creative.headline": 1, "creative.body": 1},
))

# 숫자와 같은 ID를 다시 읽은 뒤 연습 문서만 삭제한다.
collection.update_one({"_id": "practice-campaign"}, {"$set": {"priority": 3}})
print("priority", collection.find_one({"_id": "practice-campaign"})["priority"])
deleted = collection.delete_one({"_id": "practice-campaign"})
print("deleted", deleted.deleted_count,
      "remaining", collection.count_documents({"_id": "practice-campaign"}))
client.close()
