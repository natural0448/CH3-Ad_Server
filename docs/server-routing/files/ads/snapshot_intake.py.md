# ads/snapshot_intake.py

2026-10-12 현재 24일차 2~8교시 구현을 설명한다. inspect_snapshot 22개, readiness 8개, change_player/fixture 명령 17개 공식 검사는 앞선 검토에서 통과했다. 이번 5교시 13개·6교시 15개·7교시 10개 공식 검사도 통과했고 실제 계약·비교·누락 저장본이 현재 원본과 일치한다. 사용자 소스를 수정하지 않았다. 후속 8교시 검토에서 handoff_snapshot과 명령의 공식 24개 검사 및 실제 56행 파일·계약 인계가 성공했다. 기존 사용자 소스는 유지했다.

## 책임과 모듈 값

게임 snapshot 파일 경계의 제공부/실습 문제틀이다. 광고에서 게임 ORM을 import하지 않고 공개 snapshot bytes를 읽는다. 현재 DB 접근/저장이나 전달 표식 호출은 없다.

`SCHEMA_VERSION="player-snapshot/v1"`, `SOURCE_KIND="player-snapshot"`, `PUBLIC_FIELDS=("id","room_id","coins","version","updated_at")`, `SNAPSHOT_FIELDS=set(PUBLIC_FIELDS)|{"schema_version","source_kind","captured_at"}`는 모듈이 정의한다. 현재 inspect 본문은 정확한 8필드·스키마·출처를 검사한다.

`hashlib`, `io`, `json`, `Path`, `.timestamps.parse_utc`는 helper·경로 관찰·상태 비교에서 사용한다. datetime/timezone은 계약 생성 시각, .exporting.read_ndjson은 load_rows에서 사용한다. 마감 중 추가된 handoff_snapshot 본문은 shutil/tempfile도 호출한다. .exporting.write_ndjson은 현재 이 모듈 함수 본문에서 직접 호출하지 않으며 write_player_change_fixture 관리명령이 이 모듈의 import를 사용한다. 사용자 추가 import `from unittest import result`는 본문에서 사용하지 않는다. missing_summary의 result는 별도 지역 사전이다. 이 import를 정리하거나 바꾸지 않았다. 8교시 저장 코드는 공식 검사와 실제 인계까지 성공했으며 아래 증거를 따른다.

## _read_snapshot(path)

`path`는 기본값 없는 문자열/Path 호환 입력 파일 경로다. 상대경로는 실행 작업 폴더 기준이며 현재 광고 입력은 `../Game-server/data/exports/player-cdc.ndjson`이다. 반환값은 `(rows, checksum)` 튜플이다. rows는 입력 행 순서의 사전 목록, checksum은 읽은 원본 bytes의 SHA-256 64자리 문자열이다. 빈 파일은 빈 목록과 빈 bytes의 해시를 반환한다.

의사코드: Path에서 bytes 한 번 읽기 → UTF-8 decode/StringIO → 행별 빈 문자열/JSON 객체 확인 → rows 추가 → 같은 payload의 SHA-256과 목록 반환.

직접 호출: `Path(path).read_bytes()`는 bytes, `payload.decode("utf-8")`는 문자열, `io.StringIO`는 메모리 텍스트 스트림, `enumerate(...,1)`은 행 번호, `json.loads`는 JSON 값, `hashlib.sha256(payload).hexdigest()`는 checksum을 제공한다. 빈 행·사전이 아닌 행은 행 번호를 포함한 `ValueError`다. 파일/UTF-8/JSON 오류는 전파한다. 사건 스키마나 공개 상태 값까지 검사하지 않는다.

`payload`는 파일에서 온 고정 bytes, `rows=[]`는 helper가 작성하는 목록, `number`/`line`/`row`는 각 입력 행의 번호/문자열/파싱 결과다. 같은 한 번의 읽기에서 행과 checksum을 얻는다. 입력 파일을 수정하지 않는다.

## _check_public_state(row)

`row`는 기본값 없는 사전이며 키가 PUBLIC_FIELDS와 정확히 같아야 한다. id는 bool을 제외한 양의 int, room_id는 str(빈 문자열도 현재 helper가 허용), coins는 bool을 제외한 int(부호 제한 없음), version은 bool을 제외한 0 이상 int, updated_at은 parse_utc가 받아들이는 시간대 포함 ISO 문자열이다. 반환값은 성공 시 None이다.

의사코드: dict/정확한 다섯 키 확인 → id/room_id/coins/version 타입·범위 확인 → updated_at을 parse_utc로 확인 → 암묵적으로 None 반환.

