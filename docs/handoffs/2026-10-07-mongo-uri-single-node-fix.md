# 2026-10-07 · 단일 멤버 MongoDB 연결 수정과 초기화 오류 진단

> 2026-10-07 검토 주석: 아래는 해당 작업 시점의 결과를 보존한 이력입니다. 교안 버전·적용 범위·검사 수는 최신 상태와 다를 수 있습니다. [차이와 현재 상태](../server-routing/reviews/2026-10-07-lesson-deviations.md).

## 목적·결과

사용자가 환경 파일용 MONGO_URI 대입을 PowerShell에서 실행해 CommandNotFound 오류를 겪었고, replSetInitiate에서 NoReplicationEnabled를 제시했다. ads.env의 MONGO_URI 한 줄만 단일 멤버 수업 구성으로 변경했다. Django 로딩·URI 파싱·system check는 통과했다. 실제 서버 전환은 Windows 서비스 제어 권한 부족으로 완료하지 못했다.

## 시작 Git 상태·기존 작업

Chapter3/ad_server: **Git 상태 확인 불가: 저장소 아님**. 직전 커밋/staged/unstaged/untracked 분류 불가. 저장소를 만들지 않았다. 시작 전에 존재한 파일은 사용자 작업으로 취급했다. 기존 교안 동기화와 코드·계정 DB·게임 파일은 수정하지 않았다.

이전 동기화 인수인계의 환경 파일 보존 기록은 그 작업 당시의 결과다. 이번 후속 작업에서 별도로 연결 설정을 수정했다. 실제 환경 값·비밀값은 문서/검사 보고서에 기록하지 않는다.

## 이번 파일 변경

- 수정 개발 파일: ads.env의 MONGO_URI 한 줄.
- 추가 짝 문서: docs/server-routing/files/ads.env.md.
- 수정 색인: docs/server-routing/README.md.
- 추가 검사 기록: docs/server-routing/verification/mongo-single-node-fix.json.
- 추가 인수인계: 본 문서.
- 개발 파일 추가·이동·삭제 없음.

## 결정과 책임

환경 파일은 KEY=VALUE 형식이며 PowerShell 명령이 아니다. 설정 코드가 ads.env를 override=True로 읽으므로 실제 파일을 변경했다. MONGO_URI 외 다른 키와 파일 바이트를 보존했다.

연결 URI와 MongoDB 서버의 replication 옵션은 별개다. 실행 중 서버는 설치 기본 mongod.cfg/data 경로를 사용하며 복제 옵션이 없다. 수업용 mongo-node1.yml에는 복제 옵션이 있지만 현재 서버가 그 설정을 사용하지 않았다. 기존 서비스 데이터 폴더를 변경·복사·삭제하지 않았다.

## 최종 문서 정합화

환경 파일의 기존 계약을 먼저 문서화하고 수정했다. 검증 후 읽기 주체·우선순위·쓰기 소유자·최종 단일 멤버 계약을 짝 문서와 색인에 반영했다. 실제 값은 비공개로 유지했다. 비 Python 환경 파일이므로 AST 시그니처 검사는 해당 없음. Git 기반 감사 수집은 저장소가 없어 실행 불가이며 파일/문서/색인 존재와 설정 검증을 직접 수행했다.

## 검사와 결과

- 바이트/ dotenv_values 비교: MONGO_URI 한 줄 외 동일, 다른 키 보존.
- django.setup 및 pymongo.uri_parser.parse_uri: 수정 주소 로딩 성공, 단일 멤버·복제 옵션 확인.
- python -B ad_config/manage.py check: 오류 0.
- 실제 설정 DB ping: ServerSelectionTimeoutError. 서버에 복제 옵션이 없어 아직 연결되지 않음.
- 직접 연결 hello/getCmdLineOpts: 설치 기본 설정, 복제 옵션 없음.
- 문서·색인·설정 파일 존재 확인 완료.
- 최종 Git 재조회: 저장소 아님. 기존 작업과 이번 변경은 파일 범위 및 바이트 비교로 구분.
- 코드 로직 변경이 없어 앞서 통과한 21개 광고 통합 테스트는 반복하지 않았다. 이번 실제 DB 접속 실패 결과와 구분했다.

## 실행하지 못한 작업·위험

서버 전환 직전 포트 소유자가 서비스 PID와 달라 자동 전환을 중단했다. 서비스 외 별도 mongod도 확인돼 임의 프로세스 종료를 하지 않았다.

Stop-Service MongoDB는 require_escalated로 시도했지만 Windows가 “Cannot open MongoDB service”로 거부했다. 자동 승인 심사 거절이 아닌 OS 관리자 권한 부족이다. 서비스 중지·새 수업 서버 시작·복제 세트 초기화는 에이전트가 완료하지 않았다. 데이터를 삭제하거나 자격증명을 변경하지 않았다.

## 사용자 다음 순서

1. 관리자 PowerShell에서 Stop-Service MongoDB.
2. 별도로 실행한 기본 mongod 터미널이 있다면 Ctrl+C로 종료.
3. 일반 PowerShell에서 ad_server로 이동해 설치된 mongod.exe에 --config config/mongo-node1.yml을 지정하고 터미널 유지.
4. 다른 터미널에서 .venv 활성화 후 단일 멤버 replSetInitiate 실행. 이미 초기화했다면 상태 확인.
5. python tools/basics/day22_period01.py로 ping 확인.
6. 기존 Django shell을 종료하고 python ad_config/manage.py shell을 다시 열어 조회.
7. 조회가 None이면 연결은 해결됐으며 광고주 웹에서 캠페인을 저장.

