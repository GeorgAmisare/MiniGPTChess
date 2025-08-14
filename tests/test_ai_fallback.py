"""Тесты отката хода ИИ при неверном ответе GPT."""

import chess
from fastapi.testclient import TestClient


EXPECTED_FLAGS = {
    "check": False,
    "checkmate": False,
    "stalemate": False,
    "insufficient_material": False,
    "seventyfive_moves": False,
    "fivefold_repetition": False,
}


def test_ai_move_fallback(monkeypatch):
    """При неверном ходе GPT сервер выбирает легальный ход."""

    def fake_gpt(*args, **kwargs):  # pragma: no cover
        return "zzzz"

    monkeypatch.setattr("server.app.gpt_client.get_ai_move", fake_gpt)
    monkeypatch.setattr("server.app.routes.get_ai_move", fake_gpt)
    from server.app.main import app

    client = TestClient(app)
    payload = {
        "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "side": "w",
        "client_move": "e2e4",
    }
    response = client.post("/move", json=payload)
    assert response.status_code == 200
    data = response.json()
    board = chess.Board()
    board.push_uci("e2e4")
    assert chess.Move.from_uci(data["ai_move"]) in board.legal_moves
    assert data["ai_move"] != "zzzz"
    assert data["status"] == "error"
    assert data["errors"] == ["gpt_invalid_move"]
    assert data["flags"] == EXPECTED_FLAGS
