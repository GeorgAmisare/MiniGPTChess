"""Тесты проверки ходов клиента."""


def test_legal_client_move(client, monkeypatch):
    """Легальный ход должен применяться без ошибок."""

    def fake_ai(_fen, legal):  # pragma: no cover
        return legal[0]

    monkeypatch.setattr("server.app.routes.get_ai_move", fake_ai)
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


def test_invalid_fen(client):
    """Некорректный FEN приводит к ошибке."""
    payload = {"fen": "invalid", "side": "w"}
    response = client.post("/move", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["errors"] == ["invalid_fen"]


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
