# 광고 현재 진행 라우팅 문서 정합화 인수인계

사용자는 현재까지 진행에 맞춰 라우팅 문서를 갱신하고 서브에이전트를 사용하도록 요청했다. 광고 저장소 담당 서브에이전트가 실제 소스의 스킬 AST 구조를 기준으로 최초 누락 짝 문서 17개와 작업 도중 관찰한 사용자 snapshot 작성 중 소스의 짝 문서 1개를 추가하고 현재 진행 색인과 낡은 진행 설명을 맞췄다. 에이전트는 Python·설정·데이터·환경 파일을 수정하지 않았으며 export/DB 게시/전달/서버 실행·종료/stage/commit을 수행하지 않았다.

## 시작 상태와 기존 작업 보존

- 작업 폴더/Git 경계: `C:/MLO01-01/Chapter3/ad_server`의 독립 Git 저장소. HEAD는 `8f541e4 day23 - finish`다.
- 시작 시 HEAD 대비 변경, staged, unstaged는 모두 없었다. rename/delete 상태도 없었다.
- 기존 untracked: `docs/handoffs/2026-10-08-day24-period01-review.md`, `docs/handoffs/2026-10-08-day24-data-path-correction.md`, `docs/server-routing/day24-period01-index.md`, `docs/server-routing/files/tools/check_day24_logic.py.md`, `tools/check_day24_logic.py`, `docs/server-routing/verification/day24-period01-review/`와 `day24-data-path-correction/`의 기존 근거 파일들이다. 개별 경로는 [부모 에이전트 시작 상태](../server-routing/verification/day24-routing-sync/start-state.json)에 있다. 모두 작업 시작 전에 존재한 변경이다.
- `docs/server-routing/README.md`는 시작 HEAD에도 없었다. 삭제를 되돌리지 않고 별도 현재 진행 색인을 추가했다.
- 기존 `day24-period01-index.md`를 먼저 읽고 사용자의 게임 snapshot 이동/외부 data 경로 설명을 보존한 채 새 현재 색인과 소비 미적용 상태만 덧붙였다. 이전 인수인계/verification은 역사 자료로 유지했다. 비밀값·환경값·쿠키·토큰은 문서와 증거에 복사하지 않았다.

## 이번 파일 변경

새 짝 문서 18개:

- 기능 6개: `docs/server-routing/files/ads/{timestamps,exporting,delivery}.py.md`, `docs/server-routing/files/ads/management/commands/{export_ad_events,deliver_ad_events,check_ad_reports}.py.md`.
- 독립 실습/교안 참고 3개: `docs/server-routing/files/config/day23-period-{04,05,07}.py.md`.
- 초기 package/scaffold 8개: `docs/server-routing/files/ad_config/ad_config/{__init__,asgi,wsgi}.py.md`, `docs/server-routing/files/ads/{__init__,admin,apps,models}.py.md`, `docs/server-routing/files/ads/migrations/__init__.py.md`.
- 작업 중 새 사용자 파일의 짝 문서 1개: `docs/server-routing/files/ads/snapshot_intake.py.md`. 현재 제공 helper와 inspect의 작성된 검사/수집시각 검사 미호출을 구분했다.

추가한 색인은 [current-progress-index.md](../server-routing/current-progress-index.md)다. 이 인수인계와 `docs/server-routing/verification/day24-routing-sync/agent-*` 구조/링크/범위 검사 결과도 추가했다.

수정한 기존 Markdown 9개:

- `README.md`: NDJSON·보고서·전달이 아직 미적용이라고 적힌 진행 설명을 현재 소스에 맞추고 실제 메뉴와 24일차 소비 미적용/게임 data 입력 경로를 명시했다.
- `docs/server-routing/files/README.md.md`: 위 안내 문서의 현재 책임과 진행을 반영했다.
- `docs/server-routing/files/ads/templates/ads/events.html.md`: 보고서 메뉴가 상속한 base.html에 이미 있다는 현재 관계를 반영했다.
- `docs/server-routing/files/ads/repository.py.md`: save_campaign의 data가 실제 입력 mapping이며 HTMLParser 문자 데이터가 아님을 정정했다.
- `docs/server-routing/files/ads/tests.py.md`: csrf_headers가 None 대신 테스트 응답에서 만든 헤더 사전을 반환하는 계약을 정정했다.
- `docs/server-routing/files/ads/media_auth.py.md`: 최상위 함수가 decorator를 반환하고 nested decorate/wrapped가 인증·메서드 제한·원래 view 호출/오류 응답을 담당함을 추가했다.
- `docs/server-routing/day23-period06-index.md`, `day24-period01-index.md`: 당시 범위를 유지하고 현재 전체 진행 색인으로 연결했다.
- `docs/server-routing/files/tools/check_day24_logic.py.md`: 작업 중 저장된 2교시 소스와 captured_at 검사 미호출/검사 미실행을 현재 상태로 맞췄다. 원본 검사기 코드는 보존했다.

이번 작업은 문서만 추가/수정했다. 소스/문서 이동·삭제는 없고 기존 검사기 파일 추가를 이번 에이전트 작업으로 주장하지 않는다. 기존 정상 짝 문서를 일괄 재생성하지 않았다.

