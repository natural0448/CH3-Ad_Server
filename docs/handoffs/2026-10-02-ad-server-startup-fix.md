# 광고 Django 서버 시작 오류 수정

## 요청과 완료 결과

2026-10-02, 사용자가 반복되는 `runserver` 오류를 직접 수정하도록 요청했다. 현재 중첩 구조와 명령 `python ad_config/ads_manage.py ...`를 유지하고 독립 광고 인증을 완성했다. Django check, 인증 회귀 테스트 6개, 마이그레이션, 실제 8001 포트 HTTP 응답을 검증했다. 검증용 서버는 검증 후 종료했다.

## 작업 시작 전 상태

- 대상 `C:/MLO01-01/Chapter3/ad_server`, 상위 Chapter3/MLO01-01은 저장소가 아니다: **Git 상태 확인 불가: 저장소 아님**. 직전 커밋과 staged/unstaged/untracked 분류는 적용할 수 없으며 Git 초기화를 하지 않았다.
- 기존 사용자 파일은 모두 보존 대상으로 읽었다. 진입점의 루트 검색 경로 추가, 세 단계 `BASE_DIR`, 환경 파일의 광고 필수 키 작성은 작업 시작 전에 존재한 사용자 변경이다.
- `ads/auth_views.py`가 없었고 URL 목록은 두 번 대입되며 `admin` import가 없었다. `INSTALLED_APPS`에 광고 앱이 없었다. 테스트 파일에는 생성된 import/주석만 있었다.
- 초기 Django check는 `ImportError: cannot import name 'auth_views' from 'ads'`로 실패했다.
- 루트와 진입점 폴더에 기존 SQLite DB가 없음을 확인한 뒤 광고 전용 DB를 준비했다.
- 인접 Game-server의 기존 파일 재배치는 이 작업 범위 밖이며 손대지 않았다. Git 메타데이터나 환경 파일의 비밀값을 복사하지 않았다.

## 이번 변경 파일

수정:

- `ad_config/ad_config/settings.py`: 기존 환경 키를 SECRET_KEY로 사용, 로컬 호스트 허용, `ads` 등록, 광고 계정 SQLite 경로를 `BASE_DIR / "ads-auth.sqlite3"`로 지정.
- `ad_config/ad_config/urls.py`: admin import와 인증 URL을 하나의 목록으로 통합.
- `ads/tests.py`: 임시 테스트 DB와 CSRF 강제 client로 인증 회귀 테스트 6개 추가.

추가:

- `ads/auth_views.py`: JSON CSRF/로그인/로그아웃 함수와 자격 입력 검증 helper. 게임의 기존 JSON 인증 계약을 참고했으며 게임 모듈을 import하지 않는다.
- `docs/server-routing/README.md`와 `files/`의 짝 문서 5개: 진입점, 설정, URL, 인증, 테스트.
- 이 인수인계 문서.
- `ads-auth.sqlite3`: migrate로 생성된 로컬 실행 데이터. 사용자/비밀번호를 생성하지 않고 Django 기본 인증·세션 테이블만 준비했다.

파일 이동·삭제는 없다. 사용자 진입점, requirements, 환경 파일, 가상환경, 다른 기존 Python 파일은 수정하지 않았다. SECRET_KEY의 이전 코드 내 실제 값과 환경 파일 내용은 diff/문서에 복사하지 않았다. 설정 수정은 AST로 대입 위치를 찾아 적용했다.

## 책임과 설계

- 사용자의 현재 구조에서 `ad_config/ads_manage.py`가 루트 `ads`를 찾도록 한 검색 경로를 그대로 사용한다. 내부 설정 패키지 경로 `ad_config.settings`도 유지한다.
- 광고 로그인은 광고 프로젝트의 별도 SQLite DB를 사용한다. 게임 User/Player와 게임 MySQL을 읽거나 복사하지 않는다.
- CSRF middleware를 유지한다. 로그인·로그아웃은 POST, CSRF 발급은 GET이다. 비정상 JSON 400, 잘못된 자격 401, CSRF 누락 403, 메서드 불일치 405를 구분한다.
- 토큰과 비밀번호는 검사 결과/인수인계에 기록하지 않는다. 로그인 이후 회전하는 토큰을 다시 받아 로그아웃하는 흐름도 테스트했다.
- admin URL은 기존 의도를 살려 유지했다. 캠페인·입찰·MongoDB 이벤트 기능은 이번 시작 오류 수정에서 추가하지 않았다.

