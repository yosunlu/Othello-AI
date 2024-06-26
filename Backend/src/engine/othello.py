from dataclasses import dataclass, field
from enum import Enum, auto, unique
import itertools
from typing import Final, Iterable, Optional, Union
import time
from functools import cache
import pdb

@unique
class Player(Enum):
    """Player in an Othello game."""

    BLACK = auto()
    WHITE = auto()

    @property
    def adversary(self) -> 'Player':
        return Player.WHITE if self is Player.BLACK else Player.BLACK


@dataclass(frozen=True)
class Coords:
    """Coordinates on an Othello board.

    Fields:
    - ix: The integer representation of the coordinates. Defined by
          ``rank*8 + file`` where ``rank`` and ``file`` are 0-based numeric
          indices. Rank 1 is given an index of 0, rank 2 is given 1, etc. File a
          is given an index of 0, file b is given 2, etc.
    """

    ix: int

    def __post_init__(self):
        if not (0 <= self.ix < 64):
            raise ValueError('invalid ix')

    @property
    def file(self) -> int:
        return self.ix & 0x7  # self.ix % 8

    @property
    def rank(self) -> int:
        return self.ix >> 3  # self.ix // 8

    @staticmethod
    def from_file_rank(file: int, rank: int) -> 'Coords':
        """Create ``Coords`` from the numeric indices of rank and file."""
        if not (0 <= file < 8):
            raise ValueError('invalid file')

        if not (0 <= rank < 8):
            raise ValueError('invalid rank')
        return Coords(rank*8 + file)

    @staticmethod
    def from_repr(string: str) -> 'Coords':
        """Create ``Coords`` from string representation."""
        if len(string) != 2:
            raise ValueError('invalid string')

        file_str, rank_str = string

        if file_str.isupper():
            file = ord(file_str) - ord('A')
        elif file_str.islower():
            file = ord(file_str) - ord('a')
        else:
            raise ValueError('invalid file')

        try:
            rank = int(rank_str) - 1
        except ValueError:
            raise ValueError('invalid rank')

        return Coords.from_file_rank(file, rank)

    @property
    def repr(self) -> str:
        return chr(self.file + ord('a')) + str(self.rank+1)


@dataclass(frozen=True)
class Action:
    """Action of an Othello game."""

    coords: Coords
    @property
    def repr(self) -> str:
        return self.coords.repr


@dataclass(frozen=True)
class Board:
    """Board of an Othello game.

    Board Representation

    This class uses 2 64-bit words to represent a board. The i-th bit (counting
    from LSB) of the ``black_board`` field (resp. the ``white_board`` field) is
    set iff there is a black (resp. white) piece on the board at a square whose
    integer representation of the coordinates is i. Thus the i-th bit of
    ``black_board`` and ``white_board`` cannot be set at the same time for all
    0 <= i < 64.
    """

    black_board: int
    white_board: int

    def __postinit__(self):
        if not (0 <= self.black_board <= 0xffffffffffffffff):
            raise ValueError('invalid black_board')

        if not (0 <= self.white_board <= 0xffffffffffffffff):
            raise ValueError('invalid white_board')

        if self.black_board & self.white_board > 0:
            raise ValueError('board in an inconsistent state: some squares are '
                             'played by both players')

    def __getitem__(self, key: Coords) -> Optional[Player]:
        """Get the piece at a specified position."""
        mask = 0x1 << key.ix

        if self.black_board & mask > 0:
            return Player.BLACK
        elif self.white_board & mask > 0:
            return Player.WHITE
        else:
            return None

    def set(self, key: Coords, value: Optional[Player]) -> 'Board':
        """Set the piece at a specified position."""
        mask = 0x1 << key.ix

        if value is None:
            black_board = self.black_board & ~mask
            white_board = self.white_board & ~mask
        elif value is Player.BLACK:
            black_board = self.black_board | mask
            white_board = self.white_board & ~mask
        else:  # value is Player.WHITE
            black_board = self.black_board & ~mask
            white_board = self.white_board | mask

        return Board(black_board, white_board)

    @staticmethod
    def initial() -> 'Board':
        """Return the initial board configuration."""
        board = Board(0, 0)
        board = board.set(Coords.from_repr('d4'), Player.WHITE)
        board = board.set(Coords.from_repr('e4'), Player.BLACK)
        board = board.set(Coords.from_repr('d5'), Player.BLACK)
        board = board.set(Coords.from_repr('e5'), Player.WHITE)
        return board

    @staticmethod
    def set_state(given_state) -> 'Board':
        """Return the given board configuration."""
        board = Board(0, 0)
        col_map = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
            
        for row_index, row in enumerate(given_state, start=1):
            for col_index, cell in enumerate(row, start=1):
                if cell in ['W', 'B']:
                    player = Player.WHITE if cell == 'W' else Player.BLACK
                    board_index = col_map[col_index] + str(row_index)
                    board = board.set(Coords.from_repr(board_index), player)
        return board

    @staticmethod
    def from_repr(rep: Iterable[str]) -> 'Board':
        def parse_square(sq: str) -> Optional[Player]:
            if sq == '.':
                return None
            elif sq == 'B':
                return Player.BLACK
            elif sq == 'W':
                return Player.WHITE
            else:
                raise ValueError('invalid square')

        board = Board(0, 0)
        for rank, row in enumerate(rep):
            for file, square in enumerate(row):
                board = board.set(Coords.from_file_rank(file, rank),
                                  parse_square(square))

        return board

    @property
    def repr(self) -> Iterable[str]:
        """String representation of the board.

        X represents dark and O represents light.
        """
        def fmt_square(sq: Optional[Player]) -> str:
            if sq is None:
                return '.'
            elif sq is Player.BLACK:
                return 'B'
            else:  # sq is Player.WHITE:
                return 'W'

        return (''.join(fmt_square(self[Coords.from_file_rank(file, rank)])
                        for file in range(8)) for rank in range(8))


