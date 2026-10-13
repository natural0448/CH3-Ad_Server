# ads/media_urls.py

25일차 매체 API의 유일한 URL 목록이다. ad_config/ad_config/urls.py가 api/media/ 접두사로 include한다. 현재 combined views 이름에 맞춰 callable을 연결했고 광고주 웹 경로는 ads.urls에 유지한다.

`app_name = 'media_ads'`. urlpatterns는 이 모듈이 소유한 URLPattern 목록이며 함수는 없다. 직접 호출 django.urls.path의 결과를 Django resolver가 읽는다.

| 선언 경로 | 직접 callable | name/namespace |
|---|---|---|
| decision/ | views.decision_view | media_ads:decision |
| events/ | views.event_view | media_ads:events |
| context/ | views.context_view | media_ads:context |

공개 URL은 /api/media/decision/, /api/media/events/, /api/media/context/다. 메서드·매체 인증·공개 응답 책임은 각 view와 media_auth에 있다. 이름이 다른 views.decision/views.event를 새로 만들지 않았다. 원래 ads.urls의 중복 매체 경로는 제거했고 공개 주소는 보존했다.
