# 광고 서버 라우팅 색인

현재 구현만 기록한다. 중첩 프로젝트와 루트 ads를 유지한다. 표준 명령은 ad_config/manage.py, 기존 ads_manage.py도 호환된다. 계정 DB와 비밀 키는 보존했고 ads.env의 MongoDB 연결 설정은 단일 멤버 수업 구성으로 맞췄다. 교안 동기화 파일과 직접 진입점, 로컬 설정 계약이 검사 범위다.

| 개발 파일 | 짝 문서 |
|---|---|
| .env.example | [문서](files/.env.example.md) |
| .gitignore | [문서](files/.gitignore.md) |
| ads.env | [문서](files/ads.env.md) |
| ad_config/ad_config/settings.py | [문서](files/ad_config/ad_config/settings.py.md) |
| ad_config/ad_config/urls.py | [문서](files/ad_config/ad_config/urls.py.md) |
| ad_config/ads_manage.py | [문서](files/ad_config/ads_manage.py.md) |
| ad_config/manage.py | [문서](files/ad_config/manage.py.md) |
| ads/auth_views.py | [문서](files/ads/auth_views.py.md) |
| ads/management/__init__.py | [문서](files/ads/management/__init__.py.md) |
| ads/management/commands/__init__.py | [문서](files/ads/management/commands/__init__.py.md) |
| ads/management/commands/compare_ad_decisions.py | [문서](files/ads/management/commands/compare_ad_decisions.py.md) |
| ads/mongo.py | [문서](files/ads/mongo.py.md) |
| ads/repository.py | [문서](files/ads/repository.py.md) |
| ads/services.py | [문서](files/ads/services.py.md) |
| ads/templates/ads/bids.html | [문서](files/ads/templates/ads/bids.html.md) |
| ads/templates/ads/campaigns.html | [문서](files/ads/templates/ads/campaigns.html.md) |
| ads/templates/registration/login.html | [문서](files/ads/templates/registration/login.html.md) |
| ads/tests.py | [문서](files/ads/tests.py.md) |
| ads/urls.py | [문서](files/ads/urls.py.md) |
| ads/views.py | [문서](files/ads/views.py.md) |
| config/mongo-node1.yml | [문서](files/config/mongo-node1.yml.md) |
| config/mongo-node2.yml | [문서](files/config/mongo-node2.yml.md) |
| config/mongo-node3.yml | [문서](files/config/mongo-node3.yml.md) |
| tools/basics/day22_credit_model.py | [문서](files/tools/basics/day22_credit_model.py.md) |
| tools/basics/day22_period01.py | [문서](files/tools/basics/day22_period01.py.md) |
| tools/basics/day22_period02.py | [문서](files/tools/basics/day22_period02.py.md) |
| tools/verify_day22.py | [문서](files/tools/verify_day22.py.md) |
| ads/events.py | [문서](files/ads/events.py.md) |


## 22일차 추가 파일

| 개발 파일 | 짝 문서 |
|---|---|
| ads/creatives.py | [문서](files/ads/creatives.py.md) |
| ads/templates/ads/base.html | [문서](files/ads/templates/ads/base.html.md) |
| ads/static/ads/advertiser.css | [문서](files/ads/static/ads/advertiser.css.md) |
| ads/static/ads/advertiser.js | [문서](files/ads/static/ads/advertiser.js.md) |
| ads/static/ads/creatives/forest-tools.png | [문서](files/ads/static/ads/creatives/forest-tools.png.md) |
| ads/static/ads/creatives/camp-tea.png | [문서](files/ads/static/ads/creatives/camp-tea.png.md) |
| data/evidence/asset-sources.md | [문서](files/data/evidence/asset-sources.md.md) |
| tools/verify_day22_images.py | [문서](files/tools/verify_day22_images.py.md) |
| README.md | [문서](files/README.md.md) |

## 22일차 이미지 광고 흐름

광고주 폼 → campaign creative_path → 선택 당시 creative snapshot → media API → 게임 세션 Player 중계 → 동일 origin PNG bytes → Pygame main thread image decode/draw/flip. 매체 키는 두 서버 설정에만 존재하며 브라우저/접속기에 전달하지 않는다. 실제 학생 창 관찰은 별도 evidence이며 임시 fixture 검증 결과로 대신 기록하지 않는다.

| ads/media_auth.py | [문서](files/ads/media_auth.py.md) |
| ads/test_events.py | [문서](files/ads/test_events.py.md) |
| ads/management/commands/ensure_ad_event_indexes.py | [문서](files/ads/management/commands/ensure_ad_event_indexes.py.md) |
| tools/basics/day23_record_observed.py | [문서](files/tools/basics/day23_record_observed.py.md) |
| tools/verify_day23.py | [문서](files/tools/verify_day23.py.md) |

## 기존 Pygame 사건 전송과 수정 교안 범위

기존 구현의 활성 화면 draw/flip receipt → Controller impression → AuthSession/CSRF → 게임 세션 Player → 두 매체 헤더 인증 → 최초 사건 저장 → 공개 receipt 경로를 보존한다. 자동 Pygame 노출·클릭은 수정 교안의3교시 기능이며 기존 코드의 회귀검사를 수행했다. 수정1교시는 입찰 반환·선택 snapshot,2교시는 사건 API·광고주 선택/실적 목록이다. 일별 보고서·집계·파일 전달은 미적용이다.

## 수정 23일차 사건 저장

ads/events.py는 수정2교시 CODE15를 사용한다. 실제 services.clean_subject를 호출하며 수신자를 dotted 필터로 비교하고 당시 후보의 소유자·금액을 검증한다. 과거 결정은 새 선택을 요구하고 현재 값으로 보정하지 않는다. 기존 재점검 기록은 historical evidence로 남긴다.

| tools/day22_connection.py | [문서](files/tools/day22_connection.py.md) |
| tools/day22_crud.py | [문서](files/tools/day22_crud.py.md) |
| tools/verify_lesson_alignment.py | [문서](files/tools/verify_lesson_alignment.py.md) |

## 교안 정본 대응

정본은22일차 수정 교안과 「현재 ad_server에서 노출·클릭과 광고주 보고서 완성하기」 v2.3의1·2교시다. AST/실습/표23개 대조 및 적응 목록은 ad_server/docs/server-routing/verification/lesson-alignment/source-comparison.json, 실행 순서는 ad_server/README.md에 있다. 기존4인수 선택·bid_amount 스키마·이미지·계정·DB·combined view와 계층을 보존했다. 새 광고주 events 목록은 구현했고 일별 reports/집계/파일전달은 미적용이다. 이전 정본의 자동 접속기 코드는 수정3교시의 기존 구현으로 보존했다.

| config/day23-subject.py | [문서](files/config/day23-subject.py.md) |

| config/day23-period-01.py | [문서](files/config/day23-period-01.py.md) |

| config/day23-period-02.py | [문서](files/config/day23-period-02.py.md) |

| ads/management/commands/create_ad_indexes.py | [문서](files/ads/management/commands/create_ad_indexes.py.md) |

| ads/templates/ads/events.html | [문서](files/ads/templates/ads/events.html.md) |

## 수정23일차3교시 적용

현재계층 대응과실행순서는 프로젝트 README의3교시 항목에있다. 마을게시판의 실제flip→노출→확인후클릭, 임시2초재시도·영구거절2초새선택·인증정리,표시후10초유지·15초선택간격을구현했다. 실제학생창관찰은별도not_run이다.

| config/day23-period-03.py | [문서](files/config/day23-period-03.py.md) |
