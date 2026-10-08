# config/day23-period-07.py

23일차 7교시의 전달 표식 키 존재 여부를 연습하는 독립 실습 파일이다. 광고 runtime에서 import하지 않으며 실제 파일 전달과 DB 표식은 `ads/delivery.py`가 담당한다. 함수·클래스 정의는 없다.

`event={"event_id":"d1:impression"}`는 파일이 정의한다. 의사코드: file_delivered_at 키 존재 여부 출력 → 파일 내부 사전에 `"done"` 표식 추가 → 키 존재 여부 출력. 직접 호출은 두 번의 `print`이며 직접 실행 또는 import 시 `False`, `True`를 출력한다. `"done"`은 실습 문자열이며 실제 서버 UTC 전달 시각이나 DB 저장 결과가 아니다. `event`의 쓰기 소유자는 이 파일이며 DB와 파일을 호출하지 않는다.
