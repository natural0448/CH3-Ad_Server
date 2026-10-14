# 광고 서버 현재 진행 라우팅 색인

2026-10-12 현재 저장된 구현을 기준으로 한다. docs/server-routing/README.md는 작업 시작 HEAD 5e2712b day24 - chapter4에도 없으므로 복원하지 않고 이 색인을 사용한다. 1:1 짝 문서는 files/<소스 상대경로>.md다. 존재하는 소스와 계획을 구분한다.

22일차 광고주 인증·캠페인 디자인/준비된 PNG·입찰·매체 광고 선택과 23일차 선택 snapshot·노출/클릭·광고주 실적 화면이 구현돼 있다. URL은 루트 `ad_config/ad_config/urls.py`의 include에서 `ads/urls.py`로 연결하고 view는 기존 `ads/views.py`에 통합돼 있다. `ad_config/manage.py` 경로를 유지한다.

23일차 4교시의 `export_ad_events` → `ads.exporting.export_ad_events`는 `ad-event/v1` 공개 사건을 노출 기준 시각의 범위로 파일에 저장한다. 5교시 `build_ad_reports` → `read_ndjson` → `build_daily_reports` → `write_ndjson`은 서울 노출일 보고서 후보 파일을 만든다. 6교시 `load_ad_reports` → `publish_reports`는 업무 키별 게시이며 다른 날짜 행을 지우지 않는다. `ads:web-reports` → `views.report_view` → `reporting.list_reports(request.user.pk)` → `ads/reports.html`은 자기 보고서 9개 열을 표시한다. 공통 base 메뉴에 일별 보고서가 연결돼 있다.

7교시 `deliver_ad_events` → `ads.delivery.deliver_events`는 한 writer의 로컬 사건 파일을 완성한 다음 `file_delivered_at` 표식을 저장한다. 8교시 `check_ad_reports`는 전체 보관 사건으로 계산한 후보와 게시된 전체 보고서를 읽어 대조하고 결과 JSON을 저장한다. 해당 소스의 존재와 이번 문서 검증은 실제 전달/게시 재실행 성공을 뜻하지 않는다. Spark 광고 작업은 코드의 결과 메타데이터에서 `not-configured`, GUI 관찰은 `separate-manual-observation`다. `ads.delivery` import 시 모듈 하단 실습 print가 출력되는 현재 부수효과는 짝 문서에 기록했다.

24일차는 8교시까지 구현·저장 결과를 확인했다. 앞선 공식 검사는 2교시 22개·3교시 8개·4교시 17개이며 이번 5교시 13개·6교시 15개·7교시 10개가 모두 통과했다. 사용자가 추가한 build_snapshot_contract·load_rows·compare·missing_summary 및 세 명령을 수정하지 않고 문서화했다. 기존 2~4교시 함수는 HEAD와 같다. 게임 원본 ../Game-server/data/exports/player-cdc.ndjson과 새 after ../Game-server/data/exports/player-snapshot-after.ndjson은 각각 56행이다. 준비 JSON과 fixture, 인계 계약·비교·누락 JSON은 광고 루트 data 아래에 있다. 실제 파일에서 변경 1건·새 ID/누락 각 0건이며 저장 결과와 일치한다. 8교시 handoff_snapshot·관리명령은 사용자 저장 구현을 보존하면서 공식 24개 검사를 통과했다. 실제 data/exports/day24-input 수신본 56행과 checksum·계약 경로를 대조했고 기존 원본·계약은 유지했다. 광고에서 게임 ORM을 import하지 않는다.

2026-10-08의 20 통과·2 실패는 수정 전 역사 기록이다. 현재 검증은 [2교시 공식 결과](verification/2026-10-12-day24-period01-02/official-period02.json), [실제 원본 검사](verification/2026-10-12-day24-period01-02/actual-snapshot-inspection.json), [실행 순서·인수인계](../../../docs/handoffs/2026-10-12-day24-period01-02-review.md)를 따른다.

