"""Pydantic models for MiniGPTChess server."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class MoveRequest(BaseModel):
    """Client move request."""

    fen: str = Field(..., description="Board position in FEN")
    side: Literal["w", "b"]
    client_move: Optional[str] = Field(
        None, description="Player move in UCI format"
    )


class Flags(BaseModel):
    """Status flags for current board."""

    check: bool
    checkmate: bool
    stalemate: bool


class MoveResponse(BaseModel):
    """Server response to a move request."""

    status: str = "ok"
    applied_client_move: bool
    ai_move: Optional[str]
    new_fen: str
    flags: Flags
    errors: List[str] = Field(default_factory=list)
