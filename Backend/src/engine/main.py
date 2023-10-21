from alpha_beta_ai import Othello, alpha_beta_cutoff_search
from collections import namedtuple
import pdb


def query_player(game, state, verbose=False):
    """Make a move by querying standard input."""

    game.display(state)
    move = None
    available_moves = game.actions(state)

    # if there are available moves, ask for input
    if available_moves:
        while not move:
            move_string = input("\nEnter move: ")

            try:
                x, y = move_string.split(",")
                move = int(x), int(y)
            except ValueError:
                print("bad format, please format as x, y")
                continue

            # check for available moves
            if move not in available_moves:
                print("illegal move, please try again")
                move = None
    else:
        print("no legal moves: passing turn to next player")
    return move


def alpha_beta_player(game, state, verbose=False):
    return alpha_beta_cutoff_search(state, game, verbose=verbose)


if __name__ == "__main__":
    GameState = namedtuple("GameState", "to_move, utility, board, moves")
    initial_state = GameState(
        to_move="B",
        utility=0,
        board={(3, 3): "W", (4, 4): "W", (3, 4): "B", (4, 3): "B"},
        moves=[(2, 3), (3, 2), (4, 5), (5, 4)],  # moves for "B"
    )
    game = Othello()
    print(alpha_beta_player(game, initial_state))
    # B_player = query_player
    # W_player = alpha_beta_player
    # win = game.play_game(B_player, W_player, verbose=True)
