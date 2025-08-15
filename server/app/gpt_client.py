"""Клиент для обращения к OpenAI и получения хода ИИ."""

import os
import random
import logging
from typing import List, Optional

from openai import OpenAI

logger = logging.getLogger(__name__)

_MODEL = "gpt-4o-mini"
_api_key = os.getenv("OPENAI_API_KEY")
_client: Optional[OpenAI] = (
    OpenAI(api_key=_api_key) if _api_key else None
)
_MAX_RETRIES = 2  # ограничение количества повторных запросов к GPT


def get_ai_move(fen: str, legal_moves: List[str]) -> str:
    """Вернуть ход ИИ для заданной позиции.

    Parameters
    ----------
    fen: str
        Состояние доски в нотации FEN.
    legal_moves: List[str]
        Список легальных ходов в формате UCI.

    Функция обращается к OpenAI Responses API и проверяет, что полученный
    ход присутствует в ``legal_moves``. Выполняется не более двух попыток.
    При ошибке API или отсутствии корректного ответа выбирается случайный
    ход.
    """
    if not fen:
        raise ValueError("FEN must be provided")
    if not legal_moves:
        raise ValueError("legal_moves must not be empty")

    prompt = (
        "You are a chess engine. Evaluate the given position and choose the"
        " best move from the list of legal moves. Return only that move in"
        " UCI format.\n"
        f"FEN: {fen}\n"
        f"Legal moves: {', '.join(legal_moves)}"
    )

    if _client is None:
        move = random.choice(legal_moves)
        logger.info(
            "Клиент OpenAI не настроен, выбран случайный ход: %s",
            move,
        )
        return move

    for _ in range(_MAX_RETRIES):
        try:
            response = _client.responses.create(
                model=_MODEL,
                input=prompt,
                temperature=0,
                top_p=1,
                max_tokens=3,
            )
            ai_move = response.output[0].content[0].text.strip()
        except Exception as exc:  # noqa: BLE001
            logger.error("Ошибка OpenAI API: %s", exc)
            continue
        logger.info("Ответ GPT: %s", ai_move)
        if ai_move in legal_moves:
            return ai_move
    move = random.choice(legal_moves)
    logger.info("Превышен лимит повторов, выбран случайный ход: %s", move)
    return move
