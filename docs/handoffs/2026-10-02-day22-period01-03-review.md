# 22일차 1~3교시 구현 점검

- 점검일: 2026-10-02 (Asia/Seoul)
- 요청: 수정된 교안의 3교시까지 현재 구현에 잘못된 부분이 있는지 확인.
- 기준 교안: `C:/Users/이해나/Desktop/22일차 · 광고 플랫폼이 광고주의 광고를 게임 유저에게 집행한다.html`
- 대상: `C:/MLO01-01/Chapter3/ad_server`와 로컬 MongoDB의 현재 상태.
- 결과: 패키지는 설치됐으나 광고 Django 설정/URL 로딩이 실패한다. 현재 실행 중인 MongoDB에서는 복제 세트가 확인되지 않았다. 소스·환경 파일·DB·서비스를 수정하지 않고 검사 기록만 추가했다.

## 작업 시작 전 Git 상태와 기존 파일

- `C:/MLO01-01`, `C:/MLO01-01/Chapter3`, `C:/MLO01-01/Chapter3/ad_server`: **Git 상태 확인 불가: 저장소 아님**. 저장소를 초기화하지 않았다. 직전 커밋과 staged/unstaged/untracked 분류를 적용할 수 없다.
- 인접 `Game-server`: 직전 커밋 `2ae4712 day21 - finish`, staged 변경 없음. 작업 시작 전에 day19~21 연습 Python 파일 24개가 삭제 상태였고 `tools/basics/day19/`, `day20/`, `day21/`, `day22/`가 untracked였다. 해당 파일은 이번 작업 범위 밖이며 수정하지 않았다.
- `ad_server`의 기존 `.venv`, `ad_config/ad_config/`, `ad_config/ads_manage.py`, `ad_config/manage.py`, `ads/`, `requirements.txt`, `.gitignore`, `ads.env`는 모두 작업 시작 전에 존재한 사용자 파일로 취급했다.

## 현재 구조

```text
ad_server/
  .venv/
  ads.env
  requirements.txt
  ad_config/
    ads_manage.py
    manage.py
    ad_config/
      settings.py
      urls.py
      asgi.py
      wsgi.py
      __init__.py
  ads/
    apps.py
    views.py
    models.py
    tests.py
    admin.py
    __init__.py
    migrations/__init__.py
```

`ad_config`는 현재 Django 프로젝트 디렉터리이며 가상환경은 `.venv`다. 3교시의 독립 광고 서버 구성 자체는 수정 교안의 방향과 맞는다. 현재 `ads_manage.py`와 `ads`의 상대 위치가 import 실패를 만든다.

## 확인된 문제

### 1. 환경 파일 경로와 필수 키 불일치 — 시작 차단

- `ad_config/ad_config/settings.py:17~19`에서 `BASE_DIR`는 `ad_server/ad_config`이며 `load_dotenv(BASE_DIR / "ads.env", override=True)`를 호출한다.
- 실제 환경 파일은 그 상위 `ad_server/ads.env`에 있고 예상 위치 `ad_server/ad_config/ads.env`는 없다.
- 실제 환경 파일의 키 이름만 검사했다. 수정 교안의 `ADS_SECRET_KEY`, `ADS_MEDIA_KEY`, `MONGO_URI`, `MONGO_DB`가 없고 기존 게임 DB/설정 키를 사용한다. 키 값은 검사 기록에 복사하지 않았다.
- 정상 실행 조건으로 검사한 `ads_manage.py check`는 `KeyError: 'ADS_SECRET_KEY'`로 종료했다.
- 경로 수정과 광고 전용 키 작성이 함께 필요하다. 환경 파일을 찾도록 고치는 것만으로 현재 누락된 키가 생기지는 않는다.

### 2. 진입점과 앱의 상대 경로 불일치 — URL 로딩 차단

- 진입점은 `ad_server/ad_config/ads_manage.py`, 앱은 `ad_server/ads`다.
- 진입점 디렉터리에서 Python을 실행하면 상위 `ad_server`가 기본 모듈 검색 경로에 포함되지 않는다.
- 임시 비밀 키를 프로세스 내부에만 지정하고 URL 모듈을 import하면 `ModuleNotFoundError: No module named 'ads'`가 발생한다.
- 프로세스 안에서 상위 경로를 추가해도 다음 문제인 `auth_views` 누락으로 실패한다. 경로 보완만으로 완료되지 않는다.

### 3. 3교시 필수 파일과 앱 등록 누락

다음 파일이 현재 대상 프로젝트에 없다.

- `ads/auth_views.py`
- `ads/mongo.py`
- `ads/repository.py`, `ads/services.py`, `ads/urls.py` 준비 파일
- `ads/management/__init__.py`, `ads/management/commands/__init__.py`

