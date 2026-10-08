# 2026-10-07 · 교안과 실제 작업의 차이 검토

## 판정 기준과 범위

오늘의 광고 수업 작업에는 교안을 잘못 해석한 안내, 원문 밖의 추가 로직, 교안과 다른 파일 대응, 공식 검증의 미완료가 있었다. 이 문서는 이를 기록한다. 파일 구조·기존 환경을 유지하라는 사용자 조건에 따른 경로 변경과 교안 이탈을 구별한다. 검사 통과를 원문 코드 전체 일치로 취급하지 않는다.

현재 Desktop의 22일차 수정 HTML과 최신 23일차 HTML, 오늘의 인수인계 16개, 변경 목록·시작 사본·검증 JSON, 현재 소스와 라우팅 문서를 대조했다. 문서 102개가 작업 시작 시 오늘 생성·수정 후보로 수집됐다. 생성 시각·수정 시각·파일명 날짜는 작성자를 증명하지 않으므로 모든 후보를 제가 작성했다고 주장하지 않는다. 에이전트 변경의 근거가 있는 경우에만 해당 작업 기록과 연결한다.

기준 원문은 [22일차 교안](</C:/Users/이해나/Desktop/22일차 · 광고 플랫폼이 광고주의 광고를 게임 유저에게 집행한다.html>)과 [최신 23일차 교안](</C:/Users/이해나/Desktop/현재 ad_server에서 노출·클릭과 광고주 보고서 완성하기.html>)이다. 22일차 SHA-256은 `f0b7376bb7fc121aed7e3147ed1470cc8ffc90c9e8ce1c550b4847210ca13a67`, 현재 23일차는 `e71c2dac0b38748b171c5691de46b64fe361dd8682a8d5303ad13176aa004e0f`다. 이전 정합화 검사의 23일차 원문 해시는 `84f8c80719698631c66999b5e7ed4eb7ac250ad3983cf4bd4bc9a5adc4a79887`로 다르다. 당시 기록은 당시 원문에 대한 결과다.

## 확인된 이탈과 누락

