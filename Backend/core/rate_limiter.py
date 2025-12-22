import time
from fastapi import HTTPException, Request

# Very small in-memory rate limiter. Not distributed — suitable for local/dev.
# Limits are per-key or per-ip.

_STORE = {}

def rate_limit(max_calls: int = 60, period_seconds: int = 60):
    def _dep(request: Request):
        now = time.time()
        # Key by API key header if present, otherwise by client host
        key = request.headers.get("x-api-key") or request.client.host
        window = _STORE.setdefault(key, [])
        # Purge old timestamps
        while window and window[0] <= now - period_seconds:
            window.pop(0)
        if len(window) >= max_calls:
            raise HTTPException(status_code=429, detail="Too many requests")
        window.append(now)
        return True
    return _dep


def check_rate_for_key(key: str, max_calls: int = 60, period_seconds: int = 60) -> bool:
    """Programmatic rate check usable outside of FastAPI request dependencies.

    Returns True if allowed, otherwise raises HTTPException(429).
    """
    now = time.time()
    window = _STORE.setdefault(key, [])
    while window and window[0] <= now - period_seconds:
        window.pop(0)
    if len(window) >= max_calls:
        raise HTTPException(status_code=429, detail="Too many requests")
    window.append(now)
    return True
