# tools/day22_connection.py

## 22일차·23일차2교시 교안기준 최종 구현

22일차1교시연결완성 code block23. 최상위순서=환경→DB이름→MongoClient→database→practice_campaigns→이름/핑출력→close/closed. ROOT=Path(__file__).resolve().parents[1]로기존ad_server를찾고ads.env뒤root.env만읽는부분을현재환경에적응했다. uri는MONGO_URI, database_name은MONGO_DB 또는기존기본village_ads, client/database/collection은선택객체다. 문서를저장하지않는다. Django설정/import가필요없는독립실습이다.
