"""Маршруты API для сервера MiniGPTChess."""

from fastapi import APIRouter, HTTPException
import chess

from .models import ErrorCode, Flags, MoveRequest, MoveResponse
from .ai import choose_ai_move

router = APIRouter()


def _build_flags(board: chess.Board) -> Flags:
    """Сформировать флаги состояния для указанной доски."""
    return Flags(
        check=board.is_check(),
        checkmate=board.is_checkmate(),
        stalemate=board.is_stalemate(),
        insufficient_material=board.is_insufficient_material(),
        seventyfive_moves=board.is_seventyfive_moves(),
        fivefold_repetition=board.is_fivefold_repetition(),
    )


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
        try:
            client_move = chess.Move.from_uci(request.client_move)
        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail=ErrorCode.ILLEGAL_CLIENT_MOVE.value,
            ) from exc
        if client_move not in board.legal_moves:
            raise HTTPException(
                status_code=400, detail=ErrorCode.ILLEGAL_CLIENT_MOVE.value
            )
        board.push(client_move)
        applied_client_move = True
        if board.is_game_over():
            return MoveResponse(
                applied_client_move=True,
                ai_move=None,
                new_fen=board.fen(),
                flags=_build_flags(board),
                errors=[ErrorCode.NO_LEGAL_MOVES],
            )

    if not list(board.legal_moves):
        return MoveResponse(
            applied_client_move=applied_client_move,
            ai_move=None,
            new_fen=board.fen(),
            flags=_build_flags(board),
            errors=[ErrorCode.NO_LEGAL_MOVES],
        )

    ai_move = choose_ai_move(board)
    board.push(ai_move)
    return MoveResponse(
        applied_client_move=applied_client_move,
        ai_move=ai_move.uci(),
        new_fen=board.fen(),
        flags=_build_flags(board),
        errors=[],
    )
