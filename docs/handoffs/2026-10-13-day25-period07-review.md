# 25일차 7교시 진행 검토 · 2026-10-13

**후속 수정 완료:** 아래 최초 검토는 수정 전 기록이다. 현재 구현·검증·추가 파일 정리 상태는 이 문서 마지막의 후속 수정 항목을 따른다.


## 요청과 결과

사용자가 현재 25일차 7교시 진행 중이며 빠뜨린 부분의 확인을 요청했다. Desktop의 `공개 snapshot을 MongoDB context에 멱등 반영한다.html`을 로컬에서 읽고 1~7교시 제공 완성 함수·Command를 현재 저장본과 비교했다. 문서 안의 구현·실행 지시를 자동 실행 권한으로 취급하지 않았다. 사용자 Python·설정·원본·정규화 파일·checkpoint·DB 업무 문서를 수정하지 않았으며 MongoDB/웹 서버를 켜거나 끄지 않았다. 8교시 구현은 범위 밖이다.

**결과: 1~6교시 핵심 코드와 현재 산출물은 확인됐고, 7교시는 URL·인증 연결 미완료다.** 실제 코드 25개 함수/클래스가 제공 완성 코드와 docstring 제외 AST 기준 모두 같다. 구조 차이를 설명하는 검토이며 코드 복구 작업은 하지 않았다.

## 시작 Git 상태와 보존

Chapter3 루트는 `Git 상태 확인 불가: 저장소 아님`이다. 광고 저장소 HEAD는 `09e18c3 day25 - 5교시`다. staged 없음, 기존 unstaged는 ads/context_projection.py·ads/snapshot_intake.py·ads/views.py, untracked는 ads/management/commands/inspect_decision_context.py·refresh_player_context.py·ads/media_urls.py다. 게임 저장소 HEAD는 `04bafae day25 - chapter1`, staged/untracked 없음, 기존 unstaged는 server/game/ad_gateway.py·server/game/urls.py다.

위 여덟 파일은 전부 작업 시작 전에 존재한 사용자 변경이다. [광고 시작 기록](../server-routing/verification/2026-10-13-day25-period07-review/start.json)과 게임 저장소의 동명 verification/start.json에 Git 항목과 소스 SHA를 기록했다. 저장소 초기화·add·commit·reset은 하지 않았다. 마지막 source SHA와 Git 상태는 [광고 마감](../server-routing/verification/2026-10-13-day25-period07-review/finish.json) 및 게임 마감 기록으로 대조한다. 비밀값·쿠키·CSRF는 복사하지 않았다.

## 확인된 1~6교시 산출물

- 수신 data/exports/day24-input/player-cdc.ndjson과 수신 계약은 56행·공개 계약·지문·source_path 대조를 통과했다. 첫 공개 ID=1, version=460이다.
- data/exports/player-context-changes.ndjson은 정확한 변경 계약과 SHA 대조를 통과한 56행이다. 기본 data/checkpoints/player-context.json은 같은 SHA·next_line=56으로 완료다. player-context-replay.json의 next_line=1은 별도 한 행 재전송 실습 경로이며 전체 처리 미완료 오류로 판단하지 않는다.
- 새 data/exports/day25-refresh-input 원문·수신 계약도 56행으로 대조됐다. 첫 ID=1의 version=461, coins=26, room_id=room-01이다. 기존 day25-live-comparison.json은 ID 1의 version 460→461, 새 ID/누락 없음과 일치한다.
- data/exports/player-context-changes-day25-after.ndjson은 새 수신본을 현재 함수로 정규화한 결과와 56행 전체가 같다. 검사 스크립트의 최초 추정 이름 player-context-changes-refresh.ndjson은 교안의 출력 이름이 아니어서 최종 검사는 교안의 day25-after 이름으로 정정했다. 소스나 산출물을 옮기지 않았다.
- Mongo ping=1.0, village_ads.player_context count=57, media_subject_once 인덱스 unique=True다. fixture가 포함되므로 입력 56행과 전체 저장 count의 차이를 오류로 해석하지 않는다. 새 공개 입력 56개 대상에서 누락·더 오래된 저장 version·같은 version의 context 불일치가 없다.

