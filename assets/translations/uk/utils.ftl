# Layout
space = {" "}
empty = { "!empty!" }
btn-test = Button
msg-test = Message
development = Temporarily unavailable!
test-payment = Test payment
unlimited = ∞
unknown = —
expired = Expired

unit-unlimited = { $value ->
    [-1] { unlimited }
    [0] { unlimited }
    *[other] { $value }
}

# Other
payment-invoice-description = { purchase-type } subscription { $name } for { $duration }
payment-invoice-topup = Balance top-up for { $amount }
payment-invoice-extra-devices = Extra devices purchase ({ $device_count } pcs.)
contact-support-help = Hello! I need help.
contact-support-paysupport = Hello! I would like to request a refund.
contact-support-withdraw-points = Hello! I would like to request points exchange.
cmd-start = Restart bot
cmd-support = Help

referral-invite-message =
    {space}

    ✨ TEST Online - Your private internet!

    ➡️ Connect: { $url }

# Headers
hdr-user = <b>👤 User:</b>
hdr-user-profile = <b>👤 Your Profile:</b>
hdr-subscription = <b>💳 Ваша підписка:</b>
hdr-plan = <b>💳 Підписка:</b>
hdr-payment = <b>💰 Payment:</b>
hdr-error = <b>⚠️ Error:</b>
hdr-node = <b>🖥 Node:</b>
hdr-hwid = <b>📱 Device:</b>
hdr-transfer = <b>💸 Transfer:</b>
hdr-message = <b>💬 Message:</b>
hdr-balance-mode = <b>💎 Balance Mode:</b>

# Labels
lbl-your-balance = • Your balance:
lbl-commission = • Commission:
lbl-recipient = • Recipient:
lbl-transfer-amount = • Transfer amount:
lbl-status = • Status:
lbl-min-topup-amount = • Minimum top-up amount:
lbl-max-topup-amount = • Maximum top-up amount:
lbl-enabled = ✅ Enabled
lbl-disabled = 🔴 Disabled
lbl-balance-mode-combined = • <b>Combined</b> - bonuses are credited to the main balance
lbl-balance-mode-separate = • <b>Separate</b> - separate bonus balance
lbl-not-set = Not set
lbl-payment-yoomoney = ЮMoney
lbl-payment-cryptomus = Cryptomus
lbl-payment-telegram-stars = Telegram Stars

# Messages
msg-fill-data-and-send = <i>ℹ️ Fill in the data and click the "Send" button.</i>

# Fragments
frg-user =
    <blockquote>
    • <b>ID</b>: <code>{ $user_id }</code>
    • <b>Name</b>: { $user_name }{ $is_referral_enable ->
        [1] {"\u000A"}• <b>Referral Code</b>: <code>{ $referral_code }</code>
        *[0] {""}
    }{ $discount_value ->
        [0] {""}
        *[other] {"\u000A"}• <b>Discount</b>: { $discount_value }%{ $discount_is_permanent ->
            [1] {" "}(Permanent)
            *[0] { $discount_remaining ->
                [0] {" "}(One-time)
                *[other] {" "}({ $discount_remaining } { $discount_remaining ->
                    [1] day
                    *[other] days
                } left)
            }
        }
    }{ $is_balance_enabled ->
        [1] {"\u000A"}• <b>Balance</b>: { $balance }
        *[0] {""}
    }{ $is_balance_separate ->
        [1] { $is_referral_enable ->
            [1] {"\u000A"}• <b>Bonuses</b>: { $referral_balance }
            *[0] {""}
        }
        *[0] {""}
    }
    </blockquote>

frg-user-info =
    <blockquote>
    • <b>ID</b>: <code>{ $user_id }</code>
    • <b>Name</b>: { $user_name } { $username -> 
        [0] { empty }
        *[HAS] (<a href="tg://user?id={ $user_id }">@{ $username }</a>)
    }
    </blockquote>

