rows = [{"owner_user_id": 1}, {"owner_user_id": 2}]
for row in rows:
    if row["owner_user_id"] == 1:
        print(row["owner_user_id"])