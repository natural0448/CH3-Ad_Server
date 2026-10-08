# 광고 서버 현재 진행 라우팅 색인

2026-10-08의 저장된 구현을 기준으로 한다. `docs/server-routing/README.md`는 현재 HEAD `8f541e4 day23 - finish`에도 없으므로 복원하지 않고 이 색인을 사용한다. 1:1 짝 문서는 `files/<소스 상대경로>.md`다. 아래 경로는 현재 존재하는 코드/문서이며 계획 파일을 현재 구조에 넣지 않는다.

22일차 광고주 인증·캠페인 디자인/준비된 PNG·입찰·매체 광고 선택과 23일차 선택 snapshot·노출/클릭·광고주 실적 화면이 구현돼 있다. URL은 루트 `ad_config/ad_config/urls.py`의 include에서 `ads/urls.py`로 연결하고 view는 기존 `ads/views.py`에 통합돼 있다. `ad_config/manage.py` 경로를 유지한다.

23일차 4교시의 `export_ad_events` → `ads.exporting.export_ad_events`는 `ad-event/v1` 공개 사건을 노출 기준 시각의 범위로 파일에 저장한다. 5교시 `build_ad_reports` → `read_ndjson` → `build_daily_reports` → `write_ndjson`은 서울 노출일 보고서 후보 파일을 만든다. 6교시 `load_ad_reports` → `publish_reports`는 업무 키별 게시이며 다른 날짜 행을 지우지 않는다. `ads:web-reports` → `views.report_view` → `reporting.list_reports(request.user.pk)` → `ads/reports.html`은 자기 보고서 9개 열을 표시한다. 공통 base 메뉴에 일별 보고서가 연결돼 있다.

7교시 `deliver_ad_events` → `ads.delivery.deliver_events`는 한 writer의 로컬 사건 파일을 완성한 다음 `file_delivered_at` 표식을 저장한다. 8교시 `check_ad_reports`는 전체 보관 사건으로 계산한 후보와 게시된 전체 보고서를 읽어 대조하고 결과 JSON을 저장한다. 해당 소스의 존재와 이번 문서 검증은 실제 전달/게시 재실행 성공을 뜻하지 않는다. Spark 광고 작업은 코드의 결과 메타데이터에서 `not-configured`, GUI 관찰은 `separate-manual-observation`다. `ads.delivery` import 시 모듈 하단 실습 print가 출력되는 현재 부수효과는 짝 문서에 기록했다.

24일차 광고에는 공식 검사기 `tools/check_day24_logic.py`와 작성 중인 2교시 `ads/snapshot_intake.py`가 저장돼 있다. 문서 정합화 도중 관찰한 새 사용자 작업 또는 작성자를 확정할 수 없는 작업이다. 최신 inspect에는 필드/공개 상태/중복/수집값 통일 검사가 있으나 `parse_utc` 이름 식만 있어 captured_at 시각 검사는 호출되지 않는다. snapshot 검증/소비 성공으로 기록하지 않으며 3~8교시 후속 소비 구현과 관리명령은 미적용이다. Player snapshot 명령은 `../Game-server/server/game/management/commands/export_player_snapshot.py`에 있고 광고 입력 경로는 `../Game-server/data/exports/player-cdc.ndjson`이다. 게임 ORM을 광고 앱에 import하지 않는다. 기존 부재/빈칸 근거는 관찰 당시 시점자료로 보존하며 최신 소스 상태는 [사용자 저장 중 관찰](verification/day24-routing-sync/concurrent-source-observation.json)을 따른다. `Game-server/data`가 기존 출력 위치다.

2교시 완료 여부의 공식 격리 재검토는 **20 통과·2 실패**다. 수집 시각 검사 미호출과 `inspect_player_snapshot.py` 관리명령 부재가 실패 원인이다. [검사 결과](verification/day24-period02-review/official-period02-final.json), [검토 인수인계](../handoffs/2026-10-08-day24-period02-review.md)를 따른다. 소스를 고치거나 원본 파일을 다시 만들지 않았다.

