from pydantic import BaseModel
from typing import Any, Dict, Optional


class Envelope(BaseModel):
    type: str
    payload: Optional[Dict[str, Any]] = None


class ChatPayload(BaseModel):
    text: str


