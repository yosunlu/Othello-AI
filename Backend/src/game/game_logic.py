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

    def place_piece(self, state_json, cell : list, turn : str):
        """
        Places a piece on board

        parems: 
            state_json: the state of the board, an 8x8 array
            cell: the intended cell to place the piece on; a list with two elements x and y
            turn: the color of the piece to be placed
        return: 
            False if the move is not valid
            the updated board if move is valid
        """
        try:
        # check if the board passed in is valid 
            if(self._valid_board(state_json)):
                board = json.loads(state_json)
                x = cell[0]
                y = cell[1]

        except ValueError as e:
        # Handle the ValueError
            print(f"Error in validating the board: {e}")
            return False
        
        # check if the given coordinate is a valid move
        if ([x, y] not in self._valid_moves(board, turn)):
            return False
        
        board[x][y] = turn # place the piece
        updated_board = self._flip_piece(board, [x, y]) # flip the required pieces
    
        return updated_board
    
    def game_over():
        """
        """
    
    def _valid_board(self, state_json):
        """
        Given a board represented in json, checks if the state is valid

        parems:
            state_json: a json that should be a 2D array 
        return:
            True if the board is valid
        """
        parsed_board = json.loads(state_json)

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

    def _valid_moves(self, state : list, current_color : str):
        """
        Given a state of a board and the color of the piece to be placed,
        determine the valid moves for the color

        parems:
            state: the state of the board, an 8x8 array
            current_color: the color of the piece to be placed
        
        return:
            a list of valid moves

        """
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
                if state[row][col] == "":
                    for dr, dc in directions:
                        r, c = row + dr, col + dc
                        found_opponent = False

                        while (
                            0 <= r < 8
                            and 0 <= c < 8
                            and state[r][c] == opponent_color
                        ):
                            found_opponent = True
                            r += dr
                            c += dc

                        if (
                            found_opponent
                            and 0 <= r < 8
                            and 0 <= c < 8
                            and state[r][c] == current_color
                        ):
                            valid_moves.append([row, col])
                            break  # Stop checking other directions if a valid move is found
        # print(valid_moves)
        return valid_moves

    def _flip_piece(self, state : list, cell : list):
        """
        Flip required pieces after placing a piece

        parems: 
            state: the state of the board, an 8x8 array
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
        color_placed = state[x][y] # the color of the piece placed
        opponent_color = "W" if color_placed == "B" else "B"
        
        for dr, dc in directions:
            cur_dir_list = [] # list of cells of current direction 
            r, c = x + dr, y + dc
            found_opponent = False

            while (
                0 <= r < 8
                and 0 <= c < 8
                and state[r][c] == opponent_color
            ):
                found_opponent = True
                # if the cell traversed is opponent's color, append the cell
                # does not flip yet; only flip when this cell(s) can be sandwiched
                cur_dir_list.append([r, c]) 
                r += dr
                c += dc
                
            if (
                found_opponent
                and 0 <= r < 8
                and 0 <= c < 8
                and state[r][c] == color_placed # found the color_placed at the other side of this direction
            ):
                # append the cells that are sandwiched
                cell_to_flip.extend(cur_dir_list)
        
    
        for x, y in cell_to_flip:
            state[x][y] = color_placed
        
        return state


    def _print_board(self, state):
        """
        For testing purposes
        """
        for row in state:
            print(" ".join(cell if cell else "." for cell in row))
