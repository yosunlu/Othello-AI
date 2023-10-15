from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import logging
import asyncio

from src.utils.pvp_session_manager import PvpSessionManager
from src.appconfig.app_constants import PVP
from src.handlers.game_handler import GameHandler

#  TODO: handle the socket authentication

router = APIRouter()
pvpSessionManager = PvpSessionManager()
logging.basicConfig(level=logging.INFO)

@router.websocket(PVP.pvpSessionUrl)
async def pvpGameSession(websocket: WebSocket, session_id: str):
    await websocket.accept()
    await pvpSessionManager.connect(session_id, websocket)

    # if there are more than 2 players in the session disconnect the new player
    if len(pvpSessionManager.sessions[session_id]) > 2:
        await pvpSessionManager.disconnect(session_id, websocket)
        await websocket.close(1000, "Session is packed already get out of here!!!")
        return
    
    gameHandler = None
    
    # if session is full and there is no gamehandler yet start the game
    if len(pvpSessionManager.sessions[session_id]) == 2 and not pvpSessionManager.hasGameHandler(session_id):
        gameHandler = GameHandler(session_id, pvpSessionManager.sessions[session_id][0], pvpSessionManager.sessions[session_id][1])
        pvpSessionManager.setGameHandler(session_id, gameHandler)
        await pvpSessionManager.broadcast(session_id, {
            "message": "Game is starting...",
            "game_state": gameHandler.game_state
        })
        logging.info(f"Game Handler created for session ID: {session_id}")
        logging.info(f"current_turn: {gameHandler.current_turn}")
    
    try:  
        while True:

            if pvpSessionManager.hasGameHandler(session_id):
                gameHandler = pvpSessionManager.getGameHandler(session_id)
                data = await websocket.receive_json()
                isPlayerTurn = gameHandler.play_turn(websocket)

                if isPlayerTurn:
                    await pvpSessionManager.movePiece(session_id, websocket, data)
                else: 
                    await websocket.send_json({"message": "It's not your turn yet..."})
            
            else:
                await asyncio.sleep(1)

    
    except WebSocketDisconnect:
        await pvpSessionManager.disconnect(session_id, websocket)


    except Exception as e:
        logging.info(e)