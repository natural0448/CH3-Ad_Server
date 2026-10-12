# 광고 서버 현재 진행 라우팅 색인

2026-10-12 현재 저장된 구현을 기준으로 한다. docs/server-routing/README.md는 현재 HEAD 5d29085 day24 - 2교시에도 없으므로 복원하지 않고 이 색인을 사용한다. 1:1 짝 문서는 files/<소스 상대경로>.md다. 존재하는 소스와 계획을 구분한다.

22일차 광고주 인증·캠페인 디자인/준비된 PNG·입찰·매체 광고 선택과 23일차 선택 snapshot·노출/클릭·광고주 실적 화면이 구현돼 있다. URL은 루트 `ad_config/ad_config/urls.py`의 include에서 `ads/urls.py`로 연결하고 view는 기존 `ads/views.py`에 통합돼 있다. `ad_config/manage.py` 경로를 유지한다.

23일차 4교시의 `export_ad_events` → `ads.exporting.export_ad_events`는 `ad-event/v1` 공개 사건을 노출 기준 시각의 범위로 파일에 저장한다. 5교시 `build_ad_reports` → `read_ndjson` → `build_daily_reports` → `write_ndjson`은 서울 노출일 보고서 후보 파일을 만든다. 6교시 `load_ad_reports` → `publish_reports`는 업무 키별 게시이며 다른 날짜 행을 지우지 않는다. `ads:web-reports` → `views.report_view` → `reporting.list_reports(request.user.pk)` → `ads/reports.html`은 자기 보고서 9개 열을 표시한다. 공통 base 메뉴에 일별 보고서가 연결돼 있다.

7교시 `deliver_ad_events` → `ads.delivery.deliver_events`는 한 writer의 로컬 사건 파일을 완성한 다음 `file_delivered_at` 표식을 저장한다. 8교시 `check_ad_reports`는 전체 보관 사건으로 계산한 후보와 게시된 전체 보고서를 읽어 대조하고 결과 JSON을 저장한다. 해당 소스의 존재와 이번 문서 검증은 실제 전달/게시 재실행 성공을 뜻하지 않는다. Spark 광고 작업은 코드의 결과 메타데이터에서 `not-configured`, GUI 관찰은 `separate-manual-observation`다. `ads.delivery` import 시 모듈 하단 실습 print가 출력되는 현재 부수효과는 짝 문서에 기록했다.

24일차 2·3·4교시는 완료 검증됐다. ads/snapshot_intake.py의 inspect_snapshot·readiness·change_player와 각 관리명령이 구현돼 있다. 공식 최종 검사는 2교시 22개, 3교시 8개, 4교시 17개가 통과했다. 게임 원본은 ../Game-server/data/exports/player-cdc.ndjson이며 기존 56행과 checksum을 보존했다. 사용자가 입력한 write_cdc_readiness 및 4교시 함수·명령은 그대로 두고 readiness에 교안 필드 common_input·player_change_topic을 보완했다. 준비 JSON과 teaching-fixture 원문·summary를 광고 서버 루트의 data에 저장했고 교안 화면 검사도 통과했다. 5~8교시 후속 함수/명령은 미적용이다. 광고에서 게임 ORM을 import하지 않는다.

2026-10-08의 20 통과·2 실패는 수정 전 역사 기록이다. 현재 검증은 [2교시 공식 결과](verification/2026-10-12-day24-period01-02/official-period02.json), [실제 원본 검사](verification/2026-10-12-day24-period01-02/actual-snapshot-inspection.json), [실행 순서·인수인계](../../../docs/handoffs/2026-10-12-day24-period01-02-review.md)를 따른다.

수정된 3교시의 [이전 공식 결과](verification/2026-10-12-day24-period03-review/official-period03.json)와 [이전 원인·수정 순서](../../../docs/handoffs/2026-10-12-day24-period03-review.md)는 복구 전 3 통과·5 실패 기록이다. 당시 검토에서는 코드를 수정하지 않았다. 현재 상태는 [최종 2교시](verification/2026-10-12-day24-period04-recovery/official-period02-final.json), [최종 3교시](verification/2026-10-12-day24-period04-recovery/official-period03-final.json), [최종 4교시](verification/2026-10-12-day24-period04-recovery/official-period04-final.json), [화면 검사](verification/2026-10-12-day24-period04-recovery/screen-checker-final.json), [4교시까지 복구 인수인계](../handoffs/2026-10-12-day24-period04-recovery.md)를 따른다.

## 현재 MongoDB 실행 상태 · 2026-10-12 복구

사용자의 직접 복구 요청으로 설치 기본 standalone 서비스를 정상 종료하고, 기존 수업용 mongo-node1.yml과 infra/mongo/data/node1을 사용하는 노드를 재시작했다. 현재 PID 9900은 백그라운드 실행 중이며 ads-rs 단일 멤버 localhost:27017이 PRIMARY다. 실제 Django 관리명령의 ping은 exit 0, ok 1.0이다. village_ads의 campaigns/bids/decisions/ad_events/ad_daily_reports 5개 컬렉션을 읽었다. 소스·환경 설정·복제 구성은 수정하지 않았다.

