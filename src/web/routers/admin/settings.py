"""Admin settings routes."""

from __future__ import annotations

from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from src.services.settings import SettingsService
from src.web.dependencies import require_admin

router = APIRouter(prefix="/api/admin/settings", tags=["admin-settings"])


@router.get("")
async def api_admin_settings(request: Request, uid: int = Depends(require_admin)):
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        settings_service: SettingsService = await req_container.get(SettingsService)
        settings = await settings_service.get()
        features = settings.features
        ed = features.extra_devices
        tr = features.transfers
        inot = features.inactive_notifications
        gd = features.global_discount
        cr = features.currency_rates
        ref = settings.referral
        u_notif = settings.user_notifications
        s_notif = settings.system_notifications
        return JSONResponse({
            "balance_enabled": features.balance_enabled,
            "balance_mode": features.balance_mode.value if hasattr(features.balance_mode, "value") else str(features.balance_mode),
            "balance_min_amount": features.balance_min_amount,
            "balance_max_amount": features.balance_max_amount,
            "community_enabled": features.community_enabled,
            "community_url": features.community_url or "",
            "tos_enabled": features.tos_enabled,
            "referral_enabled": features.referral_enabled,
            "referral_level": ref.level.value if hasattr(ref.level, "value") else str(ref.level),
            "referral_accrual_strategy": ref.accrual_strategy.value if hasattr(ref.accrual_strategy, "value") else str(ref.accrual_strategy),
            "referral_reward_type": ref.reward.type.value if hasattr(ref.reward.type, "value") else str(ref.reward.type),
            "referral_reward_strategy": ref.reward.strategy.value if hasattr(ref.reward.strategy, "value") else str(ref.reward.strategy),
            "referral_reward_value": ref.reward.config.get(ref.level, 10),
            "referral_invite_message": ref.invite_message or "",
            "promocodes_enabled": features.promocodes_enabled,
            "notifications_enabled": features.notifications_enabled,
            "extra_devices_enabled": ed.enabled,
            "extra_devices_price": ed.price_per_device,
            "extra_devices_one_time": ed.is_one_time,
            "extra_devices_min_days": ed.min_days,
            "transfers_enabled": tr.enabled,
            "transfers_commission_type": tr.commission_type,
            "transfers_commission_value": tr.commission_value,
            "transfers_min_amount": tr.min_amount,
            "transfers_max_amount": tr.max_amount,
            "inactive_notif_enabled": inot.enabled,
            "inactive_notif_hours": inot.hours_threshold,
            "global_discount_enabled": gd.enabled,
            "global_discount_type": gd.discount_type,
            "global_discount_value": gd.discount_value,
            "global_discount_stack": gd.stack_discounts,
            "global_discount_apply_sub": gd.apply_to_subscription,
            "global_discount_apply_devices": gd.apply_to_extra_devices,
            "global_discount_apply_transfer": gd.apply_to_transfer_commission,
            "currency_rates_auto": cr.auto_update,
            "currency_rates_usd": cr.usd_rate,
            "currency_rates_eur": cr.eur_rate,
            "currency_rates_stars": cr.stars_rate,
            "access_enabled": features.access_enabled,
            "language_enabled": features.language_enabled,
            "access_mode": settings.access_mode.value if hasattr(settings.access_mode, "value") else str(settings.access_mode),
            "default_currency": settings.default_currency.value if hasattr(settings.default_currency, "value") else str(settings.default_currency),
            "purchases_allowed": settings.purchases_allowed,
            "registration_allowed": settings.registration_allowed,
            "rules_required": settings.rules_required,
            "channel_required": settings.channel_required,
            "channel_link": settings.channel_link.get_secret_value() if hasattr(settings.channel_link, "get_secret_value") else str(settings.channel_link),
            "tos_url": settings.rules_link.get_secret_value() if hasattr(settings.rules_link, "get_secret_value") else str(settings.rules_link),
            "bot_locale": settings.bot_locale.value if hasattr(settings.bot_locale, "value") else str(settings.bot_locale),
            # User notifications
            "un_expires_3d": u_notif.expires_in_3_days,
            "un_expires_2d": u_notif.expires_in_2_days,
            "un_expires_1d": u_notif.expires_in_1_days,
            "un_expired": u_notif.expired,
            "un_limited": u_notif.limited,
            "un_expired_1d_ago": u_notif.expired_1_day_ago,
            "un_referral_attached": u_notif.referral_attached,
            "un_referral_reward": u_notif.referral_reward,
            # System notifications
            "sn_bot_lifetime": s_notif.bot_lifetime,
            "sn_bot_update": s_notif.bot_update,
            "sn_user_registered": s_notif.user_registered,
            "sn_subscription": s_notif.subscription,
            "sn_extra_devices": s_notif.extra_devices,
            "sn_promocode": s_notif.promocode_activated,
            "sn_trial": s_notif.trial_getted,
            "sn_node_status": s_notif.node_status,
            "sn_user_connected": s_notif.user_first_connected,
            "sn_user_hwid": s_notif.user_hwid,
            "sn_billing": s_notif.billing,
            "sn_balance_transfer": s_notif.balance_transfer,
        })


