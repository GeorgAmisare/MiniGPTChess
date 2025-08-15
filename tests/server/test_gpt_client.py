"""Тесты для клиента GPT."""

from types import SimpleNamespace

import server.app.gpt_client as gpt_client


def test_invalid_response_falls_back(monkeypatch, caplog):
    """Проверить, что при превышении попыток используется резервный ход."""

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
    with caplog.at_level("INFO"):
        move = gpt_client.get_ai_move(
            "8/8/8/8/8/8/8/8 w - - 0 1", legal_moves
        )

    assert move in legal_moves
    assert "Превышен лимит повторов" in caplog.text


def test_retries_on_exception(monkeypatch):
    """Проверить, что при ошибке запроса выполняется повтор."""

    class DummyResponse:
        def __init__(self, text: str):
            self.output = [
                SimpleNamespace(
                    content=[SimpleNamespace(text=text)],
                )
            ]

    class DummyClient:
        def __init__(self):
            self.calls = 0
            self.responses = SimpleNamespace(create=self._create)

        def _create(self, **_):
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("fail")
            return DummyResponse("a2a3")

    dummy = DummyClient()
    monkeypatch.setattr(gpt_client, "_client", dummy)
    monkeypatch.setattr(gpt_client, "_MAX_RETRIES", 2)

    legal_moves = ["a2a3", "b2b3"]
    move = gpt_client.get_ai_move("8/8/8/8/8/8/8/8 w - - 0 1", legal_moves)

    assert move == "a2a3"
    assert dummy.calls == 2
