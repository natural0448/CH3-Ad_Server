# ads.env

기존 광고 서버의 로컬 환경 파일이며 KEY=VALUE 형식이다. PowerShell 명령 파일이 아니다. 함수·메서드는 없으며 실제 값을 문서에 복사하지 않는다.

ADS_SECRET_KEY·ADS_MEDIA_KEY는 로컬 비밀 설정이다. MONGO_URI는 현재 수업의 단일 멤버 복제 세트 연결 설정으로 변경했다. MONGO_DB는 로컬 광고 DB 선택값이다. 연결 설정 외 다른 키와 파일 바이트를 보존했다.

settings.py와 tools/basics/day22_period01.py·day22_period02.py가 루트 ads.env를 읽는다. 루트 .env가 있으면 나중에 읽어 우선 적용하며 검사 시 .env는 없었다. 파일 쓰기 소유자는 로컬 운영자이고 실행 코드는 이 파일을 수정하지 않는다.

Django 환경 로딩 및 단일 멤버·복제 옵션 파싱을 확인했다. 환경 파일 수정만으로 MongoDB의 복제 기능이 켜지지는 않는다. 실제 서버는 설치 기본 설정으로 실행 중이어서 접속 검사는 ServerSelectionTimeoutError다.

짝 문서/색인만 추가했으며 .gitignore의 ads.env 제외 규칙을 유지한다.
