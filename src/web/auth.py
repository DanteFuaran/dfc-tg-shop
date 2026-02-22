"""Authentication helpers for web and Telegram Mini App."""

from __future__ import annotations

import hashlib
import hmac
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from urllib.parse import parse_qsl

import bcrypt as _bcrypt
from jose import JWTError, jwt

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24h


# ── Password helpers ──────────────────────────────────────────────


def hash_password(password: str) -> str:
    """Hash password using bcrypt directly (passlib-free)."""
    pw = password.encode("utf-8")[:72]  # bcrypt limit
    return _bcrypt.hashpw(pw, _bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against bcrypt hash."""
    try:
        return _bcrypt.checkpw(plain.encode("utf-8")[:72], hashed.encode("utf-8"))
    except Exception:
        return False


# ── JWT helpers ───────────────────────────────────────────────────


def create_access_token(
    data: dict[str, Any],
    secret_key: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str, secret_key: str) -> Optional[dict[str, Any]]:
    try:
        return jwt.decode(token, secret_key, algorithms=[ALGORITHM])
    except JWTError:
        return None


# ── Telegram WebApp initData validation ───────────────────────────


def validate_init_data(init_data: str, bot_token: str, max_age: int = 86400) -> Optional[dict[str, str]]:
    """Validate Telegram WebApp initData string.

    Returns parsed key-value dict on success, ``None`` on failure.
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    parsed = dict(parse_qsl(init_data, keep_blank_values=True))

    received_hash = parsed.pop("hash", None)
    if not received_hash:
        return None

    # Check data freshness (auth_date)
    auth_date_str = parsed.get("auth_date")
    if not auth_date_str:
        return None
    try:
        auth_date = int(auth_date_str)
    except ValueError:
        return None
    if time.time() - auth_date > max_age:
        return None

    # Build data-check-string
    data_check = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))

    # HMAC-SHA256 verification
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    computed_hash = hmac.new(secret_key, data_check.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed_hash, received_hash):
        return None

    return parsed
