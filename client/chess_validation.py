"""Обёртка над общими функциями шахматной логики для клиента."""

from shared.chess import compute_game_flags, validate_and_apply_move

__all__ = ["validate_and_apply_move", "compute_game_flags"]
