"""Tests for checkmate and stalemate detection."""


def test_checkmate_detection(monkeypatch, client):
    """AI move leading to checkmate should set the flag accordingly."""

    def fake_gpt(*args, **kwargs):  # pragma: no cover
        return "d8h4"

    monkeypatch.setattr("server.gpt.generate_move", fake_gpt, raising=False)
    payload = {
        "fen": "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2",
        "side": "b",
        "client_move": "g2g4",
    }
    response = client.post("/move", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["flags"]["checkmate"] is True


def test_stalemate_detection(client):
    """Client move that leads to stalemate should be reported."""
    payload = {
        "fen": "k7/1Q6/2K5/8/8/8/8/8 w - - 0 1",
        "side": "w",
        "client_move": "b7c7",
    }
    response = client.post("/move", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["flags"]["stalemate"] is True
