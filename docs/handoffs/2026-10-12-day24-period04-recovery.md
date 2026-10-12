# 24일차 4교시까지 확인·복구 · 2026-10-12

## 요청과 완료 결과

사용자의 “4교시까지 진행했는데 잘못하거나 놓친 것이 있다면 복구” 요청과 “직접 입력했어 확인해봐” 응답에 따라 Desktop의 수정 교안 ‘실제 Player snapshot을 광고 서버에서 검증하고 인계하기.html’ 1~4교시를 현재 구현과 비교했다. 4교시 change_player와 write_player_change_fixture는 이미 교안 AST와 같아 그대로 보존했다. readiness 반환에서 누락된 player_change_topic="not-configured", common_input=SCHEMA_VERSION만 보완했다. 사용자가 직접 입력한 3교시 write_cdc_readiness 클래스는 수정하지 않았다.

교안 화면 제공 검사 파일을 원문 그대로 추가하고 준비 JSON·fixture 원문·summary를 저장했다. 공식 최종 2교시 22/0, 3교시 8/0, 4교시 17/0과 화면 검사 exit 0으로 확인했다. 5~8교시 기능은 미적용이다. 계획을 현재 구현으로 기록하지 않는다.

## 작업 시작 Git 상태와 사용자 작업 구분

Chapter3 루트는 `Git 상태 확인 불가: 저장소 아님`이다. 광고 서버는 별도 저장소이며 HEAD는 `5d29085 day24 - 2교시`, staged는 없었다. 시작 시 unstaged는 README.md, ads/snapshot_intake.py, current-progress-index.md, day24-period01-index.md, files/README.md.md, files/ads/snapshot_intake.py.md, files/tools/check_day24_logic.py.md였다. 기존 untracked 개발 파일은 write_cdc_readiness.py(처음에는 빈 파일), write_player_change_fixture.py였다. 이전 검증·라우팅·Mongo 인수인계도 untracked로 존재했다. 전체 목록과 76개 개발 파일의 시작 해시는 [시작 기록](../server-routing/verification/2026-10-12-day24-period04-recovery/start.json)에 보존했다. 이를 이번 에이전트 작업으로 주장하지 않는다.

사용자가 작업 중 write_cdc_readiness.py를 직접 채웠다. [동시 작성 관찰](../server-routing/verification/2026-10-12-day24-period04-recovery/concurrent-user-command.json)의 SHA-256 e18ddd6be63d161f4753e2a943703fefca91f5cd9ad2d5d5c76275de5faa667b와 최종 파일을 대조한다. fixture 명령의 기존 SHA-256은 00722c21d2cd3050e7528b5dbcbf62b83fabbae83caf0511659bc33e183e4f73이며 보존했다. Git add/commit/reset은 수행하지 않았다.

## 이번 변경 파일

- ads/snapshot_intake.py: readiness 반환에 교안 필드 두 개를 한 줄 추가. 저장 시 파일 끝 개행도 추가됐다. 이 두 부분을 제외한 bytes는 시작 파일과 일치하며 기존 inspect_snapshot, change_player와 경로 관찰 로직을 보존했다.
- check_day24_period4.py: 교안 화면 제공 검사 코드 전체를 그대로 추가. [제공 원문](../server-routing/verification/2026-10-12-day24-period04-recovery/provided-check-day24-period4.txt)과 동일한 bytes.
- README.md: 24일차 현재 진행 안내 한 문단만 갱신. 기존 변경 보존.
- data/contracts/cdc-readiness.json, data/fixtures/player-change-fixture.ndjson, data/fixtures/player-change-summary.json: 없음을 확인한 뒤 실제 관리명령으로 생성한 출력. 마감 시 준비 JSON의 connect_home은 supplied=true·exists=false로 관찰했다. 이후 실행으로 바뀔 수 있는 파일이며 그 현재 값을 보존했다.
- 아래 라우팅 문서·색인, 이 인수인계 및 이번 검증 증거를 추가/갱신. 파일 이동·삭제와 Game-server 개발 변경은 없다.

## 책임과 구조

게임의 기존 동결 입력은 ../Game-server/data/exports/player-cdc.ndjson, 56행·13,275 bytes, SHA-256 6ea30948a1c6924b186676511207bd2099683ca00cf1b1582cb595e6437375d0이며 bytes를 보존했다. Game-server/server/data는 만들지 않았다. 광고 출력은 기존 광고 프로젝트 루트 data를 사용한다. 광고에서 게임 ORM을 import하지 않는다.

readiness는 경로 supplied/exists와 not-configured/not-verified 상태를 구분한다. 폴더 존재를 CDC 실행 성공으로 처리하지 않는다. change_player는 teaching-fixture 공개 상태만 해석하며 d는 deleted=True를 반환한다. fixture 생성은 실제 Player·MongoDB를 수정하거나 삭제하지 않는다. 예제 coins=30은 교안 고정값으로 실제 게임 보상 규칙을 바꾸지 않는다. 기존 MongoDB 실행 복구는 [별도 인수인계](2026-10-12-mongodb-connection-recovery.md)이며 이번 작업에서 서버를 재시작하지 않았다.

