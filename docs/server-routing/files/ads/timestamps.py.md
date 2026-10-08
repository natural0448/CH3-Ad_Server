# ads/timestamps.py

시간대가 포함된 ISO 시각을 UTC로 정규화하는 공통 경계다. 광고 파일 내보내기와 보고서 집계가 직접 호출한다. 모듈은 `datetime`, `timezone`을 표준 라이브러리에서 가져오며 자체 상태나 DB 접근이 없다.

## parse_utc(value)

`value`는 기본값 없는 ISO 시각 문자열이다. `datetime.fromisoformat`이 처리하는 문법을 그대로 사용하며 시간대가 없거나 `utcoffset()`이 없으면 `ValueError`다. 반환값은 `timezone.utc`의 aware `datetime`이다. 문자열 타입/파싱 오류는 전파한다.

의사코드: ISO 파싱 → timezone 정보 확인 → UTC로 변환 → 반환.

직접 호출: `datetime.fromisoformat(value)`에서 datetime을 얻고 `instant.utcoffset()`으로 시간대 존재를 확인한 뒤 `instant.astimezone(timezone.utc)`로 UTC datetime을 얻는다. 지역 변수 `instant`는 입력 문자열의 파싱 결과이며 함수가 소유한다.
