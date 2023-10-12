from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from src.utils.pvp_session_manager import PvpSessionManager
from src.appconfig.app_constants import PVP

router = APIRouter()
pvpSessionManager = PvpSessionManager()

@router.websocket(PVP.pvpSessionUrl)
async def pvpGameSession(websocket: WebSocket, session_id: str):
    await websocket.accept()
    await pvpSessionManager.connect(session_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await pvpSessionManager.movePiece(session_id, websocket, data)
            # await websocket.send_json(f"Session ID: {session_id}, Current User: {current_user}, Received Data: {data}")
    except WebSocketDisconnect:
        # await websocket.close()
        await pvpSessionManager.disconnect(session_id, websocket)