| ID | 판정 | 실제 작업과 교안의 차이 | 현재 상태·근거 |
|---|---|---|---|
| D01 | 22일차 기능 누락 | 처음 광고 서버 동기화는 텍스트 캠페인·입찰에 집중했고, 이미지 소재 선택·디자인·미리보기·게임 표시가 빠졌다. 이미지 흐름을 유지하라는 수정 교안 전체를 충족한 상태가 아니었다. | 후속 요청에서 보완했다. [초기 동기화](../../handoffs/2026-10-07-day22-ad-server-sync.md), [이미지 보완](../../handoffs/2026-10-07-day22-image-serving-completion.md). 실제 학생 창 관찰은 별도 미실행 기록이다. |
| D02 | 3교시 범위 오해 | 최신 교안의 직접 구현 대상은 게임 `request_ad_event()` 본문 세 구간이다. 제가 접속기 계층 대응·재시도·표시 유지 등을 3교시 핵심 작업으로 안내하고 적용했다. 최신 교안에서는 Pygame 연결은 별도 자료다. | 안내를 정정했다. 해당 접속기 기능과 테스트는 현재 코드에 남아 있으며 이번 문서 작업에서 되돌리지 않았다. [접속기 작업 기록](</C:/MLO01-01/Chapter3/Game-client/docs/handoffs/2026-10-07-day23-period03-current-structure.md>), [현재 함수 작업](</C:/MLO01-01/Chapter3/Game-server/docs/handoffs/2026-10-07-day23-request-ad-event-lesson.md>). 별도 연결 자료 원문 전체와의 일치는 확인하지 못했다. |
| D03 | 교안의 함수 구조를 따르지 않은 구현 | 앞선 `request_ad_event()`는 payload·`call_ads()`·status/data 검증 대신 직접 Request/urlopen과 독자적인 오류 처리를 사용했다. 교안의 세 빈칸 구조와 달랐고 전제인 call_ads도 없었다. | 현재 본문은 최신 완성 코드와 AST가 동일하다. [변경 전 사본](</C:/MLO01-01/Chapter3/Game-server/docs/server-routing/verification/day23-request-ad-event/before/server/game/ad_gateway.py.txt>), [현재 대조](../verification/2026-10-07-document-review/raw-source-comparison.json). call_ads는 뒤늦게 보충했다. |
| D04 | 잘못된 파일·검사 안내 | 3교시 위치 질문에 `game/test_day23_ad_events.py`를 새로 맞추겠다고 안내했다. 최신 교안의 직접 수정 대상은 ad_gateway의 함수이고 검증 진입점은 `config/check_day23_period3.py`다. | 잘못 안내한 새 게임 테스트 파일은 실제로 생성하지 않았다. [그때의 시작 기록](</C:/MLO01-01/Chapter3/Game-server/docs/server-routing/verification/day23-game-file/start.json>)에는 해당 파일이 없다고 기록돼 있다. 공식 검증 파일도 아직 없다. |
| D05 | 오래된 실습을 최신 교안으로 표기 | `ad_server/config/day23-period-03.py`는 displayed/impression_ok를 사용해 False, True를 출력한다. 최신 3교시 초급 예제는 reply의 두 반환값을 받아 True, None을 출력한다. | 기존 코드 파일은 보존했다. 짝 문서와 현재 실행 안내에서 이전 교안 실습으로 표시했다. [현재 파일](../../../config/day23-period-03.py), [원문 대조](../verification/2026-10-07-document-review/raw-source-comparison.json). |
| D06 | 원문 밖의 추가 로직 | ads/events.py의 event_type 문자열 검사를 원문에 추가했다. choose_ad에도 입력 타입 검사·deepcopy·소재 기본값 처리 등이 포함된다. 파일 구조를 유지하는 것과 별개의 로직 변경이며 원문 그대로라고 부를 수 없다. | 추가·유지된 보호/호환 로직으로 명시한다. 일부 선택 스냅샷 변경은 23일차가 요구하는 후속 수정이다. [정규화 규칙](../../../tools/verify_lesson_alignment.py), [대조 결과](../verification/2026-10-07-document-review/raw-source-comparison.json). 이번에는 코드를 변경하지 않았다. |
| D07 | 검증 결과 표현의 한계 | 기존 23개 비교는 함수명·환경 로딩·타입 검사 등 기대 코드를 변경한 뒤 대조한 결과다. 'PASS'를 원문과 무수정 동일하다는 증거로 사용하는 것은 잘못이다. | 오늘 다시 검사해 정규화 23개 PASS, 원문 AST 그대로 일치 14개·차이 8개·템플릿 별도 비교 1개를 기록했다. 이 8개를 모두 임의 변경으로 판정하지 않는다. 아래 분류를 따른다. |
| D08 | 공식 검증 미완료·검증 방법 차이 | 공식 검증 파일을 받지 못해 기존 게임 테스트와 자체 계약 검사 24개를 실행했다. 교안은 실제 파일의 Player 값을 잠깐 999로 바꿨다가 복원하도록 안내하지만, 저는 메모리 함수 복사본에서 대상 변경을 검사했다. | 공식 검증의 실행 결과로 대체하지 않는다. [계약 검사](../verification/day23-period03/test-results.json)는 접속기 보조 검사이며, 게임 함수의 독립 계약 검사는 [별도 기록](</C:/MLO01-01/Chapter3/Game-server/docs/server-routing/verification/day23-request-ad-event/contract-checks.json>)이다. 공식 파일 다운로드는 로그인 페이지로 이동했다. |
| D09 | 문서 정합화 누락·현재 설명의 오류 | 광고 README·라우팅 색인과 일부 짝 문서에 '3교시=접속기', 'False/True가 최신 교안 그대로'라는 표현이 남았다. Game-client README를 정정한 뒤에도 짝 문서는 그 이전 설명이었다. Game-server README의 짝 문서도 없었다. | 이번 작업에서 현재 안내·짝 문서·색인을 정정하고 서버 README의 짝 문서를 추가했다. 이전 인수인계 본문은 이력으로 보존하고 검토 주석을 추가했다. |

## 원문 AST 차이 8개의 분류

| 파일·함수 | 차이의 성격 | 현재 판정 |
|---|---|---|
| ads/repository.py::save_bid | 22일차 원문에 반환이 없고 23일차 1교시에서 저장 문서를 반환하도록 변경 | 교안의 후속 수정. 임의 기능 추가로 판정하지 않는다. |
| ads/events.py::record_ad_event | 비문자열 event_type 검사 추가 | 원문 밖 추가 로직. D06. |
| ads/views.py::event_view | 원문의 event를 기존 함수 이름에 연결 | 기존 combined views와 URL 이름 유지에 따른 변경. |
| ads/views.py::advertiser_event_view | 광고주 GET 함수를 별도 이름으로 연결 | 기존 매체 handler와의 이름 충돌 방지. 구조 보존에 따른 변경. |
| ads/services.py::choose_ad | 새 owner/selected_at snapshot과 기존 4인수·bid_amount·소재·입력 검사 유지 | 교안 후속 수정, 기존 스키마 유지, 원문 밖 보호 로직이 혼재. 완전 복사본으로 주장하지 않는다. |
| tools/day22_connection.py | 실제 환경 파일 경로와 DB 설정 기본값 사용 | 현재 환경 보존에 따른 변경. |
| tools/day22_crud.py | 실제 환경 파일 경로와 DB 설정 기본값 사용 | 현재 환경 보존에 따른 변경. |
| tools/basics/day22_credit_model.py | 예제를 기존 main 진입점 안에 배치 | 실행 구조 보존에 따른 변경. |