@router.patch("")
async def api_admin_update_settings(request: Request, uid: int = Depends(require_admin)):
    body = await request.json()
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        settings_service: SettingsService = await req_container.get(SettingsService)

        # Toggle feature flags
        feature_fields = {
            "balance_enabled", "community_enabled", "tos_enabled",
            "referral_enabled", "promocodes_enabled", "notifications_enabled",
            "access_enabled", "language_enabled",
        }
        settings_fields = {"purchases_allowed", "registration_allowed", "channel_required"}
        settings_bool_fields = {"rules_required"}
        settings_str_fields = {"tos_url", "channel_link"}
        string_feature_fields = {"community_url"}

        # Sub-settings mapping: key -> (parent_attr, child_attr, type)
        sub_settings_map = {
            "balance_mode": ("features", "balance_mode", "balance_mode"),
            "balance_min_amount": ("features", "balance_min_amount", "int_or_none"),
            "balance_max_amount": ("features", "balance_max_amount", "int_or_none"),
            "extra_devices_enabled": ("features.extra_devices", "enabled", "bool"),
            "extra_devices_price": ("features.extra_devices", "price_per_device", "int"),
            "extra_devices_one_time": ("features.extra_devices", "is_one_time", "bool"),
            "extra_devices_min_days": ("features.extra_devices", "min_days", "int"),
            "transfers_enabled": ("features.transfers", "enabled", "bool"),
            "transfers_commission_type": ("features.transfers", "commission_type", "str"),
            "transfers_commission_value": ("features.transfers", "commission_value", "int"),
            "transfers_min_amount": ("features.transfers", "min_amount", "int"),
            "transfers_max_amount": ("features.transfers", "max_amount", "int"),
            "inactive_notif_enabled": ("features.inactive_notifications", "enabled", "bool"),
            "inactive_notif_hours": ("features.inactive_notifications", "hours_threshold", "int"),
            "global_discount_enabled": ("features.global_discount", "enabled", "bool"),
            "global_discount_type": ("features.global_discount", "discount_type", "str"),
            "global_discount_value": ("features.global_discount", "discount_value", "int"),
            "global_discount_stack": ("features.global_discount", "stack_discounts", "bool"),
            "global_discount_apply_sub": ("features.global_discount", "apply_to_subscription", "bool"),
            "global_discount_apply_devices": ("features.global_discount", "apply_to_extra_devices", "bool"),
            "global_discount_apply_transfer": ("features.global_discount", "apply_to_transfer_commission", "bool"),
            "currency_rates_auto": ("features.currency_rates", "auto_update", "bool"),
            "currency_rates_usd": ("features.currency_rates", "usd_rate", "float"),
            "currency_rates_eur": ("features.currency_rates", "eur_rate", "float"),
            "currency_rates_stars": ("features.currency_rates", "stars_rate", "float"),
        }

        settings = await settings_service.get()
        need_save = False

        for key, value in body.items():
            if key in feature_fields and isinstance(value, bool):
                await settings_service.toggle_feature(key)
            elif key in settings_bool_fields and isinstance(value, bool):
                settings = await settings_service.get()
                setattr(settings, key, value)
                need_save = True
            elif key in settings_str_fields and isinstance(value, str):
                settings = await settings_service.get()
                if key == "tos_url":
                    from pydantic import SecretStr
                    settings.rules_link = SecretStr(value)
                elif key == "channel_link":
                    from pydantic import SecretStr
                    settings.channel_link = SecretStr(value)
                need_save = True
            elif key in settings_fields and isinstance(value, bool):
                settings = await settings_service.get()
                setattr(settings, key, value)
                need_save = True
            elif key in string_feature_fields and isinstance(value, str):
                settings = await settings_service.get()
                setattr(settings.features, key, value)
                need_save = True
            elif key in sub_settings_map:
                parent_path, attr, val_type = sub_settings_map[key]
                # Navigate to parent object
                obj = settings
                for part in parent_path.split("."):
                    obj = getattr(obj, part)
                # Convert and set value
                if val_type == "bool":
                    setattr(obj, attr, bool(value))
                elif val_type == "int":
                    setattr(obj, attr, int(value))
                elif val_type == "int_or_none":
                    setattr(obj, attr, int(value) if value is not None else None)
                elif val_type == "float":
                    setattr(obj, attr, float(value))
                elif val_type == "str":
                    setattr(obj, attr, str(value))
                elif val_type == "balance_mode":
                    from src.core.enums import BalanceMode
                    setattr(obj, attr, BalanceMode(str(value)))
                need_save = True
            # Referral settings
            elif key == "referral_level":
                from src.core.enums import ReferralLevel
                settings.referral.level = ReferralLevel(int(value))
                need_save = True
            elif key == "referral_accrual_strategy":
                from src.core.enums import ReferralAccrualStrategy
                settings.referral.accrual_strategy = ReferralAccrualStrategy(str(value))
                need_save = True
            elif key == "referral_reward_type":
                from src.core.enums import ReferralRewardType
                settings.referral.reward.type = ReferralRewardType(str(value))
                need_save = True
            elif key == "referral_reward_strategy":
                from src.core.enums import ReferralRewardStrategy
                settings.referral.reward.strategy = ReferralRewardStrategy(str(value))
                need_save = True
            elif key == "referral_reward_value":
                settings.referral.reward.config[settings.referral.level] = int(value)
                need_save = True
            elif key == "referral_invite_message":
                settings.referral.invite_message = str(value)
                need_save = True
            # User notifications
            elif key.startswith("un_"):
                field = key[3:]
                if hasattr(settings.user_notifications, field):
                    setattr(settings.user_notifications, field, bool(value))
                    need_save = True
            # System notifications
            elif key.startswith("sn_"):
                field = key[3:]
                if hasattr(settings.system_notifications, field):
                    setattr(settings.system_notifications, field, bool(value))
                    need_save = True

        if need_save:
            await settings_service.update(settings)

        return JSONResponse({"ok": True})
