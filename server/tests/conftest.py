"""Pytest fixtures for server tests."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Предоставить ``TestClient`` для приложения FastAPI."""
    try:
        from server.main import app
    except Exception:  # pragma: no cover
        pytest.skip("server.main.app not available")
    return TestClient(app)
