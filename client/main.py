"""Клиент PyGame для отображения шахматной доски по строке FEN."""

from __future__ import annotations

import threading
from typing import Iterable

import httpx
import pygame

WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
LAST_MOVE_COLOR = (246, 246, 105)
SELECT_COLOR = (106, 170, 100)
BOARD_SIZE = 8
SQUARE_SIZE = 80
WINDOW_SIZE = BOARD_SIZE * SQUARE_SIZE
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
SERVER_URL = "http://localhost:8000"
REQUEST_TIMEOUT = 30.0  # таймаут ожидания ответа сервера, сек

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


def draw_board(
    screen: pygame.Surface,
    board: Board,
    last_move: Iterable[tuple[int, int]] | None = None,
    selected: tuple[int, int] | None = None,
) -> None:
    """Нарисовать доску и фигуры на экране."""
    font = pygame.font.SysFont(None, 64)
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
                    pygame.Color("black"),
                )
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)


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

    def send_move(move: str) -> None:
        """Отправить ход на сервер и обработать ответ."""
        nonlocal last_move, message, waiting
        try:
            payload = {
                "fen": board.fen,
                "side": board.side,
                "client_move": move,
            }
            response = httpx.post(
                f"{SERVER_URL}/move", json=payload, timeout=REQUEST_TIMEOUT
            )
            data = response.json()
            if data.get("new_fen"):
                board.set_fen(data["new_fen"])
            if data.get("ai_move"):
                last_move = list(uci_to_coords(data["ai_move"]))
            else:
                last_move = list(uci_to_coords(move))
            flags = [k for k, v in data.get("flags", {}).items() if v]
            errors = data.get("errors", [])
            parts = []
            if flags:
                parts.append("Флаги: " + ", ".join(flags))
            if errors:
                parts.append("Ошибки: " + ", ".join(errors))
            message = " | ".join(parts)
        except Exception as exc:  # pragma: no cover - сетевые ошибки
            message = f"Ошибка запроса: {exc}"
        waiting = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and not waiting
            ):
                col = event.pos[0] // SQUARE_SIZE
                row = event.pos[1] // SQUARE_SIZE
                if selected is None:
                    selected = (row, col)
                else:
                    move = coords_to_uci(*selected) + coords_to_uci(row, col)
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
