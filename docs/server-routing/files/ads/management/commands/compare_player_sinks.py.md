# ads/management/commands/compare_player_sinks.py

4교시 진행 중 사용자가 작성한 실행 명령이다. 현재 코드를 보존하고 문서만 등록했다. 동일 원본과 검증된 Lake를 대조한 후 지정 매체 Mongo 공개 상태를 비교해 결과 JSON을 저장한다. 이 문서 등록은 실제 Mongo 대조 실행 완료를 뜻하지 않는다.

## class Command(BaseCommand)

help는 같은 원본·검증한 Lake와 지정 매체 Mongo 공개 상태를 대조한다는 문자열이다. 실행 진입점은 ad_config/manage.py compare_player_sinks다.

## Command.add_arguments(self, parser)

parser는 기본값 없는 Django 파서, 반환 None. --source/--lake-dir/--output 문자열 인수는 필수다. --media-id의 기본값은 settings.ADS_MEDIA_ID에서 온다. source는 정규화 입력, lake-dir는 manifest.json이 있는 완성 run, output은 별도 결과 JSON 경로다. 상대경로는 실행 cwd 기준이다. 직접 호출 parser.add_argument 네 번이다.

## Command.handle(self, *args, **options)

args는 미사용이고 options.source/lake_dir/output/media_id는 파서가 제공한다. 반환 None이며 결과 파일과 stdout JSON을 쓴다.

의사코드: Path 구성 → output이 원본·Lake3개 파일과 동일 resolve/samefile이면 거절 → read_lake_manifest → _read_context_changes → source SHA/행 수 일치 검사 → build_history/build_current 재계산 → 저장 history/current 내용과 변환 결과 일치 검사 → compare_context_to_current(current, media_id) → 결과 메타데이터 결합 → output 부모 mkdir → UTF-8/indent2 저장 → stdout에만 path 추가 후 출력.

직접 호출 read_lake_manifest는 실제 파일 SHA·행 수를 검증한다. _read_context_changes는 검증된 rows/checksum 두 값을, build_history/build_current는 메모리 결과 목록을, read_ndjson은 저장 행 목록을, compare_context_to_current는 공개 비교 사전을 반환한다. Path.resolve/exists/samefile/mkdir/write_text, json.dumps와 stdout.write도 직접 호출한다. OSError/ValueError/KeyError/TypeError/PyMongoError는 CommandError로 감싼다.

source/lake_dir/output/protected/lake/rows/checksum/history/expected/current/compared/result는 호출 로컬값이다. same_source_verified=True는 위 검사를 통과한 결과이며 Mongo 입력 범위 일치와 구별한다. lake_current_sha256는 검증 manifest에서 온다. 기존 output은 다시 쓸 수 있고 파일 JSON에는 stdout 전용 path 키가 없다. 원본·Lake·Mongo를 수정하지 않는다. 현재 완성 Lake는 run-003/004이고 run-001/002에는 manifest가 없다.
