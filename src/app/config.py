import os
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv не обязателен в рантайме
    pass


def get_int_env(name: str, default: int) -> int:
    value: Optional[str] = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


MAX_CONNECTIONS_TOTAL: int = get_int_env("MAX_CONNECTIONS_TOTAL", 1000)
MAX_CONNECTIONS_PER_ROOM: int = get_int_env("MAX_CONNECTIONS_PER_ROOM", 100)
PING_INTERVAL_SEC: int = get_int_env("PING_INTERVAL_SEC", 20)
PONG_TIMEOUT_SEC: int = get_int_env("PONG_TIMEOUT_SEC", 30)


