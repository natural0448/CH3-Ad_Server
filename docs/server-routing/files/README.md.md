# README.md

광고 서버의 실행·계정·캠페인·입찰·소재·실적 안내와 현재 구조 대응을 설명한다. 최신 3교시의 수정 위치는 Game-server/server/game/ad_gateway.py::request_ad_event이며 공식 검증 파일은 미저장·미실행임을 명시한다. config/day23-period-03.py의 False/True는 이전 교안 실습으로 보존됐고 최신 True/None 예제와 다르다. 기존 접속기 연결 자료와 자체 HTTP/PNG/Pygame 검사 기록을 최신 3교시 평가와 구별한다. 비밀값과 실제 세션은 기록하지 않는다.

2026-10-08 현재 진행 문단은 광고 사건 파일 내보내기·후보 집계·게시·보고서 UI·파일 전달·대조 명령이 소스로 존재함을 설명하고 `docs/server-routing/current-progress-index.md`로 연결한다. 기존 설명의 "4교시 이후 미적용"과 "일별 보고서 링크 없음"을 현재 구현에 맞췄다. 이 문서 갱신에서 해당 기능을 실행했다고 주장하지 않는다.

24일차 검사기 `tools/check_day24_logic.py`와 작성 중인 2교시 `ads/snapshot_intake.py`가 저장돼 있다. 최신 inspect에는 필드/공개 상태/중복/수집값 통일 검사가 있으나 `parse_utc` 이름 식만 있어 captured_at 시각 검사는 호출되지 않는다. 검사/소비 성공을 뜻하지 않으며 3~8교시 후속 소비 구현/명령은 아직 없다. 게임 snapshot 명령 위치와 광고의 입력 경로 `../Game-server/data/exports/player-cdc.ndjson`을 안내한다. 광고에서 게임 ORM을 import하거나 `server/data`를 만들라는 안내는 없다. 루트 README는 사용자 안내 문서이며 실행 가능한 함수·클래스·상수 정의를 갖지 않는다.