## 검사와 결과

실행 위치: `C:/MLO01-01/Chapter3/ad_server`. 실제 기존 `.venv`의 Python을 사용했다. 샌드박스에서 기반 Python 실행이 거부돼 허용된 샌드박스 밖 실행으로 검증했다.

```powershell
.\.venv\Scripts\python.exe -B ad_config/ads_manage.py check
.\.venv\Scripts\python.exe -B ad_config/ads_manage.py test ads --verbosity 2
.\.venv\Scripts\python.exe -B ad_config/ads_manage.py migrate --noinput
```

- check: exit 0, `System check identified no issues (0 silenced)`.
- test: 6개 모두 통과. CSRF 발급/GET 제한, CSRF 누락 거부, 비정상 본문 거부, 잘못된 자격 거부, 로그인/로그아웃의 광고 세션, admin 경로를 검증했다. 테스트 DB는 메모리 DB이며 끝에 제거됐다.
- migrate: 기본 admin/auth/contenttypes/sessions 마이그레이션 모두 성공.
- 실제 `runserver 127.0.0.1:8001 --noreload`를 검사 프로세스에서 실행해 `/api/auth/csrf/` HTTP 200, JSON 토큰 필드, 광고 CSRF cookie를 확인했다. 실제 값은 출력하지 않았다. 자신이 시작한 검사 서버만 종료했다.

## 라우팅 문서 정합화

기존 코드와 문서가 먼저 일치하도록 변경 전 진입점/설정/URL/테스트 문서를 작성했다. 코드 검증 후 설정/URL/테스트 문서를 최종 구현으로 갱신하고 인증 짝 문서와 색인 항목을 추가했다. 문서에 미래 MongoDB/캠페인 구현을 현재 동작으로 기록하지 않았다.

`routing-doc-auditor` CLI는 Git 저장소가 아니어서 실패했다. 저장소를 임의로 초기화하지 않고 스킬의 `extract_symbols`와 `mark_documented`를 호출해 동일한 AST 기반 시그니처 검사를 수행한다. 대상은 이번 범위의 Python 파일 5개이며 실제 문서/색인과 시그니처를 대조한다. 검사 결과는 `docs/server-routing/verification/startup-fix-audit.json`에 남긴다. Git 변경 수집 불가와 파일/AST 정합성 검사 결과는 분리한다.

최종 결과는 `summary.ok = true`, 검사 파일 5개, 문서/색인/시그니처 누락 0이다. 작업 시작 해시와 대조한 변경 범위 밖의 기존 파일 14개는 모두 그대로였다. 실제 기능 변경은 설정·URL·테스트 수정과 인증 모듈 추가이며 기존 진입점은 사용자가 작성한 상태를 유지했다. 최종 Git 확인도 저장소가 아니라는 결과였다.

## 남은 범위와 다음 실행

- MongoDB 복제 세트 시작과 `ads/mongo.py` 구현은 별도 수업 단계다. 이번 인증/서버 시작 검사는 MongoDB 성공을 의미하지 않는다.
- 실제 광고주 계정은 생성하지 않았다. 필요할 때 사용자 본인이 `createsuperuser`로 입력한다.
- 기본 `/`에는 경로를 추가하지 않았다. 서버 동작은 `/api/auth/csrf/` 또는 `/admin/`에서 확인한다.

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python ad_config/ads_manage.py runserver 8001
```

광고주 계정이 필요한 시점의 명령:

```powershell
python ad_config/ads_manage.py createsuperuser
```

새 개발을 시작할 때 대상은 계속 Git 저장소가 아니므로 작업 시작 파일을 사용자 작업으로 보존하고, 바뀐 개발 파일의 짝 문서만 갱신한다.
