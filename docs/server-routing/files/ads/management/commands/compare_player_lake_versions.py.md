# ads/management/commands/compare_player_lake_versions.py

26일차3교시 제공 전체 코드다. 시작 시 빈 사용자 파일에 적용했다. 두 보존 run의 입력·파일 지문을 비교하고 stdout JSON을 반환하며 파일과 DB를 쓰지 않는다.

## read_lake_manifest(folder)

folder는 기본값 없는 Lake run 경로(str/Path)다. 반환 player-lake/v1 manifest dict. 의사코드: root/manifest.json UTF-8 JSON 읽기 → schema 확인 → history/current record.path가 정해진 파일명인지 검사 → 실제 bytes SHA와 행 수 대조 → manifest 반환. 직접 호출 Path.read_text/read_bytes, json.loads, hashlib.sha256/hexdigest, payload.splitlines. 불일치는 ValueError, 누락 필드는 KeyError, I/O는 OSError다. manifest가 없는 불완전 run은 소비하지 않는다. root/manifest/record/payload는 호출 로컬값이며 실제 파일이 검증 기준이다.

## class Command(BaseCommand)

help는 보존한 두 Lake 버전의 입력·결과 파일 지문을 대조한다는 문자열이다. 진입점은 ad_config/manage.py compare_player_lake_versions다. source·result 파일 SHA를 비교하고 created_at/output_dir 차이는 허용한다.

## Command.add_arguments(self, parser)

parser는 기본값 없는 Django 파서, 반환 None. required=True의 --before/--after 문자열 인수만 등록한다. 인수는 NDJSON 자체가 아니라 manifest.json을 포함한 run 디렉터리며 상대경로는 cwd 기준이다. 직접 호출 parser.add_argument 두 번.

## Command.handle(self, *args, **options)

args는 미사용, options.before/after는 필수 run 경로다. 반환 None/stdout JSON. 의사코드: read_lake_manifest 두 번 → source_sha256 비교 → files.history/current의 path·rows·sha256 사전 비교 → input/history/current counts 포함한 결과 → stdout json.dumps(ensure_ascii=False). 직접 호출 read_lake_manifest, json.dumps, self.stdout.write. OSError/ValueError/KeyError/TypeError를 CommandError로 감싼다. before/after/result는 로컬값, matches는 실제 비교 bool이다. matches=false도 정상 비교 결과이며 exit0이고 읽기 실패는 CommandError다. snapshot 비교/--output 저장은 기존 compare_player_snapshots 책임이다.
