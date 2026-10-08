# ads/management/commands/export_ad_events.py

현재 광고 사건 내보내기 진입점이다. 게임 snapshot 관리명령과 분리돼 있다.

## class Command(BaseCommand)

Django가 생성하는 `export_ad_events` 명령이다. 클래스가 정의한 `help`는 "공개 광고 사건을 [since, until) NDJSON으로 내보냅니다."다.

## Command.add_arguments(self, parser)

`self`는 명령 인스턴스, `parser`는 Django argparse parser이며 기본값은 없다. 직접 `parser.add_argument`를 호출해 필수 문자열 `--output`, 선택 문자열 `--since`/`--until`(미지정 None)을 등록한다. 출력 경로는 실행 작업 폴더 기준이다. 시각 범위의 허용값/검증은 [exporting 문서](../../exporting.py.md)의 계약이다. 반환값은 None이며 필수 인수 누락은 parser 오류다.

의사코드: output 필수 등록 → since 선택 등록 → until 선택 등록. 옵션 정의는 이 메서드가 소유하고 실제 값은 CLI에서 온다.

## Command.handle(self, *args, **options)

`self`는 명령 인스턴스, 위치 인수 `args`는 사용하지 않고 `options`는 parser가 만든 사전이다. `output`, `since`, `until`을 사용한다. 반환값은 None이다.

의사코드: `ads.exporting.export_ad_events(output, since, until)` → 결과 사전을 `json.dumps(..., ensure_ascii=False)` → `self.stdout.write`.

직접 호출: `export_ad_events`에서 파일/행 수/해시/스키마/범위 메타데이터 사전을 기대한다. `result`는 이 반환값이며 메서드가 출력만 소유한다. 파일/입력/DB 오류는 전파한다. 전달 표식이나 보고서 게시를 호출하지 않는다.
