"""Загрузка настроек клиента из переменных окружения."""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv

if getattr(sys, "frozen", False):
    base_dir = Path(sys.executable).resolve().parent
else:
    base_dir = Path(__file__).resolve().parent
load_dotenv(base_dir / ".env")

try:
    SERVER_URL = os.environ["SERVER_URL"]
except KeyError as exc:
    raise RuntimeError(
        "Переменная окружения SERVER_URL не задана",
    ) from exc
