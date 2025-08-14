## Architectural Principles

1. **Stateless server** — each request provides the full game state (FEN + side); the server stores no sessions (MVP).
2. **Single source of rules** — all chess logic, move validation, and check/checkmate/stalemate detection are performed on the server (`python-chess`).
3. **Simple protocol** — HTTP, JSON, minimal API (`/move`, `/new`, `/health`) with a unified data format.
4. **UCI move format** — all moves strictly use UCI notation (`e2e4`, `e7e8q`, castling `e1g1`, `resign`, `draw`).
5. **GPT move generation** — prompts include the current FEN, side to move, and a list of legal moves. GPT’s response must be exactly one move from the list, with no extra text.
6. **Separation of concerns**:

   * **Client (PyGame)** — rendering, collecting user moves, sending data, processing responses.
   * **Server (FastAPI)** — validation, game logic, GPT communication.
   * **GPT API** — selecting a move based on FEN and legal moves.
7. **Modularity** — each major part (rendering, API requests, move logic, validation) implemented in a separate module/class.

## Coding Guidelines

* **Follow PEP8** — all Python code must comply with PEP8.
* **Clear naming** — variables, functions, and classes should clearly describe their purpose.
* **Small functions** — keep functions under 20–30 lines; avoid “god functions”.
* **Clear structure** — modules and files should have a clear purpose; folder structure should reflect application logic.
* **Comments and docstrings**:

  * Brief description of each function: inputs, outputs, purpose.
  * Explanation of complex algorithms.
* **Minimal “magic”** — avoid obscure or overly clever constructs.
* **Input validation** — check all inputs before passing to business logic.
* **Always validate moves** — before applying, ensure the move matches UCI format and is legal according to `python-chess`.

## Managing Code Complexity

1. **DRY** — don’t repeat yourself; refactor repeated code into functions/utilities.
2. **KISS** — choose the simplest solution that works reliably.
3. **YAGNI** — don’t build functionality “just in case” without a clear requirement.
4. **Low coupling** — modules should be loosely coupled with high internal cohesion.
5. **Code reviews** — check that changes comply with the architecture, technical plan, and this document.

## Task Execution Format

* Before starting — verify the task aligns with the architecture and technical plan.
* After completion — ensure changes don’t break API/data formats.
* Code should be understandable to a new developer without additional explanation.
* Each new feature should have a short description in README.
* Single repository — both client and server are maintained in the same repository, sharing a single README that describes the entire project.
* When you create a text for PR, write it in Russian.

---

# Technical Plan

## 1) Architecture (MVP)

```
flowchart LR
  C[Desktop App (PyGame)] <--> S[Server (FastAPI)]
  S <--> O[GPT API]
  S --- CH[(python-chess)]
```

**Key idea:** GPT acts as a move generator, but rules, validation, and game state evaluation are handled on the server using `python-chess`. The server is **stateless**: the client sends FEN + side in every request.

## 2) Tech Stack

* **Client (Desktop):** Python, PyGame; HTTP via `httpx`/`requests`.
* **Server:** Python, FastAPI + Uvicorn; `python-chess`; `pydantic`; `httpx` for GPT API.
* **GPT:** OpenAI Responses API (strict prompt → only a move in UCI format).

## 3) Data Format and Protocol

* Primary format: **FEN** + side to move.
* `/move` request:

```json
{
  "fen": "<FEN>",
  "side": "w|b",
  "client_move": "e2e4"  
}
```

* `/move` response:

```json
{
  "status": "ok",
  "applied_client_move": true,
  "ai_move": "c7c5",
  "new_fen": "<FEN>",
  "flags": {
    "check": false,
    "checkmate": false,
    "stalemate": false
  },
  "errors": []
}
```

* Additional endpoints: `/new`, `/health`.

## 4) Server Rules

1. Validate incoming data (FEN, move).
2. Apply the player’s move and check for game end.
3. Build prompt with FEN and list of legal moves.
4. Process GPT response; retry if format is invalid; fallback if necessary.
5. Apply AI move and return the new state.


## 5) Minimal Contract

* Move format: **UCI** only (`e2e4`, `e7e8q`, `e1g1`, etc.), including `resign`, `draw`.
* The server always returns the new FEN.


## 6) Security

* GPT key is stored only on the server.
* For MVP — run on a local PC or via tunnel (ngrok/Cloudflared).