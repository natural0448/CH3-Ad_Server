# 24일차 1교시 검토 색인

현재 구현을 설명한다. 기존 `README.md`는 작업 시작 HEAD에서도 없으며 복원하지 않았다. 사용자가 snapshot 명령을 게임 앱으로 옮겼으므로 광고 앱 명령 항목과 짝 문서를 제거하고 게임 색인을 따른다.

광고의 22~23일차 현재 구현과 전체 짝 문서는 [현재 진행 색인](current-progress-index.md)을 따른다. 2026-10-12에 24일차 1·2교시를 다시 확인해 게임 12개·광고 22개 공식 검사가 통과했고 실제 원본 56행·checksum도 일치했다. 후속 [4교시까지 복구 검증](../handoffs/2026-10-12-day24-period04-recovery.md)에서는 2교시 22개·3교시 8개·4교시 17개와 교안 화면 검사·실제 원문/summary 저장이 통과했다. 현재는 [7교시까지 검토](../handoffs/2026-10-12-day24-through-period07-review.md)에서 추가 5교시 13개·6교시 15개·7교시 10개 및 실제 계약·비교·누락 저장본까지 통과했다. 8교시는 [현재 완료 검토](../handoffs/2026-10-12-day24-period08-finish.md)에서 공식 24개 검사와 실제 수신 파일·계약 인계까지 성공했다. 이전 1교시 실패·경로 정정 자료는 당시 기록으로 보존한다.

| 실제 개발 파일 | 짝 라우팅 문서 | 현재 상태 |
|---|---|---|
| tools/check_day24_logic.py | [문서](files/tools/check_day24_logic.py.md) | Downloads의 공식 원본과 bytes 동일. 후속 교시 준비용 검사 도구 |

snapshot 명령의 현재 위치는 `../Game-server/server/game/management/commands/export_player_snapshot.py`이며 [게임 짝 문서](../../../Game-server/docs/server-routing/files/server/game/management/commands/export_player_snapshot.py.md)가 현재 구현을 설명한다. 광고에서 읽을 입력 경로는 `../Game-server/data/exports/player-cdc.ndjson`이다. 옛 광고 파일의 초기 검토 기록은 verification과 인수인계에 보존했다.

게임 서버에 추가한 공식 검사 도구와 검토 결과는 [게임 서버 인수인계](../../../Game-server/docs/handoffs/2026-10-08-day24-period01-review.md), 광고 범위는 [광고 인수인계](../handoffs/2026-10-08-day24-period01-review.md)를 따른다. 검사 근거는 `verification/day24-period01-review/`에 있다.
