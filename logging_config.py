"""Настройка уровня логирования для MiniGPTChess."""

import logging
import os


def setup_logging() -> None:
    """Настроить вывод логов в зависимости от переменной окружения.

    Если переменная ``DEBUG_LOGS`` установлена в ``"1"``, уровень логирования
    устанавливается на ``INFO``. В противном случае используются предупреждения
    и ошибки.
    """
    level = logging.INFO if os.getenv("DEBUG_LOGS") == "1" else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
