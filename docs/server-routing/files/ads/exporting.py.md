# ads/exporting.py

광고 사건의 공개 필드만 NDJSON으로 저장하는 현재 23일차 4교시 모듈이다. 게임 Player snapshot 입력과는 별개다. 상대 파일 경로는 실행 작업 폴더 기준이며 이 모듈은 DB에 쓰지 않는다.

`EVENT_FIELDS`는 모듈이 정의한 튜플이다: `schema_version`, `event_id`, `decision_id`, `event_type`, `event_time`, `impression_time`, `media_id`, `subject`, `slot_id`, `campaign_id`, `owner_user_id`, `bid_amount`. `_id`, `file_delivered_at`은 공개 출력에서 제외한다.

## read_ndjson(path)

`path`는 기본값 없는 문자열 또는 Path 호환 파일 경로다. 반환값은 행 순서대로 읽은 사전 목록이며 빈 파일은 빈 목록이다. 빈 행과 사전이 아닌 JSON 행은 행 번호를 포함한 `ValueError`다. 파일/UTF-8/JSON 오류는 전파한다. 사건/보고서 스키마 자체는 검사하지 않는다.

의사코드: UTF-8 파일 열기 → 각 행의 공백 여부 확인 → JSON 파싱 → 사전 확인 → rows 추가 → 목록 반환.

직접 호출: `Path(path).open(encoding="utf-8")`에서 읽기 스트림, `enumerate(stream, 1)`에서 행 번호, `json.loads(line)`에서 JSON 값을 얻는다. `rows`는 빈 목록으로 시작하고 함수만 작성한다. `number`, `line`, `row`는 읽은 파일에서 온다.

## write_ndjson(path, rows)

`path`는 기본값 없는 문자열 또는 Path 호환 출력 경로다. `rows`는 기본값 없는 JSON 직렬화 가능 행 iterable이며 이 함수 자체는 사전 타입이나 스키마를 검사하지 않는다. 반환값은 저장 파일의 SHA-256 64자리 문자열이다. 기존 파일을 덮어쓰며 부모 폴더를 생성한다. 파일/직렬화 오류는 전파한다.

의사코드: Path 생성 → 부모 생성 → UTF-8 출력 파일 열기 → `ensure_ascii=False`, `sort_keys=True` JSON과 LF를 행마다 쓰기 → 저장 bytes의 SHA-256 반환.

직접 호출: `Path`, `target.parent.mkdir(parents=True, exist_ok=True)`, `target.open("w", encoding="utf-8", newline="\n")`, `json.dumps`, `stream.write`, `target.read_bytes`, `hashlib.sha256(...).hexdigest()`. `target`은 인수 경로, `row`는 입력 iterable에서 얻고 해당 함수가 파일 쓰기를 소유한다. 이 함수 자체는 임시 파일 교체를 하지 않는다.

## export_ad_events(output_path, since=None, until=None)

`output_path`는 필수 출력 경로다. `since`, `until`의 기본값은 `None`이며 값이 있으면 시간대 포함 ISO 문자열이다. 거짓 값은 해당 경계 없음으로 취급한다. 두 경계가 있으면 `since < until`이어야 한다. 선택 기준은 사건 발생 시각이 아니라 `impression_time`의 `[since, until)` 범위다. 같은 노출에 귀속된 클릭을 함께 내보내기 위한 현재 계약이다.

반환값은 `path`, `rows`, `sha256`, `schema_version="ad-event/v1"`, `source_kind="ad-events"`, UTC ISO `since`/`until`(경계 없으면 None)을 포함한 사전이다. DB/시각/필드 누락/파일 오류는 전파한다.

의사코드: 범위 시각 파싱/순서 검증 → ad_events 조회 → 노출 기준 범위 필터 → EVENT_FIELDS 투영 → 파싱된 UTC event_time/event_id 정렬 → NDJSON 저장 → 메타데이터 반환.

직접 호출: `.timestamps.parse_utc`에서 UTC datetime, `.mongo.get_db().ad_events.find().sort(...)`에서 사건 cursor, `rows.sort`에서 최종 순서, `write_ndjson`에서 SHA-256을 기대한다. `start`/`end`는 인수에서, `event`는 DB에서, `rows`는 빈 목록에서 공개 투영 행으로, `checksum`은 파일 writer에서 얻으며 함수 내부에서 작성한다. `export_ad_events`는 전달 표식을 쓰지 않는다.
