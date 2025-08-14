"""FastAPI application providing health check endpoint."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server.app.main:app", host="0.0.0.0", port=8000)
