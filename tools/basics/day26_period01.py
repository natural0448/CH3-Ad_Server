codes = ["a", "a", "b"]
unique = {}
for code in codes:
    unique[code] = code
print(list(unique))
print(len(unique))

import json

left = {"code": "a", "score": 2}
right = {"score": 2, "code": "a"}
print(json.dumps(left, sort_keys=True) == json.dumps(right, sort_keys=True))

items = [{"minute": 2, "code": "b"}, {"minute": 1, "code": "c"},
         {"minute": 1, "code": "a"}]
ordered = sorted(items, key=lambda item: (item["minute"], item["code"]))
print([item["code"] for item in ordered])
