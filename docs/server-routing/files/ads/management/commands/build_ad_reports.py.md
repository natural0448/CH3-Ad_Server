# ads/management/commands/build_ad_reports.py

2026-10-08 검증이 끝난 현재 구현이다. 최신 23일차 교안의 관리 명령과 전체 AST가 일치한다. 기존 `Command` 클래스의 동작은 보존했고, 파일 아래에 있던 집계 함수는 교안 지정 위치 `ads/reporting.py`로 옮겼다. 집계 로직을 이 명령 문서에 복제하지 않는다.

## class Command(BaseCommand)

Django `build_ad_reports` 관리 명령이다. `help = "고정 광고 NDJSON에서 일별 보고서 후보를 계산합니다."`는 클래스가 정의한다. 고정 파일을 읽어 후보 파일을 만들며, MongoDB 게시를 호출하지 않는다. Django가 명령 인스턴스를 생성하고 아래 메서드를 호출한다.

## Command.add_arguments(self, parser)

`self`는 명령 인스턴스, `parser`는 Django가 제공하는 argparse parser다. 기본값은 없고 필수 문자열 경로 `--source`, `--output`을 등록한다. 경로의 의미는 입력 사건 NDJSON과 출력 보고서 NDJSON이며 상대경로 기준은 실행 작업 폴더다. 반환값은 `None`이다.

의사코드: `parser.add_argument("--source", required=True)` → `parser.add_argument("--output", required=True)`. 인수 누락 시 Django/argparse가 명령 사용법 오류를 보고한다.

## Command.handle(self, *args, **options)

`self`는 명령 인스턴스다. 추가 위치 인수 `args`는 사용하지 않으며, `options["source"]`와 `options["output"]`은 위 parser의 경로 문자열이다. 반환값은 `None`이다. 표준 출력에는 행 수 `rows`, 파일 SHA-256 `sha256`, 출력 경로 `path`를 포함하는 JSON을 쓴다.

의사코드: 사건 파일 읽기 → `ads.reporting.build_daily_reports(events)` 계산 → 보고서 파일 쓰기 → 메타데이터 JSON 출력. `rows`는 집계 함수가 반환한 보고서 목록, `checksum`은 출력 함수가 반환한 해시이며 메서드 내부에서만 쓴다.

직접 호출과 기대 결과:

- `ads.exporting.read_ndjson(options["source"])`: 사건 사전 목록. 파일 부재·JSON/입력 계약 오류는 전파한다.
- `ads.reporting.build_daily_reports(events)`: 일별 보고서 후보 사전 목록. 상세 검증은 [집계 모듈 문서](../../reporting.py.md)에 있다.
- `ads.exporting.write_ndjson(options["output"], rows)`: 파일 저장 후 SHA-256 문자열. 부모 폴더를 만들며 기존 출력 파일은 덮어쓴다. 쓰기 오류는 전파한다.
- `json.dumps(..., ensure_ascii=False)`와 `self.stdout.write`: 메타데이터를 표준 출력에 기록한다.

현재 파일명으로 확인한 실행:

```powershell
python ad_config/manage.py build_ad_reports --source data/exports/ad-events-day23-seoul-day.ndjson --output data/exports/ad-reports-day23.ndjson
```

2026-10-08 사건 4건 → 후보 1건, 서울 노출일 `2026-10-07`, 노출 2건·클릭 2건을 확인했다. 출력 파일은 실행 생성물이며 함수가 바뀐 것과 별도로 인수인계에 기록한다.
