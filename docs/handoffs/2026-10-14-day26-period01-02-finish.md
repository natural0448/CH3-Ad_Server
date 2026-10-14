# 26일차 1·2교시 확인·구현 완료 · 2026-10-14

## 요청과 결과

사용자가 26일차2교시까지 진행한 코드의 누락 확인과 구현을 요청했다. Desktop의 `26일차 · 같은 입력의 Lake·Mongo와 광고 보고서.html`을 로컬에서 읽고1·2교시만 적용했다. 교안 문장은 참고 요구사항으로 사용했으며3교시 이후의 저장/DB 대조/광고 보고서는 자동 실행하지 않았다.

시작 상태에는 ads/lake_files.py의 stable_json·build_history만 있었다. 2교시 build_current와1교시의 inspect_player_lake·demo_player_lake 명령이 없었다. 사용자 history 로직은 맞았으며 오류 문자열의 chang_id 철자만 교안의 change_id와 달랐다. 이를 바로잡고 누락 함수·명령을 제공 완성 코드대로 추가했다. 세 함수와 두 명령 파일 AST가 교안과 같다.

실제25일차 인계 사본56행으로 history56/current56을 확인했다. 두 번 전달한112행과 역순에서도 단계별 결과목록SHA가 같았다. fixture 최신version4/coins40, 삭제version4 유지, 정상SHA의 같은version 충돌거절, schema/내용SHA 거절, 빈목록, 실패후 정상호출을 확인했다. 실제 명령은 written=false이며 Mongo get_db를 호출하지 않았다. 인계 네 파일과 기존checkpoint/원문은 bytes 그대로다.

## 시작 Git 상태와 사용자 작업 보존

Chapter3 상위는 `Git 상태 확인 불가: 저장소 아님`이다. 광고 저장소 HEAD는724ac87 day25 - 7교시, staged 없음이었다. 기존 unstaged는 ads/context_projection.py·ads/test_events.py와25일차 색인/짝 문서/검증JSON 변경이었다. 기존 untracked는 사용자 ads/lake_files.py, 앞 작업 export_context_handoff.py·그 짝 문서·25일차8교시 인수인계였다. 시작에 존재한 변경을 이번 작업의 신규 구현으로 주장하지 않았다. 게임 저장소는2914ac4 day25 - 7교시, 시작 clean이며 수정하지 않았다. Git 초기화/add/commit/reset은 하지 않았다.

[검증 기록](../server-routing/verification/day26-period01-02.json)의 git_start/existing_source_sha256/routing_before를 기준으로 한다. 기존 사용자 변경의 짝 문서가 이미 일치하는 것을 확인하고, 새 lake_files.py의 현재 두 함수·반환·원본참조·실제 오류문자열 문서를 먼저 만든 뒤 추가 개발을 했다. 비밀값과.env 내용은 기록하지 않았다.

## 이번 코드·문서 변경

- ads/lake_files.py: 사용자 파일의 build_history 오류 문자열을 교안대로 보정하고 build_current를 추가. imports·stable_json 및 history의 처리 계약은 보존.
- ads/test_events.py: 기존 파일 안에 PlayerLakeTests8개 검사를 추가. 이전 테스트 클래스 본문은 보존.
- ads/management/commands/inspect_player_lake.py: 제공 미리보기 Command 전체 추가.
- ads/management/commands/demo_player_lake.py: 제공 fixture_change/Command 전체 추가.
- tools/basics/day26_period01.py·day26_period02.py: 각 교시의 두 초급 예제 전체를 기존 tools/basics 안에 묶어 저장. 새 examples 폴더를 만들지 않으며 출력은 교안과 같다.

위6개 소스의1:1짝 문서와 기존 current-progress-index.md를 최종 코드에 맞췄다. 새 문서는 기존 files/<상대경로>.md 규칙을 따른다. 이 인수인계와 기존 verification 디렉터리의 day26-period01-02.json에 시작/교안/실제 출력/마감을 기록했다. 임의의 새 서버·앱·검증 디렉터리를 만들지 않았다. 이동·삭제는 없다. 이번 작업으로 새 Lake history/current NDJSON이나 Mongo 문서를 저장하지 않았다.

## 책임·데이터 계약

build_history는25일차 make_context_document를 재사용해 정확한9필드/UTC/출처/내용SHA를 검증하고, 같은 change_id를 한 번만 남겨 event_time/change_id순으로 반환한다. build_current는 history를 재검사하여 media/subject/version/change_id순으로 처리하며10필드 player-current/v1 후보를 안정_id별로 고른다. 큰version만 교체하고 같은version의 deleted/context 불일치는 거절한다. 삭제후보도 유지하며 provenance와 업무상태를 구별한다.

