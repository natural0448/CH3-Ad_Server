# ads/snapshot_intake.py

2026-10-12 현재 24일차 2·3·4교시 구현이 검증됐다. inspect_snapshot 22개, readiness 8개, change_player/fixture 명령 17개 공식 검사가 통과했다. 사용자 4교시 함수·명령과 직접 입력한 3교시 명령은 보존했고 readiness 반환에 교안 필드 두 개를 추가했다. 5~8교시 후속 함수·명령은 아직 없다.

## 책임과 모듈 값

게임 snapshot 파일 경계의 제공부/실습 문제틀이다. 광고에서 게임 ORM을 import하지 않고 공개 snapshot bytes를 읽는다. 현재 DB 접근/저장이나 전달 표식 호출은 없다.

`SCHEMA_VERSION="player-snapshot/v1"`, `SOURCE_KIND="player-snapshot"`, `PUBLIC_FIELDS=("id","room_id","coins","version","updated_at")`, `SNAPSHOT_FIELDS=set(PUBLIC_FIELDS)|{"schema_version","source_kind","captured_at"}`는 모듈이 정의한다. 현재 inspect 본문은 정확한 8필드·스키마·출처를 검사한다.

`hashlib`, `io`, `json`, `Path`, `.timestamps.parse_utc`는 helper와 경로 관찰에서 사용한다. `shutil`, `tempfile`, `datetime`, `timezone`, `.exporting.read_ndjson`, `.exporting.write_ndjson`은 import돼 있지만 현재 모듈 함수 본문에서는 호출하지 않는다. write_player_change_fixture 관리명령은 이 모듈에서 import한 write_ndjson을 사용한다. 앞으로의 구현 계획을 현재 호출 관계로 기록하지 않는다.

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
