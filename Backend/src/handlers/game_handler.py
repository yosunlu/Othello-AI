# Game handler is used to keep track of the game state and process data coming from user to call Buisness logic functions
from fastapi import WebSocket
import random

#  TODO: Assign users to players rather than websockets
#  TODO: Assign a color to each player
#  TODO: Update the game state in the database
#  TODO: Retrieve the game state from the database

class GameHandler:
    def __init__(self, game_id: str, player1: dict, player2: dict) -> None:
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        self.player1_color = None
        self.player2_color = None
        self.current_turn = self._initializeFirstTurn()
        self.game_state = self._initializeGameState()

    
    def _initializeGameState(self):
        '''
            # [['.', '.', '.', '.', '.', '.', '.', '.'],
            #  ['.', '.', '.', '.', '.', '.', '.', '.'], 
            #  ['.', '.', '.', '.', '.', '.', '.', '.'], 
            #  ['.', '.', '.', 'W', 'B', '.', '.', '.'], 
            #  ['.', '.', '.', 'B', 'W', '.', '.', '.'], 
            #  ['.', '.', '.', '.', '.', '.', '.', '.'], 
            #  ['.', '.', '.', '.', '.', '.', '.', '.'], 
            #  ['.', '.', '.', '.', '.', '.', '.', '.']]
        '''
        game_state = [["" for x in range(8)] for x in range(8)]
        game_state[3][3], game_state[3][4] = "W", "B"
        game_state[4][3], game_state[4][4] = "B", "W"
        return game_state


    def _initializeFirstTurn(self):
        first_turn = random.choice([self.player1, self.player2])

        if first_turn == self.player1:
            self.player1_color = "B"
            self.player2_color = "W"
        else:
            self.player1_color = "W"
            self.player2_color = "B"
        
        return {
            "player": first_turn, 
            "boardPiece": "B",
            "turnNumber": 1,
        }

    def switchTurn(self):
        if self.current_turn['player'] == self.player1:
            self.current_turn['player'] = self.player2
            self.current_turn['boardPiece'] = self.player2_color
            self.current_turn['turnNumber'] += 1
        else:
            self.current_turn['player'] = self.player1
            self.current_turn['boardPiece'] = self.player1_color
            self.current_turn['turnNumber'] += 1

    def turn(self, user_session_id: str):
        '''
        returns true if it's the player's turn
        else returns false
        '''
        if user_session_id != self.current_turn['player']['user_session_id']:
            return False
        
        return True
    
    def getColor(self, player: WebSocket):
        if player == self.player1:
            return self.player1_color
        else:
            return self.player2_color
    
    def setPlayer(self, user_session_id: str, websocket: WebSocket, player: str):
        if player == "player1":
            self.player1 = {
                "user_session_id": user_session_id,
                "websocket": websocket
            }
        else:
            self.player2 = {
                "user_session_id": user_session_id,
                "websocket": websocket
            }
    
    def removePlayer(self, websocket: WebSocket):
        if websocket == self.player1['websocket']:
            self.player1 = None
        elif websocket == self.player2['websocket']:
            self.player2 = None
    


