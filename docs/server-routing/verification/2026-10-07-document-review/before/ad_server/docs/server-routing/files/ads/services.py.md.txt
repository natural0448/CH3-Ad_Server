# ads/services.py

수정 23일차 v2.3 1교시. 기존 4인수 선택과 bid_amount 스키마를 유지한다. 후보는 활성 캠페인·동일 소유자의 유효 입찰이고 금액 내림차순·캠페인 ID 오름차순이다. selected_at은 서버가 만든 aware UTC datetime으로 BSON Date에 저장된다(읽기 클라이언트의 timezone 정책에 따라 naive UTC로 decode될 수 있고 밀리초 정밀도다). event_time은 같은 선택 시각의 UTC ISO 문자열이다. owner_user_id·chosen_campaign_id·chosen_bid_amount는 승자에서, candidates의 소유자·금액과 creative의 title/body/creative_path는 당시 조회에서 복사한다. context는 deepcopy다. policy_version=highest-bid/v1, schema_version=ad-decision/v1. 후보 없음은 chosen/creative/owner가 None이고 저장 결정은 유지한다. 과거 문서는 보정하지 않는다.

직접 호출의 기대 계약: get_db는 기존 Database, find_one은 dict/None, find·sort·limit는 Cursor, update_one은 UpdateResult, insert_one은 InsertOneResult, create_index는 색인 이름이다. Django render/JsonResponse는 HttpResponse, JSON parse는 dict 등 JSON 값, urlopen은 응답 stream, patch/assert는 테스트 fixture/검증을 제공한다. 하위 계층 내부는 해당 짝 문서에 있다.

## `clean_subject(subject)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| subject | 없음 | 정확한 media_id/subject_id 두 키의 비어 있지 않은 문자열 dict. |

반환·실패: 새 subject dict 또는 ValueError(subject_invalid).

의사코드: dict/정확한 두 식별자/비어 있지 않은 문자열 검사 → 두 키의 canonical dict 반환.

직접 호출: `ValueError`, `any`, `isinstance`, `set`.

## `choose_ad(media_id, subject_id, slot_id, context)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| media_id | 없음 | 매체 공개 ID 문자열; 선택 경로는 ID 정규식1..40자. |
| subject_id | 없음 | 수신자 공개 ID 문자열; 선택 경로는 ID 정규식1..40자. |
| slot_id | 없음 | village-board 또는 lobby-banner. |
| context | 없음 | dict; 선택 시 deepcopy. |

반환·실패: 저장한 결정 dict; 입력ValueError/저장소PyMongoError.

의사코드: ID/슬롯/context 검사 → 활성 캠페인과 같은 소유자의 현재 입찰 읽기 → 후보 정렬 → UUID/선택 시각/승자·소재 snapshot 구성 → decisions.insert_one → snapshot 반환.

직접 호출: `ValueError`, `bid.get`, `campaign.get`, `candidates.append`, `candidates.sort`, `datetime.now`, `db['bids'].find_one`, `db['campaigns'].find`, `db['decisions'].insert_one`, `deepcopy`, `get_db`, `isinstance`, `selected_at.isoformat`, `str`, `type`, `uuid.uuid4`, `validate_id`.

## 상태·값 출처

지역 변수는 해당 함수가 소유하며 request/입력·서버 설정·DB 조회 또는 위 의사코드의 생성 단계에서 얻는다. 저장 snapshot과 receipt의 쓰기는 서비스/사건 계층이 맡는다. 테스트 연결·patch·가짜 응답은 해당 테스트 클래스만 소유하고 정리한다. 비밀값·쿠키·CSRF 토큰은 문서/증거에 복사하지 않는다.
