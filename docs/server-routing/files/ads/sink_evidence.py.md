# ads/sink_evidence.py

4교시 진행 중 사용자가 저장한 공개 context 대조 구현이다. 이 검토에서는 코드를 수정하지 않고 현재 내용만 문서로 맞췄다. COMPARE_FIELDS는 (media_id, subject_id, version, deleted, context)이며 모듈 작성자가 고정한 업무 비교 필드다. 계정·좌표·snapshot 시각은 비교하지 않는다. 교안 기본 함수에 공개 문서 검증, 매체 필터, 불일치 값 표시가 추가된 현재 저장 상태다.

## _index_context_rows(rows)

rows는 기본값 없는 공개 문서 iterable다. 반환은 _id→원본 row 사전이다. 허용 필드는 _id/media_id/subject_id/version/deleted/context/source_kind/change_id/event_time이며 선택 schema_version은 player-current/v1이어야 한다. deleted는 bool만 허용한다.

의사코드: 행의 dict·정확한 필드·schema·bool 검사 → change 사전 구성 → make_context_document 결과와 공개 document 일치 검사 → 중복 _id 거절 → indexed 반환. 직접 호출 make_context_document는 키·내용·출처·시각·변경 SHA를 검증한 공개 문서를 반환한다. set/dict와 isinstance/type을 사용한다. 계약·중복 불일치는 ValueError다. fields/indexed/document/change는 호출 로컬값이고 원본 row는 쓰지 않는다.

## compare_rows(expected_rows, actual_rows)

두 인수는 기본값 없는 예상 Lake 공개 문서와 실제 Mongo 공개 문서 iterable다. 반환은 expected_keys/missing/extra_keys/mismatched/matched/input_scope_matches 사전이다.

의사코드: _index_context_rows 두 번 → 예상에만 있는 키 missing·실제에만 있는 키 extra 정렬 → 공통 키의 COMPARE_FIELDS 값 비교 → 다른 필드와 lake/mongo 값 사전 저장 → matched 계산 → 입력 범위 일치 반환. 직접 호출 _index_context_rows/sorted/set/len이다. input_scope_matches는 missing과 mismatched가 모두 없으면 True이며 extra만 있으면 True다. extra를 삭제로 추론하거나 DB를 변경하지 않는다. expected/actual/missing/extra/mismatched/fields/matched는 호출 로컬값이다. 검증 오류는 위 helper에서 전파된다.

## compare_context_to_current(current_rows, media_id='village-game')

current_rows는 기본값 없는 Lake 현재 상태 목록이며 두 번 순회하므로 재순회 가능한 목록을 사용한다. media_id는 기본 village-game 문자열이다. 모든 행의 media_id가 지정 값과 같아야 한다. 반환은 compare_rows 결과 사전이다.

의사코드: 입력 매체 불일치 ValueError → get_db()['player_context'].find({'media_id': media_id}) 목록으로 읽기 → compare_rows(current_rows, actual) 반환. 직접 호출 ads.mongo.get_db, Mongo collection.find, list, compare_rows다. DB 연결 실패는 PyMongoError로 호출자에게 전파된다. 광고 공개 player_context만 읽고 쓰기·삭제·게임 ORM 호출은 없다. 실제 Mongo 대조 성공 여부는 이번 Lake 경로 검증으로 확인한 것이 아니다.
