"""Web router — aggregates all sub-routers for the web API and Mini App.

Structure:
    routers/
        pages.py          — HTML page routes (/, /login, /dashboard, /miniapp)
        auth.py           — /api/auth/* (tg, check, register, login, logout)
        user.py           — /api/config, /api/user/*, /api/tickets/status
        purchase.py       — /api/purchase, /api/trial/*, /api/topup, /api/promocode/*
        tickets.py        — /api/tickets/* (user ticket CRUD)
        admin/
            stats.py      — /api/admin/stats
            users.py      — /api/admin/users/*
            plans.py      — /api/admin/plans/*
            settings.py   — /api/admin/settings
            gateways.py   — /api/admin/gateways/*
            brand.py      — /api/settings/brand
            tickets.py    — /api/admin/tickets/*
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter

from .routers import pages, auth, user, purchase, tickets
from .routers.admin import brand, gateways, plans, settings, stats, tickets as admin_tickets, users
from .routers.admin import monitoring, broadcast, promocodes, bot as admin_bot

WEB_DIR = Path(__file__).parent

router = APIRouter()

# HTML pages (no prefix — mounted at /web in app.py)
router.include_router(pages.router)

# REST API sub-routers
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(purchase.router)
router.include_router(tickets.router)

# Admin sub-routers
router.include_router(stats.router)
router.include_router(users.router)
router.include_router(plans.router)
router.include_router(settings.router)
router.include_router(gateways.router)
router.include_router(brand.router)
router.include_router(admin_tickets.router)
router.include_router(monitoring.router)
router.include_router(broadcast.router)
router.include_router(promocodes.router)
router.include_router(admin_bot.router)
