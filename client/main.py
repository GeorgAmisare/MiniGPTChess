"""Клиент PyGame для отображения шахматной доски по строке FEN."""

from __future__ import annotations

import logging
import sys
import threading
from pathlib import Path
from typing import Iterable

import httpx
import pygame

# Добавляем корневую директорию проекта в путь поиска модулей
sys.path.append(str(Path(__file__).resolve().parents[1]))
from client.chess_validation import validate_and_apply_move  # noqa: E402
from logging_config import setup_logging  # noqa: E402

WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
LAST_MOVE_COLOR = (246, 246, 105)
SELECT_COLOR = (106, 170, 100)
COORD_COLOR = (0, 0, 0)
COORD_FONT_SIZE = 16
BOARD_SIZE = 8
SQUARE_SIZE = 80
WINDOW_SIZE = BOARD_SIZE * SQUARE_SIZE
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
SERVER_URL = "http://localhost:8000"

UNICODE_PIECES = {
    "K": "\u2654",
    "Q": "\u2655",
    "R": "\u2656",
    "B": "\u2657",
    "N": "\u2658",
    "P": "\u2659",
    "k": "\u265A",
    "q": "\u265B",
    "r": "\u265C",
    "b": "\u265D",
    "n": "\u265E",
    "p": "\u265F",
}


def get_piece_color(piece: str) -> pygame.Color:
    """Вернуть цвет фигуры для отображения.

    Белые фигуры обозначаются заглавными буквами, чёрные — строчными.

    Parameters
    ----------
    piece: str
        Символ фигуры в обозначении FEN.

    Returns
    -------
    pygame.Color
        Цвет для отрисовки фигуры.
    """
    return pygame.Color("white") if piece.isupper() else pygame.Color("black")


setup_logging()
logger = logging.getLogger(__name__)


class Board:
    """Хранит состояние доски на основе строки FEN."""

    def __init__(self, fen: str = START_FEN) -> None:
        self.set_fen(fen)

    def set_fen(self, fen: str) -> None:
        """Обновить доску из строки FEN."""
        self.fen = fen
        self.side = fen.split()[1]
        self._grid = self._fen_to_grid(fen)

    @staticmethod
    def _fen_to_grid(fen: str) -> list[list[str]]:
        """Преобразовать размещение фигур FEN в двумерный массив."""
        rows = fen.split()[0].split("/")
        grid: list[list[str]] = []
        for row in rows:
            cols: list[str] = []
            for char in row:
                if char.isdigit():
                    cols.extend([""] * int(char))
                else:
                    cols.append(char)
            grid.append(cols)
        return grid

    def piece_at(self, row: int, col: int) -> str:
        """Вернуть обозначение фигуры по координатам или пустую строку."""
        return self._grid[row][col]


def coords_to_uci(row: int, col: int) -> str:
    """Преобразовать координаты матрицы в запись клетки UCI."""
    files = "abcdefgh"
    ranks = "87654321"
    return files[col] + ranks[row]


def uci_to_coords(move: str) -> tuple[tuple[int, int], tuple[int, int]]:
    """Получить координаты из хода в формате UCI."""
    files = "abcdefgh"
    ranks = "87654321"
    from_sq = (ranks.index(move[1]), files.index(move[0]))
    to_sq = (ranks.index(move[3]), files.index(move[2]))
    return from_sq, to_sq


def can_select_square(board: Board, row: int, col: int) -> bool:
    """Проверить, можно ли выбрать клетку.

    Разрешено выделять только клетки со своими фигурами.

    Parameters
    ----------
    board: Board
        Текущее состояние доски.
    row: int
        Номер строки клетки.
    col: int
        Номер столбца клетки.

    Returns
    -------
    bool
        True, если в клетке находится фигура текущей стороны.
    """
    piece = board.piece_at(row, col)
    if not piece:
        return False
    return piece.isupper() if board.side == "w" else piece.islower()


def deselect_on_right(
    button: int, selected: tuple[int, int] | None
) -> tuple[int, int] | None:
    """Снять выделение при нажатии правой кнопкой мыши."""
    return None if button == 3 else selected


