event = {"event_id": "d1:impression"}
print("file_delivered_at" in event)
event["file_delivered_at"] = "done"
print("file_delivered_at" in event)