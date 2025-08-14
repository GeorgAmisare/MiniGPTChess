import os
import random
import logging
from typing import List

from openai import OpenAI

logger = logging.getLogger(__name__)

_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
_MODEL = "gpt-4o-mini"


def get_ai_move(fen: str, legal_moves: List[str]) -> str:
    """Return an AI move for the given position.

    Parameters
    ----------
    fen: str
        Board state in Forsyth–Edwards Notation.
    legal_moves: List[str]
        List of legal moves in UCI format.

    The function queries the OpenAI Responses API, checking that the
    returned move is in ``legal_moves``. Up to two retries are
    performed. If the API call fails or a valid move is not returned,
    a random legal move is selected.
    """
    if not fen:
        raise ValueError("FEN must be provided")
    if not legal_moves:
        raise ValueError("legal_moves must not be empty")

    prompt = (
        "You are a chess engine. Given the FEN and a list of legal moves, "
        "choose one move from the list and return only that move in UCI "
        "format.\n"
        f"FEN: {fen}\n"
        f"Legal moves: {', '.join(legal_moves)}"
    )

    for _ in range(3):
        try:
            response = _client.responses.create(model=_MODEL, input=prompt)
            ai_move = response.output[0].content[0].text.strip()
        except Exception as exc:  # noqa: BLE001
            logger.error("OpenAI API error: %s", exc)
            break
        if ai_move in legal_moves:
            return ai_move
    return random.choice(legal_moves)
