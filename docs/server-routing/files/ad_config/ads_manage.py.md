# ad_config/ads_manage.py

함수 정의는 없다. 광고 Django 명령의 진입점이다.

- `Path(__file__).resolve().parent.parent`는 `ad_server`다. 사용자가 작성한 `sys.path.append(...)`가 이 경로를 추가해 루트의 `ads`를 찾게 한다.
- 스크립트 실행 시 `os.environ["DJANGO_SETTINGS_MODULE"]`을 `ad_config.settings`로 지정한다. 원래 스크립트 디렉터리에서 중첩 내부의 설정 패키지를 찾는다.
- `sys.argv`는 명령행 인자에서 온다. `execute_from_command_line(sys.argv)`가 명령을 실행하며 정상 명령은 프로세스 종료 코드 0, 오류는 명령에 따른 실패 코드다.
- 의사코드: 루트 검색 경로 추가 → Django 명령 함수 import → 직접 실행이면 설정 모듈 지정 → 입력 명령 실행.
- 직접 의존성: 표준 라이브러리 `os`, `sys`, `pathlib.Path`, Django `execute_from_command_line`. 앱이나 계정 DB를 직접 조회하지 않는다.
