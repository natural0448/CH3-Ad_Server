# tools/basics/day23_record_observed.py

## 23일차 1~2교시 최종 반영

작업 시작 전 ads/events.py 실습 코드의 원본 바이트 보존본이다. 함수 정의가 없는 최상위 실습: get_db, 선택 10건 조회, pprint, 사용자 번호 입력, 실제 표시 ID에 대응하는 subject/decision 선택, impression 두 번 호출. _id UUID 내림차순은 시간순이 아니며 실제 화면 ID를 반드시 대조한다. 단독 실행 대신 README의 Django shell exec로 실행한다. db/decisions/number/decision/decision_id/subject는 조회·입력에서 나온 모듈 상태이고 사용자만 실행한다. 자동 검증은 이 파일을 실행하지 않는다.
