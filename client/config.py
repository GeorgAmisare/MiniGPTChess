"""Загрузка настроек клиента из переменных окружения."""

import os
from dotenv import load_dotenv

load_dotenv()
try:
    SERVER_URL = os.environ["SERVER_URL"]
except KeyError as exc:
    raise RuntimeError(
        "Переменная окружения SERVER_URL не задана"
    ) from exc
