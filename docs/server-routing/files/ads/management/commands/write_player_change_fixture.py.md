# ads/management/commands/write_player_change_fixture.py

24일차 4교시의 사용자 저장본이다. 추가 개발 전에 현재 코드를 먼저 정합화했다. 교안의 Command 전체와 같은 구조로 교육 원문 r/u/d 세 행과 별도 해석 요약을 만든다. 실제 게임 Player나 광고 사건을 생성/삭제하지 않는다.

## class Command(BaseCommand)

상속은 django.core.management.base.BaseCommand다. help는 "실제 CDC와 구별한 r/u/d 교육 fixture와 해석 결과를 저장합니다."다. 함수 검사 성공 자체는 이 명령의 실제 출력 파일 저장 성공과 구분한다.

## Command.add_arguments(self, parser)

self는 명령 인스턴스, parser는 Django가 제공하는 ArgumentParser다. 기본값은 없으며 반환은 None이다. parser.add_argument로 --output(required=True), --summary(선택, 기본 None)를 등록한다. 입력은 문자열/Path 호환 경로이며 상대경로는 실행 작업 폴더 기준이다.

## Command.handle(self, *args, **options)

self는 명령 인스턴스다. args는 Django의 위치 인수이며 사용하지 않는다. options의 output은 필수 파일 경로, summary는 선택 파일 경로다. 반환은 None이며 result 사전을 JSON stdout으로 출력한다.

의사코드: 공개 원래 상태와 수정 상태 구성 → teaching-fixture r/u/d 원문 3개 구성 → summary와 output의 resolve 경로가 같으면 거절 → change_player 3회로 interpreted 구성 → write_ndjson(output,events) → path/source_kind/rows/sha256/interpreted 사전 구성 → 선택 summary 부모 폴더 생성/JSON 기록 → stdout JSON 출력.

직접 호출은 ads.snapshot_intake에서 가져온 change_player와 write_ndjson, Path.resolve/mkdir/write_text, json.dumps, self.stdout.write다. change_player는 해석 사전, write_ndjson은 실제 파일 bytes의 SHA-256 문자열을 반환한다. write_ndjson은 ads.exporting의 함수를 snapshot_intake가 import한 것을 사용한다. OSError/ValueError/TypeError/KeyError는 CommandError로 감싼다. 동일 출력 경로는 fixture 쓰기 전에 거절한다.

original은 id=1, room_id="room-01", coins=0, version=0, updated_at="2026-10-08T00:00:00+00:00"이다. updated는 coins=30, version=1, updated_at="2026-10-08T00:01:00+00:00"으로 이 명령이 구성한다. events는 출처 teaching-fixture, r(None/original), u(original/updated), d(updated/None)이다. result.rows=3, source_kind="teaching-fixture", path는 options.output, sha256은 write_ndjson 반환, interpreted는 change_player 반환 목록이다. 기대 coins/version/deleted는 0/0/False, 30/1/False, 30/1/True다.

summary는 UTF-8, ensure_ascii=False, sort_keys=True, indent=2, 마지막 newline으로 저장한다. stdout JSON은 ensure_ascii=False, sort_keys=True다. fixture 원문과 interpreted를 별도 파일/값으로 유지한다. 출력은 광고 서버 루트 data/fixtures에 두며 게임 snapshot 경로를 바꾸지 않는다.

2026-10-12 [공식 4교시 검사](../../../../verification/2026-10-12-day24-period04-recovery/official-period04-final.json) 17개가 통과했다. 실제 원문/summary 저장도 exit 0이며 3행·teaching-fixture·기대 interpreted·실제 SHA-256 일치를 [확인](../../../../verification/2026-10-12-day24-period04-recovery/actual-output-verification.json)했다. 이 사용자 명령의 소스는 수정하지 않았다.
