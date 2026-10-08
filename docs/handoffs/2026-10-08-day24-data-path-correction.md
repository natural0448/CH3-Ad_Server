# 24일차 게임 입력 경로 정정 — 광고 범위

## 요청·현재 결과

사용자가 기존 게임 루트 data 폴더를 사용하도록 정정을 요청했다. 에이전트가 앞서 server/ 기준 상대 출력 경로를 안내한 것이 잘못됐다. 올바른 광고 소비 입력은 **`../Game-server/data/exports/player-cdc.ndjson`**이다. [게임 저장 경로 정정 인수인계](../../../Game-server/docs/handoffs/2026-10-08-day24-data-path-correction.md)에 실제 파일 이동·SHA-256·검사 결과·VS Code 명령을 기록했다.

## 시작 Git 상태와 기존 변경

광고 저장소 HEAD는 `8f541e4 day23 - finish`였고 staged·unstaged는 없었다. 이전 검토에서 추가한 checker·문서·증거는 untracked로 존재했다. 옛 광고 export 명령은 이번 요청 전에 이미 없어졌고, 사용자가 교안대로 수정한 게임 명령은 게임 저장소에 있었다. 이번 에이전트의 source 이동으로 주장하지 않는다. 전체 기존 변경은 `docs/server-routing/verification/day24-data-path-correction/start-state.json`에 기록했다. Chapter3는 Git 저장소가 아니고 각 저장소 경계를 따로 확인했다.

## 이번 변경과 문서 정합화

- 사라진 광고 source의 짝 문서 `docs/server-routing/files/ads/management/commands/export_player_snapshot.py.md`를 제거했다. 초기 사용자 코드 백업·검토 증거·최초 인수인계 기록은 보존했다.
- `docs/server-routing/day24-period01-index.md`에서 광고 export 항목을 제거하고 실제 게임 source/짝 문서 및 루트 data 경로를 연결했다.
- 최초 검토 인수인계에 후속 사용자 수정과 경로 정정 상태를 명시하고 입력 경로를 고쳤다.
- 이 인수인계와 경로 정정 검증 기록을 추가했다.
- 광고 Python·checker·환경·설정·템플릿은 변경하지 않았다. data 이동은 게임 저장소 안에서만 수행했다.

사용자 코드 정합화를 데이터 이동 전에 수행했고, 검증 뒤 현재 상태를 다시 맞췄다. 현재 광고 routing에는 존재하지 않는 명령 문서를 남기지 않는다. 기존 README 부재는 복원하지 않았다.

## 검사 결과·한계·후속 순서

현재 게임 코드 공식 검사 12개 통과·0개 실패, 실제 snapshot 56행의 8필드·ID·시각·schema 형식 및 이동 해시 일치를 확인했다. 광고 범위는 같은 routing-doc-auditor AST API로 존재하는 checker 1개·문서·별도 색인을 검사했고, 삭제된 광고 source와 짝 문서 부재도 확인했다. 결과는 `routing-final-scoped.json`이다. 환경 파일 hash·기존 source 보존·최종 Git 상태는 finish-state.json을 따른다. 표준 감사 CLI는 기존 README 부재로 실행할 수 없으므로 표준 검사 통과로 주장하지 않는다.

snapshot은 이미 `C:/MLO01-01/Chapter3/Game-server/data/exports/player-cdc.ndjson`에 있다. 2교시에서 광고 작업 폴더 기준 `../Game-server/data/exports/player-cdc.ndjson`을 읽으면 된다. 아직 없는 snapshot_intake.py나 후속 관리명령을 구현했다고 기록하지 않는다. 이번에는 실제 DB 재수집·쓰기, 서버 실행/종료를 하지 않았다. 실행 명령은 연결된 게임 인수인계에 있다.
