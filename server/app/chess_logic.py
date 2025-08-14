"""Утилиты шахматной логики для проверки ходов и оценки состояния игры."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import chess

from .models import ErrorCode


def validate_and_apply_move(fen: str, move: str) -> Tuple[Optional[chess.Board], List[ErrorCode]]:
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

    errors: List[ErrorCode] = []

    try:
        board = chess.Board(fen)
    except ValueError:
        return None, [ErrorCode.INVALID_FEN]

    try:
        uci_move = chess.Move.from_uci(move)
    except ValueError:
        return None, [ErrorCode.ILLEGAL_CLIENT_MOVE]

    if uci_move not in board.legal_moves:
        return None, [ErrorCode.ILLEGAL_CLIENT_MOVE]

    board.push(uci_move)
    board.fen()

    return board, errors


def compute_game_flags(board: chess.Board) -> Dict[str, bool]:
    """Получить словарь флагов состояния игры для позиции ``board``.

    Флаги включают распространённые терминальные условия и простые проверки.
    """

    return {
        "check": board.is_check(),
        "checkmate": board.is_checkmate(),
        "stalemate": board.is_stalemate(),
        "insufficient_material": board.is_insufficient_material(),
        "seventyfive_moves": board.is_seventyfive_moves(),
        "fivefold_repetition": board.is_fivefold_repetition(),
    }
