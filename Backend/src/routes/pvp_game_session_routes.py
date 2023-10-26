from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Cookie, Request
from fastapi.responses import JSONResponse
import logging
import asyncio
import jwt

from src.utils.pvp_session_manager import PvpSessionManager
from src.appconfig.app_constants import PVP
from src.handlers.game_handler import GameHandler
from src.models.pvp_game_session_model import PvpGameSessionInput
from src.auth.token import verifyUserToken

#  TODO: handle the socket authentication in a pvp_game_session_handler.py file

router = APIRouter()
pvpSessionManager = PvpSessionManager()
logging.basicConfig(level=logging.INFO)


# the code below is a websocket endpoint that handles the pvp game session to allow the player to send and receive game data in real time
@router.websocket(PVP.pvpSessionUrl)
async def pvpGameSession(websocket: WebSocket, session_id: str):
    await websocket.accept()
    if not websocket._cookies: 
        await websocket.close(1000, "Not authenticated")
        return
    
    # check if the user is has a jwt token for authentication
    tokenCookie = websocket._cookies['token']
    if not tokenCookie:
        await websocket.close(1000, "Not authenticated")
        return
    
    # verify the jwt token
    try:
        # verify the jwt token
        # jwt_token = jwt_token.split(" ")[1]
        payload = verifyUserToken(tokenCookie)
        userInfo = {
            payload['username']: {
                "user_id": payload['user_id'],
                "user_privilege": payload['user_privilege']
            }
        }
    
    except Exception as e:
        logging.info(e)
        return
    
    playerConnect = await pvpSessionManager.connect(session_id, userInfo, websocket)
    if not playerConnect: return
    
    gameHandler = None
    
    try:  
        while True:
            # share the game state with the players and wait for the player to make a move
            if pvpSessionManager.hasGameHandler(session_id):
                gameHandler = pvpSessionManager.getGameHandler(session_id)
                data = await websocket.receive_json()
                isPlayerTurn = gameHandler.turn(websocket)

                # if it's the player's turn, send the game state to the other player
                if isPlayerTurn:
                    gameHandler.switchTurn()
                    await pvpSessionManager.movePiece(session_id, websocket, data)
                else: 
                    await websocket.send_json({"message": "It's not your turn yet..."})
            
            else:
                # await websocket.send_json({"message": "Waiting for players to join the room"})
                # await websocket.receive_text()
                await asyncio.sleep(1)
    
    except WebSocketDisconnect:
        await pvpSessionManager.disconnect(session_id, websocket)


    except Exception as e:
        logging.info(e)

# the code below is a get endpoint that returns a list of all the game sessions opened
@router.get(PVP.getPvpGameSessionsUrl)
def getGameSessions():
    return JSONResponse(content=pvpSessionManager.getSessions())