class _DrawType:
    pass


DRAW: Final[_DrawType] = _DrawType()


@dataclass(frozen=True)
class State:
    """State of an Othello game."""

    board: Board

    @staticmethod
    def initial() -> 'State':
        """Return the initial state."""
        return State(Board.initial())

    @staticmethod
    def set_state(given_state) -> 'State':
        """Return given state."""
        return State(Board.set_state(given_state))

    @cache
    def get_flips(self, player: Player, action: Action) -> int:
        """Get bitmask of pieces flipped when player performs action."""
        if self.board[action.coords] is not None:
            return 0x0

        file = action.coords.file
        rank = action.coords.rank

        mask = 0x0
        for df, dr in ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1),
                       (0, -1), (1, -1)):
            new_mask = mask
            for i in itertools.count(1):
                try:
                    target_coords = Coords.from_file_rank(file+i*df, rank+i*dr)
                except ValueError:
                    break

                if self.board[target_coords] is None:
                    break
                elif self.board[target_coords] is player:
                    mask = new_mask
                    break
                else:  # self.board[target_coords] is player.adversary
                    new_mask |= 1 << target_coords.ix

        return mask

    def n_number(self, player: Player):
        if player is Player.BLACK:
            return f'{self.board.black_board:b}'.count('1')
        elif player is Player.WHITE:
            return f'{self.board.white_board:b}'.count('1')

    def n_edge(self, player: Player):
        n_edge = 0
        edge_point = []
        for i in range(2, 8):
            edge_point.append('a' + str(i))
            edge_point.append('h' + str(i))
        for char in range(ord('b'), ord('h')):
            edge_point.append(chr(char) + '1')
            edge_point.append(chr(char) + '8')
        for point in edge_point:
            if self.board[Coords.from_repr(point)] is player:
                n_edge += 1
        return n_edge

    def n_corner(self, player: Player):
        n_corner = 0
        for point in ['a1', 'a8', 'h1', 'h8']:
            if self.board[Coords.from_repr(point)] is player:
                n_corner += 1
        return n_corner

    def n_action(self, player: Player):
        return len(list(self.get_legal_actions(player)))

    def adversary_n_action(self, player: Player):
        return -len(list(self.get_legal_actions(player.adversary)))

    def get_score(self,player: Player):
        score_number = self.n_number(player)
        score_edge = self.n_edge(player)
        score_corner = self.n_corner(player)
        score_n_action = self.n_action(player)
        score_adversary_n_action = self.adversary_n_action(player)
        score = 2 * score_number + 5 * score_edge + 10 * score_corner + score_n_action + score_adversary_n_action
        return score

    def is_legal_action(self, player: Player, action: Action) -> bool:
        """Checks if some action is a legal actions for some player."""
        return self.get_flips(player, action) > 0

    def get_legal_actions(self, player: Player) -> Iterable[Action]:
        """Return the legal actions by some player."""
        return (action for action in (Action(Coords(i)) for i in range(64))
                if self.is_legal_action(player, action))

    def perform_action(self, player: Player, action: Action):
        """Perform an action on behalf of some player."""
        if not self.is_legal_action(player, action):
            raise ValueError('illegal action')

        mask = self.get_flips(player, action)

        if player is Player.BLACK:
            black_board = self.board.black_board | (1 << action.coords.ix) | mask
            white_board = self.board.white_board & ~mask
        else:  # if player is Player.WHITE
            black_board = self.board.black_board & ~mask
            white_board = \
                self.board.white_board | (1 << action.coords.ix) | mask

        return State(Board(black_board, white_board))

    def get_conclusion(self) -> Optional[Union[Player, _DrawType]]:
        """Get the conclusion of the game.

        Returns:
        - None      if the game is still progressing.
        - A player  if that player wins the game.
        - DRAW      if the game draws.
        """
        no_legal_actions = all(False for _ in itertools.chain(
            self.get_legal_actions(Player.BLACK),
            self.get_legal_actions(Player.WHITE)))

        if no_legal_actions:
            n_blacks = self.n_number(Player.BLACK)
            n_whites = self.n_number(Player.WHITE)

            if n_blacks > n_whites:
                return Player.BLACK
            elif n_blacks < n_whites:
                return Player.WHITE
            else:
                return DRAW
        else:
            return None

    def get_difference(self):
        n_blacks = self.n_number(Player.BLACK)
        n_whites = self.n_number(Player.WHITE)
        return abs(n_blacks - n_whites)

    def is_terminal(self) -> bool:
        """Check if the state is terminal."""
        return self.get_conclusion() is not None


