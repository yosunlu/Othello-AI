import sys
sys.path.append(".")

from game_logic import GameLogic
import pytest
import json

logic = GameLogic()

def test_place_piece_single():
    """Tests the place_piece method in game_logic with one direction flip"""
    
    # case 1: one direction of pieces to be flipped
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


    # case 2: also for one direction of pieces to be flipped
    board_before = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "W", "B", "", "", ""],
        ["", "", "", "W", "B", "B", "", ""],
        ["", "", "", "W", "W", "W", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    board_json = json.dumps(board_before)
    board_after = logic.place_piece(board_json, [6, 2], "B")
    board_expected = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "W", "B", "", "", ""],
        ["", "", "", "W", "B", "B", "", ""],
        ["", "", "", "B", "W", "W", "", ""],
        ["", "", "B", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    assert board_after == board_expected


def test_place_piece_multiple():
    """Tests the place_piece method in game_logic with 2+ direction flips"""


    # case 3: two directions of pieces to be flipped
    # the board before piece being placed
    board_before = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "B", "B", "", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    board_json = json.dumps(board_before)
    # place_piece(self, board_json, cell : list, turn : str)
    board_after = logic.place_piece(board_json, [4, 2], "W")
    board_expected = [
        ["", "", "",  "",   "", "", "", ""],
        ["", "", "",  "",   "", "", "", ""],
        ["", "", "",  "B", "W", "", "", ""],
        ["", "", "",  "W", "B", "", "", ""],
        ["", "", "W", "W", "W", "", "", ""],
        ["", "", "",  "",  "",  "", "", ""],
        ["", "", "",  "",  "",  "", "", ""],
        ["", "", "",  "",  "",  "", "", ""],
    ]
    assert board_after == board_expected


    # case 4: also for 2 directions of pieces to be flipped
    board_before = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "B", "B", "B", "", "", "", ""],
        ["", "", "", "W", "W", "W", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    board_json = json.dumps(board_before)
    board_after = logic.place_piece(board_json, [4, 5], "B")
    board_expected = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "B", "B", "B", "", "", "", ""],
        ["", "", "", "W", "B", "W", "", ""],
        ["", "", "", "B", "B", "B", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    assert board_after == board_expected

    # case 5: 3 directions of pieces to be flipped
    board_before = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "W", "", "", "", ""],
        ["", "B", "B", "B", "W", "", "", ""],
        ["", "", "B", "B", "B", "W", "B", ""],
        ["", "", "W", "W", "W", "W", "W", ""],
        ["", "", "", "", "", "W", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    board_json = json.dumps(board_before)
    board_after = logic.place_piece(board_json, [5, 4], "B")
    board_expected = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "W", "", "", "", ""],
        ["", "B", "B", "B", "W", "", "", ""],
        ["", "", "B", "B", "B", "W", "B", ""],
        ["", "", "W", "B", "B", "B", "W", ""],
        ["", "", "", "", "B", "W", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    assert board_after == board_expected


def test_valid_board_init():
    """Tests the valid_board method in game_logic with correct initial board"""
    # case 1: game with intial states
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

def test_valid_board_incorrect():
    """Tests the valid_board method in game_logic with incorrect boards"""
    # case 2: initializing game with incorrect json
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

    # case 3: initializing game with incorrect json
    expected_board = [
        # board with incorrect inner array length
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "W", "B", "", "", "", ""],
        ["", "", "", "B", "W", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
    ]
    board_json = json.dumps(expected_board)
    with pytest.raises(ValueError) as excinfo:
        logic._valid_board(board_json)
    assert "Invalid board format: inner" in str(excinfo.value)

    # case 4: initializing game with incorrect json
    expected_board = [
        # board with values other that "B", "W", ""
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "P", "W", "", "", "", "", ""],
        ["", "", "B", "W", "B", "", "", ""],
        ["", "", "", "B", "W", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    board_json = json.dumps(expected_board)
    with pytest.raises(ValueError) as excinfo:
        logic._valid_board(board_json)
    assert "Invalid cell value in board string" in str(excinfo.value)


def test_flip_piece():
    # case 1: one direction of pieces needs to be flipped
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

    # case 2: two directions of pieces need to be flipped
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

def test_valid_moves_easy():
    """Tests the valid_moves function for easy cases"""
    # case 1: game with 3 valid moves
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

    # case 2: game with 5 valid moves (easy)
    board = [
        ["", "", "", "",  "",   "", "", ""],
        ["", "", "", "",  "",   "", "", ""],
        ["", "", "", "",  "",   "", "", ""],
        ["", "", "", "W", "B",  "", "", ""],
        ["", "", "", "W", "B", "B", "", ""],
        ["", "", "", "W", "",   "", "", ""],
        ["", "", "", "",  "",   "", "", ""],
        ["", "", "", "",  "",   "", "", ""],
    ]
    moves = logic._valid_moves(board, "B") # should return a list containing valid moves for the turn
    expected_moves = [[2, 2], [3, 2], [4, 2], [5, 2], [6, 2]]

    # compare 2 lists regardless of their order
    returned_tuple_set = {tuple(elem) for elem in moves}
    expected_tuple_set = {tuple(elem) for elem in expected_moves}
    assert returned_tuple_set == expected_tuple_set

    # case 3: game with 9 valid moves (easy)
    board = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "W", "B", "", "", ""],
        ["", "", "", "W", "B", "B", "", ""],
        ["", "", "", "W", "W", "W", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    moves = logic._valid_moves(board, "B") # should return a list containing valid moves for the turn
    expected_moves = [[2, 2], [3, 2], [4, 2], [5, 2], [6, 2], 
                      [6, 3], [6, 4], [6, 5], [6, 6]]

    # compare 2 lists regardless of their order
    returned_tuple_set = {tuple(elem) for elem in moves}
    expected_tuple_set = {tuple(elem) for elem in expected_moves}
    assert returned_tuple_set == expected_tuple_set


def test_valid_moves_hard():
    """Tests the valid_moves function for complicated cases"""

    # case 4: game with 10+ valid moves (complicated)
    board = [
        ["", "",  "",  "",  "",  "", "",  ""],
        ["", "",  "",  "B", "W", "", "B", ""],
        ["", "B", "B", "B", "",  "W", "", ""],
        ["", "",  "W", "B", "B", "", "W", ""],
        ["", "W", "W", "B", "B", "", "",  ""],
        ["", "B", "B", "W", "",  "B","",  ""],
        ["", "",  "W", "",  "W", "", "",  ""],
        ["", "",  "",  "",  "",  "", "",  ""],
    ]
    moves = logic._valid_moves(board, "W") # should return a list containing valid moves for the turn
    expected_moves = [[0, 3], [0, 7], [1, 0], [1, 2], [2, 4],
                      [3, 5], [4, 0], [4, 5], [4, 6], [5, 0],
                      [5, 4], [6, 0], [6, 1], [6, 3]]

    # compare 2 lists regardless of their order
    returned_tuple_set = {tuple(elem) for elem in moves}
    expected_tuple_set = {tuple(elem) for elem in expected_moves}
    assert returned_tuple_set == expected_tuple_set

    # case 5: game with 9 valid moves (complicated)
    board = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "W", "W", "W", "", ""],
        ["", "", "", "W", "B", "W", "", ""],
        ["", "", "", "B", "W", "W", "", ""],
        ["", "", "B", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    moves = logic._valid_moves(board, "B") # should return a list containing valid moves for the turn
    expected_moves = [[2, 2], [2, 3], [2, 4], [2, 6], 
                      [4, 2], [4, 6],
                      [5, 6], [6, 4], [6, 6]]

    # compare 2 lists regardless of their order
    returned_tuple_set = {tuple(elem) for elem in moves}
    expected_tuple_set = {tuple(elem) for elem in expected_moves}
    assert returned_tuple_set == expected_tuple_set