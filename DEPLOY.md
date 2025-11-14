# Деплой Telegram MCP Server на PaaS (SSE для ChatGPT)

Этот документ описывает процесс деплоя Telegram MCP сервера с поддержкой SSE (Server-Sent Events) для использования в ChatGPT Connectors.

## 📋 Требования

- GitHub репозиторий с кодом
- Telegram API credentials:
  - `TELEGRAM_API_ID`
  - `TELEGRAM_API_HASH`
  - `TELEGRAM_SESSION_STRING`

## 🐳 Docker конфигурация

### Dockerfile
Использует `python:3.13-slim`, устанавливает `uv` и `mcp-proxy`, запускает сервер через SSE прокси.

### docker-compose.yml
Для локального тестирования:
```bash
docker compose up --build
```
SSE endpoint будет доступен на `http://localhost:8787/sse`

## 🚀 Деплой на PaaS

### Вариант 1: Render.com (Рекомендуется)

1. **Создайте новый Web Service:**
   - Перейдите на [render.com](https://render.com)
   - Нажмите "New +" → "Web Service"
   - Подключите ваш GitHub репозиторий

2. **Настройки Build:**
   - **Environment:** Docker
   - **Dockerfile Path:** `Dockerfile` (по умолчанию)
   - **Build Command:** (не требуется, используется Dockerfile)

3. **Настройки Start:**
   - **Start Command:** (не требуется, используется ENTRYPOINT из Dockerfile)

4. **Environment Variables:**
   Добавьте в секцию "Environment Variables":
   ```
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   TELEGRAM_SESSION_STRING=your_session_string
   PORT=8080
   ```

5. **После деплоя:**
   - Render автоматически назначит публичный URL
   - SSE endpoint: `https://<your-service-name>.onrender.com/sse`

### Вариант 2: Railway.app

1. **Создайте новый проект:**
   - Перейдите на [railway.app](https://railway.app)
   - Нажмите "New Project" → "Deploy from GitHub repo"
   - Выберите репозиторий

2. **Настройки:**
   - Railway автоматически определит Dockerfile
   - Добавьте переменные окружения в разделе "Variables":
     ```
     TELEGRAM_API_ID=your_api_id
     TELEGRAM_API_HASH=your_api_hash
     TELEGRAM_SESSION_STRING=your_session_string
     PORT=8080
     ```

3. **После деплоя:**
   - Railway назначит публичный URL
   - SSE endpoint: `https://<your-service-name>.railway.app/sse`

### Вариант 3: Northflank

1. **Создайте новый сервис:**
   - Перейдите на [northflank.com](https://northflank.com)
   - Создайте проект → "Add Service" → "Docker"
   - Подключите GitHub репозиторий

2. **Настройки:**
   - **Dockerfile:** `Dockerfile`
   - Добавьте переменные окружения в "Environment Variables"

3. **После деплоя:**
   - SSE endpoint: `https://<your-service-name>.northflank.app/sse`

## ✅ Проверка деплоя

После успешного деплоя проверьте SSE endpoint:

```bash
curl -I https://<your-host>/sse
```

Ожидаемый ответ:
```
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
```

## 🔗 Настройка ChatGPT Connectors

1. Откройте ChatGPT → Settings → Connectors
2. Нажмите "Create" → "MCP Server"
3. Заполните форму:
   - **Transport Type:** SSE (Server-Sent Events)
   - **URL:** `https://<your-host>/sse`
   - **Authentication:** None (или настройте при необходимости)
4. Сохраните и протестируйте подключение

## 📝 Переменные окружения

| Переменная | Описание | Обязательная |
|-----------|----------|--------------|
| `TELEGRAM_API_ID` | Telegram API ID из [my.telegram.org/apps](https://my.telegram.org/apps) | Да |
| `TELEGRAM_API_HASH` | Telegram API Hash | Да |
| `TELEGRAM_SESSION_STRING` | Строка сессии Telegram (получена через `session_string_generator.py`) | Да |
| `PORT` | Порт для SSE сервера (по умолчанию 8080) | Нет |

## 🔒 Безопасность

- **Никогда не коммитьте** `.env` файл в Git
- Используйте секреты PaaS для хранения credentials
- Рекомендуется настроить аутентификацию для SSE endpoint в production

## 🐛 Troubleshooting

### Сервер не запускается
- Проверьте, что все переменные окружения установлены
- Проверьте логи в панели PaaS
- Убедитесь, что `TELEGRAM_SESSION_STRING` валиден

### SSE endpoint не отвечает
- Проверьте, что порт правильно проброшен
- Убедитесь, что `mcp-proxy` установлен и доступен в PATH
- Проверьте логи на наличие ошибок запуска

### ChatGPT не подключается
- Убедитесь, что URL правильный и доступен публично
- Проверьте CORS настройки (`--allow-origin "*"`)
- Проверьте формат URL (должен заканчиваться на `/sse`)

