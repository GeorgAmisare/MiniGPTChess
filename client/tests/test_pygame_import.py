"""Простейший тест клиента."""

import pytest

pygame = pytest.importorskip("pygame")


def test_pygame_import() -> None:
    """Проверяет, что модуль ``pygame`` доступен."""
    assert hasattr(pygame, "__version__")
