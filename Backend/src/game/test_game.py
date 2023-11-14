from game_logic import GameLogic
import pytest
import json

logic = GameLogic()

def test_place_piece():
    """Tests the place_piece method in game_logic"""
    # the board before piece being placed
    board_before = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "W", "B", "", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    board_json = json.dumps(board_before)
    # place_piece(self, board_json, cell : list, turn : str)
    board_after = logic.place_piece(board_json, [2, 3], "B")

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


def test_valid_board():
    """Tests the valid_board method in game_logic"""
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
    # valid_board(self, board_json)
    assert logic._valid_board(board_json) == True

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
        logic._valid_board(board_json)
    assert "Invalid board format: outer" in str(excinfo.value)

def test_flip_piece():
    # test case: one direction of pieces needs to be flipped
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
        ["", "", "",  "",  "",  "",  "", ""],
        ["", "", "",  "",  "",  "",  "", ""],
        ["", "", "",  "B", "W", "",  "", ""],
        ["", "", "",  "W", "B", "B", "", ""],
        ["", "", "W", "W", "W", "B", "", ""],
        ["", "", "",  "B", "W", "",  "", ""],
        ["", "", "",  "",  "",  "",  "", ""],
        ["", "", "",  "",  "",  "",  "", ""],
    ]
    # [2, 3] is where the piece was placed
    board_after = logic._flip_piece(board_before, [5, 3]) 
    board_expected = [
        ["", "", "",  "",  "",  "",  "", ""],
        ["", "", "",  "",  "",  "",  "", ""],
        ["", "", "",  "B", "W", "",  "", ""],
        ["", "", "",  "B", "B", "B", "", ""],
        ["", "", "W", "B", "B", "B", "", ""],
        ["", "", "",  "B", "W", "",  "", ""],
        ["", "", "",  "",  "",  "",  "", ""],
        ["", "", "",  "",  "",  "",  "", ""],
    ]
    assert board_after == board_expected

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
    moves = logic._valid_moves(board, "W") # should return a list containing valid moves for the turn
    expected_moves = [[2, 2], [4, 2], [2, 4]]

    # compare 2 lists regardless of their order
    returned_tuple_set = {tuple(elem) for elem in moves}
    expected_tuple_set = {tuple(elem) for elem in expected_moves}
    assert returned_tuple_set == expected_tuple_set
