# ads/context_projection.py

2026-10-13 사용자 저장본을 설명한다. 공개 snapshot과 수신 계약을 검증하고 정규화 변경을 `player_context`에 반영한다. HTTP 인증·게임 ORM·광고 선택을 맡지 않는다. 기존 13개 함수는 25일차 1~6교시 제공 완성 코드와 AST가 같고 보존했다. 2026-10-14 추가한 두 인계 함수도 8교시 제공 완성 코드와 AST가 같다. 실제 HTTP 연결 완료 여부는 별도다.

## 값과 책임 경계

`PUBLIC_FIELDS`, `SNAPSHOT_FIELDS`, `SCHEMA_VERSION`, `SOURCE_KIND`, `_check_public_state`, `_read_snapshot`, `inspect_snapshot`은 `snapshot_intake`에서 읽는다. `SOURCE_KIND`는 `player-snapshot`, snapshot schema는 `player-snapshot/v1`이다. 변경 schema는 `player-context-change/v1`, checkpoint schema는 `context-checkpoint/v1`이다. 기본 매체는 `village-game`이다. 경로는 호출 프로세스 작업 폴더 기준이며 source·contract를 이 모듈에서 수정하지 않는다. 지역 rows·document·changes·counts·state는 각 함수가 만든 값이다. 저장 문서는 `_id`, media_id, subject_id, version, source_kind, change_id, event_time, deleted, context의 아홉 필드다.

직접 외부 호출은 `Path` 파일 접근, JSON·SHA256, `parse_utc`의 UTC datetime, `write_ndjson`의 파일 지문, `get_db()`의 Mongo Database다. 정규화 출력과 checkpoint 쓰기 소유자는 아래 파일 함수다. `apply_context`가 Mongo 공개 복사본의 쓰기를 소유한다.

## read_snapshot_package(source, contract_path)

두 인수는 기본값 없는 문자열/Path 호환 입력 파일과 수신 계약 JSON 경로다. 반환은 `(검증된 행 list, inspected dict)`다. 의사코드: 계약 사전 읽기 → inspect_snapshot 결과와 고정 artifact/collector/position/public_fields 대조 → created_at 시각·source_path 절대 경로 대조 → 같은 입력 bytes 재조회와 SHA 확인 → 반환. 직접 호출은 `inspect_snapshot`, `_read_snapshot`, `parse_utc`, `Path.resolve/read_text`, `json.loads/dumps`다. 불일치·읽기 오류는 전파하고 파일/DB를 쓰지 않는다.

## normalize_snapshot(row, media_id='village-game')

row는 정확한 공개 여덟 필드의 사전이고 media_id는 비어 있지 않은 문자열이다. 기본 매체는 village-game이다. 반환은 change_id를 포함한 아홉 필드 upsert 변경 사전이다. 의사코드: 공개 필드·schema·출처·업무 값·captured_at 검증 → id 문자열과 UTC updated_at으로 공개 다섯 필드 context 생성 → 변경 사전을 정렬 JSON으로 SHA256 → change_id 추가. 직접 호출은 `_check_public_state`, `parse_utc`, `json.dumps`, `hashlib.sha256`이다. 입력 사전을 수정하지 않고 DB를 호출하지 않는다. captured_at은 change_id 업무 내용에 넣지 않는다.

## normalize_snapshot_file(source, contract_path, output, media_id='village-game')

source·contract_path는 수신 파일 쌍, output은 둘과 다른 출력 경로, media_id는 비어 있지 않은 문자열이다. 반환은 path, rows, sha256, schema_version, source_kind, source_sha256, media_id, op_counts, unique_change_ids, preview 요약이다. 의사코드: 출력 경로 보호 → read_snapshot_package → 모든 행 normalize_snapshot → change_id 중복 거절 → 같은 출력 부모의 임시 NDJSON 완성 → os.replace → 요약. 직접 호출은 두 상위 helper, `write_ndjson`, `tempfile.TemporaryDirectory`, `Path.mkdir`, `os.replace`다. 변환 실패는 출력 저장 전에 발견한다. 성공 시 output은 교체되며 source/contract는 보존한다.

## context_subject_key(media_id, subject_id)

두 인수는 기본값 없는 비어 있지 않고 콜론 없는 문자열이다. 반환은 `media_id + ':' + subject_id` 안정 키다. 검사 실패는 ValueError다. 의사코드: 두 값의 타입·공백·콜론 검사 → 연결 반환. DB/파일 외부 호출은 없다.

