# MiniGPTChess

Минимальная шахматная песочница, где ходы за ИИ выбирает модель GPT. Проект демонстрирует взаимодействие клиента на PyGame и сервера на FastAPI, использующего `python-chess` для проверки правил.

## Возможности

- Отрисовка доски с помощью PyGame.
- Stateless сервер: клиент передает FEN и сторону хода в каждом запросе.
- Проверка ходов и генерация ответного хода на сервере.
- Подключение к OpenAI Responses API для выбора хода (переменная окружения `OPENAI_API_KEY`). При недоступности API используется случайный легальный ход.
- Валидация ходов через `validate_and_apply_move` и вычисление флагов состояния `compute_game_flags`.
- Клиент позволяет выбирать клетки мышью, отправлять ход на сервер и получать ответ ИИ.

## Структура

```
client/        # PyGame интерфейс
server/app/    # FastAPI сервер и логика игры
tests/         # тесты утилит
```

## Установка

```bash
pip install -r requirements-server.txt
pip install -r requirements-client.txt
```

## Переменные окружения

Создайте файл `.env` на основе `.env.example` и укажите ключ:

```bash
cp .env.example .env
# заполните OPENAI_API_KEY=<ваш ключ>
```

## Запуск

### Сервер

```bash
uvicorn server.app:app --reload --env-file .env
```

#### Эндпоинты

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

При ошибках сервер возвращает код 200 и JSON с `status: "error"` и
заполненным списком `errors`.

### Коды ошибок

- `illegal_client_move` — клиент отправил некорректный или запрещённый ход;
- `no_legal_moves` — отсутствуют легальные ходы;
- `invalid_fen` — некорректная строка FEN;
- `side_to_move_mismatch` — указанная сторона не совпадает со стороной хода в FEN;
- `gpt_invalid_move` — модель GPT вернула недопустимый ход;
- `server_error` — внутренняя ошибка сервера.

### Ограничения

- Строка FEN в запросе ограничена **100** символами.
- Поле `client_move` принимает строки длиной не более **8** символов.
- При обращении к GPT выполняется не более **двух** повторных попыток; если
  корректный ход получить не удалось, выбирается случайный легальный ход.

### Клиент

```bash
python client/main.py
```

Клиент отображает шахматную доску в стартовой позиции и взаимодействует с сервером для обмена ходами.

## Тестирование

```bash
pytest
```
