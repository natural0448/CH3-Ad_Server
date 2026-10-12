# 24일차 8교시 완료 · 2026-10-12

## 요청과 완료 결과

8교시까지 마무리하고 사용자가 입력할 명령을 정리했다. 데스크톱의 수정 교안 ‘실제 Player snapshot을 광고 서버에서 검증하고 인계하기.html’의 8교시를 읽고 현재 사용자 함수와 명령을 검증했다. 공식 검사 24 통과·0 실패, 실제 관리명령 exit 0이다. 원본 56행과 5교시 계약을 새 광고 `data/exports/day24-input` 폴더에 함께 인계했다. 원본·계약 보존, 복사 bytes·checksum 일치, 수신 계약의 source_path만 변경됨을 확인했다.

## 시작 Git 상태와 사용자 작업

Chapter3 루트는 `Git 상태 확인 불가: 저장소 아님`이다. 광고 HEAD는 `5e2712b day24 - chapter4`, 게임 HEAD는 `14f23ae day24 - chapter4`다. 두 저장소 staged는 없었다. 광고 unstaged는 README.md, ads/snapshot_intake.py, docs/server-routing/current-progress-index.md, day24-period01-index.md, files/README.md.md, files/ads/snapshot_intake.py.md, files/tools/check_day24_logic.py.md였다. 기존 미추적 Python은 compare_player_snapshots.py, handoff_player_snapshot.py, read_snapshot_missing.py, write_snapshot_contract.py, tools/check_day24_period5.py였다. 이전 인수인계·짝 문서·verification 기록도 미추적 상태였다. 게임 unstaged는 docs/server-routing/README.md, day24-progress.md, files/README.md.md였다.

전체 staged·unstaged·untracked 목록, 개발 파일과 원본 산출물 해시는 [시작 기록](../server-routing/verification/2026-10-12-day24-period08-finish/start.json)에 있다. 작업 시작 전에 존재한 변경은 작성자를 재분류하지 않고 모두 사용자 작업으로 취급했다. 기존 기능 소스·기존 JSON을 덮어쓰거나 정리하지 않았으며 Git add/commit/reset은 하지 않았다.

## 이번 파일 변경

새 실제 산출물은 data/exports/day24-input/player-cdc.ndjson과 player-cdc-contract.json이다. 기존 target이 없는지 먼저 확인했고 둘을 검증한 임시 폴더를 한 번에 최종 이름으로 배치했다. 같은 원본과 같은 계약으로 기존 target에 재인계하지 않았다.

새 짝 문서는 docs/server-routing/files/data/exports/day24-input/player-cdc.ndjson.md와 player-cdc-contract.json.md다. 두 경로를 current-progress-index.md에 등록했다. 기존 짝 문서 files/ads/snapshot_intake.py.md, files/ads/management/commands/handoff_player_snapshot.py.md, files/tools/check_day24_logic.py.md, files/README.md.md와 광고 README.md·current-progress-index.md·day24-period01-index.md의 8교시 상태를 갱신했다. 게임 docs/server-routing/README.md·day24-progress.md·files/README.md.md와 Chapter3/docs/routing/README.md에서도 현재 광고 인계 상태를 연결했다. 이번 인수인계와 verification/2026-10-12-day24-period08-finish는 새 기록이다.

이번 Python 코드 수정·추가·이동·삭제는 없다. 기존 소스와 원본의 보존 여부, 이번 문서와 산출물 변경 목록은 [마감 기록](../server-routing/verification/2026-10-12-day24-period08-finish/finish.json)에 기록한다.

## 설계·교안 대응과 책임 경계

게임 데이터 원본은 기존 바깥 Game-server/data/exports를 사용했다. Game-server/server/data/exports의 별도 사용자 파일들과 혼용하거나 이동하지 않았다. 광고는 파일 검증·복사·계약 대조만 담당하고 게임 ORM·게임 계정 DB를 조회하지 않는다. 실제 MongoDB·MySQL·Kafka·Connect 기동이나 광고 선택에 Player 상태를 연결하는 작업은 하지 않았다. 인계 성공은 25일차 입력 준비의 완료다.

교안 정답과 현재 사용자 코드는 같은 처리 순서다. 제공 정답은 contract[field]와 value를 직접 비교하고 사용자 함수는 sort_keys JSON 문자열을 비교한다. 거절 메시지도 사용자 문구다. 제공 명령의 compact stdout과 달리 사용자 stdout은 indent=2다. [AST 비교](../server-routing/verification/2026-10-12-day24-period08-finish/lesson-comparison.json)는 이 차이 때문에 exact match=false이며, 이를 숨기거나 정답 파일을 통째로 덮어쓰지 않았다. 요구되는 인계·거절·정리 동작은 공식 24개 검사가 통과했고 현재 사용자 구현을 보존했다. 앞선 1~7교시 이력은 [이전 검토](2026-10-12-day24-through-period07-review.md)를 따른다.

