# ads/management/commands/handoff_player_snapshot.py · 8교시 완료

사용자가 저장한 8교시 명령을 수정하지 않고 검증했다. [공식 24/0](../../../../verification/2026-10-12-day24-period08-finish/official-period08-before.json) 및 [실제 인계](../../../../verification/2026-10-12-day24-period08-finish/actual-handoff.json)가 통과했다. 기존 게임 원본과 5교시 계약을 새 data/exports/day24-input 수신 폴더에 함께 저장했다.

## class Command(BaseCommand)

help는 "검증한 원본과 계약을 새 수신 폴더에 함께 인계합니다."다. Django 명령 이름은 handoff_player_snapshot이다.

## Command.add_arguments(self, parser)

parser는 Django/argparse 파서다. 필수 --source·--contract·--target 문자열 인수를 등록하고 None을 반환한다. 각각 기존 원본 NDJSON·계약 JSON·새 수신 폴더 경로이며 기본값은 없다. 직접 호출은 parser.add_argument 세 번이다.

## Command.handle(self, *args, **options)

args는 사용하지 않는다. options의 source·contract·target을 handoff_snapshot에 전달하고 반환 사전을 stdout에 ensure_ascii=False/sort_keys=True/indent=2 JSON으로 출력한다. 반환값은 None이다.

직접 호출은 ads.snapshot_intake.handoff_snapshot(행 수/checksum/출처/target 사전), json.dumps, self.stdout.write다. OSError·ValueError·TypeError·KeyError는 CommandError(str(exc))로 연결한다. 실제 폴더/파일 쓰기는 하위 함수의 책임이며 이번 작업에서 광고 루트의 ad_config/manage.py를 통해 호출해 56행을 인계했다. 제공 명령은 compact JSON stdout이며 현재 사용자 코드는 indent=2다. 기능이 같고 검사가 통과해 출력 형식을 유지했다. result는 하위 반환 사전이다. 상대 입력·수신 경로 기준은 실행 폴더다.