현재 산출물로 완료 상태를 확인했지만 과거 중지/재개의 모든 콘솔 출력, 실제 Pygame 행동 성공 응답, 충돌/삭제 fixture 실험의 각 단계 화면은 직접 관찰하지 않았다. 검토 때문에 이 실험을 다시 쓰기 실행하지 않았다.

## 7교시 누락과 구조 차이 · 수정 미적용

| 위치 | 현재 사실 | 필요한 연결 |
|---|---|---|
| Game-server/server/game/urls.py:25 | ad_views.ad_context를 참조하지만 ad_views.py와 views.py 모두 함수가 없음. 실제 game check가 AttributeError로 실패 | 교안 제공 ad_context와 imports를 현재 views/ad_views 분리 구조에 맞게 정의하고 실제 존재하는 함수로 URL 연결 |
| ad_server/ad_config/ad_config/urls.py | ads.urls만 include하며 ads.media_urls include 없음. 현재 resolver에서 /api/media/context/가 404 | 기존 활성 URL 순서를 확인하고 매체 include를 연결. 실행 스크립트만으로 해결되지 않음 |
| ad_server/ads/media_urls.py:6~8 | 제공 이름 views.decision/views.event를 썼지만 현재 combined 모듈의 실제 이름은 decision_view/event_view. 모듈 import 시 먼저 decision AttributeError | 현재 함수 이름과 같은 callable을 사용. 기존 decision/events 경로를 중복 등록하지 않도록 상위 include와 함께 조정 |
| Game-server/server/game/ad_gateway.py::request_context + ad_server/ads/media_auth.py::read_media_body | request_context는 교안과 같은 subject-only payload. 현재 광고 인증은 본문의 top-level media_id로 기대 키를 찾으며 이를 헤더와 대조 | 현재 인증 계약과 조회 payload를 일치시켜야 함. 현재 인증을 유지한다면 조회 payload에도 서버 설정의 media_id를 넣는 것이 필요한 차이. 변경하지 않음 |
| ad_server/examples/context-request.json | 폴더와 파일이 없음 | 7교시 무키 POST curl.exe가 읽을 공개 JSON 파일을 교안대로 저장. 키는 넣지 않음 |

또한 examples/copy_context.py(7교시 초급), examples/count_context_statuses.py(앞 교시 초급)가 저장돼 있지 않다. 다른 경로/콘솔에서 연습했는지까지 판단하지 않는다. game/urls.py의 play·events 중복과 두 광고 미리보기 name 중복은 보존했으며 이번 검토로 정리하지 않았다.

현재 인증 decorator의 GET 결과는 405·Allow=POST이지만 빈 본문이다. 교안 예시의 JSON error=method_not_allowed 본문과는 다르다. HTTP 메서드 거절 성공과 JSON 본문 일치를 구별한다. 최신 subject 1의 기존 두 decision은 여전히 context={}이며 현재 공개 복사본보다 이전에 만들어진 기록이다. 과거 값을 새 상태로 덮어쓰지 않았고 이 기록을 7교시 새 연결 성공의 증거로 주장하지 않는다.

## 이번 변경 파일과 책임 경계

개발 파일 추가·수정·이동·삭제는 없다. 광고 짝 문서 네 개를 새로 만들었다: files/ads/context_projection.py.md, files/ads/media_urls.py.md, files/ads/management/commands/refresh_player_context.py.md, files/ads/management/commands/inspect_decision_context.py.md. 기존 files/ads/views.py.md·snapshot_intake.py.md와 current-progress-index.md를 해당 사용자 변경에 맞췄다. 게임은 기존 files/server/game/ad_gateway.py.md·urls.py.md와 docs/server-routing/README.md만 정합화했다. 두 저장소에 이 작업의 handoff와 scoped verification 기록을 추가했다. 소스 파일 이동·새 server/data 디렉터리 생성은 없다.

정규화 계층은 공개 파일과 계약을 검증하고 공개 복사본만 쓰는 기존 사용자 구현이다. 게임 세션 계층은 request.user의 Player를 찾고, gateway는 매체 헤더를 서버 설정에서 읽는다. 광고 인증·HTTP 라우팅·선택 저장은 각각 기존 모듈이 맡는다. 문서에는 현재 import 실패와 401을 기록했으며 미적용 연결을 현재 구조로 묘사하지 않았다.

## 검사 결과

