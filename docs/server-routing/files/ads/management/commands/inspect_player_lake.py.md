# ads/management/commands/inspect_player_lake.py

26일차1교시 제공 명령 전체와 AST가 같다. 고정 파일·인계 manifest/완료 checkpoint를 검사하여 history 또는 current의 미리보기/목록 지문을 출력한다. 저장과 Mongo 조회는 하지 않는다.

## class Command(BaseCommand)

help 초기값은 고정 입력의 history/current를 저장 없이 미리 봅니다. 옵션 작성자는 이 클래스다.

## Command.add_arguments(self, parser)

self는 Command 인스턴스, parser는 Django ArgumentParser이고 기본값 없다. 반환 None. 필수 --source 문자열, --manifest(default None), --stage(history/current, default history), --repeat(int, default1), --reverse(store_true, defaultFalse)를 등록한다. 직접 호출 parser.add_argument다.

## Command.handle(self, *args, **options)

args는 미사용 Django 위치 인수, options는 위 옵션 사전이다. 반환 None, stdout은 stage/source/source_sha256/input_rows/supplied_rows/history_rows/result_rows/result_sha256/preview/written JSON이다. repeat는1 이상이다. 의사코드: _read_context_changes로 실제 bytes/행 계약 검사 → manifest를 주면 입력SHA·행수·schema·출처·매체·완료checkpoint 대조 → 메모리에서만 rows 반복/역순 → build_history → current stage만 build_current lazy import/계산 → stable_json 결과목록의 SHA·첫행(없으면[])·written=False → stdout. 직접 호출은 _read_context_changes, _read_context_checkpoint, Path.read_text, JSON, build_history, build_current, stable_json, hashlib.sha256와 self.stdout.write다. OSError/ValueError/TypeError/KeyError는 CommandError다.

원본source SHA와 result목록 SHA 및 다음 교시NDJSON 파일 SHA는 다르다. --repeat/--reverse는 파일에 덧쓰지 않는다. manifest.checkpoint_path는 기존 광고 작업 폴더 기준이며 같은 파일SHA와 next_line=input_rows를 요구한다. 결과의 숫자는 입력 범위만 뜻한다.
