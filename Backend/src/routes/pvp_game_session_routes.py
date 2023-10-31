from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Cookie, Request
from fastapi.responses import JSONResponse
import logging
import asyncio
import jwt

from src.utils.pvp_session_manager import PvpSessionManager
from src.appconfig.app_constants import PVP
from src.utils.game_session import GameSession
from src.models.pvp_game_session_model import PvpGameSessionInput
from src.auth.token import verifyUserToken
from src.handlers.pvp_game_session_handler import PvpGameSessionHandler

#  TODO: handle the socket authentication in a pvp_game_session_handler.py file

router = APIRouter()
pvpSessionManager = PvpSessionManager()
logging.basicConfig(level=logging.INFO)


# the code below is a websocket endpoint that handles the pvp game session to allow the player to send and receive game data in real time
@router.websocket(PVP.pvpSessionUrl)
async def pvpGameSession(websocket: WebSocket, pvp_session_id: str):
    '''
    The websocket endpoint that handles the pvp game session to allow the player to send and receive game data in real time

    Args:
        websocket (WebSocket): the websocket object
        pvp_session_id (str): the id of the pvp session

    Raises:
        WebSocketDisconnect: if the websocket is disconnected

    Returns:
        [type]: [description]
    '''
    await websocket.accept()

    # check if the websocket is authenticated and get the user session id from the jwt token
    pvpGameSessionHandler = PvpGameSessionHandler(websocket)
    user_session_id = pvpGameSessionHandler.checkWebsocket()
    if not user_session_id:
        await websocket.close(1000, "Not authenticated")  
        return

    # connect the player to the game session
    playerConnect = await pvpSessionManager.connect(pvp_session_id, user_session_id, websocket)
    if not playerConnect:
        await websocket.close(1000, "Could not connect to the session") 
        return

    gameSession = None
    
    try:  
        while True:
            # share the game state with the players and wait for the player to make a move
            if pvpSessionManager.hasGameSession(pvp_session_id):
                gameSession = pvpSessionManager.getGameSession(pvp_session_id)
                data = await websocket.receive_json()
                isPlayerTurn = gameSession.turn(user_session_id)

                # if it's the player's turn, send the game state to the other player
                if isPlayerTurn:
                    gameSession.switchTurn()
                    await pvpSessionManager.movePiece(pvp_session_id, websocket, data)
                else: 
                    await websocket.send_json({"message": "It's not your turn yet..."})
            
            else:
                # await websocket.send_json({"message": "Waiting for players to join the room"})
                # await websocket.receive_text()
                await asyncio.sleep(1)
    
    except WebSocketDisconnect:
        await pvpSessionManager.disconnect(pvp_session_id, websocket)


    except Exception as e:
        logging.info(e)

# the code below is a get endpoint that returns a list of all the game sessions opened
@router.get(PVP.getPvpGameSessionsUrl)
def getGameSessions():
    '''
    Returns a list of all the game sessions opened
    '''
    return JSONResponse(content=pvpSessionManager.getSessions())