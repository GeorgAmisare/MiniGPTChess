"""Клиент PyGame для отображения шахматной доски по строке FEN."""

from __future__ import annotations

import pygame

WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
BOARD_SIZE = 8
SQUARE_SIZE = 80
WINDOW_SIZE = BOARD_SIZE * SQUARE_SIZE
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

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


def draw_board(screen: pygame.Surface, board: Board) -> None:
    """Нарисовать доску и фигуры на экране."""
    font = pygame.font.SysFont(None, 64)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            rect = pygame.Rect(
                col * SQUARE_SIZE,
                row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE,
            )
            pygame.draw.rect(screen, color, rect)
            piece = board.piece_at(row, col)
            if piece:
                text = font.render(UNICODE_PIECES[piece], True, pygame.Color("black"))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)


def main() -> None:
    """Инициализировать окно и отрисовать стартовую доску."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("MiniGPTChess")
    board = Board()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_board(screen, board)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main()
