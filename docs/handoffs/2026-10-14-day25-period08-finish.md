# 25일차 8교시 구현·인계 완료 · 2026-10-14

## 요청과 완료 결과

사용자가 25일차 8교시까지 마무리를 요청했다. 로컬 교안 `공개 snapshot을 MongoDB context에 멱등 반영한다.html`을 기준으로 8교시 helper·완성 함수·관리명령을 적용하고 실제 완료 기록 및 네 파일 인계까지 실행했다. 이전 새 파일 금지 지시에 대해 사용자가 “폴더 구조를 유지한 채 새로 파일을 환경에 맞춰서 제작”이라고 범위를 확인했다. 기존 서버·앱·명령·data 배치는 유지하고 필요한 소스/짝 문서는 기존 위치에 추가했다. 교안 출력 폴더만 기존 광고 루트 data 아래에 만들었다.

최신 입력56행에 새 checkpoint를 만들었고 duplicate56/applied0, next_line=rows=56, done=true였다. 같은 완료 명령과 인계 사본의 실제 소비는 각각 processed=0이다. 네 인계 파일의 SHA와 manifest 경로를 대조했다. 현재 공개 복사본57행은 player-snapshot56행+teaching-fixture1행이다. 기존 인계 폴더 반복 요청과 미완료 기록은 기대 CommandError로 거절됐다. 입력·기존5교시 checkpoint·Mongo 공개 문서의 해시를 보존했다.

## 작업 시작 전 Git 상태

Chapter3 상위는 `Git 상태 확인 불가: 저장소 아님`이다. 광고 저장소 HEAD는 `724ac87 day25 - 7교시`, 시작 staged/unstaged/untracked 모두 없음이다. Git 초기화·add·commit·reset은 하지 않았다. 시작 상태와 보호할 파일 지문은 기존 verification/2026-10-13-day25-period07-review/start.json의 day25_period08에 기록했다. 이전7교시 코드와 문서는 사용자가 커밋한 기존 구현으로 취급했다. 게임/접속기 저장소는 수정하지 않았다.

## 이번 개발 파일 변경

수정은 ads/context_projection.py(필요한 import 및 두 인계 함수 추가)와 ads/test_events.py(기존 파일 안에 인계 검사 클래스 추가)다. 추가 소스는 ads/management/commands/export_context_handoff.py다. 기존13개 projection 함수의 AST와 기존 테스트 클래스 본문은 보존했다. 인계 helper·완성 함수·새 Command의 AST가 교안 완성 코드와 같다. 기존 명령 이름을 바꾸거나 새 서버/앱 폴더를 만들지 않았다.

추가 수업 결과물은 다음 여섯 파일이다.

- data/checkpoints/player-context-day25-after.json: 최신 입력의 완료 기록, next_line56.
- data/checkpoints/player-context-day25-incomplete.json: 거절 관찰용 별도 한 행 기록, next_line1. 완료하지 않는 것이 해당 실습의 의도다.
- data/handoff/day25-run1/player-context-changes.ndjson: 최신 정규화 입력56행의 bytes 사본.
- data/handoff/day25-run1/checkpoint.json: 인계 사본의 완료 기록.
- data/handoff/day25-run1/player-context.ndjson: 지정 매체 공개 복사본57행.
- data/handoff/day25-run1/manifest.json: 최종 경로·행 수·입력/복사본 SHA·출처·안정 artifact ID 계약.

삭제·이동은 없다. 기존 원본과 계약·5교시 출력/기록·6교시 새 입력은 덮어쓰지 않았다. 실패 관찰의 data/handoff/day25-rejected는 생성되지 않았다.

## 설계 결정과 책임 경계

교안 함수·명령을 그대로 사용했다. _read_handoff_context는 지정 매체를 읽고 아홉 공개 필드·키·삭제 bool·정규화 내용 SHA를 make_context_document로 대조한다. export_context_handoff는 같은 입력 SHA와 완료 위치를 확인한 뒤 입력 bytes 사본·공개 문서 파일·기록·manifest를 임시 package에서 완성하고 마지막에 rename한다. 기존 target은 즉시 거절한다. 입력 SHA와 context SHA는 서로 다른 파일 지문이다.

artifact_id는 MongoDB village_ads.player_context, artifact_version은 v2, 입력 schema는 player-context-change/v1, source_kind는 player-snapshot, binlog_cdc_status는 not-configured다. fixture는 각 문서의 source_kind와 집계에서 구별하며 다른 매체와 추론한 삭제를 추가하지 않는다. 여러 Mongo 문서를 하나의 동일 시점 트랜잭션으로 읽는 모델은 아니며 동결 입력/단일 작성자 조건을 따른다. 정상 적용 작업은 기존 공개 상태가 같은56건이라 Mongo 문서를 새로 쓰지 않았다. 서버 프로세스는 시작/중지하지 않았다.

## 라우팅 문서와 색인

