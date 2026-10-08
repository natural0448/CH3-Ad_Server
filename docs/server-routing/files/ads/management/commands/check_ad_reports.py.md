# ads/management/commands/check_ad_reports.py

고정 사건 입력에서 다시 계산한 보고서와 현재 게시된 전체 MongoDB 보고서를 대조하는 현재 23일차 8교시 관리명령이다. DB는 조회하고 결과 JSON 파일만 작성한다. 일부 날짜 파일만 넣으면 다른 날짜의 게시 행이 extra로 잡힐 수 있으므로 입력 의미는 전체 보관 사건이다.

## class Command(BaseCommand)

Django `check_ad_reports` 명령이다. 클래스가 정의한 `help`는 "전체 보관 사건의 고정 입력과 게시 보고서를 대조합니다."다.

## Command.add_arguments(self, parser)

`self`는 명령 인스턴스, `parser`는 Django argparse parser이며 기본값은 없다. 직접 `parser.add_argument`로 필수 문자열 `--source`(전체 사건 NDJSON), `--output`(대조 결과 JSON)을 등록한다. 상대경로는 실행 작업 폴더 기준이다. 반환값은 None이며 인수 누락은 parser 오류다.

의사코드: source 필수 등록 → output 필수 등록.

## Command.handle(self, *args, **options)

`self`는 명령 인스턴스, 추가 위치 인수 `args`는 사용하지 않으며 `options`는 CLI parser 값이다. 반환값은 성공 시 None이다. 불일치면 결과 파일을 먼저 저장한 뒤 `CommandError("검사 결과를 확인하세요.")`를 발생시킨다. 성공 JSON을 stdout에 따로 쓰지 않는다.

의사코드: source 읽기 → `build_daily_reports` 후보를 _id별 사전으로 만들기 → 게시 컬렉션 전체 조회를 _id별 사전으로 만들기 → 누락/추가/공통 키의 지표 불일치 정렬 → 입력 해시·관찰 메타데이터·판정 JSON 저장 → 불일치면 CommandError.

직접 호출과 기대 결과: `ads.exporting.read_ndjson`은 사건 목록, `ads.reporting.build_daily_reports`는 후보 목록, `ads.mongo.get_db().ad_daily_reports.find()`는 게시 문서 cursor, `hashlib.sha256(source.read_bytes()).hexdigest()`는 입력 파일 해시, `datetime.now(timezone.utc).isoformat()`는 관찰 시각, `target.parent.mkdir`/`target.write_text`는 UTF-8 결과 파일 저장이다. DB 게시 함수를 호출하지 않는다.

`expected`/`actual`은 각 계산/조회 결과로 만들고 `fields=("impressions", "clicks", "ctr", "bid_units_sum", "source_max_event_time")`만 값을 대조한다. `generated_at`은 비교하지 않는다. `missing`, `extra`, `different`는 업무 _id 문자열 목록이며 비어 있으면 `ok=True`다. `source_rows`는 파일 행 수, `unique_events`는 event_id 종류 수다. 고정 메타데이터는 `artifact_id="village-lab.ads-analytics"`, `artifact_version="v2"`, `source_kind="ad-events"`, `transport="file"`, `spark_ad_job_status="not-configured"`, `gui_status="separate-manual-observation"`다. `result`, `target`은 메서드가 소유한다. Spark 실행이나 GUI 관찰을 성공으로 판단하는 검사로 확대 해석하지 않는다. 파일/JSON/집계/필드/DB 오류는 전파한다.
