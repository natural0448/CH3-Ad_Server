# 24일차 7교시까지 검토·라우팅 반영 · 2026-10-12

## 요청과 결과

사용자의 “7교시까지 맞게 했는지 확인하고 라우팅 문서에 반영” 요청으로 수정 교안 ‘실제 Player snapshot을 광고 서버에서 검증하고 인계하기.html’과 현재 구현을 대조했다. 5교시 build_snapshot_contract, 6교시 load_rows/compare, 7교시 missing_summary는 docstring을 제외한 AST가 제공 함수와 같다. 앞선 오류의 title/when 예시는 사용자가 올바른 업무 필드로 수정한 상태였다.

공식 검사는 5교시 13/0, 6교시 15/0, 7교시 10/0, 총 38개 통과다. tools에 저장된 5교시 화면 검사도 exit 0이다. 실제 사용자 원본 두 파일은 각 56행이며 변경 1건·새 ID 0건·누락 0건이다. 기존 계약과 비교·누락 결과가 현재 입력의 재계산과 일치한다. 7교시의 빈 누락 목록·빈 삭제 목록·삭제 추론 불가 값은 정상이다.

## 시작 Git 상태와 기존 작업

Chapter3 루트는 `Git 상태 확인 불가: 저장소 아님`이다. 광고 저장소 HEAD는 `5e2712b day24 - chapter4`, staged는 없었다. unstaged는 ads/snapshot_intake.py, untracked는 ads/management/commands/compare_player_snapshots.py, read_snapshot_missing.py, write_snapshot_contract.py 및 tools/check_day24_period5.py였다. 이 다섯 Python 파일은 전부 작업 시작 전에 존재한 사용자 변경으로 취급했다. 게임 저장소 HEAD는 `14f23ae day24 - chapter4`, staged/unstaged/untracked Git 상태는 비어 있었다.

기존 ignored 데이터 파일인 after·광고 계약·비교·누락 JSON도 사용자 산출물로 보존했다. [시작 기록](../server-routing/verification/2026-10-12-day24-period05-07-review/start.json)은 전체 Git 목록·82개 개발 파일 해시·before/after 해시를 기록한다. Git add/commit/reset, Python 수정·추가·이동·삭제, 기존 JSON 덮어쓰기, 실제 DB 변경은 수행하지 않았다.

마감 중 사용자가 ads/snapshot_intake.py에 handoff_snapshot을 추가하고 ads/management/commands/handoff_player_snapshot.py를 새로 저장했다. [동시 저장 관찰](../server-routing/verification/2026-10-12-day24-period05-07-review/concurrent-user-period08.json)에 그 사용자 변경을 별도로 기록했다. 이 추가분을 에이전트 개발 변경으로 주장하지 않는다. 현재 저장 상태를 라우팅 문서에 맞추되 8교시 실행·검사 성공으로 확대하지 않았다. 최종 모듈에서도 5~7교시 검사를 재확인했다.

## 이번 파일 변경과 라우팅 정합화

검사기 구조 결과에 따라 누락된 짝 문서를 먼저 만들고 사용자 코드의 실제 시그니처·허용 입력·반환·의사코드·직접 호출·값 출처를 반영했다. 기능 검증이 끝난 뒤 별도 마감 단계에서 현재 상태와 증거를 맞췄다.

새 광고 짝 문서:

- docs/server-routing/files/ads/management/commands/write_snapshot_contract.py.md
- docs/server-routing/files/ads/management/commands/compare_player_snapshots.py.md
- docs/server-routing/files/ads/management/commands/read_snapshot_missing.py.md
- docs/server-routing/files/ads/management/commands/handoff_player_snapshot.py.md: 동시 저장된 사용자 8교시 명령, 미검증 구분
- docs/server-routing/files/tools/check_day24_period5.py.md
- docs/server-routing/files/data/contracts/player-cdc-contract.json.md
- docs/server-routing/files/data/checks/day24-comparison.json.md
- docs/server-routing/files/data/checks/day24-missing.json.md

광고 기존 문서 변경은 README.md의 24일차 진행 문단, docs/server-routing/current-progress-index.md, day24-period01-index.md, files/ads/snapshot_intake.py.md, files/README.md.md, files/tools/check_day24_logic.py.md다. README는 안내 문단만 갱신한 문서 변경이며 Python 개발 변경과 구분한다.

