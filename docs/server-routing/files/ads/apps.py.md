# ads/apps.py

## class AdsConfig(AppConfig)

Django 광고 앱 설정 클래스다. 사용자 정의 메서드/함수와 직접 호출은 없다. 클래스가 소유하는 `name="ads"`는 앱 패키지 이름, `default_auto_field="django.db.models.BigAutoField"`는 Django ORM 모델의 기본 PK 필드 설정이다. 현재 `ads/models.py`에는 모델 정의가 없으며 이 설정 자체가 캠페인·사건을 ORM에 저장한다는 뜻은 아니다. 클래스의 생명주기는 Django 앱 레지스트리가 관리한다.
