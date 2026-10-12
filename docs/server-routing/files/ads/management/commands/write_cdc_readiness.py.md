# ads/management/commands/write_cdc_readiness.py

## 현재 사용자 구현 · 4교시 복구 중 사전 정합화

사용자가 교안의 제공 코드를 직접 입력해 현재는 Command 클래스가 있다. 아래 빈 파일 관찰은 입력 전의 이력이다. 이번 에이전트는 이 사용자 관리명령을 교체하지 않는다.

### class Command(BaseCommand)

django.core.management.base.BaseCommand를 상속한다. help는 "경로 존재와 CDC 미구성 상태를 분리한 준비 기록을 저장합니다."다. 모듈은 json, Path, BaseCommand/CommandError, ads.snapshot_intake.readiness를 import한다.

### Command.add_arguments(self, parser)

self는 명령 인스턴스, parser는 Django ArgumentParser이며 기본값 없이 받는다. None 반환이다. --output은 required=True인 출력 파일 문자열이다. --mysql-config, --connect-home, --debezium-dir는 선택 경로 문자열이며 미제공 기본값 None이고 options에서는 밑줄 이름으로 전달된다.

### Command.handle(self, *args, **options)

args는 Django 위치 인수로 사용하지 않는다. options.output은 필수 출력 파일 경로이며 나머지 세 경로는 선택 입력이다. None을 반환하고 실제 readiness 사전을 stdout JSON과 출력 JSON에 기록한다.

의사코드: options.get으로 세 선택 경로 전달 → readiness 결과 받기 → output의 부모 mkdir → UTF-8·정렬 키·indent=2·마지막 newline으로 JSON 저장 → stdout JSON 출력.

현재 [공식 3교시 검사](../../../../verification/2026-10-12-day24-period04-recovery/official-period03-final.json) 8개와 실제 data/contracts/cdc-readiness.json 저장이 통과했다. 사용자가 직접 입력한 명령의 bytes는 유지했으며 readiness의 누락된 반환 필드만 모듈에서 복구했다.

직접 호출은 readiness, Path/mkdir/write_text, json.dumps, self.stdout.write다. readiness에서 현재 경로 관찰 사전을 기대하며 DB나 외부 프로세스를 호출하지 않는다. OSError/ValueError/TypeError를 CommandError로 변환한다. result는 readiness의 반환값, target은 options.output을 Path로 변환한 값이다. stdout은 ensure_ascii=False, sort_keys=True다. 실제 MySQL/Connect/Debezium 상태를 추가 조회하지 않는다.

## 과거 빈 파일 관찰

2026-10-12 검토 도중 사용자 작업으로 새로 관찰한 3교시 관리명령 초안 파일이다. 10:27경 관찰한 파일은 0 bytes였으며 import·클래스·함수·메서드·상수 정의가 없었다. Command 실행 연결 완료로 등록하지 않는다.

앞선 요청의 검증 범위는 1·2교시였고 당시에는 이 파일을 완성하거나 실행하지 않았다. 대응하는 모듈 readiness 함수의 실제 관찰은 [snapshot_intake.py 짝 문서](../../snapshot_intake.py.md)를 따른다. 빈 파일의 존재는 실행 가능한 Django 관리명령이나 CDC 기동 증거가 아니다.

## 수정 교안의 3교시 실행 검토 · 2026-10-12

별도 검토에서도 파일은 0 bytes다. `python ad_config/manage.py write_cdc_readiness --output <검증 폴더>/readiness-attempt.json`을 광고 서버 루트에서 실행하면 Django의 `load_command_class`가 `module.Command()`를 찾는 단계에서 `AttributeError: module 'ads.management.commands.write_cdc_readiness' has no attribute 'Command'`를 발생시킨다. 종료 코드 1이며 결과 파일은 생성되지 않았다. [재현 결과](../../../../verification/2026-10-12-day24-period03-review/command-result.json), [오류 로그](../../../../verification/2026-10-12-day24-period03-review/command-error.txt)를 따른다.

파일을 채우거나 함수·인수·반환값·외부 호출을 임의로 구현하지 않았다. 교안은 링크로 제공하는 Command 전체를 이 경로에 저장하도록 안내한다. 아직 실행 가능한 명령 시그니처와 옵션 정의는 없으며, `--output` 등 교안의 계약을 현재 구현으로 등록하지 않는다.
