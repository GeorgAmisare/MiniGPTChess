"""Tests for validating client moves."""

import chess


def test_legal_client_move(client):
    """A legal move should be applied and no errors returned."""
    payload = {
        "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "side": "w",
        "client_move": "e2e4",
    }
    response = client.post("/move", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["applied_client_move"] is True
    assert data["errors"] == []


def test_illegal_client_move(client):
    """An illegal move should not be applied and errors should be reported."""
    payload = {
        "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "side": "w",
        "client_move": "e2e5",
    }
    response = client.post("/move", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["applied_client_move"] is False
    assert data["errors"]
