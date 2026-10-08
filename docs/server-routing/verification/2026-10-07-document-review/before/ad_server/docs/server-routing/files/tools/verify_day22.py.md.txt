# tools/verify_day22.py

--mongod 필수, --port 기본 27107/범위 1~65535. infra/runtime의 새 UUID 폴더에서 ads-sync-validation 단일 노드를 초기화하고 PRIMARY 확인 후 테스트를 실행한다. 결과 출력/종료 코드를 확인하고 skip은 실패다. 자신이 만든 서버만 종료하며 로그는 보존한다. 정상 main 반환은 테스트 종료 코드 int다.

## main()

파라미터 없음.

반환·실패: 테스트 종료 코드 int. 잘못된 인자/기동/검증 실패는 예외 또는 parser 종료..

의사코드: --mongod 필수, --port 기본 27107/범위 1~65535. infra/runtime의 새 UUID 폴더에서 ads-sync-validation 단일 노드를 초기화하고 PRIMARY 확인 후 테스트를 실행한다. 결과 출력/종료 코드를 확인하고 skip은 실패다. 자신이 만든 서버만 종료하며 로그는 보존한다. 정상 main 반환은 테스트 종료 코드 int다.

직접 호출: (owned / 'mongod.log').open, MongoClient, Path, Path(__file__).resolve, RuntimeError, argparse.ArgumentParser, dict, direct.admin.command, direct.admin.command('hello').get, direct.close, log.close, owned.mkdir, owned.relative_to, owned.resolve, owned.resolve().is_relative_to, parser.add_argument, parser.error, parser.parse_args, print, range, runtime.mkdir, runtime.resolve, server.poll, server.terminate, server.wait, sock.bind, socket.socket, str, subprocess.Popen, subprocess.run, time.sleep, uuid.uuid4. MongoClient의 command 결과로 ping·PRIMARY 상태를 확인한다. subprocess.Popen은 자신이 만든 mongod 프로세스, subprocess.run은 CompletedProcess를 반환한다. socket.bind는 포트 사용 가능 여부를 검사하고 대기/종료 함수는 해당 자식 프로세스만 처리한다.

## 변수·상수의 출처

--mongod 필수, --port 기본 27107/범위 1~65535. infra/runtime의 새 UUID 폴더에서 ads-sync-validation 단일 노드를 초기화하고 PRIMARY 확인 후 테스트를 실행한다. 결과 출력/종료 코드를 확인하고 skip은 실패다. 자신이 만든 서버만 종료하며 로그는 보존한다. 정상 main 반환은 테스트 종료 코드 int다.

지역 입력은 함수 인자/요청/CLI/환경 설정에서 오고 해당 함수가 작성한다. 연결은 공유 cache, 소유자는 Django 세션, ID/시간은 uuid4/UTC에서 생성한다. 테스트 값은 임시 계정/테스트 DB에서만 사용한다. secrets·password·cookie·token 실제 값은 문서에 복사하지 않는다.
