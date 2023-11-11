import Backend.src.game.game_logic
import pytest
import json


def test_constructor():
    """Tests the constructor with and without given string and turn"""
    # test case: game with intial states
    new_game = Game()
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
    assert new_game._board == expected_board

    # test case: game with given and correct json and turn
    existing_board = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "B", "", "", "", ""],
        ["", "", "", "W", "B", "", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    board_json = json.dumps(existing_board)
    new_game = Game(board_json=board_json, turn="W")
    assert new_game._board == existing_board and new_game._current_turn == "W"

    # test case: initializing game with incorrect json
    saved_board = [
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
    board_json = json.dumps(saved_board)
    with pytest.raises(ValueError) as excinfo:
        saved_game = Game(board_json=board_json, turn="W")
    assert "Invalid board format: outer" in str(excinfo.value)

    # test case: initializing game with incorrect turn
    with pytest.raises(ValueError) as excinfo:
        saved_game = Game(board_json=board_json, turn="InvalidValue")
    assert "Invalid turn" in str(excinfo.value)


def test_valid_moves():
    """Tests the valid_moves function"""
    # test case: game with valid moves
    saved_board = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "B", "", "", "", ""],
        ["", "", "", "B", "B", "", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    board_json = json.dumps(saved_board)
    saved_game = Game(board_json=board_json, turn="W")
    expected_moves = [[2, 2], [4, 2], [2, 4]]

    # compare 2 lists regardless of their order
    returned_tuple_set = {tuple(elem) for elem in saved_game.valid_moves()}
    expected_tuple_set = {tuple(elem) for elem in expected_moves}
    assert returned_tuple_set == expected_tuple_set


def place_piece():
    # TODO not implemented
    return


def test_move_is_valid():
    # TODO not implemented
    return


def test_get_board():
    # TODO tnot implemented
    return


def get_count():
    # TODO not implemented
    return


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
