from fastapi import WebSocket, WebSocketDisconnect, Depends
from src.utils.game_session import GameSession
import logging
from typing import Dict, List, Optional, Union

# TODO: map websocket to user in sessions
# TODO: handle connection based on user authentication
# TODO: handle reconnections. if a user reconnects to a session, map the websocket to the user

logging.basicConfig(level=logging.INFO)

class PvpSessionManager:

    def __init__(self) -> None:
        self.pvp_sessions: dict[str, list[dict[str, Union[str, WebSocket] ]]] = {}  # maps websocket and user_session_id to pvp_session_id
        self.gameSessions: dict[str, GameSession] = {}                              # maps pvp_session_id to GameSession
        self.userSessions: dict[str, list[dict[str, Union[str, WebSocket] ]]] = {}  # maps user_session_id to pvp_session_id with the websocket of the user

    
    async def connect(self, pvp_session_id: str, user_session_id: str, websocket: WebSocket):
        '''
        connects the player to the pvp session. handles the connection of the player to the session

        params:
            pvp_session_id: str
            user_session_id: str
            websocket: WebSocket

        returns a message if the player is connected to the session
        returns None if the player is not connected to the session
        '''
        
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

        # if session is full (2 websockets) and there is no gameSession yet start the game
        if len(self.pvp_sessions[pvp_session_id]) == 2 and not self.hasGameSession(pvp_session_id):
            # gameSession = GameSession(pvp_session_id, player1=self.pvp_sessions[pvp_session_id][0], player2=self.pvp_sessions[pvp_session_id][1])
            gameSession = GameSession(pvp_session_id, 
                                      player1 = self.pvp_sessions[pvp_session_id][0], 
                                      player2 = self.pvp_sessions[pvp_session_id][1])
            self.setGameSession(pvp_session_id, gameSession)
            await self.broadcast(pvp_session_id, {
                "message": "Game is starting...",
                "game_state": gameSession.game_state
            })

            # send the color of the player to each player
            # Figure out the websocket of the player based on the user_session_id and the pvp_session_id
            await self.sendMessagetoPlayer(pvp_session_id, 
                                           gameSession.player1["websocket"], 
                                           {"message": f'you are player 1', "color": f'{gameSession.player1_color}'})
            await self.sendMessagetoPlayer(pvp_session_id, 
                                           gameSession.player2["websocket"], 
                                           {"message": f'you are player 2', "color": f'{gameSession.player2_color}'})

            # logging the game session info
            logging.info(f"Game Handler created for session ID: {pvp_session_id}")
            logging.info(f"current_turn: {gameSession.current_turn}")

            # for player in self.sessions[pvp_session_id]:
            #     if player != websocket:
            #         await player.send_text("text")

        # if session is full (2 websockets) and there is a gameSession, send the game state to the new player
        elif len(self.pvp_sessions[pvp_session_id]) == 2 and self.hasGameSession(pvp_session_id):
            gameSession = self.getGameSession(pvp_session_id)

            if not gameSession.player1:
                gameSession.setPlayer(user_session_id, websocket, "player1")
                await self.sendMessagetoPlayer(pvp_session_id, 
                                               websocket, 
                                               {"message": f'you are player 1', "color": f'{gameSession.player1_color}'})
            else:
                gameSession.setPlayer(user_session_id, websocket, "player2")
                await self.sendMessagetoPlayer(pvp_session_id, 
                                               websocket, 
                                               {"message": f'you are player 2', "color": f'{gameSession.player2_color}'})
                        
            await self.broadcast(pvp_session_id, {
                "message": "picking up game from last state...",
                "game_state": gameSession.game_state
            })

        return "Get Ready to be DESTROYED!!!"
    

    async def disconnect(self, pvp_session_id: str, websocket: WebSocket):
        '''
        disconnects the player from the pvp session and the game session if there is one

        params:
            pvp_session_id: str
            websocket: WebSocket

        returns a message if the player is disconnected from the session
        returns None if the player is not disconnected from the session
        '''
        
        if pvp_session_id in self.pvp_sessions:
            # remove the player from the pvp_sessions
            for player in self.pvp_sessions[pvp_session_id]:
                if player["websocket"] == websocket:
                    self.pvp_sessions[pvp_session_id].remove(player)
            
            # if there is a game session, remove the player from the game session
            if self.hasGameSession(pvp_session_id):
                gameSession = self.getGameSession(pvp_session_id)
                gameSession.removePlayer(websocket)
        
            # if no players left in the session, remove the session and game handler
            if not self.pvp_sessions[pvp_session_id]:
                del self.pvp_sessions[pvp_session_id]
                # if the session has a game handler, remove it
                if pvp_session_id in self.gameSessions: del self.gameSessions[pvp_session_id]
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

    async def broadcast(self, pvp_session_id: str, data: dict):
        '''
        broadcasts the data to all players in the pvp session

        params:
            pvp_session_id: str
            data: dict

        returns None
        '''
        if pvp_session_id in self.pvp_sessions:
            for player in self.pvp_sessions[pvp_session_id]:
                await player["websocket"].send_json(data)


    async def movePiece(self, pvp_session_id: str, websocket: WebSocket, data: dict):
        '''
        moves the piece in the game session and broadcasts the game state to all players in the pvp session

        params:
            pvp_session_id: str
            websocket: WebSocket
            data: dict

        returns None
        '''
        if pvp_session_id in self.pvp_sessions:
            for player in self.pvp_sessions[pvp_session_id]:
                if player["websocket"] != websocket:
                    await player["websocket"].send_json({"message": "moved", "game_state": data})


    def hasGameSession(self, pvp_session_id: str):
        '''
        returns true if the pvp session has a game session
        else returns false

        params:
            pvp_session_id: str
        '''
        if pvp_session_id not in self.gameSessions: return False
        return True  

    def setGameSession(self, pvp_session_id, gameSession):
        '''
        sets the game session for the pvp session

        params:
            pvp_session_id: str
            gameSession: GameSession
        '''
        self.gameSessions[pvp_session_id] = gameSession

    def getGameSession(self, pvp_session_id):
        '''
        returns the game session of the pvp session

        params:
            pvp_session_id: str

        returns GameSession
        '''
        return self.gameSessions[pvp_session_id]
    
    async def sendMessagetoPlayer(self, pvp_session_id: str, player: WebSocket, message: str):
        '''
        sends a message to a player in the pvp session

        params:
            pvp_session_id: str
            player: WebSocket
            message: str

        returns None
        '''
        if pvp_session_id in self.pvp_sessions:
            for p in self.pvp_sessions[pvp_session_id]:
                if p["websocket"] == player:
                    await p["websocket"].send_json(message)
                    return
        return
    
    def get_pvp_sessions(self):
        '''
        returns a list of all the pvp sessions

        returns List[str]
        '''
        return list(self.pvp_sessions.keys())

        
    


    