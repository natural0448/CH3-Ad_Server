# ads/reporting.py

2026-10-08 검증이 끝난 현재 구현이다. 최신 23일차 교안의 `ads/reporting.py`와 전체 AST가 일치한다. 작업 시작 시 관리 명령 아래에 있었던 집계 함수를 본문 변경 없이 이 모듈로 옮겼다. 이전 구조는 `verification/day23-period05-location-fix/before/`와 `before-docs/`에 기록했다.

## 책임과 모듈 값

사건 사전에서 일별 보고서 후보를 계산하고, 별도의 호출자가 요청할 때 후보 게시/소유자별 조회를 수행한다. 집계 함수는 DB를 호출하지 않는다. 5교시 명령은 계산과 파일 저장만 직접 호출한다.

`SEOUL = timezone(timedelta(hours=9), name="Asia/Seoul")`은 모듈이 정의하는 고정 UTC+9 시간대다. JSON 인코딩에는 `ensure_ascii=False`, 업무 키 인코딩에는 `separators=(",", ":")`를 사용한다.

## build_daily_reports(events, generated_at=None)

- `events`: `ad-event/v1` 사건 사전 iterable. 필요한 필드는 `event_id`, `decision_id`, `event_type`, `event_time`, `impression_time`, `subject`, `campaign_id`, `owner_user_id`, `slot_id`, `bid_amount`다. `event_type`은 `impression` 또는 `click`이다. 클릭과 같은 결정의 노출은 업무 값과 노출 기준 시각이 같아야 한다. 파일 내 노출 행이 클릭보다 앞에 위치할 필요는 없다.
- `generated_at`: 기본값 `None`. 값이 있으면 시간대 포함 ISO 문자열을 `.timestamps.parse_utc`에 전달한다. 값이 없거나 거짓이면 `datetime.now(timezone.utc)`를 사용한다. `datetime` 객체를 직접 받는 계약은 없다.
- 반환값: `_id` 문자열순으로 정렬된 `ad-report/v1` 사전 목록. 빈 입력이면 빈 목록이다. `_id`는 광고주·캠페인·슬롯·서울 노출일 튜플의 JSON 문자열이다. 행은 노출/클릭 수, 노출 입찰액 합계, CTR, UTC 생성 시각과 최대 사건 시각을 포함한다.

의사코드: 생성 시각 결정 → 같은 사건 ID 중복 제거/내용 충돌 거절 → 결정·종류·ID와 노출 기준 시각 검증 → 클릭의 선행 노출 및 업무 값 검증 → 서울 노출일로 그룹화 → 종류별 계수와 노출 금액 누적 → CTR 계산 → ID순 목록 반환.

현재 검증 범위: 스키마·동일 ID 충돌·ID 구성·노출 기준 시각·클릭 선행 노출/업무 값·종류 위반은 `ValueError`다. 필드 누락은 `KeyError`, 입력 타입 오류는 해당 Python 오류를 전파한다. ID/업무 필드 타입, 입찰액의 비음수 조건, 클릭 시각의 시간적 선후까지 모두 검증하는 함수로 확대 해석하지 않는다.

함수 내부 값의 소유자는 해당 함수다. `generated`는 인수 또는 UTC 현재 시각, `unique`와 `groups`는 빈 사전으로 시작한다. `unique[event_id]`는 원본 사건, `groups[key]`는 집계 행이다. `same`은 `(subject, campaign_id, owner_user_id, slot_id, bid_amount)` 비교 필드 튜플이다. `day`는 `impression_time`의 서울 날짜, `key`는 사건의 광고주·캠페인·슬롯·그 날짜다. 집계 행의 `impressions`, `clicks`, `bid_units_sum`은 0으로 시작한다. `source_max_event_time`은 최초 사건 UTC 시각에서 시작해 최대값으로 갱신한다. `ctr`는 클릭/노출이며 노출 0이면 `0.0`이다.

직접 호출: `.timestamps.parse_utc(value)`에서 UTC `datetime`을 기대한다. `datetime.now(timezone.utc)`, `datetime.astimezone(SEOUL)`, `json.dumps`, `sorted`를 사용한다. NDJSON 입출력과 DB 게시를 이 함수의 책임으로 넣지 않는다.

## publish_reports(rows)

`rows`는 `ad-report/v1` 보고서 사전 iterable이다. 각 행의 광고주·캠페인·슬롯·날짜 튜플을 JSON ID로 만들고 `_id`와 비교한다. 일치하면 `.mongo.get_db().ad_daily_reports.replace_one({"_id": row["_id"]}, row, upsert=True)`를 직접 호출한다. 처리한 행 수 정수를 반환하며 빈 입력이면 0이다.

의사코드: `count=0` → 행마다 스키마/업무 ID 검증 → 해당 업무 ID로 upsert → count 증가 → count 반환. 스키마나 ID 불일치는 `ValueError`, 필드 누락은 `KeyError`, DB 오류는 전파한다. 순차 저장이므로 중간 실패 전의 저장은 남을 수 있다. `count`와 `key`, `expected_id`는 함수 내부 값이다. 이번 5교시 검증에서는 이 함수를 실행하지 않았다.

## list_reports(owner_user_id)

`owner_user_id`는 보고서 소유자 ID이며 기본값은 없다. 현재 함수 자체에는 타입 검증이 없다. `.mongo.get_db().ad_daily_reports.find({"owner_user_id": owner_user_id}, {"_id": 0})` 후 날짜 내림차순·캠페인/슬롯 오름차순으로 정렬해 사전 목록을 반환한다. 빈 결과는 빈 목록, DB 오류는 전파한다.

의사코드: 소유자로 조회 → `_id` 제외 → 세 필드 정렬 → cursor를 목록으로 변환. 이번 5교시 검증에서는 실행하지 않았다.
