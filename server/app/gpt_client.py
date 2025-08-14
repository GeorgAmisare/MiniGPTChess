"""Клиент для обращения к OpenAI и получения хода ИИ."""

import os
import random
import logging
from typing import List

from openai import OpenAI

logger = logging.getLogger(__name__)

_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
_MODEL = "gpt-4o-mini"


def get_ai_move(fen: str, legal_moves: List[str]) -> str:
    """Вернуть ход ИИ для заданной позиции.

    Parameters
    ----------
    fen: str
        Состояние доски в нотации FEN.
    legal_moves: List[str]
        Список легальных ходов в формате UCI.

    Функция обращается к OpenAI Responses API и проверяет, что полученный
    ход присутствует в ``legal_moves``. Выполняется до трёх попыток. При
    ошибке API или отсутствии корректного ответа выбирается случайный ход.
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
            logger.error("Ошибка OpenAI API: %s", exc)
            break
        if ai_move in legal_moves:
            return ai_move
    return random.choice(legal_moves)
