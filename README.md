# MiniGPTChess

Минимальная шахматная песочница, где ходы за ИИ выбирает модель GPT. Проект демонстрирует взаимодействие клиента на PyGame и сервера на FastAPI, использующего `python-chess` для проверки правил.

## Возможности

- Отрисовка доски с помощью PyGame.
- Stateless сервер: клиент передает FEN и сторону хода в каждом запросе.
- Проверка ходов и генерация ответного хода на сервере.
- Подключение к OpenAI Responses API для выбора хода (переменная окружения `OPENAI_API_KEY`). При недоступности API используется случайный легальный ход.

## Структура

```
client/        # PyGame интерфейс
server/app/    # FastAPI сервер и логика игры
tests/         # тесты утилит
```

## Установка зависимостей

```bash
pip install fastapi uvicorn python-chess pygame httpx openai pydantic
```

## Запуск сервера

```bash
export OPENAI_API_KEY=<ваш ключ>
uvicorn server.app:app --reload
```

### Эндпоинты

- `GET /health` — проверка работоспособности.
- `POST /move` — применяет ход игрока и возвращает ход ИИ.

Пример запроса:

```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "side": "w",
  "client_move": "e2e4"
}
```

Пример ответа:

```json
{
  "status": "ok",
  "applied_client_move": true,
  "ai_move": "c7c5",
  "new_fen": "...",
  "flags": {
    "check": false,
    "checkmate": false,
    "stalemate": false,
    "insufficient_material": false,
    "seventyfive_moves": false,
    "fivefold_repetition": false
  },
  "errors": []
}
```

### Коды ошибок

- `illegal_client_move` — клиент отправил некорректный или запрещённый ход;
- `no_legal_moves` — отсутствуют легальные ходы;
- `invalid_fen` — некорректная строка FEN;
- `gpt_invalid_move` — модель GPT вернула недопустимый ход;
- `server_error` — внутренняя ошибка сервера.

## Запуск клиента

```bash
python client/main.py
```

Клиент отображает шахматную доску в стартовой позиции и может быть расширен для взаимодействия с сервером.

## Тестирование

```bash
pytest
```
