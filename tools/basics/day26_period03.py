import hashlib

payload = b"same"
digest = hashlib.sha256(payload).hexdigest()
print(len(digest))
print(digest == hashlib.sha256(b"same").hexdigest())
