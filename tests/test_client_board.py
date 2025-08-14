"""Тесты для клиентской доски.

Пропускаются, если отсутствует ``pygame``.
"""

import os
import pytest
import pygame

from client.main import (
    Board,
    coords_to_uci,
    uci_to_coords,
    draw_board,
    WHITE,
    BROWN,
    LAST_MOVE_COLOR,
    SELECT_COLOR,
    WINDOW_SIZE,
    SQUARE_SIZE,
)

pygame = pytest.importorskip("pygame")

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def test_coords_roundtrip() -> None:
    """Проверить преобразование координат в UCI и обратно."""
    start = (6, 4)  # e2
    end = (4, 4)  # e4
    move = coords_to_uci(*start) + coords_to_uci(*end)
    assert uci_to_coords(move) == (start, end)


def test_board_piece_parsing() -> None:
    """Проверить чтение фигур из строки FEN."""
    board = Board("8/8/8/8/8/8/8/4K3 w - - 0 1")
    assert board.piece_at(7, 4) == "K"
    board.set_fen("8/8/8/8/8/8/8/3k4 b - - 0 1")
    assert board.side == "b"
    assert board.piece_at(7, 3) == "k"


def test_draw_board_colors() -> None:
    """Убедиться, что подсветка и базовые цвета отрисовываются корректно."""
    pygame.init()
    screen = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
    board = Board("8/8/8/8/8/8/8/8 w - - 0 1")
    draw_board(screen, board, last_move=[(0, 1)], selected=(1, 1))
    assert screen.get_at((1, 1))[:3] == WHITE
    assert screen.get_at((SQUARE_SIZE + 1, 1))[:3] == LAST_MOVE_COLOR
    assert screen.get_at(
        (SQUARE_SIZE * 3 + 1, 1)
    )[:3] == BROWN
    assert screen.get_at(
        (SQUARE_SIZE + 1, SQUARE_SIZE + 1)
    )[:3] == SELECT_COLOR
    pygame.quit()
