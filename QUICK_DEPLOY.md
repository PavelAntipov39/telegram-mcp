# Быстрый деплой для получения публичного URL

## 🚀 Render.com (5 минут)

1. **Зайдите на [render.com](https://render.com)** и войдите через GitHub

2. **Создайте Web Service:**
   - Нажмите "New +" → "Web Service"
   - Подключите репозиторий `chigwell/telegram-mcp`
   - Имя сервиса: `telegram-mcp` (или любое другое)

3. **Настройки:**
   - **Environment:** Docker
   - **Region:** Singapore (или ближайший)
   - **Branch:** main
   - **Auto-Deploy:** Yes

4. **Environment Variables** (в разделе "Environment"):
   ```
   TELEGRAM_API_ID=<ваш_api_id>
   TELEGRAM_API_HASH=<ваш_api_hash>
   TELEGRAM_SESSION_STRING=<ваш_session_string>
   PORT=8080
   ```

5. **Нажмите "Create Web Service"**

6. **После деплоя (2-3 минуты):**
   - Render покажет URL вида: `https://telegram-mcp-xxxx.onrender.com`
   - **Ваш SSE endpoint:** `https://telegram-mcp-xxxx.onrender.com/sse`

## 🔗 Использование в ChatGPT

URL для ChatGPT Connectors:
```
https://telegram-mcp-xxxx.onrender.com/sse
```

Замените `xxxx` на реальный ID вашего сервиса из Render.

## ✅ Проверка

```bash
curl -I https://telegram-mcp-xxxx.onrender.com/sse
```

Должен вернуть:
```
HTTP/1.1 200 OK
Content-Type: text/event-stream
```

