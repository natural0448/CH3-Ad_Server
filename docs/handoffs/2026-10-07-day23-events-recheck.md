# 2026-10-07 · 23일차 사건 파일 재점검

> 2026-10-07 검토 주석: 이 문서의 clean_subject 제거는 당시 수정 이력입니다. 현재는 실제 services.clean_subject를 사용하는 후속 구현이며 아래 본문을 현재 구조로 읽지 않습니다. [차이와 현재 상태](../server-routing/reviews/2026-10-07-lesson-deviations.md).

## 요청·결과

사용자가 2교시 저장 여부와 events.py 내용 차이를 질문했다. 정확한 경로는 ad_server/ads/events.py이며 root events.py는 없다. 원본 HTML 재열람 결과 events는1교시 저장 함수,2교시는 media_auth/event_view/URL 및 게임·접속기 호출 연결이다. 현재 events 파일이 직전 검증 기록의 해시와 다르고 존재하지 않는 ads.services.clean_subject import가 있어 Django check ImportError를 재현했다. 해당 의존성만 교안의 내부 입력 검사로 바꾸고 비문자열 사건 종류를 ValueError로 처리했다.

## 시작 Git·기존 변경

Chapter3/ad_server: Git 상태 확인 불가: 저장소 아님. source SHA256와 재점검 직전 원본은 docs/server-routing/verification/day23-events-recheck/start.json 및 before-fix.txt에 보존했다. 작성자를 추정하지 않고 작업 시작 전에 존재한 변경으로 취급했다. Game-server HEAD6aa5329, Game-client HEAD2dd8d97, staged 없음. 두 게임 프로젝트의 기존23일차 코드/문서 unstaged 및 untracked는 앞 작업에서 존재한 상태이며 이번에는 수정하지 않았다. 최종 정확한 목록은 verification/day23-events-recheck/git-final.json이다. 과거 day23-changes.json은 이전 실행의 기록으로 보존했다.

## 이번 변경 파일·설계

- ads/events.py: 없는 clean_subject import·호출 제거, 교안 subject 검사·복사, event_type 문자열 검사 추가.
- docs/server-routing/files/ads/events.py.md: 작업 시작 전 실제 코드부터 정합화 후 검증 완료한 최종 코드로 재작성.
- docs/server-routing/README.md: 기존 짝 문서 색인 유지 및 재점검 설명 추가.
- docs/server-routing/verification/day23-events-recheck/: 원본·AST/테스트·Git·통합 증거 추가.
- 이 인수인계 문서 추가. 개발 파일 추가·이동·삭제 없음.

기존 dotted subject 조회는 Mongo 내장 문서의 필드 순서에 의존하지 않으며 유지했다. candidates/선택 후보·광고주·금액 snapshot 검사도 유지했다. 기존 최초 저장·노출 선행 클릭·당시 입찰·UTC contract는 같다. 환경/비밀값 및 실수업 DB 사건은 변경하지 않았다.

## 검증·최종 문서

`python ad_config/manage.py check`: 재점검 전 ImportError, 수정 후 오류0. `python tools/verify_day22.py --mongod "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe"`: 광고31개 통과, skip0. `python tools/verify_day23.py --mongod "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe"`: 별도 Mongo/SQLite·HTTP·SDL dummy 두 슬롯 노출/모의클릭/재전송/당시금액 검증 통과. 실제8000/8001 사건경로 GET405 확인. 광고 서버 autoreload로 수정이 반영됐다. 한 개발 파일의 최종 AST·짝 문서·색인은 final.json에서 ok=true다.

코드 검증 후 별도 최종 문서 정합화 단계를 완료했다. 다른 프로젝트 검사는 이번에 코드를 변경하지 않아 반복 실행하지 않았다. 새 단위 테스트 파일은 추가하지 않았고 기존 잘못된 종류/수신자/중복 검사가 이번 수정을 검증한다. 실제 학생 클릭 관찰은 not_run이다.

## 다음 확인

광고 서버 가상환경에서 `python ad_config/manage.py check`로 로딩을 확인하고 정확한 ads/events.py 경로를 연다. 2교시 API는 ads/views.py의 event_view와 ads/urls.py의 api/media/events/다. 기존 Pygame 접속기의 실제 광고 표시·클릭 확인은 계속 수업 계정에서 진행한다. 코드 내용은 교안과 완전한 문자 복사본이 아니며 현재 폴더 구조와 오류 처리에 맞춘 구현이다.