frg-user-details =
    <blockquote>
    • <b>ID</b>: <code>{ $user_id }</code>
    • <b>Name</b>: { $user_name } { $username -> 
        [0] { space }
        *[HAS] (<a href="tg://user?id={ $user_id }">@{ $username }</a>)
    }
    • <b>Role</b>: { role }
    • <b>Language</b>: { language }{ $is_referral_enable ->
        [1] {"\u000A"}• <b>Referral Code</b>: <code>{ $referral_code }</code>
        *[0] {""}
    }{ $is_balance_enabled ->
        [1] {"\u000A"}• <b>Balance</b>: { $balance } ₽
        *[0] {""}
    }{ $is_balance_separate ->
        [1] { $is_referral_enable ->
            [1] {"\u000A"}• <b>Referral Balance</b>: { $referral_balance } ₽
            *[0] {""}
        }
        *[0] {""}
    }
    </blockquote>

frg-user-discounts-details =
    <blockquote>
    • <b>Personal</b>: { $personal_discount }%
    • <b>Next purchase</b>: { $purchase_discount }%
    </blockquote>

frg-subscription =
    <blockquote>
    • <b>Plan:</b> { $current_plan_name }
    • <b>Traffic Limit</b>: { $traffic_limit }
    • <b>Device Limit</b>: { $device_limit_number }{ $device_limit_bonus ->
        [0] {""}
        *[other] +{ $device_limit_bonus }
    }{ $extra_devices ->
        [0] {""}
        *[other] {" "}(+{ $extra_devices } extra)
    }
    • <b>Remaining</b>: { $expire_time }
    </blockquote>

frg-subscription-details =
    <blockquote>
    • <b>ID</b>: <code>{ $subscription_id }</code>
    • <b>Status</b>: { subscription-status }
    • <b>Plan:</b> { $plan_name }
    • <b>Traffic</b>: { $traffic_used } / { $traffic_limit }
    • <b>Device Limit</b>: { $device_limit_number }{ $device_limit_bonus ->
        [0] {""}
        *[other] +{ $device_limit_bonus }
    }{ $extra_devices ->
        [0] {""}
        *[other] {" "}(+{ $extra_devices } extra)
    }
    • <b>Remaining</b>: { $expire_time }
    </blockquote>

frg-payment-info =
    <blockquote>
    • <b>ID</b>: <code>{ $payment_id }</code>
    • <b>Payment Method</b>: { gateway-type }
    • <b>Amount</b>: { frg-payment-amount }
    </blockquote>

frg-payment-amount = { $final_amount }{ $discount_percent -> 
    [0] { space }
    *[more] { space } <strike>{ $original_amount }</strike> (-{ $discount_percent }%)
    }

frg-plan-snapshot =
    <blockquote>
    • <b>Plan</b>: <code>{ $plan_name }</code>
    • <b>Type</b>: { plan-type }
    • <b>Traffic Limit</b>: { $plan_traffic_limit }
    • <b>Device Limit</b>: { $plan_device_limit }
    • <b>Duration</b>: { $plan_duration }
    • <b>Price</b>: { $plan_price }
    </blockquote>

frg-plan-snapshot-comparison =
    <blockquote>
    • <b>Plan</b>: <code>{ $previous_plan_name }</code> -> <code>{ $plan_name }</code>
    • <b>Type</b>: { $previous_plan_type } -> { plan-type }
    • <b>Traffic Limit</b>: { $previous_plan_traffic_limit } -> { $plan_traffic_limit }
    • <b>Device Limit</b>: { $previous_plan_device_limit } -> { $plan_device_limit }
    • <b>Duration</b>: { $previous_plan_duration } -> { $plan_duration }
    </blockquote>

frg-node-info =
    <blockquote>
    • <b>Name</b>: { $country } { $name }
    • <b>Address</b>: <code>{ $address }:{ $port }</code>
    • <b>Traffic</b>: { $traffic_used } / { $traffic_limit }
    { $last_status_message -> 
    [0] { empty }
    *[HAS] • <b>Last Status</b>: { $last_status_message }
    }
    { $last_status_change -> 
    [0] { empty }
    *[HAS] • <b>Status Changed</b>: { $last_status_change }
    }
    </blockquote>

