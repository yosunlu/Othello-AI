from pydantic import BaseModel, Field

class GameSession(BaseModel):
    game_id: str
    player1: dict
    player2: dict
    player1_color: str
    player2_color: str
    current_turn: dict
    game_state: list

    class Config:
        schema_extra = {
            "example": {
                "game_id": "1234567890",
                "player1": {
                    "username": "player1",
                    "websocket": "websocket1"
                },
                "player2": {
                    "username": "player2",
                    "websocket": "websocket2"
                },
                "player1_color": "B",
                "player2_color": "W",
                "current_turn": {
                    "player": {
                        "username": "player1",
                        "websocket": "websocket1"
                    },
                    "boardPiece": "B",
                    "turnNumber": 1
                },
                "game_state": [
                    ["", "", "", "", "", "", "", ""],
                    ["", "", "", "", "", "", "", ""],
                    ["", "", "", "", "", "", "", ""],
                    ["", "", "", "W", "B", "", "", ""],
                    ["", "", "", "B", "W", "", "", ""],
                    ["", "", "", "", "", "", "", ""],
                    ["", "", "", "", "", "", "", ""],
                    ["", "", "", "", "", "", "", ""]
                ]
            }
        }