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
from src.engine.AI_engine import AI_player

from src.game.game_logic import GameLogic

# routes for the pvp game sessions.
# instantiate the pvp game session manager singleton to manage pvp game sessions
# instantiate the game logic singleton to handle game logic
router = APIRouter()
pvpSessionManager = PvpSessionManager()
gameLogic = GameLogic()
logging.basicConfig(level=logging.INFO)

logic = GameLogic()

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
                
                isPlayerTurn = gameSession.turn(user_session_id)

                # if it's the player's turn, send the game state to the other player
                if isPlayerTurn:
                    # get the game state, and the player's color from the game session
                    game_state = json.dumps(gameSession.getGameState())
                    player_color = gameSession.getPlayerColor(user_session_id)
                    new_board = gameLogic.place_piece(game_state, data['turn'], player_color)
                    if not new_board:
                        await websocket.send_json({"type": 2, "event": "invalid_move"})
                        continue
                    elif new_board == "game over":
                        # check for the winner
                        winner = gameSession.game_over()
                        await websocket.send_json({"type": 2, "event": "game_finished", "data": {"winner": winner}})
                        continue
                    #update the game state
                    gameSession.updateGameState(new_board)
                    # switch the turn
                    gameSession.switchTurn()
                    # send the game state to the other player
                    await pvpSessionManager.movePiece(pvp_session_id, websocket, new_board)
                    # collect valid moves for the next player and send them to the player
                    valid_moves = gameLogic._valid_moves(new_board, gameSession.current_turn['boardPiece'])
                    next_player = gameSession.current_turn['player']['websocket']
                    await pvpSessionManager.sendMessagetoPlayer_full(pvp_session_id, next_player, data=valid_moves)
                else: 
                    await websocket.send_json({"type": 2, "event": "placement_failure"})
            
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

@router.get(PVP.getAISuggestionUrl)
def getAIResponse(pvp_session_id: str):
    '''
    invoked when the player tries to get an AI suggestion
    sends a board state to the AI and returns the AI's response

    params:
        pvp_session_id: the id of the pvp session
    '''
    game_session = pvpSessionManager.getGameSession(pvp_session_id)
    # Initialize ai player
    # mapp B to black and W to white
    if game_session.current_turn['boardPiece'] == "B":
        ai_player = AI_player(AI_method="mcts", AI_color="black")
    else:
        ai_player = AI_player(AI_method="mcts", AI_color="white")

    # Run the AI to get the best move
    game_state = game_session.getGameState()
    best_move = ai_player.run(game_state)
    best_move = list(best_move)
    best_move[0] = best_move[0] - 1
    best_move[1] = best_move[1] - 1

    return JSONResponse(content={"message": best_move})