frg-user-hwid =
    <blockquote>
    • <b>HWID</b>: <code>{ $hwid }</code>

    • <b>Platform</b>: { $platform }
    • <b>Model</b>: { $device_model }
    • <b>OS Version</b>: { $os_version }
    • <b>Agent</b>: { $user_agent }
    </blockquote>

frg-build-info =
    { $has_build ->
    [0] { space }
    *[HAS]
    <b>🏗️ Build Information:</b>
    <blockquote>
    Build Time: { $time }
    Branch: { $branch } ({ $tag })
    Commit: <a href="{ $commit_url }">{ $commit }</a>
    </blockquote>
    }

# Roles
role-dev = Developer
role-admin = Administrator
role-user = User
role = 
    { $role ->
    [DEV] { role-dev }
    [ADMIN] { role-admin }
    *[USER] { role-user }
}


# Units
unit-device = { $value -> 
    [-1] { unlimited }
    [0] Disabled
    *[other] { $value } 
} { $value ->
    [-1] { space }
    [0] { space }
    [one] device
    *[other] devices
}

unit-byte = { $value } B
unit-kilobyte = { $value } KB
unit-megabyte = { $value } MB
unit-gigabyte = { $value } GB
unit-terabyte = { $value } TB

unit-second = { $value } { $value ->
    [one] second
    *[other] seconds
}

unit-minute = { $value } { $value ->
    [one] minute
    *[other] minutes
}

unit-hour = { $value } { $value ->
    [one] hour
    *[other] hours
}

unit-day = { $value } { $value ->
    [one] day
    *[other] days
}

unit-month = { $value } { $value ->
    [one] month
    *[other] months
}

unit-year = { $value } { $value ->
    [one] year
    *[other] years
}


# Types
plan-type = { $plan_type -> 
    [TRAFFIC] Traffic
    [DEVICES] Devices
    [BOTH] Traffic + Devices
    [UNLIMITED] Unlimited
    *[OTHER] { $plan_type }
}

promocode-type = { $promocode_type -> 
    [DURATION] Duration
    [TRAFFIC] Traffic
    [DEVICES] Devices
    [SUBSCRIPTION] Subscription
    [PERSONAL_DISCOUNT] Permanent Discount
    [PURCHASE_DISCOUNT] One-time Discount
    *[OTHER] { $promocode_type }
}

promocode-type-name = { $type -> 
    [DURATION] Days to Subscription
    [TRAFFIC] Traffic
    [DEVICES] Devices
    [SUBSCRIPTION] Subscription
    [PERSONAL_DISCOUNT] Permanent Discount
    [PURCHASE_DISCOUNT] One-time Discount
    *[OTHER] { $type }
}

availability-type = { $availability_type -> 
    [ALL] For Everyone
    [NEW] For New Users
    [EXISTING] For Existing Users
    [INVITED] For Invited
    [ALLOWED] For Allowed
    [TRIAL] For Trial
    *[OTHER] { $availability_type }
}

gateway-type = { $gateway_type ->
    [TELEGRAM_STARS] ⭐ Telegram Stars
    [YOOKASSA] 💳 YooKassa
    [YOOMONEY] 💳 YooMoney
    [CRYPTOMUS] 🔐 Cryptomus
    [HELEKET] 💎 Heleket
    [URLPAY] UrlPay
    [BALANCE] 💰 З балансу
    *[OTHER] { $gateway_type }
}

access-mode = { $mode ->
    [PUBLIC] 🟢 Open for Everyone
    [INVITED] 🟡 Invited Only
    [RESTRICTED] 🔴 Restricted
    *[OTHER] { $mode }
}

audience-type = { $audience_type ->
    [ALL] Everyone
    [PLAN] By Plan
    [SUBSCRIBED] With Subscription
    [UNSUBSCRIBED] Without Subscription
    [EXPIRED] Expired
    [TRIAL] With Trial
    *[OTHER] { $audience_type }
}

broadcast-status = { $broadcast_status ->
    [PROCESSING] Processing
    [COMPLETED] Completed
    [CANCELED] Canceled
    [DELETED] Deleted
    [ERROR] Error
    *[OTHER] { $broadcast_status }
}

