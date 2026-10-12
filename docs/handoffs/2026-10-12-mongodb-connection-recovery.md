# MongoDB 연결 직접 복구 · 2026-10-12

사용자는 안내대로 실행해도 연결/Compass 표시가 해결되지 않아 직접 복구를 요청했다. 서버 전환을 완료했고 실제 광고 설정의 ping 및 수업 DB 조회가 성공했다. Compass 화면과 활성 연결 주소는 아직 직접 확인하지 못했으며 사용자가 계속 미표시를 알려 주소·오류 상태를 요청했다.

## 시작 Git 상태

Chapter3는 `Git 상태 확인 불가: 저장소 아님`이다. ad_server는 별도 저장소이고 HEAD는 `5d29085 day24 - 2교시`, staged는 없다.

시작 전 unstaged는 README.md, ads/snapshot_intake.py, docs/server-routing/current-progress-index.md, day24-period01-index.md, files/README.md.md, files/ads/snapshot_intake.py.md, files/tools/check_day24_logic.py.md다. 기존 untracked는 빈 write_cdc_readiness.py, inspect_player_snapshot/write_cdc_readiness 짝 문서 2개, 앞선 MongoDB 진단 인수인계, 1·2교시 및 3교시 검증 폴더다. [시작 기록](../server-routing/verification/mongo-recovery-2026-10-12/start.json)에 전체 목록과 75개 개발 파일의 시작 SHA-256을 보존했다. 전부 작업 시작 전에 존재한 변경으로 취급했다. stage·commit·reset은 하지 않았다.

## 원인과 실제 조치

기본 MongoDB 서비스 PID 5836과 수업용 프로세스 PID 12292가 동시에 있었다. 27017 포트는 기본 서비스가 사용했고 실제 명령 옵션은 설치 기본 mongod.cfg/data, replication 없음이었다. 광고 설정은 ads-rs를 기대하므로 ReplicaSetNoPrimary/ServerSelectionTimeoutError가 발생했다.

중지 전 guard가 한 번 취소된 뒤 서비스·포트 소유자를 다시 확인했다. 재확인 시 기본 서비스와 포트 소유자가 일치했으나 Stop-Service는 OS 서비스 제어 권한 때문에 Cannot open MongoDB service로 실패했다. 자동 승인 심사 거절은 없었다. 실제 MongoDB의 설정/데이터 경로·service 옵션·standalone 상태를 검증한 다음 admin shutdown(force=False)을 사용해 기본 서버를 정상 종료했다. 기본 서비스 Stopped를 확인했다.

그 뒤 기존 수업용 프로세스가 포트를 사용했지만 replSetGetStatus는 코드 93 InvalidReplicaSetConfig였다. replSetGetConfig에서 기존 ads-rs, version 1, 단일 localhost:27017 멤버를 확인했다. 충돌 상태에서 시작한 프로세스를 정상 종료하고, 포트가 비고 이전 PID가 종료됐음을 확인한 뒤 같은 설정/데이터 폴더로 재시작했다. 두 서버 동시 실행과 관련된 시작 상태로 판단했으며 기존 수업 프로세스의 전체 시작 로그가 없어 더 세부적인 내부 원인은 확정하지 않는다. replica 초기화·강제 재구성은 하지 않았다.

현재 수업용 PID는 **9900**이며 Start-Process -WindowStyle Hidden으로 백그라운드 실행 중이다. 작업 폴더는 ad_server, 설정은 config/mongo-node1.yml의 절대 경로, 기존 데이터 폴더는 infra/mongo/data/node1이다. 로그는 infra/runtime/mongo-recovery-2026-10-12/stdout.log 및 stderr.log, 시작 정보는 [restart.json](../server-routing/verification/mongo-recovery-2026-10-12/restart.json)에 있다. 서비스의 Auto 시작 유형은 변경하지 않았다.

## 변경 파일과 책임 경계

개발 소스·설정·테스트·실행 스크립트의 추가·수정·이동·삭제는 없다. 업무 레코드 생성/수정/삭제, 데이터 폴더 삭제/복사, 재수출은 하지 않았다. MongoDB 정상 종료/기동의 체크포인트 등 물리 DB 파일 갱신은 발생할 수 있으므로 데이터 디렉터리의 bytes 불변을 주장하지 않는다.

문서 변경은 현재 실행 상태를 추가한 docs/server-routing/current-progress-index.md, 과거 진단에 복구 결과를 연결한 docs/handoffs/2026-10-12-mongodb-connection-diagnosis.md다. 새 파일은 이 인수인계와 docs/server-routing/verification/mongo-recovery-2026-10-12/ 검증 기록이다. infra/runtime 아래 stdout/stderr는 실행 로그이며 Git 무시 대상이다.

