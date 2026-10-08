# ads/management/commands/compare_ad_decisions.py

필수 first_id/second_id의 저장 결정만 읽어 chosen_campaign_id/chosen_bid_amount를 출력용 campaign_id/bid_amount로 매핑한다. 현재 입찰로 재계산하지 않는다. Command.help는 명령 설명, stdout은 Django 출력 스트림이다.

## class Command(BaseCommand)

기반 클래스: BaseCommand. 수명과 호출은 Django runner/management가 관리한다.

## Command.add_arguments(self, parser)

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | Django command 또는 테스트 인스턴스. |
| parser | 없음 | Django/argparse parser. |

반환·실패: None.

의사코드: 두 위치 인자 등록.

직접 호출: parser.add_argument. parser.add_argument는 CLI 파라미터를 등록한다. get_db는 Database, decisions.find_one은 dict/None이다. json.dumps는 문자열이며 self.stdout.write는 명령 출력 스트림에 쓴다. CommandError는 CLI 실패로 전파된다.

## Command.handle(self, *args, **options)

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | Django command 또는 테스트 인스턴스. |
| args | 가변 | 가변 CLI 위치 인자. |
| options | 가변 키워드 | first_id/second_id 등이 있는 CLI 옵션 dict. |

반환·실패: None, stdout 두 줄; 오류 CommandError.

의사코드: 두 ID 순서대로 find_one → 없음 CommandError → 저장된 근거 JSON 출력.

직접 호출: CommandError, get_db, get_db().decisions.find_one, json.dumps, self.stdout.write. parser.add_argument는 CLI 파라미터를 등록한다. get_db는 Database, decisions.find_one은 dict/None이다. json.dumps는 문자열이며 self.stdout.write는 명령 출력 스트림에 쓴다. CommandError는 CLI 실패로 전파된다.

## 변수·상수의 출처

필수 first_id/second_id의 저장 결정만 읽어 chosen_campaign_id/chosen_bid_amount를 출력용 campaign_id/bid_amount로 매핑한다. 현재 입찰로 재계산하지 않는다. Command.help는 명령 설명, stdout은 Django 출력 스트림이다.

지역 입력은 함수 인자/요청/CLI/환경 설정에서 오고 해당 함수가 작성한다. 연결은 공유 cache, 소유자는 Django 세션, ID/시간은 uuid4/UTC에서 생성한다. 테스트 값은 임시 계정/테스트 DB에서만 사용한다. secrets·password·cookie·token 실제 값은 문서에 복사하지 않는다.
