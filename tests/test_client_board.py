"""Тесты для клиентской доски.

Пропускается, если отсутствует pygame."""

import pytest

pygame = pytest.importorskip("pygame")


def test_pygame_import() -> None:
    """Проверяет возможность импорта pygame."""
    assert pygame
