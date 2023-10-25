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
        self.sessions: dict[str, list[WebSocket]] = {}
        self.gameHandlers: dict[str, GameHandler] = {}

    
    async def connect(self, session_id: str, websocket: WebSocket):
        
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append(websocket)
        logging.info(f"session ID: {session_id}, added client: {websocket}")

        # if there are more than 2 players in the session disconnect the new player
        if len(self.sessions[session_id]) > 2:
            await self.sendMessagetoPlayer(session_id, websocket, "Session is full, get out of here!!!")
            await self.disconnect(session_id, websocket)
            await websocket.close(1000, "Session is packed already get out of here!!!")
            return
        

        # if session is full and there is no gamehandler yet start the game
        if len(self.sessions[session_id]) == 2 and not self.hasGameHandler(session_id):
            gameHandler = GameHandler(session_id, player1=self.sessions[session_id][0], player2=self.sessions[session_id][1])
            self.setGameHandler(session_id, gameHandler)
            await self.broadcast(session_id, {
                "message": "Game is starting...",
                "game_state": gameHandler.game_state
            })

            # send the color of the player to each player
            await self.sendMessagetoPlayer(session_id, gameHandler.player1, f'you are player 1 and playing with {gameHandler.player1_color}')
            await self.sendMessagetoPlayer(session_id, gameHandler.player2, f'you are player 2 and playing with {gameHandler.player2_color}')

            # logging the game session info
            logging.info(f"Game Handler created for session ID: {session_id}")
            logging.info(f"current_turn: {gameHandler.current_turn}")

            # for player in self.sessions[session_id]:
            #     if player != websocket:
            #         await player.send_text("text")


        return "Get Ready to be DESTROYED!!!"
    
    
    async def disconnect(self, session_id: str, websocket: WebSocket):
        
        if session_id in self.sessions:
            self.sessions[session_id].remove(websocket)
        
            # if no players left in the session, remove the session
            if not self.sessions[session_id]:
                del self.sessions[session_id]
                # if the session has a game handler, remove it
                if session_id in self.gameHandlers: del self.gameHandlers[session_id]
                logging.info(f"session ID: {session_id}, removed client: {websocket}")
                return "Session is Empty, Bye Bye!!!"
        
        logging.info(f"session ID: {session_id}, removed client: {websocket}")
        return


    async def broadcast(self, session_id: str, data: dict):
        if session_id in self.sessions:
            for player in self.sessions[session_id]:
                await player.send_json(data)


    async def movePiece(self, session_id: str, websocket: WebSocket, data: dict):
        if session_id in self.sessions:
            for player in self.sessions[session_id]:
                if player != websocket:
                    await player.send_json(data)


    def hasGameHandler(self, session_id: str):
        return session_id in self.gameHandlers    

    def setGameHandler(self, session_id, gameHandler):
        self.gameHandlers[session_id] = gameHandler

    def getGameHandler(self, session_id):
        return self.gameHandlers[session_id]
    
    async def sendMessagetoPlayer(self, session_id: str, player: WebSocket, message: str):
        if session_id in self.sessions:
            for p in self.sessions[session_id]:
                if p == player:
                    await p.send_text(message)
                    return
        return
    
    # returns a list of all sessions available
    def getSessions(self):
        return list(self.sessions.keys())

        
    


    