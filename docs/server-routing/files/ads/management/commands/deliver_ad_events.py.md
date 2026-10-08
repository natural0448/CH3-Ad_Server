# ads/management/commands/deliver_ad_events.py

현재 한 writer 파일 전달 명령이다. 실행하면 파일과 MongoDB의 전달 표식을 작성한다.

## class Command(BaseCommand)

Django의 `deliver_ad_events` 명령이며 클래스가 소유한 `help`는 "광고 실적을 한 writer의 로컬 파일로 전달합니다."다. import한 `ads.delivery`의 하단 실습 print가 명령 JSON 전에 출력될 수 있는 현재 부수효과는 [delivery 문서](../../delivery.py.md)를 따른다.

## Command.add_arguments(self, parser)

`self`는 명령 인스턴스, `parser`는 Django argparse parser이며 기본값은 없다. 직접 `parser.add_argument`로 필수 문자열 `--output`과 선택 정수 `--limit`(기본값 100)을 등록한다. 출력 상대경로는 실행 작업 폴더 기준이며 limit은 전달 함수에서 1 이상 정수로 검증한다. 반환값은 None이다.

의사코드: output 필수 등록 → limit int/default100 등록. CLI 입력 누락/정수 파싱 오류는 parser가 보고한다.

## Command.handle(self, *args, **options)

`self`는 명령 인스턴스, 위치 인수 `args`는 사용하지 않으며 `options["output"]`, `options["limit"]`은 CLI에서 온다. 반환값은 None이다.

의사코드: `ads.delivery.deliver_events(output, limit)` → processed/total/pending 사전 → `json.dumps(..., ensure_ascii=False)` → `self.stdout.write`.

직접 호출: `deliver_events`에서 결과 사전을 기대한다. `result`는 해당 반환값이며 메서드가 stdout을 작성한다. 파일/충돌/DB 오류는 전파한다. 전달 내부 로직은 하위 모듈 문서가 설명한다.
