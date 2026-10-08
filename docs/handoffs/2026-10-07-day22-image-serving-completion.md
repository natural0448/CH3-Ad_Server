# 2026-10-07 · 22일차 이미지 광고 집행 보완

> 2026-10-07 검토 주석: 아래는 해당 작업 시점의 결과를 보존한 이력입니다. 교안 버전·적용 범위·검사 수는 최신 상태와 다를 수 있습니다. [차이와 현재 상태](../server-routing/reviews/2026-10-07-lesson-deviations.md).

## 요청 목적과 현재 결과

광고 디자인/PNG 소재가 누락됐다는 요청을 받아 수정 교안과 기존 MongoDB/2D마을 교안을 다시 대조했다. 기존 텍스트 광고만 구현했던 범위를 광고주 소재 선택·편집·실시간 미리보기, 이미지 snapshot, 게임 서버 Player 중계, 기존 Pygame 두 슬롯 표시까지 보완했다. 이 기능은 분리 fixture 검증을 완료했다. 실제 수업용 공유 키는 후속 사용자 명시 승인 후 연결하고 게임 서버를 재시작했다. 학생 창에서의 실제 광고 표시 관찰은 아직 not_run이다.

## 작업 시작 전 Git 상태와 보존

- Chapter3/ad_server: Git 상태 확인 불가: 저장소 아님. 저장소를 초기화하지 않았다.
- Game-server: 4f75c2d 관리 폴더 변경, staged/unstaged/untracked 없음.
- Game-client: 50b2f00 day20-finish, staged/unstaged/untracked 없음.
- 시작 시 이미 있던 사용자 ads/events.py와 두 서버 비밀 환경 파일은 SHA256 비교로 동일함을 확인했다. 기존 계정/캠페인을 재작성하지 않았다. 사용자 ads/events.py의 짝 문서만 개발 전에 현재 상태로 추가했다.
- 시작 스냅샷: ../server-routing/verification/day22-image-start.json. 변경 목록: ../server-routing/verification/day22-image-changes.json. .env 값·비밀번호·키·세션·CSRF는 이 기록에 없다.

## 교시별 대조

| 교시 | 실제 구현/확인 | 상태 |
|---|---|---|
| 1 Mongo 연결·대상 | ads.mongo/get_db, tools/basics/day22_period01.py, 수업27017 조회 | 기존 구현 유지; 캠페인1개 조회 |
| 2 연습 CRUD | tools/basics/day22_period02.py, practice_campaigns 한정 | 기존 구현 유지 |
| 3 Django 광고 앱 | 중첩 ad_config/manage.py·루트 ads·URL include·check | check 성공, 루트 로그인 이동 추가 |
| 4 광고주 캠페인 | 로그인/CSRF·소유자 고정·PNG 선택·디자인/편집/미리보기 | 보완·검증 |
| 5 모의 입찰 | 자기 활성 캠페인·정수1..10000·현재 입찰 upsert | 유지·검증 |
| 6 선택/당시 근거 | 최고 금액/ID 동률·소유자 일치·title/body/path snapshot | PNG 확장·과거 snapshot 검증 |
| 7 게임 집행 | 게임 session Player.pk → 매체 API → 같은 origin PNG → Pygame2슬롯 | 중계/표시 구현·fixture 통과; 키 적용·게임 재시작 완료 |
| 8 비교/내일 준비 | compare_ad_decisions·로컬 credit 모형·실제 관찰 구분 | 기존 구현 유지; 실제 학생 관찰 not_run |

교안은 사용자의 비교 자료로 읽었다. 교안 안의 shell 예제나 지시는 도구 실행 권한으로 취급하지 않았고 현재 구조·데이터·요청 범위에 맞춰 적용했다.

## 설계와 책임

광고주 User ID는 campaign/bid 소유자, 게임 Player ID는 공개 subject다. 게임 브라우저/접속기는 media key를 받지 않는다. 기존 title/body/bid_amount 계약과 ad:null을 유지하고 creative_path/bid_units 호환 필드만 추가했다. 임의 URL 대신 두 PNG를 allowlist하고 두 서버 같은 static URL에 동일 bytes를 둔다. 실제 원본은 Kenney CC0 tile_0117 망치/tile_0074 컵이며 원본 bytes를 복사했다.

