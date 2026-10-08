# 24일차 2교시 완료 여부 검토 · 2026-10-08

사용자가 직접 작성한 2교시를 제대로 마무리했는지 확인하도록 요청했다. 현재 소스와 데스크톱 교안의 2교시 제공부·문제 틀·완성 코드·완료 기준을 읽고 공식 검사기로 검토했다. 결과는 **미완료: 20 통과·2 실패**다. 검토 요청이므로 코드나 관리명령을 대신 작성하지 않았다.

## 시작 Git 상태와 기존 변경

Chapter3는 `Git 상태 확인 불가: 저장소 아님`이다. 대상 ad_server는 독립 저장소이며 HEAD는 `8f541e4 day23 - finish`다. staged 변경은 없었다. 시작 시 README 및 기존 라우팅 문서 6개가 수정돼 있었고 사용자 `ads/snapshot_intake.py`, 공식 검사기와 기존 day24 문서·인수인계·검증 자료가 untracked였다. 전부 작업 시작 전에 존재한 변경으로 보존했다. 전체 목록과 소스 해시는 [start-state](../server-routing/verification/day24-period02-review/start-state.json)에 있다. Git 초기화/stage/commit은 수행하지 않았다.

## 확인 결과와 교안 경계

| 항목 | 결과 |
|---|---|
| 정확한 8필드·스키마·출처 | 통과 |
| 공개 상태, bool 거절·int 범위·음수 coins | 통과 |
| ID 중복·정렬·원본 bytes checksum | 통과 |
| updated_at 시간대, 파일 내 수집값 일치 | 통과 |
| 0바이트·빈 행·사전 아닌 행 | 통과 |
| captured_at 시간대 거절 | **실패**: inspect 63행은 `parse_utc` 이름만 평가하며 호출하지 않음 |
| 검사 관리명령 | **실패**: `ads/management/commands/inspect_player_snapshot.py` 없음 |

교안의 문제 4는 `____(row["captured_at"])`에서 helper 이름을 채우는 문제다. 최종 코드는 `parse_utc(row["captured_at"])`다. 현재 다른 문제 구간은 작성되어 있으나 시간대 없는 수집 시각이 받아들여진다. 교안이 제공하는 Command를 기존 관리명령 폴더에 저장해야 실제 원본의 검사 명령을 실행할 수 있다. 누락된 파일을 현재 존재하는 라우팅으로 등록하지 않았다.

## 검사와 실행 환경

[공식 최종 결과](../server-routing/verification/day24-period02-review/official-period02-final.json)는 20 통과·2 실패, `student_sources_unchanged=true`, Mongo 미연결·SQLite 메모리만 사용한 결과다. 현재 snapshot 소스 SHA-256은 `5bfe0f260290025ac882f2f35dffb391101b6f06b01b350787a078b9b8fa7994`다. 실제 `Game-server/data/exports/player-cdc.ndjson`은 읽기 전후 원본 해시가 같고 재생성하지 않았다.

기존 Game-server Python3.12 환경에는 pymongo가 없어 첫 시도는 검사 준비 단계에서 실패했다. 광고의 기존 Python3.14 환경은 Python 경로 경고가 출력돼도 Django/pymongo import가 가능했다. sandbox 안의 이 환경은 상대 `Path.resolve()` 결과가 중복 경로로 관찰되고 기본 임시 폴더 접근이 거절돼, 최종 검사는 **절대 프로젝트/출력 경로**와 허용된 verification 폴더를 프로세스 내 tempfile 기준으로 지정해 공식 검사기를 그대로 실행했다. 검사기나 사용자 파일은 수정하지 않았다. 앞선 환경/경로 실패 시도는 같은 verification 폴더의 `official-period02*.json`에 보존했다.

최종 실행의 동등한 설정은 광고 `.venv/Scripts/python.exe -X utf8 -B`로 `runpy.run_path()`를 호출하고 `sys.argv`에 공식 검사기·절대 project·period 2·절대 output을 지정하는 것이다. `tempfile.tempdir`만 프로세스 안에서 verification 폴더로 지정했다. 공식 검사기의 Mongo 금지 mock 때문에 프로세스 종료 시 `close_client`가 `cache_info`를 찾지 못하는 부가 출력이 있었으며, 이는 보고서의 두 실패 원인과 구분했다. 실제 Mongo 연결은 없었다.

라우팅 스킬 CLI는 기존 routing README 부재로 실행 실패한다. [CLI 시작 결과](../server-routing/verification/day24-period02-review/routing-cli-before.json)에 기록하고 동일 스킬 AST API로 snapshot의 실제 3함수와 현재 색인·짝 문서를 대조했다. 최종 문서·링크·소스 보존·Git 검사는 [finish-state](../server-routing/verification/day24-period02-review/finish-state.json)를 따른다.

## 이번 변경과 최종 문서 정합화

- 수정 문서: `docs/server-routing/files/ads/snapshot_intake.py.md`, `docs/server-routing/current-progress-index.md`에 실제 격리 검사 결과와 두 실패를 반영했다.
- 추가: 이 검토 인수인계와 `docs/server-routing/verification/day24-period02-review/`의 Git·해시·검사·문서 근거.
- 개발 소스·설정·테스트·환경·원본 데이터의 추가/수정/이동/삭제 없음. 기존 변경과 이번 문서·증거 추가를 구분했다. 비밀값은 기록하지 않았다.

## 다음 확인 순서

사용자가 inspect의 `parse_utc` 한 줄을 실제 호출로 완성하고 교안의 `inspect_player_snapshot.py` Command를 기존 `C:/MLO01-01/Chapter3/ad_server/ads/management/commands/`에 저장한 뒤 광고 가상환경에서 실행한다.

```powershell
cd C:\MLO01-01\Chapter3\ad_server
python tools/check_day24_logic.py --project C:\MLO01-01\Chapter3\ad_server --period 2
python ad_config/manage.py inspect_player_snapshot --source ../Game-server/data/exports/player-cdc.ndjson
```

격리 검사 실패가 0이고 실제 원본 검사 rows·checksum이 원본과 같은지 확인하면 2교시 완료 여부를 다시 판정할 수 있다. 관리명령 파일이 없는 현재 실제 원본 Command 검사는 실행하지 않았다. 파일 검사만으로 광고 선택 context에 Player 상태가 연결되었다고 기록하지 않는다.