직접 호출: `isinstance`, `set`, `type`으로 형태를 확인하고 `.timestamps.parse_utc(row["updated_at"])`에서 UTC datetime을 기대한다(반환값은 버림). 입력 위반은 ValueError이며 시각 입력 타입/파싱 오류는 helper에서 전파한다. 이 함수는 row를 쓰지 않는다. 현재 inspect는 snapshot 행에서 PUBLIC_FIELDS만 투영한 사전을 이 helper에 전달한다.

## inspect_snapshot(path)

`path`는 기본값 없는 문자열/Path 호환 snapshot 입력 파일 경로다. `_read_snapshot(path)` 반환 행을 순회하며 정확한 8필드, SCHEMA_VERSION/SOURCE_KIND 일치, 공개 상태, ID 중복, 시간대 있는 captured_at을 검사한다. 첫 captured_at 문자열을 보관하고 후속 문자열이 다르면 ValueError를 발생시킨다. 비어 있지 않은 입력은 parse_utc 검사를 먼저 통과해야 하므로 첫 수집값은 유효한 시각 문자열이다. 빈 입력에서는 초기값 None을 유지한다.

의사코드: 입력 bytes 읽기/해시 → seen/captured_at 초기화 → 행별 8필드/스키마·출처 검사 → 공개 상태 검사 → ID 중복 거절/등록 → parse_utc(row["captured_at"]) 호출 → 첫 수집값 보관/후속 값 비교 → 메타데이터 사전 반환.

현재 반환 사전은 `rows=len(rows)`, `public_ids=sorted(seen)`, `source_kind=SOURCE_KIND`, `schema_version=SCHEMA_VERSION`, `captured_at=captured_at`, `sha256=checksum`이다. public_ids는 등록한 정수 ID의 오름차순 목록이다. 빈 파일은 rows=0, public_ids=[], captured_at=None을 반환한다. 필드/출처/공개 값/중복/수집값 차이는 ValueError이며 읽기/JSON/updated_at 타입·파싱 오류는 전파한다.

직접 호출은 `_read_snapshot`, `set`, `_check_public_state`, `seen.add`, `parse_utc`, 반환 분기의 `len`/`sorted`다. parse_utc에서 UTC datetime을 기대하고 반환값은 버리며, 시각 형식/시간대 오류는 전파한다. `rows`/`checksum`은 같은 한 번의 bytes 읽기에서 온다. `seen`은 이 함수가 ID를 등록하는 집합이고 `captured_at`은 첫 입력 문자열을 보관한다. 입력 파일은 수정하지 않는다.

updated_at 검사는 공개 상태 helper, captured_at 검사는 inspect가 직접 담당한다. 최초 빈칸과 시간대 검사 미호출은 과거 관찰 자료로 보존하고 현재 구현과 구분한다.

## 현재 완료 검증 · 2026-10-12

공식 검사 **22 통과·0 실패**, 실제 `inspect_player_snapshot` 관리명령 **exit 0**이다. 원본 56행·56개 공개 ID의 수집 시각과 SHA-256이 기존 파일과 일치했고 파일 bytes는 유지됐다. [최종 검사](../../verification/2026-10-12-day24-period01-02/official-period02.json), [실제 원본 검사](../../verification/2026-10-12-day24-period01-02/actual-snapshot-inspection.json)를 따른다. 파일 검사만으로 광고 선택 문맥을 Player 상태와 연결하지 않는다.

## 과거 2교시 완료 여부 재검토 · 2026-10-08

다음 실패 기록은 수정 전 관찰이다. 현재 2교시 완료 판정은 위 2026-10-12 검증을 따른다.

당시 저장본을 공식 `tools/check_day24_logic.py --period 2`로 격리 검사한 결과 **20 통과·2 실패**다. [검사 결과](../../verification/day24-period02-review/official-period02-final.json)와 [검토 인수인계](../../../handoffs/2026-10-08-day24-period02-review.md)에 근거를 기록했다.

실패는 `naive captured_at 거절`과 `검사 관리명령`이다. 전자는 inspect의 `parse_utc` 이름 식이 시각 검사를 호출하지 않기 때문이며, 후자는 `ads/management/commands/inspect_player_snapshot.py`가 없기 때문이다. 중복·정확한 필드/출처·bool/정수·updated_at·수집값 일치·빈 파일/빈 행 및 메타데이터 검사는 통과했다. 실제 원본의 관리명령 검사는 수행할 수 없어 2교시 완료로 기록하지 않는다. 검사기는 격리 파일/SQLite 메모리만 사용했고 MongoDB와 실제 입력 파일에 쓰지 않았다. 학생 소스는 변경하지 않았다.

