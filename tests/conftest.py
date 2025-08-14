"""Фикстуры pytest для тестов сервера."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Предоставить ``TestClient`` для приложения FastAPI."""
    try:
        from server.app.main import app
    except Exception:  # pragma: no cover
        pytest.skip("server.app.main.app недоступно")
    return TestClient(app)
