# ads/auth_views.py

광고 계정 JSON 인증과 Django CSRF/session. JSON 오류 invalid_json, 필드 오류 missing_credentials, 인증 실패 authenticated=false/401이다. 실제 비밀번호/키를 응답이나 문서에 기록하지 않는다.

## csrf_token(request)

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| request | 없음 | Django HttpRequest. HTTP 메서드·인증·본문 제한은 파일 책임과 의사코드 참고. |

데코레이터: require_GET, ensure_csrf_cookie.

반환·실패: JsonResponse 200 또는 메서드405.

의사코드: GET → get_token → csrfToken JSON과 cookie.

직접 호출: JsonResponse, get_token. get_token은 CSRF 문자열을 반환하고 JsonResponse는 HTTP 응답을 만든다. authenticate는 User/None을 반환하며 Django login/logout은 요청 세션을 갱신한다. json.loads는 Python 객체 또는 JSONDecodeError다.

## read_credentials(request)

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| request | 없음 | Django HttpRequest. HTTP 메서드·인증·본문 제한은 파일 책임과 의사코드 참고. |

데코레이터: sensitive_variables('body', 'password', 'credentials').

반환·실패: 자격 dict 또는 ValueError.

의사코드: JSON 타입·객체·자격 필드 검사 → username trim → 자격 사전, 오류는 ValueError.

직접 호출: ValueError, body.get, isinstance, json.loads, sensitive_variables, username.strip. get_token은 CSRF 문자열을 반환하고 JsonResponse는 HTTP 응답을 만든다. authenticate는 User/None을 반환하며 Django login/logout은 요청 세션을 갱신한다. json.loads는 Python 객체 또는 JSONDecodeError다.

## login_view(request)

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| request | 없음 | Django HttpRequest. HTTP 메서드·인증·본문 제한은 파일 책임과 의사코드 참고. |

데코레이터: require_POST, sensitive_variables('credentials').

반환·실패: JsonResponse 200/400/401.

의사코드: read_credentials → authenticate → 실패401 또는 login → JSON.

직접 호출: JsonResponse, authenticate, login, read_credentials, sensitive_variables, str. get_token은 CSRF 문자열을 반환하고 JsonResponse는 HTTP 응답을 만든다. authenticate는 User/None을 반환하며 Django login/logout은 요청 세션을 갱신한다. json.loads는 Python 객체 또는 JSONDecodeError다.

## logout_view(request)

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| request | 없음 | Django HttpRequest. HTTP 메서드·인증·본문 제한은 파일 책임과 의사코드 참고. |

데코레이터: require_POST.

반환·실패: JsonResponse 200.

의사코드: POST → logout → authenticated=false.

직접 호출: JsonResponse, logout. get_token은 CSRF 문자열을 반환하고 JsonResponse는 HTTP 응답을 만든다. authenticate는 User/None을 반환하며 Django login/logout은 요청 세션을 갱신한다. json.loads는 Python 객체 또는 JSONDecodeError다.

## 변수·상수의 출처

광고 계정 JSON 인증과 Django CSRF/session. JSON 오류 invalid_json, 필드 오류 missing_credentials, 인증 실패 authenticated=false/401이다. 실제 비밀번호/키를 응답이나 문서에 기록하지 않는다.

지역 입력은 함수 인자/요청/CLI/환경 설정에서 오고 해당 함수가 작성한다. 연결은 공유 cache, 소유자는 Django 세션, ID/시간은 uuid4/UTC에서 생성한다. 테스트 값은 임시 계정/테스트 DB에서만 사용한다. secrets·password·cookie·token 실제 값은 문서에 복사하지 않는다.
