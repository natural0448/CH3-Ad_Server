# 2026-10-07 · 22일차 광고 서버 동기화

> 2026-10-07 검토 주석: 아래는 해당 작업 시점의 결과를 보존한 이력입니다. 교안 버전·적용 범위·검사 수는 최신 상태와 다를 수 있습니다. [차이와 현재 상태](../server-routing/reviews/2026-10-07-lesson-deviations.md).

## 요청 목적과 결과

수정 교안 「22일차 · 광고 플랫폼이 광고주의 광고를 게임 유저에게 집행한다」의 광고 서버 부분을 기존 ad_server에 동기화했다. 텍스트 캠페인·입찰·최고 입찰 선택·선택 시점 스냅샷·광고주 웹·매체 키 API와 1/2교시 PyMongo 연습, 8교시 결정 비교/로컬 크레딧 모형을 추가했다. 게임 서버 중계나 Pygame 화면 표시를 완료한 것으로 기록하지 않는다.

후속 요청인 오늘 교안의 1교시 준비 점검에서 MONGO_URI가 Django 설정 모듈명으로 잘못 대입되던 한 줄을 발견했다. 환경변수 MONGO_URI를 읽도록 수정했으며 DJANGO_SETTINGS_MODULE을 설정 파일에서 덮어쓰지 않는다. 오늘 수업의 사건 저장·보고서 기능은 아직 수업 진행 전이며 구현하지 않았다.

## 작업 시작 전 Git 상태와 기존 작업 보존

- Chapter3 및 ad_server: **Git 상태 확인 불가: 저장소 아님**. 직전 커밋/staged/unstaged/untracked를 Git으로 분류할 수 없다. 임의 초기화하지 않았다.
- 상위 C:/MLO01-01 조회는 최초 점검에서 권한 오류가 있었다. 대상 두 경로의 저장소 아님 결과와 구분한다.
- 최종 상위 경계 재조회는 저장소 아님으로 확인됐다. 시작 전에 존재한 겹치는 개발 파일을 먼저 읽고 문서를 맞춘 뒤 개발했고, 테스트 종료 후 이번 변경분만 다시 정합화했다.
- 시작 파일 목록과 SHA256 비교를 사용했다. 시작 전에 존재한 모든 파일은 사용자 작업으로 취급했다.
- 기존 ads.env의 내용/해시는 변경하지 않았다. 실제 비밀값과 환경 파일 값은 본 문서와 검사 보고서에 기록하지 않았다.
- 계정 DB ads-auth.sqlite3를 계속 사용하며 기존 ads_manage.py의 경로 추가를 보존했다. DB는 읽기 점검만 했고 본 작업에서 계정 생성·실데이터 시딩·migrate를 실행하지 않았다.
- requirements.txt, 기존 인수인계 두 건, 사용자 작성 ads_manage.py 등 보존 여부는 변경 목록 JSON에 기록했다.

## 이번 개발 변경

기존 파일 수정 7개:

- .gitignore
- ads/auth_views.py
- ads/tests.py
- ads/views.py
- ad_config/manage.py
- ad_config/ad_config/settings.py
- ad_config/ad_config/urls.py

새 개발 파일 18개:

- .env.example
- ads/mongo.py
- ads/repository.py
- ads/services.py
- ads/urls.py
- config/mongo-node1.yml
- config/mongo-node2.yml
- config/mongo-node3.yml
- tools/verify_day22.py
- tools/basics/day22_credit_model.py
- tools/basics/day22_period01.py
- tools/basics/day22_period02.py
- ads/management/__init__.py
- ads/templates/ads/bids.html
- ads/templates/ads/campaigns.html
- ads/templates/registration/login.html
- ads/management/commands/compare_ad_decisions.py
- ads/management/commands/__init__.py

파일 이동·삭제는 없다. README.md를 새로 작성했고 수업용 빈 데이터 폴더 infra/mongo/data/node1~3을 준비했다. 테스트가 생성한 infra/runtime 로그는 .gitignore 대상이다.

## 설계 결정과 책임 경계

- 중첩 ad_config와 바깥 ads 구조를 유지한다. BASE_DIR는 ad_config, WORKING_DIR는 ad_server다. 표준 명령은 ad_config/manage.py이며 기존 ads_manage.py도 호환된다.
- 기존 ads.env를 읽은 뒤 루트 .env가 실제로 있으면 우선 적용한다. 새 비밀 환경 파일을 생성하지 않았다.
- SQLite 계정은 기존 ads-auth.sqlite3를 유지한다. 광고 campaigns/bids/decisions는 PyMongo를 사용한다.
- 광고주 HTTP는 세션·로그인·CSRF, 매체 선택은 X-Media-Key 인증이다. 결정은 현재 입찰과 독립된 후보·소재·맥락 스냅샷이다.
- 최고 금액 우선, 동률은 campaign_id 오름차순. 후보가 없어도 결정은 저장하고 API는 ad:null을 응답한다.
- 다른 소유자의 같은 ID 캠페인/입찰을 덮어쓰지 않는다. 입력 검증은 400, 매체 인증은 403, MongoDB 장애는 503으로 처리한다.
- 저장 문서의 chosen_campaign_id/chosen_bid_amount를 비교 명령의 campaign_id/bid_amount 표시로 매핑했다. 교안의 저장 필드명 불일치를 반영했다.
- 실제 지갑 차감·노출 기록·게임 연동은 이번 동기화 범위 밖이다. 크레딧 예제의 22/78은 로컬 모형이다.

