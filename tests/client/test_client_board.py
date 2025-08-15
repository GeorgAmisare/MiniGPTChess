import os
import pygame

from client.main import (
    Board,
    coords_to_uci,
    uci_to_coords,
    draw_board,
    get_piece_color,
    WHITE,
    BROWN,
    LAST_MOVE_COLOR,
    SELECT_COLOR,
    WINDOW_SIZE,
    SQUARE_SIZE,
    COORD_COLOR,
    COORD_FONT_SIZE,
)

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def test_coords_roundtrip() -> None:
    """Проверить преобразование координат в UCI и обратно."""
    start = (6, 4)  # e2
    end = (4, 4)  # e4
    move = coords_to_uci(*start) + coords_to_uci(*end)
    assert uci_to_coords(move) == (start, end)


def test_coords_edges() -> None:
    """Проверить преобразование крайних координат."""
    assert coords_to_uci(7, 0) == "a1"
    assert coords_to_uci(0, 7) == "h8"


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


def test_coordinates_no_overlap() -> None:
    """Проверить, что буквенно-цифровая разметка не перекрывается в углах."""
    pygame.init()
    screen = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
    board = Board("8/8/8/8/8/8/8/8 w - - 0 1")
    draw_board(screen, board)
    has_file = any(
        screen.get_at((x, y))[:3] == COORD_COLOR
        for x in range(SQUARE_SIZE)
        for y in range(COORD_FONT_SIZE)
    )
    has_rank = any(
        screen.get_at((x, y))[:3] == COORD_COLOR
        for x in range(COORD_FONT_SIZE)
        for y in range(SQUARE_SIZE)
    )
    assert has_file
    assert has_rank
    assert screen.get_at((2, 2))[:3] != COORD_COLOR
    pygame.quit()