또한 `settings.py:37~44`의 `INSTALLED_APPS`에 `ads`가 없다. 독립 로그인 URL은 `auth_views`를 이미 참조하지만 해당 모듈이 없어 import할 수 없다. `get_client()`, `get_db()`, `close_client()`가 구현되지 않았으므로 PyMongo의 패키지 설치 성공을 앱의 DB 연결 성공으로 해석할 수 없다.

### 4. URL 목록 중복 정의와 정의되지 않은 admin

- `ad_config/ad_config/urls.py:4~8`에 인증 URL을 정의한 뒤 `9~11`에서 `urlpatterns`를 다시 정의한다.
- 마지막 목록의 `admin.site.urls`를 사용하지만 `admin`을 import하지 않았다.
- 현재의 앱 import 실패를 먼저 해결하면 이 부분에서 `NameError`가 발생할 수 있다. admin import만 추가해도 두 번째 대입 때문에 앞의 인증 URL 목록은 교체된다.
- URL 목록은 현재 요구하는 경로를 담은 하나의 목록으로 정리해야 한다. 아직 이 수정은 적용하지 않았다.

### 5. settings 중복 정의가 광고 전용 값을 덮어씀

- `settings.py:19`에서 환경 변수로 읽는 `SECRET_KEY`가 `27`의 생성 당시 상수로 덮어써진다.
- `20`의 로컬 호스트 허용 목록이 `32`의 빈 목록으로 덮어써진다.
- 프로세스 내부 임시 키로 설정을 불러온 검사에서 환경 키 적용 여부는 False, 최종 `ALLOWED_HOSTS`는 `[]`였다.
- 환경 키 접근이 먼저 실행되므로 아래 기본 키가 존재해도 최초 `KeyError`는 방지되지 않는다.

### 6. 광고 계정 DB 설정과 마이그레이션 상태

- `settings.py:79~84`는 별도 SQLite를 사용하므로 게임 MySQL과는 분리돼 있다.
- 파일명은 `db.sqlite3`이고 교안의 명시적 계약은 `ads-auth.sqlite3`다. 파일명만 다르다는 이유로 DB 분리가 실패했다고 판단하지는 않았다.
- 현재 예상 위치에 두 DB 파일 모두 없다. 따라서 로컬 파일 기준으로 계정 마이그레이션/생성 완료를 확인하지 못했다.
- 설정과 URL 로딩 문제를 먼저 해결한 뒤 마이그레이션과 광고주 계정 생성을 확인해야 한다. 이번 점검에서는 DB 생성이나 마이그레이션을 실행하지 않았다.

### 7. 1교시의 현재 MongoDB 실행 상태가 복제 세트 조건과 다름

- `localhost:27017`은 응답하며 `hello`에 복제 세트 이름과 멤버 목록이 없다.
- `rs.status()` 결과는 `not running with --replSet`다.
- `localhost:27018`, `localhost:27019`는 직접 연결에서 연결 거부가 발생했다.
- 따라서 현재 이 주소에서 PRIMARY 1개/SECONDARY 2개의 `ads-rs` 상태를 확인하지 못했다. 과거 실습의 성공 여부까지 부정하는 결과는 아니다.
- 27017의 `village_ads`는 ping 1, 컬렉션 목록 `[]`, 캠페인 개수 0이었다.
- 2교시 CRUD는 연습 문서를 마지막에 삭제하므로 문서 개수 0만으로 미실행이라고 단정하지 않았다. 생성/부분 수정/삭제의 기록이 있어야 순서와 결과를 검증할 수 있다.
- 점검한 `ad_server`와 `Game-server/data/evidence`에는 day22 제출 증거가 없었고, `Game-server/tools/basics/day22`에는 1교시 파일만 확인됐다. 다른 경로의 기록이나 저장하지 않은 편집 내용은 점검하지 않았다.

## 정상 확인된 부분

- 기존 `.venv`는 Python 3.14.6, Django 5.2.17, PyMongo 4.18.2를 사용한다. `dotenv` import도 성공했다. Python은 교안의 3.12와 다르지만 이번 시작 오류의 원인으로 단정하지 않았다.
- 기존 가상환경 실행이 처음에는 샌드박스에서 기반 Python 접근 거부로 실패했다. 샌드박스 밖의 읽기 전용 검사에서 정상 실행돼 가상환경 파손으로 보고하지 않았다.
- 광고 세션/CSRF 쿠키 이름은 `ads_sessionid`, `ads_csrftoken`으로 설정돼 있다.
- `ads_manage.py`는 `DJANGO_SETTINGS_MODULE`을 `ad_config.settings`로 명시적으로 지정한다.
- 게임 앱/설정 import는 현재 광고 설정에 없다.
- 광고 프로젝트의 Python 소스 14개는 AST 구문 분석에 성공했다. 구문 성공은 Django 설정/URL 로딩 성공과 별개다.