## 최종 라우팅 문서 정합화

개발 변경 25개 각각에 docs/server-routing/files/<상대경로>.md를 대응시켰다. 색인 docs/server-routing/README.md에 25개와 기존 호환 진입점 ads_manage.py를 합쳐 26개를 등록했다. 함수 시그니처/인자/반환·실패/의사코드/직접 호출·기대 결과 및 설정 출처를 확인했다.

routing-doc-auditor의 Git CLI는 저장소가 없어 실행할 수 없었다. 동일 도구의 extract_symbols와 mark_documented를 명시적 파일 목록에 적용했다. 26개 문서·색인, Python 18개 시그니처 검사에서 누락 0, 전체 대상 소스 AST 구문 오류 0이다. Git 수집 불가와 문서 검사 통과를 별도 필드로 기록했다.

- docs/server-routing/verification/day22-sync-audit.json
- docs/server-routing/verification/day22-sync-changes.json

## 실행한 검사와 결과

모든 Python 명령은 ad_server의 기존 .venv에서 실행했다.

1. python -B ad_config/manage.py check: 오류 0.
2. python -B ad_config/manage.py test ads: 기본 환경에서 일반 테스트 9개 통과, Mongo 통합 12개는 테스트 전용 주소가 없어 skip.
3. python -B tools/verify_day22.py --mongod "C:/Program Files/MongoDB/Server/8.3/bin/mongod.exe": 별도 포트 27107의 실제 테스트 복제 세트에서 **21개 전부 통과, skip 0**. MONGO_URI 수정 후 다시 전부 통과했다. 테스트 DB를 제거하고 자신이 만든 자식 mongod만 종료했다.
4. 1/2교시 PyMongo 스크립트를 별도 포트 27108의 임시 DB에서 실행: ping 성공, 연습 문서 삽입/조회/수정(우선순위 3)/삭제 성공, 잔여 0. 임시 DB 및 소유 프로세스 정리.
5. day22_credit_model.py: 고유 노출/클릭/전환 각 1, 차감 22, 잔액 78.
6. 별도 Django 포트 18001 HTTP: 웹 로그인 200, CSRF API 200, 매체 키 없는 요청 403. 토큰·쿠키 내용은 기록하지 않았다. 검사 서버 종료.
7. compare_ad_decisions를 제어된 저장 문서로 실행: 당시 camp-tea/20과 forest-tools/30을 정상 표시. 실DB에는 쓰지 않았다.
8. 환경 로딩 검증: MONGO_URI가 환경에서 로딩되고 Django 모듈명이 유지됨. URI 파싱 성공. 실제 구성 DB ping은 ServerSelectionTimeoutError여서 준비 완료로 표시하지 않았다.
9. 최종 문서·색인·AST 검사: 26개 모두 통과.

최종 테스트 로그: infra/runtime/day22-validation-9b58ca0137d14aaf853bdca05ef6f275/mongod.log.

## 남은 준비사항과 다음 순서

현재 MongoDB Windows 서비스는 27017의 단독 서버다. 기존 환경 설정은 세 멤버 복제 세트 연결을 요구한다. 서비스나 사용자 데이터를 이번 작업에서 변경하지 않았다. 현재 광고주 계정 0, 조회한 단독 서버의 캠페인/결정 0이다. 실제 Pygame 광고 표시 증거도 확인되지 않았다.

1. README.md의 MongoDB 실행 절차로 선택한 복제 세트를 준비한다. 오늘 교안은 단일 멤버 방식이므로 기존 환경 파일의 연결 방식과 함께 맞춰야 한다.
2. python ad_config/manage.py check
3. python ad_config/manage.py createsuperuser (사용자가 계정/비밀번호 직접 입력)
4. python ad_config/manage.py runserver 127.0.0.1:8001
5. 광고주 웹에서 캠페인과 입찰을 저장하고 shell에서 조회한다.
6. 실제 게임 표시·subject·새 결정 ID를 확보한 후 오늘 1교시의 노출 기록 실습을 진행한다.

세부 사전 점검 결과와 시작 명령은 docs/handoffs/2026-10-07-day23-period01-preflight.md에 있다. 실제 Game-server/MySQL/Pygame 전체 연동은 해당 기능이 현 폴더에서 확인되지 않아 검증하지 못했다. 새로운 Kafka/Spark/Connect 설치는 하지 않았다.