기존 projection/test_events 짝 문서에 실제 새 함수·클래스·파라미터·반환·의사코드·직접 호출·값 출처를 반영했다. 새 Command의 짝 문서와 여섯 결과물의 1:1 짝 문서를 files/<상대경로>.md 규칙으로 추가했다. 기존 current-progress-index.md에 구현과 결과물 색인 및 현재 완료 상태를 연결했다. code/명령/수업 결과물의 실제 경로는 그대로다. 임의의 새로운 검증 디렉터리를 만들지 않고 기존 verification/2026-10-13-day25-period07-review JSON에 day25_period08 항목으로 이번 증거를 추가했다.

## 실행 검사와 결과

- `python ad_config/manage.py check`: 정상.
- `python ad_config/manage.py test ads.test_events.ContextHandoffTests ads.test_events.ContextApiTests ads.test_events.EventAuthTests ads.tests.AuthenticationTests --verbosity 1`: 25개 통과. 실제 MongoDB는 mock, 파일 데이터는 테스트 소유 임시 폴더다. 최초 sandbox 실행은 Windows 임시 폴더 권한 때문에7개 테스트의 setup/cleanup 총14오류였으며, sandbox 밖 실제 사용자 실행 환경에서25개가 통과했다. 교안 소스를 권한 문제 때문에 변경하지 않았다.
- 입력 검사: source56행, document preview version461, 현재 공개 문서57행.
- 최신 입력 새 기록: processed56/duplicate56/applied0/done=true. 반복·사본 소비·최종 완료 확인 각각 processed0.
- 기존 output 재사용: `새 인계 폴더를 지정하세요.` 거절, 네 파일 해시 불변.
- 미완료 기록 인계: `동일 파일의 끝까지 반영한 checkpoint가 필요합니다.` 거절, rejected 폴더 없음.
- 원본/기존 기록 여섯 파일의 해시 불변, Mongo 공개 문서의 정렬 JSON SHA 전후 동일.
- 문서 검사: 표준 routing-doc-auditor는 기존 광고 routing README 부재로 exit2다. 기존 current-progress-index를 유지하고 스킬 extract_symbols/mark_documented API로 이번9개 개발/결과물 파일의 짝 문서·시그니처·색인을 대조했다. CLI 실패를 API 성공으로 바꾸어 기록하지 않는다. 최종 검사와 Git 상태는 기존 finish.json의 day25_period08을 따른다.

실제 실행 증거는 [read-only-checks.json의 day25_period08](../server-routing/verification/2026-10-13-day25-period07-review/read-only-checks.json), [교안 AST 대조](../server-routing/verification/2026-10-13-day25-period07-review/lesson-comparison.json), [마감](../server-routing/verification/2026-10-13-day25-period07-review/finish.json)에 있다. 실제 실행 기록 파일 이름은 이전 작업의 이름을 유지한 것이며 이번 항목에는 승인된 checkpoint/인계 파일 쓰기가 포함된다.

## 제한과 다음 단계

브라우저의 로그인·두 새 광고 선택이나26일차 파이프라인은 이번 파일 인계 범위 밖이라 새로 실행하지 않았다. 원래 SQLite/MySQL Player·광고주 계정·과거 decision·노출/클릭 문서를 변경하지 않았다. 실 Mongo 문서를 바꾸는 충돌/삭제 fixture를 다시 만들지 않았다. 새 checkpoint를 다른 입력 SHA로 재사용하거나 완료 입력을 다음 새 입력으로 덮어쓰지 않는다. 지금 인계는 이미 완료됐으므로 같은 출력 폴더의 export를 다시 실행하면 정상적으로 거절된다.

기존 .gitignore의 **/data/ 규칙은 수업 데이터와 이를 미러링한 새 files/data 짝 문서도 무시한다. 여섯 결과물과 여섯 짝 문서는 실제 파일로 저장돼 있으며 색인/경로 검사는 통과했다. 이 작업에서 기존 Git ignore 정책을 변경하거나 force add하지 않았다. Git에 함께 보관할 필요가 생기면 결과물과 문서의 보관 범위를 별도로 정한다. 이번 로컬 인계 완료와 Git 추적 여부를 구별한다.

## 사용자의 다음 명령

광고 서버 폴더와 기존 가상환경에서 인계 사본을 읽어 완료 상태를 확인할 수 있다. MongoDB는 사용자의 기존 VS Code 터미널에서 유지한다.

```powershell
cd C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python ad_config/manage.py project_player_context --source data/handoff/day25-run1/player-context-changes.ndjson --checkpoint data/handoff/day25-run1/checkpoint.json
```

정상 기대값은 processed=0, next_line=rows=56, done=true다. 다음 소비자는 manifest의 input_path/input_sha256와 checkpoint_path를 함께 사용하며 원래6교시 입력과 인계 사본을 구별한다. 새 인계가 필요할 때만 기존 패키지를 보존하고 새 output-dir를 지정한다. 기존 day25-run1을 삭제하거나 복제하기 위해 덮어쓰지 않는다.
