# MiniGPTChess


This repository hosts a minimal chess application exploring GPT-generated moves.

## Server

Pydantic models for the `/move` endpoint live in `server/app/schemas.py`. They define
request and response bodies along with enumerated error codes and game state flags.

FastAPI server with health check endpoint.

### Run Server

```bash
python -m server.app.main
```

### Endpoints

- `GET /health` — return service status.