[실제 연결 결과](verification/mongo-recovery-2026-10-12/connection-after.json), [관리명령 ping](verification/mongo-recovery-2026-10-12/manage-ping.json), [복구 인수인계](../handoffs/2026-10-12-mongodb-connection-recovery.md)를 따른다. 사용자가 Compass에서도 DB가 표시됐다고 확인했다. 에이전트가 GUI를 직접 검사한 것은 아니다. 기본 MongoDB 서비스의 시작 유형 Auto는 바꾸지 않았으므로 재부팅 뒤 서버 선택은 다시 확인해야 한다. MongoDB 실행 복구와 이후 3교시 코드 보완은 별도 작업이다.

`config/day23-*.py`와 `tools/basics/*`는 독립 실습/교안 참고 코드다. 서버 runtime 구현과 구분한다. 초기 package/scaffold 문서는 현재 정의가 없음을 명시한다. 검증용 도구의 존재도 최근 기능 테스트 실행을 뜻하지 않는다.

## Python 파일과 1:1 문서

| 현재 소스 | 짝 문서 | 책임/상태 |
|---|---|---|
| `check_day24_period4.py` | [문서](files/check_day24_period4.py.md) | 교안 화면 제공 검사; r/u/d·거절·입력 보존 |
| `ads/management/commands/write_player_change_fixture.py` | [문서](files/ads/management/commands/write_player_change_fixture.py.md) | 4교시 사용자 저장본; r/u/d 원문과 해석 summary 파일 저장 |
| `ads/management/commands/write_cdc_readiness.py` | [문서](files/ads/management/commands/write_cdc_readiness.py.md) | 사용자 입력 Command 보존; 공식 8개 및 실제 준비 JSON 저장 통과 |
| `ads/management/commands/inspect_player_snapshot.py` | [문서](files/ads/management/commands/inspect_player_snapshot.py.md) | 2교시 입력 검사 및 공개 JSON 출력 |

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
| `ads/snapshot_intake.py` | [문서](files/ads/snapshot_intake.py.md) | 2교시 snapshot·3교시 준비 상태·4교시 r/u/d 해석 검증 완료 |
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
| `tools/check_day24_logic.py` | [문서](files/tools/check_day24_logic.py.md) | 공식 검사기; 현재 2~4교시 47개 통과, 5~8교시 미적용 |
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

## 24일차 3·4교시 저장 산출물

| 현재 파일 | 짝 문서 | 책임 |
|---|---|---|
| data/contracts/cdc-readiness.json | [문서](files/data/contracts/cdc-readiness.json.md) | 경로 관찰·CDC 미구성 준비 상태 |
| data/fixtures/player-change-fixture.ndjson | [문서](files/data/fixtures/player-change-fixture.ndjson.md) | 고정 teaching-fixture r/u/d 원문 3행 |
| data/fixtures/player-change-summary.json | [문서](files/data/fixtures/player-change-summary.json.md) | 원문 checksum·change_player 해석 결과 |

이 파일들은 광고 서버 루트 data 아래의 교안 산출물이다. 기존 게임 snapshot의 경로와 bytes를 유지했고 server/data는 만들지 않았다. [실제 출력 검사](verification/2026-10-12-day24-period04-recovery/actual-output-verification.json)를 따른다.

## 과거 검증과 이전 기록 (2026-10-08)

이번 범위의 스킬 AST API 검사 결과는 [최종 구조 검사](verification/day24-routing-sync/agent-routing-final.json), [문서 경로 검사](verification/day24-routing-sync/agent-document-checks.json), [snapshot 파일 경계의 앞선 관찰](verification/day24-routing-sync/agent-snapshot-boundary.json), [인수인계](../handoffs/2026-10-08-ad-routing-progress-sync.md)를 따른다. 새 사용자 소스를 포함한 전체 Git 추적/미추적 Python 57파일·153심볼을 이 색인과 짝 문서에 대조했다. 표준 CLI는 기존 라우팅 README를 필수로 요구하는 제한으로 종료 코드 2이며 그 사실을 별도 결과에 보존한다. API 성공은 짝 문서/구조의 일치이며 문제틀의 기능 검사 통과를 뜻하지 않는다. API 성공을 CLI 성공으로 기록하지 않는다.

이전 작업의 [23일차 6교시 색인](day23-period06-index.md), [24일차 1교시 색인](day24-period01-index.md), [보고서 UI 인수인계](../handoffs/2026-10-08-day23-period06-report-template.md), [snapshot 검토 인수인계](../handoffs/2026-10-08-day24-period01-review.md), [출력 경로 정정 인수인계](../handoffs/2026-10-08-day24-data-path-correction.md)는 당시 근거다. 과거 실패/검토/제안을 현재 구현 상태로 바꾸지 않고 원래 기록을 보존한다.
