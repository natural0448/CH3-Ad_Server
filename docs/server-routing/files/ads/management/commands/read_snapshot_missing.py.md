# ads/management/commands/read_snapshot_missing.py

24일차 7교시의 사용자 작성 Command다. 동결 snapshot의 ID 누락을 관찰한 결과만 JSON으로 저장한다. [공식 10/0](../../../../verification/2026-10-12-day24-period05-07-review/official-period07-final.json) 및 [실제 누락 기록 대조](../../../../verification/2026-10-12-day24-period05-07-review/actual-file-verification.json)가 통과했다. 현재 missing_unknown=[]·delete_events=[]·delete_inference_allowed=False는 입력 파일과 일치하는 정상 결과다. 원본과 기존 결과를 다시 쓰지 않았다.

## class Command(BaseCommand)

help는 "스냅샷의 누락을 삭제 사건으로 바꾸지 않고 기록합니다."다. 이름은 read_snapshot_missing이며 ad_config/manage.py에서 실행한다. 삭제 API·DB 반영은 호출하지 않는다.

## Command.add_arguments(self, parser)

parser는 Django/argparse 파서다. 기본값 없는 필수 --before·--after·--output 문자열 인수를 등록하고 None을 반환한다. 앞의 두 값은 기존 snapshot 경로, output은 별도 결과 JSON 경로다. 직접 호출은 parser.add_argument 세 번이며 상대경로는 실행 폴더 기준이다.

## Command.handle(self, *args, **options)

args는 사용하지 않는다. options의 before·after·output은 필수 파서 값이다. 반환값은 None이며 JSON 파일과 stdout을 쓴다.

의사코드: 두 load_rows 결과 → missing_summary → output resolve가 before/after 중 하나면 ValueError → 부모 폴더 생성 → UTF-8/sort_keys/indent=2/newline JSON 저장 → stdout에 compact JSON 출력.

직접 호출은 ads.snapshot_intake.load_rows(검증된 ID 사전), missing_summary(누락 관찰과 삭제 추론 불가 사전), Path.resolve/parent.mkdir/write_text, json.dumps 및 self.stdout.write다. OSError·ValueError·TypeError·KeyError는 CommandError로 연결한다. 기존 output은 다시 쓸 수 있지만 입력과 같은 경로는 거절한다.

result는 하위 함수 반환 사전, target은 출력 Path다. delete_events 빈 목록과 delete_inference_allowed=False의 제공자는 missing_summary이며 이 명령은 실제 Player/MongoDB를 삭제하지 않는다.
