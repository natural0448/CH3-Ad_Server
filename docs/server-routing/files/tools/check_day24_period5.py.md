# tools/check_day24_period5.py

24일차 5교시 교안 화면의 제공 검사 코드가 사용자가 정한 tools 경로에 저장돼 있다. 독립 스크립트이며 import 시 모듈 본문을 실행한다. 실제 export 파일 대신 TemporaryDirectory 아래 시험 파일만 쓴다. 2026-10-12 [화면 검사 exit 0](../../verification/2026-10-12-day24-period05-07-review/screen-period05.json)으로 정상·빈 입력·5개 거절·원문 보존 PASS를 확인했다. 샌드박스 실행만 tempfile.tempdir를 검증 폴더로 지정했고 파일은 수정하지 않았다.

## write_rows(path, rows)

path는 기본값 없는 출력 Path, rows는 JSON으로 직렬화 가능한 사전 목록이다. 반환은 같은 path다. 의사코드: rows를 ensure_ascii=False JSON 행 + newline으로 합치기 → UTF-8 write_text → path 반환. 직접 호출은 json.dumps와 Path.write_text이며 직렬화/쓰기 오류는 전파한다. 시험 파일만 쓰도록 호출부가 임시 path를 제공한다.

## 모듈 본문과 값

row는 교안 고정 player-snapshot/v1/source_kind=player-snapshot 예제다. id=2, room_id=room-01, coins=30, version=1, captured_at=2026-10-08T01:00:00+00:00, updated_at=2026-10-08T00:00:00+00:00이다. 다른 ID=1을 더해 두 행과 정렬 ID를 검사한다. expected/metadata는 제공 계약, source/saved는 임시 원문 Path/bytes, started/finished는 UTC 호출 전후 시각이다. created/captured는 파싱한 datetime, empty/result는 빈 시험 입력/반환 계약이다. invalid는 중복·비공개 필드·필수 필드 누락·출처·naive 수집 시각 5개 사례다. 반복문의 number/name/rows/path/before는 사례 번호·명칭·원문·Path·기존 bytes다.

직접 호출: tempfile.TemporaryDirectory, write_rows, ads.snapshot_intake.build_snapshot_contract, Path.read_bytes, hashlib.sha256(...).hexdigest, datetime.now/fromisoformat, timedelta, enumerate, print다. 정상 메타데이터·실제 checksum·created_at 범위·입력 보존, 0행, 거절 사례를 assert로 검증한다. 오류 입력에서 ValueError를 기대하며 미거절/assert 불일치는 AssertionError다.

파일 머리말의 python check_day24_period5.py는 루트 파일 배치 예시지만 실제 파일은 tools에 있다. 광고 루트에서 `python -m tools.check_day24_period5`로 실행하면 기존 파일 위치를 유지하면서 ads를 import할 수 있다. 실제 DB나 저장된 계약·게임 export 파일을 변경하지 않는다.
