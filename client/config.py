"""Загрузка настроек клиента из переменных окружения."""

import os
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL", "http://<PUBLIC_IP>:<PORT>")