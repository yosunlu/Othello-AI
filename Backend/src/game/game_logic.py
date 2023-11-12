import json


class GameLogic():
    """
    A singleton class that defines game logic methods
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameLogic, cls).__new__(cls)
        return cls._instance  

    def place_piece(self, board_json : list, cell : list, turn : str):
        """
        Places a piece on board

        parems: 
            board_json: the state of the board, an 8x8 array
            grid: the intended grid to place the piece on; a list with two elements x and y
            turn: the color of the piece to be placed
        return: 
            false if the move is not valid
            the updated array if move is valid
        """
        try:
        # check if the board passed in is valid 
            if(self.valid_board(board_json)):
                parsed_board = json.loads(board_json)
                x = cell[0]
                y = cell[1]

        except ValueError as e:
        # Handle the ValueError
            print(f"Error in validating the board: {e}")
            return False
        
        # check if the given cordinate is a valid move
        if ([x, y] not in self._valid_moves(parsed_board, turn)):
            return False
        
        parsed_board[x][y] = turn # place the piece
        updated_board = self._flip_piece(parsed_board, [x, y]) # flip the required pieces
    
        return updated_board
    
    def valid_board(self, board_json):
        """
        Given a board represented in json, checks if the state is valid

        parems:
            board_json: a json that should be a 2D array 
        return:
            True if the board is valid
        """
        parsed_board = json.loads(board_json)

        # a board should be a list with size of 8
        if not isinstance(parsed_board, list) or len(parsed_board) != 8:
            raise ValueError("Invalid board format: outer")

        # each row of the board should be a list with size of 8
        if not all(isinstance(row, list) or len(row) != 8 for row in parsed_board):
            raise ValueError("Invalid board format: inner")

        for row in parsed_board:
            for cell in row:
                if cell not in ["", "W", "B"]:
                    raise ValueError("Invalid cell value in board string")

        return True

    def _valid_moves(self, board_json, current_color):
        """
        Given a state of a board and the color of the piece to be placed, determine the valid moves for the color

        parems:
            board_json: the state of the board, an 8x8 array
            current_color: the color of the piece to be placed
        
        return:
            a list of valid moves

        """
        parsed_board = json.loads(board_json)
        valid_moves = [] # Initialize an empty 8*8 matrix for valid moves
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

        opponent_color = "B" if current_color == "W" else "W"

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
                            and parsed_board[r][c] == opponent_color
                        ):
                            found_opponent = True
                            r += dr
                            c += dc

                        if (
                            found_opponent
                            and 0 <= r < 8
                            and 0 <= c < 8
                            and parsed_board[r][c] == current_color
                        ):
                            valid_moves.append([row, col])
                            break  # Stop checking other directions if a valid move is found
        # print(valid_moves)
        return valid_moves

    def _flip_piece(self, board, cell):
        """
        Flip required pieces after a placing a piece

        parems: 
            board_json: the state of the board, an 8x8 array
            cell : the cell to place the piece on; a list with two elements x and y
        return: 
            the updated board
        """
        # the 8 directions to be explored
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
        cell_to_flip = [] # the list of cell with opponent's color that

        # the coordinates of the cell where the piece was placed
        x = cell[0]
        y = cell[1]
        color_placed = board[x][y] # the color of the piece placed
        opponent_color = "W" if color_placed == "B" else "B"
        
        for dr, dc in directions:
            cur_dir_list = [] #  list of cell of current direction 
            r, c = x + dr, y + dc
            found_opponent = False

            while (
                0 <= r < 8
                and 0 <= c < 8
                and board[r][c] == opponent_color
            ):
                found_opponent = True
                cur_dir_list.append([r, c])
                r += dr
                c += dc
                
            if (
                found_opponent
                and 0 <= r < 8
                and 0 <= c < 8
                and board[r][c] == color_placed # found the color_placed at the other side of this direction
            ):
                # append the cells that are sandwiched
                cell_to_flip.extend(cur_dir_list)
        
    
        for x, y in cell_to_flip:
            board[x][y] = color_placed
        
        return board


    def _print_board(self, board):
        """
        For testing purposes
        """
        for row in board:
            print(" ".join(cell if cell else "." for cell in row))

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
