"""Приложение FastAPI с эндпоинтом проверки состояния."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Добавляем корневую директорию проекта в путь поиска модулей
sys.path.append(str(Path(__file__).resolve().parents[2]))
from logging_config import setup_logging  # noqa: E402

from .routes import router  # noqa: E402

setup_logging()

app = FastAPI()

# Список разрешённых источников можно задать через CORS_ALLOW_ORIGINS
_origins_env = os.getenv("CORS_ALLOW_ORIGINS")
_allow_origins = (
    [o.strip() for o in _origins_env.split(",")] if _origins_env else ["*"]
)

# Включаем CORS, чтобы клиент мог обращаться с другого домена
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allow_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Вернуть статус работоспособности сервиса."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server.app.main:app", host="0.0.0.0", port=8000)
