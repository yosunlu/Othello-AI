from fastapi import WebSocket
import random

#  TODO: Assign users to players rather than websockets
#  TODO: Assign a color to each player
#  TODO: Update the game state in the database
#  TODO: Retrieve the game state from the database

class GameHandler:
    def __init__(self, game_id: str, player1: WebSocket, player2: WebSocket) -> None:
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        self.current_turn = self._initializeFirstTurn()
        self.game_state = self._initializeGameState()

    def _initializeFirstTurn(self):
        return random.choice([self.player1, self.player2])
    
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

    def _switchTurn(self):
        if self.current_turn == self.player1:
            self.current_turn = self.player2
        else:
            self.current_turn = self.player1

    def play_turn(self, player: WebSocket):
        if player != self.current_turn:
            return False

        self._switchTurn()
        return True
    


