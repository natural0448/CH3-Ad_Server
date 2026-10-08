record = {"name": "민지", "score": 8, "teacher_note": "다음에 확인"}
fields = ("name", "score")
public = {name: record[name] for name in fields}
print(public)
print("teacher_note" in public)

rows = [
    {"minute": 3, "code": "b"},
    {"minute": 1, "code": "z"},
    {"minute": 3, "code": "a"},
]
rows.sort(key=lambda row: (row["minute"], row["code"]))
for row in rows:
    print(row["code"])