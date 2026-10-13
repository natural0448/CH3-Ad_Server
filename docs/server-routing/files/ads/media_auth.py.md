# ads/media_auth.py

25일차 7교시와 기존 요청을 함께 인증한다. 매체 ID의 출처는 X-Media-ID 헤더이며 settings.MEDIA_KEYS에서 읽은 키를 X-Media-Key와 compare_digest로 대조한다. subject-only 조회를 허용하고, 선택/사건 요청에 기존 top-level media_id가 있으면 같은 인증 매체여야 한다. 본문/subject/헤더만으로 다른 매체의 권한을 만들지 않는다. 실제 키를 문서나 응답에 복사하지 않는다.

## read_media_body(request)

request는 기본값 없는 Django HttpRequest다. 반환은 `(본문 dict, 정리한 subject dict)`다. 의사코드: application/json·JSON 객체 검사 → 헤더 ID로 기대 키 조회 → 키 비교와 선택적 본문 media_id 대조 → subject 동일 매체·비어 있지 않은 subject_id 문자열 검사 → 반환. 직접 호출은 json.loads, request.headers.get, settings.MEDIA_KEYS.get, secrets.compare_digest다. 키/매체 인증 실패는 PermissionError, 형식/subject 실패는 ValueError 또는 UnicodeDecodeError다. DB·파일을 쓰지 않는다. 기존 본문 media_id가 없으면 인증 헤더가 기준이며, 있으면 불일치를 401로 유지한다.

## media_api_methods(*methods)

methods는 허용 메서드 문자열 varargs이고 현재 매체 API는 POST다. 반환은 decorate callable이다. 의사코드: methods closure를 저장 → decorate 반환. 이 계층에서 DB를 조회하지 않는다.

## media_api_methods.decorate(view)

view는 기본값 없는 Django view callable이며 반환은 csrf_exempt와 wraps(view)가 적용된 wrapped다. 직접 호출은 위 두 decorator다. 서버간 매체 요청만 csrf_exempt이며 게임·광고주 웹의 CSRF는 유지한다.

## media_api_methods.decorate.wrapped(request, *args, **kwargs)

request는 HttpRequest, args/kwargs는 원래 view에 전달할 인수다. 정상 반환은 원래 view의 HttpResponse다. 의사코드: 허용 메서드가 아니면 JSON method_not_allowed/405/Allow 헤더 → read_media_body → 검증 본문·subject를 request.media_body/request.subject에 부착 → view 호출 → PermissionError 401, 입력 오류 400, PyMongoError 503. 직접 호출은 read_media_body, view, JsonResponse와 ', '.join(methods)다.

입력 허용 오류 집합은 decision_snapshot_missing, decision_not_found_for_subject, impression_required, decision_id_required, event_type_invalid이며 다른 입력 오류는 invalid_event다. 저장소 오류는 ads_unavailable로 내부 문구를 숨긴다. methods/view는 closure, 본문/subject는 read_media_body, 각 응답은 wrapper가 소유한다. GET 405 JSON은 교안 관찰과 같고 키·수신자 검사는 DB 접근 전에 수행한다.
