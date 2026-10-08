# ads/snapshot_intake.py

2026-10-08 문서 정합화 도중 새로 관찰한 사용자 작업 또는 작성자를 확정할 수 없는 작업이다. 16:44경 저장본에는 24일차 2교시 제공 helper와 inspect 함수의 필드/공개 상태/중복/수집값 통일 검사가 작성돼 있다. 수집 시각 검사 위치의 `parse_utc`는 이름만 있는 독립 식이며 `captured_at`으로 호출하지 않는다. 2교시는 작성 중 상태이고 snapshot 검사/소비 성공으로 기록하지 않는다. 이번 에이전트는 소스를 작성·완성·교정하지 않았다. 3~8교시 후속 소비 구현과 관리명령은 아직 없다.

## 책임과 모듈 값

게임 snapshot 파일 경계의 제공부/실습 문제틀이다. 광고에서 게임 ORM을 import하지 않고 공개 snapshot bytes를 읽는다. 현재 DB 접근/저장이나 전달 표식 호출은 없다.

`SCHEMA_VERSION="player-snapshot/v1"`, `SOURCE_KIND="player-snapshot"`, `PUBLIC_FIELDS=("id","room_id","coins","version","updated_at")`, `SNAPSHOT_FIELDS=set(PUBLIC_FIELDS)|{"schema_version","source_kind","captured_at"}`는 모듈이 정의한다. 현재 inspect 본문은 정확한 8필드·스키마·출처를 검사한다.

`hashlib`, `io`, `json`, `Path`, `.timestamps.parse_utc`는 현재 제공 helper에서 사용한다. `shutil`, `tempfile`, `datetime`, `timezone`, `.exporting.read_ndjson`, `.exporting.write_ndjson`은 import돼 있지만 현재 세 함수 본문에서는 호출하지 않는다. 앞으로의 구현 계획을 현재 호출 관계로 기록하지 않는다.

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

`path`는 기본값 없는 문자열/Path 호환 snapshot 입력 파일 경로다. 저장된 함수는 `_read_snapshot(path)`를 호출하고 `seen=set()`, `captured_at=None`을 초기화한 뒤 rows를 순회한다. 정확한 8필드, SCHEMA_VERSION/SOURCE_KIND 일치, 공개 상태 helper, ID 중복 검사가 작성돼 있다. 첫 captured_at 값을 보관하고 후속 값과 다르면 ValueError를 발생시킨다. captured_at이 None이면 계속 초기화 분기로 들어가는 현재 코드다.

의사코드(현재 실행): 입력 읽기/해시 → seen/captured_at 초기화 → 행별 8필드/스키마·출처 검사 → 공개 상태 검사 → ID 중복 거절/등록 → parse_utc 이름을 평가하고 버림 → 첫 수집값 보관/후속 값 비교 → 메타데이터 사전 반환.

현재 반환 사전은 `rows=len(rows)`, `public_ids=sorted(seen)`, `source_kind=SOURCE_KIND`, `schema_version=SCHEMA_VERSION`, `captured_at=captured_at`, `sha256=checksum`이다. public_ids는 등록한 정수 ID의 오름차순 목록이다. 빈 파일은 rows=0, public_ids=[], captured_at=None을 반환한다. 필드/출처/공개 값/중복/수집값 차이는 ValueError이며 읽기/JSON/updated_at 타입·파싱 오류는 전파한다.

현재 직접 호출은 `_read_snapshot`, `set`, `_check_public_state`, `seen.add`, 반환 분기의 `len`/`sorted`다. `rows`/`checksum`은 읽기 helper 반환값, `seen`은 빈 집합에서 ID를 등록하고 `captured_at`은 첫 입력 값에서 온다. `parse_utc`는 독립 이름 식으로만 등장하며 이 함수에서 호출하지 않는다.

수집 시각의 ISO 문법/시간대 확인은 현재 미적용이다. `_check_public_state`의 updated_at 검사와 captured_at 검사를 혼동하지 않는다. 잘못된 captured_at도 같은 값이면 이 함수의 수집 시각 검사에서 거절되지 않는다. 메타데이터 반환이 2교시 검사 통과나 실제 snapshot 소비 성공을 의미하지 않는다. 이번 문서 작업에서는 2교시 검사 실행이나 실제 snapshot 소비를 수행하지 않았다. 최초 빈칸 저장본은 당시 관찰 증거로 보존하며 현재 설명은 16:44경 저장본을 기준으로 한다.
