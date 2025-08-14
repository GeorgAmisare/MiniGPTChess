"""Pydantic-схемы для сервера MiniGPTChess."""

from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ErrorCode(str, Enum):
    """Коды возможных ошибок при обработке хода."""

    ILLEGAL_CLIENT_MOVE = "illegal_client_move"
    NO_LEGAL_MOVES = "no_legal_moves"
    INVALID_FEN = "invalid_fen"
    GPT_INVALID_MOVE = "gpt_invalid_move"
    SERVER_ERROR = "server_error"


class MoveRequest(BaseModel):
    """Запрос хода от клиента."""

    fen: str = Field(..., description="Позиция на доске в формате FEN")
    side: Literal["w", "b"]
    client_move: Optional[str] = Field(
        None, description="Ход игрока в формате UCI"
    )


class Flags(BaseModel):
    """Флаги состояния текущей позиции."""

    check: bool
    checkmate: bool
    stalemate: bool
    insufficient_material: bool
    seventyfive_moves: bool
    fivefold_repetition: bool


class MoveResponse(BaseModel):
    """Ответ сервера на запрос хода."""

    status: str = "ok"
    applied_client_move: bool
    ai_move: Optional[str]
    new_fen: str
    flags: Flags
    errors: List[ErrorCode] = Field(default_factory=list)
