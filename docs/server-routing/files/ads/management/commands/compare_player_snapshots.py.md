# ads/management/commands/compare_player_snapshots.py

24일차 6교시의 사용자 작성 Command다. 검증한 동결 파일 두 개의 공개 상태를 ID 기준으로 비교해 JSON에 저장한다. [공식 15/0](../../../../verification/2026-10-12-day24-period05-07-review/official-period06-final.json) 및 [실제 비교 대조](../../../../verification/2026-10-12-day24-period05-07-review/actual-file-verification.json)가 통과했다. 각 56행의 입력에서 changed 1건·newly_seen/missing_unknown 각 0건이 저장 결과와 일치한다. 원본과 기존 결과를 다시 쓰지 않았다.

## class Command(BaseCommand)

help는 "동결된 두 파일의 공개 상태를 ID 기준으로 비교합니다."다. 이름은 compare_player_snapshots, 실행 진입점은 ad_config/manage.py다. 직접 DB·게임 ORM 호출은 없다.

## Command.add_arguments(self, parser)

parser는 Django/argparse 파서이며 필수 --before·--after·--output 문자열 인수를 등록한다. 반환값은 None이다. before/after는 수집 시점이 다른 기존 snapshot 경로, output은 별도 결과 JSON 경로다. 상대경로는 실행 폴더 기준이다. 직접 호출은 parser.add_argument 세 번이다.

## Command.handle(self, *args, **options)

args는 사용하지 않는 Django 위치 인수다. options의 before·after·output은 파서가 제공하는 필수 값이다. 반환값은 None이며 결과 파일과 stdout을 쓴다.

의사코드: load_rows(before)/load_rows(after) → compare 두 ID 사전 → output이 두 입력 resolve 중 하나면 거절 → 부모 폴더 준비 → UTF-8/sort_keys/indent=2/newline 저장 → stdout에도 indent=2 JSON 출력.

직접 호출은 ads.snapshot_intake.load_rows(검증된 ID→행 사전), compare(변경·새 ID·원인 미상 누락 사전), Path.resolve/parent.mkdir/write_text, json.dumps, self.stdout.write다. OSError·ValueError·TypeError·KeyError를 CommandError로 연결한다. 출력이 입력과 같은 경로면 ValueError다. 기존 output은 재실행 시 다시 쓴다. 원본을 수정하거나 사라진 Player를 삭제하지 않는다.

result는 compare 반환 사전, target은 출력 Path다. 상태 비교의 세부 구현은 하위 함수가 맡는다. 교안 제공 Command의 stdout은 compact JSON이지만 현재 사용자 파일은 indent=2로 여러 줄 출력한다. 키·값·파일 JSON은 같은 계약이며 이 차이를 보존했다.

## 2026-10-14 복구 검증

26일차3교시 검토 시작 시 Lake 비교 코드가 잘못 붙여져 --output 및 snapshot 비교가 사라져 있었다. 시작 소스는 verification/day26-period03.json의 source_before에 보존했고, 현재 코드는 직전 커밋 d68b511의 기존 snapshot 비교와 같다. 복구 회귀검사는 두 입력 보존·changed1·JSON 결과 저장·출력 경로가 입력이면 거절을 확인했다. Lake 비교는 별도 compare_player_lake_versions 명령이 맡는다.
