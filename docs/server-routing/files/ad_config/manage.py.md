# ad_config/manage.py

main()은 ad_config.settings를 명시 지정하고 sys.argv를 Django CLI에 전달한다. 함수 인자는 없으며 정상 반환은 None, Django import 실패는 ImportError다.

## main()

파라미터 없음.

반환·실패: None. assertion/외부 오류 발생 시 실패..

의사코드: main()은 ad_config.settings를 명시 지정하고 sys.argv를 Django CLI에 전달한다. 함수 인자는 없으며 정상 반환은 None, Django import 실패는 ImportError다.

직접 호출: ImportError, execute_from_command_line. execute_from_command_line은 Django 명령을 디스패치하며 실행 오류를 호출자에 전파한다. 환경 모듈 이름은 진입점에서 광고 설정으로 지정한다.

## 변수·상수의 출처

main()은 ad_config.settings를 명시 지정하고 sys.argv를 Django CLI에 전달한다. 함수 인자는 없으며 정상 반환은 None, Django import 실패는 ImportError다.

지역 입력은 함수 인자/요청/CLI/환경 설정에서 오고 해당 함수가 작성한다. 연결은 공유 cache, 소유자는 Django 세션, ID/시간은 uuid4/UTC에서 생성한다. 테스트 값은 임시 계정/테스트 DB에서만 사용한다. secrets·password·cookie·token 실제 값은 문서에 복사하지 않는다.
