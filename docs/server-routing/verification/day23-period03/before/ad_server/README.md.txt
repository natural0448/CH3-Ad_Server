# 22~23일차 광고 집행

22일차 수정 교안과 원본 교안의 PNG 소재 흐름을 현재 폴더 구조에 반영했다. 광고주가 숲 도구점·모닥불 찻집 소재를 골라 미리보고 저장하며, 입찰 결과의 이미지·문구·금액·결정 ID가 게임 서버와 기존 Pygame 접속기로 전달된다. 기존 문구 광고와 계정·캠페인 데이터는 유지한다.

## 광고 서버

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python ad_config/manage.py check
python ad_config/manage.py runserver 127.0.0.1:8001
```

루트 주소는 로그인으로 이동한다. 로그인은 기존 광고 서버 계정을 사용하며 계정이 없는 경우에만 본인이 `python ad_config/manage.py createsuperuser`를 실행한다. 초기 계정 테이블이 없는 경우에만 `python ad_config/manage.py migrate`가 필요하다. 비밀번호를 자동 변경하지 않는다.

- [광고주 로그인](http://127.0.0.1:8001/accounts/login/)
- [캠페인 디자인·저장](http://127.0.0.1:8001/advertiser/campaigns/)
- [입찰 관리](http://127.0.0.1:8001/advertiser/bids/)
- 매체 API: POST `/api/media/decision/`

`ads.env`를 먼저, 루트 `.env`가 있으면 그 값으로 덮어 읽는다. 필수 설정은 ADS_SECRET_KEY, ADS_MEDIA_KEY, MONGO_URI이며 MONGO_DB 기본은 village_ads다. 실제 키 값은 문서에 없다. 현재 수업 환경은 27017 단일 멤버 ads-rs다. 이미 PRIMARY인 서버에 replSetInitiate를 반복하거나 기존 서비스를 중복 실행하지 않는다. 중지 상태일 때만 별도 터미널에서 실행한다.

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server
& "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe" --config config/mongo-node1.yml
```

Compass도 같은 27017 인스턴스에 접속해야 한다. DB는 `village_ads`이며 광고주 웹에서 캠페인을 실제 저장하면 `campaigns`, 입찰 저장 후 `bids`, 선택 요청 후 `decisions`가 만들어진다. 로그인·조회만으로 컬렉션은 생성되지 않는다.

## 수업 순서

1. 캠페인 화면에서 forest-tools를 제목 숲 도구점, 소재 숲 도구점, 위치 마을 게시판, 활성 상태로 저장한다.
2. camp-tea도 모닥불 찻집 소재와 같은 마을 게시판으로 저장한다. 각 광고는 문구를 입력할 수 있고 이미지 광고는 빈 문구도 허용한다.
3. 입찰 관리에서 forest-tools 10, camp-tea 20을 저장한다. 게임의 다음 선택은 camp-tea다.
4. forest-tools 입찰을30으로 바꾸고 15초 후 게임의 새로 보기 버튼을 누르면 forest-tools로 바뀐다. 예전 결정은 찻집 snapshot으로 남는다.
5. 로비는 별도 캠페인 ID(예: lobby-tea), 모닥불 찻집 이미지, lobby-banner 위치, 입찰18로 저장한다.

소재 경로는 `/static/ads/creatives/forest-tools.png`와 `/static/ads/creatives/camp-tea.png`다. 기존 Kenney Tiny Dungeon CC0 원본 망치·컵 PNG를 사용하며 라이선스/원본 경로는 `data/evidence/asset-sources.md`에 있다. 외부 이미지 URL은 입력받지 않는다.

## 게임 연결

