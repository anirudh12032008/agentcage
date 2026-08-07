import os
import time
from collections import defaultdict
from fastapi import HTTPException, Request
API_KEY = os.environ.get("ARENA_API_KEY")
RATE_LIMIT = 30
R = 60
_request_log: dict[str, list[float]] = defaultdict(list)

def check_api_key(request: Request):
    if not API_KEY:
        return
    if request.header.get("x-api-key") != API_KEY:
        raise HTTPException(status_code=401, detail="invalid api")

def check_rate_limit(request: Request):
    ip = request.client.host if request.client else "unknown"
    now = time.monotonic()
    ts = _request_log[ip]
    cutoff = now - R
    while ts and ts[0] < cutoff:
        ts.pop(0)
    if len(ts) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="rate limit!! tf u doing?")
    ts.append(now)
    