ads/mongo.py, ad_config/ad_config/settings.py, config/mongo-node1.yml의 1:1 짝 문서를 읽어 현재 연결 책임·설정 로딩·실행 폴더와 일치함을 확인했다. 코드 변화가 없어 짝 문서를 재작성하지 않았고 현재 색인에 runtime 결과만 추가했다. 기존 3교시 readiness/빈 관리명령 오류는 이 작업에서 수정하지 않았다.

## 검증 결과

- 실제 광고 설정 `get_db().command('ping')`: ok 1.0.
- 실제 Django 명령 `python ad_config/manage.py shell -c "from ads.mongo import get_db; print(get_db().command('ping')['ok'])"`: exit 0, 출력 1.0. [검사 기록](../server-routing/verification/mongo-recovery-2026-10-12/manage-ping.json).
- hello/replSetGetStatus: ads-rs, localhost:27017, PRIMARY, health 1.0.
- 기존 replica 구성은 version 1과 단일 멤버로 유지됨. [이전 구성](../server-routing/verification/mongo-recovery-2026-10-12/classroom-replica-before.json), [연결·현재 구성](../server-routing/verification/mongo-recovery-2026-10-12/connection-after.json).
- village_ads 컬렉션과 당시 문서 수: campaigns 2, bids 2, decisions 30, ad_events 26, ad_daily_reports 3. 사용자 업무 DB에는 읽기 조회만 수행했다.
- 기본 서비스는 Stopped, 27017 소유자는 PID 9900, mongod는 수업용 하나만 실행 중이다. [프로세스 확인](../server-routing/verification/mongo-recovery-2026-10-12/process-after.json).

별도 기능 테스트는 코드 변경이 없어 반복하지 않았다. 한 검사 셀에서 관리명령 ping 자체는 성공했지만 뒤의 sandbox Get-Process 조회가 실패해 셀 종료 코드가 1로 표시됐다. 명령 exit 상태를 별도로 보존한 위 manage-ping.json의 exit 0을 기준으로 한다. 기본 serverStatus 조회는 드라이버 InvalidBSON으로 실패해 PID 근거로 사용하지 않았고 Windows 서비스/포트 조회와 MongoDB getCmdLineOpts로 대상과 상태를 확인했다.

최종 개발 파일 보존·AST/문서 링크·Git 검사는 [마감 기록](../server-routing/verification/mongo-recovery-2026-10-12/finish.json)을 따른다. 검사한 시작 개발 파일 75개 중 74개의 해시는 유지됐다. 작업 중 사용자가 snapshot_intake에 change_player를 추가하고 write_player_change_fixture 관리명령을 새로 저장한 것을 관찰했다. Mongo 복구 작업에서는 그 변경을 보존했고 Python 소스에 쓰지 않았다. 이후 4교시 검토 요청은 별도 작업으로 구분한다. 사용자가 후속 답변으로 Compass에서 DB가 나왔다고 확인했다. 이 GUI 확인은 사용자 관찰이며 에이전트의 직접 화면 검사는 아니다.

## 사용자 다음 단계와 재부팅 뒤 순서

현재 서버를 중복 실행하지 않는다. Compass의 기존 연결을 끊고 아래 주소로 다시 연결한 뒤 village_ads를 확인한다.

```text
mongodb://localhost:27017/?replicaSet=ads-rs
```

현재 연결에도 DB가 보이지 않으면 사용 중인 실제 주소와 연결 오류/DB 필터 상태를 확인해야 한다. 새 DB를 생성하거나 기존 데이터를 다른 서버로 복사할 필요는 없다.

기본 서비스는 Auto이므로 재부팅 후에는 다시 기본 인스턴스가 27017을 사용할 수 있다. 그때 관리자 PowerShell에서 기본 서비스를 멈추고, 수업용 서버가 실행 중이지 않을 때만 다음 명령을 별도 VS Code 터미널에서 실행한다.

```powershell
Stop-Service -Name MongoDB
```

```powershell
cd C:\MLO01-01\Chapter3\ad_server
& "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe" --config config/mongo-node1.yml
```

VS Code 터미널에서 수동 실행한 경우 그 터미널을 유지한다. 다른 터미널의 실제 연결 검사는 다음과 같다.

```powershell
cd C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python ad_config/manage.py shell -c "from ads.mongo import get_db; print(get_db().command('ping')['ok'])"
```