`config/day23-*.py`와 `tools/basics/*`는 독립 실습/교안 참고 코드다. 서버 runtime 구현과 구분한다. 초기 package/scaffold 문서는 현재 정의가 없음을 명시한다. 검증용 도구의 존재도 최근 기능 테스트 실행을 뜻하지 않는다.

## Python 파일과 1:1 문서

| 현재 소스 | 짝 문서 | 책임/상태 |
|---|---|---|
| `ad_config/ad_config/__init__.py` | [문서](files/ad_config/ad_config/__init__.py.md) | 현재 Python package 초기화; 짝 문서의 정의 여부 참조 |
| `ad_config/ad_config/asgi.py` | [문서](files/ad_config/ad_config/asgi.py.md) | 현재 Django 서버 application 진입점 |
| `ad_config/ad_config/settings.py` | [문서](files/ad_config/ad_config/settings.py.md) | Django/광고/Mongo 환경 설정; 값은 설정 소유 |
| `ad_config/ad_config/urls.py` | [문서](files/ad_config/ad_config/urls.py.md) | 인증·admin·광고 include 루트 URL |
| `ad_config/ad_config/wsgi.py` | [문서](files/ad_config/ad_config/wsgi.py.md) | 현재 Django 서버 application 진입점 |
| `ad_config/ads_manage.py` | [문서](files/ad_config/ads_manage.py.md) | 루트 ads 검색 경로를 더하는 기존 명령 진입점 |
| `ad_config/manage.py` | [문서](files/ad_config/manage.py.md) | 기존 Django 명령 진입점 |
| `ads/__init__.py` | [문서](files/ads/__init__.py.md) | 현재 Python package 초기화; 짝 문서의 정의 여부 참조 |
| `ads/admin.py` | [문서](files/ads/admin.py.md) | 현재 Django scaffold/앱 설정; 광고 ORM 모델 없음 |
| `ads/apps.py` | [문서](files/ads/apps.py.md) | 현재 Django scaffold/앱 설정; 광고 ORM 모델 없음 |
| `ads/auth_views.py` | [문서](files/ads/auth_views.py.md) | 광고주 JSON CSRF/session 로그인·로그아웃 |
| `ads/creatives.py` | [문서](files/ads/creatives.py.md) | 준비된 PNG 선택·검증 |
| `ads/delivery.py` | [문서](files/ads/delivery.py.md) | 한 writer 파일 전달·전달 표식·실습 print |
| `ads/events.py` | [문서](files/ads/events.py.md) | 선행 노출/수신자·결정 검증과 최초 사건 저장 |
| `ads/exporting.py` | [문서](files/ads/exporting.py.md) | 공개 사건 NDJSON; 노출 기준 시각 범위 |
| `ads/management/__init__.py` | [문서](files/ads/management/__init__.py.md) | 현재 Python package 초기화; 짝 문서의 정의 여부 참조 |
| `ads/management/commands/__init__.py` | [문서](files/ads/management/commands/__init__.py.md) | 현재 Python package 초기화; 짝 문서의 정의 여부 참조 |
| `ads/management/commands/build_ad_reports.py` | [문서](files/ads/management/commands/build_ad_reports.py.md) | 고정 사건 파일 → 후보 파일; 게시 없음 |
| `ads/management/commands/check_ad_reports.py` | [문서](files/ads/management/commands/check_ad_reports.py.md) | 전체 입력 후보와 게시 행 읽기 대조·결과 파일 |
| `ads/management/commands/compare_ad_decisions.py` | [문서](files/ads/management/commands/compare_ad_decisions.py.md) | 저장된 두 결정 snapshot 조회 |
| `ads/management/commands/create_ad_indexes.py` | [문서](files/ads/management/commands/create_ad_indexes.py.md) | 현재 고유 사건 색인 명령 |
| `ads/management/commands/deliver_ad_events.py` | [문서](files/ads/management/commands/deliver_ad_events.py.md) | 파일 전달·DB 표식 쓰기 진입점 |
| `ads/management/commands/ensure_ad_event_indexes.py` | [문서](files/ads/management/commands/ensure_ad_event_indexes.py.md) | 기존 고유 사건 색인 명령 보존 |
| `ads/management/commands/export_ad_events.py` | [문서](files/ads/management/commands/export_ad_events.py.md) | 공개 사건 파일 내보내기 |
| `ads/management/commands/load_ad_reports.py` | [문서](files/ads/management/commands/load_ad_reports.py.md) | 후보 파일 → 업무 키별 DB 게시 |
| `ads/media_auth.py` | [문서](files/ads/media_auth.py.md) | 두 매체 헤더·공개 subject 인증 decorator |
| `ads/migrations/__init__.py` | [문서](files/ads/migrations/__init__.py.md) | 현재 Python package 초기화; 짝 문서의 정의 여부 참조 |
| `ads/models.py` | [문서](files/ads/models.py.md) | 현재 Django scaffold/앱 설정; 광고 ORM 모델 없음 |
| `ads/mongo.py` | [문서](files/ads/mongo.py.md) | 공유 지연 Mongo 연결 |
| `ads/reporting.py` | [문서](files/ads/reporting.py.md) | 노출일 후보 집계·업무 키 게시·소유자 조회 |
| `ads/repository.py` | [문서](files/ads/repository.py.md) | 소유자 캠페인과 현재 입찰 저장·조회 |
| `ads/services.py` | [문서](files/ads/services.py.md) | 선택 당시 후보·승자·소재 snapshot |
| `ads/snapshot_intake.py` | [문서](files/ads/snapshot_intake.py.md) | 24일차 2교시 작성 중; captured_at 시각 검사 미호출·소비 성공 아님 |
| `ads/test_events.py` | [문서](files/ads/test_events.py.md) | 기존 검증/회귀검사 도구; 실행 이력 별도 |
| `ads/tests.py` | [문서](files/ads/tests.py.md) | 기존 검증/회귀검사 도구; 실행 이력 별도 |
| `ads/timestamps.py` | [문서](files/ads/timestamps.py.md) | 시간대 포함 ISO 시각의 UTC 정규화 |
| `ads/urls.py` | [문서](files/ads/urls.py.md) | 광고주 웹/매체 API 6개 URL |
| `ads/views.py` | [문서](files/ads/views.py.md) | 캠페인·입찰·매체 API·실적·보고서 통합 view |
| `config/day23-period-01.py` | [문서](files/config/day23-period-01.py.md) | 23일차 독립 기초 실습/교안 참고; runtime import 없음 |
| `config/day23-period-02.py` | [문서](files/config/day23-period-02.py.md) | 23일차 독립 기초 실습/교안 참고; runtime import 없음 |
| `config/day23-period-03.py` | [문서](files/config/day23-period-03.py.md) | 이전 False/True 실습; 최신 3교시 정본과 구분 |
| `config/day23-period-04.py` | [문서](files/config/day23-period-04.py.md) | 23일차 독립 기초 실습/교안 참고; runtime import 없음 |
| `config/day23-period-05.py` | [문서](files/config/day23-period-05.py.md) | 23일차 독립 기초 실습/교안 참고; runtime import 없음 |
| `config/day23-period-06.py` | [문서](files/config/day23-period-06.py.md) | 23일차 독립 기초 실습/교안 참고; runtime import 없음 |
| `config/day23-period-07.py` | [문서](files/config/day23-period-07.py.md) | 23일차 독립 기초 실습/교안 참고; runtime import 없음 |
| `config/day23-subject.py` | [문서](files/config/day23-subject.py.md) | 23일차 독립 기초 실습/교안 참고; runtime import 없음 |
| `tools/basics/day22_credit_model.py` | [문서](files/tools/basics/day22_credit_model.py.md) | 독립 기초 실습/보존 자료; runtime 분리 |
| `tools/basics/day22_period01.py` | [문서](files/tools/basics/day22_period01.py.md) | 독립 기초 실습/보존 자료; runtime 분리 |
| `tools/basics/day22_period02.py` | [문서](files/tools/basics/day22_period02.py.md) | 독립 기초 실습/보존 자료; runtime 분리 |
| `tools/basics/day23_record_observed.py` | [문서](files/tools/basics/day23_record_observed.py.md) | 독립 기초 실습/보존 자료; runtime 분리 |
| `tools/check_day24_logic.py` | [문서](files/tools/check_day24_logic.py.md) | 24일차 공식 검사기 준비; 소비 구현 없음 |
| `tools/day22_connection.py` | [문서](files/tools/day22_connection.py.md) | 22일차 Mongo 연결 실습 |
| `tools/day22_crud.py` | [문서](files/tools/day22_crud.py.md) | 22일차 캠페인·입찰 CRUD 실습 |
| `tools/verify_day22.py` | [문서](files/tools/verify_day22.py.md) | 기존 검증/회귀검사 도구; 실행 이력 별도 |
| `tools/verify_day22_images.py` | [문서](files/tools/verify_day22_images.py.md) | 기존 검증/회귀검사 도구; 실행 이력 별도 |
| `tools/verify_day23.py` | [문서](files/tools/verify_day23.py.md) | 기존 검증/회귀검사 도구; 실행 이력 별도 |
| `tools/verify_lesson_alignment.py` | [문서](files/tools/verify_lesson_alignment.py.md) | 기존 검증/회귀검사 도구; 실행 이력 별도 |

