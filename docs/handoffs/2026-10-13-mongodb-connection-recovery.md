# MongoDB 연결 재발 복구 · 2026-10-13

## 요청과 완료 결과

사용자의 “또 MongoDB 커넥션이 안 되는데 해결” 요청으로 실제 광고 연결을 복구했다. 복구 당시 수업용 MongoDB PID 27664를 기존 config/mongo-node1.yml 및 infra/mongo/data/node1로 백그라운드 실행했다. 그 시점 ads-rs 단일 localhost:27017 멤버가 PRIMARY이고 Django get_db의 ping=1.0, exit 0이었다. village_ads의 기존 5개 컬렉션을 읽었다. Compass GUI를 직접 관찰하지 않았으며 재연결 주소는 mongodb://localhost:27017/?replicaSet=ads-rs다.

후속 사용자가 VS Code에서 직접 실행하겠다고 요청했다. 에이전트 서버 PID 27664에 guarded shutdown(force=False, timeoutSecs=5)을 보내 정상 종료했고, [종료 확인](../server-routing/verification/mongo-recovery-2026-10-13/stop-confirmed.json)에서 해당 PID 없음·mongod 없음·27017 listener 없음을 확인했다. 이후 추가 기동하지 않았다. 현재 상태는 복구 후 사용자 요청 중지이며 사용자가 자기 터미널에서 실행할 차례다.

기본 Windows 서비스의 자동 시작을 수동으로 바꾸는 시도는 OS 관리자 권한 부족으로 실패했다. 현재 서비스는 정상 종료했지만 StartMode=Auto는 남아 있으므로 재발 방지를 위해 아래 관리자 명령이 필요하다. 자동 승인 심사의 거절은 없었다.

## 시작 Git 상태

Chapter3 루트는 `Git 상태 확인 불가: 저장소 아님`이다. 광고 저장소 HEAD는 `4e896c7 day25 - chapter1`이며 작업 시작 시 staged·unstaged·untracked가 모두 비어 있었다. Git 저장소 초기화나 add/commit/reset은 하지 않았다. [시작 기록](../server-routing/verification/mongo-recovery-2026-10-13/start.json)에 전체 상태와 85개 개발 파일의 시작 해시를 남겼다. 기존 25일차 코드도 그대로 보존했다.


마감 검사 중 작업 시작 후 별도로 변경된 사용자 작업을 확인했다: `ads/context_projection.py`. 이번 MongoDB 복구 작업의 수정으로 주장하지 않으며 해당 코드와 짝 문서는 수정하지 않았다. 따라서 시작 해시 85개 전체가 불변이라는 판정은 하지 않는다. 이 파일의 수업 구현 검토는 이번 연결·서버 종료 요청 범위에 포함하지 않았다.

## 원인과 실제 조치

오늘 마지막 부팅은 한국 시각 09:02:44였다. 설치 기본 MongoDB 서비스는 Auto·Running, PID 5936이었다. 직접 Mongo 조회에서 설치 mongod.cfg·설치 기본 data 경로·복제 설정 없음이 확인됐다. 실제 광고 URI는 ads-rs를 기대하므로 ReplicaSetNoPrimary/ServerSelectionTimeoutError가 발생했다. 동시에 수업용 설정으로 시작한 PID 22344도 있었다. 서비스·포트 조회와 직접 DB 조회를 함께 확인했으며 포트 조회 한 번만으로 서버 구성을 단정하지 않았다.

1. 서비스 경로를 검증한 후 Set-Service Manual과 Stop-Service를 시도했으나 Windows 관리자 권한이 없어 각각 Access denied·Cannot open service로 실패했다.
2. 설치 config·설치 data 경로·복제 설정 없음이라는 guard를 통과한 서버에 shutdown(force=False)을 보내 정상 종료했다. 기본 서비스 Stopped를 확인했다.
3. 남은 수업 프로세스는 InvalidReplicaSetConfig(code 93)였다. 기존 ads-rs/version 1/단일 localhost:27017 구성을 확인하고 같은 서버에 정상 shutdown을 보냈다. 초기화나 강제 reconfig는 하지 않았다.
4. 기존 프로세스 종료·빈 포트를 확인한 뒤 같은 수업 config/data로 재기동했다. 첫 sandbox 내부 자식 PID 20636은 명령 종료 후 살아 있지 않아 연결 검사가 거절됐다. 해당 로그와 restart 기록을 보존하고, 다시 빈 포트를 확인한 뒤 sandbox 밖에서 PID 27664를 Start-Process -WindowStyle Hidden으로 기동했다. [최종 기동](../server-routing/verification/mongo-recovery-2026-10-13/persistent-restart.json)을 기준으로 한다.

서버 데이터 삭제·복사·재생성, replica 초기화·강제 재구성, 업무 문서 insert/update/delete는 하지 않았다. 정상 종료·기동에 따른 내부 체크포인트 등 물리 DB 파일 갱신은 가능하므로 데이터 디렉터리 bytes 불변을 주장하지 않는다.