## readiness(mysql_config=None, connect_home=None, debezium_dir=None)

1·2교시 검증 이후 사용자가 readiness를 추가했다. 앞선 검토의 누락 두 필드를 이번 4교시까지 복구 요청에서 교안대로 추가했다. 사용자 함수의 경로 관찰 로직은 그대로 유지했다. 공식 3교시 8개와 실제 관리명령 저장이 통과했다.

세 파라미터는 기본값 None인 선택 경로다. 현재 supplied_paths가 이름별 사용자 입력을 소유하고 paths는 각 값의 bool로 supplied, 값이 있을 때 Path(path).exists()로 exists를 기록한다. 입력 경로를 생성/변경하거나 외부 프로세스를 시작하지 않는다.

의사코드: 세 경로 mapping → supplied/exists 관찰 → 현재 readiness 메타데이터 사전 반환.

현재 반환 키는 schema_version="cdc-readiness/v1", paths, mysql_binlog="not-verified", cdc_reader/connect_worker/debezium_connector/player_change_topic="not-configured", common_input=SCHEMA_VERSION, binlog_cdc_observed=False다. 반환은 새로운 준비 상태 사전이며 직접 호출은 bool, Path, Path.exists뿐이다. 선택 경로는 문자열/Path 호환 값이고 None/빈 문자열은 미제공 처리한다. Path 변환/존재 확인의 TypeError/OSError 등은 전파할 수 있다. 경로 존재를 실제 CDC 실행 증거로 바꾸지 않는다. [현재 3교시 결과](../../verification/2026-10-12-day24-period04-recovery/official-period03-final.json)를 따른다.

## 수정 교안의 3교시 실행 검토 · 2026-10-12

다음은 복구 전 검토 이력이다. 현재 완료 결과는 위 readiness와 아래 4교시까지 최종 검증을 따른다.

[당시 공식 검사](../../verification/2026-10-12-day24-period03-review/official-period03.json)는 3 통과·5 실패다. 당시 함수는 경로 미제공과 제공/존재 구분 검사를 통과했지만 `common_input`, `player_change_topic` 조회에서 KeyError를 일으켰다. 교안이 요구하는 값은 각각 `SCHEMA_VERSION`, `"not-configured"`이며 당시 코드에는 아직 적용되지 않았다.

당시 호출부 `ads.management.commands.write_cdc_readiness` 파일은 0 bytes로 Command 클래스가 없어 저장/출력 오류 검사도 실패했다. 그 검토에서 함수와 관리명령 소스의 시작·종료 SHA-256이 같고 검사기는 실제 MongoDB에 접속하지 않았다. 존재 관찰을 실제 CDC 성공으로 바꾸는 후속 구현은 하지 않았다.

## change_player(event) · 사용자 4교시 구현 사전 정합화

event는 기본값 없는 teaching-fixture 사전이다. source_kind="teaching-fixture", op="r"/"u"/"d", before/after 공개 상태 또는 None을 읽는다. r은 before=None·after=공개 상태, u는 두 공개 상태의 같은 ID, d는 before=공개 상태·after=None을 요구한다. 공개 상태의 정확한 5필드와 각 타입/시각 허용 범위는 _check_public_state를 따른다.

반환은 새 사전 {op, player_id, coins, version, deleted}다. r/u는 after, d는 before에서 id/coins/version을 얻고 d에서만 deleted=True다. 입력은 변경하지 않는다. 출처·종류·전후 모양·공개 상태·u의 ID 위반은 ValueError다. event 자체는 사전이 입력 계약이며 사전이 아니면 .get 호출의 AttributeError가 전파될 수 있다. 그 계약을 임의 확장하지 않는다.

의사코드: 출처 확인 → op/before/after 읽기 → op별 모양·공개 상태 검사 → u ID 일치 확인 → d는 before, r/u는 after 선택 → 해석 사전 반환.

직접 호출은 event.get, isinstance, _check_public_state다. DB, 게임 ORM, Kafka, 파일 쓰기, 삭제 API를 호출하지 않는다. op/before/after는 입력에서 읽고 state는 검증한 상태 참조를 고르며 새 반환 사전만 이 함수가 작성한다. 이미 작성된 이 함수는 교안 전체 함수와 일치하며 추가 개발 전에 사용자 코드의 현재 책임을 기록했다.

