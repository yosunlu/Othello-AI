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
    
    # if session is full and there is no gamehandler yet start the game
    if len(pvpSessionManager.sessions[session_id]) == 2 and not pvpSessionManager.hasGameHandler(session_id):
        gameHandler = GameHandler(session_id, player1=pvpSessionManager.sessions[session_id][0], player2=pvpSessionManager.sessions[session_id][1])
        pvpSessionManager.setGameHandler(session_id, gameHandler)
        await pvpSessionManager.broadcast(session_id, {
            "message": "Game is starting...",
            "game_state": gameHandler.game_state
        })

        # send the color of the player to each player
        await pvpSessionManager.sendMessagetoPlayer(session_id, gameHandler.player1, f'you are player 1 and playing with {gameHandler.player1_color}')
        await pvpSessionManager.sendMessagetoPlayer(session_id, gameHandler.player2, f'you are player 2 and playing with {gameHandler.player2_color}')

        # logging the game session info
        logging.info(f"Game Handler created for session ID: {session_id}")
        logging.info(f"current_turn: {gameHandler.current_turn}")
    
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