@dataclass
class Game:
    """An Othello game."""

    # state: State = field(default=State.initial())
    # next_player: Player = field(default=Player.BLACK)

    def __init__(self, given_state=None,given_player=None):
        if given_state is None:
            self.state = State.initial()
            self.next_player = Player.BLACK
        else:
            self.state = State.set_state(given_state)
            self.next_player = given_player

    def play(self, player: Player, action: Optional[Action]) -> None:
        """Play a move or skip on behalf of a player."""
        if player is not self.next_player:
            raise ValueError('not player\'s turn')

        if any(True for _ in self.state.get_legal_actions(player)):
            if action is None:
                raise ValueError('cannot skip when there is an legal action')
            self.state = self.state.perform_action(player, action)
        else:
            if action is not None:
                raise ValueError('cannot play when there is no legal action')

        self.next_player = self.next_player.adversary

    def get_score(self, player: Player):
        """Get the score of the player
        Return: score
        """
        if player is Player.BLACK:
            return f'{self.state.board.black_board:b}'.count('1')
        elif player is Player.WHITE:
            return f'{self.state.board.white_board:b}'.count('1')

    def get_conclusion(self) -> Optional[Union[Player, _DrawType]]:
        """Get the conclusion of the game.

        Returns:
        - None      if the game is still progressing.
        - A player  if that player wins the game.
        - DRAW      if the game draws.
        """
        return self.state.get_conclusion()


class AI:
    """Base class for AIs that play Othello."""

    def play(self, state: State) -> Optional[Action]:
        """Play a move.

        Arguments:
        - state: Current game state.

        Returns:
        - An action  if the AI intends to play such action.
        - None       if the AI intends to skip.

        Note that the AI can skip iff there is no legal action.
        """
        raise NotImplementedError('method not overridden')


class Referee:
    """A class that runs the game and coordinates the two AIs."""

    def __init__(self, black_ai: AI, white_ai: AI):
        self.game = Game()
        self.ais = {Player.BLACK: black_ai, Player.WHITE: white_ai}
        self.n_step = 0
        self.time_black = 0
        self.time_white = 0

    def cb_post_move(self, player: Player, action: Optional[Action]) -> None:
        """Callback invoked after each move."""
        pass

    def cb_game_end(self) -> None:
        """Callback invoked when the game ends."""
        pass

    def run(self):
        """Run the game."""
        while self.game.get_conclusion() is None:
            start_time = time.time()
            player = self.game.next_player
            action = self.ais[player].play(self.game.state)
            self.n_step += 1
           
            self.game.play(player, action)
            end_time = time.time()
            time_duration = end_time - start_time
            
            if player is Player.BLACK:
                self.time_black += time_duration
            elif player is Player.WHITE:
                self.time_white += time_duration
            self.cb_post_move(player, action)

        self.cb_game_end()
