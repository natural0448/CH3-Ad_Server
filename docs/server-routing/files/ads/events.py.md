# ads/events.py

수정 교안 2교시 CODE15와 같은 함수이며 비문자열 event_type 거부만 추가했다. clean_subject는 services의 실제 helper다. subject.media_id·subject.subject_id의 점 표기 조회로 내장 문서 필드 순서에 영향받지 않는다. ID는 decision_id:event_type, event_time은 서버 aware UTC ISO 문자열, schema_version=ad-event/v1. owner_user_id·bid_amount·slot_id는 선택 당시 결정/후보에서 가져온다. click의 impression_time은 최초 노출 시각이며 impression은 자신의 사건 시각이다. $setOnInsert/upsert와 DuplicateKeyError 처리로 최초 내용만 유지한다. 캠페인/현재 입찰을 읽거나 과거 결정을 수정하지 않는다.

직접 호출의 기대 계약: get_db는 기존 Database, find_one은 dict/None, find·sort·limit는 Cursor, update_one은 UpdateResult, insert_one은 InsertOneResult, create_index는 색인 이름이다. Django render/JsonResponse는 HttpResponse, JSON parse는 dict 등 JSON 값, urlopen은 응답 stream, patch/assert는 테스트 fixture/검증을 제공한다. 하위 계층 내부는 해당 짝 문서에 있다.

## `record_ad_event(subject, decision_id, event_type)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| subject | 없음 | 정확한 media_id/subject_id 두 키의 비어 있지 않은 문자열 dict. |
| decision_id | 없음 | 선택 결정 ID 문자열; 이벤트 중계는1..128자. |
| event_type | 없음 | impression 또는 click 문자열. |

반환·실패: event_id/event_type/created dict; decision_id_required,event_type_invalid,decision_not_found_for_subject,decision_snapshot_missing,impression_required의 ValueError; 저장소PyMongoError.

의사코드: clean_subject → ID/종류 검사 → dotted 수신자 결정 조회 → 당시 후보/금액/슬롯 검사 → 클릭이면 노출 조회 필수 → 최초 문서 upsert → created 판정.

직접 호출: `ValueError`, `chosen.get`, `clean_subject`, `datetime.now`, `datetime.now(timezone.utc).isoformat`, `db.ad_events.find_one`, `db.ad_events.update_one`, `db.decisions.find_one`, `decision.get`, `get_db`, `isinstance`, `next`, `row.get`, `type`.

## 상태·값 출처

지역 변수는 해당 함수가 소유하며 request/입력·서버 설정·DB 조회 또는 위 의사코드의 생성 단계에서 얻는다. 저장 snapshot과 receipt의 쓰기는 서비스/사건 계층이 맡는다. 테스트 연결·patch·가짜 응답은 해당 테스트 클래스만 소유하고 정리한다. 비밀값·쿠키·CSRF 토큰은 문서/증거에 복사하지 않는다.
