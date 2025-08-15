"""Локальная проверка ходов с использованием python-chess."""

from __future__ import annotations

from typing import List, Optional, Tuple

import chess


def validate_and_apply_move(
    fen: str, move: str
) -> Tuple[Optional[chess.Board], List[str]]:
    """Проверить ход в формате UCI и применить его к позиции ``fen``.

    Parameters
    ----------
    fen: str
        Текущее состояние игры в нотации FEN.
    move: str
        Ход в формате UCI (например, ``"e2e4"``).

    Returns
    -------
    tuple
        ``(board, errors)``: ``board`` — обновлённый ``chess.Board`` при успехе
        (``None`` при ошибке), ``errors`` — список кодов ошибок.
    """
    errors: List[str] = []

    try:
        board = chess.Board(fen)
    except ValueError:
        return None, ["invalid_fen"]

    try:
        uci_move = chess.Move.from_uci(move)
    except ValueError:
        return None, ["illegal_client_move"]

    if uci_move not in board.legal_moves:
        return None, ["illegal_client_move"]

    board.push(uci_move)
    board.fen()

    return board, errors