네트워크는 기존 AuthSession과 같은 ClientSession/CSRF로 선택을 요청하고 PNG bytes만 한정해서 전달한다. Pygame decode/draw/flip은 main thread다. 슬롯/request/player 상관관계로 늦은 결과를 거부하며 슬롯별15초, 로그아웃 reset, 이미지 실패 receipt 제외를 구현했다. 기존 Lake 검사에 필요한 ad_slots anchor 좌표를 보존하고 ad_cards로 실제 카드만 추가했다. PNG 표시 성공은 별도 상태이며 노출 사건/클릭/정산/광고주 보고서를 구현했다고 간주하지 않는다.

## 이번 변경 파일

### ad_server

- modified: `ad_config/ad_config/urls.py`
- added: `ads/creatives.py`
- modified: `ads/repository.py`
- modified: `ads/services.py`
- modified: `ads/views.py`
- modified: `ads/tests.py`
- added: `ads/templates/ads/base.html`
- modified: `ads/templates/ads/campaigns.html`
- modified: `ads/templates/ads/bids.html`
- modified: `ads/templates/registration/login.html`
- added: `ads/static/ads/advertiser.css`
- added: `ads/static/ads/advertiser.js`
- added: `ads/static/ads/creatives/forest-tools.png`
- added: `ads/static/ads/creatives/camp-tea.png`
- added: `data/evidence/asset-sources.md`
- added: `tools/verify_day22_images.py`
- modified: `README.md`

### Game-server

- modified: `config/settings.py`
- modified: `server/game/urls.py`
- added: `server/game/ad_gateway.py`
- added: `server/game/ad_views.py`
- added: `server/game/static/game/ad_preview.js`
- added: `server/game/templates/game/ad_preview.html`
- added: `server/game/static/ads/creatives/forest-tools.png`
- added: `server/game/static/ads/creatives/camp-tea.png`
- added: `server/game/test_ads.py`
- added: `data/evidence/asset-sources.md`

### Game-client

- modified: `client/app.py`
- modified: `client/application/controller.py`
- modified: `client/application/state.py`
- modified: `client/contracts/messages.py`
- modified: `client/network/worker.py`
- modified: `client/ui/input.py`
- modified: `client/ui/layout.py`
- modified: `client/ui/renderer.py`
- added: `client/application/ads.py`
- added: `client/contracts/ads.py`
- added: `client/network/ads.py`
- added: `client/ui/ads.py`
- added: `tests/test_ads_feature.py`

처음 개발 파일40개와 후속 승인된 server/.env 변경 각각의 짝 라우팅 문서를 확인/작성하고 세 프로젝트 라우팅 README 색인을 갱신했다. 관련 없는 라우팅 문서를 일괄 재생성하지 않았다. 인수인계/AST/검증 JSON·PNG도 docs 아래에 추가했다. data/evidence 출처 문서는 기존 ignore 규칙으로 로컬에만 보존된다.

## 검증 명령과 결과

