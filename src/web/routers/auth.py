"""Authentication API routes."""

from __future__ import annotations

import json

from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger

from aiogram.types import User as AiogramUser

from src.infrastructure.database import UnitOfWork
from src.infrastructure.database.models.sql.web_credential import WebCredential
from src.services.settings import SettingsService
from src.services.user import UserService
from src.web.auth import (
    create_access_token,
    hash_password,
    validate_init_data,
    verify_password,
)
from src.web.dependencies import get_bot_token, get_secret
from src.web.schemas import LoginRequest, PasswordLoginRequest, RegisterRequest

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/tg")
async def auth_telegram(request: Request):
    """Authenticate via Telegram Mini App initData. Auto-registers new users."""
    body = await request.json()
    init_data = body.get("initData", "")
    bot_token = get_bot_token(request)

    parsed = validate_init_data(init_data, bot_token)
    if parsed is None:
        raise HTTPException(status_code=401, detail="Invalid initData")

    user_json = parsed.get("user")
    if not user_json:
        raise HTTPException(status_code=401, detail="No user in initData")

    try:
        user_obj = json.loads(user_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=401, detail="Invalid user JSON")

    telegram_id = user_obj.get("id")
    if not telegram_id:
        raise HTTPException(status_code=401, detail="No user id")

    # Auto-register user if they've never started the bot
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        existing = await user_service.get(telegram_id=telegram_id)
        if existing is None:
            try:
                settings_service: SettingsService = await req_container.get(SettingsService)
                settings = await settings_service.get()
                aiogram_user = AiogramUser(
                    id=telegram_id,
                    is_bot=False,
                    first_name=user_obj.get("first_name") or "User",
                    last_name=user_obj.get("last_name"),
                    username=user_obj.get("username"),
                    language_code=user_obj.get("language_code"),
                )
                await user_service.create(aiogram_user, settings=settings)
                logger.info(f"Auto-registered user {telegram_id} via Mini App initData")
            except Exception as exc:
                logger.warning(f"Auto-register failed for user {telegram_id}: {exc}")

    token = create_access_token(
        {"telegram_id": telegram_id, "source": "miniapp"},
        get_secret(request),
    )
    response = JSONResponse({"ok": True, "telegram_id": telegram_id})
    response.set_cookie("access_token", token, httponly=True, samesite="none", secure=True, max_age=86400)
    return response


@router.post("/check")
async def auth_check_telegram_id(request: Request, body: LoginRequest):
    """Step 1 of web login: check if telegram_id has web credentials."""
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        user_service: UserService = await req_container.get(UserService)

        user = await user_service.get(telegram_id=body.telegram_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь с таким Telegram ID не найден")

        cred = await uow.repository.web_credentials.get_by_telegram_id(body.telegram_id)
        return JSONResponse({
            "has_credentials": cred is not None,
            "name": user.name,
            "web_username": cred.web_username if cred else None,
        })


@router.post("/register")
async def auth_register(request: Request, body: RegisterRequest):
    """Register web credentials for a telegram user."""
    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="Пароль должен быть не менее 6 символов")
    if len(body.web_username) < 3:
        raise HTTPException(status_code=400, detail="Логин должен быть не менее 3 символов")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        user_service: UserService = await req_container.get(UserService)

        user = await user_service.get(telegram_id=body.telegram_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь с таким Telegram ID не найден")

        existing = await uow.repository.web_credentials.get_by_telegram_id(body.telegram_id)
        if existing:
            raise HTTPException(status_code=409, detail="Учётные данные уже существуют")

        username_taken = await uow.repository.web_credentials.get_by_username(body.web_username)
        if username_taken:
            raise HTTPException(status_code=409, detail="Этот логин уже занят")

        try:
            pw_hash = hash_password(body.password)
        except Exception as exc:
            logger.error(f"Password hashing failed: {exc}")
            raise HTTPException(status_code=500, detail="Ошибка при создании учётных данных")

        credential = WebCredential(
            telegram_id=body.telegram_id,
            web_username=body.web_username,
            password_hash=pw_hash,
        )
        try:
            await uow.repository.web_credentials.create(credential)
            await uow.commit()
        except Exception as exc:
            logger.error(f"Failed to save web credentials: {exc}")
            raise HTTPException(status_code=500, detail="Ошибка при сохранении учётных данных")

    token = create_access_token(
        {"telegram_id": body.telegram_id, "source": "web"},
        get_secret(request),
    )
    response = JSONResponse({"ok": True})
    response.set_cookie("access_token", token, httponly=True, samesite="lax", secure=True, max_age=86400)
    return response


@router.post("/login")
async def auth_login(request: Request, body: PasswordLoginRequest):
    """Login with username + password."""
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        uow: UnitOfWork = await req_container.get(UnitOfWork)

        cred = await uow.repository.web_credentials.get_by_username(body.web_username)
        if cred is None:
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")

        if not verify_password(body.password, cred.password_hash):
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token = create_access_token(
        {"telegram_id": cred.telegram_id, "source": "web"},
        get_secret(request),
    )
    response = JSONResponse({"ok": True})
    response.set_cookie("access_token", token, httponly=True, samesite="lax", secure=True, max_age=86400)
    return response


@router.post("/logout")
async def auth_logout():
    response = JSONResponse({"ok": True})
    response.delete_cookie("access_token")
    return response
