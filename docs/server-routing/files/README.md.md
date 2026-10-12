# README.md

광고 서버의 실행·계정·캠페인·입찰·소재·실적 안내와 현재 구조 대응을 설명한다. 최신 3교시의 수정 위치는 Game-server/server/game/ad_gateway.py::request_ad_event이며 공식 검증 파일은 미저장·미실행임을 명시한다. config/day23-period-03.py의 False/True는 이전 교안 실습으로 보존됐고 최신 True/None 예제와 다르다. 기존 접속기 연결 자료와 자체 HTTP/PNG/Pygame 검사 기록을 최신 3교시 평가와 구별한다. 비밀값과 실제 세션은 기록하지 않는다.

2026-10-08 현재 진행 문단은 광고 사건 파일 내보내기·후보 집계·게시·보고서 UI·파일 전달·대조 명령이 소스로 존재함을 설명하고 `docs/server-routing/current-progress-index.md`로 연결한다. 기존 설명의 "4교시 이후 미적용"과 "일별 보고서 링크 없음"을 현재 구현에 맞췄다. 이 문서 갱신에서 해당 기능을 실행했다고 주장하지 않는다.

24일차 안내는 앞선 1교시 12개, 최종 2교시 22개·3교시 8개·4교시 17개 통과 및 실제 원본 56행·checksum 보존을 반영한다. snapshot 검사, readiness, change_player 및 관리명령/화면 검사가 구현됐다. 광고 입력은 ../Game-server/data/exports/player-cdc.ndjson이며 readiness/fixture 결과는 광고 루트 data/contracts와 data/fixtures다. 파일 검사는 MongoDB/runserver 기동 없이 실행하고 5~8교시 후속 구현은 미적용이다. 현재 인수인계로 연결한다. README는 설명 문서이며 함수·클래스 정의가 없고 소스/원본을 쓰지 않는다.
