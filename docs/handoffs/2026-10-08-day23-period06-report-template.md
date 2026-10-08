# 23일차 6교시 보고서 템플릿을 현재 광고주 화면에 연결

작업일: 2026-10-08. 요청은 "6교시 템플릿까지 지금 화면 구상에서 맞춰줘"다. 현재 광고 스튜디오의 크림색/초록색 공통 레이아웃에 보고서를 연결하고 상단에 일별 보고서 메뉴를 추가했다. 교안의 9개 출력 필드, CTR 0~1 표시, 원본 시각 문자열과 빈 목록 계약은 보존했다.

## 작업 시작 전 Git 상태

`C:/MLO01-01/Chapter3`: Git 상태 확인 불가: 저장소 아님. 작업 대상 `ad_server`의 Git 루트는 `C:/MLO01-01/Chapter3/ad_server`, 직전 커밋은 `9b0aaa1 day23-ad_sever 준비`다. staged 변경은 없었다.

기존 unstaged는 `ads/views.py`, `ads/urls.py` 수정과 `docs/server-routing/README.md` 삭제였다. 기존 untracked 개발 파일은 `ads/management/commands/build_ad_reports.py`, `ads/management/commands/load_ad_reports.py`, `ads/reporting.py`, `ads/templates/ads/reports.html`, `config/day23-period-06.py`였다. 그 밖에 앞선 5교시/DB 복구 인수인계·짝 문서·검증 폴더가 untracked로 존재했다. 전체 목록은 `../server-routing/verification/day23-period06-template/start.json`의 Git 기록을 따른다.

기존 코드와 문서 삭제는 작업 시작 전에 존재한 변경으로 취급했다. 해당 소스/문서 원본은 `before/`, `before-docs/`에 보존했다. 환경 파일은 내용 없이 해시만 기록했다. 기존 라우팅 README 삭제를 되돌리지 않았다.

## 먼저 수행한 사용자 코드 문서 정합화

현재 `report_view`와 게시 명령, 보고서 URL·기초 실습이 이미 작성되어 있었다. 추가 개발 전에 실제 AST 시그니처와 책임을 확인했고, `views.py`와 `urls.py` 짝 문서를 갱신했다. `load_ad_reports.py`, `config/day23-period-06.py`, `reports.html`의 짝 문서를 추가해 당시 구현을 먼저 등록했다. 해당 상태는 `user-code-documented/`와 `routing-user-code-documented.json`에 보존했다.

기존 검사기는 삭제된 `docs/server-routing/README.md`를 필수로 요구해 초기 CLI 검사에서 "routing directory is incomplete"를 보고했다. 이를 숨기거나 README를 복구하지 않았다. 같은 routing-doc-auditor의 `extract_symbols`/`mark_documented` AST API와 별도 `docs/server-routing/day23-period06-index.md`를 사용해 6개 Python 파일/15개 심볼, 총 9개 개발 파일 짝 문서/색인을 검증했다. 표준 CLI가 통과한 것으로 기록하지 않는다.

## 이번 개발 변경

- `ads/templates/ads/reports.html`: 독립 HTML에서 기존 `ads/base.html` 상속으로 연결. 제목·설명·9열 표를 기존 카드 디자인으로 감쌌고 오류 알림, 빈 행, 가로 스크롤 영역과 접근성 속성을 적용했다. 필드 순서와 `row.ctr|floatformat:3`을 보존했다.
- `ads/templates/ads/base.html`: 로그인 메뉴에 `ads:web-reports` 일별 보고서 링크 추가. 보고서 페이지에서 `aria-current="page"`를 표시한다. 기존 계정 표시·로그아웃 POST/CSRF·정적 리소스·footer는 보존했다.
- `ads/static/ads/advertiser.css`: 기존 파일 바이트를 유지하고 보고서 표·현재 메뉴·작은 화면 메뉴 줄바꿈 스타일을 끝에 추가했다.

개발 파일 추가·이동·삭제는 없다. 사용자 코드인 views/URL/집계 모듈/두 관리 명령/기초 실습은 시작 해시와 동일하다. 그 기존 변경을 이번 에이전트 구현으로 주장하지 않는다. 실제 수정 파일은 위 3개뿐이다.

## 설계 결정과 교안 대응

정본은 바탕화면의 「현재 ad_server에서 노출·클릭과 광고주 보고서 완성하기.html」 6교시다. 기존 report_view 함수와 load 명령은 정본 AST와 일치했다. 기존 reports.html도 정본 HTML과 같았다. 이번 사용자의 화면 맞춤 요청에 따라 HTML 외형/공통 레이아웃만 적용했고 업무 계약은 그대로다.

교안의 `ads/web_views.py`는 현재 프로젝트의 combined `ads/views.py`에서 `report_view`로 이미 구현돼 있었다. 새 web_views 파일을 만들거나 로직을 옮기지 않았다. `ads:web-reports` → `views.report_view` → `reporting.list_reports(request.user.pk)` → template 경계를 유지한다. 템플릿은 계산/게시/DB 접속을 하지 않는다.

