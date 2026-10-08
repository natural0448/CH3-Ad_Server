# 2026-10-07 · 오늘 문서 등록과 교안 차이 검토

## 요청과 결과

오늘 작성·수정한 문서를 모두 라우팅에서 찾을 수 있게 등록하고, 교안을 따르지 않은 구현·안내가 있었는지 확인해 기록했다. [등록 목록](../server-routing/reviews/2026-10-07-document-registry.md)과 [교안 차이 검토](../server-routing/reviews/2026-10-07-lesson-deviations.md)를 각 프로젝트 라우팅 색인에 연결했다.

작업 시작 시 오늘 문서 후보는 102개였다. 작성 주체가 확실하지 않은 문서도 목록에는 포함하지만 제 작업으로 단정하지 않는다. 인수인계 원문을 보존하고 최신 교안과 다른 부분에 검토 주석을 추가했다. 현재 안내·짝 문서의 오래된 3교시 설명을 정정했고 누락된 Game-server README의 짝 문서를 추가했다.

## 시작 Git 상태와 기존 변경

Chapter3/ad_server: `Git 상태 확인 불가: 저장소 아님`. 상위 경계 조회는 권한 제한으로 확인 불가. 저장소를 초기화하지 않았다.

Game-server HEAD `6aa5329 22일차 - 진행사항 반영`, Game-client HEAD `2dd8d97 22일차 내용 반영`, 두 저장소 staged 없음. 게임 서버의 ad_gateway/ad_views/test_ads/urls 및 짝 문서·README 변경, 접속기의 application/network/ui/contracts/tests와 짝 문서·README 변경은 작업 시작 전에 존재한 변경이다.

전체 staged·unstaged·untracked 목록, 시작 문서 해시와 사본은 [start.json](../server-routing/verification/2026-10-07-document-review/start.json)과 before/에 있다. 기존 코드 변경을 이번 작업으로 주장하지 않는다. 코드·설정·환경 파일은 값 대신 SHA-256만 보존했다.

## 이번 문서 변경과 책임

- ad_server/README.md: 최신 3교시를 게임 서버 함수 작성으로 정정. 기존 기초 파일과 보조 통합 검사를 최신 평가와 구별.
- 세 프로젝트 라우팅 README: 오늘 문서 전체 등록 목록과 교안 차이 기록 연결, 오래된 3교시 설명 정정.
- ad_server의 README·기초 실습·보조 검증기 짝 문서와 Game-client의 README·광고 상태 짝 문서: 실제 현재 코드/문서에 맞게 설명 정정.
- Game-server/docs/server-routing/files/README.md.md: 기존 README의 누락된 짝 문서 추가 및 색인 등록.
- 오늘 기존 인수인계 16개: 본문 보존, 작업 시점/현재 교안 차이 검토 주석 추가.
- reviews/2026-10-07-document-registry.md, reviews/2026-10-07-lesson-deviations.md, 본 인수인계 및 verification/2026-10-07-document-review/: 등록·검토·검사 기록 추가.

상세 추가/수정 목록은 종료 시 changes.json에 기록한다. 파일 이동·삭제·실행 코드·설정 변경은 없다. 개발 파일의 기존 짝 문서는 유지하고, 인수인계/검토 문서는 경로로 직접 등록한다. 문서의 짝 문서를 반복 생성하는 구조는 사용하지 않는다.

## 핵심 발견

22일차 이미지/디자인 누락, 최신 3교시를 접속기 작업으로 오해한 범위, call_ads 전제를 건너뛴 이전 사건 함수, 잘못 안내한 게임 테스트 파일, 오래된 False/True 기초 실습, 원문 밖 타입 검사 등 추가 로직, 정규화 PASS의 표현 한계, 공식 검증의 미완료, 현재 안내/짝 문서의 잔여 오류를 구분해 기록했다. 실제 임의 추가와 사용자 조건에 따른 경로·스키마 보존을 동일하게 취급하지 않는다. 관련 코드의 자동 원복이나 추가 개발은 수행하지 않았다.

## 검사와 문서 정합화

현재 교안 소스 비교 명령:

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\python.exe -X utf8 -B tools/verify_lesson_alignment.py --output docs/server-routing/verification/2026-10-07-document-review/current-source-comparison.json
```

정규화 23개 PASS. 별도 원문 AST 비교에서는 14개 일치·8개 차이·템플릿 별도 비교 1개였다. 최신 request_ad_event는 원문 AST와 동일하며 이전 False/True 실습은 최신 초급 예제와 다르다. 상세는 raw-source-comparison.json에 기록했다.

시작 라우팅 감사는 Game-server 변경 Python 4개/21 symbols, Game-client 변경 Python 14개/117 symbols에서 PASS였다. 광고 서버의 전체 42개 Python 검사에는 기존 8개 짝/색인 누락이 있었다. 이번 등록 대상 짝 문서에 해당하지 않는 기존 scaffold 누락으로 기록했고 관련 없는 문서를 일괄 생성하지 않았다. 최종 scoped 검사·링크·등록 누락 검사는 final-verification.json에 기록한다.

본 요청에서는 기능 코드가 바뀌지 않아 이전 기능 테스트를 반복하지 않았다. 현재 검사 결과를 과거 20/24/37/57개 기능 검사 결과와 구별한다. 공식 교안 검증 파일은 로그인 다운로드 제한으로 미실행이며 실제 학생 창 관찰도 이번 문서 검사로 대신하지 않는다.

검사 후 별도의 최종 문서 정합화 단계에서 변경한 문서·색인·짝 경로를 재확인했다. 전체 변경 목록·등록 수·소스 해시 보존·Git 최종 상태는 verification 폴더의 종료 기록에 있다.

## 다음 읽기 순서

각 프로젝트의 docs/server-routing/README.md 또는 docs/client-routing/README.md → 오늘 문서 전체 등록 목록 → 교안 차이 검토의 D01~D09 → 해당 코드 짝 문서와 과거 인수인계 순서로 읽는다. 이 문서 검토 요청을 위해 사용자가 실행할 별도 명령은 없다. 공식 3교시 검증은 로그인한 교안에서 원본을 받는 후속 단계로 남아 있다.

## 최종 확인 결과

문서 106개와 JSON 근거 72개를 등록했다. 등록 누락·깨진 등록 링크 0건, 광고 서버 오늘 등록 범위 Python 33개/105 symbols PASS, 게임 서버 4개/21 symbols PASS, 접속기 14개/117 symbols PASS, 접속기 전체 77파일/77짝 검사 PASS, 두 Git 저장소 diff --check PASS다. 소스·설정 235개 해시가 시작과 같고 새 staged 변경·커밋은 없다. 기존 범위 밖 scaffold 8개의 짝 문서 누락은 별도 기록으로 남긴다.

이번 요청의 문서 추가/수정은 총 29개이며 상세 경로·해시는 changes.json에 기록했다. 기능 테스트는 문서 변경만 있어 반복하지 않았다. 공식 3교시 검증 파일 미실행 상태를 변경하지 않았다.
