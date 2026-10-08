# 24일차 1교시 검토 — 광고 서버 범위

> 후속 정정: 사용자가 snapshot 명령을 게임 앱으로 옮기고 수정했다. 기존 광고 파일이 없으므로 그 짝 문서·색인 항목도 게임으로 맞췄다. 실제 소비 입력은 `../Game-server/data/exports/player-cdc.ndjson`이다. 아래 최초 검토 결과는 과거 관찰이며 최신 상태는 [게임 저장 경로 정정 기록](../../../Game-server/docs/handoffs/2026-10-08-day24-data-path-correction.md)을 따른다.

## 최초 검토의 요청·결과

새 교안의 준비와 진행 중인 1교시를 검토했다. 게임 공개 snapshot 명령은 광고 앱에서 실행할 수 없으며 현재 사용자 코드에 파일 위치·조회 필드·행 메타데이터 문제가 있음을 재현했다. 자세한 최소 수정 안내와 VS Code 명령은 [게임 서버 검토 기록](../../../Game-server/docs/handoffs/2026-10-08-day24-period01-review.md)에 **코드 적용 전**으로 기록했다. 현재 사용자 파일을 이동·삭제·수정하지 않았다.

## 시작 Git 상태와 기존 변경

저장소는 `C:/MLO01-01/Chapter3/ad_server`, HEAD는 `8f541e4 day23 - finish`였다. staged·unstaged는 없었고 기존 untracked는 `ads/management/commands/export_player_snapshot.py` 하나였다. 그 파일은 작업 시작 전에 존재한 사용자 코드이며 이번 에이전트 추가가 아니다. Chapter3는 Git 저장소가 아니고 상위 디렉터리는 접근 권한으로 확인 불가였다. 게임 저장소 HEAD와 상태는 연결된 게임 인수인계를 따른다.

## 최초 검토의 변경과 문서 정합화

- 추가 개발 파일: `tools/check_day24_logic.py`. 사용자가 지정한 Downloads 원본과 bytes 동일. 로직 변경 없음.
- 기존 사용자 코드의 새 짝 문서: `docs/server-routing/files/ads/management/commands/export_player_snapshot.py.md`. **검사기 추가 전** 현재 구현을 먼저 문서화했다.
- 새 검사기 짝 문서: `docs/server-routing/files/tools/check_day24_logic.py.md`.
- 새 범위 색인: `docs/server-routing/day24-period01-index.md`. 기존 README 부재를 복원하지 않았다.
- 이 인수인계와 `docs/server-routing/verification/day24-period01-review/` 증거를 추가했다. source 백업은 `.txt`로 보관했다.

라우팅 문서는 현 광고 명령의 `from game.models import Player`, 잘못된 `name/level/score` 조회, 실제 `schema/source` 행 키를 설명한다. 제안한 정상 게임 코드를 이미 구현한 것으로 기록하지 않았다. 환경 값·비밀번호는 인수인계나 diff에 복사하지 않았다.

## 최초 검토의 검증 결과·책임 경계

광고 Django check 종료 0, 공식 검사기 --help 종료 0. 광고 `export_player_snapshot --help`는 종료 1로 `No module named 'game'`를 재현했다. 게임 현재 폴더의 공식 1교시 검사는 명령 부재로 실패했다. 사용자 코드의 격리 시험은 잘못된 ORM 필드로 실패하고 조회만 고친 임시 사본도 8필드 계약에 실패했다. 이 임시 사본 결과를 실제 사용자 코드 통과로 주장하지 않는다. 실제 MySQL count 읽기만 성공했으며 DB 쓰기는 없었다.

검증 후 별도 문서 마감 단계에서 짝 문서·색인의 실제 시그니처·경로·직접 호출을 확인했다. 표준 감사 CLI는 README를 필수로 요구하므로 현재 저장소에서는 실패한다. 그 결과는 `routing-before.json`에 기록했고 기존 README를 임의 복원하지 않았다. 같은 스킬의 AST API로 현재 변경 Python 2개와 1:1 문서·별도 색인을 검사한 최종 결과는 `routing-final-scoped.json`에 기록한다. 게임은 표준 검사기를 사용했다.

기존 사용자 원본과 환경 파일의 hash 보존, 공식 검사기 bytes 동일 여부, 최종 Git 상태는 `finish-state.json`을 따른다. commit·stage·reset·서버 실행/종료·실제 snapshot 생성은 수행하지 않았다. 공식 checker 복사 외에 광고 Python·설정·템플릿은 수정하지 않았다.

## 다음 단계

사용자가 고친 1교시 코드는 공식 검사 12개 통과·0개 실패이며 생성 파일은 기존 게임 루트 data/exports에 있다. 정확한 PowerShell 명령은 게임 인수인계에 있다. 광고 작업 폴더에서 2교시 소비 입력은 `../Game-server/data/exports/player-cdc.ndjson`이다. 광고에서 `game` 앱을 추가하지 않는다. 2~8교시 구현은 미적용 상태다. 새 광고 DB·Kafka·Connect·Debezium 설치를 공통 준비에 추가하지 않았다.