## 이번 변경과 문서 정합화

에이전트가 수행한 개발 소스·환경 파일·Mongo YAML·테스트·실행 스크립트의 추가·수정·이동·삭제는 없다. 현재 상태를 docs/server-routing/current-progress-index.md의 Mongo 실행 절에 반영하고 기존 config/mongo-node1.yml의 짝 문서 링크도 색인에 명시했다. 새 파일은 이 인수인계와 docs/server-routing/verification/mongo-recovery-2026-10-13 아래 검증 기록이다. 실행 로그는 Git 무시 대상 infra/runtime/mongo-recovery-2026-10-13의 stdout-active.log·stderr-active.log이며 첫 실패 로그도 보존했다.

ads/mongo.py, ad_config/ad_config/settings.py, config/mongo-node1.yml 짝 문서의 연결·설정·작업 폴더 책임은 구현과 같아 재작성하지 않았다. 스킬 AST API로 Python 시그니처와 세 파일의 짝 문서·색인을 확인했다. [최종 검사](../server-routing/verification/mongo-recovery-2026-10-13/finish.json)에 시작/종료 소스 해시·Git 상태·라우팅 결과를 기록한다.

## 검사 결과와 제한

- [Django 관리명령](../server-routing/verification/mongo-recovery-2026-10-13/manage-ping.json): exit 0, ping 1.0, database village_ads.
- [직접 연결·복제 구성](../server-routing/verification/mongo-recovery-2026-10-13/connection-after.json): ads-rs, PRIMARY, health 1.0, 기존 config version 1/단일 멤버 유지.
- 기존 컬렉션 관찰값: campaigns 2, bids 2, decisions 40, ad_events 38, ad_daily_reports 3. 이는 복구 후 읽은 현재 값이며 이번 작업에서 생성한 문서 수가 아니다.
- [프로세스/서비스](../server-routing/verification/mongo-recovery-2026-10-13/process-after.json): 복구 당시 수업용 mongod 하나, 27017 소유자 PID 27664, 기본 서비스 Stopped/Auto. 이후 사용자 요청 종료 상태는 stop-confirmed.json을 따른다.
- 표준 routing-doc-auditor CLI는 기존 docs/server-routing/README.md 부재로 exit 2다. 기존 current-progress-index.md를 유지하고 extract_symbols/mark_documented API로 제한된 연결 소스와 문서만 대조했다. [CLI 기록](../server-routing/verification/mongo-recovery-2026-10-13/routing-cli-status.json), [마감 구조](../server-routing/verification/mongo-recovery-2026-10-13/routing-final.json)을 따른다. API 성공을 CLI 성공으로 기록하지 않는다.

코드 변경이 없어 수업 기능 테스트는 반복하지 않았다. sandbox에서 CIM 조회는 접근 거부였으므로 sandbox 밖의 읽기 조회로 실제 서비스를 확인했다. 이 권한 전환은 Windows 관리자 승격과 다르며, 실제 서비스 시작 유형 변경은 여전히 OS 권한으로 거부됐다. Python 경로 경고는 관리명령의 성공 종료와 별도 관찰이다. GUI Compass·기존 웹 서버의 활성 연결은 직접 조작하지 않았다.

## 사용자 다음 명령

에이전트가 실행한 MongoDB는 사용자 요청대로 정상 종료했고 포트가 빈 것을 확인했다. 아래를 **별도 VS Code PowerShell 터미널**에서 실행한다.

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server
& "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe" --config config/mongo-node1.yml
```

명령이 로그를 출력하고 입력 프롬프트로 돌아오지 않는 상태가 서버가 실행 중인 정상 상태다. 그 터미널을 유지한다. 다른 터미널에서 광고 연결을 확인한다.

```powershell
Set-Location C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python ad_config/manage.py shell -c "from ads.mongo import get_db; print(get_db().command('ping')['ok'])"
```

Compass의 기존 연결을 끊고 아래 주소로 다시 연결한 뒤 village_ads를 확인한다.

```text
mongodb://localhost:27017/?replicaSet=ads-rs
```

재부팅 후 설치 기본 서비스가 27017을 다시 차지하지 않게 **관리자 권한 PowerShell**에서 다음 명령을 한 번 실행한다. 일반 VS Code 터미널은 같은 권한 거부가 발생할 수 있다.

```powershell
Set-Service -Name MongoDB -StartupType Manual
Get-Service -Name MongoDB | Select-Object Name,Status,StartType
```

연결 복구 검증은 성공했고, 한 번의 관리자 설정은 에이전트 권한으로 적용하지 못했다. 정상 종료·재기동에 사용하는 기존 데이터 경로를 유지하며 DB 폴더를 삭제하거나 다시 초기화하지 않는다. 에이전트가 종료를 확인한 이후 사용자가 새로 기동한 프로세스는 사용자 소유로 취급하며 추가 중지하지 않는다.