inspect는 --manifest로 입력bytesSHA·행수·schema·출처·매체·같은SHA의 완료checkpoint를 확인한다. --repeat/--reverse는 메모리 목록만 바꾼다. result_sha256는 stable_json(결과목록)의SHA이며 원본파일SHA나3교시 저장NDJSON파일SHA와 구별한다. fixture-lake는 teaching-fixture이며 실제 Player/선택/DB를 만들지 않는다.

선택한 입력은 data/handoff/day25-run1/player-context-changes.ndjson, manifest는 같은폴더 manifest.json, checkpoint는 같은폴더 checkpoint.json이다. 원본SHA는18dbb0bd715f69a4bfde646623cd3d39932f9c147fdf7858f6276732bb51e154다. history목록SHA는2d9523e069398c701fd562d1f36909eb47c96b35775318bd5cac063b616afd77, current목록SHA는fa547973889369783752a5f575caba092817791b32853ad5793c8277290e0c23다.

history첫행은 subject3/version1, current첫행은_id=village-game:1/version461/coins26/deletedFalse다. history는시각정렬이고 current는문자열_id정렬이므로 첫행이 같아야 한다고 판단하지 않는다. current56은 입력범위의 대상이며25일차 Mongo/export57행(별도fixture포함)과 자동으로 같은값이라고 가정하지 않는다. 그런 비교는4교시 범위다.

## 검사 결과

- `python ad_config/manage.py check`: 정상.
- `python ad_config/manage.py test ads.test_events.PlayerLakeTests ads.test_events.ContextHandoffTests ads.test_events.ContextApiTests ads.test_events.EventAuthTests ads.tests.AuthenticationTests --verbosity 1`:33개 통과. Windows sandbox의 알려진 임시폴더ACL 문제를 피하여 sandbox밖에서 격리된 테스트파일/Test DB/Mock Mongo로 실행했다.
- 초급1교시 실행: ['a','b'],2,True,['a','c','b']. 2교시:1,4,4,3,sample-current/v1.
- 실제 history/current 명령4회: N=56, 반복supplied112, H=K=56, 각단계 목록SHA 동일, writtenFalse.
- demo 정상duplicates/versions/delete/empty와 잘못된schema/change-id-conflict/version-conflict 기대CommandError를 확인. 거절은 정상stdout을 출력하지 않고 이후versions호출은 다시version4/coins40이다.
- 실제 명령의 get_db 호출0을 mock으로 확인했으며 기존 인계4파일·기록·새원문 총7파일 SHA는 전후 같다.
- 표준 routing-doc-auditor CLI는 기존 광고 routing README 부재로exit2다. 기존 current-progress-index를 유지하고 스킬 extract_symbols/mark_documented API로 이번6개 소스의 짝 문서/시그니처/색인을 검사한다. CLI 실패와 범위API 성공을 별도로 기록한다. Git변경·보존·문서링크·최종검사는 증거JSON의finish를 따른다.

외부웹/실시간Mongo 대조는1·2교시 범위 밖이고 필요하지 않아 실행하지 않았다. 실제.preview 함수는파일을읽고 메모리만 계산한다.3교시 build_lake_version/build_player_lake 및 출력run은 미적용이며 계획을 현재 구현처럼 기록하지 않는다.

## 사용자가 실행할 명령과3교시 입력

기존 광고 작업폴더/가상환경에서 실행한다.1·2교시 미리보기에는 runserver/MongoDB 기동이 필요하지 않다.

```powershell
cd C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python ad_config/manage.py inspect_player_lake --source data/handoff/day25-run1/player-context-changes.ndjson --manifest data/handoff/day25-run1/manifest.json --stage history
python ad_config/manage.py inspect_player_lake --source data/handoff/day25-run1/player-context-changes.ndjson --manifest data/handoff/day25-run1/manifest.json --stage current --repeat 2 --reverse
```

두 번째 기대값은 input_rows56/supplied_rows112/history_rows56/result_rows56/writtenFalse다. fixture조회는 `python ad_config/manage.py demo_player_lake --case versions`, 삭제는`--case delete`, 기대거절은`--case version-conflict`를 사용한다. 초급파일은`python tools/basics/day26_period01.py`·day26_period02.py다.

3교시는 위 동일한 인계 source/manifest/checkpoint와 지문을 넘긴다. 뒤 교안의 예전 기본경로 data/exports/player-context-changes.ndjson으로 바꾸거나 bytes를 덮어쓰지 않는다. 새 run저장은3교시 작업에서 기존원본을 보존하며 진행한다.
