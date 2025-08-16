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


def test_server_url_from_file(monkeypatch):
    """SERVER_URL должен считываться из client/.env."""
    from pathlib import Path

    env_path = Path(__file__).resolve().parents[2] / "client" / ".env"
    env_path.write_text("SERVER_URL=http://fromfile\n")
    try:
        monkeypatch.delenv("SERVER_URL", raising=False)
        import client.config as config
        importlib.reload(config)
        assert config.SERVER_URL == "http://fromfile"
    finally:
        env_path.unlink()
