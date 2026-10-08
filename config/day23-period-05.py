groups = {}
for room in ["광장", "광장", "숲"]:
    row = groups.setdefault(room, {"count": 0})
    row["count"] += 1
print(groups)


from datetime import datetime, timedelta, timezone
seoul = timezone(timedelta(hours=9))
for text in ["2026-10-04T14:59:59+00:00", "2026-10-04T15:00:00+00:00"]:
    instant = datetime.fromisoformat(text)
    print(instant.astimezone(seoul).date().isoformat())