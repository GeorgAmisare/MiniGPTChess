"""Тесты проверки ходов клиента."""

from fastapi.testclient import TestClient


EXPECTED_FLAGS = {
    "check": False,
    "checkmate": False,
    "stalemate": False,
    "insufficient_material": False,
    "seventyfive_moves": False,
    "fivefold_repetition": False,
}


def test_legal_client_move(monkeypatch):
    """Легальный ход должен применяться без ошибок."""

    def fake_ai(_fen, legal):  # pragma: no cover
        return legal[0]

    monkeypatch.setattr("server.app.gpt_client.get_ai_move", fake_ai)
    monkeypatch.setattr("server.app.routes.get_ai_move", fake_ai)
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
    assert data["status"] == "ok"
    assert data["applied_client_move"] is True
    assert data["errors"] == []
    assert data["flags"] == EXPECTED_FLAGS


def test_illegal_client_move(client):
    """Нелегальный ход должен вернуть ошибку."""
    payload = {
        "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "side": "w",
        "client_move": "e2e5",
    }
    response = client.post("/move", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["applied_client_move"] is False
    assert data["errors"] == ["illegal_client_move"]
    assert data["flags"] == EXPECTED_FLAGS


def test_invalid_fen(client):
    """Некорректный FEN приводит к ошибке."""
    payload = {"fen": "invalid", "side": "w"}
    response = client.post("/move", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["errors"] == ["invalid_fen"]
    assert data["flags"] == EXPECTED_FLAGS


def test_side_to_move_mismatch(client):
    """Несовпадение стороны хода фиксируется как ошибка."""
    payload = {
        "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "side": "b",
    }
    response = client.post("/move", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["errors"] == ["side_to_move_mismatch"]
    assert data["flags"] == EXPECTED_FLAGS
