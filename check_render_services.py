#!/usr/bin/env python3
"""
Скрипт для проверки задеплоенных сервисов на Render
"""
import os
import sys
import requests
from typing import Optional, List, Dict

RENDER_API_BASE = "https://api.render.com/v1"


def get_render_services(api_key: str) -> Dict:
    """
    Получает список всех сервисов на Render
    
    Args:
        api_key: Render API ключ
    
    Returns:
        dict с информацией о сервисах
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    try:
        # Получаем список сервисов
        response = requests.get(
            f"{RENDER_API_BASE}/services",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            services = response.json()
            return {
                "success": True,
                "services": services,
                "count": len(services) if isinstance(services, list) else 0
            }
        elif response.status_code == 401:
            return {
                "success": False,
                "error": "Неверный API ключ"
            }
        else:
            return {
                "success": False,
                "error": f"Ошибка API: {response.status_code}",
                "response": response.text[:200]
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Ошибка подключения: {str(e)}"
        }


def find_telegram_mcp_service(services: List[Dict]) -> Optional[Dict]:
    """
    Ищет Telegram MCP сервис среди списка сервисов
    
    Args:
        services: Список сервисов
    
    Returns:
        Информация о найденном сервисе или None
    """
    if not isinstance(services, list):
        return None
    
    # Ищем сервисы с "telegram" или "mcp" в названии
    for service in services:
        name = service.get("service", {}).get("name", "").lower()
        if "telegram" in name or "mcp" in name:
            return service.get("service", {})
    
    return None


def check_service_health(api_key: str, service_id: str) -> Dict:
    """
    Проверяет статус и здоровье сервиса
    
    Args:
        api_key: Render API ключ
        service_id: ID сервиса
    
    Returns:
        dict с информацией о статусе
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(
            f"{RENDER_API_BASE}/services/{service_id}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "service": response.json()
            }
        else:
            return {
                "success": False,
                "error": f"Ошибка: {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def test_sse_endpoint(url: str) -> Dict:
    """
    Проверяет доступность SSE endpoint
    
    Args:
        url: URL SSE endpoint (должен заканчиваться на /sse)
    
    Returns:
        dict с результатами проверки
    """
    if not url.endswith("/sse"):
        url = f"{url.rstrip('/')}/sse"
    
    try:
        # Увеличиваем таймаут для "пробуждения" сервиса
        response = requests.get(url, timeout=30, stream=True)
        
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "url": url,
            "content_type": response.headers.get("Content-Type", ""),
            "is_sse": "text/event-stream" in response.headers.get("Content-Type", "")
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Таймаут подключения (сервис может быть в режиме сна на бесплатном тарифе)"
        }
    except requests.exceptions.ConnectionError as e:
        return {
            "success": False,
            "error": f"Ошибка подключения: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Ошибка: {str(e)}"
        }


def main():
    """Главная функция"""
    api_key = os.getenv("RENDER_API_KEY")
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    if not api_key:
        print("❌ Ошибка: API ключ не найден")
        print("Использование: python check_render_services.py [API_KEY]")
        print("Или установите переменную окружения: export RENDER_API_KEY='ваш_ключ'")
        return 1
    
    print("🔍 Проверка сервисов на Render...\n")
    
    # Получаем список сервисов
    result = get_render_services(api_key)
    
    if not result.get("success"):
        print(f"❌ Ошибка: {result.get('error')}")
        return 1
    
    services = result.get("services", [])
    print(f"📊 Найдено сервисов: {len(services)}\n")
    
    # Ищем Telegram MCP сервис
    telegram_service = find_telegram_mcp_service(services)
    
    if telegram_service:
        print("✅ Найден Telegram MCP сервис!")
        print(f"   Название: {telegram_service.get('name')}")
        print(f"   ID: {telegram_service.get('id')}")
        
        # Получаем детальную информацию о сервисе
        service_id = telegram_service.get('id')
        if service_id:
            health_info = check_service_health(api_key, service_id)
            if health_info.get("success"):
                service_details = health_info.get("service", {})
                service_url = service_details.get("serviceDetails", {}).get("url")
                status = service_details.get("serviceDetails", {}).get("healthCheckStatus", "unknown")
                print(f"   Статус: {status}")
                
                if service_url:
                    print(f"   URL: {service_url}")
                    sse_url = f"{service_url.rstrip('/')}/sse"
                    print(f"\n{'='*60}")
                    print(f"🔗 SSE ENDPOINT ДЛЯ CHATGPT:")
                    print(f"   {sse_url}")
                    print(f"{'='*60}\n")
                    
                    # Проверяем доступность
                    print("🧪 Проверка SSE endpoint...")
                    print("   (На бесплатном тарифе Render сервис может засыпать)")
                    print("   (Первое подключение может занять до 30 секунд для пробуждения)\n")
                    
                    sse_test = test_sse_endpoint(service_url)
                    
                    if sse_test.get("success") and sse_test.get("is_sse"):
                        print("✅ SSE endpoint работает!")
                        print(f"   Status: {sse_test.get('status_code')}")
                        print(f"   Content-Type: {sse_test.get('content_type')}")
                    elif sse_test.get("success"):
                        print("⚠️ Endpoint доступен, но не возвращает SSE")
                        print(f"   Status: {sse_test.get('status_code')}")
                        print(f"   Content-Type: {sse_test.get('content_type')}")
                    else:
                        print(f"⚠️ Endpoint не отвечает: {sse_test.get('error')}")
                        print("\n💡 Возможные причины:")
                        print("   - Сервис в режиме сна (бесплатный тариф)")
                        print("   - Сервис еще деплоится")
                        print("   - Проблема с конфигурацией")
                        print("\n💡 Решения:")
                        print("   - Попробуйте подключиться через ChatGPT (он разбудит сервис)")
                        print("   - Проверьте логи в Render Dashboard")
                        print("   - Убедитесь, что все переменные окружения установлены")
                else:
                    print("⚠️ URL сервиса не найден")
            else:
                print(f"⚠️ Не удалось получить детали: {health_info.get('error')}")
    else:
        print("❌ Telegram MCP сервис не найден на Render")
        print("\n💡 Для деплоя:")
        print("   1. Откройте https://dashboard.render.com")
        print("   2. New + → Web Service")
        print("   3. Подключите GitHub репозиторий")
        print("   4. Environment: Docker")
        print("   5. Добавьте переменные окружения:")
        print("      - TELEGRAM_API_ID")
        print("      - TELEGRAM_API_HASH")
        print("      - TELEGRAM_SESSION_STRING")
        print("      - PORT=8080")
        print("   6. После деплоя URL будет: https://<service-name>.onrender.com")
        print("   7. SSE endpoint: https://<service-name>.onrender.com/sse")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

