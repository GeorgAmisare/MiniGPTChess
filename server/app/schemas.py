"""Pydantic schemas for the server API."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class MoveErrorCode(str, Enum):
    """Enumeration of possible move processing errors."""

    INVALID_FEN = "invalid_fen"
    INVALID_MOVE = "invalid_move"
    ILLEGAL_MOVE = "illegal_move"
    ENGINE_ERROR = "engine_error"


class MoveRequest(BaseModel):
    """Request body for the `/move` endpoint."""

    fen: str = Field(..., description="Board position in FEN notation.")
    side: str = Field(..., description="Side to move: 'w' for white or 'b' for black.")
    client_move: Optional[str] = Field(
        None,
        description="Optional move supplied by the client in UCI notation.",
    )


class Flags(BaseModel):
    """Game state flags returned with a move response."""

    check: bool = False
    checkmate: bool = False
    stalemate: bool = False


class MoveResponse(BaseModel):
    """Response body for the `/move` endpoint."""

    status: str = Field(..., description="Overall status of the request.")
    applied_client_move: bool = Field(
        ..., description="Indicates whether the client's move was applied."
    )
    ai_move: Optional[str] = Field(
        None, description="Move chosen by the AI opponent in UCI notation."
    )
    new_fen: Optional[str] = Field(
        None, description="Resulting board position in FEN notation."
    )
    flags: Flags = Field(default_factory=Flags, description="Game state flags.")
    errors: List[MoveErrorCode] = Field(
        default_factory=list, description="List of errors encountered."
    )
