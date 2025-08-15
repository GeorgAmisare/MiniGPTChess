"""Тесты для клиента GPT."""

from types import SimpleNamespace

import server.app.gpt_client as gpt_client


def test_invalid_response_falls_back(monkeypatch):
    """Проверить, что возвращается ход из списка легальных."""

    class DummyResponse:
        def __init__(self, text: str):
            self.output = [
                SimpleNamespace(
                    content=[SimpleNamespace(text=text)],
                )
            ]

    class DummyClient:
        def __init__(self):
            self.responses = SimpleNamespace(
                create=lambda **_: DummyResponse("h7h5"),
            )

    monkeypatch.setattr(gpt_client, "_client", DummyClient())
    monkeypatch.setattr(gpt_client, "_MAX_RETRIES", 1)
    monkeypatch.setattr(gpt_client.random, "choice", lambda seq: seq[0])

    legal_moves = ["a2a3", "b2b3"]
    move = gpt_client.get_ai_move("8/8/8/8/8/8/8/8 w - - 0 1", legal_moves)

    assert move in legal_moves