## 화면·정적 자산·안내의 짝 문서

| 현재 파일 | 짝 문서 |
|---|---|
| README.md | [문서](files/README.md.md) |
| ads/templates/registration/login.html | [문서](files/ads/templates/registration/login.html.md) |
| ads/templates/ads/base.html | [문서](files/ads/templates/ads/base.html.md) |
| ads/templates/ads/campaigns.html | [문서](files/ads/templates/ads/campaigns.html.md) |
| ads/templates/ads/bids.html | [문서](files/ads/templates/ads/bids.html.md) |
| ads/templates/ads/events.html | [문서](files/ads/templates/ads/events.html.md) |
| ads/templates/ads/reports.html | [문서](files/ads/templates/ads/reports.html.md) |
| ads/static/ads/advertiser.css | [문서](files/ads/static/ads/advertiser.css.md) |
| ads/static/ads/advertiser.js | [문서](files/ads/static/ads/advertiser.js.md) |
| ads/static/ads/creatives/forest-tools.png | [문서](files/ads/static/ads/creatives/forest-tools.png.md) |
| ads/static/ads/creatives/camp-tea.png | [문서](files/ads/static/ads/creatives/camp-tea.png.md) |

## 검증과 이전 기록

이번 범위의 스킬 AST API 검사 결과는 [최종 구조 검사](verification/day24-routing-sync/agent-routing-final.json), [문서 경로 검사](verification/day24-routing-sync/agent-document-checks.json), [snapshot 파일 경계의 앞선 관찰](verification/day24-routing-sync/agent-snapshot-boundary.json), [인수인계](../handoffs/2026-10-08-ad-routing-progress-sync.md)를 따른다. 새 사용자 소스를 포함한 전체 Git 추적/미추적 Python 57파일·153심볼을 이 색인과 짝 문서에 대조했다. 표준 CLI는 기존 라우팅 README를 필수로 요구하는 제한으로 종료 코드 2이며 그 사실을 별도 결과에 보존한다. API 성공은 짝 문서/구조의 일치이며 문제틀의 기능 검사 통과를 뜻하지 않는다. API 성공을 CLI 성공으로 기록하지 않는다.

이전 작업의 [23일차 6교시 색인](day23-period06-index.md), [24일차 1교시 색인](day24-period01-index.md), [보고서 UI 인수인계](../handoffs/2026-10-08-day23-period06-report-template.md), [snapshot 검토 인수인계](../handoffs/2026-10-08-day24-period01-review.md), [출력 경로 정정 인수인계](../handoffs/2026-10-08-day24-data-path-correction.md)는 당시 근거다. 과거 실패/검토/제안을 현재 구현 상태로 바꾸지 않고 원래 기록을 보존한다.
