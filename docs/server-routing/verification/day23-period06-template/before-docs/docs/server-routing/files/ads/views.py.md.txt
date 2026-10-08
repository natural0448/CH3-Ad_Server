# ads/views.py

광고주 캠페인/입찰 폼과 매체 API를 담당하는 기존 combined views 모듈이다. 수정 교안 views.event는 현재 event_view, web_views.event_view는 advertiser_event_view로 연결하여 이름 충돌을 막았다. 기존 이미지 편집과 로그인·CSRF는 유지한다. 새 광고주 목록은 request.user.pk의 owner_user_id 결정만 selected_at 내림차순으로30개 조회하고 결정별 최초 노출·클릭 문서를 찾는다. 목록 조회는 write를 하지 않는다. 매체 API는 media_api_methods로 두 헤더를 인증하고, 성공 이벤트는 no-store다. 빈 결정 응답도 policy_version을 사용한다. CREATIVES는 creatives.py의 서버 소재 선택지다.

직접 호출의 기대 계약: get_db는 기존 Database, find_one은 dict/None, find·sort·limit는 Cursor, update_one은 UpdateResult, insert_one은 InsertOneResult, create_index는 색인 이름이다. Django render/JsonResponse는 HttpResponse, JSON parse는 dict 등 JSON 값, urlopen은 응답 stream, patch/assert는 테스트 fixture/검증을 제공한다. 하위 계층 내부는 해당 짝 문서에 있다.

## `campaign_view(request)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| request | 없음 | Django HttpRequest; decorator가 로그인/메서드/CSRF 또는 매체 인증을 검사한다. |

반환·실패: HTML200/400/503; 미로그인302; 다른 메서드405.

의사코드: POST면 캠페인 저장 → 자기 목록 → edit를 목록 내 탐색/실패 입력 복원 → 기존 소재 폼 render.

직접 호출: `list_campaigns`, `next`, `render`, `request.GET.get`, `request.POST.get`, `require_http_methods`, `save_campaign`, `str`.

Decorator: `login_required`, `require_http_methods(['GET', 'POST'])`.

## `bid_view(request)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| request | 없음 | Django HttpRequest; decorator가 로그인/메서드/CSRF 또는 매체 인증을 검사한다. |

반환·실패: HTML200/400/503; 미로그인302; 다른 메서드405.

의사코드: POST면 현재 입찰 저장 → 자기 입찰 목록 → render.

직접 호출: `list_bids`, `render`, `request.POST.get`, `require_http_methods`, `save_bid`, `str`.

Decorator: `login_required`, `require_http_methods(['GET', 'POST'])`.

## `decision_view(request)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| request | 없음 | Django HttpRequest; decorator가 로그인/메서드/CSRF 또는 매체 인증을 검사한다. |

반환·실패: JSON200,입력400,저장소503; decorator 인증401/메서드405.

의사코드: decorator의 본문·수신자 사용 → 기존4인수 choose_ad → 빈 광고/공개 이미지·문구 응답.

직접 호출: `JsonResponse`, `choose_ad`, `decision['creative'].get`, `media_api_methods`, `payload.get`, `subject.get`.

Decorator: `media_api_methods('POST')`.

## `event_view(request)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| request | 없음 | Django HttpRequest; decorator가 로그인/메서드/CSRF 또는 매체 인증을 검사한다. |

반환·실패: JsonResponse200; 오류는 media_api_methods 처리.

의사코드: decorator의 subject/본문 → record_ad_event → receipt JSON → Cache-Control=no-store.

직접 호출: `JsonResponse`, `media_api_methods`, `record_ad_event`, `request.media_body.get`.

Decorator: `media_api_methods('POST')`.

## `advertiser_event_view(request)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| request | 없음 | Django HttpRequest; decorator가 로그인/메서드/CSRF 또는 매체 인증을 검사한다. |

반환·실패: HTML200/503; 미로그인302; POST405.

의사코드: 로그인 GET → owner_user_id 필터/selected_at 역순/limit30 → 결정별 최초 사건 조회 → rows HTML; 저장소 장애는 message HTML.

직접 호출: `bool`, `decision.get`, `get_db`, `get_db().ad_events.find_one`, `get_db().decisions.find`, `get_db().decisions.find({'owner_user_id': request.user.pk}).sort`, `get_db().decisions.find({'owner_user_id': request.user.pk}).sort('selected_at', -1).limit`, `list`, `login_required`, `render`, `require_http_methods`, `rows.append`.

Decorator: `login_required(login_url='/accounts/login/')`, `require_http_methods(['GET'])`.

## 상태·값 출처

지역 변수는 해당 함수가 소유하며 request/입력·서버 설정·DB 조회 또는 위 의사코드의 생성 단계에서 얻는다. 저장 snapshot과 receipt의 쓰기는 서비스/사건 계층이 맡는다. 테스트 연결·patch·가짜 응답은 해당 테스트 클래스만 소유하고 정리한다. 비밀값·쿠키·CSRF 토큰은 문서/증거에 복사하지 않는다.