수정된 3교시의 [이전 공식 결과](verification/2026-10-12-day24-period03-review/official-period03.json)와 [이전 원인·수정 순서](../../../docs/handoffs/2026-10-12-day24-period03-review.md)는 복구 전 3 통과·5 실패 기록이다. 당시 검토에서는 코드를 수정하지 않았다. 현재 상태는 [최종 2교시](verification/2026-10-12-day24-period04-recovery/official-period02-final.json), [최종 3교시](verification/2026-10-12-day24-period04-recovery/official-period03-final.json), [최종 4교시](verification/2026-10-12-day24-period04-recovery/official-period04-final.json), [화면 검사](verification/2026-10-12-day24-period04-recovery/screen-checker-final.json), [4교시까지 복구 인수인계](../handoffs/2026-10-12-day24-period04-recovery.md)를 따른다.

## 24일차 5~7교시 현재 검증

이번 5~7교시 결과는 [5교시 검사](verification/2026-10-12-day24-period05-07-review/official-period05-final.json), [6교시 검사](verification/2026-10-12-day24-period05-07-review/official-period06-final.json), [7교시 검사](verification/2026-10-12-day24-period05-07-review/official-period07-final.json), [5교시 화면 검사](verification/2026-10-12-day24-period05-07-review/screen-period05.json), [실제 파일 대조](verification/2026-10-12-day24-period05-07-review/actual-file-verification.json), [7교시까지 인수인계](../handoffs/2026-10-12-day24-through-period07-review.md)를 따른다. 코드·원본·기존 산출물은 그대로 보존했고 게임 행동의 성공 응답 자체는 이번에 직접 관찰하지 않았다.

교안의 game_server 예시는 현재 Game-server 이름에 맞춘다. 광고 루트에서 `python ad_config/manage.py inspect_player_snapshot --source "../Game-server/data/exports/player-cdc.ndjson"`의 [실제 실행](verification/2026-10-12-day24-period05-07-review/actual-inspect-command.json)은 exit 0, rows=56이다. 입력 경로를 수정하며 기존 폴더 이름·배치는 유지한다.

## 24일차 8교시 완료 검증

[공식 24 통과·0 실패](verification/2026-10-12-day24-period08-finish/official-period08-before.json), [실제 인계](verification/2026-10-12-day24-period08-finish/actual-handoff.json), [8교시 인수인계와 입력 명령](../handoffs/2026-10-12-day24-period08-finish.md)을 따른다. 사용자 Python 구현은 변경하지 않았고 새 수신 NDJSON·계약만 만들었다. 기존 target은 덮어쓰지 않으며 재인계는 다른 새 target을 사용한다. 25일차 소비 입력은 data/exports/day24-input/player-cdc.ndjson이다. 파일 인계는 MongoDB/runserver 기동 없이 끝났으며 CDC 실행·실시간 광고 선택 완료로 기록하지 않는다.

## 현재 MongoDB 실행 상태 · 2026-10-13 사용자 터미널 인계

재부팅 후 Auto인 설치 기본 MongoDB 서비스가 복제 설정 없는 서버로 응답해 광고의 ads-rs 연결이 실패했다. 기본 서버를 정상 종료하고 기존 수업 DB·복제 구성(version 1/단일 localhost:27017)을 유지해 재기동했다. 복구 당시 PID 27664는 PRIMARY, Django get_db의 ping은 exit 0/1.0이었고 기존 village_ads 5개 컬렉션을 읽었다.

후속 사용자가 VS Code에서 직접 실행하겠다고 요청해 에이전트가 기동한 PID 27664를 정상 종료했다. [종료 확인](verification/mongo-recovery-2026-10-13/stop-confirmed.json) 당시 mongod와 27017 listener는 없었다. 에이전트는 추가 기동하지 않으며 사용자가 광고 작업 폴더에서 기존 명령으로 서버를 실행하고 그 터미널을 유지한다. 복구 검증 성공과 현재 사용자 요청에 따른 중지 상태를 구별한다.