- [교안 AST 대조](../server-routing/verification/2026-10-13-day25-period07-review/lesson-comparison.json): 25개/25개 일치. 기존 apply/normalize/preview/inspect/demo/project/refresh 및 7교시 request/inspect 함수를 포함한다.
- [Django check](../server-routing/verification/2026-10-13-day25-period07-review/django-checks.json): 광고 환경에서 ad_config/manage.py check exit=0. 게임의 server/.venv에서 manage.py check exit=1, game.ad_views.ad_context 없음. 광고 check 성공은 아직 include되지 않은 media_urls의 정상 import를 뜻하지 않는다.
- [읽기 검사와 직접 view probe](../server-routing/verification/2026-10-13-day25-period07-review/read-only-checks.json): 실제 resolver context 404, media_urls import 실패, Mongo/파일 대조 성공. RequestFactory로 context_view만 호출하여 무키 POST 401, 정상 헤더+교안 subject-only POST 401, 기존 인증과 같은 본문 POST 200/no-store/공개 다섯 필드, GET 405/Allow POST를 확인했다. 실 서버 context 경로 성공으로 해석하지 않는다.
- 라우팅 검사: 광고 표준 CLI는 기존 docs/server-routing/README.md가 없어 exit=2다. 기존 current-progress-index.md를 유지하고 스킬 extract_symbols/mark_documented API로 여섯 변경 파일의 짝 문서/색인을 대조한다. 게임은 표준 CLI 두 변경 파일을 검사한다. [광고 CLI 기록](../server-routing/verification/2026-10-13-day25-period07-review/routing-cli-status.json)과 routing-final.json을 따른다.
- git diff --check의 전체 사용자 변경에는 ads/snapshot_intake.py:202의 기존 EOF 빈 줄 문제가 있다. 코드 검사 목적으로 이를 지우지 않았다. 이번 문서 변경만의 whitespace 검사와 전체 결과를 마감 기록에서 구분한다.

초기 검토용 스크립트에서 불필요한 compare_snapshots import와 bs4 가용성 추정이 실패하여 표준 HTMLParser와 실제 모듈 함수로 정정했다. 게임을 광고 가상환경에서 실행한 최초 시도는 daphne 부재로 실패했고, 이후 기존 게임 server/.venv에서 올바른 AttributeError를 재현했다. 의존성을 설치하거나 사용자 실행 환경을 변경하지 않았다. 조회·비교 검토이므로 새로운 테스트 파일이나 업무 데이터를 만들지 않았다. 로그인 브라우저의 본인 조회·쿼리 ID 무시·두 새 광고 선택의 과거 기록 보존은 위 연결 수정 전이라 미검증이다.

## 다음 확인 순서와 정확한 명령

이 검토는 위 연결을 수정하지 않았으므로 다음 두 check 중 게임은 현재 실패한다. 함수·URL·인증 계약을 먼저 연결한 뒤 각각 해당 기존 가상환경에서 확인한다.

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python ad_config/manage.py check
```

```powershell
Set-Location C:\MLO01-01\Chapter3\Game-server\server
.\.venv\Scripts\Activate.ps1
python manage.py check
```

두 check 성공 후 기존 VS Code 터미널에서 광고는 `python ad_config/manage.py runserver 127.0.0.1:8001`, 게임은 `python manage.py runserver 127.0.0.1:8000`으로 실행한다. MongoDB는 사용자가 현재 실행한 터미널을 그대로 유지한다. 요청 JSON을 저장한 뒤 광고 작업 폴더에서 교안의 무키 POST 401와 GET 405를 검사하고, 로그인 브라우저에서 `http://127.0.0.1:8000/api/ads/context/`의 본인 공개 ID와 `http://127.0.0.1:8000/ads-preview/`의 새 선택 ID를 대조한다. URL 쿼리의 다른 subject로 조회 대상을 바꾸지 않는다.

광고 작업 폴더에서 실제 본인 subject가 1이면 다음을 사용한다. 다른 ID면 그 값만 바꾼다.

```powershell
python ad_config/manage.py inspect_decision_context --subject 1 --latest
```

출력 latest ID를 방금 화면 ID와 확인한 뒤 같은 명령의 `--decision-id`에 그 실제 ID를 넣어 당시/현재 context를 읽는다. 그 다음 새 선택을 한 번 더 요청해 두 ID를 구별하고 첫 ID의 context/selected_at 보존을 확인한다. 기존 빈 context decision을 고치거나 예시 UUID로 새 기록을 만들지 않는다.


