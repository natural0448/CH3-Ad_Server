# 24일차 1교시 검토 색인

현재 구현을 설명한다. 기존 `README.md`는 작업 시작 HEAD에서도 없으며 복원하지 않았다. 사용자가 snapshot 명령을 게임 앱으로 옮겼으므로 광고 앱 명령 항목과 짝 문서를 제거하고 게임 색인을 따른다.

광고의 22~23일차 현재 구현과 전체 짝 문서는 [현재 진행 색인](current-progress-index.md)을 따른다. 현재 광고의 24일차에는 공식 검사기와 작성 중인 2교시 [snapshot_intake](files/ads/snapshot_intake.py.md)가 저장돼 있다. 최신 inspect에는 필드/공개 상태/중복/수집값 통일 검사가 있으나 `parse_utc` 이름 식만 있어 captured_at 시각 검사가 호출되지 않는다. snapshot 검사/소비 성공 상태가 아니며 3~8교시 후속 소비 구현과 관리명령은 아직 없다. 게임 ORM은 광고 앱에서 import하지 않는다.

| 실제 개발 파일 | 짝 라우팅 문서 | 현재 상태 |
|---|---|---|
| tools/check_day24_logic.py | [문서](files/tools/check_day24_logic.py.md) | Downloads의 공식 원본과 bytes 동일. 후속 교시 준비용 검사 도구 |

snapshot 명령의 현재 위치는 `../Game-server/server/game/management/commands/export_player_snapshot.py`이며 [게임 짝 문서](../../../Game-server/docs/server-routing/files/server/game/management/commands/export_player_snapshot.py.md)가 현재 구현을 설명한다. 광고에서 읽을 입력 경로는 `../Game-server/data/exports/player-cdc.ndjson`이다. 옛 광고 파일의 초기 검토 기록은 verification과 인수인계에 보존했다.

게임 서버에 추가한 공식 검사 도구와 검토 결과는 [게임 서버 인수인계](../../../Game-server/docs/handoffs/2026-10-08-day24-period01-review.md), 광고 범위는 [광고 인수인계](../handoffs/2026-10-08-day24-period01-review.md)를 따른다. 검사 근거는 `verification/day24-period01-review/`에 있다.
