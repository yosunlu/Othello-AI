import othello
from alpha_beta_ai import AlphaBetaAI
from mcts_ai import MCTSAI

def othello_index_to_row_col(index: str) -> tuple[int, int]:
    """
    Convert an Othello board index (e.g., 'f5') to row and column indices (1-8).

    Args:
    index (str): The Othello board index, e.g., 'f5'.

    Returns:
    tuple of int: The row and column indices (1-8).
    """
    # Map each letter to a corresponding column number
    col_map = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

    # Extract the column letter and row number from the index
    col, row = index[0], index[1]

    # Return the row and column as integers
    return int(row), col_map[col.lower()]

class AI_player:
    def __init__(self, AI_method: str = "alpha_beta", AI_color: str = 'black'):
        # Initialize the AI player with a specified method and color
        if AI_method == "alpha_beta":
            self.AI_method = AlphaBetaAI
        elif AI_method == "mcts":
            self.AI_method = MCTSAI
        else:
            raise ValueError("AI_method must be either alpha_beta or mcts")
        
        # Set the player color
        if AI_color == 'black':
            self.AI_color = othello.Player.BLACK
        elif AI_color == 'white':
            self.AI_color = othello.Player.WHITE
        else:   
            raise ValueError("AI_color must be either black or white")
        
    def run(self, game_state: list[list[str]]) -> tuple[int, int]:
        # Run the AI on the given game state
        game = othello.Game(game_state, self.AI_color)
        
        # Calculate the AI's move
        action = self.AI_method(self.AI_color).play(game.state)

        # Convert the move to row and column indices
        best_move = othello_index_to_row_col(action.repr)
        return best_move

if __name__ == "__main__":
    # Define the initial game state
    game_state = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "W", "B", "", "", ""],
        ["", "", "", "B", "W", "B", "", ""],
        ["", "", "", "", "", "W", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""]
    ]

    # Create an AI player with a specified method and color
    AI_player_instance = AI_player(AI_method="mcts", AI_color='black')

    # Run the AI to get the best move
    best_move = AI_player_instance.run(game_state)

    # Print the best move
    print(best_move)
