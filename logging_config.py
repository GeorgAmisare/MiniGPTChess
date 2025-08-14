"""Настройка логирования проекта."""

import logging


def setup_logging() -> None:
    """Настроить базовое логирование."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

