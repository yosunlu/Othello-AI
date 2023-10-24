import json

def parse_board(board_string: str):
    """Parse a board string from JSON and return an Object representing the board, or False if the string is not valid"""
    parsed = json.loads(board_string)

    if isinstance(parsed, list):
        if len(parsed) != 8:
            return False
        for i in range(0, 8):
            if len(parsed[i]) != 8:
                return False
            for ii in range(0, 8):
                if parsed[i][ii] != '' and parsed[i][ii] != 'W' and  parsed[i][ii] != 'B':
                    return False
    return parsed

def test_parse_board():
    """Tests parse_board for each of the cases it must handle"""
    # Should not return false (board is valid)
    assert False != parse_board('[["W","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","W","B","","",""],["","","","B","W","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]')

    # Should return false due to an improper outer array length
    assert False == parse_board('[["","","","","","","",""],["","","","","","","",""],["","","","W","B","","",""],["","","","B","W","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]')
    
    # Should return false due to an improper inner array length
    assert False == parse_board('[["W","","","","","","",""],["","","","","","",""],["","","","","","","",""],["","","","W","B","","",""],["","","","B","W","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]')
    
    # Should return false due to an invalid piece code
    assert False == parse_board('[["W","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","W","B","","",""],["","","","C","W","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]')

# TODO WARNING idk if validity is a real property of Othello boards. Remove if this does not make sense
def verify_board(board_obj: list):
    """Interpret a board Object return True or False depending on whether or not the board is valid"""
    # TODO not implemented
    return True

def valid_moves(board_obj: list, turn: str):
    """Interpret a board Object return a list of valid moves in Row-major order, for a given color's turn. Each valid move is a list of two ints"""
    # TODO not implemented
    return True

def move_is_valid(board_obj: list, move: list, turn: str):
    """Interpret a board Object return True if a space on the board is a valid move for a given color"""
    # TODO not implemented
    return True