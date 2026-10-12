"""광고 서버 작업 폴더에서 python check_day24_period4.py로 실행합니다."""
from copy import deepcopy

from ads.snapshot_intake import change_player


# 실제 Player와 DB를 사용하지 않는 별도 교육 원문입니다.
original = {"id": 1, "room_id": "room-01", "coins": 0, "version": 0,
            "updated_at": "2026-10-08T00:00:00+00:00"}
updated = {**original, "coins": 30, "version": 1,
           "updated_at": "2026-10-08T00:01:00+00:00"}
events = [
    {"source_kind": "teaching-fixture", "op": "r", "before": None, "after": original},
    {"source_kind": "teaching-fixture", "op": "u", "before": original, "after": updated},
    {"source_kind": "teaching-fixture", "op": "d", "before": updated, "after": None},
]
expected = [
    {"op": "r", "player_id": 1, "coins": 0, "version": 0, "deleted": False},
    {"op": "u", "player_id": 1, "coins": 30, "version": 1, "deleted": False},
    {"op": "d", "player_id": 1, "coins": 30, "version": 1, "deleted": True},
]

# 반환값과 입력 원문을 따로 확인합니다.
saved = deepcopy(events)
for event, answer in zip(events, expected):
    result = change_player(event)
    assert result == answer, f"{event['op']}: 기대 {answer}, 실제 {result}"
    assert type(result["deleted"]) is bool, "deleted는 bool이어야 합니다."
assert events == saved, "정상 호출이 원문을 변경했습니다."
print("PASS: r/u/d 해석과 원문 보존")

# 정상 원문에서 한 조건만 바꿔 거절 여부를 확인합니다.
invalid = [
    ("다른 출처", {**events[0], "source_kind": "player-snapshot"}),
    ("다른 op", {**events[0], "op": "c"}),
    ("u의 다른 ID", {**events[1], "after": {**updated, "id": 2}}),
    ("d의 after 존재", {**events[2], "after": updated}),
    ("r의 before 존재", {**events[0], "before": original}),
    ("u의 after 누락", {**events[1], "after": None}),
    ("공개 상태의 bool coins", {**events[0], "after": {**original, "coins": True}}),
    ("비공개 필드 혼입", {**events[0], "after": {**original, "user_id": 1}}),
]
for name, event in invalid:
    saved = deepcopy(event)
    try:
        change_player(event)
    except ValueError:
        pass
    else:
        raise AssertionError(f"거절하지 않았습니다: {name}")
    assert event == saved, f"실패 호출이 원문을 변경했습니다: {name}"
    print(f"PASS: {name} 거절·원문 보존")

print("PASS: 4교시 검사 완료 (실제 DB·snapshot 파일 변경 없음)")
