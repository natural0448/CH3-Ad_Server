# ad_config/ad_config/settings.py


BASE_DIR는 ad_config, WORKING_DIR는 ad_server다. WORKING_DIR를 sys.path에 추가한다. ads.env 다음 .env를 override=True로 읽는다. 실제 비밀값을 문서에 복사하지 않는다. 계정 SQLite는 WORKING_DIR/ads-auth.sqlite3에 유지한다. DEBUG=True, ALLOWED_HOSTS=localhost/127.0.0.1, 기본 Django 앱과 ads를 등록한다. 기본 middleware/template 설정을 유지한다. 쿠키는 ads_sessionid/ads_csrftoken, LOGIN_URL=/accounts/login/, LOGIN_REDIRECT_URL=/advertiser/campaigns/, LOGOUT_REDIRECT_URL=/accounts/login/이다. MEDIA_KEYS는 ADS_MEDIA_ID(기본 village-game)와 ADS_MEDIA_KEY에서 온다. MONGO_DB 기본 village_ads, ADS_BASE_URL 기본 http://127.0.0.1:8001이다.

## 변수·상수의 출처

BASE_DIR는 ad_config, WORKING_DIR는 ad_server다. WORKING_DIR를 sys.path에 추가한다. ads.env 다음 .env를 override=True로 읽는다. 실제 비밀값을 문서에 복사하지 않는다. 계정 SQLite는 WORKING_DIR/ads-auth.sqlite3에 유지한다. DEBUG=True, ALLOWED_HOSTS=localhost/127.0.0.1, 기본 Django 앱과 ads를 등록한다. 기본 middleware/template 설정을 유지한다. 쿠키는 ads_sessionid/ads_csrftoken, LOGIN_URL=/accounts/login/, LOGIN_REDIRECT_URL=/advertiser/campaigns/, LOGOUT_REDIRECT_URL=/accounts/login/이다. MEDIA_KEYS는 ADS_MEDIA_ID(기본 village-game)와 ADS_MEDIA_KEY에서 온다. MONGO_DB 기본 village_ads, ADS_BASE_URL 기본 http://127.0.0.1:8001이다.

SECRET_KEY는 ADS_SECRET_KEY, MONGO_URI는 MONGO_URI 환경변수에서 필수로 읽는다. 설정 파일은 DJANGO_SETTINGS_MODULE을 다시 쓰지 않는다. Django 기본 계정 검증기·템플릿 context processor·middleware·static 경로는 위 코드의 Django 기본 구성을 사용한다. LANGUAGE_CODE=en-us, TIME_ZONE=UTC, USE_I18N=True, USE_TZ=True, STATIC_URL=static/, DEFAULT_AUTO_FIELD=django.db.models.BigAutoField이다.
