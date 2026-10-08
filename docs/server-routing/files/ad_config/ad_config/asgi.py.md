# ad_config/ad_config/asgi.py

현재 Django ASGI 진입 모듈이다. 함수·클래스 정의는 없다. 모듈을 로드할 때 `os.environ.setdefault("DJANGO_SETTINGS_MODULE","ad_config.settings")`를 직접 호출해 미설정 환경에서 설정 모듈을 지정하고 `django.core.asgi.get_asgi_application()`을 호출한다.

`application`은 이 모듈이 초기화한 Django ASGI callable이다. 설정·Django 초기화 오류는 전파한다. 자체 광고 서비스 함수를 구현하지 않으며 광고 라우트는 설정의 URLConf가 연결한다. `setdefault`이므로 이미 지정된 환경값은 덮어쓰지 않는다.
