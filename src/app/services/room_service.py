import json
from fastapi import WebSocket

from ..core.connection_manager import ConnectionManager


class RoomService:
    def __init__(self, manager: ConnectionManager) -> None:
        self.manager = manager

    async def handle_message(self, room: str, websocket: WebSocket, raw_text: str) -> None:
        try:
            data = json.loads(raw_text)
        except Exception:
            return

        msg_type = data.get("type")
        if msg_type == "pong":
            # heartbeat помечается в маршруте, здесь игнор
            return

        if msg_type == "message":
            await self.manager.broadcast(room, json.dumps(data))


