"""Tests for AI move fallback when GPT returns invalid move."""

import chess


def test_ai_move_fallback(monkeypatch, client):
    """If GPT suggests an invalid move, server should fall back to a legal one."""

    def fake_gpt(*args, **kwargs):  # pragma: no cover
        return "zzzz"

    monkeypatch.setattr("server.gpt.generate_move", fake_gpt, raising=False)
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
