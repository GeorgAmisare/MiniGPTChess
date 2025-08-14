"""Тесты для эндпоинта создания новой игры."""

import chess


def test_new_game(client):
    """Эндпоинт /new возвращает стартовый FEN и сторону "w"."""
    response = client.post("/new")
    assert response.status_code == 200
    assert response.json() == {"fen": chess.STARTING_FEN, "side": "w"}

