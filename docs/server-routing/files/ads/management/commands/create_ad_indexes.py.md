# ads/management/commands/create_ad_indexes.py

수정 교안1교시 CODE8 그대로. Command.help는 광고 실적의 결정·종류 고유 색인 생성 안내다. get_db의 기존 ad_events에 [(decision_id,1),(event_type,1)] unique=True, name=decision_event_once를 만들고 이름만 출력한다. 기존 문서를 삭제/수정하지 않는다. 기존 ensure_ad_event_indexes 명령도 유지한다.

직접 호출의 기대 계약: get_db는 기존 Database, find_one은 dict/None, find·sort·limit는 Cursor, update_one은 UpdateResult, insert_one은 InsertOneResult, create_index는 색인 이름이다. Django render/JsonResponse는 HttpResponse, JSON parse는 dict 등 JSON 값, urlopen은 응답 stream, patch/assert는 테스트 fixture/검증을 제공한다. 하위 계층 내부는 해당 짝 문서에 있다.

## `class Command(BaseCommand)`

기반 클래스: BaseCommand. 메서드와 상태는 아래 계약을 따른다.

## `Command.handle(self, *args, **options)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |
| args | 없음 | Django decorator/view 또는 command 위치 인자; 전달만 한다. |
| options | 없음 | management command 옵션; 해당 명령은 사용하지 않는다. |

반환·실패: None; PyMongoError는 management command 호출자에 전파.

의사코드: get_db.ad_events.create_index → stdout.write(name).

직접 호출: `get_db`, `get_db().ad_events.create_index`, `self.stdout.write`.

## 상태·값 출처

지역 변수는 해당 함수가 소유하며 request/입력·서버 설정·DB 조회 또는 위 의사코드의 생성 단계에서 얻는다. 저장 snapshot과 receipt의 쓰기는 서비스/사건 계층이 맡는다. 테스트 연결·patch·가짜 응답은 해당 테스트 클래스만 소유하고 정리한다. 비밀값·쿠키·CSRF 토큰은 문서/증거에 복사하지 않는다.