transaction-status = { $transaction_status ->
    [PENDING] Pending
    [COMPLETED] Completed
    [CANCELED] Canceled
    [REFUNDED] Refunded
    [FAILED] Failed
    *[OTHER] { $transaction_status }
}

subscription-status = { $subscription_status ->
    [ACTIVE] Active
    [DISABLED] Disabled
    [LIMITED] Traffic Exhausted
    [EXPIRED] Expired
    [DELETED] Deleted
    *[OTHER] { $subscription_status }
}

purchase-type = { $purchase_type ->
    [NEW] Purchase
    [RENEW] Renewal
    [CHANGE] Change
    *[OTHER] { $purchase_type }
}

traffic-strategy = { $strategy_type -> 
    [NO_RESET] On Payment
    [DAY] Daily
    [WEEK] Weekly
    [MONTH] Monthly
    *[OTHER] { $strategy_type }
    }

reward-type = { $reward_type -> 
    [POINTS] Points
    [EXTRA_DAYS] Days
    [MONEY] Money
    *[OTHER] { $reward_type }
    }

accrual-strategy = { $accrual_strategy_type -> 
    [ON_FIRST_PAYMENT] First Payment
    [ON_EACH_PAYMENT] Each Payment
    *[OTHER] { $accrual_strategy_type }
    }

reward-strategy = { $reward_strategy_type -> 
    [AMOUNT] Fixed
    [PERCENT] Percentage
    *[OTHER] { $reward_strategy_type }
    }

# Fragment: Current subscription with check
frg-subscription-conditional =
    { $has_subscription ->
    [true]
    { frg-subscription }
    *[false]
    <blockquote>
    • You don't have an active subscription.
    </blockquote>
    }

# Fragment: Full subscription status (with explanations)
frg-subscription-status-full =
    { $status ->
    [ACTIVE] { frg-subscription }
    [EXPIRED]
    <blockquote>
    • Subscription expired.
    
    <i>{ $is_trial ->
    [0] Your subscription has expired. Renew it to continue using the service!
    *[1] Your free trial period has ended. Purchase a subscription to continue using the service!
    }</i>
    </blockquote>
    [LIMITED]
    <blockquote>
    • Your traffic is exhausted.

    <i>{ $is_trial ->
    [0] { $traffic_strategy ->
        [NO_RESET] Renew your subscription to reset traffic and continue using the service!
        *[RESET] Traffic will be restored in { $reset_time }. You can also renew your subscription to reset traffic.
        }
    *[1] { $traffic_strategy ->
        [NO_RESET] Purchase a subscription to continue using the service!
        *[RESET] Traffic will be restored in { $reset_time }. You can also purchase a subscription to use the service without restrictions.
        }
    }</i>
    </blockquote>
    [DISABLED]
    <blockquote>
    • Your subscription is disabled.

    <i>Contact support to find out the reason!</i>
    </blockquote>
    *[NONE]
    <blockquote>
    • You don't have an active subscription.
    </blockquote>

    <i>ℹ️ To get access, go to the <b>"Subscription"</b> menu.</i>
    }

# Fragment: Short subscription status (for admin panel)
frg-subscription-status-short =
    { $status ->
    [ACTIVE]
    { frg-subscription }
    [EXPIRED]
    <blockquote>
    • Subscription expired.
    </blockquote>
    [LIMITED]
    <blockquote>
    • Traffic limit exceeded.
    </blockquote>
    [DISABLED]
    <blockquote>
    • Subscription disabled.
    </blockquote>
    *[NONE]
    <blockquote>
    • No current subscription.
    </blockquote>
    }

# Fragment: Purchase type warning
frg-purchase-type-warning =
    { $purchase_type ->
    [RENEW] <i>⚠️ Current subscription will be <u>extended</u>.</i>
    [CHANGE] <i>⚠️ Current subscription will be <u>replaced</u> without recalculating remaining time.</i>
    *[OTHER] { empty }
    }

