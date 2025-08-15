"""Обёртка над общими функциями шахматной логики для клиента."""

from chess_logic.common import compute_game_flags, validate_and_apply_move

__all__ = ["validate_and_apply_move", "compute_game_flags"]
