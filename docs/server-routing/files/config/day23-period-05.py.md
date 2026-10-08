# config/day23-period-05.py

23일차 5교시의 그룹 누적과 서울 날짜 경계를 연습하는 독립 실습 파일이다. 광고 runtime에서 import하지 않으며 실제 보고서 계산은 `ads/reporting.py`가 담당한다. 함수·클래스 정의는 없다. 직접 실행 또는 import하면 아래 print가 실행된다.

`groups={}`는 파일이 정의하고 `room`을 `"광장","광장","숲"` 순으로 순회한다. `groups.setdefault(room,{"count":0})`에서 얻은 `row`의 count를 누적한다. `seoul=timezone(timedelta(hours=9))`는 이름을 따로 부여하지 않은 고정 UTC+9 시간대다. 입력 ISO 문자열은 `2026-10-04T14:59:59+00:00`, `2026-10-04T15:00:00+00:00`다.

의사코드: 방별 count 누적/출력 → UTC 두 시각 파싱 → 서울 날짜로 변환/출력. 직접 호출은 `dict.setdefault`, `print`, `timezone`, `timedelta`, `datetime.fromisoformat`, `instant.astimezone(seoul).date().isoformat()`이다. 출력은 `{'광장': {'count': 2}, '숲': {'count': 1}}`, `2026-10-04`, `2026-10-05`다. 집계/시각 변수는 이 파일이 소유하며 DB/파일 입출력이나 실제 광고 보고서 게시를 수행하지 않는다.
