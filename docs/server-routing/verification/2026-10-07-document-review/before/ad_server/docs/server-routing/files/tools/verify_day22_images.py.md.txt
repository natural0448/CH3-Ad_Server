# tools/verify_day22_images.py

## 22일차 이미지 광고 최종 반영

전체 HTTP 흐름의 분리 검증 진입점이다. ROOT=ad_server, WORKSPACE=Chapter3, REPORT=docs/server-routing/verification/day22-images. 자신이 만든 infra/runtime/day22-images-UUID 폴더, Mongo27109 ads-image-validation, 별도 SQLite 두 개, 웹18001/18000만 사용한다. key는 임시 synthetic fixture 설정이고 수업 키 전달을 하지 않는다. 비밀번호는 무작위 process env에서만 읽는다. 실제 수업 계정·Mongo27017·MySQL을 쓰지 않는다. 광고주 세션 폼 저장 → 게임 세션 Player12 → 매체 API → 게임-origin PNG → 입찰20/30 변경 → 이전 snapshot 유지 → SDL dummy 두 슬롯 frame → 설치된 Chrome의 웹/게임 미리보기를 확인한다. finally는 자기 Popen만 종료한다. actual_student_game_observation=not_run으로 기록한다.

클래스 계약: `class Web`.


### `child(component, owned)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| component | 없음 | ad/game/render 중 fixture 역할. |
| owned | 없음 | 자기 infra/runtime UUID 작업 폴더 Path. |

반환·실패: None; 검증 실패 assertion/예외.

의사코드: fixture component에 맞춰 override DB/키 설정 후 migrate/create fixture/runserver 또는 SDL frame.

직접 호출: `django.setup`, `call_command`, `get_user_model().objects.create_user`, `sys.path.insert`, `pygame.display.init`, `pygame.font.init`, `pygame.display.set_mode`, `Controller`, `controller.game.apply_identity`, `ScreenRenderer`, `json.loads`, `enumerate`, `pygame.quit`, `str`, `Player.objects.create`, `Network`. 호출 결과는 이 함수의 반환·상태 갱신에 사용한다. 외부 계층의 내부 구현은 그 계층 문서에서 설명한다.

### `Web.__init__(self, base, csrf_name='csrftoken')`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 클래스 인스턴스; 클래스가 소유한 상태에만 쓴다. |
| base | 없음 | 분리 fixture server origin. |
| csrf_name | `'csrftoken'` | fixture 서버의 CSRF cookie 이름; 값은 기록하지 않는다. |

반환·실패: None.

의사코드: 해당 파일 책임에 정의한 소유 상태/fixture를 초기화·정리 또는 교체.

직접 호출: `http.cookiejar.CookieJar`, `build_opener`, `HTTPCookieProcessor`. 호출 결과는 이 함수의 반환·상태 갱신에 사용한다. 외부 계층의 내부 구현은 그 계층 문서에서 설명한다.

### `Web.get(self, path)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 클래스 인스턴스; 클래스가 소유한 상태에만 쓴다. |
| path | 없음 | 허용된 상대 PNG URL 또는 fixture HTTP 경로; 외부 URL은 PNG fetch 금지. |

반환·실패: bytes; HTTP/network 오류.

의사코드: 자기 cookie opener로 fixture GET → 응답 read → close.

직접 호출: `self.opener.open`, `response.read`. 호출 결과는 이 함수의 반환·상태 갱신에 사용한다. 외부 계층의 내부 구현은 그 계층 문서에서 설명한다.

### `Web.csrf(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 클래스 인스턴스; 클래스가 소유한 상태에만 쓴다. |

반환·실패: csrf 문자열을 memory로만 반환; 없으면 StopIteration.

의사코드: 자기 fixture CookieJar에서 지정 이름 검색.

직접 호출: `next`. 호출 결과는 이 함수의 반환·상태 갱신에 사용한다. 외부 계층의 내부 구현은 그 계층 문서에서 설명한다.

### `Web.post(self, path, fields, json_body=False)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 클래스 인스턴스; 클래스가 소유한 상태에만 쓴다. |
| path | 없음 | 허용된 상대 PNG URL 또는 fixture HTTP 경로; 외부 URL은 PNG fetch 금지. |
| fields | 없음 | fixture form/JSON dict; 비밀번호는 process memory에서만 전달. |
| json_body | `False` | JSON encoding 여부 bool. |

반환·실패: bytes; HTTP/network 오류.

의사코드: form/JSON encoding → memory csrf header → fixture POST → 응답 read.

직접 호출: `Request`, `json.dumps(fields).encode`, `urlencode(fields).encode`, `self.opener.open`, `response.read`, `json.dumps`, `urlencode`, `self.csrf`. 호출 결과는 이 함수의 반환·상태 갱신에 사용한다. 외부 계층의 내부 구현은 그 계층 문서에서 설명한다.

### `wait_http(url, process)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| url | 없음 | 검사할 fixture HTTP URL. |
| process | 없음 | 자기 생성 subprocess.Popen. |

반환·실패: None 또는 RuntimeError.

의사코드: fixture process 상태+HTTP 반복확인 → timeout.

직접 호출: `build_opener`, `range`, `RuntimeError`, `process.poll`, `opener.open`, `time.sleep`. 호출 결과는 이 함수의 반환·상태 갱신에 사용한다. 외부 계층의 내부 구현은 그 계층 문서에서 설명한다.

### `main()`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|

반환·실패: 성공0 또는 실패 예외.

의사코드: 인자·포트 확인 → owned Mongo/웹 fixture 시작 → 로그인/광고·입찰 저장 → 슬롯선택·PNG·snapshot 비교 → render/Chrome → JSON evidence → finally 종료.

직접 호출: `argparse.ArgumentParser`, `parser.add_argument`, `parser.parse_args`, `owned.mkdir`, `owned.resolve().is_relative_to`, `REPORT.mkdir`, `dict`, `MongoClient`, `child`, `parser.error`, `(ROOT / 'infra/runtime').resolve`, `(owned / (name + '.log')).open`, `logs.append`, `subprocess.Popen`, `processes.append`, `start`. 호출 결과는 이 함수의 반환·상태 갱신에 사용한다. 외부 계층의 내부 구현은 그 계층 문서에서 설명한다.

### `main.start(command, name, cwd)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| command | 없음 | fixture 자식 프로세스 인자 list. |
| name | 없음 | fixture 로그 식별자/테스트 helper 문자열. |
| cwd | 없음 | fixture 프로젝트 작업 폴더. |

반환·실패: 코드 반환 식: `process`.

의사코드: 기존 입력·상태 검사 → 직접 호출 → 현재 결과/상태 전달; 이미지 추가 책임은 위 파일 설명 참조.

직접 호출: `(owned / (name + '.log')).open`, `logs.append`, `subprocess.Popen`, `processes.append`. 호출 결과는 이 함수의 반환·상태 갱신에 사용한다. 외부 계층의 내부 구현은 그 계층 문서에서 설명한다.
