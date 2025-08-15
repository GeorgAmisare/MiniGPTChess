"""Тесты обнаружения шахматных окончаний."""

from fastapi.testclient import TestClient


def test_checkmate_detection(monkeypatch):
    """Ход ИИ, приводящий к мату, должен установить флаг."""

    def fake_gpt(*args, **kwargs):  # pragma: no cover
        return "d8h4"

    monkeypatch.setattr("server.app.gpt_client.get_ai_move", fake_gpt)
    monkeypatch.setattr("server.app.routes.get_ai_move", fake_gpt)
    from server.app.main import app

    client = TestClient(app)
    payload = {
        "fen": "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2",
        "side": "b",
    }
    response = client.post("/move", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["errors"] == []
    assert data["flags"] == {
        "check": True,
        "checkmate": True,
        "stalemate": False,
        "insufficient_material": False,
        "seventyfive_moves": False,
        "fivefold_repetition": False,
    }


def test_stalemate_detection(client):
    """Ход клиента, ведущий к пату, должен быть зафиксирован без ошибок."""
    payload = {
        "fen": "k7/1Q6/2K5/8/8/8/8/8 w - - 0 1",
        "side": "w",
        "client_move": "b7c7",
    }
    response = client.post("/move", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["errors"] == []
    assert data["flags"] == {
        "check": False,
        "checkmate": False,
        "stalemate": True,
        "insufficient_material": False,
        "seventyfive_moves": False,
        "fivefold_repetition": False,
    }


def test_checkmate_after_client_move(client):
    """Ход клиента, приводящий к мату, должен завершить игру без ошибок."""

    payload = {
        "fen": "k7/8/1QK5/8/8/8/8/8 w - - 0 1",
        "side": "w",
        "client_move": "b6b7",
    }
    response = client.post("/move", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["errors"] == []
    assert data["flags"] == {
        "check": True,
        "checkmate": True,
        "stalemate": False,
        "insufficient_material": False,
        "seventyfive_moves": False,
        "fivefold_repetition": False,
    }