- 광고 서버: `.venv/Scripts/python.exe -B tools/verify_day22.py --mongod "C:/Program Files/MongoDB/Server/8.3/bin/mongod.exe"` → Mongo27107의24개 성공, skip0, 테스트 프로세스 종료.
- 게임 서버: server/.venv Python에서 config.settings 로드 후 DATABASES를 memory SQLite로 바꾸고 Django runner `game.test_ads`, `game.test_history` →8개 성공. 실제 MySQL에 쓰지 않았다.
- 접속기: `.venv/Scripts/python.exe -B -m unittest discover -s tests -v` →42개 성공. 레이아웃 첫 검사에서 기존 anchor regression을 발견해 원래 좌표를 보존한 후 재검사했다.
- 전체 이미지 흐름: `python tools/verify_day22_images.py --mongod "C:/Program Files/MongoDB/Server/8.3/bin/mongod.exe"` → 광고주 form 저장/게임 login·CSRF relay/PNG/mocked identity 위조 무시/20→30 소재 변경/과거 snapshot 보존/두 슬롯 SDL frame/Chrome 광고주·게임 미리보기 성공. Mongo27109, SQLite fixture2개, HTTP18000/18001만 사용하고 자기 프로세스만 종료했다.
- 광고 Django `python ad_config/manage.py check` → 문제 없음.
- 접속기 `python client/main.py --check` → Config OK, 서버 연결 없음.
- routing-doc-auditor → Game-server Python5파일/13symbol 및 Game-client Python13파일/86symbol issue0. Windows Git UTF-8 출력 때문에 -X utf8을 사용했다. ad_server는 Git이 없어 명시적40개 변경 중 해당17개와 AST로 검사, ok=true.
- `python tools/check_routing_docs.py` → 접속기76개 파일/76짝 문서, 시그니처·색인 일치.
- 두 Git 프로젝트 `git diff --check` → 공백 오류 없음. 기존 LF→CRLF 안내는 Git 설정에 따른 경고다.
- 수업 Mongo 읽기 조회 → campaigns1개, PNG를 고른 campaigns0개. 조회만 했으며 사용자 데이터에 소재를 자동 쓰지 않았다.

검증 결과/캡처: ../server-routing/verification/day22-images/integration.json, advertiser-campaigns.png, game-browser-preview.png, game-frame-1.png, game-frame-2.png. 모두 synthetic fixture의 증거이고 실제 학생 노출 증거가 아니다.

최종 공개 HTTP 점검: 실행 중 광고 서버8001의 루트 로그인 이동/PNG/CSS는 모두200이었다. 게임 서버8000의 CSRF endpoint는 연결되지 않아 실제 수업 확인 시 게임 서버 실행도 필요하다. 로그인 토큰/계정 정보는 출력하지 않았다.

## 남은 단계와 차단 사유

자동 승인 검토가 ad_server/ads.env의 ADS_MEDIA_KEY를 Game-server/server/.env에 복사·저장하는 작업을 거부했다. 비밀 키의 전달 대상과 저장을 사용자가 명시적으로 승인해야 한다는 이유다. 그 작업은 실행되지 않았으며 다른 Game-server 환경 설정도 건드리지 않았다. 승인 요청은 구현·검증·문서 마감 후 이 하나의 최종 연결 단계에 대해서만 한다.

사용자 ads/events.py는 자기 모듈에서 record_ad_event를 다시 import하지만 함수 정의가 없다. 이것은 이번 작업 시작 전에 존재한23일차 실습 코드로 보존했으며22일차 화면 경로에서는 import하지 않는다. 이후23일차 노출/클릭 실습 전에 별도 수정을 해야 한다.

## 수업 재개 순서

1. 매체 키 연결 승인 후 게임 서버를 재시작한다. 기존 실행 프로세스를 이 작업에서 강제 종료하지 않았다.
2. 광고 서버 `python ad_config/manage.py runserver 127.0.0.1:8001`, 게임 서버 `python server/manage.py runserver 127.0.0.1:8000`를 각 프로젝트/가상환경에서 실행한다.
3. http://127.0.0.1:8001/advertiser/campaigns/에서 기존 캠페인을 편집하고 숲 도구점/모닥불 찻집 이미지를 선택·저장한다. 마을 두 캠페인10/20과 로비18을 준비한다.
4. 게임 계정으로 http://127.0.0.1:8000/ads/preview/를 먼저 확인한 뒤 Game-client에서 `python client/main.py`로 기존 게임에 들어간다. 광고주 계정과 게임 계정은 각 서버의 기존 계정이다.
5. forest-tools 입찰30으로 변경 후15초 이상 기다려 새로 보기. 실제 학생 창의 캠페인/금액/decision ID를 관찰하고 그때만 실제 serving evidence를 작성한다.

## 마감 Git 구분

시작 시 두 Git 저장소는 clean이었다. 이번 unstaged/untracked 개발 변경은 위 목록과 라우팅/검증/인수인계 문서다. staged 변경을 만들지 않았고 커밋하지 않았다. ad_server는 시작·종료 모두 저장소가 없어 파일 hash 스냅샷으로 구분했다. 기존 events.py/ads.env/server/.env의 동일 hash를 확인해 이번 개발 변경과 분리했다.

