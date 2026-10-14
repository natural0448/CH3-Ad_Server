# ads/lake_files.py

26일차1·2교시의 메모리 history/current 계산이다. 기존 사용자 stable_json·build_history를 보존하는 범위에서 history 오류 문자열을 교안의 change_id로 바로잡고 build_current를 추가했다. 세 함수 AST가 제공 완성 코드와 같다. DB 조회·쓰기와 Lake 파일 저장은 하지 않는다.

## stable_json(row)

row는 기본값 없는 JSON 직렬화 가능 값이며 실제 호출에서는 정규화 dict/결과 list다. 반환은 ensure_ascii=False·sort_keys=True·separators=(comma,colon)의 고정 JSON 문자열이다. 의사코드: json.dumps 고정옵션 → 문자열. 직접 호출 json.dumps이며 직렬화 불가능한 값은 TypeError다. 입력/파일을 쓰지 않는다.

## build_history(rows)

rows는 기본값 없는 정규화 변경 사전 iterable이며 make_context_document의 정확한9필드·출처·ID·version·UTC 시각·내용 SHA 계약을 만족해야 한다. 반환은 change_id별 고유 행의 새 list이고 각 dict는 원본 참조다. 의사코드: 행마다 make_context_document → 같은 change_id 이전 행 읽기 → stable_json 내용이 다르면 ValueError(same change_id has conflicting content) → unique에 행 저장 → parse_utc(event_time), change_id 순 sorted 반환. 직접 호출 make_context_document/stable_json/parse_utc/sorted와 dict.get/values다. 서로 다른 version은 같은 대상이어도 history에 남는다. 잘못된 SHA는 helper에서 먼저 거절된다.

## build_current(history)

history는 기본값 없는 정규화 행 iterable다. 반환은 player-current/v1 schema와 기존9개 공개 문서 필드의10필드 사전 list, 대상별1행이며 _id 문자열 오름차순이다. 빈 입력은[]다. 의사코드: build_history 재검사/중복제거 → media_id/subject_id/version/change_id 순 정렬 → make_context_document → document._id 안정키와 candidate 구성 → 처음/큰 version만 교체 → 같은 version에서 deleted 또는 context가 다르면 ValueError(same subject/version has conflicting content) → sorted key로 반환. 직접 호출 build_history, make_context_document, sorted, dict.get다. 오래된 upsert는 최신 deleted=true/context={} 후보를 되살리지 않는다. 같은 version/같은 업무 상태는 정렬에서 처음 택한 출처 후보를 유지하여 역순 입력에도 결과가 같다. provenance와 최신 업무 상태의 비교를 구별한다.

## 값·책임 경계

unique/current/old/candidate/document/ordered는 각 호출 로컬값이다. _id는 기존 make_context_document/context_subject_key의 media_id:subject_id에서 오고 change_id는 검증한 정규화 내용의 SHA다. make_context_document는 저장하지 않는 helper, parse_utc는 timestamps다. 제공 import의 datetime/timezone/Path/hashlib/read_ndjson은3교시 준비로 유지하되 현재 함수에서 저장을 실행하지 않는다. current는 이번 입력 대상만 다루며 Mongo 전체 문서 수나 게임 전체 인원으로 해석하지 않는다.
