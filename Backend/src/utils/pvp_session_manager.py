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
        
        return "Get Ready to be DESTROYED!!!"
    
    
    async def disconnect(self, session_id: str, websocket: WebSocket):
        
        if session_id in self.sessions:
            self.sessions[session_id].remove(websocket)
        
            if not self.sessions[session_id]:
                del self.sessions[session_id]
                del self.gameHandlers[session_id]
                logging.info(f"session ID: {session_id}, removed client: {websocket}")
                logging.info(f"session ID: {session_id} empty --> removed")
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
        
    


    