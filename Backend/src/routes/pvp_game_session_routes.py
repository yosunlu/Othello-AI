from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Cookie, Request
from fastapi.responses import JSONResponse
import logging
import asyncio
import jwt
import json

from src.utils.pvp_session_manager import PvpSessionManager
from src.appconfig.app_constants import PVP
from src.utils.game_session import GameSession
from src.models.pvp_game_session_model import PvpGameSessionInput
from src.auth.token import verifyUserToken
from src.handlers.pvp_game_session_handler import PvpGameSessionHandler
from src.game.game_logic import GameLogic

# routes for the pvp game sessions.
# instantiate the pvp game session manager singleton to manage pvp game sessions
# instantiate the game logic singleton to handle game logic
router = APIRouter()
pvpSessionManager = PvpSessionManager()
gameLogic = GameLogic()
logging.basicConfig(level=logging.INFO)

@router.websocket(PVP.pvpSessionUrl)
async def pvpGameSession(websocket: WebSocket, pvp_session_id: str):
    '''
    this event is invoked when the player connects to the game session
    The websocket endpoint that handles the pvp game session to allow the player to send and receive game data in real time.

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
                # get the game session
                gameSession = pvpSessionManager.getGameSession(pvp_session_id)
                data = await websocket.receive_json()
                # TODO: Create a game session handler to handle the game session logic
                isPlayerTurn = gameSession.turn(user_session_id)

                # if it's the player's turn, send the game state to the other player
                if isPlayerTurn:
                    # get the game state, and the player's color from the game session
                    game_state = json.dumps(gameSession.getGameState())
                    player_color = gameSession.getPlayerColor(user_session_id)
                    new_board = gameLogic.place_piece(game_state, data, player_color)
                    if not new_board:
                        await websocket.send_json({"message": "Invalid move"})
                        continue
                    #update the game state
                    gameSession.updateGameState(new_board)
                    # switch the turn
                    gameSession.switchTurn()
                    # send the game state to the other player
                    await pvpSessionManager.movePiece(pvp_session_id, websocket, new_board)
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
    invoked when the player tries to get a list of all the game sessions opened
    Returns a list of all the game sessions opened
    '''
    return JSONResponse(content=pvpSessionManager.getSessions())