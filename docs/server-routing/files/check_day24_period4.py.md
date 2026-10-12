# check_day24_period4.py

24일차 수정 교안 화면의 검사 코드 전체를 광고 서버 루트에 그대로 저장한 독립 검사 진입점이다. 실행은 python check_day24_period4.py다. 함수·클래스 정의는 없으며 import/실행 시 모듈 본문이 순서대로 실행된다. 실제 DB나 게임 snapshot 파일에 접근하지 않는다.

직접 호출은 copy.deepcopy, ads.snapshot_intake.change_player, zip, type, print다. change_player에서 기대한 해석 사전 또는 ValueError를 받는다. assert 불일치와 잘못된 입력의 미거절은 AssertionError로 종료한다. 정상 r/u/d와 실패 입력 모두 원문 보존을 확인한다.

original/updated는 공개 id=1, room_id="room-01", coins=0/30, version=0/1, updated_at="2026-10-08T00:00:00+00:00"/"2026-10-08T00:01:00+00:00"의 고정 사전이다. events는 teaching-fixture 출처의 r(None/original), u(original/updated), d(updated/None) 원문 세 개다. expected는 동일 ID, coins=0/30/30, version=0/1/1, deleted=False/False/True다.

saved는 deepcopy한 원문 비교값으로 두 반복문이 갱신한다. event/answer/result는 정상 입력·기대 사전·실제 반환이고 name/event는 실패 이름·변형 원문이다. invalid는 다른 출처, 다른 op, u ID 차이, d after 존재, r before 존재, u after 누락, bool coins, 비공개 user_id 혼입 8개다.

의사코드: 고정 원문/기대값 준비 → 세 정상 입력의 반환·deleted bool 확인 → 정상 원문 보존 확인/PASS → 잘못된 입력별 ValueError와 원문 보존 확인/PASS → 마지막 완료 PASS 출력.

검사는 입력 해석을 확인하며 실제 Player 삭제·binlog 수집·MongoDB 접속 검사가 아니다. 교안의 사용자 코드를 검증하는 제공 검사로 추가했으며 함수에 없는 별도 기능을 구현하지 않았다.

2026-10-12 실제 python check_day24_period4.py 실행이 exit 0으로 완료됐다. [PASS 출력](../verification/2026-10-12-day24-period04-recovery/screen-checker-final.json)은 정상 r/u/d, 8개 거절 사례, 입력 원문 보존을 확인한다.