# Fragment: Purchase confirmation header
frg-purchase-confirm-header =
    { $purchase_type ->
    [RENEW] <b>🛒 Підтвердження продовження підписки</b>
    [CHANGE] <b>🛒 Підтвердження зміни підписки</b>
    *[OTHER] <b>🛒 Підтвердження покупки підписки</b>
    }

# Фрагмент: Інформація користувача без blockquote (для confirm повідомлень)
frg-user-info-inline =
    • <b>ID</b>: <code>{ $user_id }</code>
    • <b>Ім'я</b>: { $user_name }{ $is_referral_enable ->
        [1] {"\u000A"}• <b>Реферальний код</b>: <code>{ $referral_code }</code>
        *[0] {""}
    }{ $discount_value ->
        [0] {""}
        *[other] {"\u000A"}• <b>Знижка</b>: { $discount_value }%{ $discount_is_permanent ->
            [1] {" "}(Постійна)
            *[0] { $discount_remaining ->
                [0] {" "}(Одноразова)
                *[other] {" "}(Залишилось { $discount_remaining } { $discount_remaining ->
                    [1] день
                    [2] дні
                    [3] дні
                    [4] дні
                    *[other] днів
                })
            }
        }
    }{ $is_balance_enabled ->
        [1] {"\u000A"}• <b>Баланс</b>: { $balance }
        *[0] {""}
    }{ $is_balance_separate ->
        [1] { $is_referral_enable ->
            [1] {"\u000A"}• <b>Бонуси</b>: { $referral_balance }
            *[0] {""}
        }
        *[0] {""}
    }

# Фрагмент: Підписка без blockquote (для confirm повідомлень)
frg-subscription-inline =
    • <b>Тариф:</b> { $current_plan_name }
    • <b>Ліміт трафіку</b>: { $traffic_limit }
    • <b>Ліміт пристроїв</b>: { $device_limit_number }{ $device_limit_bonus ->
        [0] {""}
        *[other] +{ $device_limit_bonus }
    }{ $extra_devices ->
        [0] {""}
        *[other] {" "}(+{ $extra_devices } дод.)
    }
    • <b>Залишилось</b>: { $expire_time }

language = { $language ->
    [ar] Arabic
    [az] Azerbaijani
    [be] Belarusian
    [cs] Czech
    [de] German
    [en] English
    [es] Spanish
    [fa] Persian
    [fr] French
    [he] Hebrew
    [hi] Hindi
    [id] Indonesian
    [it] Italian
    [ja] Japanese
    [kk] Kazakh
    [ko] Korean
    [ms] Malay
    [nl] Dutch
    [pl] Polish
    [pt] Portuguese
    [ro] Romanian
    [ru] Russian
    [sr] Serbian
    [tr] Turkish
    [uk] Ukrainian
    [uz] Uzbek
    [vi] Vietnamese
    *[OTHER] { $language }
}

# Hardcoded strings - UI elements
frg-empty-slot = Empty slot
frg-not-assigned = Not assigned
frg-import-name = Import
frg-extra-devices-name = Extra devices (x{ $count })
frg-day-plural = { $value ->
    [one] day
    [few] days
    *[many] days
}

# ===== Web Connect Page =====
msg-connect-page-title = Connecting...
msg-connect-loading = Opening app...
msg-connect-success-title = Subscription added successfully
msg-connect-success-desc = Page will close automatically...

# ===== Invite Message =====
msg-invite-welcome = Welcome!
msg-invite-connect = Connect
# ===== Settings Display Values =====
# Commission/Discount Types
settings-type-percent = Відсоткова
settings-type-fixed = Фіксована

# Commission Values
settings-commission-free = Безкоштовно

# Discount Values
settings-discount-none = Без знижки

# Stack Mode
settings-stack-mode-stacked = Складена
settings-stack-mode-max = Максимальна

# Apply To
settings-apply-subscription = Підписка
settings-apply-extra-devices = Дод.пристрої
settings-apply-commission = Комісія
settings-apply-nothing = Нічого

# Plan Status
settings-subscription-activated = Підписка активована