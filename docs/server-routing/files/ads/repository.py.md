# ads/repository.py

광고주 소유 캠페인과 캠페인당 현재 입찰 한 건을 관리한다. VALID_SLOTS={village-board,lobby-banner}; ID는 [a-z0-9_-]{1,40}. 제목 trim 후1..80자, 본문0..300자이며 이미지 경로가 없으면 빈 본문은 거부한다. active는 입력 on일 때True. campaign _id=campaign_id, owner_user_id는 최초 쓰기에서 고정한다. bid_amount는 ASCII 숫자 문자열/정수 검증 후 int1..10000; updated_at은 서버 UTC ISO 문자열이다. 수정23일차1교시에서 save_bid의 마지막 반환은 저장한 bids 문서 조회다. 기존 검증·소유자 필터와 스키마를 유지한다.

직접 호출의 기대 계약: get_db는 기존 Database, find_one은 dict/None, find·sort·limit는 Cursor, update_one은 UpdateResult, insert_one은 InsertOneResult, create_index는 색인 이름이다. Django render/JsonResponse는 HttpResponse, JSON parse는 dict 등 JSON 값, urlopen은 응답 stream, patch/assert는 테스트 fixture/검증을 제공한다. 하위 계층 내부는 해당 짝 문서에 있다.

## `validate_id(value, label='ID')`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| value | 없음 | 검사할 공개 ID 문자열. |
| label | 'ID' | ID 오류 안내 이름 문자열. |

반환·실패: 검증한 str 또는 ValueError.

의사코드: 문자열·정규식 검사 → value 반환.

직접 호출: `ValueError`, `isinstance`, `re.fullmatch`.

## `get_campaign(campaign_id)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| campaign_id | 없음 | 캠페인 ID 문자열; 쓰기 경로는 [a-z0-9_-]{1,40}. |

반환·실패: dict 또는 None.

의사코드: campaigns의 _id로 단일 조회.

직접 호출: `get_db`, `get_db()['campaigns'].find_one`.

## `list_campaigns(owner_user_id)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| owner_user_id | 없음 | 광고주 Django User의 정수 pk. |

반환·실패: list[dict].

의사코드: owner_user_id로 campaigns 조회 → campaign_id 순 정렬 → list.

직접 호출: `get_db`, `get_db()['campaigns'].find`, `get_db()['campaigns'].find({'owner_user_id': owner_user_id}).sort`, `list`.

## `save_campaign(owner_user_id, data)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| owner_user_id | 없음 | 광고주 Django User의 정수 pk. |
| data | 없음 | 캠페인 입력 mapping 또는 HTMLParser 문자 데이터. |

반환·실패: None 또는 ValueError/PyMongoError.

의사코드: 입력/소재/소유자 검사 → 값 구성 → 소유자 조건 upsert → 중복 ID는 입력 오류.

직접 호출: `ValueError`, `body.strip`, `data.get`, `datetime.now`, `datetime.now(timezone.utc).isoformat`, `get_db`, `get_db()['campaigns'].update_one`, `isinstance`, `len`, `title.strip`, `validate_creative`, `validate_id`.

## `list_bids(owner_user_id)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| owner_user_id | 없음 | 광고주 Django User의 정수 pk. |

반환·실패: list[dict].

의사코드: owner_user_id로 bids 조회 → campaign_id 정렬 → list.

직접 호출: `get_db`, `get_db()['bids'].find`, `get_db()['bids'].find({'owner_user_id': owner_user_id}).sort`, `list`.

## `save_bid(owner_user_id, campaign_id, bid_amount)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| owner_user_id | 없음 | 광고주 Django User의 정수 pk. |
| campaign_id | 없음 | 캠페인 ID 문자열; 쓰기 경로는 [a-z0-9_-]{1,40}. |
| bid_amount | 없음 | 정수 또는 ASCII 숫자 문자열;1..10000. |

반환·실패: 저장된 bids dict(조회 결과는 dict/None); ValueError/PyMongoError.

의사코드: ID/금액/소유자/활성 검사 → 소유자 조건 bids upsert → 같은 _id·소유자 bids 조회 반환.

직접 호출: `ValueError`, `datetime.now`, `datetime.now(timezone.utc).isoformat`, `get_campaign`, `get_db`, `get_db()['bids'].find_one`, `get_db()['bids'].update_one`, `int`, `re.fullmatch`, `str`, `validate_id`.

## 상태·값 출처

지역 변수는 해당 함수가 소유하며 request/입력·서버 설정·DB 조회 또는 위 의사코드의 생성 단계에서 얻는다. 저장 snapshot과 receipt의 쓰기는 서비스/사건 계층이 맡는다. 테스트 연결·patch·가짜 응답은 해당 테스트 클래스만 소유하고 정리한다. 비밀값·쿠키·CSRF 토큰은 문서/증거에 복사하지 않는다.
