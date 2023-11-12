from game_logic import GameLogic
import pytest
import json

logic = GameLogic()

def test_valid_board():
    """Tests the valid_board method"""
    # test case: game with intial states
    expected_board = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "W", "B", "", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    board_json = json.dumps(expected_board)
    assert logic.valid_board(board_json) == True

    # test case: initializing game with incorrect json
    expected_board = [
        # board with incorrect outer array length
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "B", "", "", "", ""],
        ["", "", "", "B", "B", "", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    board_json = json.dumps(expected_board)
    with pytest.raises(ValueError) as excinfo:
        logic.valid_board(board_json)
    assert "Invalid board format: outer" in str(excinfo.value)

def test_flip_piece():
    # test case: one direction of pieces need to be flipped
    board_before = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "B", "", "", "", ""],
        ["", "", "", "W", "B", "", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]

    board_after = logic._flip_piece(board_before, [2, 3]) # [2, 3] is where the piece was placed
    board_expected = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "B", "", "", "", ""],
        ["", "", "", "B", "B", "", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    assert board_after == board_expected

    # test case: two directions of pieces need to be flipped
    board_before = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "W", "B", "B", "", ""],
        ["", "", "W", "W", "W", "B", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    board_after = logic._flip_piece(board_before, [5, 3]) # [2, 3] is where the piece was placed
    board_expected = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "B", "B", "B", "", ""],
        ["", "", "W", "B", "B", "B", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    assert board_after == board_expected
    
    return


#     # test case: game with given and correct json and turn
#     existing_board = [
#         ["", "", "", "", "", "", "", ""],
#         ["", "", "", "", "", "", "", ""],
#         ["", "", "", "B", "", "", "", ""],
#         ["", "", "", "W", "B", "", "", ""],
#         ["", "", "", "B", "W", "", "", ""],
#         ["", "", "", "", "", "", "", ""],
#         ["", "", "", "", "", "", "", ""],
#         ["", "", "", "", "", "", "", ""],
#     ]
#     board_json = json.dumps(existing_board)
#     new_game = Game(board_json=board_json, turn="W")
#     assert new_game._board == existing_board and new_game._current_turn == "W"



#     # test case: initializing game with incorrect turn
#     with pytest.raises(ValueError) as excinfo:
#         saved_game = Game(board_json=board_json, turn="InvalidValue")
#     assert "Invalid turn" in str(excinfo.value)


def test_valid_moves():
    """Tests the valid_moves function"""
    # test case: game with valid moves
    board = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "B", "", "", "", ""],
        ["", "", "", "B", "B", "", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    board_json = json.dumps(board)
    moves = logic._valid_moves(board_json, "W") # should return a list containing valid moves for the turn
    expected_moves = [[2, 2], [4, 2], [2, 4]]

    # compare 2 lists regardless of their order
    returned_tuple_set = {tuple(elem) for elem in moves}
    expected_tuple_set = {tuple(elem) for elem in expected_moves}
    assert returned_tuple_set == expected_tuple_set


# def place_piece():
#     # TODO not implemented
#     return


# def test_move_is_valid():
#     # TODO not implemented
#     return


#     # Should not return false (board is valid)
#     assert False != parseBoard(
#         '[["W","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","W","B","","",""],["","","","B","W","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]'
#     )

#     # Should return false due to an improper outer array length
#     assert False == parseBoard(
#         '[["","","","","","","",""],["","","","","","","",""],["","","","W","B","","",""],["","","","B","W","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]'
#     )

#     # Should return false due to an improper inner array length
#     assert False == parseBoard(
#         '[["W","","","","","","",""],["","","","","","",""],["","","","","","","",""],["","","","W","B","","",""],["","","","B","W","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]'
#     )

#     # Should return false due to an invalid piece code
#     assert False == parseBoard(
#         '[["C","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","W","B","","",""],["","","","B","W","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]'
#     )


# # TODO WARNING idk if validity is a real property of Othello boards. Remove if this does not make sense


# def verifyBoard(board_obj: list):
#     """Interpret a board Object return True or False depending on whether or not the board is valid"""
#     # TODO not implemented
#     return True
