"""Тесты для модуля client.config."""

import importlib

import pytest


def test_server_url_from_env(monkeypatch):
    """Проверить чтение SERVER_URL из окружения."""
    monkeypatch.setenv("SERVER_URL", "http://example.com")
    import client.config as config
    importlib.reload(config)
    assert config.SERVER_URL == "http://example.com"


def test_missing_server_url_raises(monkeypatch):
    """Отсутствие SERVER_URL должно вызывать ошибку."""
    import client.config as config
    monkeypatch.delenv("SERVER_URL", raising=False)
    with pytest.raises(RuntimeError):
        importlib.reload(config)
