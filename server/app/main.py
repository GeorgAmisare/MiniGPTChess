"""Приложение FastAPI с эндпоинтом проверки состояния."""

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Добавляем корневую директорию проекта в путь поиска модулей
sys.path.append(str(Path(__file__).resolve().parents[2]))
from logging_config import setup_logging  # noqa: E402

from .routes import router  # noqa: E402

setup_logging()

app = FastAPI()
# Разрешаем запросы с любых источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