## _check_context_change(change)

change는 정확한 아홉 필드의 정규화 사전이다. 정상 반환은 None, 계약 불일치는 ValueError다. 의사코드: schema·출처·op·대상 키 검증 → 공개 Player는 양의 정수 원형 문자열/upsert만, fixture는 별도 fixture- 대상 → version 정수와 UTC 정규 시각 검증 → delete 빈 context 또는 upsert 공개 다섯 필드·같은 ID/version/시각 검증 → change_id 제외한 내용의 SHA 대조. 직접 호출은 `context_subject_key`, `parse_utc`, JSON·SHA다. 입력·파일·DB는 변경하지 않는다.

## make_context_document(change)

기본값 없는 변경 사전을 받는다. 반환은 안정 _id와 삭제 표시를 포함한 아홉 필드 저장 문서다. 의사코드: _check_context_change → context_subject_key → 출처 여섯 필드 복사 → _id/deleted/context 추가. delete의 context는 빈 사전, upsert는 context의 새 사전이다. 두 helper를 직접 호출하며 Mongo에 저장하지 않는다.

## apply_context(change)

기본값 없는 변경 사전을 받는다. 반환은 `applied`, `duplicate`, `stale` 중 하나다. 의사코드: make_context_document → get_db().player_context → 최대 세 번 현재 문서 읽기 → 없으면 insert, 중복 키 경쟁은 재조회 → 저장 version이 더 크면 stale → 같은 version·같은 deleted/context면 duplicate, 상태가 다르면 version_conflict → 작은 version은 기존 version 조건 replace_one → matched_count=1이면 applied. 재시도 소진은 concurrent_update ValueError다. 직접 호출은 `make_context_document`, `get_db`, `find_one`, `insert_one`, `replace_one`이며 `DuplicateKeyError`만 내부 경쟁 처리한다. 최신 상태와 과거 입력을 구별하고 원본 Player를 수정하지 않는다.

## get_context(media_id, subject_id)

두 인수는 context_subject_key와 같은 문자열 계약이다. 반환은 미삭제 문서 context의 새 dict, 문서 없음/삭제 상태면 `{}`다. 의사코드: 안정 키 → get_db().player_context.find_one → 삭제 여부 검사 → 복사 반환. 직접 호출은 `context_subject_key`, `get_db`, `find_one`, `dict`다. DB 쓰기·인덱스 생성은 하지 않는다.

## _read_context_changes(source)

source는 기본값 없는 정규화 NDJSON 경로다. 반환은 `(모든 검증 행 list, 원본 bytes SHA256 문자열)`이다. 의사코드: read_bytes → bytes 행 분리 → 빈 행 거절 → UTF-8 JSON 읽기 → 각 make_context_document 검증 → 행과 SHA 반환. 직접 호출은 `Path.read_bytes`, JSON·SHA, `make_context_document`다. Mongo 쓰기는 없다.

## _read_context_checkpoint(checkpoint, checksum, row_count)

checkpoint는 JSON 경로, checksum은 현재 입력 SHA 문자열, row_count는 입력 행 수다. 모두 기본값 없다. 반환은 `0 <= next_line <= row_count` 정수다. 의사코드: 정확한 schema_version/source_sha256/next_line 세 필드 검사 → schema와 64자리 소문자 SHA 형식 및 입력 일치 → bool을 제외한 정수 위치 범위 검사. 직접 호출은 `Path.read_text`, `json.loads`다. 기존 checkpoint를 수정하지 않는다.

## _save_context_checkpoint(checkpoint, checksum, position)

checkpoint는 기록 경로, checksum은 입력 SHA, position은 다음 읽을 index다. 반환은 세 필드 checkpoint 사전이다. 의사코드: 부모 mkdir → schema/SHA/next_line 구성 → 같은 부모 임시 state.json 저장 → os.replace → 반환. 직접 호출은 Path 쓰기, `tempfile.TemporaryDirectory`, `json.dumps`, `os.replace`다. position의 검증은 호출자가 맡는다.

## project_context_file(source_path, checkpoint_path=None, limit=None)

