# 26일차 4교시 진행 중 Lake 비교 경로 해결 · 2026-10-14

## 요청과 결과

사용자가 실행한 run-001/002의 compare_player_lake_versions 오류를 재현하고 현재 구조에서 해결 경로를 확인했다. 원인은 run-001/manifest.json 부재다. 이전의 잘못된 저장 함수가 만든 run-001/002에는 summary.json만 있고 완성 manifest가 없다. 비교 명령 코드는 교안 계약대로 동작한다.

완성된 run-003/004로 비교하면 exit0이며 source/history/current_matches가 모두true, N=H=K=56이다. 기존 데이터나 소비 규칙을 바꾸지 않고 실행 인수만 올바른 run으로 지정하는 해결이다. 원래 run-001/002 명령은 그대로 실패하는 것이 맞으며 이 명령까지 성공했다고 기록하지 않는다.

교안 원문 SHA는 이전 검증 기록과 같았다. 교안의 불완전 run 보존·새 이름 사용 지침을 유지했다. 4교시 참조도 run-003으로 연결하며, 아직4교시 전체나 실제 Mongo 대조 완료를 판정하지 않았다.

## 작업 시작 전 Git 상태

Chapter3는 **Git 상태 확인 불가: 저장소 아님**. 광고 저장소 HEAD는 d68b511 day25 - 챕터2다. staged는 비어 있었다. 작업 시작 전에 존재한 unstaged 파일은 ads/lake_files.py, ads/test_events.py, docs/server-routing/current-progress-index.md, files/ads/lake_files.py.md, files/ads/management/commands/compare_player_snapshots.py.md, files/ads/test_events.py.md다. files 표기는 docs/server-routing/files 아래다.

기존 untracked 소스는 build_player_lake.py, compare_player_lake_versions.py, compare_player_sinks.py, demo_player_sink_comparison.py(모두 ads/management/commands 아래), ads/sink_evidence.py, tools/basics/day26_period03.py다. 기존 untracked 문서·검증 기록은 이전3교시 handoff, 두 build/Lake 비교 명령 짝 문서, 초급 예제 짝 문서, verification/day26-period03.json이다. 정확한 전체 목록은 [이번 검증 기록](../server-routing/verification/day26-period04-lake-path.json)의 git_start에 있다.

이 상태는 이전 에이전트 작업을 포함하더라도 모두 이번 작업 시작 전에 존재한 변경으로 구분했다. stage/reset/commit은 수행하지 않았다. source8개와 인계/run 데이터16개의 시작 SHA가 작업 후 동일하다.

## 이번 변경과 책임

코드·설정·데이터 추가/수정/이동/삭제는 없다. 새 사용자4교시 파일3개에 짝 문서를 등록했다: ads/sink_evidence.py, ads/management/commands/compare_player_sinks.py, ads/management/commands/demo_player_sink_comparison.py. 새 문서는 docs/server-routing/files/<소스경로>.md다. current-progress-index.md에 이3개와 실제 해결 경로를 추가했다. verification/day26-period04-lake-path.json과 이 인수인계를 작성했다.

사용자 sink 구현은 교안 기본 함수에 공개 문서 검증·매체 필터·불일치 값 표시를 추가한 상태이며 현재 구현을 그대로 설명했다. 소스 수정은 하지 않았다. compare_player_sinks 명령은 원본/완성 Lake 검사 뒤 Mongo를 읽고 output을 저장한다. 이번에는 이 Mongo 명령을 실행하지 않았다. 서버·MongoDB 프로세스·업무 문서는 조작하지 않았다.

## 실행·검사 결과

run-001/002 비교: exit1, CommandError의 누락 경로는 data/lake/gold/player_current/run-001/manifest.json이다. run-003/004 비교: exit0, 세matches true, 양쪽 counts56/56/56이다. 실제 CLI 출력은 검증 기록에 보관했다. 입력·결과 파일은 읽기만 했다.

검증 이후 별도 문서 정합화에서 변경 상태의 Python8개를 AST로 확인했고 시그니처 누락0·색인 누락0이었다. routing-doc-auditor 표준CLI는 기존 README.md 부재로 exit1을 반환해 완료하지 못했다. 같은 검사기의 AST API와 실제 current-progress-index.md 대조 결과를 사용했으며 CLI 성공으로 기록하지 않는다. git diff --check는 통과했고 기존 LF/CRLF 안내만 있었다.

이번에는 실행 인수 해결과 문서 등록만 했으므로 새로운 테스트를 만들거나 기존39개 테스트를 반복 실행하지 않았다. 실제 Mongo 대조·4교시 입력 재반영·GUI 관찰도 수행하지 않았다. 3교시 이전39개 통과는 이전 인수인계의 검사 기록이다.

## 사용자가 실행할 명령

광고 작업 폴더와 활성화된 가상환경에서 실행한다.

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server
python ad_config/manage.py compare_player_lake_versions --before data/lake/gold/player_current/run-003 --after data/lake/gold/player_current/run-004
```

세matches가true이면 정상이다. 이 비교에는 MongoDB가 필요하지 않다. 4교시 shell의 read_ndjson 입력은 data/lake/gold/player_current/run-003/current.ndjson으로 바꾼다. 기존 사용자 compare_player_sinks 명령을 이용하는 경우의 올바른 인수는 다음과 같다. 이 두 번째 명령은 MongoDB 연결이 필요하며 이번에 실행하지 않았다.

```powershell
python ad_config/manage.py compare_player_sinks --source data/handoff/day25-run1/player-context-changes.ndjson --lake-dir data/lake/gold/player_current/run-003 --output data/contracts/day26-sinks.json
```

source는1교시 선택 인계와 같은 bytes를 유지한다. Mongo가 더 최신이면 mismatched가 나올 수 있으며 이는 해당 시점 차이를 기록하는 비교 결과다. extra_keys가 있다는 이유로 삭제하지 않는다. 새로 저장하는 Lake 실습에는 아직 없는 run 이름을 사용한다.
