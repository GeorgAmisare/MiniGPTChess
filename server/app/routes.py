"""Маршруты API для сервера MiniGPTChess."""

from fastapi import APIRouter
import chess

from .chess_logic import compute_game_flags, validate_and_apply_move
from .models import ErrorCode, Flags, MoveRequest, MoveResponse
from .gpt_client import get_ai_move

router = APIRouter()


@router.post("/new")
async def new_game() -> dict[str, str]:
    """Создать новую игру и вернуть стартовый FEN."""
    return {"fen": chess.STARTING_FEN, "side": "w"}


@router.post("/move", response_model=MoveResponse)
async def move(request: MoveRequest) -> MoveResponse:
    """Обработать ход клиента и вернуть ответ ИИ."""
    try:
        board = chess.Board(request.fen)
    except ValueError:
        empty_flags = Flags(**compute_game_flags(chess.Board()))
        return MoveResponse(
            status="error",
            applied_client_move=False,
            ai_move=None,
            new_fen=request.fen,
            flags=empty_flags,
            errors=[ErrorCode.INVALID_FEN],
        )

    expected_turn = chess.WHITE if request.side == "w" else chess.BLACK
    if board.turn != expected_turn:
        return MoveResponse(
            status="error",
            applied_client_move=False,
            ai_move=None,
            new_fen=board.fen(),
            flags=Flags(**compute_game_flags(board)),
            errors=[ErrorCode.SIDE_TO_MOVE_MISMATCH],
        )

    applied_client_move = False
    if request.client_move:
        new_board, errors = validate_and_apply_move(
            request.fen, request.client_move
        )
        if errors:
            return MoveResponse(
                status="error",
                applied_client_move=False,
                ai_move=None,
                new_fen=board.fen(),
                flags=Flags(**compute_game_flags(board)),
                errors=errors,
            )
        board = new_board
        applied_client_move = True
        if board.is_game_over():
            return MoveResponse(
                status="error",
                applied_client_move=True,
                ai_move=None,
                new_fen=board.fen(),
                flags=Flags(**compute_game_flags(board)),
                errors=[ErrorCode.NO_LEGAL_MOVES],
            )

    flags_before_ai = Flags(**compute_game_flags(board))
    legal_moves = [m.uci() for m in board.legal_moves]
    if not legal_moves:
        return MoveResponse(
            status="error",
            applied_client_move=applied_client_move,
            ai_move=None,
            new_fen=board.fen(),
            flags=flags_before_ai,
            errors=[ErrorCode.NO_LEGAL_MOVES],
        )

    ai_move_uci = get_ai_move(board.fen(), legal_moves)
    status = "ok"
    errors = []
    if ai_move_uci not in legal_moves:
        ai_move_uci = legal_moves[0]
        status = "error"
        errors = [ErrorCode.GPT_INVALID_MOVE]
    ai_move = chess.Move.from_uci(ai_move_uci)
    board.push(ai_move)
    return MoveResponse(
        status=status,
        applied_client_move=applied_client_move,
        ai_move=ai_move_uci,
        new_fen=board.fen(),
        flags=Flags(**compute_game_flags(board)),
        errors=errors,
    )