[복구 시 연결 결과](verification/mongo-recovery-2026-10-13/connection-after.json), [Django ping](verification/mongo-recovery-2026-10-13/manage-ping.json), [사용자 요청 종료](verification/mongo-recovery-2026-10-13/user-requested-stop.json), [이번 인수인계](../handoffs/2026-10-13-mongodb-connection-recovery.md)를 따른다. 실제 설정은 [config/mongo-node1.yml](files/config/mongo-node1.yml.md)이며 기존 infra/mongo/data/node1을 사용한다. 코드·환경·YAML·복제 구성·업무 문서는 변경하지 않았다.

기본 서비스는 현재 Stopped지만 StartMode=Auto가 남아 있다. Set-Service Manual 시도는 Windows 관리자 권한 부족으로 거부돼 미적용이며, 자동 승인 심사 거절은 없었다. 재발 방지는 관리자 PowerShell의 Set-Service -Name MongoDB -StartupType Manual 한 번으로 적용한다. Compass는 mongodb://localhost:27017/?replicaSet=ads-rs로 수업 서버 기동 후 재연결한다. GUI는 직접 관찰하지 않았다.

[2026-10-12 복구 이력](../handoffs/2026-10-12-mongodb-connection-recovery.md)과 당시 사용자 Compass 확인은 과거 기록이다. 당시 PID 9900을 현재 실행 프로세스로 해석하지 않는다.

`config/day23-*.py`와 `tools/basics/*`는 독립 실습/교안 참고 코드다. 서버 runtime 구현과 구분한다. 초기 package/scaffold 문서는 현재 정의가 없음을 명시한다. 검증용 도구의 존재도 최근 기능 테스트 실행을 뜻하지 않는다.

## 25일차 7교시 진행 검토 · 2026-10-13

**상태: 7교시 연결 수정 완료, 브라우저의 새 선택 관찰은 사용자 실행 단계.** 1~6교시 사용자 함수·수신 데이터·56행 checkpoint·version 461은 보존했다. 광고 상위 URL에 media_urls를 연결하고 실제 decision_view/event_view 이름으로 맞췄다. ads.urls의 매체 중복 두 항목은 전용 목록으로 일원화했고 공개 주소는 같다. 인증은 헤더 매체/키로 subject-only 조회를 허용하고 기존 top-level media_id 본문도 같은 매체인지 검사한다. GET은 JSON 405/Allow POST다. 게임은 기존 views.py에 제공 ad_context를 추가하고 URL 한 항목을 연결했다. ad_gateway와 기존 선택·사건·미리보기 함수는 그대로다.

두 서버 Django check 성공, 기존 광고 test_events.py·게임 test_ads.py에 추가한 context 검사 및 관련 인증/사건 회귀 검사 총 24개(18+6)가 통과했다. 사용자 지시로 새 예제·별도 테스트 파일 네 개와 빈 examples 폴더를 제거하고 기존 파일만 수정했다. 추가 검증 폴더 두 개는 최초 자동 승인 거절 후 사용자의 명시적 삭제 승인에 따라 경로·파일 목록·해시를 재검증하여 삭제했다. 개발 구조에는 새 파일이 남지 않았다.

[수정 전후 읽기 검사](verification/2026-10-13-day25-period07-review/read-only-checks.json), [교안 대조](verification/2026-10-13-day25-period07-review/lesson-comparison.json), [두 서버 및 테스트 기록](verification/2026-10-13-day25-period07-review/django-checks.json), [기존 인수인계의 후속 수정](../handoffs/2026-10-13-day25-period07-review.md)을 따른다. MongoDB 프로세스·업무 문서·원본·checkpoint를 검토 때문에 변경하지 않았다. 8교시 구현은 범위 밖이다.

