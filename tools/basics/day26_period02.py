versions = [1, 4, 2]
chosen = 0
for version in versions:
    if version > chosen:
        chosen = version
    print(chosen)

document = {"_id": "sample:member", "version": 3, "deleted": False}
candidate = {"schema_version": "sample-current/v1", **document}
current = {}
old = current.get(candidate["_id"])
if old is None or candidate["version"] > old["version"]:
    current[candidate["_id"]] = candidate
print(current["sample:member"]["version"])
print(candidate["schema_version"])
