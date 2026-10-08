# config/day23-period-04.py

23일차 4교시의 공개 필드 투영과 두 키 정렬을 연습하는 독립 실습 파일이다. Django/광고 API에서 import하지 않으며 실제 NDJSON 내보내기 구현은 `ads/exporting.py`다. 함수·클래스 정의는 없다. 직접 실행 또는 import하면 아래 print가 실행된다.

`record={"name":"민지","score":8,"teacher_note":"다음에 확인"}`, `fields=("name","score")`는 파일이 정의한다. `public`은 record에서 fields만 뽑은 사전이다. `rows`는 `(minute,code)`가 `(3,"b"),(1,"z"),(3,"a")`인 세 사전 목록이며 파일이 소유한다.

의사코드: 공개 두 필드로 사전 생성/출력 → 비공개 키 포함 여부 출력 → rows를 minute/code 순으로 sort → code 출력. 직접 호출은 `print`, `rows.sort(key=lambda row: (row["minute"], row["code"]))`다. 출력은 `{'name': '민지', 'score': 8}`, `False`, `z`, `a`, `b`다. DB/파일 입출력이나 광고 사건 스키마 검증을 수행하지 않는다.