표는 서울 날짜·캠페인·슬롯·노출·클릭·CTR 0~1·모의 포인트 합·원본 마지막 시각·보고서 생성 시각의 9개 열이다. CTR을 백분율로 바꾸거나 모의 포인트를 청구액으로 적지 않는다. 두 시각 문자열을 자동으로 서울 시각으로 바꾸지 않는다. `rows|length`는 표시된 보고서 행 수이며 추가 실적 집계는 없다.

서버 실행/종료는 사용자가 VS Code PowerShell에서 수행한다는 선호를 따랐다. 에이전트는 MongoDB·Django·검증용 HTTP 서버를 시작/종료하지 않았고 실제 DB에 보고서를 게시하지 않았다.

## 최종 라우팅 문서와 색인

검증 후 별도 문서 정합화 단계에서 변경한 reports.html, base.html, advertiser.css의 짝 문서를 최종 코드 기준으로 갱신했다. views.py/urls.py와 신규 사용자 코드의 짝 문서도 확인했다. 별도 색인 `docs/server-routing/day23-period06-index.md`에 총 9개 소스와 짝 문서, 본 인수인계 및 검사 근거를 등록했다.

기존 `docs/server-routing/README.md` 삭제는 최종 Git에서도 유지했다. 범위 밖 문서를 일괄 재생성하지 않았다. 최종 AST/짝 문서/색인 검사는 `routing-final-scoped.json`에 있다.

## 검사 명령과 결과

실제 Python은 `ad_server/.venv/Scripts/python.exe -X utf8 -B`를 사용했다.

```powershell
python ad_config/manage.py check
python ad_config/manage.py load_ad_reports --help
python config/day23-period-06.py
```

모두 종료 코드 0이다. Django system check는 문제 0개, 관리 명령은 정상 사용법 출력, 초급 예제는 `1` 출력이다. help 확인은 게시 명령 실행이 아니다.

RequestFactory와 mock rows로 정상 HTML, 9개 헤더/필드/행당 셀, CTR 소수점 세 자리, ISO 시각 보존, 자동 escape, 빈 목록, DB 오류 503/알림, 미로그인 로그인 이동, POST 405, 로그인 사용자 pk 전달을 검증했다. 실제 MongoDB나 계정/세션 DB를 쓰지 않은 fixture 검사다. 초기 테스트 기본 host `testserver`가 기존 ALLOWED_HOSTS에서 거절되어 fixture host만 `127.0.0.1`로 수정했다. 설정 파일은 변경하지 않았다. 결과는 `functional-checks.json`에 있다.

기존 로그인 브라우저의 실제 `http://127.0.0.1:8001/advertiser/reports/`에서 게시된 3개 행과 현재 템플릿을 확인했다. 기본 viewport 1280×720에서 페이지 가로 넘침이 없고 9개 열이 표시됐다. 390×844에서 페이지 client/scroll 폭은 모두 375px, 표만 295px/1000px로 가로 스크롤되며 메뉴 링크가 페이지 폭 안에 들어갔다. 스크린샷을 도구 화면에서 관찰했고 검사 수치는 `visual-checks.json`에 기록했다. 임시 viewport는 복원했고 보고서 탭을 결과로 유지했다.

로컬 fixture HTML은 CSRF input/실제 토큰을 제거하고 CSS만 내장한 검증용 샘플이다. 브라우저의 file: 프로토콜 정책 때문에 이 샘플 파일의 브라우저 열기가 거절됐다. 우회하지 않았으며 사용자가 이미 실행 중인 실제 HTTP 보고서 화면으로 확인했다. 샘플 HTML을 실제 게시 결과로 취급하지 않는다.

## 남은 범위와 사용자 다음 확인

실제 load 명령은 사용자가 수행하는 단계이고, 다른 광고주 계정으로 직접 로그인해 보는 교안 관찰은 이번 작업에서 실행하지 않았다. 화면은 현재 로그인 상태의 보고서 3건을 읽었다. 소유자 필터 계약은 기존 코드와 mock 호출 인수로 검증했으며 다른 계정 GUI 관찰을 했다고 기록하지 않는다.

광고 서버가 실행 중이면 [일별 보고서](http://127.0.0.1:8001/advertiser/reports/)를 새로고침한다. 새 보고서 후보를 게시해야 할 때만 사용자 터미널에서 아래 명령을 실행한다.

```powershell
cd C:\MLO01-01\Chapter3\ad_server
python ad_config/manage.py load_ad_reports --source data/exports/ad-reports-day23.ndjson
```

서버가 종료돼 있다면 사용자 VS Code 터미널에서 기존 MongoDB 명령과 별도 광고 서버 `python ad_config/manage.py runserver 127.0.0.1:8001`을 실행한다. 실행 중인 서버를 중복 시작하지 않는다.

최종 Git 비교와 변경 구분은 `finish.json`을 따른다. 기존 사용자 변경·README 삭제·환경 파일을 보존했고 staging·commit을 수행하지 않았다.
