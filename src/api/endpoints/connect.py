from __future__ import annotations

import html
import json
import re
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from aiogram import Bot
from fluentogram import TranslatorHub
from dishka.integrations.fastapi import FromDishka, inject
from redis.asyncio import Redis
from src.core.config import AppConfig
from src.services.user import UserService
from src.services.notification import NotificationService

router = APIRouter(prefix="/api/v1", tags=["connect"])

# Ссылки для скачивания приложений по платформам
DOWNLOAD_URLS = {
    "android": "https://play.google.com/store/apps/details?id=com.happproxy",
    "windows": "https://github.com/Happ-proxy/happ-desktop/releases/latest/download/setup-Happ.x64.exe",
    "ios": "https://apps.apple.com/app/happ-proxy-utility-plus/id6746188973",
    "macos": "https://github.com/Happ-proxy/happ-desktop/releases/",
}

# Дефолтная ссылка (Android как самая популярная платформа)
DEFAULT_DOWNLOAD_URL = DOWNLOAD_URLS["android"]


def detect_platform(user_agent: str) -> str:
    """Определяет платформу по User-Agent."""
    ua_lower = user_agent.lower()
    
    # Проверяем в порядке специфичности
    if "iphone" in ua_lower or "ipad" in ua_lower:
        return "ios"
    if "android" in ua_lower:
        return "android"
    if "macintosh" in ua_lower or "mac os" in ua_lower:
        return "macos"
    if "windows" in ua_lower:
        return "windows"
    
    return "unknown"


@router.get("/download")
async def download_app(request: Request) -> RedirectResponse:
    """
    Автоматически определяет ОС пользователя и редиректит на соответствующую ссылку для скачивания.
    """
    user_agent = request.headers.get("user-agent", "")
    platform = detect_platform(user_agent)
    
    download_url = DOWNLOAD_URLS.get(platform, DEFAULT_DOWNLOAD_URL)
    return RedirectResponse(url=download_url, status_code=302)


@router.get("/user-devices/{subscription_url:path}")
@inject
async def get_user_devices_count(
    subscription_url: str,
    request: Request,
    user_service: FromDishka[UserService],
    remnawave_service: FromDishka[Any],  # RemnawaveService - избегаем циклического импорта
):
    """
    Получить количество устройств пользователя по subscription_url.
    Возвращает JSON с количеством устройств.
    """
    from fastapi.responses import JSONResponse
    
    try:
        # Получаем пользователя по subscription_url
        user = await user_service.get_by_subscription_url(subscription_url)
        
        if not user or not user.current_subscription:
            return JSONResponse({"device_count": 0})
        
        # Получаем список устройств из Remnawave
        devices = await remnawave_service.get_devices_user(user=user)
        device_count = len(devices) if devices else 0
        
        return JSONResponse({"device_count": device_count})
    except Exception as e:
        from loguru import logger
        logger.error(f"Error getting device count: {e}")
        return JSONResponse({"device_count": 0})