게임은 docs/server-routing/files/data/exports/player-snapshot-after.ndjson.md를 추가하고 docs/server-routing/README.md·day24-progress.md의 현재 진행·after 색인을 갱신했다. files/README.md.md의 안쪽 data 부재 설명도 실제 관찰로 정정했다. Chapter3/docs/routing/README.md의 프로젝트 간 표와 현재 검토 링크도 갱신했다. 이 인수인계와 이번 verification 폴더는 신규 기록이다. 기존 실패·복구 이력은 삭제하지 않았다.

## 책임과 교안 차이

게임 파일 생산은 기존 export_player_snapshot의 책임이다. 광고는 공개 파일을 검사해 계약·비교·누락 관찰을 생성한다. 게임 ORM이나 광고 HTTP 경로는 변경하지 않았다. before는 ../Game-server/data/exports/player-cdc.ndjson, after는 ../Game-server/data/exports/player-snapshot-after.ndjson이다. Game-server/server/data는 만들지 않았다.

비교는 room_id·coins·version·UTC updated_at을 사용하고 captured_at 차이를 제외한다. 누락은 원인 미상 관찰이며 delete_events=[], delete_inference_allowed=False를 유지한다. 원본 checksum과 계약 작성 시각은 서로 다른 값의 책임이다. 실제 Kafka/binlog 실행과 8교시 인계 성공을 이번 검증 결과로 기록하지 않는다.

사용자 compare_player_snapshots Command는 교안과 달리 stdout JSON에도 indent=2를 준다. 파일의 JSON 계약·결과는 같고 공식 검사가 통과하므로 사용자 형식을 보존했다. ads/snapshot_intake.py에 추가된 `from unittest import result`는 함수 본문에서 사용하지 않는다. missing_summary의 지역 result와 다른 값이며 기능 검사는 통과했다. 미사용 import를 임의 정리하지 않았다.

tools/check_day24_period5.py 머리말은 루트 파일 실행 예시지만 실제 사용자 저장 위치는 tools다. 파일을 옮기지 않고 광고 루트에서 `python -m tools.check_day24_period5`로 검사했다.

## 실행한 검사와 결과

공식 검사 진입점은 tools/check_day24_logic.py, project는 광고 루트의 절대 경로, period는 5/6/7이다. 샌드박스 임시 경로 제한에 맞춰 process-local tempfile.tempdir를 이번 검증 폴더로 지정하고 runpy.run_path로 실행했다. 검사기와 학생 코드 자체는 바꾸지 않았다.

| 검사 | 결과/증거 |
|---|---|
| 공식 --period 5 | [13 통과·0 실패](../server-routing/verification/2026-10-12-day24-period05-07-review/official-period05-final.json) |
| 공식 --period 6 | [15 통과·0 실패](../server-routing/verification/2026-10-12-day24-period05-07-review/official-period06-final.json) |
| 공식 --period 7 | [10 통과·0 실패](../server-routing/verification/2026-10-12-day24-period05-07-review/official-period07-final.json) |
| 5교시 화면 제공 검사 | [exit 0, 정상·빈 입력·거절·원문 보존 PASS](../server-routing/verification/2026-10-12-day24-period05-07-review/screen-period05.json) |
| 교안 AST 대조 | [네 함수 일치, 기존 2~4교시 함수 HEAD와 동일](../server-routing/verification/2026-10-12-day24-period05-07-review/lesson-comparison.json) |
| 실제 기존 파일 읽기 대조 | [계약·비교·누락 모두 일치](../server-routing/verification/2026-10-12-day24-period05-07-review/actual-file-verification.json) |
| 실제 inspect_player_snapshot 명령 | [exit 0, 원본 56행·56개 공개 ID·checksum 일치](../server-routing/verification/2026-10-12-day24-period05-07-review/actual-inspect-command.json) |
| 라우팅/해시/Git 마감 | [최종 결과](../server-routing/verification/2026-10-12-day24-period05-07-review/finish.json) |

공식 검사는 SQLite 메모리와 Mongo mock·임시 파일을 사용한다. mock이 get_client를 대체해 atexit close_client의 cache_info AttributeError가 표시됐지만 세 프로세스 모두 exit 0이며 failed=0이다. 이를 실제 Mongo 연결 오류로 해석하거나 ads.mongo 소스를 수정하지 않았다. Python의 설치 경로 경고도 exit 0과 별도 관찰이다.

