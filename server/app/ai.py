"""Простейший выбор хода ИИ для MiniGPTChess."""

import random

import chess


def choose_ai_move(board: chess.Board) -> chess.Move:
    """Вернуть случайный легальный ход для текущей позиции."""
    return random.choice(list(board.legal_moves))
