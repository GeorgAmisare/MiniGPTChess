"""Маршруты API для сервера MiniGPTChess."""

from fastapi import APIRouter, HTTPException
import chess

from .models import ErrorCode, Flags, MoveRequest, MoveResponse
from .chess_logic import compute_game_flags, validate_and_apply_move
from .gpt_client import get_ai_move

router = APIRouter()


@router.post("/move", response_model=MoveResponse)
async def move(request: MoveRequest) -> MoveResponse:
    """Обработать ход клиента и вернуть ответ ИИ."""
    try:
        board = chess.Board(request.fen)
    except ValueError as exc:
        raise HTTPException(
            status_code=400, detail=ErrorCode.INVALID_FEN.value
        ) from exc

    expected_turn = chess.WHITE if request.side == "w" else chess.BLACK
    if board.turn != expected_turn:
        raise HTTPException(status_code=400, detail="side_to_move_mismatch")

    applied_client_move = False
    if request.client_move:
        board, errors = validate_and_apply_move(request.fen, request.client_move)
        if errors:
            raise HTTPException(status_code=400, detail=errors[0].value)
        applied_client_move = True
        flags_after_client = Flags(**compute_game_flags(board))
        if board.is_game_over():
            return MoveResponse(
                applied_client_move=True,
                ai_move=None,
                new_fen=board.fen(),
                flags=flags_after_client,
                errors=[ErrorCode.NO_LEGAL_MOVES],
            )

    legal_moves = [m.uci() for m in board.legal_moves]
    if not legal_moves:
        return MoveResponse(
            applied_client_move=applied_client_move,
            ai_move=None,
            new_fen=board.fen(),
            flags=flags_after_client if request.client_move else Flags(**compute_game_flags(board)),
            errors=[ErrorCode.NO_LEGAL_MOVES],
        )

    ai_move_uci = get_ai_move(board.fen(), legal_moves)
    ai_move = chess.Move.from_uci(ai_move_uci)
    board.push(ai_move)
    return MoveResponse(
        applied_client_move=applied_client_move,
        ai_move=ai_move_uci,
        new_fen=board.fen(),
        flags=Flags(**compute_game_flags(board)),
        errors=[],
    )
