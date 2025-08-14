"""API routes for MiniGPTChess server."""

from fastapi import APIRouter, HTTPException
import chess

from .models import Flags, MoveRequest, MoveResponse
from .ai import choose_ai_move

router = APIRouter()


def _build_flags(board: chess.Board) -> Flags:
    """Create status flags for a given board."""
    return Flags(
        check=board.is_check(),
        checkmate=board.is_checkmate(),
        stalemate=board.is_stalemate(),
    )


@router.post("/move", response_model=MoveResponse)
async def move(request: MoveRequest) -> MoveResponse:
    """Process a move from the client and respond with the AI move."""
    try:
        board = chess.Board(request.fen)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid FEN") from exc

    expected_turn = chess.WHITE if request.side == "w" else chess.BLACK
    if board.turn != expected_turn:
        raise HTTPException(status_code=400, detail="Side to move mismatch")

    applied_client_move = False
    if request.client_move:
        try:
            client_move = chess.Move.from_uci(request.client_move)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="Invalid move format") from exc
        if client_move not in board.legal_moves:
            raise HTTPException(status_code=400, detail="Illegal move")
        board.push(client_move)
        applied_client_move = True
        if board.is_game_over():
            return MoveResponse(
                applied_client_move=True,
                ai_move=None,
                new_fen=board.fen(),
                flags=_build_flags(board),
                errors=[],
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
