from __future__ import annotations

import asyncio
from typing import Dict, Set, Tuple
from fastapi import WebSocket

from ..config import MAX_CONNECTIONS_TOTAL, MAX_CONNECTIONS_PER_ROOM


class ConnectionManager:
    def __init__(self) -> None:
        self._room_to_clients: Dict[str, Set[WebSocket]] = {}
        self._client_to_room: Dict[WebSocket, str] = {}
        self._lock = asyncio.Lock()

    @property
    def total_connections(self) -> int:
        return len(self._client_to_room)

    def room_size(self, room: str) -> int:
        return len(self._room_to_clients.get(room, set()))

    async def can_accept(self, room: str) -> Tuple[bool, str]:
        async with self._lock:
            if self.total_connections >= MAX_CONNECTIONS_TOTAL:
                return False, "global limit reached"
            if self.room_size(room) >= MAX_CONNECTIONS_PER_ROOM:
                return False, "room limit reached"
            return True, "ok"

    async def connect(self, room: str, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._room_to_clients.setdefault(room, set()).add(websocket)
            self._client_to_room[websocket] = room

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            room = self._client_to_room.pop(websocket, None)
            if room is None:
                return
            clients = self._room_to_clients.get(room)
            if clients is not None:
                clients.discard(websocket)
                if not clients:
                    self._room_to_clients.pop(room, None)

    async def broadcast(self, room: str, message_text: str) -> None:
        # не блокируем весь менеджер на отправку
        clients = list(self._room_to_clients.get(room, set()))
        if not clients:
            return
        coros = []
        for ws in clients:
            coros.append(ws.send_text(message_text))
        await asyncio.gather(*coros, return_exceptions=True)


