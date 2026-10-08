# ad_config/ad_config/urls.py

단일 urlpatterns에서 admin, JSON 인증(csrf/api-login/api-logout), Django form 인증(login/logout), 루트 ads.urls include를 연결한다.

## 변수·상수의 출처

단일 urlpatterns에서 admin, JSON 인증(csrf/api-login/api-logout), Django form 인증(login/logout), 루트 ads.urls include를 연결한다.

지역 입력은 함수 인자/요청/CLI/환경 설정에서 오고 해당 함수가 작성한다. 연결은 공유 cache, 소유자는 Django 세션, ID/시간은 uuid4/UTC에서 생성한다. 테스트 값은 임시 계정/테스트 DB에서만 사용한다. secrets·password·cookie·token 실제 값은 문서에 복사하지 않는다.

## 22일차 이미지 광고 최종 반영

루트 GET을 기존 광고주 로그인으로 302 이동한다. 기존 admin/auth/광고주/매체 API include는 유지한다. urlpatterns의 home은 RedirectView(pattern_name="login", permanent=False)이며 로그인 후 기존 LOGIN_REDIRECT_URL이 캠페인으로 보낸다.