## 교안의 경로 안내에서 주의할 부분

3교시의 경로 안내가 내부적으로 섞여 있다. `ad_project_seed`를 준비하라고 설명하면서 생성 명령은 `python -m django startproject ad_config`로 되어 있어 실행 위치 아래에 `ad_config/manage.py`와 `ad_config/ad_config/`가 생성된다. 이어서 설명에는 임시 폴더에서 설정 패키지를 옮기는 흐름이 있으나 명령에는 임시 폴더 대상이 지정돼 있지 않다. 또한 `server/ads_manage.py`를 만들라고 한 뒤 앱 생성 명령에는 `ad_config/ads_manage.py`를 사용한다. 현재 중첩 구조가 이 안내에서 비롯됐을 가능성이 있다. 이 부분은 사용자 코드 오류와 구분한다.

## 수정 순서 제안 — 계획, 미적용

1. 광고 프로젝트 루트와 진입점/설정 패키지/앱/환경 파일의 상대 위치를 먼저 통일한다.
2. 실제 환경 파일의 광고 전용 필수 키와 로드 경로를 맞추고 중복 `SECRET_KEY`/`ALLOWED_HOSTS` 정의를 정리한다.
3. `ads` 등록, 독립 인증 모듈, 단일 URL 목록을 완성한다.
4. MongoDB 복제 세트의 세 멤버를 다시 확인하고 `ads/mongo.py`의 재사용 연결 함수를 작성한다.
5. `check` 성공 후 계정 DB 마이그레이션/광고주 계정 생성과 DB ping/클라이언트 재사용을 검증한다.
6. 각 교시 실제 관찰값을 제출 증거에 남긴다. 신규 개발을 수행할 때 해당 파일의 짝 라우팅 문서와 색인을 함께 만든다.

## 검사 명령과 결과

진입점 위치에서 실행한 실제 검사:

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server\ad_config
& ..\.venv\Scripts\python.exe -B ads_manage.py check
```

- 실패(exit 1): `KeyError: 'ADS_SECRET_KEY'`.
- 이후 오류를 분리하기 위해 임시 키와 모듈 검색 경로를 검사 프로세스 안에서만 지정했다. 실제 환경 파일과 시스템 환경은 바꾸지 않았다. `ads` 모듈 경로 오류, `auth_views` 누락, 덮어써진 설정 값을 확인했다.

MongoDB 복제 세트 연결 검사:

```powershell
mongosh "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=ads-rs&serverSelectionTimeoutMS=3000" --quiet --eval 'printjson(rs.status().members.map(m=>({name:m.name,role:m.stateStr,health:m.health})))'
```

- 실패(exit 1): 연결 거부. 각 포트의 directConnection 검사로 27017 단독 서버 응답, 27018/27019 연결 거부를 구분했다.
- 27017 직접 연결에서 `hello`, `rs.status`, `village_ads` ping/컬렉션명/개수만 읽었다. 데이터를 쓰거나 삭제하지 않았다.
- `mongosh` 자체 로그 디렉터리는 샌드박스에서 쓰기가 거부돼 경고가 있었지만 27017의 읽기 요청은 성공했다.
- Python AST 검사: 14개 성공. 별도 동작 테스트 파일을 추가하지 않았다.

## 문서와 최종 변경 범위

- 이번에 추가한 파일: 이 인수인계 문서 1개.
- 기존 소스, 설정, 환경 파일, 가상환경, DB, MongoDB 서비스/복제 설정의 수정·이동·삭제 없음.
- 현재 `ad_server`에는 라우팅 문서와 색인이 없다. 이번에는 개발 파일을 변경하지 않아 갱신 대상 짝 문서가 없었다. 라우팅 문서 정합화 완료 또는 3교시 구현 완료로 보고하지 않는다.
- Git 기반 라우팅 검사기는 대상이 Git 저장소가 아니므로 적용할 수 없다. 저장소를 임의로 초기화하지 않았다.
- 기능 테스트, 로그인 요청, 계정 생성, PyMongo 앱 연결 검사는 필요한 모듈과 설정이 미완성이라 성공 상태까지 진행할 수 없었다.
- 다음 작업은 위 수정 순서에 따라 먼저 Django 시작 오류를 해결하는 것이다. 현재 명령을 반복 실행하는 것만으로 누락 파일이나 환경 키는 생성되지 않는다.