## 책임 경계와 현재 구현

기존 루트 include·`ads/urls.py`·통합 `ads/views.py` 구조와 `ad_config/manage.py`를 유지한다. 광고주 인증, 캠페인/입찰/PNG, 매체 선택, 결정 snapshot, 최초 노출·클릭과 실적 목록이 현재 구현이다. 파일 내보내기/후보 계산/업무 키 게시/보고서 UI/한 writer 전달/게시 보고서 대조의 실제 소스도 있다. 코드 존재·문서 정합성·과거 실행 증거를 구분하며 이번 문서 작업에서 실제 쓰기 명령을 실행하지 않았다.

`export_ad_events`는 impression_time의 `[since, until)` 범위로 공개 사건을 저장하고 `build_ad_reports`는 후보 파일만 만든다. `load_ad_reports`/`publish_reports`만 게시 쓰기를 담당한다. 보고서 view는 로그인 광고주의 게시 행을 읽으며 공통 메뉴에서 9개 열·CTR 0~1·원본 ISO 시각·빈 목록을 표시한다. 7교시 전달은 파일 교체 뒤 DB 표식을 저장한다. 8교시 `check_ad_reports`는 게시 전체 조회와 전체 보관 사건 후보를 대조하며 Spark/GUI 실행 성공을 보장하지 않는다.

광고 24일차는 현재 공식 검사기와 작성 중인 2교시 `ads/snapshot_intake.py`가 저장된 상태다. 최신 inspect는 8필드/출처 확인 → 공개 다섯 필드 helper → ID 중복 거절/등록 → parse_utc 이름 식 → 첫 수집값 보관/후속 값 비교 → 메타데이터 반환 순서다. parse_utc를 captured_at으로 호출하지 않아 수집 시각 ISO/시간대 검사는 아직 수행하지 않는다. 실제 2교시 검사를 실행하지 않았으며 snapshot 검증/소비 성공으로 기록하지 않는다. 3~8교시 후속 소비 구현과 관리명령은 없고 게임 ORM import도 없다. snapshot 명령은 게임 `server/game/management/commands/export_player_snapshot.py`, 광고 입력 경로는 `../Game-server/data/exports/player-cdc.ndjson`다. 앞선 읽기 전용 메타데이터 검사에서 56행·13275 bytes·SHA-256 `6ea30948a1c6924b186676511207bd2099683ca00cf1b1582cb595e6437375d0`이고 `Game-server/server/data`와 옛 광고 snapshot 명령은 없음을 확인했다. 파일/DB 데이터는 수정하지 않았다.

## 작업 중 새 사용자 파일 관찰

부모의 최종 확인 중 `ads/snapshot_intake.py`가 새로 생성돼 있었고 최초 파일 수정 시각은 2026-10-08 16:40경이었다. 이 파일은 작업 시작의 비문서 소스 69개에 없던 새 사용자 작업 또는 작성자 확인 불가 변경이다. 에이전트 구현으로 주장하지 않으며 소스를 완성/교정하지 않았다. 최초 관찰 bytes는 3526, SHA-256은 `dd09b141e4fcd154ad1931f0cd84357130a26b71956b4e415b1ef4436180e6ad`였고 빈칸이 남은 문제틀이었다. [최초 소스 관찰 구조](../server-routing/verification/day24-routing-sync/agent-user-snapshot-observation.json)에 당시 세 함수의 AST와 소스 해시를 보존했다.

사용자가 계속 저장해 16:44:28경 소스는 3712 bytes, SHA-256 `02fa6834b3fd64bc69706976851544cf8db41008036feaeba7376258ec80483d`로 바뀌었다. 이 저장본에는 빈칸이 없고 필드/공개 상태/중복/수집값 통일 검사가 작성돼 있으나 captured_at 검사 helper는 호출되지 않는다. [부모의 사용자 저장 중 관찰](../server-routing/verification/day24-routing-sync/concurrent-source-observation.json)에 최초/최신 저장 이력이 있다. 초기 해시와 달라진 것은 작업 중 사용자 저장으로 구분하며 최초 빈칸/부재를 현재 동작으로 기록하지 않는다. 최신 문서와 별도 관찰 해시를 대조해 마감했다.

새 소스를 읽고 짝 문서를 추가한 뒤 현재 진행 색인·README·24일차 색인·검사기 짝 문서의 상태만 최소 정정했다. 이전 snapshot_intake 부재를 기록한 `agent-snapshot-boundary.json`은 관찰 당시 근거로 보존했다. 앞선 56파일·150심볼/27문서 결과도 `agent-*-before-user-addition.json`으로 보존하고, 최신 구조/링크 결과는 새 사용자 소스를 포함해 다시 생성했다. 문서 구조의 일치는 작성 중 함수의 기능 성공을 뜻하지 않는다.

## 검사와 근거

