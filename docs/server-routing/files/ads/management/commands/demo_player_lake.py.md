# ads/management/commands/demo_player_lake.py

26일차1교시 제공 fixture helper/Command와 AST가 같다. teaching-fixture의 메모리 변경으로 중복·최신version·삭제·충돌·빈 입력을 관찰하며 실제 Player/Mongo/광고 선택을 실행하지 않는다.

## fixture_change(version, coins=10, op='upsert')

version은 기본값 없는 fixture 정수(명령에서1/2/4 사용), coins는 정수 기본10, op는 기본upsert이며 명령의 delete 사례에서delete를 사용한다. 반환은 player-context-change/v1의9필드 dict다. 의사코드: 고정2026-10-14 UTC 시각의 초를version으로 구성 → delete면{} 아니면 공개5필드context → village-game/fixture-lake/teaching-fixture 사전 → stable_json 내용 SHA를change_id에 추가 → 반환. 직접 호출 stable_json/hashlib.sha256다. 일반 입력검사는 downstream build_history/make_context_document가 맡으며 임의의 큰version이 유효한 초 문자열이라고 보장하지 않는다.

## class Command(BaseCommand)

help는 메모리의 별도 fixture로 Lake 중복·버전·삭제·거절을 관찰합니다. fixture의 쓰기 소유자는 이 호출의 rows 지역값이고 DB쓰기는 없다.

## Command.add_arguments(self, parser)

self는 Command, parser는 기본값 없는ArgumentParser다. 반환 None. 필수 --case 문자열에 duplicates/invalid-schema/change-id-conflict/versions/delete/version-conflict/empty 선택지를 등록한다. 직접 호출 parser.add_argument다.

## Command.handle(self, *args, **options)

args는 미사용 Django 위치인수, options.case는 위 사례다. 반환 None이고 stdout은 case/source_kind/input_rows/history_rows/current_rows/current/written=False/database_changed=False JSON이다. 의사코드: fixture version1/4/2 생성 → 선택사례에 맞춰 목록 구성 → build_history → duplicates 외의 정상사례는 build_current lazy import/계산 → stdout. 직접 호출 fixture_change/build_history/build_current/json.dumps/self.stdout.write이며 ValueError/TypeError/KeyError는 CommandError다. duplicates의 current=[]는1교시 history만 관찰하기 위한 제공 동작이다. 잘못된schema/내용SHA/같은version의 다른상태는 정상요약 없이 거절된다. 실패 후보를 다음 호출에 보관하지 않는다.
