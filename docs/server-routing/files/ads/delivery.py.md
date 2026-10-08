# ads/delivery.py

현재 23일차 7교시의 한 writer 로컬 파일 전달이다. 전달한 공개 사건 파일과 MongoDB의 `file_delivered_at` 표식을 관리한다. 게임 Player snapshot 소비와 Spark 작업은 이 모듈에 없다.

## deliver_events(output_path, limit=100)

`output_path`는 필수 문자열/Path 호환 출력 경로이며 상대경로는 실행 작업 폴더 기준이다. `limit` 기본값은 100이고 `type(limit) is int`인 1 이상 정수만 허용한다(bool 제외). 반환값은 `processed`(이번 미전달 조회 행 수), `total`(전체 DB 사건 수), `pending`(표식 없는 DB 사건 수)의 사전이다. 입력/같은 ID의 내용 충돌은 `ValueError`, 파일/JSON/필드/DB 오류는 전파한다.

의사코드: 기존 파일 읽기 또는 빈 목록 → event_id별 내용 충돌 확인 → DB에서 표식 없는 사건을 event_time/event_id 순으로 최대 limit 조회 → EVENT_FIELDS 공개 투영과 기존 ID 충돌 확인 → 전체 행을 event_time 문자열/event_id 순으로 정렬 → `.tmp` 파일 작성 → target 교체 → 조회했던 DB 사건에 UTC ISO 표식 쓰기 → 처리/전체/미전달 수 반환.

직접 호출과 기대 결과: `.exporting.read_ndjson(target)`은 사전 목록, `.mongo.get_db().ad_events.find(...).sort(...).limit(limit)`는 cursor, `.exporting.write_ndjson(temporary, ordered)`는 저장 후 해시(여기서는 사용하지 않음), `temporary.replace(target)`는 파일 교체, `collection.update_one`은 전달 표식 저장, `count_documents`는 사건 수다. `datetime.now(timezone.utc).isoformat()`은 이번 전달 완료 시각이다. 공개 필드 목록은 `.exporting.EVENT_FIELDS`에서 가져온다.

`existing`은 빈 사전에서 시작해 event_id별 공개 행을 보관한다. `pending_rows`는 조회 시점의 미전달 행 목록, `temporary`는 출력 파일명에 `.tmp`를 붙인 Path, `delivered_at`은 파일 교체 뒤 만든 UTC ISO 문자열이다. 이 함수가 파일과 전달 표식을 작성한다. 파일을 먼저 완성하므로 표식 작성 중 중단된 사건은 다음 실행에서 같은 ID/내용을 확인한 뒤 표식을 보완할 수 있다. 한 writer가 사용하는 계약이며 여러 writer 동시 실행이나 전체 표식 원자 처리를 구현한 것은 아니다. 정렬은 시각 문자열순이며 서로 다른 offset 시각의 UTC 순서를 별도로 정규화하지 않는다.

## delivery_summary(events)

`events`는 기본값 없는, `len()`과 반복을 지원하는 사건 목록이다. 반환값은 `total`, `pending` 정수 사전이다. 표식의 값이 아닌 `file_delivered_at` 키의 존재 여부로 미전달을 센다.

의사코드: total=len(events), pending=0 → 사건별 키 부재면 pending 증가 → 사전 반환. 직접 호출은 `len(events)`이며 DB나 파일은 호출하지 않는다. `total`과 `pending`은 함수가 소유한다.

현재 모듈 하단에는 `print(delivery_summary([{"event_id":"a"},{"event_id":"b","file_delivered_at":"now"}]))`가 있다. 직접 실행뿐 아니라 import 시에도 `{'total': 2, 'pending': 1}`이 출력된다. `deliver_ad_events`의 JSON stdout 앞에도 이 실습 출력이 붙을 수 있는 현재 코드 부수효과이며 이번 문서 작업에서 코드를 수정하지 않았다.