| 현재 사용자 파일 | 짝 문서 | 실제 책임·상태 |
|---|---|---|
| ads/context_projection.py | [문서](files/ads/context_projection.py.md) | 수신 검증·정규화·버전 반영·재개·갱신 |
| ads/media_urls.py | [문서](files/ads/media_urls.py.md) | 미연결이며 기존 view 이름과 달라 import 실패 |
| ads/management/commands/refresh_player_context.py | [문서](files/ads/management/commands/refresh_player_context.py.md) | 새 수신 입력을 공개 복사본 갱신 함수에 전달 |
| ads/management/commands/inspect_decision_context.py | [문서](files/ads/management/commands/inspect_decision_context.py.md) | 선택 당시와 현재 공개 context 읽기 비교 |

## 25일차 8교시 완료 · 2026-10-14

교안 제공 _read_handoff_context·export_context_handoff와 export_context_handoff Command를 현재 ads/context_projection.py 및 기존 ads/management/commands 폴더에 적용했다. 세 코드 AST가 원문과 같고 기존13개 함수는 그대로다. 최신 56행 입력에 새 완료 기록을 만들어 counts.duplicate=56/applied=0, next_line=rows=56/done=true를 확인했다. 반복 실행과 실제 인계 사본 소비는 processed=0이었다. 인계 폴더 재사용·미완료 위치는 거절했고 기존 원본/5교시 기록/Mongo 공개 문서 SHA를 보존했다.

기존 data 루트 아래 data/handoff/day25-run1에 정확한 네 파일을 작성했다. 현재 공개 복사본57행은 player-snapshot56+teaching-fixture1이며 입력 행 수와 같아야 하는 값이 아니다. 두 파일 지문과 manifest 최종 경로를 대조했다. 테스트25개와 Django check가 통과했다. Windows sandbox 임시 폴더 권한 실패 뒤 실제 사용자 환경의 격리 테스트로 검증했으며 서버 프로세스는 켜거나 끄지 않았다.

[8교시 인수인계](../handoffs/2026-10-14-day25-period08-finish.md), [실제 실행 기록의 day25_period08](verification/2026-10-13-day25-period07-review/read-only-checks.json), [코드 대조](verification/2026-10-13-day25-period07-review/lesson-comparison.json)를 따른다.

| 추가된 개발 파일·결과물 | 짝 문서 | 역할 |
|---|---|---|
| ads/management/commands/export_context_handoff.py | [문서](files/ads/management/commands/export_context_handoff.py.md) | 교안 관리명령 |
| data/checkpoints/player-context-day25-after.json | [문서](files/data/checkpoints/player-context-day25-after.json.md) | 실제 8교시 결과물 |
| data/checkpoints/player-context-day25-incomplete.json | [문서](files/data/checkpoints/player-context-day25-incomplete.json.md) | 실제 8교시 결과물 |
| data/handoff/day25-run1/player-context-changes.ndjson | [문서](files/data/handoff/day25-run1/player-context-changes.ndjson.md) | 실제 8교시 결과물 |
| data/handoff/day25-run1/checkpoint.json | [문서](files/data/handoff/day25-run1/checkpoint.json.md) | 실제 8교시 결과물 |
| data/handoff/day25-run1/player-context.ndjson | [문서](files/data/handoff/day25-run1/player-context.ndjson.md) | 실제 8교시 결과물 |
| data/handoff/day25-run1/manifest.json | [문서](files/data/handoff/day25-run1/manifest.json.md) | 실제 8교시 결과물 |

## Python 파일과 1:1 문서