## 후속 요청 · 기존 폴더·파일만 사용한 7교시 수정

사용자가 수정까지 요청한 후 새 폴더/파일을 만들지 말라고 지정했다. 최초 추가한 별도 context 테스트 파일 두 개와 examples의 공개 JSON·초급 예제 파일 두 개를 확인·제거하고, 빈 examples 디렉터리도 제거했다. context 테스트 클래스는 기존 ads/test_events.py와 Game-server/server/game/test_ads.py에 통합했다. 테스트 추가로 기존 테스트 클래스 본문을 교체하지 않았다. 문서·검증 기록은 이 기존 인수인계 및 기존 verification/2026-10-13-day25-period07-review 파일에 후속 항목으로 반영했다.

수정 시작 Git은 최초 검토 마감 상태 그대로였으며 HEAD는 광고09e18c3·게임04bafae, 기존 staged 없음이다. 이전 문서/사용자 Python 변경은 작업 시작 전에 존재한 것으로 분류했다. 정확한 시작 상태·작업 전 소스 사본·SHA는 기존 start.json의 followup_fix_start에 있다. 기존 사용자 여덟 개발 파일의 짝 문서/색인이 일치함을 먼저 확인한 뒤 코드 수정을 시작했다. 최종 차이는 finish.json의 followup_fix에서 시작 시점과 비교한다.

실제 개발 변경은 광고 ads/media_urls.py(기존 callable 이름), ad_config/ad_config/urls.py(매체 include), ads/urls.py(매체 두 항목을 전용 목록으로 일원화), ads/media_auth.py(헤더 매체 인증과 JSON405), ads/test_events.py(새 context 클래스)와 게임 server/game/views.py(제공 ad_context/import), server/game/urls.py(views.ad_context 연결), server/game/test_ads.py(새 context 클래스)의 총 여덟 기존 파일이다. 사용자 context_projection·snapshot_intake·views의 context_view·두 관리명령·게임 gateway/ad_views 본문은 보존했다. ad_context는 교안 제공 함수 AST와 같다.

기존 광고주 폼·로그인·선택·사건의 공개 주소는 같다. 매체 URL을 media_ads namespace로 일원화했으며 소스의 ads:decision/ads:events reverse 사용은 검색에서 없었다. 기존 top-level media_id 요청은 계속 허용하되 헤더와 다른 값은 기존처럼401다. 인증한 매체와 다른 subject는400다. 교안처럼 subject만 보낸 정상 헤더 조회가200, GET이JSON405/Allow POST다. 매체 서버만 csrf_exempt이고 게임/광고주 CSRF는 유지한다.

두 실제 가상환경의 check가 모두 exit0다. 광고 `python ad_config/manage.py test ads.test_events.ContextApiTests ads.test_events.EventAuthTests ads.tests.AuthenticationTests --verbosity 1`은18개, 게임 `python manage.py test game.test_ads.PlayerContextTests game.test_ads.GatewayTests.test_event_error_codes_are_preserved_without_private_details game.test_ads.GatewayTests.test_event_public_receipt_duplicate_and_recipient --verbosity 1`은6개 통과했다. 전체 수업 테스트를 통과했다고 주장하지 않으며 수정한 인증·세션 경계·HTTP contract 범위다. 초기 별도 테스트 파일의 검사도 통과했으나 최종 결과는 기존 파일로 통합한 뒤 실행한 결과다. django-checks.json의 followup-fix-existing-files-only 항목에 명령/종료/출력을 보존했다.

실제 MongoDB를 사용하는 Django Client에서 /api/media/context/를 정상 인증으로 읽어200/no-store/subject1/version461을 확인했다. 무키401, GET405/Allow POST/method_not_allowed JSON도 확인했다. campaign/bid/decision/event/context count는 이 읽기 검사 전후 같았다. 첫 Client probe는 기본 testserver Host로400이어서 실제 허용한127.0.0.1 Host로 수정해 재검사했다. ALLOWED_HOSTS나 환경 설정은 바꾸지 않았다. MongoDB 및 사용자 웹 서버 프로세스를 시작/중지하지 않았다. 테스트 광고 선택은 모의 HTTP이고 실제 새 decision은 만들지 않았으므로 로그인 브라우저의 두 새 결정 관찰은 사용자 단계다.

