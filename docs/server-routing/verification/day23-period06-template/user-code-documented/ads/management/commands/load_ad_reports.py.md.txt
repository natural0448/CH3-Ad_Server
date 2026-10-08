# ads/management/commands/load_ad_reports.py

작업 시작 전에 존재한 사용자 코드다. 교안 6교시의 전체 관리 명령과 일치하며 이번 템플릿 작업에서 코드나 게시 동작을 변경하지 않는다.

## class Command(BaseCommand)

Django의 `load_ad_reports` 명령이다. 클래스 값 `help`는 "보고서 후보의 업무 키만 게시합니다. 다른 날짜 행은 유지합니다."이며 클래스가 소유한다.

## Command.add_arguments(self, parser)

`self`는 명령 인스턴스, `parser`는 Django가 제공하는 argparse parser이며 기본값은 없다. `parser.add_argument("--source", required=True)`를 직접 호출해 필수 문자열 NDJSON 경로를 등록한다. 상대경로는 실행 작업 폴더 기준이다. 반환값은 `None`; 인수 누락은 argparse/Django 오류다.

## Command.handle(self, *args, **options)

추가 위치 인수 `args`는 사용하지 않는다. `options["source"]`는 보고서 후보 파일 경로 문자열이다. 의사코드: `read_ndjson(source)` → `publish_reports(rows)` → `self.stdout.write(f"published={count}")`. 반환값은 `None`이며 표준 출력에 게시한 행 수를 기록한다.

직접 호출: `ads.exporting.read_ndjson`에서 사전 목록, `ads.reporting.publish_reports`에서 게시 수 정수를 기대한다. `count`는 게시 함수 반환값으로 해당 메서드가 소유한다. 파일/JSON/스키마/DB 오류는 전파한다. 업무 키별 upsert의 세부 계약은 reporting.py 짝 문서에 있으며 이 명령 문서에 DB 로직을 복제하지 않는다. 빈 후보는 게시 수 0이며 기존 행 삭제를 요청하지 않는다.

이번 작업은 사용자 실습 DB에 이 명령을 실행하지 않는다. 사용자가 직접 실행할 명령은 인수인계에 있다.