| 현재 소스 | 짝 문서 | 책임/상태 |
|---|---|---|
| `ads/management/commands/handoff_player_snapshot.py` | [문서](files/ads/management/commands/handoff_player_snapshot.py.md) | 8교시 공식 24개 통과; 새 수신 폴더에 원본·계약 인계 완료 |
| `ads/management/commands/write_snapshot_contract.py` | [문서](files/ads/management/commands/write_snapshot_contract.py.md) | 5교시 사용자 구현; 검사 원본과 인계 계약 JSON 연결 |
| `ads/management/commands/compare_player_snapshots.py` | [문서](files/ads/management/commands/compare_player_snapshots.py.md) | 6교시 사용자 구현; 검증한 두 파일의 업무 상태 비교 |
| `ads/management/commands/read_snapshot_missing.py` | [문서](files/ads/management/commands/read_snapshot_missing.py.md) | 7교시 사용자 구현; 누락 관찰과 삭제 추론 불가 기록 |
| `tools/check_day24_period5.py` | [문서](files/tools/check_day24_period5.py.md) | 교안 제공 검사; tools 배치를 유지한 모듈 실행 |
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
| `ads/snapshot_intake.py` | [문서](files/ads/snapshot_intake.py.md) | 2~7교시 snapshot·준비·fixture·계약·상태 비교·누락 관찰 |
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
| `tools/check_day24_logic.py` | [문서](files/tools/check_day24_logic.py.md) | 공식 검사기; 이전 2~4교시 47개·5~7교시 38개·8교시 24개 통과 |
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

## 24일차 3~8교시 저장 산출물

| 현재 파일 | 짝 문서 | 책임 |
|---|---|---|
| data/contracts/cdc-readiness.json | [문서](files/data/contracts/cdc-readiness.json.md) | 경로 관찰·CDC 미구성 준비 상태 |
| data/fixtures/player-change-fixture.ndjson | [문서](files/data/fixtures/player-change-fixture.ndjson.md) | 고정 teaching-fixture r/u/d 원문 3행 |
| data/fixtures/player-change-summary.json | [문서](files/data/fixtures/player-change-summary.json.md) | 원문 checksum·change_player 해석 결과 |
| data/contracts/player-cdc-contract.json | [문서](files/data/contracts/player-cdc-contract.json.md) | 5교시 검증 원본·공개 계약·시각·checksum |
| data/checks/day24-comparison.json | [문서](files/data/checks/day24-comparison.json.md) | 6교시 실제 업무 상태 변경 1건·새 ID/누락 0건 |
| data/checks/day24-missing.json | [문서](files/data/checks/day24-missing.json.md) | 7교시 누락 0건·빈 삭제 목록·삭제 추론 불가 |
| data/exports/day24-input/player-cdc.ndjson | [문서](files/data/exports/day24-input/player-cdc.ndjson.md) | 8교시 실제 수신 원본 56행·원본 bytes/checksum 유지 |
| data/exports/day24-input/player-cdc-contract.json | [문서](files/data/exports/day24-input/player-cdc-contract.json.md) | 8교시 수신 계약·source_path만 수신 파일 경로 |

이 파일들은 광고 서버 루트 data 아래의 교안 산출물이다. 기존 게임 snapshot의 경로와 bytes를 유지했고 server/data는 만들지 않았다. [실제 출력 검사](verification/2026-10-12-day24-period04-recovery/actual-output-verification.json)를 따른다.

5~7교시 사용자 저장본은 [이번 실제 파일 검사](verification/2026-10-12-day24-period05-07-review/actual-file-verification.json)를 따른다. after의 생산 책임과 원본은 [게임 데이터 짝 문서](../../../Game-server/docs/server-routing/files/data/exports/player-snapshot-after.ndjson.md)에서 확인한다.

## 과거 검증과 이전 기록 (2026-10-08)

이번 범위의 스킬 AST API 검사 결과는 [최종 구조 검사](verification/day24-routing-sync/agent-routing-final.json), [문서 경로 검사](verification/day24-routing-sync/agent-document-checks.json), [snapshot 파일 경계의 앞선 관찰](verification/day24-routing-sync/agent-snapshot-boundary.json), [인수인계](../handoffs/2026-10-08-ad-routing-progress-sync.md)를 따른다. 새 사용자 소스를 포함한 전체 Git 추적/미추적 Python 57파일·153심볼을 이 색인과 짝 문서에 대조했다. 표준 CLI는 기존 라우팅 README를 필수로 요구하는 제한으로 종료 코드 2이며 그 사실을 별도 결과에 보존한다. API 성공은 짝 문서/구조의 일치이며 문제틀의 기능 검사 통과를 뜻하지 않는다. API 성공을 CLI 성공으로 기록하지 않는다.

