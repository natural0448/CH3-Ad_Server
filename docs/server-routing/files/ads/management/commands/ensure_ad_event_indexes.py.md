# ads/management/commands/ensure_ad_event_indexes.py

## 23일차 1~2교시 최종 반영

BaseCommand.handle은 get_db().ad_events에 [(decision_id,1),(event_type,1)] unique=True, name=decision_event_once 인덱스를 만든다. 반복 실행 가능하며 기존 문서를 삭제·수정하지 않는다. DB 또는 기존 중복 실패는 공개 CommandError로 알리고 임의 정리하지 않는다. help와 성공 메시지는 명령 사용 안내다.

클래스 계약: `class Command(BaseCommand)`.

### `Command.handle(self, *args, **options)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 클래스 인스턴스; 클래스가 소유한 상태에만 쓴다. |
| args | 없음 | BaseCommand/fixture 가변 인자; 해당 호출 계약의 위치 인자. |
| options | 없음 | Django 관리명령 옵션 dict; 이 명령은 추가 사용자 옵션 없음. |

반환·실패: None.

의사코드: get_db → unique compound index create → 공개 완료 출력; 실패CommandError.

직접 호출: `self.stdout.write`, `get_db().ad_events.create_index`, `self.style.SUCCESS`, `CommandError`, `get_db`. 기대 결과는 위 반환·상태 변화에 사용한다. 하위 계층 내부 구현은 그 짝 문서를 따른다.
