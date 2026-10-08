import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

# 기존 작업 폴더의 .env를 읽고 연결 객체를 만든다.
# 현재 작업환경: 기존 ads.env를 읽고 루트 .env가 있으면 덮어 읽는다.
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / "ads.env", override=True)
load_dotenv(ROOT / ".env", override=True)
uri = os.environ["MONGO_URI"]
database_name = os.environ.get("MONGO_DB", "village_ads")
print("database", database_name)
client = MongoClient(uri)

# 데이터베이스와 연습 컬렉션을 선택한다.
database = client[database_name]
collection = database["practice_campaigns"]
print("collection", collection.name)
print("server", client.admin.command("ping")["ok"])
client.close()
print("closed")