source_path는 변경 NDJSON 경로다. checkpoint_path 기본 None은 기록 없는 처리, 지정 시 공백 없는 원본과 다른 경로여야 한다. limit 기본 None은 끝까지, 지정 시 bool을 제외한 양수 정수다. 반환은 processed/applied/skipped/counts/start_line/next_line/rows/done/source_sha256/checkpoint_path/checkpoint_state 요약이다. 의사코드: 경로·limit 보호 → 모든 변경 검증 → 기존 기록의 동일 SHA·위치 확인 → limit 범위에서 apply_context → 성공한 행 뒤에 checkpoint 저장 → 위치/상태 집계 → 빈 입력도 필요하면 위치 0 저장 → 요약. 직접 호출은 `_read_context_changes`, `_read_context_checkpoint`, `apply_context`, `_save_context_checkpoint`다. 완료된 기록은 재실행 시 processed=0이다. DB와 checkpoint는 서로 다른 쓰기이고 DB 성공 뒤 기록한다. 실패한 행의 위치는 올리지 않는다.

## refresh_snapshot(source, contract_path, media_id='village-game')

source와 contract_path는 새로운 동결 수신 파일 쌍이다. media_id는 기본 village-game, context_subject_key의 매체 계약을 만족해야 한다. 반환은 source/contract/rows/source_sha256/media_id/counts/preview 요약이다. 의사코드: 매체 검사 → read_snapshot_package → 모든 normalize_snapshot 선변환 → 각각 apply_context와 상태 집계 → 요약. 직접 호출은 세 helper와 context_subject_key다. 파일 출력이나 checkpoint를 만들지 않고 5교시 기존 기록을 재사용하지 않는다. 전체 선변환 뒤에 Mongo 쓰기를 시작하되 HTTP·전체 파일 단일 트랜잭션은 제공하지 않는다.


## _read_handoff_context(media_id)

media_id는 기본값 없는 지정 매체 식별자다. 반환은 해당 매체의 공개 저장 문서 list다. 의사코드: get_db().player_context.find(media_id).sort(_id,1) → 각 문서가 정확한 아홉 필드·deleted bool인지 검사 → 삭제 표시에서 op 복원 → make_context_document로 키·출처·공개 상태·change_id 재대조 → 반환. 직접 호출은 get_db, collection.find/sort, make_context_document다. 잘못된 문서는 ValueError, 저장소 오류는 PyMongoError로 전파한다. 문서와 DB를 변경하지 않고 다른 매체는 query에서 제외한다. fixture는 source_kind로 구별한다.

## export_context_handoff(source_path, checkpoint_path, output_dir, media_id='village-game')

source_path는 최신 정규화 NDJSON, checkpoint_path는 같은 SHA의 완료 JSON, output_dir는 기존에 없는 인계 폴더 문자열/Path 호환 경로다. 세 인수는 기본값 없다. media_id 기본 village-game이며 context_subject_key가 받는 콜론 없는 비어 있지 않은 문자열이다. 반환은 manifest 사전이다. 같은 출력 경로, 다른 SHA/미완료 위치, 다른 매체/fixture 입력, 잘못된 공개 문서, 복사 중 입력 변경은 거절한다.

의사코드: 매체·새 출력 검사 → _read_context_changes → _read_context_checkpoint와 next_line=rows → 지정 매체의 player-snapshot 입력 검사 → _read_handoff_context → 같은 부모 임시 package → 원본 bytes copy와 SHA 대조 → 공개 복사본 NDJSON과 별도 SHA → checkpoint/manifest JSON → staged.rename(target) → manifest 반환. 직접 호출은 context_subject_key, _read_context_changes, _read_context_checkpoint, _read_handoff_context, Path, tempfile.TemporaryDirectory, shutil.copyfile, hashlib.sha256, write_ndjson, json.dumps, datetime.now(timezone.utc), Path.rename다. write_ndjson은 쓴 파일 SHA를 반환하고 rename은 완성된 새 폴더를 공개한다. 원본·기존 기록·기존 인계·Mongo 문서를 쓰지 않는다.

manifest의 artifact_id는 MongoDB village_ads.player_context, artifact_version은 v2, input_schema_version은 player-context-change/v1, source_kind는 player-snapshot, binlog_cdc_status는 not-configured다. input_path/checkpoint_path/context_path는 최종 폴더의 세 파일을 가리키며 original_input_path는 소비한 원문이다. 입력 SHA와 context SHA는 서로 다른 파일 지문이다. context_fields는 아홉 저장 필드이며 context_source_kind_counts는 player-snapshot/teaching-fixture 건수를 구별한다. created_at은 함수가 만든 aware UTC 시각, context_route는 /api/ads/context/, advertiser_report_route는 /advertiser/reports/다. 단일 작성자·동결 입력 모델이며 여러 Mongo 문서를 동일 시점 트랜잭션으로 읽는다고 주장하지 않는다.
