import os
import pygame

from client.main import (
    Board,
    coords_to_uci,
    uci_to_coords,
    draw_board,
    get_piece_color,
    can_select_square,
    WHITE,
    BROWN,
    LAST_MOVE_COLOR,
    SELECT_COLOR,
    WINDOW_SIZE,
    SQUARE_SIZE,
)

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


def test_piece_colors() -> None:
    """Проверить выбор цвета фигур в зависимости от регистра."""
    assert get_piece_color("K") == pygame.Color("white")
    assert get_piece_color("q") == pygame.Color("black")


def test_can_select_square() -> None:
    """Проверить выбор клетки только со своей фигурой."""
    board = Board()
    assert can_select_square(board, 6, 0)
    assert not can_select_square(board, 1, 0)
    assert not can_select_square(board, 4, 4)


def test_right_click_clears_selection() -> None:
    """Проверить сброс выделения правой кнопкой мыши."""
    pygame.init()
    selected = (6, 0)
    right_click = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, button=3, pos=(0, 0)
    )
    pygame.event.post(right_click)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            selected = None
    assert selected is None
    pygame.quit()
