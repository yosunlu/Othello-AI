from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import JSONResponse
import logging
import asyncio

from src.utils.pvp_session_manager import PvpSessionManager
from src.appconfig.app_constants import PVP
from src.handlers.game_handler import GameHandler

#  TODO: handle the socket authentication

router = APIRouter()
pvpSessionManager = PvpSessionManager()
logging.basicConfig(level=logging.INFO)


# the code below is a websocket endpoint that handles the pvp game session to allow the player to send and receive game data in real time
@router.websocket(PVP.pvpSessionUrl)
async def pvpGameSession(websocket: WebSocket, session_id: str):
    await websocket.accept()
    playerConnect = await pvpSessionManager.connect(session_id, websocket)
    if not playerConnect: return
    
    gameHandler = None
    
    try:  
        while True:
            # share the game state with the players and wait for the player to make a move
            if pvpSessionManager.hasGameHandler(session_id):
                gameHandler = pvpSessionManager.getGameHandler(session_id)
                data = await websocket.receive_json()
                isPlayerTurn = gameHandler.play_turn(websocket)

                # if it's the player's turn, send the game state to the other player
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

# the code below is a get endpoint that returns a list of all the game sessions opened
@router.get(PVP.getPvpGameSessionsUrl)
def getGameSessions():
    return JSONResponse(content=pvpSessionManager.getSessions())