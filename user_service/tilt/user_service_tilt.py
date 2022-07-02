from tilt import tilt
import json
from hashlib import sha256
from datetime import datetime

result = {}
result["_hash"] = sha256('<insert hashable content here>'.encode('utf-8')).hexdigest()
result["_id"] = 'user-service-tilt-01'
result["created"] = '2022-07-02T10:03:27+0000'
result["language"] = 'en'
result["modified"] = datetime.now().isoformat()
result["name"] = 'Kopfsachen e.V.'
result["status"] = 'active'
result["url"] = 'https://www.kopfsachen.org/'
result["version"] = 1

meta = tilt.Meta.from_dict(result)

print(meta)
# <tilt.tilt.Meta object at 0x7fef287928d0>

print(meta.to_dict())