@router.post("/notify-device-connected/{subscription_url:path}")
@inject
async def notify_device_connected(
    subscription_url: str,
    request: Request,
    user_service: FromDishka[UserService],
    notification_service: FromDishka[NotificationService],
    remnawave_service: FromDishka[Any],  # RemnawaveService - избегаем циклического импорта
    redis_client: FromDishka[Redis],
):
    """
    Отправляет уведомление пользователю и разработчикам в Telegram об успешном подключении устройства.
    Уведомление разработчикам отправляется при добавлении нового устройства.
    """
    from fastapi.responses import JSONResponse
    from src.core.utils.message_payload import MessagePayload
    from src.core.enums import SystemNotificationType
    from src.bot.keyboards import get_user_keyboard
    from loguru import logger
    import json
    
    try:
        # Получаем пользователя по subscription_url
        user = await user_service.get_by_subscription_url(subscription_url)
        
        if not user:
            return JSONResponse({"success": False, "error": "User not found"})
        
        # Отправляем уведомление пользователю об успешном подключении
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-device-connected")
        )
        
        # Получаем список устройств пользователя
        devices = await remnawave_service.get_devices_user(user)
        
        if not devices:
            return JSONResponse({"success": True})
        
        # Ключ для хранения списка известных HWID в Redis
        redis_key = f"known_hwids:{user.telegram_id}"
        
        # Получаем список известных HWID из Redis
        known_hwids_str = await redis_client.get(redis_key)
        known_hwids: set[str] = set(json.loads(known_hwids_str)) if known_hwids_str else set()
        
        # Текущие HWID устройств
        current_hwids = {device.hwid for device in devices}
        
        # Находим новые устройства (которых не было раньше)
        new_hwids = current_hwids - known_hwids
        
        # Сохраняем текущий список HWID в Redis (с TTL 30 дней)
        await redis_client.set(redis_key, json.dumps(list(current_hwids)), ex=30 * 24 * 3600)
        
        # Если есть новые устройства - отправляем уведомление
        if new_hwids:
            # Находим данные нового устройства
            for device in devices:
                if device.hwid in new_hwids:
                    logger.info(f"New device detected for user {user.telegram_id}: {device.hwid}")
                    
                    # Отправляем уведомление разработчикам о добавлении устройства
                    await notification_service.system_notify(
                        ntf_type=SystemNotificationType.USER_HWID,
                        payload=MessagePayload.not_deleted(
                            i18n_key="ntf-event-user-hwid-added",
                            i18n_kwargs={
                                "user_id": str(user.telegram_id),
                                "user_name": user.name,
                                "username": user.username or False,
                                "hwid": device.hwid,
                                "platform": device.platform,
                                "device_model": device.device_model,
                                "os_version": device.os_version,
                                "user_agent": device.user_agent,
                            },
                            reply_markup=get_user_keyboard(user.telegram_id),
                            close_button_style="success",
                        ),
                    )
                    break  # Отправляем уведомление только для одного нового устройства
            
            return JSONResponse({"status": "success", "new_devices": len(new_hwids)})
        
        return JSONResponse({"status": "checked", "new_devices": 0})
    except Exception as e:
        from loguru import logger
        logger.error(f"Error sending device connected notification: {e}")
        return JSONResponse({"status": "error", "error": "Internal server error"}, status_code=500)


@router.get("/connect/{subscription_url:path}")
@inject
async def connect_to_happ(
    subscription_url: str,
    request: Request,
    config: FromDishka[AppConfig],
):
    """
    Страница для подключения к Happ.
    Использует HTML с JavaScript для надежного открытия приложения через happ://add/
    """
    from fastapi import HTTPException
    from fastapi.responses import HTMLResponse
    
    # Проверяем что URL не пустой и имеет корректный формат
    if not subscription_url or not subscription_url.strip():
        raise HTTPException(status_code=400, detail="Subscription URL is empty")
    
    # Убеждаемся что URL начинается с http:// или https://
    if not subscription_url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid subscription URL format")
    
    # Дополнительная валидация: только буквы, цифры, допустимые URL-символы
    if not re.match(r'^https?://[a-zA-Z0-9._\-:/\?&=%#+@]+$', subscription_url):
        raise HTTPException(status_code=400, detail="Invalid subscription URL format")
    
    # Экранируем URL для безопасной вставки в HTML/JS
    safe_happ_url = json.dumps(f"happ://add/{subscription_url}")
    safe_display_url = html.escape(subscription_url)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Подключение</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #0a0e27;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
                color: #e8e8e8;
            }}
            
            .container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 20px;
                text-align: center;
            }}
            
            .loader {{
                width: 60px;
                height: 60px;
                border: 4px solid rgba(0, 168, 232, 0.2);
                border-top: 4px solid #00a8e8;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }}
            
            .text {{
                font-size: 16px;
                color: #a0a0a0;
                line-height: 1.5;
            }}
            
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="loader"></div>
            <p class="text">Добавление подписки в приложение...<br>Страница будет закрыта автоматически</p>
        </div>
        
        <script>
            const happUrl = {safe_happ_url};
            
            // Создаем невидимый iframe для попытки открытия deep link
            const iframe = document.createElement('iframe');
            iframe.style.display = 'none';
            iframe.src = happUrl;
            document.body.appendChild(iframe);
            
            // Также пробуем прямую навигацию
            setTimeout(() => {{
                window.location.href = happUrl;
            }}, 500);
            
            // Автоматически закрываем страницу через 3 секунды
            setTimeout(() => {{
                window.close();
            }}, 3000);
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


@router.get("/subscription/{subscription_url:path}")
@inject
async def subscription_page(
    subscription_url: str,
    request: Request,
    config: FromDishka[AppConfig],
):
    """
    Открыть страницу подписки пользователя.
    Работает точно так же как /connect/ - с отслеживанием новых устройств.
    """
    # Используем ту же логику что и connect_to_happ
    return await connect_to_happ(subscription_url, request, config)
