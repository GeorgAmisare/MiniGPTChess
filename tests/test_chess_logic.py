"""Тесты утилит шахматной логики."""

import chess


def test_validate_and_apply_move_success():
    from server.app.chess_logic import validate_and_apply_move

    board, errors = validate_and_apply_move(chess.STARTING_FEN, "e2e4")
    assert not errors
    assert board is not None
    assert board.fen() == "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"


def test_validate_and_apply_move_illegal():
    from server.app.chess_logic import validate_and_apply_move

    board, errors = validate_and_apply_move(chess.STARTING_FEN, "e2e5")
    assert board is None
    assert errors


def test_compute_game_flags_checkmate():
    board = chess.Board()
    for mv in ["f2f3", "e7e5", "g2g4", "d8h4"]:
        board.push_uci(mv)
    from server.app.chess_logic import compute_game_flags

    flags = compute_game_flags(board)
    assert flags["checkmate"]
    assert flags["check"]
    assert not flags["stalemate"]
