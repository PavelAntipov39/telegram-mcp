# Настройка Render MCP Server

Инструкция по подключению и проверке Render MCP сервера согласно [официальной документации](https://render.com/docs/mcp-server).

## 📋 Шаг 1: Создание API ключа

1. Откройте [Render Dashboard → Account Settings → API Keys](https://dashboard.render.com/settings#api-keys)
2. Нажмите **"Create API Key"**
3. Дайте ключу имя (например, `mcp-server-key`)
4. **Скопируйте ключ** (он показывается только один раз!)

⚠️ **Важно:** Render API ключи имеют широкие права доступа ко всем workspace и сервисам вашего аккаунта.

## 🔧 Шаг 2: Настройка Claude Desktop

Откройте файл конфигурации Claude Desktop:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Добавьте конфигурацию Render MCP сервера:

```json
{
  "mcpServers": {
    "telegram-mcp": {
      "command": "/PATH-TO/uv",
      "args": [
        "--directory",
        "/PATH-TO/telegram-mcp",
        "run",
        "main.py"
      ]
    },
    "render": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.render.com/mcp",
        "--header",
        "Authorization: Bearer ${RENDER_API_KEY}"
      ],
      "env": {
        "RENDER_API_KEY": "<YOUR_API_KEY>"
      }
    }
  }
}
```

**Замените `<YOUR_API_KEY>` на ваш реальный API ключ.**

## 🧪 Шаг 3: Проверка подключения

### Вариант 1: Использование тестового скрипта

1. Установите переменную окружения:
   ```bash
   export RENDER_API_KEY='ваш_api_ключ'
   ```

2. Запустите тестовый скрипт:
   ```bash
   python test_render_mcp.py
   ```
   
   Или передайте ключ напрямую:
   ```bash
   python test_render_mcp.py 'ваш_api_ключ'
   ```

3. Ожидаемый результат:
   ```
   ✅ УСПЕХ!
   ✅ Render MCP сервер доступен и отвечает!
   Status Code: 200
   ```

### Вариант 2: Проверка через Claude Desktop

1. Перезапустите Claude Desktop после изменения конфигурации
2. Попросите Claude:
   - "List my Render workspaces"
   - "Set my Render workspace to [WORKSPACE_NAME]"
   - "List my Render services"

## 📝 Шаг 4: Использование

После успешной настройки вы можете использовать Render MCP через естественный язык:

### Примеры команд:

**Управление сервисами:**
- "Create a new database named user-db with 5 GB storage"
- "List my Render services"
- "What was the busiest traffic day for my service this month?"

**Работа с базами данных:**
- "Query my Render database for daily signup counts for the last 30 days"
- "Using my Render database, tell me which items were the most frequently bought together"

**Анализ метрик:**
- "What did my service's autoscaling behavior look like yesterday?"
- "Pull the most recent error-level logs for my API service"

**Устранение неполадок:**
- "Why isn't my site at example.onrender.com working?"

## 🔍 Доступные инструменты Render MCP

### Workspaces
- List all workspaces you have access to
- Set the current workspace
- Fetch details of the currently selected workspace

### Services
- Create a new web service or static site
- List all services in the current workspace
- Retrieve details about a specific service
- Update all environment variables for a service

### Deploys
- List the deploy history for a service
- Get details about a specific deploy

### Logs
- List logs matching provided filters
- List all values for a given log label

### Metrics
- Fetch performance metrics for services and datastores:
  - CPU / memory usage
  - Instance count
  - Datastore connection counts
  - Web service response counts
  - Response times (требует Professional workspace)
  - Outbound bandwidth usage

### Render Postgres
- Create a new database
- List all databases in the current workspace
- Get details about a specific database
- Run a read-only SQL query against a specific database

### Render Key Value
- List all Key Value instances
- Get details about a specific Key Value instance
- Create a new Key Value instance

## ⚠️ Ограничения

- Render MCP сервер поддерживает создание только:
  - Web services
  - Static sites
  - Render Postgres databases
  - Render Key Value instances
  
- Не поддерживается:
  - Создание free instances
  - Private services, background workers, cron jobs
  - Удаление ресурсов (кроме изменения environment variables)
  - Триггер деплоев
  - Изменение scaling settings

## 🐛 Устранение неполадок

### Ошибка 401: Unauthorized
- Проверьте правильность API ключа
- Убедитесь, что ключ не истек

### Ошибка 403: Forbidden
- Проверьте права доступа API ключа
- Убедитесь, что ключ активен

### Сервер не отвечает
- Проверьте интернет-соединение
- Убедитесь, что URL правильный: `https://mcp.render.com/mcp`
- Проверьте, что npx установлен (для локального запуска)

### Claude Desktop не видит Render MCP
- Перезапустите Claude Desktop
- Проверьте синтаксис JSON в конфигурационном файле
- Убедитесь, что путь к конфигурационному файлу правильный

## 📚 Дополнительные ресурсы

- [Официальная документация Render MCP](https://render.com/docs/mcp-server)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Render API Documentation](https://render.com/docs/api)

