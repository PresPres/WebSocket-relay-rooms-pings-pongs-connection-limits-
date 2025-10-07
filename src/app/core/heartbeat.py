import asyncio
import json
import time
from typing import Optional
from fastapi import WebSocket

from ..config import PING_INTERVAL_SEC, PONG_TIMEOUT_SEC


class Heartbeat:
    def __init__(self, websocket: WebSocket) -> None:
        self.websocket = websocket
        self._last_pong_ts: float = time.time()
        self._task: Optional[asyncio.Task] = None
        self._stopped = asyncio.Event()

    def mark_pong(self) -> None:
        self._last_pong_ts = time.time()

    async def start(self) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        self._stopped.set()
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except Exception:
                pass

    async def _run(self) -> None:
        try:
            while not self._stopped.is_set():
                await asyncio.sleep(PING_INTERVAL_SEC)
                ping_payload = {"type": "ping", "payload": {"ts": int(time.time())}}
                await self.websocket.send_text(json.dumps(ping_payload))

                # ждем понг в течение таймаута
                await asyncio.sleep(PONG_TIMEOUT_SEC)
                if time.time() - self._last_pong_ts > PONG_TIMEOUT_SEC:
                    await self.websocket.close(code=4000)
                    break
        except Exception:
            # тихо завершаем, соединение будет закрыто уровнем выше
            pass