def draw_coordinates(screen: pygame.Surface) -> None:
    """Рисует буквенно-цифровую разметку внутри углов крайних клеток."""
    font = pygame.font.SysFont("DejaVu Sans", COORD_FONT_SIZE)
    files = "abcdefgh"  # слева -> вправо
    ranks = "87654321"  # сверху -> вниз
    pad = 4  # отступ от края угла

    # Верхний ряд: буквы в правом-верхнем углу каждой верхней клетки
    top_row_y = 0
    for col, file_char in enumerate(files):
        text = font.render(file_char, False, COORD_COLOR)
        x = (col + 1) * SQUARE_SIZE - pad
        y = top_row_y + pad
        rect = text.get_rect(topright=(x, y))
        screen.blit(text, rect)

    # Нижний ряд: буквы в левом-нижнем углу каждой нижней клетки
    bottom_row_y = (BOARD_SIZE - 1) * SQUARE_SIZE
    for col, file_char in enumerate(files):
        text = font.render(file_char, False, COORD_COLOR)
        x = col * SQUARE_SIZE + pad
        y = bottom_row_y + SQUARE_SIZE - pad
        rect = text.get_rect(bottomleft=(x, y))
        screen.blit(text, rect)

    # Левый столбец: цифры в левом-верхнем углу каждой левой клетки
    left_col_x = 0
    for row, rank_char in enumerate(ranks):
        text = font.render(rank_char, False, COORD_COLOR)
        x = left_col_x + pad
        y = row * SQUARE_SIZE + pad
        rect = text.get_rect(topleft=(x, y))
        screen.blit(text, rect)

    # Правый столбец: цифры в правом-нижнем углу каждой правой клетки
    right_col_x = (BOARD_SIZE - 1) * SQUARE_SIZE
    for row, rank_char in enumerate(ranks):
        text = font.render(rank_char, False, COORD_COLOR)
        x = right_col_x + SQUARE_SIZE - pad
        y = (row + 1) * SQUARE_SIZE - pad
        rect = text.get_rect(bottomright=(x, y))
        screen.blit(text, rect)


def draw_board(
    screen: pygame.Surface,
    board: Board,
    last_move: Iterable[tuple[int, int]] | None = None,
    selected: tuple[int, int] | None = None,
) -> None:
    """Нарисовать доску и фигуры на экране."""
    font = pygame.font.SysFont("DejaVu Sans", 64)
    last_move = set(last_move or [])
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            base_color = WHITE if (row + col) % 2 == 0 else BROWN
            color = base_color
            if (row, col) in last_move:
                color = LAST_MOVE_COLOR
            if selected == (row, col):
                color = SELECT_COLOR
            rect = pygame.Rect(
                col * SQUARE_SIZE,
                row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE,
            )
            pygame.draw.rect(screen, color, rect)
            piece = board.piece_at(row, col)
            if piece:
                text = font.render(
                    UNICODE_PIECES[piece],
                    True,
                    get_piece_color(piece),
                )
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    draw_coordinates(screen)


def main() -> None:
    """Основной цикл клиента."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("MiniGPTChess")
    board = Board()
    clock = pygame.time.Clock()
    running = True
    selected: tuple[int, int] | None = None
    last_move: list[tuple[int, int]] | None = None
    message = ""
    waiting = False
    logger.info("Клиент запущен")

    def send_move(move: str) -> None:
        """Отправить ход на сервер и обработать ответ."""
        nonlocal last_move, message, waiting
        try:
            payload = {
                "fen": board.fen,
                "side": board.side,
                "client_move": move,
            }
            logger.info("Отправка хода: %s", payload)
            response = httpx.post(
                f"{SERVER_URL}/move", json=payload, timeout=30.0
            )
            data = response.json()
            logger.info("Ответ сервера: %s", data)
            if data.get("new_fen"):
                board.set_fen(data["new_fen"])
            if data.get("ai_move"):
                last_move = list(uci_to_coords(data["ai_move"]))
            else:
                last_move = list(uci_to_coords(move))
            flags = [k for k, v in data.get("flags", {}).items() if v]
            errors = data.get("errors", [])
            if flags:
                logger.info("Флаги от сервера: %s", flags)
            if errors:
                logger.warning("Ошибки от сервера: %s", errors)
            parts = []
            if flags:
                parts.append("Флаги: " + ", ".join(flags))
            if errors:
                parts.append("Ошибки: " + ", ".join(errors))
            message = " | ".join(parts)
        except Exception as exc:  # pragma: no cover - сетевые ошибки
            logger.error("Ошибка запроса: %s", exc)
            message = f"Ошибка запроса: {exc}"
        waiting = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and not waiting
            ):
                col = event.pos[0] // SQUARE_SIZE
                row = event.pos[1] // SQUARE_SIZE
                selected = deselect_on_right(event.button, selected)
                if event.button == 1:
                    if selected is None:
                        if can_select_square(board, row, col):
                            selected = (row, col)
                    else:
                        move = (
                            coords_to_uci(*selected)
                            + coords_to_uci(row, col)
                        )
                        logger.info("Ход игрока: %s", move)
                        _, errors = validate_and_apply_move(board.fen, move)
                        if errors:
                            message = "Ошибки: " + ", ".join(errors)
                        else:
                            message = ""
                            waiting = True
                            threading.Thread(
                                target=send_move,
                                args=(move,),
                                daemon=True,
                            ).start()
                        selected = None

        draw_board(screen, board, last_move, selected)
        font = pygame.font.SysFont(None, 24)
        if message:
            text = font.render(message, True, pygame.Color("red"))
            screen.blit(text, (5, WINDOW_SIZE - 20))
        if waiting:
            wait_text = font.render(
                "Ожидание...",
                True,
                pygame.Color("blue"),
            )
            screen.blit(wait_text, (WINDOW_SIZE - 120, WINDOW_SIZE - 20))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main()
