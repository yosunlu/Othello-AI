from pydantic import BaseModel
from typing import Optional
from fastapi import WebSocket

class PvpGameSessionInput(BaseModel):
    session_id: int

