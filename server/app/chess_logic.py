"""Chess logic utilities for move validation and game state evaluation."""

from __future__ import annotations

from typing import List, Optional, Tuple, Dict

import chess


def validate_and_apply_move(fen: str, move: str) -> Tuple[Optional[chess.Board], List[str]]:
    """Validate a UCI move and apply it to a board described by ``fen``.

    Parameters
    ----------
    fen: str
        Current game state in Forsyth-Edwards Notation.
    move: str
        Move in UCI notation (e.g. ``"e2e4"``).

    Returns
    -------
    tuple
        ``(board, errors)`` where ``board`` is the updated ``chess.Board`` on
        success (``None`` if validation fails) and ``errors`` contains any
        validation error messages.
    """

    errors: List[str] = []

    try:
        board = chess.Board(fen)
    except ValueError:
        return None, ["invalid FEN"]

    try:
        uci_move = chess.Move.from_uci(move)
    except ValueError:
        return None, ["invalid move format"]

    if uci_move not in board.legal_moves:
        return None, ["illegal move"]

    board.push(uci_move)
    # Recalculate FEN to keep board state consistent after the move.
    board.fen()

    return board, errors


def compute_game_flags(board: chess.Board) -> Dict[str, bool]:
    """Return a mapping of game state flags for ``board``.

    The flags include common terminal conditions as well as simple checks.
    """

    return {
        "check": board.is_check(),
        "checkmate": board.is_checkmate(),
        "stalemate": board.is_stalemate(),
        "insufficient_material": board.is_insufficient_material(),
        "seventyfive_moves": board.is_seventyfive_moves(),
        "fivefold_repetition": board.is_fivefold_repetition(),
    }
