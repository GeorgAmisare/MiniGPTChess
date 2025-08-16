"""Загрузка настроек клиента из переменных окружения."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Определяем директорию, где искать файл `.env`
_base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
load_dotenv(_base_dir / ".env")
try:
    SERVER_URL = os.environ["SERVER_URL"]
except KeyError as exc:
    raise RuntimeError(
        "Переменная окружения SERVER_URL не задана"
    ) from exc
