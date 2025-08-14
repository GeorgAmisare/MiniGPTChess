"""Pytest fixtures for server tests."""

import pytest
from fastapi.testclient import TestClient

try:
    from server.main import app
except Exception:  # pragma: no cover
    app = None


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    if app is None:
        pytest.skip("server.main.app not available")
    return TestClient(app)
