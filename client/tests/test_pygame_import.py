"""Простейший тест клиента."""


def test_pygame_import() -> None:
    """Проверяет, что модуль ``pygame`` доступен."""
    import pygame  # noqa: WPS433

    assert hasattr(pygame, "__version__")