## 후속 진단 · 게임 광고 요청 실패 화면

스크린샷의 서버 요청 실패 메시지를 기준으로 읽기 진단했다. 게임8000/광고8001 공개 endpoint는200, Mongo27017 PRIMARY, 캠페인2개/입찰2개로 확인됐다. 현재 게임 설정의 ADS_MEDIA_KEY configured=False였고 gateway를 같은 설정으로 검사하면 network 호출 전에 media_key_missing이 발생했다. 따라서 이미지 renderer 단계 이전의 매체 인증 설정 문제다. 키 실제 값/비밀번호/토큰을 출력하지 않았고, 캠페인·입찰·결정을 쓰거나 서버를 종료하지 않았다. source code 변경 없음. 이전 개발 변경이 이번 진단 시작 전에 이미 존재했고 두 저장소의 staged는 여전히 비어 있다. 키 전달은 사용자 승인 대기 상태다. 승인 후 게임 프로세스를 재시작하고15초 이후 새로 보기를 해야 한다.

## 후속 승인 · 매체 키 적용 완료

사용자가 “복사·저장 승인’을 선택”이라고 명시했다. 이전 자동 승인 거부 사유가 해소되어 실제 ADS_MEDIA_KEY를 ad_server/ads.env에서 Game-server/server/.env 같은 항목에 복사·저장했다. 이 후속 시작 시 이전 개발 변경은 이미 Git unstaged/untracked에 존재했고 이번 변경은 로컬 server/.env 한 항목, 해당 짝 문서/색인, 광고 README의 연결 상태와 인수인계·검증 기록뿐이다. 원본 파일 bytes 보존, 대상의 다른 key/value 파싱 결과 보존을 확인했다. 비밀값은 출력/문서/Git에 복사하지 않았다.

기존 서버는 --noreload로 실행 중이었다. settings.py touch는 파일 bytes/hash를 바꾸지 않았지만 실제 자동 재시작을 하지 못했다. PID15320이8000의 manage.py runserver --noreload임을 확인한 뒤 그 프로세스만 종료했다. 기존 가상환경으로 Game-server 루트에서 `server/manage.py runserver 127.0.0.1:8000 --noreload`를 숨김으로 재시작했다. 현재 listener PID20244이며 Mongo/광고 서버를 재시작하거나 변경하지 않았다. 재시작 로그는 Game-server/infra/runtime/ads-key-restart-20261007-112559.*.log다.

키 적용 후 새 settings 키 존재/광고 key 일치=True, Django check 문제 없음, live 광고 API의 인증 probe400, 새 게임 endpoint200을 확인했다. probe의 subject는 의도적으로 invalid여서 인증 후 choose_ad 전에 거부됐으며 결정/노출을 쓰지 않았다. 기존 학생 게임 창에서15초 후 새로 보기를 누르면 된다. 자동 WS 재연결이 완료되지 않으면 접속기에서 기존 게임 계정으로 다시 로그인한다. 학생 실제 화면 표시 성공을 확인하지 않았으므로 fixture 캡처를 실제 노출 증거로 기록하지 않는다.

추가 라우팅: Game-server/docs/server-routing/files/server/.env.md 및 server-routing/README.md. 설정 적용 검증 JSON: Game-server/docs/server-routing/verification/day22-media-key-apply.json. 대상은 Git ignore 파일이라 Git diff에 private 값이 나타나지 않는다. 처음 단계의 private_env_and_user_event_preserved 기록은 승인 전 시점이며 현재 .env에는 승인된 한 항목 변경이 있다.

최종 추가 읽기 검사: village-board 선택 가능 캠페인2개 중 PNG소재 선택1개, lobby-banner 선택 가능 캠페인0개였다. 재시작 직후 새 로그의 게임 광고 POST 상태 목록은 비어 있어 학생 새로 보기 이후의 실제 화면 성공은 아직 관찰하지 않았다. 로비 광고를 보려면 광고주 웹에서 별도 lobby-banner 캠페인과 입찰을 저장해야 한다. 접속기76짝 문서 검사와 두 Git diff --check는 계속 통과했고 staged 없음이다.
