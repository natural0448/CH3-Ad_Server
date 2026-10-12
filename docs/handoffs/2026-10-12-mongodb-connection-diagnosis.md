# MongoDB 접속 상태 진단 · 2026-10-12

요청은 현재 광고 서버가 MongoDB에 연결되는지 확인하는 것이다. 읽기 검사로 연결 실패와 원인을 확인했다. 서버 실행·종료·재시작, 서비스 설정 변경, 복제 초기화, DB 쓰기는 하지 않았다.

## 확인한 결과

- 로컬 27017 TCP 연결과 직접 연결 `ping`: 성공.
- 실제 광고 설정의 `ads.mongo.get_client()` 연결: ServerSelectionTimeoutError, ReplicaSetNoPrimary.
- 직접 연결 `hello`: 복제 세트 이름 없음.
- `replSetGetStatus`: OperationFailure 코드 76, `not running with --replSet`.
- `getCmdLineOpts`: 설치 기본 mongod.cfg와 설치 폴더의 data를 사용하는 서비스 프로세스, replication 설정 없음.
- 현재 직접 연결한 기본 서버의 DB 목록에는 수업 광고 DB가 없다. 수업 데이터가 삭제됐다는 뜻은 아니며 기존 수업 데이터 폴더의 내용을 이번에 조회하지 않았다.

광고 서버가 기대하는 복제 세트와 현재 포트를 점유한 standalone 서비스가 맞지 않는다. 기존 수업 config/mongo-node1.yml은 27017, ads-rs, infra/mongo/data/node1을 지정한다. 현재 서버는 이 파일로 실행되지 않았다. 환경 비밀값과 환경 파일 원문은 기록하지 않았다.

## Git와 이번 변경 구분

Chapter3는 `Git 상태 확인 불가: 저장소 아님`이고 ad_server는 별도 저장소다. 직전 커밋은 `5d29085 day24 - 2교시`이며 staged는 없다.

기존 unstaged는 README.md, ads/snapshot_intake.py, docs/server-routing/current-progress-index.md, day24-period01-index.md, files/README.md.md, files/ads/snapshot_intake.py.md, files/tools/check_day24_logic.py.md다. 기존 untracked는 write_cdc_readiness.py, inspect_player_snapshot/write_cdc_readiness 짝 문서 2개, 이전 1·2교시 및 3교시 review 검증 폴더다. 모두 이번 작업 시작 전에 존재한 변경이다.

이번 추가는 이 인수인계 문서 하나다. 소스·설정·실행 스크립트·라우팅 색인을 수정하지 않았다. ads.mongo의 지연 연결 책임과 mongo-node1.yml의 실행 설정 설명은 그대로 유효하므로 짝 라우팅 문서 재작성은 필요하지 않다. 기존 사용자 변경을 이번 변경으로 주장하지 않는다.

## 검사 범위와 제한

광고 가상환경으로 Django 설정을 로딩하고 실제 앱 연결 ping, localhost TCP 검사, 직접 Mongo 연결 ping/hello/replSetGetStatus/getCmdLineOpts 및 DB 목록 조회를 수행했다. 실제 앱 연결은 실패했고 기본 standalone 서버의 직접 연결만 성공했다. 27018/27019 TCP 검사는 timeout이다. 서비스 제어/CIM 조회는 sandbox 권한 때문에 사용할 수 없었으나 MongoDB의 실제 명령 옵션에서 서비스 모드 실행을 확인했다. 레지스트리에도 MongoDB 기본 서비스가 등록돼 있다.

코드 변경이 없어 기능 테스트와 AST 문서 검사를 반복하지 않았다. 서비스 전환 뒤 수업용 DB 접속 성공은 아직 확인하지 않았다. 24일차 3교시 파일 검사에는 MongoDB가 필요 없으며, 이번 접속 실패와 앞선 readiness 필드·빈 Command 파일의 오류는 별개다.

## 사용자가 직접 실행할 순서

1. 관리자 PowerShell에서 현재 설치 기본 서비스를 중지한다.

```powershell
Stop-Service -Name MongoDB
```

2. VS Code의 별도 PowerShell 터미널에서 수업 서버를 실행하고 이 터미널을 열어 둔다.

```powershell
cd C:\MLO01-01\Chapter3\ad_server
& "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe" --config config/mongo-node1.yml
```

3. 다른 VS Code 터미널에서 실제 광고 설정의 연결을 확인한다.

```powershell
cd C:\MLO01-01\Chapter3\ad_server
.\.venv\Scripts\Activate.ps1
python ad_config/manage.py shell -c "from ads.mongo import get_db; print(get_db().command('ping'))"
```

`ok: 1.0`이 확인되면 실제 앱 설정으로 연결된 것이다. 이미 설정된 복제 세트를 새로 초기화하거나 강제 reconfig하지 않는다. 계속 실패한다면 새 수업 서버의 로그와 상태를 확인해야 한다. 현재 수업 데이터 폴더가 존재함만 확인했으며 내부 파일을 삭제·복사하지 않았다.

## 후속 Compass 미표시 재확인

같은 날 사용자가 Compass에서 DB가 보이지 않는다고 알려 재조회했다. 직접 ping은 성공하지만 여전히 설치 기본 mongod.cfg/data 경로이고 복제 세트 이름은 없었다. 직접 DB 목록에 village_ads가 없으며 실제 광고 설정으로 연결하면 ServerSelectionTimeoutError다. 수업용 인스턴스로의 전환 성공이 아직 관찰되지 않았다. 사용자의 Compass 연결 주소와 화면은 확인하지 못했다.

수업용 서버가 실행된 뒤 Compass에서 `mongodb://localhost:27017/?replicaSet=ads-rs`로 재연결하고 DB 이름 village_ads를 확인한다. 앞서 안내한 수업용 mongod 실행 터미널의 마지막 로그 또는 Stop-Service 오류를 사용자에게 요청했다. 임의 DB 생성·복제 초기화·서버 실행은 하지 않았다. 이번 후속 변경은 이 문서의 관찰 기록 추가뿐이며 기존 Git 변경, 소스, 라우팅 문서는 그대로 유지했다.

사용자가 제공한 실제 Django ping traceback도 `No replica set members available for replica set name "ads-rs"`, ReplicaSetNoPrimary, servers=[]다. 확인한 standalone 서비스 상태와 일치한다. 이는 수업용 mongod의 시작 로그가 아니므로 서비스 중지나 새 서버 시작의 성공으로 해석하지 않는다. 관리자 PowerShell에서 Stop-Service 실행 뒤 Get-Service의 Stopped 상태를 확인하고, 별도 VS Code 터미널에서 기존 yml로 실행하도록 안내했다. Compass에는 이 전환이 완료된 뒤 기존 ads-rs 주소로 연결하도록 안내한다.

## 후속 직접 복구 완료

이후 사용자가 직접 작업을 요청해 서버를 전환했다. 앞의 연결 실패 관찰은 복구 전 기록이다. 현재 ads-rs PRIMARY, 실제 Django ping ok 1.0, village_ads의 5개 컬렉션 조회에 성공했다. [별도 복구 인수인계](2026-10-12-mongodb-connection-recovery.md)를 현재 서버 상태의 기준으로 사용한다. Compass 화면의 현재 연결은 아직 확인되지 않아 활성 주소와 오류/DB 미표시 상태를 사용자에게 요청했다.

최종 후속 답변에서 사용자가 Compass에도 DB가 표시됐다고 확인했다. 연결 복구와 사용자 관찰을 완료 결과로 기록하며 앞선 미표시는 복구 전/재연결 전 상태다.