이전 작업의 [23일차 6교시 색인](day23-period06-index.md), [24일차 1교시 색인](day24-period01-index.md), [보고서 UI 인수인계](../handoffs/2026-10-08-day23-period06-report-template.md), [snapshot 검토 인수인계](../handoffs/2026-10-08-day24-period01-review.md), [출력 경로 정정 인수인계](../handoffs/2026-10-08-day24-data-path-correction.md)는 당시 근거다. 과거 실패/검토/제안을 현재 구현 상태로 바꾸지 않고 원래 기록을 보존한다.


## 26일차 1·2교시 완료 · 2026-10-14

사용자가 먼저 작성한 lake_files.py stable_json/build_history를 문서로 맞춘 뒤, history 오류문자열을 교안대로 보정하고 current 함수를 추가했다. 두 함수/JSON helper와 inspect_player_lake·demo_player_lake 두 명령이 제공 완성코드 AST와 같다. 인계 source/manifest/checkpoint와SHA를같이검사하고 결과목록을 메모리에서만 계산한다. 이 기록은1·2교시 완료 시점이며3교시 저장 구현은 아래 별도 검토 기록을 따른다.

실제 25일차 인계56행에서 history56/current56, 반복112행/역순에도 단계별목록SHA가 같다. history 첫대상3/version1과 current 첫대상1/version461은 서로다른정렬기준에 따른 결과다. fixture최신4/coins40, 삭제4유지, 내용SHA·동일version충돌거절, 빈목록을 확인했다. 실제 명령의 get_db호출0·writtenFalse·원본/인계/기록bytes보존을 확인했으며 관련33개 검사와Django check가통과했다.

[1·2교시 인수인계](../handoffs/2026-10-14-day26-period01-02-finish.md), [시작/교안/실행/마감증거](verification/day26-period01-02.json)를 따른다. 기존25일차 미커밋 변경은 보존했다. 초급코드는 새examples 폴더 대신 기존tools/basics 위치에저장했고 코드내용/출력은같다.

| 현재 개발파일 | 짝 문서 | 책임 |
|---|---|---|
| ads/lake_files.py | [문서](files/ads/lake_files.py.md) | 검증·중복제거·최신후보 메모리계산 |
| ads/management/commands/inspect_player_lake.py | [문서](files/ads/management/commands/inspect_player_lake.py.md) | 같은인계검사·history/current 미리보기 |
| ads/management/commands/demo_player_lake.py | [문서](files/ads/management/commands/demo_player_lake.py.md) | DB없는fixture관찰 |
| tools/basics/day26_period01.py | [문서](files/tools/basics/day26_period01.py.md) | 1교시두초급예제 |
| tools/basics/day26_period02.py | [문서](files/tools/basics/day26_period02.py.md) | 2교시두초급예제 |

## 26일차3교시 완료 검증 · 2026-10-14

사용자가 저장한 변경4개를 먼저 짝 문서에 정합화했다. 발견한3개 문제는 build_lake_version의 summary.json 저장명, 빈 compare_player_lake_versions 파일, compare_player_snapshots에 잘못 중복 저장된 Lake 비교 코드다. 저장명은manifest.json으로 수정하고 Lake 명령에 교안 전체를 적용했으며 snapshot 명령은 d68b511의 기존 기능으로 복구했다. 사용자의1·2교시 함수와 build_player_lake는 유지했다.

교안의 불완전 run 복구 절차대로 기존 run-001/002는 수정하지 않고 새 run-003/004를 만들었다. 둘의 source/history/current_matches는 모두true, N=H=K=56이다. input SHA=18dbb0bd715f69a4bfde646623cd3d39932f9c147fdf7858f6276732bb51e154이며1교시 선택 인계와 같다. history 파일SHA=ad682d307f0508b2cbffbd48beece93ad974cb03e7cc9161b3b725d64e4d3a98, current 파일SHA=2814cd044e44ebe3f92e63c3e53631aa04a41a87c34cae0b948829c458df60ac다. 같은run 재작성은CommandError, 기존14개 원본/완료기록/인계/사용자run 파일의SHA는보존됐다. 네 번째 교시에는 완성된run-003/current.ndjson과 동일 인계 source를 연결한다. 기존run-001/002는manifest가 없으므로 현재도불완전하며 소비하지 않는다.

