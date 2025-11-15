# Инструкция по отправке изменений в GitHub

## Текущая ситуация

✅ Изменения закоммичены локально
✅ Remote настроен на: `https://github.com/pavelantipov39/telegram-mcp.git`

## Варианты отправки в GitHub

### Вариант 1: Personal Access Token (Рекомендуется)

1. **Создайте Personal Access Token:**
   - Откройте https://github.com/settings/tokens
   - Нажмите "Generate new token" → "Generate new token (classic)"
   - Название: `telegram-mcp-deploy`
   - Срок действия: 90 дней (или по вашему выбору)
   - Права: отметьте `repo` (полный доступ к репозиториям)
   - Нажмите "Generate token"
   - **Скопируйте токен** (он показывается только один раз!)

2. **Используйте токен для push:**
   ```bash
   git push -u origin main
   ```
   Когда запросит:
   - Username: `pavelantipov39`
   - Password: **вставьте токен** (не пароль от GitHub!)

### Вариант 2: GitHub CLI

Если установлен GitHub CLI:
```bash
gh auth login
gh repo create pavelantipov39/telegram-mcp --public --source=. --remote=origin --push
```

### Вариант 3: Настроить SSH ключ

1. Проверьте наличие SSH ключа:
   ```bash
   ls -la ~/.ssh/id_*.pub
   ```

2. Если нет ключа, создайте:
   ```bash
   ssh-keygen -t ed25519 -C "pavelantipov39@gmail.com"
   ```

3. Добавьте ключ в GitHub:
   - Скопируйте публичный ключ: `cat ~/.ssh/id_ed25519.pub`
   - Откройте https://github.com/settings/keys
   - New SSH key → вставьте ключ

4. Измените remote на SSH:
   ```bash
   git remote set-url origin git@github.com:pavelantipov39/telegram-mcp.git
   git push -u origin main
   ```

### Вариант 4: Создать репозиторий вручную

Если репозиторий еще не существует:

1. Откройте https://github.com/new
2. Repository name: `telegram-mcp`
3. Выберите Public или Private
4. **НЕ** добавляйте README, .gitignore или license
5. Нажмите "Create repository"
6. Затем используйте Вариант 1 для push

## После успешного push

После того как изменения окажутся в GitHub, вы сможете:

1. Задеплоить на Render.com:
   - New Web Service → подключите репозиторий `pavelantipov39/telegram-mcp`
   - Environment: Docker
   - Добавьте переменные окружения
   - Получите URL: `https://telegram-mcp-xxxx.onrender.com/sse`

## Текущий статус коммита

Коммит готов к отправке:
```
[main 485ca3f] Add SSE support via mcp-proxy for remote deployment
 6 files changed, 384 insertions(+), 42 deletions(-)
```

Файлы в коммите:
- Dockerfile (обновлен)
- docker-compose.yml (обновлен)
- .dockerignore (новый)
- DEPLOY.md (новый)
- QUICK_DEPLOY.md (новый)
- GET_URL.md (новый)

