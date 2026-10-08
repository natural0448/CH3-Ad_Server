# 23일차 6교시 현재 구현 색인

기존 `docs/server-routing/README.md`는 작업 시작 시 삭제돼 있었다. 그 삭제를 유지하고 이번 범위만 이 별도 색인에 등록한다. 짝 문서는 기존 `files/<소스 상대경로>.md` 규칙을 사용한다.

2026-10-08까지 광고 전체 진행의 현재 구현은 [현재 진행 색인](current-progress-index.md)을 따른다. 이 문서는 6교시 보고서 화면 작업 범위와 당시 검증 근거를 유지한다.

사용자가 추가한 보고서 view·URL·게시 명령·기초 실습과 표 템플릿을 개발 변경 전 실제 코드 기준으로 먼저 정합화했다. 현재 보고서 템플릿은 기존 `base.html`과 CSS를 사용하며 상단 메뉴에서 직접 들어갈 수 있다. 교안의 9개 출력 항목·CTR 0~1·원본 시각 문자열·빈 목록 계약을 유지한다. 검증이 끝난 현재 구현과 이전 상태의 근거는 `verification/day23-period06-template/`에 있다.

| 개발 파일 | 짝 문서 |
|---|---|
| ads/views.py | [문서](files/ads/views.py.md) |
| ads/urls.py | [문서](files/ads/urls.py.md) |
| ads/reporting.py | [문서](files/ads/reporting.py.md) |
| ads/management/commands/build_ad_reports.py | [문서](files/ads/management/commands/build_ad_reports.py.md) |
| ads/management/commands/load_ad_reports.py | [문서](files/ads/management/commands/load_ad_reports.py.md) |
| config/day23-period-06.py | [문서](files/config/day23-period-06.py.md) |
| ads/templates/ads/reports.html | [문서](files/ads/templates/ads/reports.html.md) |
| ads/templates/ads/base.html | [문서](files/ads/templates/ads/base.html.md) |
| ads/static/ads/advertiser.css | [문서](files/ads/static/ads/advertiser.css.md) |

기존 통합 views 구조에서 `ads:web-reports` → `views.report_view` → `reporting.list_reports(request.user.pk)` → `ads/reports.html`로 연결한다. `load_ad_reports`는 사용자가 직접 후보 파일을 게시할 때 실행하는 명령이다. 서버 실행/종료와 실제 게시 명령은 이번 UI 작업에서 자동 수행하지 않는다.

[요청 결과와 인수인계](../handoffs/2026-10-08-day23-period06-report-template.md), [표시 계약 검사](verification/day23-period06-template/functional-checks.json), [실제 화면 검사](verification/day23-period06-template/visual-checks.json)를 함께 읽는다. 기본 검사기는 삭제된 README를 필수로 요구하므로 별도 색인과 짝 문서 검사는 같은 스킬의 AST API로 수행했다. 기존 README 삭제를 되돌려 표준 검사 통과로 기록하지 않는다.