## 4교시까지 최종 검증

[공식 2교시](../../verification/2026-10-12-day24-period04-recovery/official-period02-final.json) 22/0, [공식 3교시](../../verification/2026-10-12-day24-period04-recovery/official-period03-final.json) 8/0, [공식 4교시](../../verification/2026-10-12-day24-period04-recovery/official-period04-final.json) 17/0다. 교안 화면 검사도 통과했다. 사용자 change_player/fixture 명령의 AST가 교안 원문과 같았고 소스를 수정하지 않았다. 실제 readiness·원문 fixture·summary의 [출력 검증](../../verification/2026-10-12-day24-period04-recovery/actual-output-verification.json)도 통과했다. 게임 snapshot의 bytes 해시는 유지했다.

## build_snapshot_contract(source)

source는 기본값 없는 기존 snapshot 문자열/Path 호환 경로다. inspect_snapshot(source)의 검사 메타데이터를 읽고 새 contract 사전에 합쳐 반환한다. 입력 파일을 쓰지 않는다. 검사 예외와 경로/파싱 오류는 전파한다.

초기 contract는 artifact_id="data/exports/player-cdc.ndjson", artifact_version="v2", source_path=str(source), created_at=현재 aware UTC ISO 문자열, collector="game.export_player_snapshot", binlog_cdc_status="not-configured", position_kind="file-line", kafka_position=None, public_fields=list(PUBLIC_FIELDS)다. contract.update(inspected)로 실제 rows/public_ids/captured_at/sha256/source_kind/schema_version을 더한다. inspected는 입력 검사 결과, contract는 이 함수가 소유한 새 사전이다. created_at과 입력 captured_at을 구별한다.

의사코드: 원본 검사 → 고정 인계 조건·현재 계약 시각·원본 경로 → 검사 결과 update → contract 반환. 직접 호출은 inspect_snapshot, str, datetime.now(timezone.utc).isoformat, list와 dict.update다. 경로 기준은 호출 프로세스 작업 폴더다. 파일 이름의 cdc를 실제 binlog 성공이나 Kafka 위치로 해석하지 않는다.

## load_rows(path)

path는 기본값 없는 동결 snapshot 경로다. 먼저 inspect_snapshot(path)를 호출해 형식·중복 ID 등을 검사한 다음 read_ndjson(path)의 사전 목록을 id→row 사전으로 변환하여 반환한다. 입력을 쓰지 않는다. 읽기/검사 오류는 전파한다.

의사코드: snapshot 검사 → 같은 파일을 NDJSON reader로 다시 읽기 → row["id"]를 키로 등록 → 사전 반환. 직접 호출은 inspect_snapshot와 .exporting.read_ndjson이며 두 번 읽는 사이에 원문을 잠그는 기능은 없다. 같은 동결 파일을 유지하는 호출 계약이다. row는 reader가 반환하는 각 사전이다.

## compare(before, after)

before/after는 기본값 없는 검증된 정수 Player ID→공개 행 사전이다. 함수 자체는 입력 형식 검사·파일 읽기·DB 쓰기를 수행하지 않는다. 반환은 {changed, newly_seen, missing_unknown} 새 사전이다.

의사코드: 공통 ID 오름차순 → old/new 공개 행 → room_id/coins/version/parse_utc(updated_at) 튜플 비교 → 다르면 id·before_version·after_version·before_coins·after_coins 행 추가 → 새 ID와 원인 미상 누락 ID 정렬 반환.

직접 호출은 set/sorted, .timestamps.parse_utc, changed.append다. parse_utc의 반환 UTC datetime으로 같은 순간의 다른 offset 표현을 동일하게 본다. captured_at은 업무 상태 비교에서 제외한다. 입력 사전은 수정하지 않는다. 없는 키/잘못된 수정 시각은 KeyError/시각 파싱 오류 등으로 전파한다.

changed=[]는 함수가 소유하는 결과 목록, player_id는 공통 ID, old/new는 입력 행 참조, old_state/new_state는 비교 튜플이다. changed 행의 키는 id이며 설명용 예시 title/when/old_value/new_value를 사용하지 않는다. newly_seen은 after에만, missing_unknown은 before에만 있는 정수 ID 오름차순이다.

## missing_summary(before, after)

before/after는 기본값 없는 정수 ID→공개 행 사전이다. 이 함수는 행 값을 읽지 않고 키 집합 차이만 관찰한다. 반환은 {missing_unknown: 정렬된 before-only ID 목록, source_kind: "snapshot-comparison", delete_events: [], delete_inference_allowed: False}다.

