"""Пакет сервера для MiniGPTChess.

Загружает переменные окружения из файла ``server/.env``.
"""

from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")
