from fastapi import WebSocket, WebSocketDisconnect, Depends

class PvpSessionManager:

    def __init__(self) -> None:
        self.sessions: dict[str, list[WebSocket]] = {}

    async def connect(self, session_id: str, websocket: WebSocket):
        
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append(websocket)

        # ensure there is only 2 players in a session
        if len(self.sessions[session_id]) > 2:
            await websocket.close()
            return "Session is packed already get out of here!!!"
        
        return "Get Ready to be DESTROYED!!!"
    
    async def disconnect(self, session_id: str, websocket: WebSocket):
        
        if session_id in self.sessions:
            self.sessions[session_id].remove(websocket)
        
            if not self.sessions[session_id]:
                del self.sessions[session_id]
                return "Session is Empty, Bye Bye!!!"
            
    async def movePiece(self, session_id: str, websocket: WebSocket, data: dict):
        if session_id in self.sessions:
            for player in self.sessions[session_id]:
                if player != websocket:
                    await player.send_json(data)
        
    


    