템플릿은 기존 base/menu에 연결하고 아직 구현하지 않은 보고서 링크를 생략한 상태에서 본문 표를 비교했다. 전체 HTML의 무수정 일치 검사가 아니다.

## 사용자 조건에 따른 구조 변경과 확인 한계

- 중첩 `ad_config/ad_config`, 루트 ads, 기존 manage 호환 진입점, 게임의 `server/game`, 접속기의 contracts/application/network/ui 구조는 사용자 요청대로 유지했다. 교안의 평면 파일명을 그대로 복사하지 않은 이유를 경로·함수 대응으로 기록한다.
- 기존 계정 DB·매체 키·게임 설정을 유지한 것은 교안 이탈로 판정하지 않는다. 앞선 매체 키 복사·저장은 사용자의 명시 승인 기록이 있다. 실제 값은 이 문서에 기록하지 않는다.
- 현재 call_ads의 HTTPError 처리 구간은 23일차 2교시 diff를 따른다. 누락돼 있던 전체 helper의 JSON POST 조립은 교안의 계약에 맞춰 보충한 구현이다. helper 전체의 정본 파일을 확보해 무수정 동일성을 검사한 것은 아니다.
- 광고 폼 디자인과 소재 연결은 후속 사용자 요청에 따라 구현했다. 기존 Kenney PNG 재사용 기록은 있으나 교안의 원본 이미지·디자인과 픽셀/스타일이 동일하다고 검증하지 않았다.
- ads/events.py 재점검 때 존재하지 않는 clean_subject import로 ImportError가 있었고 내부 검사로 바꿨다가 후속 정합화에서 실제 helper를 연결했다. [당시 기록](../../handoffs/2026-10-07-day23-events-recheck.md)을 보존한다. 비 Git 파일의 당시 작성자가 확실하지 않아 최초 잘못된 import의 작성자를 단정하지 않는다.
- 이전 31/37/50/57개 테스트 수와 별도 13/20개 게임 검사 수는 서로 다른 시점·범위의 결과다. 오늘 기능 검사를 다시 실행한 것으로 표기하지 않는다. 기능 테스트 통과는 공식 검증·원문 전체 일치·실제 학생 화면 관찰을 보증하지 않는다.

## 문서 등록과 검사 범위

오늘 문서는 [전체 등록 목록](2026-10-07-document-registry.md)으로 각 프로젝트 라우팅 색인에 연결했다. 개발 파일의 1:1 짝 문서는 기존 위치를 사용하고, 인수인계와 검토 문서는 문서 경로로 직접 등록한다. 문서 자체에 다시 짝 문서를 만드는 무한 중첩 구조는 만들지 않는다. 새 검토 문서와 본 작업 인수인계도 목록에 포함한다.

Git 기반 시작 감사: Game-server 변경 Python 4개·시그니처 21개 PASS, Game-client 변경 Python 14개·시그니처 117개 PASS. 이는 교안 준수 검사가 아니라 문서 시그니처·색인 검사다.

광고 서버의 넓은 전체 검사에서는 Python 42개 중 기존 8개에 짝 문서·색인 누락이 발견됐다: ads/admin.py, apps.py, models.py, __init__.py, migrations/__init__.py, ad_config/ad_config/asgi.py, wsgi.py, __init__.py. 이 파일들은 오늘 등록할 문서 후보 목록에 해당 짝 문서가 없으며 이번 개발 변경 대상도 아니다. 관련 없는 문서를 일괄 생성하지 않고 범위 밖 기존 누락으로 기록했다. 기존 scoped PASS를 전체 42개 완전 문서화로 확대하지 않는다. [넓은 검사](../verification/2026-10-07-document-review/ad-server-start-audit.json)를 따른다.

이번 변경은 문서·색인·검토 기록이다. 소스/설정 235개 시작 해시를 보존했고 종료 시 실제 코드·환경 파일이 그대로임을 확인했다. 최종 문서 등록·링크·짝 문서 검사 결과와 Git 변경 구분은 [본 작업 인수인계](../../handoffs/2026-10-07-document-registration-and-lesson-review.md)에 기록한다.

최종 등록 검사: 문서 106개·JSON 근거 72개, 등록 누락/깨진 등록 링크 0건. 등록된 Python 문서와 색인·시그니처 검사, 접속기 77개 파일의 짝 검사, 두 저장소 diff --check가 통과했다. 기능 코드는 이번에 변경하지 않았다. [최종 결과](../verification/2026-10-07-document-review/final-verification.json)를 따른다.
