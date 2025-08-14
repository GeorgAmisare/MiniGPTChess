# MiniGPTChess

## Server Chess Logic

The server provides helper utilities for working with chess rules in
`server/app/chess_logic.py`. The module validates UCI moves against a
supplied FEN, applies legal moves, recalculates the board's FEN, and
computes game state flags such as checkmate or stalemate.

