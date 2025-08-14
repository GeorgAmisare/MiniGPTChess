"""Simple AI move selection for MiniGPTChess."""

import random

import chess


def choose_ai_move(board: chess.Board) -> chess.Move:
    """Return a random legal move for the current board."""
    return random.choice(list(board.legal_moves))
