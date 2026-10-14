# ads/management/commands/build_player_lake.py

26일차3교시 사용자 작성 명령이며 제공 코드와 같다. 동결 입력에서 새 Lake run을 만들고 결과 manifest를 stdout으로 출력한다.

## class Command(BaseCommand)

help는 고정 입력에서 새 NDJSON Player Lake 버전을 만든다는 문자열이다. 실행 진입점은 ad_config/manage.py build_player_lake다.

## Command.add_arguments(self, parser)

parser는 기본값 없는 Django 파서다. --source/--output을 required=True로 등록한다. 반환 None. 각각 읽을 입력 경로와 아직 없는 출력 run 경로다. 상대경로는 실행 cwd 기준이다. 직접 호출 parser.add_argument 두 번.

## Command.handle(self, *args, **options)

args는 미사용, options.source/output은 필수 경로 문자열이다. 반환 None/stdout JSON. 의사코드: build_lake_version(source, output) → result → json.dumps(ensure_ascii=False) → stdout.write. 직접 호출 ads.lake_files.build_lake_version은 저장한 manifest dict를 반환한다. OSError/ValueError/KeyError/TypeError를 CommandError로 감싼다. 이 계층은 변환·파일 지문 계산을 복제하지 않는다. DB 호출 없음.