Game-server의 `config/settings.py`는 ADS_BASE_URL(기본 http://127.0.0.1:8001), ADS_MEDIA_ID(기본 village-game), ADS_MEDIA_KEY를 읽는다. 매체 키는 광고 서버와 일치해야 한다. 수업 키는 사용자 명시 승인 후 `Game-server/server/.env`의 ADS_MEDIA_KEY 항목에 복사·저장했다. 광고 서버와 키 일치를 확인하고 게임 개발 서버를 재시작했다. 다른 기존 DB·게임 설정과 원본 ads.env는 보존했다.

```powershell
Set-Location C:\MLO01-01\Chapter3\Game-server
.\server\.venv\Scripts\Activate.ps1
python server/manage.py runserver 127.0.0.1:8000
```

게임 계정으로 [게임 서버 로그인](http://127.0.0.1:8000/accounts/login/) 후 [광고 미리보기](http://127.0.0.1:8000/ads/preview/)를 확인한다. 게임 서버는 session User에 연결된 Player.pk로 subject를 만들며 요청의 player_id는 사용하지 않는다. POST `/api/ads/decision/`은 기존 session과 CSRF를 사용한다. PNG는 같은 게임 서버 origin의 static 경로에서 제공한다.

```powershell
Set-Location C:\MLO01-01\Chapter3\Game-client
.\.venv\Scripts\Activate.ps1
python client/main.py
```

현재 접속기는 로그인하고 최초 WS 상태를 받은 뒤 두 슬롯을 자동 요청한다. 새로 보기 버튼은 슬롯별15초 이후 가능하다. 이미지 decode 실패는 실패 문구를 표시하고 표시 성공으로 취급하지 않는다. 매체 키는 접속기·브라우저·광고 응답에 넣지 않는다. 서버 설정 변경 후 기존 프로세스를 재시작해야 한다.

## 검증과 증거

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python tools/verify_day22.py --mongod "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe"
python tools/verify_day22_images.py --mongod "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe"
```

첫 검사는 임시 Mongo27107의31개 테스트, 둘째는 Mongo27109·SQLite·웹18000/18001·무작위 임시 계정·synthetic 매체 키로 실제 HTTP 흐름과 Pygame 두 프레임/Chrome 화면을 검증한다. 둘째는 옆 폴더 두 프로젝트의 기존 가상환경과 Codex 번들 Playwright/설치된 Chrome을 사용한다. 테스트 프로세스만 종료하고 수업용27017·MySQL을 변경하지 않는다. 접속기 전체50개, 게임 서버 관련11개 테스트도 통과했다.

`docs/server-routing/verification/day22-images/integration.json`과 PNG 캡처는 분리 fixture의 증거다. 실제 학생 게임 창 관찰은 not_run이며 이 캡처를 실제 수업 노출 증거로 기록하지 않는다. 수정된 23일차 1·2교시의 결정 보완·실적 API·확인 화면은 아래에 반영했다. 광고주 보고서·파일 전달·집계는 다음 교시 범위다. 작업 시작 전 `ads/events.py`의 실습 코드는 `tools/basics/day23_record_observed.py`에 원본 바이트로 보존했다.

기존 기초 명령은 `python tools/basics/day22_period01.py`, `python tools/basics/day22_period02.py`, `python tools/basics/day22_credit_model.py`다. 크레딧 예제는 로컬 모형이며 실정산이 아니다. 저장 결정은 chosen_campaign_id/chosen_bid_amount, 응답은 campaign_id/bid_amount이고 이미지 호환 응답에는 bid_units도 같은 금액으로 포함한다.

## 수정 23일차 v2.3 · 1·2교시

정본은 데스크톱의 「현재 ad_server에서 노출·클릭과 광고주 보고서 완성하기.html」이다. 이전 「기존 접속기 노출·클릭에서 광고주 웹 보고서까지」와 교시 구성이 다르다. 1교시는 입찰 반환·결정 스냅샷·색인, 2교시는 기존 인증을 이용한 사건 API와 광고주 선택·실적 목록이다. 자동 Pygame 전송은 수정 교안의 3교시이며 기존에 작성된 구현을 보존했다. NDJSON·집계·일별 보고서·전달은 미적용 후속 교시다.

1교시에서 `save_bid`는 저장한 `bids` 문서를 반환한다. 새 결정에는 `owner_user_id`, UTC BSON datetime `selected_at`, `chosen_campaign_id`, `chosen_bid_amount`, 후보의 `owner_user_id`·`bid_amount`가 저장된다. 기존 4인수 `choose_ad(media_id, subject_id, slot_id, context)`·`bid_amount` 저장 형식·이미지·슬롯을 유지한다. 이미지 응답의 `bid_units`는 같은 금액의 호환 이름이며 `policy_version`은 선택·빈 응답에 같은 이름으로 들어간다. 현재 입찰 변경은 과거 결정이나 사건의 금액을 수정하지 않는다.

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python config/day23-subject.py
python config/day23-period-01.py
python config/day23-period-02.py
python ad_config/manage.py create_ad_indexes
```

세 기초 파일은 교안 코드 그대로이며 DB를 호출하지 않는다. 예상 출력은 중첩 사전·7, `40 30`, `sample-decision:impression`·`sample-decision:click`이다. 색인 명령의 출력은 `decision_event_once`이며 반복 실행해도 기존 고유 색인을 유지한다. 기존 `ensure_ad_event_indexes` 명령도 보존했다.

2교시의 `ads/events.py`는 `clean_subject`를 통해 공개 수신자를 검사하고 점 표기 필터로 결정의 두 식별자를 비교한다. 선택된 후보 스냅샷에서 소유자·금액·슬롯을 읽으며 과거 문서의 누락을 현재 입찰로 채우지 않는다. 노출 ID는 `decision_id:impression`, 클릭 ID는 `decision_id:click`이다. 클릭은 선행 노출이 있어야 저장하고 `$setOnInsert`로 최초 사건을 유지한다. 재전송의 `created:false`는 성공이다. JSON의 비문자열 사건 종류는 입력 오류로 거절하는 타입 검사만 교안에 추가했다.

매체 POST `/api/media/events/`와 기존 decision 경로는 `X-Media-ID`·`X-Media-Key` 두 헤더를 기존 서버 설정으로 인증한다. 헤더 누락·불일치는401, 결정·수신자 불일치나 스냅샷 누락은 구체적 공개 오류 코드와400, 저장소 장애는503이다. 게임 POST `/api/ads/events/`는 기존 로그인·CSRF를 사용하고 로그인한 Player에서 subject를 만든다. 본문은 `decision_id`·`event_type` 두 필드만 허용한다. 사건 응답에는 `Cache-Control: no-store`가 설정된다.

광고주 웹 [선택·실적](http://127.0.0.1:8001/advertiser/events/)에서 기존 광고 계정으로 로그인한다. 자기 소유 결정만 `selected_at` 내림차순으로 최대30개 조회하여 캠페인·선택 당시 포인트·결정 ID·선택 시각·스냅샷·노출/클릭 시각을 표시한다. 선택만 있어도 행이 보이며 사건이 없으면 **미기록**이다. 웹 조회는 사건을 저장하지 않는다. 기존 캠페인/입찰 디자인에 선택·실적 메뉴를 추가했다. 아직 구현하지 않은 일별 보고서 링크는 연결하지 않았다.

표가 비어 있으면 기존 결정에 `owner_user_id`가 없는지, 현재 광고주의 캠페인이 승자인지 확인하고 게임에서 새 광고를 요청한다. 기존 과거 문서는 수정하지 않는다. Compass는 기존27017의 `village_ads` → `decisions`에서 Sort `{"selected_at": -1}`로 새 문서를 확인한다. UUID `_id`의 역순은 시간순이 아니다. 광고주 계정 ID와 게임 Player ID는 같을 필요가 없다. Django shell에서 subject·결정 ID를 직접 만들어 사건을 기록하는 과거 실습 파일은 보존 자료이며 수정 교안의 실행 과정으로 사용하지 않는다.

| 교안 위치 | 현재 구조의 적용 파일 |
|---|---|
| repository.save_bid_document 반환 수정 | `ads/repository.py.save_bid` · 기존 함수/필드명 보존 |
| 3인수 choose_ad의 저장부 | `ads/services.py`의 기존4인수 choose_ad에 소유자·selected_at 추가 |
| ads/events.py 전체 코드 | `ads/events.py`, helper는 `ads/services.py.clean_subject` |
| views.py의 event | 기존 `ads/views.py.event_view` · 같은 media API 이름 보존 |
| ads/web_views.py.event_view | 기존 combined `ads/views.py.advertiser_event_view` · 매체 함수와 이름 충돌 방지 |
| ads/media_urls.py events/ | 기존 루트 include 구조의 `ads/urls.py`에 api/media/events/ 유지 |
| game/ad_events.py | 기존 `Game-server/server/game/ad_views.py.ad_event` · game/urls.py의 기존 경로 사용 |
| game/ad_gateway.py call_ads diff | 기존 별도 request_ad_event HTTPError 처리·두 헤더에 적용 |
| ads/templates/ads/events.html | 교안 표·빈 상태 그대로, 기존 base 스타일/메뉴 사용 |

22일차 정본은 「22일차 · 광고 플랫폼이 광고주의 광고를 게임 유저에게 집행한다.html」이다. `tools/day22_connection.py`·`tools/day22_crud.py`는 기존 ads.env/root .env·village_ads 환경에 적응한 교안 코드다. 기존 basics 실행 파일은 정본 파일을 호출하며 정산 모형은 main 진입점에서 교안 입력·처리·출력을 실행한다. 현재 인증·계정·이미지 경로는 유지한다.

```powershell
python tools/verify_lesson_alignment.py
python tools/verify_day22.py --mongod "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe"
python tools/verify_day23.py --mongod "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe"
```

원본 HTML과 AST/실습/실적 표의23개 대조, 광고37개·게임13개·접속기50개 테스트가 통과했다. 분리된 MongoDB·SQLite·HTTP·SDL dummy 환경의 기존 Pygame 표시/모의 클릭 회귀검사도 통과했다. `verify_day23.py`의 이전 이름/증거 경로 day23-period02는 유지하지만 자동 전송 검사는 수정 교안의3교시에 해당하는 기존 기능의 회귀검사다. 실제 학생 창 관찰은 not_run이며 fixture를 실제 수업 사건 증거로 주장하지 않는다. 테스트는 수업 데이터에 사건이나 캠페인을 추가하지 않았다. 근거는 `docs/server-routing/verification/lesson-alignment/`와 인수인계 문서에 있다.
