## WebSocket-relay (комнаты, пинги/понги, лимиты подключений)

Минималистичный ретранслятор сообщений по комнатам на FastAPI WebSocket с:
- комнатами (join/leave, broadcast);
- приложенческим пинг/понг протоколом и таймаутами;
- лимитами подключений: глобальными и на комнату.

### Быстрый старт

1) Установите зависимости:
```bash
pip install -r requirements.txt
```

2) Скопируйте переменные окружения и при необходимости измените значения:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/macOS
```

3) Запуск:
```bash
# Windows PowerShell
scripts/run.ps1

# Linux/macOS
bash scripts/run.sh
```

Сервер поднимется на `http://127.0.0.1:8000`. Точка подключения WebSocket: `ws://127.0.0.1:8000/ws?room=<room>&client_id=<id>`.

### Протокол сообщений

Сообщения — JSON-объекты с полями `type` и `payload`.

- Пользовательские сообщения для широковещательной отправки в комнате:
```json
{"type":"message","payload":{"text":"hello"}}
```

- Пинг (от сервера к клиенту):
```json
{"type":"ping","payload":{"ts": 1690000000}}
```

- Понг (от клиента к серверу):
```json
{"type":"pong","payload":{"ts": 1690000000}}
```

Если понг не получен в течение `PONG_TIMEOUT_SEC`, соединение разрывается.

### Переменные окружения (.env)

- `MAX_CONNECTIONS_TOTAL` — глобальный лимит подключений (по умолчанию 1000)
- `MAX_CONNECTIONS_PER_ROOM` — лимит подключений в одной комнате (по умолчанию 100)
- `PING_INTERVAL_SEC` — интервал отправки пингов сервером (по умолчанию 20)
- `PONG_TIMEOUT_SEC` — таймаут ожидания понга (по умолчанию 30)

### Структура проекта

```
.
├── README.md
├── requirements.txt
├── .env.example
├── scripts/
│   ├── run.ps1
│   └── run.sh
└── src/
    └── app/
        ├── main.py
        ├── config.py
        ├── models/
        │   ├── __init__.py
        │   └── messages.py
        ├── core/
        │   ├── __init__.py
        │   ├── connection_manager.py
        │   └── heartbeat.py
        ├── services/
        │   ├── __init__.py
        │   └── room_service.py
        ├── routes/
        │   ├── __init__.py
        │   └── ws.py
        └── utils/
            ├── __init__.py
            └── time.py
```

### Тестирование

Добавлен файл-заглушка в `tests/`. Запуск (если установлен pytest):
```bash
pytest -q
```

### Пример минимального клиента (JavaScript)

```javascript
const url = `ws://127.0.0.1:8000/ws?room=lobby&client_id=${crypto.randomUUID()}`;
const ws = new WebSocket(url);

ws.onmessage = (ev) => {
  const data = JSON.parse(ev.data);
  if (data.type === 'ping') {
    ws.send(JSON.stringify({ type: 'pong', payload: { ts: data.payload.ts } }));
  } else {
    console.log('message:', data);
  }
};

ws.onopen = () => {
  ws.send(JSON.stringify({ type: 'message', payload: { text: 'hello room' } }));
};
```

### Лицензия

MIT


