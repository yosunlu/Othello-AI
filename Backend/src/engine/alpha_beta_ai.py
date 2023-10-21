"""
Sources:
- AIMA: https://github.com/aimacode/aima-python/blob/master/games4e.py
- Othello methods: https://github.com/JaimieMurdock/othello
"""

import numpy as np
from collections import namedtuple
import random
import pdb


GameState = namedtuple("GameState", "to_move, utility, board, moves")


# ______________________________________________________________________________
# alpha beta search with cutoff and evaluation function


def alpha_beta_cutoff_search(
    state, game, d=4, cutoff_test=None, eval_fn=None, verbose=False
):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    player = game.to_move(state)
    if verbose:
        game.display(state)
    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(game, state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(game, state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # random move
    if eval_fn == "random":
        return random.choice(game.actions(state))

    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = cutoff_test or (
        lambda state, depth: depth > d or game.terminal_test(state)
    )
    eval_fn = eval_fn or (lambda _, state: game.utility(state, player))

    best_score = -np.inf
    beta = np.inf
    best_action = None

    actions = []

    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        actions.append((v, a))
        if v > best_score:
            best_score = v
            best_action = a

    # introduce randomness
    # if there are multiple actions with the same best value, choose randomly
    best_actions = []
    for action in actions:
        if action[0] == best_score:
            best_actions.append(action[1])

    if len(best_actions) > 1:
        best_action = random.choice(best_actions)

    return best_action


# ______________________________________________________________________________
# Game classes


class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

    def play_game(self, *players, verbose=False):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state, verbose=verbose)
                state = self.result(state, move)
                # if no moves left, compute utility
                if self.terminal_test(state):

                    score = self.utility(state, self.to_move(self.initial))

                    if verbose:
                        self.display(state)
                        print("Black wins" if score > 0 else "White wins")

                    if score == 0:
                        return -1

                    return 1 if score > 0 else 0


class Othello(Game):
    """Play Othello on 8x8 board, with "B" as the black and "W" as the white.
    The intial board has 4 discs in the center, two of each color.

    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'B' or 'W'.

    keep track of the count of B and W by implementing a count method

    the utility is the largest difference between B and W

    """

    _directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

    def __init__(self, h=8, v=8):
        self.h = h
        self.v = v

        self.initial = GameState(
            to_move="B",
            utility=0,
            board={(3, 3): "W", (4, 4): "W", (3, 4): "B", (4, 3): "B"},
            moves=[(2, 3), (3, 2), (4, 5), (5, 4)],  # moves for "B"
        )

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):

        if move not in state.moves:
            return state  # Illegal move has no effect

        board = state.board.copy()

        # add player move to board
        board[move] = state.to_move

        # compute utility of move
        utility = self.compute_utility(board, move, state.to_move)

        # compute moves for next player
        player = "W" if state.to_move == "B" else "B"
        moves = self._get_legal_moves(board, player)

        return GameState(
            to_move=player,
            utility=utility,
            board=board,
            moves=moves,
        )

    def utility(self, state, player):
        """the difference between B and W"""
        (count_b, count_w) = self.count(state.board)
        if player == "B":
            return count_b - count_w
        else:
            return count_w - count_b

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return len(state.moves) == 0

    def display(self, state):
        """Print the board and show the utility for each player."""
        board = state.board
        print("\n=================================")
        print("B: %d, W: %d" % self.count(board))
        print(f"\n{state.to_move}'s turn")
        moves = self._get_legal_moves(board, state.to_move)
        print(f"moves: {moves}")

        for x in range(self.h):
            for y in range(self.v):
                if (x, y) in moves:
                    print("@", end=" ")
                else:
                    print(board.get((x, y), "."), end=" ")
            print()

    def count(self, board):
        """Return the number of discs for both player on the board."""
        count_b, count_w = 0, 0

        for x in range(self.h):
            for y in range(self.v):
                if board.get((x, y)) == "B":
                    count_b += 1
                elif board.get((x, y)) == "W":
                    count_w += 1
        return (count_b, count_w)

    def compute_utility(self, board, move, player):
        """perform given move and flip discs as necessary"""

        flips = (
            flip
            for direction in self._directions
            for flip in self._get_flips(board, move, direction, player)
        )

        # flip discs
        for x, y in flips:
            board[x, y] = player

        if player == "B":
            return self.count(board)[0]
        else:
            return self.count(board)[1]

    def _get_player_discs(self, board, player):
        """Get coordinates (x, y) for all discs on board for a given player"""

        discs = []
        for x in range(self.h):
            for y in range(self.v):
                if board.get((x, y)) == player:
                    discs.append((x, y))
        return discs

    @staticmethod
    def _walk(move, direction):
        """Generator expression for walking in a given direction
        from a given move"""

        (dx, dy) = direction
        x, y = move

        # keep walking in the given direction until we hit the edge
        while 0 <= x + dx < 8 and 0 <= y + dy < 8:
            x, y = x + dx, y + dy
            yield (x, y)

    def _find_moves(self, board, origin, direction):
        """we start at origin and walk in the given direction, if we hit an
        empty square and we would already "flipped" a disc, that means
        that is a valid move, since the rules are the the new disc has to have
        a disc of opposite color in between them"""

        color = board.get(origin)
        flips = []

        for x, y in self._walk(origin, direction):

            # if we hit an empty square, and we have "flipped" discs
            if board.get((x, y)) is None and flips:
                return (x, y)

            # saw disc of the same color,
            # or empty square and no discs flipped so far
            # no possible moves in this direction
            elif board.get((x, y)) == color or (
                board.get((x, y)) is None and not flips
            ):
                return None

            # if we see a disct of the opposite color, we store it and
            # continue walking
            elif board.get((x, y)) != color:
                flips.append((x, y))

    def _get_moves_for_disc(self, board, disc):
        """return all legal movies given a disc (x, y))"""

        moves = []

        for direction in self._directions:
            move = self._find_moves(board, disc, direction)
            if move:
                moves.append(move)

        return moves

    def _get_legal_moves(self, board, player):
        """return all legal movies for the current player"""

        moves = set()

        for disc in self._get_player_discs(board, player):

            moves.update(self._get_moves_for_disc(board, disc))

        return list(moves)

    def _get_flips(self, board, origin, direction, player):
        """get list of flips for origin and direction for player"""

        flips = []

        for x, y in self._walk(origin, direction):

            disc = board.get((x, y))

            # see different colored disc, add it to flips
            if disc != player and disc is not None:
                flips.append((x, y))

            # if we hit an empty square, no flips
            elif board.get((x, y)) is None:
                break

            # once we see disc of the same color, and we have flips
            # we can flip everything
            elif disc == player and len(flips) > 0:
                return flips

        return []