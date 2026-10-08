# ads/media_auth.py

기존 read_media_body를 유지하면서 수정 교안의 두 매체 헤더와 공유 decorator를 연결했다. 본문 media_id와 X-Media-ID가 같고 settings.MEDIA_KEYS에서 읽은 서버 키와 X-Media-Key가 compare_digest로 같아야 한다. 키 실제 값은 문서/응답에 기록하지 않는다. subject_id는 비어 있지 않은 문자열이며 subject는 인증한 매체와 같아야 한다. decorator는 media_body·subject를 request에 부착하고 허용한 오류 코드만 공개한다. 인증401, 입력400, 저장소503, 메서드405; 서버간 매체 요청만 csrf_exempt다. 게임과 광고주 웹 CSRF는 유지한다.

직접 호출의 기대 계약: get_db는 기존 Database, find_one은 dict/None, find·sort·limit는 Cursor, update_one은 UpdateResult, insert_one은 InsertOneResult, create_index는 색인 이름이다. Django render/JsonResponse는 HttpResponse, JSON parse는 dict 등 JSON 값, urlopen은 응답 stream, patch/assert는 테스트 fixture/검증을 제공한다. 하위 계층 내부는 해당 짝 문서에 있다.

## `read_media_body(request)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| request | 없음 | Django HttpRequest; decorator가 로그인/메서드/CSRF 또는 매체 인증을 검사한다. |

반환·실패: (dict,subject dict); PermissionError 또는 ValueError/UnicodeDecodeError.

의사코드: content-type/JSON 객체 → media_id와 두 헤더 인증 → 동일 매체 subject 검사 → 본문과 공개 수신자 반환.

직접 호출: `PermissionError`, `ValueError`, `data.get`, `expected.encode`, `isinstance`, `json.loads`, `request.headers.get`, `secrets.compare_digest`, `settings.MEDIA_KEYS.get`, `subject.get`, `supplied.encode`.

## `media_api_methods(*methods)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| methods | 없음 | 허용 HTTP 메서드 문자열 varargs; 매체 API는 POST. |

반환·실패: view를 받는 decorate callable.

의사코드: 허용 HTTP 메서드를 closure로 저장 → decorator 반환.

직접 호출: .

## 상태·값 출처

지역 변수는 해당 함수가 소유하며 request/입력·서버 설정·DB 조회 또는 위 의사코드의 생성 단계에서 얻는다. 저장 snapshot과 receipt의 쓰기는 서비스/사건 계층이 맡는다. 테스트 연결·patch·가짜 응답은 해당 테스트 클래스만 소유하고 정리한다. 비밀값·쿠키·CSRF 토큰은 문서/증거에 복사하지 않는다.
