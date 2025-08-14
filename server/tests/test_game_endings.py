"""Тесты обнаружения шахматных окончаний."""


def test_checkmate_detection(monkeypatch, client):
    """Ход ИИ, приводящий к мату, должен установить флаг."""

    def fake_gpt(*args, **kwargs):  # pragma: no cover
        return "d8h4"

    monkeypatch.setattr("server.app.routes.get_ai_move", fake_gpt)
    payload = {
        "fen": "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2",
        "side": "b",
    }
    response = client.post("/move", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["errors"] == []
    assert data["flags"]["checkmate"] is True


def test_stalemate_detection(client):
    """Ход клиента, ведущий к пату, должен быть зафиксирован."""
    payload = {
        "fen": "k7/1Q6/2K5/8/8/8/8/8 w - - 0 1",
        "side": "w",
        "client_move": "b7c7",
    }
    response = client.post("/move", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["errors"] == ["no_legal_moves"]
    assert data["flags"]["stalemate"] is True
