"""Тесты отката хода ИИ при неверном ответе GPT."""

import chess


def test_ai_move_fallback(monkeypatch, client):
    """При неверном ходе GPT сервер выбирает легальный ход."""

    def fake_gpt(*args, **kwargs):  # pragma: no cover
        return "zzzz"

    monkeypatch.setattr("server.app.routes.get_ai_move", fake_gpt)
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
