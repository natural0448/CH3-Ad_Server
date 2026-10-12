# README.md

광고 서버의 실행·계정·캠페인·입찰·소재·실적 안내와 현재 구조 대응을 설명한다. 최신 3교시의 수정 위치는 Game-server/server/game/ad_gateway.py::request_ad_event이며 공식 검증 파일은 미저장·미실행임을 명시한다. config/day23-period-03.py의 False/True는 이전 교안 실습으로 보존됐고 최신 True/None 예제와 다르다. 기존 접속기 연결 자료와 자체 HTTP/PNG/Pygame 검사 기록을 최신 3교시 평가와 구별한다. 비밀값과 실제 세션은 기록하지 않는다.

2026-10-08 현재 진행 문단은 광고 사건 파일 내보내기·후보 집계·게시·보고서 UI·파일 전달·대조 명령이 소스로 존재함을 설명하고 `docs/server-routing/current-progress-index.md`로 연결한다. 기존 설명의 "4교시 이후 미적용"과 "일별 보고서 링크 없음"을 현재 구현에 맞췄다. 이 문서 갱신에서 해당 기능을 실행했다고 주장하지 않는다.

24일차 안내는 앞선 1~4교시 성공 이력과 이번 5교시 13개·6교시 15개·7교시 10개 및 화면 검사 통과를 반영한다. snapshot/readiness/fixture, 인계 계약·상태 비교·누락 관찰 함수와 명령이 구현됐다. 광고 입력은 ../Game-server/data/exports/player-cdc.ndjson과 ../Game-server/data/exports/player-snapshot-after.ndjson이며 각 56행이다. 실제 계약·비교·누락 JSON도 일치하고 변경 1건·새 ID/누락 각 0건이다. 파일 검사는 MongoDB/runserver 기동 없이 실행하고 8교시 인계 함수·명령은 공식 24개 검사를 통과하고 data/exports/day24-input에 실제 인계까지 완료했다. 수신 NDJSON은 56행이고 원본 checksum과 같으며 계약은 source_path만 수신 경로로 바뀌었다. 이번 문서 작업에서 사용자 Python 소스와 기존 원본·산출물을 쓰지 않았다. 현재 인수인계로 연결한다. README는 설명 문서이며 함수·클래스 정의가 없다.
