# ads/management/commands/inspect_player_snapshot.py

사용자가 작성해 커밋한 24일차 2교시 실행 연결 명령이다. 공개 snapshot을 `ads.snapshot_intake.inspect_snapshot`으로 검사하고 결과 JSON을 stdout에 출력한다. 파일·DB를 쓰지 않으며 게임 ORM을 import하지 않는다. 2026-10-12 공식 검사 22개와 실제 56행 원본 검사에서 정상 실행됐다.

## class Command(BaseCommand)

기반 클래스는 Django `BaseCommand`다. 클래스 값 `help="저장된 플레이어 공개 스냅샷을 검사합니다."`는 이 파일이 정의하는 설명 문자열이다. 명령 이름은 Django의 모듈 파일명에서 오는 `inspect_player_snapshot`이다. 생성·실행 수명은 Django 관리명령 계층이 소유한다.

## Command.add_arguments(self, parser)

`self`는 현재 명령 인스턴스, `parser`는 Django가 제공한 argparse 호환 명령 파서다. 기본값 없는 필수 옵션 `--source`를 등록하고 None을 반환한다. source는 입력 NDJSON 파일 경로 문자열이며 문자열/Path 변환과 실제 검사는 호출하는 하위 함수가 담당한다.

의사코드: parser.add_argument("--source", required=True) → 암묵적으로 None 반환.

직접 호출은 `parser.add_argument`다. 사용자 인수에서 source 옵션이 없으면 파서가 명령 실행 전에 거절한다. source 값은 사용자 옵션에서 오며 이 계층이 기본 경로를 정하지 않는다.

## Command.handle(self, *args, **options)

`self`는 현재 명령, `args`는 Django 위치 인수(본문에서 사용하지 않음), `options`는 관리명령 옵션 사전이다. `options["source"]`를 검사 함수에 전달한다. 직접 호출이나 CLI에서 source 값이 있어야 하며, 상대 경로는 프로세스 실행 폴더 기준이다.

반환값은 성공 시 None이고 stdout에는 `rows`, `public_ids`, `source_kind`, `schema_version`, `captured_at`, `sha256`을 포함하는 JSON 한 줄이 출력된다. result는 inspect_snapshot 반환 사전이며 이 명령이 다른 Player 값을 추가하지 않는다.

의사코드: try inspect_snapshot(options["source"]) → OSError/ValueError/TypeError/KeyError를 CommandError로 전파 → json.dumps(ensure_ascii=False, sort_keys=True) → self.stdout.write → None.

직접 호출과 기대 결과:

- `ads.snapshot_intake.inspect_snapshot`: 검증된 공개 메타데이터 사전 또는 검사 예외. 입력 검증 내부 구현은 그 짝 문서가 설명한다.
- `CommandError(str(exc))`: 위 네 가지 예외를 관리명령의 실패 종료로 연결하고 원인 예외를 유지한다.
- `json.dumps`: 키를 정렬한 UTF-8 표현용 JSON 문자열.
- `self.stdout.write`: Django stdout에 JSON을 출력한다.

## 현재 실행 위치와 검증

```powershell
cd C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python ad_config/manage.py inspect_player_snapshot --source C:\MLO01-01\Chapter3\Game-server\data\exports\player-cdc.ndjson
```

실제 파일은 Game-server의 기존 루트 data 폴더에 있다. 교안 예시 `game_server` 대신 실제 `Game-server` 이름을 사용한다. `server/data`를 생성하거나 원본을 다시 export하지 않는다. 검사 자체에는 MongoDB·게임 DB·Django runserver 기동이 필요하지 않는다.

[현재 실제 원본 결과](../../../../verification/2026-10-12-day24-period01-02/actual-snapshot-inspection.json): exit 0, 56행, checksum 일치. 원본 해시는 snapshot 생산·소비 계층의 증거이며 실시간 DB 최신 상태나 binlog CDC 실행 증거가 아니다.
