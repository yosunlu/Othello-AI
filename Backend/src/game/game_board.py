import json

def createBoard():
    """Create and return game board Object with only the starting positions occupied"""
    board = []
    for i in range(0, 8):
        board[i] = ["", "", "", "", "", "", "", ""]

    board[3][3] = "W"
    board[4][3] = "B"
    board[4][4] = "W"
    board[3][4] = "B"
    
    return board

def parseBoard(board_string: str):
    """Parse a board string from JSON and return an Object representing the board, or False if the string is not valid"""
    parsed = json.loads(board_string)

    if isinstance(parsed, list):
        if len(parsed) != 8:
            return False
        for i in range(0, 8):
            if not isinstance(parsed[i], list) or len(parsed[i]) != 8:
                return False
            for ii in range(0, 8):
                if parsed[i][ii] != '' and parsed[i][ii] != 'W' and  parsed[i][ii] != 'B':
                    return False
    else:
        return False
    return parsed

def testParseBoard():
    """Tests parse_board for each of the cases it must handle"""
    # Should not return false (board is valid)
    assert False != parseBoard('[["W","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","W","B","","",""],["","","","B","W","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]')

    # Should return false due to an improper outer array length
    assert False == parseBoard('[["","","","","","","",""],["","","","","","","",""],["","","","W","B","","",""],["","","","B","W","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]')
    
    # Should return false due to an improper inner array length
    assert False == parseBoard('[["W","","","","","","",""],["","","","","","",""],["","","","","","","",""],["","","","W","B","","",""],["","","","B","W","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]')
    
    # Should return false due to an invalid piece code
    assert False == parseBoard('[["C","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","W","B","","",""],["","","","B","W","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]')

# TODO WARNING idk if validity is a real property of Othello boards. Remove if this does not make sense
def verifyBoard(board_obj: list):
    """Interpret a board Object return True or False depending on whether or not the board is valid"""
    # TODO not implemented
    return True

def validMoves(board_obj: list, turn: str):
    """Interpret a board Object return a list of valid moves in Row-major order, for a given color's turn. Each valid move is a list of two ints"""

    # Initialize an empty 8*8 matrix for valid moves
    valid_moves_matrix = [['' for i in range(8)] for i in range(8)]

    # Define directions for checking valid moves (horizontally, vertically, diagonally)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Opponent's color (is opposite of the current turn)
    opponent_turn = 'B' if turn == 'W' else 'W'

    # Iterate through each cell of the board
    for row in range(8):
        for col in range(8):
            # Check if the cell is empty
            if board_obj[row][col] == '':
                # Check in all directions
                for dr, dc in directions:
                    r, c = row + dr, col + dc

                    # Check if there is a valid move in this direction
                    if 0 <= r < 8 and 0 <= c < 8 and board_obj[r][c] == opponent_turn:
                        r += dr
                        c += dc
                        while 0 <= r < 8 and 0 <= c < 8 and board_obj[r][c] == opponent_turn:
                            r += dr
                            c += dc
                        if 0 <= r < 8 and 0 <= c < 8 and board_obj[r][c] == turn:
                            valid_moves_matrix[row][col] = turn
                            break
                        
    return valid_moves_matrix

def moveIsValid(board_obj: list, move: list, turn: str):
    """Interpret a board Object return True if a space on the board is a valid move for a given color"""
    # TODO not implemented
    return True

def gameWonByColor(board_obj: list):
    """Interpret a board Object return str(W), str(B), or False if White, Black or nobody has won the game"""
    # TODO not implemented
    return False