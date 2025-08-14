"""Приложение FastAPI с эндпоинтом проверки состояния."""

from fastapi import FastAPI

from .routes import router

app = FastAPI()
app.include_router(router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Вернуть статус работоспособности сервиса."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server.app.main:app", host="0.0.0.0", port=8000)
