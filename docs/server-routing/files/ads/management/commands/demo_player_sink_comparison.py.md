# ads/management/commands/demo_player_sink_comparison.py

4교시 진행 중 사용자가 작성한 메모리 fixture 명령이다. 코드 변경 없이 현재 내용대로 등록했다. 실제 Player·Mongo 데이터와 분리한 공개 상태 대조의 정상·차이 사례다.

## class Command(BaseCommand)

help는 별도 메모리 fixture로 공개 상태 대조의 정상·차이를 확인한다는 문자열이다. 진입점은 ad_config/manage.py demo_player_sink_comparison이다.

## Command.add_arguments(self, parser)

parser는 기본값 없는 Django 파서, 반환 None. 필수 --case의 choices는 same/missing/newer/extra/duplicate/invalid다. 직접 호출 parser.add_argument 한 번이다.

## Command.handle(self, *args, **options)

args는 미사용, options.case는 위 허용 사례 문자열이다. 반환 None/stdout JSON이다.

의사코드: version2/coins20 fixture 공개 문서 expected 생성 → actual 복사 → case에 따라 빈실제·최신4·추가키·중복·잘못된 문서 구성 → compare_rows → case/source_kind=teaching-fixture/database_changed=False 결합 → stdout 출력. extra는 subject_id와 context.player_id를 fixture-extra로 바꾸고 stable_json 본문의 SHA로 change_id를 다시 만든다.

직접 호출 fixture_change, make_context_document, stable_json, hashlib.sha256/hexdigest, compare_rows, json.dumps와 stdout.write다. ValueError/KeyError/TypeError는 CommandError다. expected/actual/case/change/result는 호출 로컬값이다. missing/newer는 입력 범위 False, extra는 입력 범위 True와 추가키가 함께 나올 수 있다. 실제 DB·파일·입력에 쓰거나 game ORM을 조회하지 않는다.