여덟 개발 파일의 기존 짝 문서와 기존 색인을 검증 후 정합화했다. 변하지 않은 gateway/광고 context_view 짝 문서의 과거404·401 상태 설명도 새 연결 상태로 정정했다. 새로운 짝 문서·인수인계 파일을 만들지 않았다. 광고 스킬 CLI의 README 부재 exit2는 그대로이며 scoped AST API로 기존 색인과 문서를 검증한다. 게임 표준 CLI와 scoped 검사는 마감 기록을 따른다. 전체 git diff --check의 기존 사용자 snapshot_intake EOF 빈 줄과 이번 변경 문서/소스 검사를 구분한다.

### 새 검증 기록 폴더 정리 · 사용자 승인 후 삭제 완료

수정 시작에 에이전트가 새로 만든 `ad_server/docs/server-routing/verification/2026-10-13-day25-period07-fix`와 `Game-server/docs/server-routing/verification/2026-10-13-day25-period07-fix` 두 기록 폴더는 사용자 명시적 승인 후 경로·파일 목록·SHA를 재대조하여 삭제했다. 내용은 시작 JSON·라우팅 결과·작업 전 소스 사본이며 기존 start.json으로 필요한 기록을 통합했다. 이 기록 폴더의 재귀 삭제가 자동 승인 심사에서 거절됐다. 사유는 사용자가 새 파일 생성을 거부했지만 기록 삭제를 명시적으로 승인하지 않았다는 것이다. 우회 삭제하지 않았고 사용자의 “새 검증 기록 폴더 두 개 삭제” 응답 후 승인 범위의 두 폴더만 삭제했다. 공개 개발 구조의 새 파일은 없지만, 기록 폴더 정리도 완료됐다. 경로·해시·원래 요청의 범위와 삭제 확인 결과는 기존 start.json의 followup_remove_agent_created_files 및 finish.json에 기록한다.

### 사용자가 실행할 명령

새 예제 파일 없이 기존 VS Code 두 터미널에서 재시작한다. MongoDB 터미널은 현재 실행 상태를 유지한다.

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python ad_config/manage.py runserver 127.0.0.1:8001
```

```powershell
Set-Location C:\MLO01-01\Chapter3\Game-server\server
.\.venv\Scripts\Activate.ps1
python manage.py runserver 127.0.0.1:8000
```

교안의 무키 POST는 새 JSON 파일을 만드는 대신 같은 공개 본문을 stdin으로 전송한다.

```powershell
'{"subject":{"media_id":"village-game","subject_id":"1"}}' | curl.exe --include --request POST "http://127.0.0.1:8001/api/media/context/" --header "Content-Type: application/json" --data-binary "@-"
curl.exe --include --request GET "http://127.0.0.1:8001/api/media/context/"
```

첫 요청401, 두 번째405/Allow POST/JSON을 읽는다. 기존 로그인 브라우저의 http://127.0.0.1:8000/api/ads/context/에서 본인 subject를 확인하고 /ads-preview/에서 광고를 새로 요청한다. 광고 폴더의 `python ad_config/manage.py inspect_decision_context --subject 1 --latest`에서 화면 ID와 대조한다. 본인 공개ID가 다르면1만 실제 값으로 바꾼다. 이후 첫 실제ID로 --decision-id 조회하여 두 번째 선택 뒤에도 과거 context/selected_at이 보존되는지 관찰한다. 기존 빈 context 기록을 수정하지 않는다.


후속 마감에서 사용자가 작업 중 일부 게임 변경을 staged한 것을 확인했다. 이미 삭제된 에이전트 생성 테스트 파일/검증 사본 여섯 항목도 인덱스에 남아 있어, 생성 당시 내용과 Git CRLF/LF 정규화의 동일성을 확인한 뒤 해당 경로만 git rm --cached로 제거했다. 첫 sandbox 시도는 index.lock 쓰기 권한이 없어 실패했고 승인된 cleanup 범위의 sandbox 밖 실행으로 완료했다. 다른 사용자 staged 코드/문서 항목은 보존했고 add/commit/reset을 수행하지 않았다. 마지막 Git HEAD·staged/unstaged 분류와 생성 경로의 인덱스 잔존 여부는 finish.json의 followup_fix가 기준이다.
