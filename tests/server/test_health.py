"""Тесты для эндпоинта проверки состояния."""


def test_health(client):
    """Эндпоинт /health возвращает статус ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
