import json
from typing import Any

import redis as redis_lib

_REDIS_URL = "redis://localhost:6379/0"
CACHE_TTL = 60

_client: redis_lib.Redis | None = None

try:
    _client = redis_lib.Redis.from_url(_REDIS_URL, decode_responses=True, socket_connect_timeout=2)
    _client.ping()
except Exception:
    _client = None


def get(key: str) -> Any | None:
    if _client is None:
        return None
    try:
        raw = _client.get(key)
        return json.loads(raw) if raw is not None else None
    except Exception:
        return None


def set_value(key: str, value: Any, ttl: int = CACHE_TTL) -> None:
    if _client is None:
        return
    try:
        _client.setex(key, ttl, json.dumps(value, default=str))
    except Exception:
        pass


def invalidate(*patterns: str) -> None:
    if _client is None:
        return
    try:
        for pattern in patterns:
            if "*" in pattern:
                keys = _client.keys(pattern)
                if keys:
                    _client.delete(*keys)
            else:
                _client.delete(pattern)
    except Exception:
        pass
