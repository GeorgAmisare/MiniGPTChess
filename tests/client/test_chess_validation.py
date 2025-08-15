"""Тесты локальной проверки ходов на клиенте."""

import chess

from client.chess_validation import validate_and_apply_move


def test_validate_and_apply_move_success() -> None:
    """Ход должен применяться без ошибок."""
    board, errors = validate_and_apply_move(chess.STARTING_FEN, "e2e4")
    assert not errors
    assert board is not None
    assert board.fen() == (
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
    )


def test_validate_and_apply_move_illegal() -> None:
    """Нелегальный ход возвращает ошибку."""
    board, errors = validate_and_apply_move(chess.STARTING_FEN, "e2e5")
    assert board is None
    assert errors


def test_validate_and_apply_move_invalid_fen() -> None:
    """Неверная строка FEN должна вызывать ошибку."""
    board, errors = validate_and_apply_move("invalid", "e2e4")
    assert board is None
    assert errors
