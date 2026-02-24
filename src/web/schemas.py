"""Pydantic request/response models for web API."""

from __future__ import annotations

from pydantic import BaseModel


# ── Auth ──────────────────────────────────────────────────────────


class LoginRequest(BaseModel):
    telegram_id: int


class RegisterRequest(BaseModel):
    telegram_id: int
    web_username: str
    password: str


class PasswordLoginRequest(BaseModel):
    web_username: str
    password: str