`routing-doc-auditor`의 `scripts/audit_routing.py`를 먼저 실행하고 그 스킬의 `changed_paths`, `extract_symbols`, `mark_documented` API 구조화 결과로 범위를 좁혔다. 첫 전체 구조 검사는 Python 56파일·150심볼의 기존 짝 시그니처가 있는 문서는 일치했고, 짝 문서 17개와 기존 두 교시 색인에 없는 경로를 보고했다. API의 전체 범위는 Git tracked/untracked Python이며 `.venv`/데이터/비밀값 원문을 읽어 문서화하는 검사가 아니다.

표준 CLI 명령:

```powershell
& 'C:\Users\이해나\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -X utf8 -B 'C:\Users\이해나\.codex\skills\routing-doc-auditor\scripts\audit_routing.py' --repo 'C:\MLO01-01\Chapter3\ad_server' --routing-dir 'docs/server-routing' --include-all --format json --output 'C:\MLO01-01\Chapter3\ad_server\docs\server-routing\verification\day24-routing-sync\agent-routing-cli-final.json'
```

현재 CLI는 라우팅 README를 필수로 요구하므로 `routing directory is incomplete`, 종료 코드 2, `summary.ok=false`다. README를 임의 복원해 CLI 성공으로 기록하지 않았다. 동일 스킬 API의 새 현재 색인 검사는 [agent-routing-final.json](../server-routing/verification/day24-routing-sync/agent-routing-final.json)에 있으며 새 사용자 파일을 포함한 Python 57파일·153심볼, 누락/파싱 오류 0개, `summary.ok=true`다. 추가/정정 문서의 상대 링크와 실제 파일 경계는 [agent-document-checks.json](../server-routing/verification/day24-routing-sync/agent-document-checks.json), snapshot 경계의 앞선 관찰은 [agent-snapshot-boundary.json](../server-routing/verification/day24-routing-sync/agent-snapshot-boundary.json)을 따른다. 이 구조 검사는 inspect 문제틀의 실행 성공을 검사하지 않는다.

기존 교안 정합화 도구 실행:

```powershell
& 'C:\Users\이해나\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -X utf8 -B 'C:\MLO01-01\Chapter3\ad_server\tools\verify_lesson_alignment.py' --output 'C:\MLO01-01\Chapter3\ad_server\docs\server-routing\verification\day24-routing-sync\agent-lesson-alignment.json'
```

결과: 종료 코드 0, `Lesson source comparison: PASS 23 checks`. 22일차와 수정 23일차 1·2교시의 선언된 구조 적응을 반영한 AST/표 비교다. 최신 3교시 공식 검사나 이후 모든 교시의 원문 일치를 의미하지 않는다. 소스/링크 검사를 마친 뒤 이번 문서만 다시 정합화하고 Git 상태/기존 소스 해시 보존을 확인했다.

최종 문서 검사에서 작업 Markdown 29개의 상대 링크 깨짐은 0개였고 시작 상태의 비문서 소스 69개 SHA-256이 모두 유지됐다. 작업 중 추가된 snapshot 소스는 최신 별도 관찰 해시로 보존을 확인했다. [최종 Git 확인](../server-routing/verification/day24-routing-sync/agent-git-final.json)의 HEAD는 시작과 같고 staged는 비어 있다. 기존 미추적 자료, 새 사용자 소스, 이번 문서 추가/수정은 시작 상태/별도 관찰과 파일 변경 목록으로 구분했다. 부모 에이전트도 별도 최종 상태/해시 검사를 수행한다.

마지막 `git diff --check`는 종료 코드 0이고 공백 오류가 없었다. Git의 기존 LF→CRLF 정책 안내만 출력됐으며 줄바꿈 설정을 변경하지 않았다.

최초 광고 `.venv/Scripts/python.exe` 시도는 실제 Python314 경로를 찾지 못해 종료 코드 1로 검사기 실행까지 도달하지 못했다. 환경을 고치거나 runtime을 설치하지 않고 이미 제공된 번들 Python으로 표준 라이브러리 기반 검사를 수행했다. 종료 코드와 README로 인한 CLI 제한을 별개로 기록한다.

## 남은 사항과 다음 확인

문서 작업에서 DB 쓰기를 수반하는 기존 Mongo 통합검사·전달·export·보고서 게시 명령, 실제 사용자 창 관찰은 재실행하지 않았다. 기존 기능 검증 결과는 해당 시점의 인수인계/verification에 보존했다. 현재 코드에서 발견한 `ads/delivery.py` 하단 demo print는 import 시 stdout에 예시 사전을 쓰므로 deliver 명령의 출력이 JSON 한 줄만 나오지 않을 수 있다. 해당 부수효과는 코드 수정 없이 실제 동작으로 문서화했다. 파일 전달의 시각 정렬은 문자열순이며 별도 UTC 정규화가 없다는 실제 계약도 명시했다.

다음 작업은 [현재 진행 색인](../server-routing/current-progress-index.md)에서 해당 소스/짝 문서를 먼저 읽는다. 24일차 2교시 검사 함수는 작성 중이고 captured_at 시각 검사 미호출로 미완료이며, 3~8교시 후속 소비는 미적용이다. 문서 갱신만 요청한 이번 결과를 확인하기 위해 사용자가 서버를 재시작하거나 기존 snapshot을 다시 내보낼 필요는 없다. Git stage/commit은 수행하지 않았다.