## 실행한 검사와 결과

- 공식 `tools/check_day24_logic.py --project . --period 8`: [24 통과·0 실패](../server-routing/verification/2026-10-12-day24-period08-finish/official-period08-before.json). 이름의 before는 소스 변경 전 검사라는 뜻이며 이후 소스 변경은 없으므로 최종 소스 검증 결과다.
- 실제 `ad_config/manage.py handoff_player_snapshot --source ../Game-server/data/exports/player-cdc.ndjson --contract data/contracts/player-cdc-contract.json --target data/exports/day24-input`: [exit 0](../server-routing/verification/2026-10-12-day24-period08-finish/manage-command.json).
- [실제 파일 대조](../server-routing/verification/2026-10-12-day24-period08-finish/actual-handoff.json): 56행, source/received bytes 동일, NDJSON checksum 일치, source_path만 변경, 기존 원본·계약·이전 결과 5파일 불변, 임시 형제 폴더 남음 없음.
- 수신 `inspect_player_snapshot` 및 라우팅 시그니처/색인/링크·Git 마감은 [마감 기록](../server-routing/verification/2026-10-12-day24-period08-finish/finish.json)을 따른다.

공식 검사는 SQLite 메모리와 Mongo mock·임시 파일만 사용했다. 샌드박스의 기본 임시 경로 접근 제한을 피하려고 process-local tempfile.tempdir만 이번 evidence 폴더로 지정하고 runpy.run_path로 원래 검사기를 실행했다. 학생·검사기 소스는 수정하지 않았다. mock이 get_client를 대체하여 종료 시 close_client의 cache_info AttributeError가 표시되지만 failed=0, exit=0이며 실제 Mongo 연결 오류가 아니다. venv의 Python 경로 경고도 성공 종료와 별도 기록이다.

## 검사 제한과 남은 범위

이번에는 8교시만 공식 재검사했다. 1~7교시 공식 성공은 이전 이력으로 구분한다. 표준 routing-doc-auditor CLI는 기존 docs/server-routing/README.md 부재로 exit 2다. 기존 색인 current-progress-index.md를 유지하며 스킬의 extract_symbols/mark_documented API로 실제 짝 문서와 색인을 대조했다. CLI 실패를 API 성공으로 숨기지 않는다. [CLI 기록](../server-routing/verification/2026-10-12-day24-period08-finish/routing-cli-status.json), [최종 구조 검사](../server-routing/verification/2026-10-12-day24-period08-finish/routing-final.json)를 따른다.

여러 작성자 경쟁·파일 잠금은 교안의 현재 구현 범위 밖이다. 동결 원본을 사용하며 target은 새 폴더여야 한다. 사용자 8교시 소스의 기존 공백도 임의 정리하지 않았다.

마감 AST 검사에서 Python 7파일·42심볼의 짝 문서와 색인이 일치했고, 새 수신 데이터 두 파일도 각각 짝 문서와 색인에 등록했다. 관련 로컬 링크도 확인했다. Git diff --check는 게임 exit 0, 광고 exit 2이며 광고 출력은 작업 시작부터 있던 ads/snapshot_intake.py:169의 공백 한 줄이다. 사용자 Python의 시작·종료 해시가 같아 기존 공백을 임의 수정하지 않았다.

## 사용자가 입력할 명령

실제 인계는 이미 완료됐으므로 아래는 VS Code PowerShell에서 직접 재확인하는 명령이다. MongoDB나 runserver를 새로 켤 필요는 없다.

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python tools/check_day24_logic.py --project . --period 8
python ad_config/manage.py inspect_player_snapshot --source data/exports/day24-input/player-cdc.ndjson
Get-Content data/exports/day24-input/player-cdc-contract.json
```

검사 결과는 passed=24, failed=0, 수신 검사 rows=56이다. 계약 rows=56과 sha256을 수신 결과와 비교한다. source_path는 data/exports/day24-input/player-cdc.ndjson으로 해석되고 kafka_position=null, binlog_cdc_status=not-configured다.

새 인계가 필요할 때만 이미 없는 다른 target을 사용한다. 아래 -02 폴더도 기존에 생겼다면 다른 새 이름으로 바꾼다. 현재 day24-input 폴더를 삭제할 필요는 없다.

```powershell
python ad_config/manage.py handoff_player_snapshot --source "../Game-server/data/exports/player-cdc.ndjson" --contract data/contracts/player-cdc-contract.json --target data/exports/day24-input-02
```

25일차 입력으로 넘길 실제 원본은 C:/MLO01-01/Chapter3/ad_server/data/exports/day24-input/player-cdc.ndjson이며 함께 보관할 계약은 같은 폴더의 player-cdc-contract.json이다. 다른 새 target을 썼다면 그 수신 경로를 소비자에게 전달한다.
