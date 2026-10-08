# ads/mongo.py

lru_cache(maxsize=1)로 MongoClient를 재사용한다. 서버 선택/접속 제한은 각각 3000ms, appname=village-ads다. URI/DB 이름은 settings에서 읽는다. atexit는 이미 생성한 연결만 닫는다. get_db 선택 자체는 저장/실제 연결 성공의 증거가 아니다.

## get_client()

파라미터 없음.

데코레이터: lru_cache(maxsize=1).

반환·실패: MongoClient.

의사코드: 캐시 → 없으면 설정 URI로 MongoClient → 재사용.

직접 호출: MongoClient, lru_cache. MongoClient는 지연 연결 클라이언트를 생성하고 Database 선택은 공유 클라이언트의 DB 핸들을 반환한다. close와 cache_clear는 연결·캐시를 해제한다.

## get_db()

파라미터 없음.

반환·실패: Database.

의사코드: get_client → 설정 MONGO_DB 선택.

직접 호출: get_client. MongoClient는 지연 연결 클라이언트를 생성하고 Database 선택은 공유 클라이언트의 DB 핸들을 반환한다. close와 cache_clear는 연결·캐시를 해제한다.

## close_client()

파라미터 없음.

반환·실패: None.

의사코드: 캐시가 있으면 close → cache_clear.

직접 호출: get_client, get_client().close, get_client.cache_clear, get_client.cache_info. MongoClient는 지연 연결 클라이언트를 생성하고 Database 선택은 공유 클라이언트의 DB 핸들을 반환한다. close와 cache_clear는 연결·캐시를 해제한다.

## 변수·상수의 출처

lru_cache(maxsize=1)로 MongoClient를 재사용한다. 서버 선택/접속 제한은 각각 3000ms, appname=village-ads다. URI/DB 이름은 settings에서 읽는다. atexit는 이미 생성한 연결만 닫는다. get_db 선택 자체는 저장/실제 연결 성공의 증거가 아니다.

지역 입력은 함수 인자/요청/CLI/환경 설정에서 오고 해당 함수가 작성한다. 연결은 공유 cache, 소유자는 Django 세션, ID/시간은 uuid4/UTC에서 생성한다. 테스트 값은 임시 계정/테스트 DB에서만 사용한다. secrets·password·cookie·token 실제 값은 문서에 복사하지 않는다.
