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

첫 검사는 임시 Mongo27107의31개 테스트, 둘째는 Mongo27109·SQLite·웹18000/18001·무작위 임시 계정·synthetic 매체 키로 실제 HTTP 흐름과 Pygame 두 프레임/Chrome 화면을 검증한다. 둘째는 옆 폴더 두 프로젝트의 기존 가상환경과 Codex 번들 Playwright/설치된 Chrome을 사용한다. 테스트 프로세스만 종료하고 수업용27017·MySQL을 변경하지 않는다. 접속기 전체48개, 게임 서버 관련11개 테스트도 통과했다.

`docs/server-routing/verification/day22-images/integration.json`과 PNG 캡처는 분리 fixture의 증거다. 실제 학생 게임 창 관찰은 not_run이며 이 캡처를 실제 수업 노출 증거로 기록하지 않는다. 23일차 1~2교시의 노출·클릭 저장은 아래에 반영했다. 광고주 보고서·파일 전달·집계는 다음 교시 범위다. 작업 시작 전 `ads/events.py`의 실습 코드는 `tools/basics/day23_record_observed.py`에 원본 바이트로 보존했다.

기존 기초 명령은 `python tools/basics/day22_period01.py`, `python tools/basics/day22_period02.py`, `python tools/basics/day22_credit_model.py`다. 크레딧 예제는 로컬 모형이며 실정산이 아니다. 저장 결정은 chosen_campaign_id/chosen_bid_amount, 응답은 campaign_id/bid_amount이고 이미지 호환 응답에는 bid_units도 같은 금액으로 포함한다.

## 23일차 1~2교시 · 노출·클릭 저장

`ads/events.py`의 `record_ad_event(subject, decision_id, event_type)`는 해당 수신자의 선택된 결정을 검증하고 `ad_events`에 저장한다. ID는 `decision_id:impression` 또는 `decision_id:click`이며 `$setOnInsert`로 최초 내용만 유지한다. 재전송은 `created:false`로 성공을 확인한다. 클릭에는 기존 노출이 필요하고 광고주·금액·슬롯은 선택 당시 후보 snapshot에서 가져온다. event_time은 aware UTC 문자열이고 클릭의 impression_time은 최초 노출 시각이다.

고유 인덱스는 수업 DB에 적용했다. 다음 명령은 반복 실행해도 같은 인덱스를 유지한다. 기존 자료에 중복이 있어 실패하면 자동 삭제하지 않고 원인을 먼저 확인한다.

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python ad_config/manage.py ensure_ad_event_indexes
```

매체 POST `/api/media/events/`는 서버 매체 키를 검사한다. 게임 POST `/api/ads/events/`는 기존 로그인·CSRF를 사용하고 세션 User의 Player.pk를 수신자로 삼는다. 본문의 player_id·subject는 수신자를 바꾸지 않는다. 접속기는 기존 AuthSession에서 CSRF를 갱신하고 결정 ID·사건 종류만 전송한다.

Pygame의 PNG 표시와 flip이 성공한 활성 화면에서만 노출을 요청한다. API 보기·조회 패널·최소화·이미지 실패에는 새 표시 receipt가 없다. 노출 저장 응답 전 클릭은 기록하지 않는다. 광고 카드 영역의 실제 마우스 클릭 후 클릭을 요청하며 새로 보기 버튼은 클릭 실적으로 세지 않는다. 화면의 **노출 완료·클릭 완료**는 서버 저장 확인 상태다. 실패한 노출은 같은 광고를 표시할 때 2초 후 재시도하고, 실패한 클릭은 2초 후 다시 클릭한다. 저장 중 새 선택은 막고 새 광고·로그아웃 때 확인 상태를 초기화한다.

기존 접속기 창을 종료하고 아래 명령으로 다시 실행한다. 로그인 후 광고의 노출 완료를 확인하고 광고 이미지를 클릭한 뒤 클릭 완료를 확인한다. Compass에서 같은 27017의 `village_ads` → `ad_events`를 새로 고친다. 선택만 하면 `decisions`만 증가하며 광고주 웹 미리보기는 노출·클릭을 생성하지 않는다. 현재 로비 후보가 없다면 앞 절의 lobby-banner 캠페인·입찰을 직접 저장한다.

```powershell
Set-Location C:\MLO01-01\Chapter3\Game-client
.\.venv\Scripts\Activate.ps1
python client/main.py
```

기존 수동 실습 코드는 실제 화면에서 확인한 결정에만 사용한다. UUID 정렬은 시간순이 아니므로 번호만으로 최신 표시를 추측하지 않는다. 자동 접속기 저장과 함께 실행하면 같은 ID가 이미 있어 `created:false`가 나올 수 있다.

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server
python ad_config/manage.py shell -c "exec(open('tools/basics/day23_record_observed.py', encoding='utf-8').read())"
python tools/verify_day23.py --mongod "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe"
```

통합 검사는 별도 Mongo27109·SQLite·HTTP18000/18001에서 두 슬롯을 표시하고 모의 클릭하여 노출2·클릭2만 저장되는지, 재전송 및 현재 입찰 변경에도 snapshot이 유지되는지 확인한다. 증거는 `docs/server-routing/verification/day23-period02/`다. 이 검사는 실제 학생 클릭의 증거가 아니며 수업 사건을 만들지 않는다.
