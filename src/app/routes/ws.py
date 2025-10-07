import json
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

from ..core.connection_manager import ConnectionManager
from ..core.heartbeat import Heartbeat
from ..services.room_service import RoomService


router = APIRouter()

manager = ConnectionManager()
service = RoomService(manager)


@router.websocket("/ws")
async def ws_endpoint(
    websocket: WebSocket,
    room: str = Query(..., min_length=1),
    client_id: Optional[str] = Query(None),
):
    allowed, reason = await manager.can_accept(room)
    if not allowed:
        await websocket.close(code=4001)
        return

    await manager.connect(room, websocket)
    hb = Heartbeat(websocket)
    await hb.start()

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
                if data.get("type") == "pong":
                    hb.mark_pong()
                    continue
            except Exception:
                pass
            await service.handle_message(room, websocket, raw)
    except WebSocketDisconnect:
        pass
    finally:
        await hb.stop()
        await manager.disconnect(websocket)


