````markdown
# MiniGPTChess

This repository hosts a minimal chess application exploring GPT-generated moves.

Server uses the OpenAI Responses API to select AI moves. Set the
`OPENAI_API_KEY` environment variable before running the server. If the
API call fails or returns an invalid move, a random legal move is used.

## Client

`client/main.py` opens a PyGame window and renders a chess board using
Unicode pieces. The board state is stored as a FEN string so it can be
updated after each move.

Run the client:

```bash
python client/main.py
````

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

```
```