관련39개 테스트·Django check·초급64/True가통과했다. 표준 라우팅CLI는 기존README.md 부재로실패해 기존current-progress-index와 AST API로변경범위를검사한다. [실행·시작코드·검증](verification/day26-period03.json)과 [인수인계](../handoffs/2026-10-14-day26-period03-fix.md)를 따른다. MongoDB·게임·웹서버는변경하지 않았다.

| 현재 소스 | 짝 문서 | 현재 책임 |
|---|---|---|
| ads/management/commands/build_player_lake.py | [문서](files/ads/management/commands/build_player_lake.py.md) | 선택 입력에서 새 run 저장 |
| ads/management/commands/compare_player_lake_versions.py | [문서](files/ads/management/commands/compare_player_lake_versions.py.md) | 실제 파일 지문·행 수 검증 및 비교 |
| tools/basics/day26_period03.py | [문서](files/tools/basics/day26_period03.py.md) | bytes와SHA 초급 예제 |


| 생성 결과물 | 짝 문서 | 상태 |
|---|---|---|
| data/lake/gold/player_current/run-003/history.ndjson | [문서](files/data/lake/gold/player_current/run-003/history.ndjson.md) | 완성run3교시결과물 |
| data/lake/gold/player_current/run-003/current.ndjson | [문서](files/data/lake/gold/player_current/run-003/current.ndjson.md) | 완성run3교시결과물 |
| data/lake/gold/player_current/run-003/manifest.json | [문서](files/data/lake/gold/player_current/run-003/manifest.json.md) | 완성run3교시결과물 |
| data/lake/gold/player_current/run-004/history.ndjson | [문서](files/data/lake/gold/player_current/run-004/history.ndjson.md) | 완성run3교시결과물 |
| data/lake/gold/player_current/run-004/current.ndjson | [문서](files/data/lake/gold/player_current/run-004/current.ndjson.md) | 완성run3교시결과물 |
| data/lake/gold/player_current/run-004/manifest.json | [문서](files/data/lake/gold/player_current/run-004/manifest.json.md) | 완성run3교시결과물 |

## 26일차 4교시 진행 중 · Lake 비교 경로 확인

사용자의 run-001/002 비교 명령은 run-001/manifest.json 부재로 CommandError였다. 기존 summary.json만 있는 두 run은 보존한다. 완성된 run-003/004 비교를 재실행해 source/history/current_matches 모두 true와 N=H=K=56을 확인했다. 4교시에서도 lake-dir 또는 shell current 입력을 run-003으로 지정한다. 소비 검사를 summary.json으로 완화하거나 이전 결과를 덮어쓰지 않았다.

사용자가 새로 저장한 아래3개 파일은 현재 코드 그대로 문서에 등록했고 수정하지 않았다. 실제 Mongo 대조 및 4교시 완료 판정은 이번 요청 범위에서 실행하지 않았다. [실행·Git 상태](verification/day26-period04-lake-path.json), [인수인계·정확한 명령](../handoffs/2026-10-14-day26-period04-lake-path.md)를 따른다.

| 현재 소스 | 짝 문서 | 현재 책임 |
|---|---|---|
| ads/sink_evidence.py | [문서](files/ads/sink_evidence.py.md) | 공개 문서 검증·다섯 필드 대조·지정 매체 읽기 |
| ads/management/commands/compare_player_sinks.py | [문서](files/ads/management/commands/compare_player_sinks.py.md) | 같은 원본/완성 Lake 검증 후 공개 Mongo 대조 JSON 저장 |
| ads/management/commands/demo_player_sink_comparison.py | [문서](files/ads/management/commands/demo_player_sink_comparison.py.md) | 메모리 fixture 사례 대조 |
