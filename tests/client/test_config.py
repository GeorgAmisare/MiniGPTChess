"""Тесты для модуля client.config."""

import importlib


def test_server_url_from_env(monkeypatch):
    """Проверить чтение SERVER_URL из окружения."""
    monkeypatch.setenv("SERVER_URL", "http://example.com")
    import client.config as config
    importlib.reload(config)
    assert config.SERVER_URL == "http://example.com"
