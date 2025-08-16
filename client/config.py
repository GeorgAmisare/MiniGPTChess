"""Загрузка настроек клиента из переменных окружения."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def load_env_smart() -> None:
    # A) если уже есть переменная — ничего не делаем
    if "SERVER_URL" in os.environ:
        return

    # B) стандартная загрузка из текущего рабочего каталога (dev)
    load_dotenv()
    if "SERVER_URL" in os.environ:
        return

    # C) PyInstaller onefile: ресурсы распакованы в sys._MEIPASS
    meipass = Path(getattr(sys, "_MEIPASS", Path.cwd()))
    env_in_bundle = meipass / ".env"
    if env_in_bundle.exists():
        load_dotenv(env_in_bundle, override=False)
        if "SERVER_URL" in os.environ:
            return

    # D) .env в корне проекта рядом с папкой client (dev/pytest)
    project_root_env = Path(__file__).resolve().parents[1] / ".env"
    if project_root_env.exists():
        load_dotenv(project_root_env, override=False)

load_env_smart()

SERVER_URL = os.getenv("SERVER_URL")
if not SERVER_URL:
    raise RuntimeError("Переменная окружения SERVER_URL не задана")