의사코드: before 키에서 after 키 빼기 → 정렬 → 누락 관찰·고정 출처·빈 삭제 목록·삭제 추론 불가 사전 → 반환. 직접 호출은 set/sorted다. missing은 정렬 ID 목록, result는 이 함수가 작성하는 지역 사전이다. 두 입력을 바꾸지 않으며 파일·게임 ORM·MongoDB·삭제 API를 호출하지 않는다. 누락 이유와 실제 삭제 version/시각을 추론하지 않는다.

## 5~7교시 최종 검증 · 2026-10-12

[5교시 13/0](../../verification/2026-10-12-day24-period05-07-review/official-period05-final.json), [6교시 15/0](../../verification/2026-10-12-day24-period05-07-review/official-period06-final.json), [7교시 10/0](../../verification/2026-10-12-day24-period05-07-review/official-period07-final.json)과 [5교시 화면 검사](../../verification/2026-10-12-day24-period05-07-review/screen-period05.json)가 통과했다. [교안 AST 대조](../../verification/2026-10-12-day24-period05-07-review/lesson-comparison.json)는 네 추가 함수가 docstring을 제외한 제공 함수와 같고 기존 2~4교시 함수가 HEAD와 같음을 확인한다.

[실제 저장본 대조](../../verification/2026-10-12-day24-period05-07-review/actual-file-verification.json)에서 before/after 각 56행, changed 1건·newly_seen 0건·missing_unknown 0건이다. 계약 메타데이터/원본 checksum·비교·누락 JSON이 현재 파일과 일치한다. 실제 게임 행동의 성공 응답은 이 검토에서 직접 관찰하지 않았고 원본·산출물을 다시 쓰지 않았다.

## handoff_snapshot(source, contract_path, target) · 8교시 완료

세 파라미터는 기본값 없는 경로다. source는 기존 snapshot, contract_path는 JSON 계약, target은 아직 없는 최종 수신 폴더다. 사용자가 저장한 함수를 변경하지 않고 공식 24개 검사와 실제 수신 폴더 인계를 확인했다.

현재 의사코드: source/target Path → 계약 JSON 읽기 → source 검사 → expected 메타데이터/검사값을 sort_keys JSON으로 비교 → created_at parse_utc → 기존 target 거절 → 부모 준비/같은 부모 임시 폴더 → 원본 copyfile → 복사 bytes checksum 검사 → 계약 복사/source_path를 최종 경로로 변경 → 임시 계약 JSON 저장 → 임시 폴더 rename → 행 수/checksum/출처/target 반환. 임시 단계 Exception이면 rmtree(ignore_errors=True) 후 재전파한다.

expected의 고정 값은 artifact_id=data/exports/player-cdc.ndjson, artifact_version=v2, public_fields=list(PUBLIC_FIELDS), position_kind=file-line, kafka_position=None, collector=game.export_player_snapshot, binlog_cdc_status=not-configured이며 inspect_snapshot 반환을 합친다. expected에는 source_path를 넣지 않는 현재 구현이다. contract는 읽은 사전, inspected는 원본 검사 결과, field/value는 대조 항목, temporary는 mkdtemp Path, received는 임시 player-cdc.ndjson, received_contract는 복사한 계약 사전이다.

직접 호출은 Path/read_text/exists/parent.mkdir/rename, json.loads/dumps, inspect_snapshot, list, parse_utc, tempfile.mkdtemp, shutil.copyfile/rmtree, hashlib.sha256(...).hexdigest, received.read_bytes 및 계약 Path.write_text다. 반환은 {rows: inspected rows, sha256: inspected checksum, source_kind: SOURCE_KIND, target: str(target)}다. 값 불일치·기존 target·복사 checksum 불일치는 ValueError이고 읽기/JSON/경로 오류 등은 전파한다. 내부에서 폴더/복사 파일을 쓰는 함수다. [공식 24/0](../../verification/2026-10-12-day24-period08-finish/official-period08-before.json), [실제 인계 56행·체크섬/경로 일치](../../verification/2026-10-12-day24-period08-finish/actual-handoff.json)를 따른다. 제공 정답은 사전 값을 직접 비교하고 현재 사용자 코드는 sort_keys JSON으로 비교한다. 오류 문구도 다르지만 교안의 계약 대조·복사·새 대상 보호 동작은 검사에 통과해 사용자 구현을 유지했다.