## 라우팅 문서 정합화

개발 전 사용자 change_player와 두 관리명령을 현재 코드에 맞춰 먼저 기록했다. 코드 검사 후 별도 마감 단계에서 다음 짝 문서를 실제 최종 구현과 맞췄다.

- files/ads/snapshot_intake.py.md
- files/ads/management/commands/write_cdc_readiness.py.md
- files/ads/management/commands/write_player_change_fixture.py.md
- files/check_day24_period4.py.md
- files/README.md.md 및 files/tools/check_day24_logic.py.md
- files/data/contracts/cdc-readiness.json.md, files/data/fixtures/player-change-fixture.ndjson.md, files/data/fixtures/player-change-summary.json.md

모두 docs/server-routing 아래다. current-progress-index.md, day24-period01-index.md 및 Chapter3/docs/routing/README.md도 현재 2~4교시 완료 상태로 갱신했다. 과거 3/5 실패와 빈 명령 관찰은 역사 기록으로 보존했다. 마지막 문서·Git 검사는 [마감 기록](../server-routing/verification/2026-10-12-day24-period04-recovery/finish.json)을 따른다.

## 검사 명령과 결과

공식 tools/check_day24_logic.py에 절대 광고 프로젝트 경로와 --period 2/3/4, 각 --output 증거 경로를 전달했다. 샌드박스 임시 경로 제한 때문에 process-local tempfile.tempdir를 이번 증거 폴더로 지정하고 runpy로 실행했다. 공식 검사기·학생 명령 소스를 바꾸지 않았다.

| 검사 | 결과 |
|---|---|
| [공식 2교시](../server-routing/verification/2026-10-12-day24-period04-recovery/official-period02-final.json) | 22 통과·0 실패 |
| [공식 3교시](../server-routing/verification/2026-10-12-day24-period04-recovery/official-period03-final.json) | 8 통과·0 실패 |
| [공식 4교시](../server-routing/verification/2026-10-12-day24-period04-recovery/official-period04-final.json) | 17 통과·0 실패 |
| python check_day24_period4.py | [exit 0, 정상/거절/입력 보존 PASS](../server-routing/verification/2026-10-12-day24-period04-recovery/screen-checker-final.json) |
| python ad_config/manage.py write_cdc_readiness --output data/contracts/cdc-readiness.json | exit 0, 준비 JSON 저장 |
| python ad_config/manage.py write_player_change_fixture --output data/fixtures/player-change-fixture.ndjson --summary data/fixtures/player-change-summary.json | exit 0, 원문 3행·summary 저장 |
| [출력 대조](../server-routing/verification/2026-10-12-day24-period04-recovery/actual-output-verification.json) | 해석·행 수·checksum 일치, 기존 게임 원본 및 사용자 명령 보존 |

이번 공식 최종 검사는 총 47개다. 1교시 공식 12/0은 같은 날짜 앞선 검토 결과이며 이번에 재실행하지 않았다. 공식 검사기는 SQLite 메모리 및 Mongo mock을 사용했다. Python 환경의 경로 경고와 검사기 mock에 대한 atexit 경고는 종료 코드 0·위 PASS와 별도 관찰이다.

## 실행하지 않은 검사와 제한

라우팅 표준 CLI는 기존 docs/server-routing/README.md를 필수로 요구하지만 해당 파일이 HEAD에도 없다. 이를 임의 생성하지 않고 현재 색인과 스킬의 AST API로 범위 내 짝 문서·시그니처·경로를 검사한다. API 성공을 표준 CLI 성공으로 기록하지 않는다. 공식 3교시 Command 다운로드 링크의 로그인 제한은 사용자가 직접 입력한 실제 Command를 확인하여 해결했으며 임의 구현으로 대체하지 않았다.

실제 binlog/Debezium/Kafka 실행·5~8교시 구현·게임 플레이 재실행은 요청 범위에 포함하지 않았다. 현재 준비 JSON도 binlog_cdc_observed=false다. 실제 게임 입력은 수정하지 않아 파일 재수집이 필요 없다.

## 다음 확인 순서

현재 작성 결과는 저장돼 있다. VS Code PowerShell에서 화면 검사만 다시 확인하려면 다음 명령을 사용한다. 이 검사는 MongoDB나 runserver를 켤 필요가 없다.

```powershell
cd C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python check_day24_period4.py
```

fixture 원문과 summary가 각각 data/fixtures에 있는지 확인한 후 5교시 교안으로 넘어간다. 출력 명령은 같은 경로의 파일을 다시 쓰므로 기존 저장본을 보존하려면 다른 출력명을 사용한다.
