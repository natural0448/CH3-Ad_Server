# ads/management/commands/write_snapshot_contract.py

24일차 5교시의 사용자 작성 Command다. 게임의 기존 공개 snapshot을 읽어 인계 계약 JSON을 저장하고 stdout에도 출력한다. [공식 13/0](../../../../verification/2026-10-12-day24-period05-07-review/official-period05-final.json) 및 [실제 계약 대조](../../../../verification/2026-10-12-day24-period05-07-review/actual-file-verification.json)가 통과했다. 사용자 명령을 수정하거나 기존 계약 파일을 다시 쓰지 않았다.

## class Command(BaseCommand)

help는 "검사한 파일의 행 수·ID·체크섬을 인계 계약으로 저장합니다."다. Django 명령 이름은 write_snapshot_contract이며 실행 진입점은 ad_config/manage.py다. DB·게임 ORM을 직접 호출하지 않는다.

## Command.add_arguments(self, parser)

parser는 Django/argparse 파서이며 기본값 없이 필수 --source·--output 문자열 인수를 등록한다. 반환값은 None이다. source는 읽을 기존 NDJSON, output은 저장할 별도 JSON 경로다. 상대경로 기준은 프로세스 작업 폴더다.

직접 호출은 parser.add_argument 두 번이다. 의사코드: source 필수 등록 → output 필수 등록.

## Command.handle(self, *args, **options)

args는 Django가 전달한 위치 인수이며 사용하지 않는다. options["source"], options["output"]은 필수 파서 값이다. 반환값은 None, 부수효과는 계약 JSON 파일 쓰기와 stdout 쓰기다.

의사코드: build_snapshot_contract(source) → output Path 구성 → source와 resolve 경로가 같으면 ValueError → 부모 폴더 생성 → UTF-8/sort_keys/indent=2/newline JSON 저장 → stdout에 compact JSON 출력.

직접 호출: ads.snapshot_intake.build_snapshot_contract는 검사 메타데이터와 인계 조건의 사전을 반환한다. Path.resolve는 입력·출력 동일 경로 확인, Path.parent.mkdir(parents=True, exist_ok=True)는 출력 부모 준비, Path.write_text는 JSON 쓰기다. json.dumps와 self.stdout.write는 직렬화와 터미널 출력이다. OSError·ValueError·TypeError·KeyError를 CommandError(str(exc))로 연결하고 다른 예외는 전파한다. 입력 파일을 덮어쓰지 않도록 같은 경로를 거절한다. 기존 output이 있으면 write_text로 다시 쓴다.

result는 하위 함수 반환 사전, target은 options 출력 경로를 담은 Path다. 계약의 업무 필드·checksum 제공 책임은 하위 함수이며 이 계층에서 다시 계산하지 않는다.
