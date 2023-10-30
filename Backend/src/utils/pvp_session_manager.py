from fastapi import WebSocket, WebSocketDisconnect, Depends
from src.handlers.game_handler import GameHandler
import logging
from typing import Dict, List, Optional, Union

# TODO: map websocket to user in sessions
# TODO: handle connection based on user authentication
# TODO: handle reconnections. if a user reconnects to a session, map the websocket to the user

logging.basicConfig(level=logging.INFO)

class PvpSessionManager:

    def __init__(self) -> None:
        self.pvp_sessions: dict[str, list[dict[str, Union[str, WebSocket] ]]] = {}  # maps websocket and user_session_id to pvp_session_id
        self.gameHandlers: dict[str, GameHandler] = {}                              # maps pvp_session_id to gameHandler
        self.userSessions: dict[str, list[dict[str, Union[str, WebSocket] ]]] = {}  # maps user_session_id to pvp_session_id with the websocket of the user

    
    async def connect(self, pvp_session_id: str, user_session_id: str, websocket: WebSocket):
        
        # map the websocket to the pvp_session_id
        if pvp_session_id not in self.pvp_sessions:
            self.pvp_sessions[pvp_session_id] = []
        obj = {
            "user_session_id": user_session_id,
            "websocket": websocket
        }
        self.pvp_sessions[pvp_session_id].append(obj)
        logging.info(f"session ID: {pvp_session_id}, added client: {websocket} for user_session_id: {user_session_id}")

        # if there are more than 2 players (websockets) in the session disconnect the new player
        if len(self.pvp_sessions[pvp_session_id]) > 2:
            await self.sendMessagetoPlayer(pvp_session_id, websocket, {"message": "Session is full, get out of here!!!"})
            await self.disconnect(pvp_session_id, websocket)
            await websocket.close(1000, {"message": "Session is packed already get out of here!!!"})
            return
        
        # map the pvp_session_id and websocket to the user_session_id
        if user_session_id not in self.userSessions:
            self.userSessions[user_session_id] = []
        obj = {
            "pvp_session_id": pvp_session_id,
            "websocket": websocket
        }
        self.userSessions[user_session_id].append(obj)

        # if session is full (2 websockets) and there is no gamehandler yet start the game
        if len(self.pvp_sessions[pvp_session_id]) == 2 and not self.hasGameHandler(pvp_session_id):
            # gameHandler = GameHandler(pvp_session_id, player1=self.pvp_sessions[pvp_session_id][0], player2=self.pvp_sessions[pvp_session_id][1])
            gameHandler = GameHandler(pvp_session_id, 
                                      player1 = self.pvp_sessions[pvp_session_id][0], 
                                      player2 = self.pvp_sessions[pvp_session_id][1])
            self.setGameHandler(pvp_session_id, gameHandler)
            await self.broadcast(pvp_session_id, {
                "message": "Game is starting...",
                "game_state": gameHandler.game_state
            })

            # send the color of the player to each player
            # Figure out the websocket of the player based on the user_session_id and the pvp_session_id
            await self.sendMessagetoPlayer(pvp_session_id, 
                                           gameHandler.player1["websocket"], 
                                           {"message": f'you are player 1 and playing with {gameHandler.player1_color}'})
            await self.sendMessagetoPlayer(pvp_session_id, 
                                           gameHandler.player2["websocket"], 
                                           {"message": f'you are player 2 and playing with {gameHandler.player2_color}'})

            # logging the game session info
            logging.info(f"Game Handler created for session ID: {pvp_session_id}")
            logging.info(f"current_turn: {gameHandler.current_turn}")

            # for player in self.sessions[pvp_session_id]:
            #     if player != websocket:
            #         await player.send_text("text")

        # if session is full (2 websockets) and there is a gamehandler, send the game state to the new player
        elif len(self.pvp_sessions[pvp_session_id]) == 2 and self.hasGameHandler(pvp_session_id):
            gameHandler = self.getGameHandler(pvp_session_id)

            if not gameHandler.player1:
                gameHandler.setPlayer(user_session_id, websocket, "player1")
                await self.sendMessagetoPlayer(pvp_session_id, 
                                               websocket, 
                                               {"message": f'you are player 1 and playing with {gameHandler.player1_color}'})
            else:
                gameHandler.setPlayer(user_session_id, websocket, "player2")
                await self.sendMessagetoPlayer(pvp_session_id, 
                                               websocket, 
                                               {"message": f'you are player 2 and playing with {gameHandler.player2_color}'})
                        
            await self.broadcast(pvp_session_id, {
                "message": "picking up game from last state...",
                "game_state": gameHandler.game_state
            })

        return "Get Ready to be DESTROYED!!!"
    

    async def disconnect(self, pvp_session_id: str, websocket: WebSocket):
        
        if pvp_session_id in self.pvp_sessions:
            # remove the player from the pvp_sessions
            for player in self.pvp_sessions[pvp_session_id]:
                if player["websocket"] == websocket:
                    self.pvp_sessions[pvp_session_id].remove(player)
            
            # if there is a game handler, remove the player from the game handler
            if self.hasGameHandler(pvp_session_id):
                gameHandler = self.getGameHandler(pvp_session_id)
                gameHandler.removePlayer(websocket)
        
            # if no players left in the session, remove the session and game handler
            if not self.pvp_sessions[pvp_session_id]:
                del self.pvp_sessions[pvp_session_id]
                # if the session has a game handler, remove it
                if pvp_session_id in self.gameHandlers: del self.gameHandlers[pvp_session_id]
                logging.info(f"session ID: {pvp_session_id}, removed client: {websocket}")
                return "Session is Empty, Bye Bye!!!"
        
        # remove session Id from user sessions for that username
        # look for username in userSessions using its websocket
        for user in self.userSessions:
            for connection in self.userSessions[user]:
                if connection["websocket"] == websocket:
                    self.userSessions[user].remove(connection)
                    break

        logging.info(f"session ID: {pvp_session_id}, removed client: {websocket}")
        return

    # TODO: fix broadcast to send the message to the other player based on new structure
    async def broadcast(self, pvp_session_id: str, data: dict):
        if pvp_session_id in self.pvp_sessions:
            for player in self.pvp_sessions[pvp_session_id]:
                await player["websocket"].send_json(data)


    async def movePiece(self, pvp_session_id: str, websocket: WebSocket, data: dict):
        if pvp_session_id in self.pvp_sessions:
            for player in self.pvp_sessions[pvp_session_id]:
                if player["websocket"] != websocket:
                    await player["websocket"].send_json(data)


    def hasGameHandler(self, pvp_session_id: str):
        if pvp_session_id not in self.gameHandlers: return False
        return True  

    def setGameHandler(self, pvp_session_id, gameHandler):
        self.gameHandlers[pvp_session_id] = gameHandler

    def getGameHandler(self, pvp_session_id):
        return self.gameHandlers[pvp_session_id]
    
    async def sendMessagetoPlayer(self, pvp_session_id: str, player: WebSocket, message: str):
        if pvp_session_id in self.pvp_sessions:
            for p in self.pvp_sessions[pvp_session_id]:
                if p["websocket"] == player:
                    await p["websocket"].send_json(message)
                    return
        return
    
    # returns a list of all sessions available
    def get_pvp_sessions(self):
        return list(self.pvp_sessions.keys())

        
    


    