실제 원본에서 inspect_snapshot/load_rows/compare/missing_summary를 읽기만 수행했다. 계약의 source_path·고정 조건·56행/ID/checksum·수집 시각·UTC 작성 시각 및 저장 결과를 대조했다. 실제 생성 명령을 기존 output에 재실행하지 않았다. 실제 게임 행동 성공 응답과 수집 사이의 인과·시점 일치는 이번에 직접 관찰하지 않았다.

## 실행하지 않은 검사와 제한

앞선 1교시 12개·2교시 22개·3교시 8개·4교시 17개는 기존 성공 이력이다. 이번에는 5~7교시와 저장본만 새로 검사했으며 기존 2~4교시 함수의 AST가 HEAD와 같음을 확인했다. 8교시 소스·명령은 마감 중 사용자가 추가 저장했으며 검사·실제 인계는 이번에 실행하지 않았다.

마감 시 Game-server/server/data/exports에 player-cdc.ndjson·player-snapshot-before.ndjson·player-snapshot-after.ndjson도 관찰했다. 작성 주체는 확정하지 않고 사용자 작업으로 취급해 보존했다. 각 56행이며 바깥 파일과 bytes가 다르고 안쪽 before/after 비교도 변경 1건·새 ID/누락 0건이다. 이번 공식 검사와 기존 광고 계약·결과 대조의 입력은 바깥 Game-server/data/exports였다. 이 두 묶음을 서로 바꿔 쓰지 않으며, 기존 계약 checksum에 안쪽 player-cdc 파일을 끼워 넣지 않는다. export_player_snapshot의 상대 --output은 실행 위치 기준이다. [별도 관찰](../server-routing/verification/2026-10-12-day24-period05-07-review/nested-exports-observation.json)을 따른다.

라우팅 표준 CLI는 docs/server-routing/README.md가 없어서 exit 2다. 해당 파일은 기존 HEAD에도 없고 current-progress-index.md를 사용하는 현재 구조를 유지했다. 스킬 AST API로 시작 시 사용자 변경 Python 5파일과 마감 중 새 명령 1파일의 짝 문서·시그니처·색인과 관련 로컬 링크를 따로 검사한다. API 성공을 CLI 성공으로 기록하지 않는다. [CLI 상태](../server-routing/verification/2026-10-12-day24-period05-07-review/routing-cli-status.json)를 따른다.

Git diff --check는 게임 exit 0이다. 광고 exit 1은 사용자 동시 저장한 8교시 ads/snapshot_intake.py:169의 공백 때문이다. 이번 문서 변경에서 생긴 공백 오류는 없고 사용자 소스를 정리하지 않았다.

## 다음 작업과 실행 순서

7교시 저장 결과가 이미 있으므로 같은 결과 파일을 다시 만들 필요는 없다. 필요할 때 광고 루트에서 제공 검사를 다시 실행한다.

교안의 ../game_server는 예시 폴더 이름이다. 현재 실제 이름은 Game-server이므로 입력 인수를 ../Game-server/data/exports/player-cdc.ndjson으로 바꾼다. 사용자 후속 질문의 inspect_player_snapshot도 이 경로로 직접 실행해 56행을 확인했다. Game-server 이름이나 기존 폴더를 바꿀 필요는 없다.

```powershell
cd C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\python.exe ad_config/manage.py inspect_player_snapshot --source "../Game-server/data/exports/player-cdc.ndjson"
.\.venv\Scripts\python.exe -m tools.check_day24_period5
.\.venv\Scripts\python.exe tools/check_day24_logic.py --project C:/MLO01-01/Chapter3/ad_server --period 5
.\.venv\Scripts\python.exe tools/check_day24_logic.py --project C:/MLO01-01/Chapter3/ad_server --period 6
.\.venv\Scripts\python.exe tools/check_day24_logic.py --project C:/MLO01-01/Chapter3/ad_server --period 7
```

파일 검사에는 MongoDB/runserver 기동이 필요 없다. 8교시 인계 함수·명령은 마감 중 사용자 저장이 관찰됐으며 미검증 상태다. 기존 before/after/계약/결과와 폴더 배치를 유지하고 해당 교시 검토 때 수정 교안과 검사기로 확인한다.
