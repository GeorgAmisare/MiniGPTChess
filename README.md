# MiniGPTChess

This repository hosts a minimal chess application exploring GPT-generated moves.

## Server

Pydantic models for the `/move` endpoint live in `server/app/schemas.py`. They define
request and response bodies along with enumerated error codes and game state flags.

FastAPI server with health check endpoint.

### Server Chess Logic

The server provides helper utilities for working with chess rules in
`server/app/chess_logic.py`. The module validates UCI moves against a
supplied FEN, applies legal moves, recalculates the board's FEN, and
computes game state flags such as checkmate or stalemate.

### Run Server

```bash
python -m server.app.main
```

### Endpoints

- `GET /health` — return service status.