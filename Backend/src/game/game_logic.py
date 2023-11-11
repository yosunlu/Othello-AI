import json


class GameLogic:
    """
    A singleton class that defines game logic methods
    """

    def valid_board(board_json):
        parsed_board = json.loads(board_json)

        # a board should be a list with size of 8
        if not isinstance(parsed_board, list) or len(parsed_board) != 8:
            raise ValueError("Invalid board format: outer")

        # each row of the board should be a list with size of 8
        if not all(isinstance(row, list) or len(row) != 8 for row in parsed_board):
            raise ValueError("Invalid board format: inner")

        white_count = 0
        black_count = 0

        for row in parsed_board:
            for cell in row:
                if cell not in ["", "W", "B"]:
                    raise ValueError("Invalid cell value in board string")
                if cell == "W":
                    white_count += 1
                elif cell == "B":
                    black_count += 1

        return [black_count, white_count]

    def valid_moves(board_json, current_turn):
        """
        Return a list of valid moves in row-major order for a given color's turn.
        Each valid move is a list of two ints.
        """

        parsed_board = json.loads(board_json)

        # Initialize an empty 8*8 matrix for valid moves
        valid_moves = []
        directions = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        opponent_turn = "B" if current_turn == "W" else "W"

        # for each empty cell, search the eight directions
        # if opponent's piece(s) found and can be sandwiched, append the empty cell
        for row in range(8):
            for col in range(8):
                if parsed_board[row][col] == "":
                    for dr, dc in directions:
                        r, c = row + dr, col + dc
                        found_opponent = False

                        while (
                            0 <= r < 8
                            and 0 <= c < 8
                            and parsed_board[r][c] == opponent_turn
                        ):
                            found_opponent = True
                            r += dr
                            c += dc

                        if (
                            found_opponent
                            and 0 <= r < 8
                            and 0 <= c < 8
                            and parsed_board[r][c] == self._current_turn
                        ):
                            valid_moves.append([row, col])
                            break  # Stop checking other directions if a valid move is found
        # print(valid_moves)
        return valid_moves

    def place_piece(board_json : list, grid : list, turn : str):
        """
        Given a grid's coordinate and turn:
        1. Check if the move is valid (will call _move_is_valid); if not, return false
        2. If true, place the piece on board, call flip_piece, change turn, then check winning condition: no more valid move for opponent
        3. If winning condition is met, return current turn; if not, return true
        """
        # TODO not implemented
        return

    def flip_piece(self):
        # TODO not implemented
        # flip self._board
        pass

    def _move_is_valid(self, move):
        """Given a coordinate of a grid,"""
        return move in self.valid_moves()


# def gameOver(self):
#     """Interpret a board Object; return True if game is over, False if not"""
#     # return False if game is not over, return either "B" or "W" if game is won by the color

#     def turnHasValidMove(self):
#         """Interpret a board Object return True if turn has a valid move, False if not"""

#         # Define directions for checking valid moves (horizontally, vertically, diagonally)
#         directions = [
#             (0, 1),
#             (1, 0),
#             (0, -1),
#             (-1, 0),
#             (1, 1),
#             (1, -1),
#             (-1, 1),
#             (-1, -1),
#         ]

#         # Opponent's color (is opposite of the current turn)
#         opponent_turn = "B" if self.turn == "W" else "W"

#         # Iterate through each cell of the board
#         for row in range(8):
#             for col in range(8):
#                 # Check if the cell is empty
#                 if self.board[row][col] == "":
#                     # Check in all directions
#                     for dr, dc in directions:
#                         r, c = row + dr, col + dc

#                         # Check if there is a valid move in this direction
#                         if (
#                             0 <= r < 8
#                             and 0 <= c < 8
#                             and self.board[r][c] == opponent_turn
#                         ):
#                             r += dr
#                             c += dc
#                             while (
#                                 0 <= r < 8
#                                 and 0 <= c < 8
#                                 and self.board[r][c] == opponent_turn
#                             ):
#                                 r += dr
#                                 c += dc
#                             if (
#                                 0 <= r < 8
#                                 and 0 <= c < 8
#                                 and self.board[r][c] == self.turn
#                             ):
#                                 return True

#         return False

#     # Check if either player has a valid move left
#     black_has_move = turnHasValidMove(self.board, "B")
#     white_has_move = turnHasValidMove(self.board, "W")

#     # If neither player has a valid move, the game is over
#     return not (black_has_move or white_has_move)

# def gameWonByColor(self):
#     """Interpret a board Object return str(W), str(B), or False if White, Black or nobody has won the game"""

#     def is_valid(row, col):
#         """Check if a position is valid"""
#         return 0 <= row < 8 and 0 <= col < 8

#     # Return 'B' if black won, 'W' is white won, 'DRAW' if draw, 'None' for any other situation
#     if self.gameOver() == True:
#         black_count = sum(row.count("B") for row in self._board)
#         white_count = sum(row.count("W") for row in self._board)
#         if black_count > white_count:
#             return "B"
#         elif white_count > black_count:
#             return "W"
#         else:
#             return "DRAW"
#     elif not black_has_move:
#         return "W"
#     elif not white_has_move:
#         return "B"
#     else:
#         return None
