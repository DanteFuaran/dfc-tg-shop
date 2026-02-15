# Dashboard
btn-dashboard-broadcast = 📢 Broadcast
btn-dashboard-statistics = 📊 Statistics
btn-dashboard-users = 👥 Users
btn-dashboard-plans = 📦 Pricing Plans
btn-dashboard-promocodes = 🎟 Promo Codes
btn-dashboard-remnawave = 🌊 Panel Monitoring
btn-dashboard-remnashop = 🛍 Telegram
btn-dashboard-access = 🔓 Access Mode
btn-dashboard-features = ⚙️ Features
btn-dashboard-importer = 📥 X-UI Import
btn-dashboard-bot-management = 🤖 Bot Management
btn-dashboard-user-management = 👥 Users

# Bot Management
btn-bot-check-update = 🔍 Check for Updates
btn-bot-restart = 🔁 Restart

# Database Management
btn-dashboard-db = 🗄 Database Management
btn-db-save = 💾 Save
btn-db-load = 📦 Load
btn-db-close = ❌ Close
btn-db-sync-from-panel = 📥 Remnawave Import
btn-db-clear-all = 🗑 Clear All
btn-db-clear-users = 👥 Clear Users
btn-db-imports = 📥 Import
btn-db-sync = 🔄 Sync
btn-db-remnawave-import = 📥 Remnawave Import
btn-db-xui-import = 💩 X-UI Import
btn-db-sync-remnawave-to-bot = 📥 From Panel to Bot
btn-db-sync-bot-to-remnawave = 📤 From Bot to Panel

# Settings
btn-dashboard-settings = ⚙️ Features
btn-settings-extra-devices = 📱 Extra Devices
btn-settings-balance = 💰 Balance
btn-settings-transfers = 💸 Transfers
btn-settings-notifications = 🔔 Notifications
btn-settings-access = 🔓 Access Mode
btn-settings-referral = 👥 Referral System
btn-settings-promocodes = 🏷️ Promo Codes
btn-settings-community = 👥 Community
btn-settings-community-set-url = 📝 Set Group
btn-settings-tos = 📜 Agreement
btn-tos-set-url = Set Source
btn-settings-global-discount = 🏷️ Global Discount
btn-settings-finances = 💰 Finances
btn-settings-currency-rates = 💱 Exchange Rates
btn-settings-language = 🌐 Language
btn-language-multilang = { $enabled ->
    [1] 🟢 Multilingual
    *[0] 🔴 Multilingual
}
btn-language-ru = 🇷🇺 Russian
btn-language-uk = 🇺🇦 Ukrainian
btn-language-en = 🇬🇧 English
btn-language-de = 🇩🇪 German
btn-language-cancel = ❌ Cancel
btn-language-apply = ✅ Apply
btn-finances-sync = { $enabled ->
    [1] 🟢 Rate Synchronization
    *[0] 🔴 Rate Synchronization
    }
btn-finances-currency-rates = 💱 Exchange Rates
btn-finances-gateways = 🌐 Payment Systems
btn-balance-mode-combined = { $selected ->
    [1] 🔘 Combined
    *[0] ⚪ Combined
    }
btn-balance-mode-separate = { $selected ->
    [1] 🔘 Separate
    *[0] ⚪ Separate
    }
btn-currency-auto-toggle = { $enabled ->
    [1] 🟢 Automatic
    *[0] 🔴 Automatic
    }
btn-settings-toggle = { $enabled ->
    [1] 🟢
    *[0] 🔴
    }
btn-toggle-setting = { $name }: { $enabled ->
    [1] ✅ Enabled
    *[0] 🔴 Disabled
    }
btn-setting-value = { $name }: { $value }
btn-commission-type-percent = 
    { $selected ->
    [1] 🔘 Percentage
    *[0] ⚪ Percentage
    }
btn-commission-type-fixed = 
    { $selected ->
    [1] 🔘 Fixed
    *[0] ⚪ Fixed
    }
btn-commission-value = 💵 Commission: { $value } { $unit }

unit-percent-or-rub = { $commission_type ->
    [percent] %
    *[fixed] ₽
    }

# Global Discount
btn-discount-type-percent = 
    { $selected ->
    [1] 🔘 Percentage
    *[0] ⚪ Percentage
    }
btn-discount-type-fixed = 
    { $selected ->
    [1] 🔘 Fixed
    *[0] ⚪ Fixed
    }
btn-discount-value = 🏷️ Discount: { $value } { $unit }

unit-discount-percent-or-rub = { $discount_type ->
    [percent] %
    *[fixed] ₽
    }

# Discount Stacking Mode
btn-global-discount-mode = ⚙️ Mode
btn-global-discount-apply-to = 📌 Applies To

# Mode submenu (radio buttons)
btn-discount-mode-max = { $selected ->
    [1] 🔘 Maximum
    *[0] ⚪ Maximum
    }
btn-discount-mode-stack = { $selected ->
    [1] 🔘 Stacked
    *[0] ⚪ Stacked
    }

# What the discount applies to (checkboxes)
btn-apply-to-subscription = { $enabled ->
    [1] ✅ Subscription
    *[0] ⬜ Subscription
    }
btn-apply-to-extra-devices = { $enabled ->
    [1] ✅ Extra Devices
    *[0] ⬜ Extra Devices
    }
btn-apply-to-transfer-commission = { $enabled ->
    [1] ✅ Transfer Commission
    *[0] ⬜ Transfer Commission
    }

btn-discount-free = { $selected ->
    [1] [🚫 No Discount]
    *[0] 🚫 No Discount
    }

# Discount - Percentage Values
btn-discount-5 = { $selected ->
    [1] [5%]
    *[0] 5%
    }
btn-discount-10 = { $selected ->
    [1] [10%]
    *[0] 10%
    }
btn-discount-15 = { $selected ->
    [1] [15%]
    *[0] 15%
    }
btn-discount-20 = { $selected ->
    [1] [20%]
    *[0] 20%
    }
btn-discount-25 = { $selected ->
    [1] [25%]
    *[0] 25%
    }
btn-discount-30 = { $selected ->
    [1] [30%]
    *[0] 30%
    }
btn-discount-35 = { $selected ->
    [1] [35%]
    *[0] 35%
    }
btn-discount-40 = { $selected ->
    [1] [40%]
    *[0] 40%
    }
btn-discount-45 = { $selected ->
    [1] [45%]
    *[0] 45%
    }
btn-discount-50-percent = { $selected ->
    [1] [50%]
    *[0] 50%
    }
btn-discount-55 = { $selected ->
    [1] [55%]
    *[0] 55%
    }
btn-discount-60 = { $selected ->
    [1] [60%]
    *[0] 60%
    }
btn-discount-65 = { $selected ->
    [1] [65%]
    *[0] 65%
    }
btn-discount-70 = { $selected ->
    [1] [70%]
    *[0] 70%
    }
btn-discount-75 = { $selected ->
    [1] [75%]
    *[0] 75%
    }
btn-discount-80 = { $selected ->
    [1] [80%]
    *[0] 80%
    }
btn-discount-85 = { $selected ->
    [1] [85%]
    *[0] 85%
    }
btn-discount-90 = { $selected ->
    [1] [90%]
    *[0] 90%
    }
btn-discount-95 = { $selected ->
    [1] [95%]
    *[0] 95%
    }
btn-discount-100 = { $selected ->
    [1] [100%]
    *[0] 100%
    }

# Discount - Fixed Values (rubles)
btn-discount-50-rub = { $selected ->
    [1] [50 ₽]
    *[0] 50 ₽
    }
btn-discount-100-rub = { $selected ->
    [1] [100 ₽]
    *[0] 100 ₽
    }
btn-discount-150-rub = { $selected ->
    [1] [150 ₽]
    *[0] 150 ₽
    }
btn-discount-200-rub = { $selected ->
    [1] [200 ₽]
    *[0] 200 ₽
    }
btn-discount-250-rub = { $selected ->
    [1] [250 ₽]
    *[0] 250 ₽
    }
btn-discount-300-rub = { $selected ->
    [1] [300 ₽]
    *[0] 300 ₽
    }
btn-discount-350-rub = { $selected ->
    [1] [350 ₽]
    *[0] 350 ₽
    }
btn-discount-400-rub = { $selected ->
    [1] [400 ₽]
    *[0] 400 ₽
    }
btn-discount-450-rub = { $selected ->
    [1] [450 ₽]
    *[0] 450 ₽
    }
btn-discount-500-rub = { $selected ->
    [1] [500 ₽]
    *[0] 500 ₽
    }
btn-discount-600-rub = { $selected ->
    [1] [600 ₽]
    *[0] 600 ₽
    }
btn-discount-700-rub = { $selected ->
    [1] [700 ₽]
    *[0] 700 ₽
    }
btn-discount-800-rub = { $selected ->
    [1] [800 ₽]
    *[0] 800 ₽
    }
btn-discount-900-rub = { $selected ->
    [1] [900 ₽]
    *[0] 900 ₽
    }
btn-discount-1000-rub = { $selected ->
    [1] [1000 ₽]
    *[0] 1000 ₽
    }

# Back
btn-back = ⬅️ Back
btn-main-menu = 🏠 Main Menu
btn-back-main-menu = 🏠 Main Menu
btn-back-dashboard = ⚙️ Control Panel
btn-back-users = 👥 Users
btn-done = ✅ Done


# Telegram
btn-remnashop-release-latest = 👀 View
btn-remnashop-how-upgrade = ❓ How to Update
btn-remnashop-github = ⭐ GitHub
btn-remnashop-telegram = 👪 Telegram
btn-remnashop-donate = 💰 Support the Developer
btn-remnashop-guide = ❓ Guide


# Other
btn-rules-accept = ✅ Accept Rules
btn-channel-join = ❤️ Go to Channel
btn-channel-confirm = ✅ Confirm
btn-notification-close = ❌ Close
btn-goto-main-menu = 🏠 To Main Menu
btn-contact-support = 📩 Go to Support
btn-cancel = ❌ Cancel
btn-accept = ✅ Accept
btn-confirm = ✅ Confirm
btn-confirm-payment = ✅ Confirm Payment
btn-select-all = 📋 All Subscriptions
btn-select-all-toggle =
    { $all_selected ->
    [1] ✅ All Subscriptions
    *[0] ⬜ All Subscriptions
    }

btn-squad-choice = { $selected -> 
    [1] 🔘
    *[0] ⚪
    } { $name }

btn-role-choice = { $selected -> 
    [1] 🔘
    *[0] ⚪
    } { $name }


# Menu
btn-menu-connect = 🚀 Connect
btn-menu-connect-open = 🔗 Connect
btn-menu-connect-subscribe = 📄 Subscription Page
btn-menu-connect-qr = 📱 QR Code
btn-menu-connect-key = 🔑 Show Key
btn-menu-download = 📥 Download App
btn-menu-download-android = 📱 Android
btn-menu-download-windows = 🖥 Windows
btn-menu-download-iphone = 🍎 iPhone
btn-menu-download-macos = 💻 macOS

btn-menu-connect-not-available =
    ⚠️ { $status -> 
    [LIMITED] Traffic Limit Exceeded
    [EXPIRED] Subscription Expired
    *[OTHER] No Subscription
    }

btn-menu-trial = { $is_referral_trial ->
    [1] 📢 Referral Subscription
    *[0] 🎁 Trial Subscription
    }
btn-menu-devices = 📱 My Devices
btn-menu-devices-empty = ⚠️ No Linked Devices
btn-menu-add-device = ➕ Add Device
btn-menu-extra-devices = 📱 Extra Device Management
btn-extra-device-item = { $device_count } pcs. • { $price } ₽/mo • { $expires_at }
btn-extra-device-disable-auto-renew = ❌ Disable Auto-Renewal
btn-extra-device-delete = 🗑 Delete Now
btn-menu-try-free = 🎁 Try Free
btn-menu-balance = 💰 Balance: { $balance }
btn-menu-subscription = 💳 Subscription
btn-menu-connect-subscribe = 🔗 Connect
btn-menu-topup = ➕ Top Up
btn-menu-invite = 👥 Invite
btn-menu-invite-about = ❓ More About Rewards
btn-menu-invite-copy = 🔗 Invitation Link
btn-menu-invite-send = 📩 Invite
btn-menu-invite-qr = 🧾 QR Code
btn-menu-invite-withdraw-points = 💰 Withdraw Balance
btn-menu-invite-withdraw-balance = 💸 Activate Bonuses
btn-menu-promocode = 🎟 Promo Code
btn-menu-support = 🆘 Help
btn-menu-tos = 📋 Agreement
btn-menu-community = 👥 Community
btn-menu-dashboard = 🛠 Control Panel

# Balance
btn-balance-topup = ➕ Top Up
btn-balance-withdraw = ➖ Withdraw
btn-balance-transfer = 💸 Transfer
btn-balance-gateway = 
    { $gateway_type ->
    [YOOMONEY] 💳 YooMoney
    [YOOKASSA] 💳 YooKassa
    [CRYPTOMUS] 🔐 Cryptomus
    [HELEKET] 💎 Heleket
    [TELEGRAM_STARS] ⭐ Telegram
    *[OTHER] 💳 { $gateway_type }
    }

# Subscription Key
btn-subscription-key-close = ❌ Close
btn-balance-custom-amount = ✏️ Custom Amount
btn-balance-pay = ✅ Pay
btn-balance-transfer-recipient = 👤 Recipient
btn-balance-transfer-amount = 💵 Amount: { $amount } ₽
btn-balance-transfer-message = 💬 Message
btn-balance-transfer-send = ✅ Send
btn-balance-transfer-history = 📜 User History
btn-transfer-amount-100 = { $selected ->
    [1] [100 ₽]
    *[0] 100 ₽
    }
btn-transfer-amount-250 = { $selected ->
    [1] [250 ₽]
    *[0] 250 ₽
    }
btn-transfer-amount-500 = { $selected ->
    [1] [500 ₽]
    *[0] 500 ₽
    }
btn-transfer-amount-1000 = { $selected ->
    [1] [1000 ₽]
    *[0] 1000 ₽
    }
btn-transfer-amount-2000 = { $selected ->
    [1] [2000 ₽]
    *[0] 2000 ₽
    }
btn-transfer-amount-5000 = { $selected ->
    [1] [5000 ₽]
    *[0] 5000 ₽
    }

# Bonus Activation
btn-bonus-custom-amount = ✏️ Custom Amount

# Dashboard
btn-dashboard-statistics = 📊 Statistics
btn-dashboard-users = 👥 Users
btn-dashboard-broadcast = 📢 Broadcast
btn-dashboard-promocodes = 🎟 Promo Codes
btn-dashboard-access = 🔓 Access Mode
btn-dashboard-features = ⚙️ Features
btn-dashboard-remnawave = 🌊 Panel Monitoring
btn-dashboard-remnashop = 🛍 Telegram
btn-dashboard-importer = 📥 User Import
btn-dashboard-save-db = 💾 Save DB
btn-db-export = 📤 Export
btn-db-import = 📥 Import

# Features
btn-feature-toggle =
    { $enabled ->
    [1] ✅ { $name }
    *[0] ⬜ { $name }
    }

btn-extra-devices-menu = 📱 Extra Devices
btn-extra-devices-price = 💰 Cost: { $price } ₽
btn-extra-devices-min-days = ⏳ Min Days: { $days }
btn-extra-devices-one-time = 
    { $selected ->
    [1] 🔘 One-Time
    *[0] ⚪ One-Time
    }
btn-extra-devices-monthly = 
    { $selected ->
    [1] 🔘 Monthly
    *[0] ⚪ Monthly
    }

# Days for minimum period
btn-days-1 = { $selected ->
    [1] [1 day]
    *[0] 1 day
}
btn-days-3 = { $selected ->
    [1] [3 days]
    *[0] 3 days
}
btn-days-5 = { $selected ->
    [1] [5 days]
    *[0] 5 days
}
btn-days-7 = { $selected ->
    [1] [7 days]
    *[0] 7 days
}
btn-days-10 = { $selected ->
    [1] [10 days]
    *[0] 10 days
}
btn-days-14 = { $selected ->
    [1] [14 days]
    *[0] 14 days
}
btn-days-30 = { $selected ->
    [1] [30 days]
    *[0] 30 days
}

# Extra device prices
btn-price-free = { $selected ->
    [1] [Free]
    *[0] Free
    }
btn-price-100 = { $selected ->
    [1] [100 ₽]
    *[0] 100 ₽
    }
btn-price-200 = { $selected ->
    [1] [200 ₽]
    *[0] 200 ₽
    }
btn-price-300 = { $selected ->
    [1] [300 ₽]
    *[0] 300 ₽
    }
btn-price-400 = { $selected ->
    [1] [400 ₽]
    *[0] 400 ₽
    }
btn-price-500 = { $selected ->
    [1] [500 ₽]
    *[0] 500 ₽
    }
btn-price-600 = { $selected ->
    [1] [600 ₽]
    *[0] 600 ₽
    }
btn-price-700 = { $selected ->
    [1] [700 ₽]
    *[0] 700 ₽
    }
btn-price-800 = { $selected ->
    [1] [800 ₽]
    *[0] 800 ₽
    }
btn-price-900 = { $selected ->
    [1] [900 ₽]
    *[0] 900 ₽
    }
btn-price-1000 = { $selected ->
    [1] [1000 ₽]
    *[0] 1000 ₽
    }
btn-manual-input = ✏️ Manual Input
btn-commission-free = { $selected ->
    [1] [🆓 Free]
    *[0] 🆓 Free
    }
btn-commission-cancel = ❌ Cancel
btn-commission-accept = ✅ Accept

# Transfer commission - Percentage values
btn-commission-1 = { $selected ->
    [1] [1%]
    *[0] 1%
    }
btn-commission-2 = { $selected ->
    [1] [2%]
    *[0] 2%
    }
btn-commission-3 = { $selected ->
    [1] [3%]
    *[0] 3%
    }
btn-commission-4 = { $selected ->
    [1] [4%]
    *[0] 4%
    }
btn-commission-5 = { $selected ->
    [1] [5%]
    *[0] 5%
    }
btn-commission-6 = { $selected ->
    [1] [6%]
    *[0] 6%
    }
btn-commission-7 = { $selected ->
    [1] [7%]
    *[0] 7%
    }
btn-commission-8 = { $selected ->
    [1] [8%]
    *[0] 8%
    }
btn-commission-9 = { $selected ->
    [1] [9%]
    *[0] 9%
    }
btn-commission-10 = { $selected ->
    [1] [10%]
    *[0] 10%
    }
btn-commission-11 = { $selected ->
    [1] [11%]
    *[0] 11%
    }
btn-commission-12 = { $selected ->
    [1] [12%]
    *[0] 12%
    }
btn-commission-13 = { $selected ->
    [1] [13%]
    *[0] 13%
    }
btn-commission-14 = { $selected ->
    [1] [14%]
    *[0] 14%
    }
btn-commission-15 = { $selected ->
    [1] [15%]
    *[0] 15%
    }
btn-commission-16 = { $selected ->
    [1] [16%]
    *[0] 16%
    }
btn-commission-17 = { $selected ->
    [1] [17%]
    *[0] 17%
    }
btn-commission-18 = { $selected ->
    [1] [18%]
    *[0] 18%
    }
btn-commission-19 = { $selected ->
    [1] [19%]
    *[0] 19%
    }
btn-commission-20 = { $selected ->
    [1] [20%]
    *[0] 20%
    }
btn-commission-25 = { $selected ->
    [1] [25%]
    *[0] 25%
    }
btn-commission-30 = { $selected ->
    [1] [30%]
    *[0] 30%
    }
btn-commission-35 = { $selected ->
    [1] [35%]
    *[0] 35%
    }
btn-commission-40 = { $selected ->
    [1] [40%]
    *[0] 40%
    }
btn-commission-45 = { $selected ->
    [1] [45%]
    *[0] 45%
    }
btn-commission-50-percent = { $selected ->
    [1] [50%]
    *[0] 50%
    }
btn-commission-55 = { $selected ->
    [1] [55%]
    *[0] 55%
    }
btn-commission-60 = { $selected ->
    [1] [60%]
    *[0] 60%
    }
btn-commission-65 = { $selected ->
    [1] [65%]
    *[0] 65%
    }
btn-commission-70 = { $selected ->
    [1] [70%]
    *[0] 70%
    }
btn-commission-75 = { $selected ->
    [1] [75%]
    *[0] 75%
    }
btn-commission-80 = { $selected ->
    [1] [80%]
    *[0] 80%
    }
btn-commission-85 = { $selected ->
    [1] [85%]
    *[0] 85%
    }
btn-commission-90 = { $selected ->
    [1] [90%]
    *[0] 90%
    }
btn-commission-95 = { $selected ->
    [1] [95%]
    *[0] 95%
    }
btn-commission-100 = { $selected ->
    [1] [100%]
    *[0] 100%
    }

# Transfer commission - Fixed values
btn-commission-50-rub = { $selected ->
    [1] [50 ₽]
    *[0] 50 ₽
    }
btn-commission-100-rub = { $selected ->
    [1] [100 ₽]
    *[0] 100 ₽
    }
btn-commission-150-rub = { $selected ->
    [1] [150 ₽]
    *[0] 150 ₽
    }
btn-commission-200-rub = { $selected ->
    [1] [200 ₽]
    *[0] 200 ₽
    }
btn-commission-250-rub = { $selected ->
    [1] [250 ₽]
    *[0] 250 ₽
    }
btn-commission-300-rub = { $selected ->
    [1] [300 ₽]
    *[0] 300 ₽
    }
btn-commission-350-rub = { $selected ->
    [1] [350 ₽]
    *[0] 350 ₽
    }
btn-commission-400-rub = { $selected ->
    [1] [400 ₽]
    *[0] 400 ₽
    }
btn-commission-450-rub = { $selected ->
    [1] [450 ₽]
    *[0] 450 ₽
    }
btn-commission-500-rub = { $selected ->
    [1] [500 ₽]
    *[0] 500 ₽
    }
btn-commission-550-rub = { $selected ->
    [1] [550 ₽]
    *[0] 550 ₽
    }
btn-commission-600-rub = { $selected ->
    [1] [600 ₽]
    *[0] 600 ₽
    }
btn-commission-650-rub = { $selected ->
    [1] [650 ₽]
    *[0] 650 ₽
    }
btn-commission-700-rub = { $selected ->
    [1] [700 ₽]
    *[0] 700 ₽
    }
btn-commission-750-rub = { $selected ->
    [1] [750 ₽]
    *[0] 750 ₽
    }
btn-commission-800-rub = { $selected ->
    [1] [800 ₽]
    *[0] 800 ₽
    }
btn-commission-850-rub = { $selected ->
    [1] [850 ₽]
    *[0] 850 ₽
    }
btn-commission-900-rub = { $selected ->
    [1] [900 ₽]
    *[0] 900 ₽
    }
btn-commission-950-rub = { $selected ->
    [1] [950 ₽]
    *[0] 950 ₽
    }
btn-commission-1000-rub = { $selected ->
    [1] [1000 ₽]
    *[0] 1000 ₽
    }

# Transfer min and max amounts
btn-amount-no-limit = { $selected ->
    [1] [🔓 No Limit]
    *[0] 🔓 No Limit
    }
btn-amount-10 = { $selected ->
    [1] [10 ₽]
    *[0] 10 ₽
    }
btn-amount-50 = { $selected ->
    [1] [50 ₽]
    *[0] 50 ₽
    }
btn-amount-100 = { $selected ->
    [1] [100 ₽]
    *[0] 100 ₽
    }
btn-amount-500 = { $selected ->
    [1] [500 ₽]
    *[0] 500 ₽
    }
btn-amount-1000 = { $selected ->
    [1] [1000 ₽]
    *[0] 1000 ₽
    }
btn-amount-5000 = { $selected ->
    [1] [5000 ₽]
    *[0] 5000 ₽
    }
btn-amount-10000 = { $selected ->
    [1] [10000 ₽]
    *[0] 10000 ₽
    }
btn-amount-50000 = { $selected ->
    [1] [50000 ₽]
    *[0] 50000 ₽
    }
btn-amount-100000 = { $selected ->
    [1] [100000 ₽]
    *[0] 100000 ₽
    }
btn-amount-500000 = { $selected ->
    [1] [500000 ₽]
    *[0] 500000 ₽
    }
btn-amount-cancel = ❌ Cancel
btn-amount-accept = ✅ Accept


# Bonus activation
btn-bonus-activate-all = { $selected ->
    [true] [Activate All ({ $referral_balance } ₽)]
    *[other] Activate All ({ $referral_balance } ₽)
}
btn-bonus-amount-100 = { $selected ->
    [true] [100 ₽]
    *[other] 100 ₽
}
btn-bonus-amount-200 = { $selected ->
    [true] [200 ₽]
    *[other] 200 ₽
}
btn-bonus-amount-300 = { $selected ->
    [true] [300 ₽]
    *[other] 300 ₽
}
btn-bonus-amount-500 = { $selected ->
    [true] [500 ₽]
    *[other] 500 ₽
}
btn-bonus-amount-750 = { $selected ->
    [true] [750 ₽]
    *[other] 750 ₽
}
btn-bonus-amount-1000 = { $selected ->
    [true] [1000 ₽]
    *[other] 1000 ₽
}
btn-bonus-amount-1500 = { $selected ->
    [true] [1500 ₽]
    *[other] 1500 ₽
}
btn-bonus-amount-2000 = { $selected ->
    [true] [2000 ₽]
    *[other] 2000 ₽
}
btn-bonus-amount-2500 = { $selected ->
    [true] [2500 ₽]
    *[other] 2500 ₽
}


# Statistics
btn-statistics-page =
    { $target_page1 ->
    [1] 👥
    [2] 🧾
    [3] 💳
    [4] 📦
    [5] 🎁
    [6] 👪
    *[OTHER] page
    }

btn-statistics-current-page =
    { $current_page1 ->
    [1] [👥]
    [2] [🧾]
    [3] [💳]
    [4] [📦]
    [5] [🎁]
    [6] [👪]
    *[OTHER] [page]
    }


# Users
btn-users-search = 🔍 Search User
btn-users-recent-registered = 🆕 Recently Registered
btn-users-recent-activity = 📝 Recently Active
btn-users-all = 👥 All Users
btn-users-blacklist = 🚫 Blacklist
btn-users-unblock-all = 🔓 Unblock All


# User
btn-user-discount = 💸 Permanent Discount
btn-user-points = 💰 Change Balance
btn-user-main-balance = 💰 Main Balance
btn-user-referral-balance = 🎁 Bonus Balance
btn-user-balance = 💳 Finances
btn-user-subscription = 📋 Subscription
btn-user-statistics = 📊 Statistics
btn-user-message = 📩 Send Message
btn-user-role = 👮‍♂️ Change Role
btn-user-transactions = 🧾 Payments
btn-user-give-access = 🔑 Plan Access
btn-user-current-subscription = 💳 Current Subscription
btn-user-change-subscription = 🎁 Change Subscription
btn-user-subscription-traffic-limit = 🌐 Traffic Limit
btn-user-subscription-device-limit = 📱 Add Devices
btn-user-subscription-expire-time = ⏳ Expiration Time
btn-user-subscription-squads = 🔗 Squads
btn-user-subscription-traffic-reset = 🔄 Reset Traffic
btn-user-subscription-devices = 🧾 Device List
btn-user-subscription-url = 📋 Copy Link
btn-user-subscription-set = ✅ Set Subscription
btn-user-subscription-delete = ❌ Delete
btn-user-message-preview = 👀 Preview
btn-user-message-confirm = ✅ Send
btn-user-sync = 🌀 Synchronize
btn-user-sync-remnawave = 🌊 Use Remnawave Data
btn-user-sync-remnashop = 🛍 Use DFC Shop Data
btn-user-give-subscription = 🎁 Give Subscription
btn-user-subscription-internal-squads = ⏺️ Internal Squads
btn-user-subscription-external-squads = ⏹️ External Squad

btn-user-allowed-plan-choice = { $selected ->
    [1] 🔘
    *[0] ⚪
    } { $plan_name }

btn-user-subscription-active-toggle = { $is_active ->
    [1] 🔴 Disable
    *[0] 🟢 Enable
    }

btn-user-transaction = { $status ->
    [PENDING] 🕓
    [COMPLETED] ✅
    [CANCELED] ❌
    [REFUNDED] 💸
    [FAILED] ⚠️
    *[OTHER] { $status }
} { $created_at }

btn-user-block = { $is_blocked ->
    [1] 🔓 Unblock
    *[0] 🔒 Block
    }

btn-user-referrals = 👥 Referrals
btn-user-referrals-list = 📋 Referral List
btn-user-referral-item = { $telegram_id } ({ $name }) | { $total_spent } ₽
btn-user-referral-bind = 🔗 Bind Referral
btn-user-delete = ❌ Delete User


# Broadcast
btn-broadcast-list = 📄 All Broadcasts List
btn-broadcast-all = 👥 To Everyone
btn-broadcast-plan = 📦 By Plan
btn-broadcast-subscribed = ✅ With Subscription
btn-broadcast-unsubscribed = ❌ Without Subscription
btn-broadcast-expired = ⌛ Expired
btn-broadcast-trial = ✳️ With Trial
btn-broadcast-content = ✉️ Edit Content
btn-broadcast-buttons = ✳️ Edit Buttons
btn-broadcast-preview = 👀 Preview
btn-broadcast-confirm = ✅ Start Broadcast
btn-broadcast-refresh = 🔄 Refresh Data
btn-broadcast-viewing = 👀 View
btn-broadcast-cancel = ⛔ Stop Broadcast
btn-broadcast-delete = ❌ Delete Sent

btn-broadcast-button-choice = { $selected ->
    [1] 🔘
    *[0] ⚪
    }

btn-broadcast =  { $status ->
    [PROCESSING] ⏳
    [COMPLETED] ✅
    [CANCELED] ⛔
    [DELETED] ❌
    [ERROR] ⚠️
    *[OTHER] { $status }
} { $created_at }


# Go to
btn-goto-subscription = 💳 Buy Subscription
btn-goto-promocode = 🎟 Activate Promo Code
btn-goto-invite = 👥 Invite
btn-goto-subscription-renew = 🔄 Renew Subscription
btn-goto-user-profile = 👤 Go to User


# Promocodes
btn-promocodes-list = 📃 Promo Code List
btn-promocodes-search = 🔍 Search Promo Code
btn-promocodes-create = 🆕 Create
btn-promocodes-delete = 🗑️ Delete
btn-promocodes-edit = ✏️ Edit


# Access
btn-access-mode = { access-mode }

btn-access-purchases-toggle = { $enabled ->
    [1] 🔘
    *[0] ⚪
    } Purchases

btn-access-registration-toggle = { $enabled ->
    [1] 🔘
    *[0] ⚪
    } Registration

btn-access-conditions = ⚙️ Access Conditions
btn-access-rules = ✳️ Rules Acceptance
btn-access-channel = ❇️ Channel Subscription

btn-access-condition-toggle = { $enabled ->
    [1] 🔘 Enabled
    *[0] ⚪ Disabled
    }

# Features
feature-community = Community
feature-tos = Agreement
feature-balance = Balance
feature-extra-devices = Extra Devices
feature-transfers = Transfers


# RemnaShop
btn-remnashop-admins = 👮‍♂️ Administrators
btn-remnashop-gateways = 🌐 Payment Systems
btn-remnashop-referral = 👥 Referral System
btn-remnashop-advertising = 🎯 Advertising
btn-remnashop-plans = 📦 Plans
btn-remnashop-notifications = 🔔 Notifications
btn-remnashop-logs = 📄 Logs
btn-remnashop-audit = 🔍 Audit
btn-remnashop-extra-devices = 📱 Extra Devices


# Gateways
btn-gateway-title = { gateway-type }
btn-gateways-setting = { $field }
btn-gateways-webhook-copy = 📋 Copy Webhook

btn-gateway-active = { $is_active ->
    [1] 🟢 Enabled
    *[0] 🔴 Disabled
    }

btn-gateway-test = 🐞 Test
btn-gateways-default-currency = 💸 Default Currency
btn-gateways-placement = 🔢 Change Positioning

btn-gateways-default-currency-choice = { $enabled -> 
    [1] 🔘
    *[0] ⚪
    } { $symbol } { $currency }


# Referral
btn-referral-level = 🔢 Level
btn-referral-reward-type = 🎀 Reward Type
btn-referral-accrual-strategy = 📍 Accrual Condition
btn-referral-reward-strategy = ⚖️ Accrual Method
btn-referral-reward = 🎁 Reward
btn-referral-invite-message = ✉️ Invitation Settings
btn-reset-default = 🔄 Reset to Default
btn-invite-edit = ✏️ Edit Content
btn-invite-preview = 👁 Preview
btn-invite-close-preview = ❌ Close

btn-referral-enable = { $is_enable -> 
    [1] 🟢 Enabled
    *[0] 🔴 Disabled
    }

# Level buttons with radio toggle
btn-referral-level-one = { $selected ->
    [1] 🔘 One Level
    *[0] ⚪ One Level
    }

btn-referral-level-two = { $selected ->
    [1] 🔘 Two Levels
    *[0] ⚪ Two Levels
    }

# Editable level toggle buttons in reward menu
btn-reward-level-one = { $selected ->
    [1] 🔘 First Level
    *[0] ⚪ First Level
    }

btn-reward-level-two = { $selected ->
    [1] 🔘 Second Level
    *[0] ⚪ Second Level
    }

# Reward type buttons with radio toggle
btn-referral-type-money = { $selected ->
    [1] 🔘 Money
    *[0] ⚪ Money
    }

btn-referral-type-days = { $selected ->
    [1] 🔘 Days
    *[0] ⚪ Days
    }

# Accrual condition buttons with radio toggle
btn-referral-accrual-first = { $selected ->
    [1] 🔘 First Payment
    *[0] ⚪ First Payment
    }

btn-referral-accrual-each = { $selected ->
    [1] 🔘 Each Payment
    *[0] ⚪ Each Payment
    }

# Accrual method buttons with radio toggle
btn-referral-strategy-fixed = { $selected ->
    [1] 🔘 Fixed
    *[0] ⚪ Fixed
    }

btn-referral-strategy-percent = { $selected ->
    [1] 🔘 Percentage
    *[0] ⚪ Percentage
    }

# "No Reward" button
btn-reward-free = { $selected ->
    [1] [ No Reward ]
    *[0] No Reward
    }

# Reward buttons for percentage (commission style)
btn-reward-5 = { $selected ->
    [1] [ 5% ]
    *[0] 5%
    }
btn-reward-10 = { $selected ->
    [1] [ 10% ]
    *[0] 10%
    }
btn-reward-15 = { $selected ->
    [1] [ 15% ]
    *[0] 15%
    }
btn-reward-20 = { $selected ->
    [1] [ 20% ]
    *[0] 20%
    }
btn-reward-25 = { $selected ->
    [1] [ 25% ]
    *[0] 25%
    }
btn-reward-30 = { $selected ->
    [1] [ 30% ]
    *[0] 30%
    }
btn-reward-35 = { $selected ->
    [1] [ 35% ]
    *[0] 35%
    }
btn-reward-40 = { $selected ->
    [1] [ 40% ]
    *[0] 40%
    }
btn-reward-45 = { $selected ->
    [1] [ 45% ]
    *[0] 45%
    }
btn-reward-50 = { $selected ->
    [1] [ 50% ]
    *[0] 50%
    }

# Reward buttons for fixed amounts (commission style)
btn-reward-fixed-10 = { $selected ->
    [1] [ 10{ $suffix } ]
    *[0] 10{ $suffix }
    }
btn-reward-fixed-20 = { $selected ->
    [1] [ 20{ $suffix } ]
    *[0] 20{ $suffix }
    }
btn-reward-fixed-30 = { $selected ->
    [1] [ 30{ $suffix } ]
    *[0] 30{ $suffix }
    }
btn-reward-fixed-50 = { $selected ->
    [1] [ 50{ $suffix } ]
    *[0] 50{ $suffix }
    }
btn-reward-fixed-100 = { $selected ->
    [1] [ 100{ $suffix } ]
    *[0] 100{ $suffix }
    }
btn-reward-fixed-150 = { $selected ->
    [1] [ 150{ $suffix } ]
    *[0] 150{ $suffix }
    }
btn-reward-fixed-200 = { $selected ->
    [1] [ 200{ $suffix } ]
    *[0] 200{ $suffix }
    }
btn-reward-fixed-250 = { $selected ->
    [1] [ 250{ $suffix } ]
    *[0] 250{ $suffix }
    }
btn-reward-fixed-300 = { $selected ->
    [1] [ 300{ $suffix } ]
    *[0] 300{ $suffix }
    }
btn-reward-fixed-500 = { $selected ->
    [1] [ 500{ $suffix } ]
    *[0] 500{ $suffix }
    }

# Reward buttons for days (Extra days)
btn-reward-days-1 = { $selected ->
    [1] [ 1 ]
    *[0] 1
    }
btn-reward-days-2 = { $selected ->
    [1] [ 2 ]
    *[0] 2
    }
btn-reward-days-3 = { $selected ->
    [1] [ 3 ]
    *[0] 3
    }
btn-reward-days-4 = { $selected ->
    [1] [ 4 ]
    *[0] 4
    }
btn-reward-days-5 = { $selected ->
    [1] [ 5 ]
    *[0] 5
    }
btn-reward-days-6 = { $selected ->
    [1] [ 6 ]
    *[0] 6
    }
btn-reward-days-7 = { $selected ->
    [1] [ 7 ]
    *[0] 7
    }
btn-reward-days-8 = { $selected ->
    [1] [ 8 ]
    *[0] 8
    }
btn-reward-days-9 = { $selected ->
    [1] [ 9 ]
    *[0] 9
    }
btn-reward-days-10 = { $selected ->
    [1] [ 10 ]
    *[0] 10
    }
btn-reward-days-11 = { $selected ->
    [1] [ 11 ]
    *[0] 11
    }
btn-reward-days-12 = { $selected ->
    [1] [ 12 ]
    *[0] 12
    }
btn-reward-days-13 = { $selected ->
    [1] [ 13 ]
    *[0] 13
    }
btn-reward-days-14 = { $selected ->
    [1] [ 14 ]
    *[0] 14
    }
btn-reward-days-15 = { $selected ->
    [1] [ 15 ]
    *[0] 15
    }

# Old buttons (kept for compatibility)
btn-referral-level-choice = { $type -> 
    [1] 1️⃣
    [2] 2️⃣
    [3] 3️⃣
    *[OTHER] { $type }
    }

btn-referral-reward-choice = { $type -> 
    [POINTS] 💎 Points
    [EXTRA_DAYS] ⏳ Days
    [MONEY] 💰 Money
    *[OTHER] { $type }
    }

btn-referral-accrual-strategy-choice = { $type -> 
    [ON_FIRST_PAYMENT] 💳 First Payment
    [ON_EACH_PAYMENT] 💸 Each Payment
    *[OTHER] { $type }
    }

btn-referral-reward-strategy-choice = { $type -> 
    [AMOUNT] 🔸 Fixed
    [PERCENT] 🔹 Percentage
    *[OTHER] { $type }
    }


# Notifications
btn-notifications-user = 👥 User Notifications

btn-notifications-user-choice = { $enabled ->
    [1] 🔘
    *[0] ⚪
    } { $type ->
    [EXPIRES_IN_3_DAYS] Subscription Expiring (3 days)
    [EXPIRES_IN_2_DAYS] Subscription Expiring (2 days)
    [EXPIRES_IN_1_DAYS] Subscription Expiring (1 day)
    [EXPIRED] Subscription Expired
    [LIMITED] Traffic Exhausted
    [EXPIRED_1_DAY_AGO] Subscription Expired (1 day)
    [REFERRAL_ATTACHED] Referral Attached
    [REFERRAL_REWARD] Reward Received
    *[OTHER] { $type }
    }

btn-notifications-system = ⚙️ System Notifications

btn-notifications-system-choice = { $enabled -> 
    [1] 🔘
    *[0] ⚪
    } { $type ->
    [BOT_LIFETIME] Bot Lifecycle
    [BOT_UPDATE] Bot Updates
    [USER_REGISTERED] User Registration
    [SUBSCRIPTION] Subscription Purchase
    [PROMOCODE_ACTIVATED] Promo Code Activation
    [TRIAL_GETTED] Trial Received
    [NODE_STATUS] Node Status
    [USER_FIRST_CONNECTED] First Connection
    [USER_HWID] User Devices
    [BILLING] Financial Operations
    [BALANCE_TRANSFER] Financial Transfers
    *[OTHER] { $type }
    }


# Plans
btn-plans-statistics = 📊 Statistics
btn-plans-create = 🆕 Create
btn-plan-save = ✅ Save
btn-plan-create = ✅ Create Plan
btn-plan-delete = ❌ Delete
btn-plan-name = 🏷️ Name
btn-plan-description = 💬 Description
btn-plan-description-remove = ❌ Remove Current Description
btn-plan-tag = 📌 Tag
btn-plan-tag-remove = ❌ Remove Current Tag
btn-plan-type = 🔖 Type
btn-plan-availability = ✴️ Access
btn-plan-durations-prices = 💰 Pricing
btn-plan-traffic = 🌐 Traffic
btn-plan-devices = 📱 Devices
btn-plan-allowed = 👥 Allowed Users
btn-plan-squads = 🔗 Squads
btn-plan-internal-squads = ⏺️ Internal Squads
btn-plan-external-squads = ⏹️ External Squad
btn-allowed-user = { $id }
btn-plan-duration-add = 🆕 Add
btn-plan-price-choice = 💸 { $price } { $currency }

btn-plan = { $is_active ->
    [1] 🟢
    *[0] 🔴 
    } { $name }

btn-plan-active = { $is_active -> 
    [1] 🟢 Enabled
    *[0] 🔴 Disabled
    }

btn-plan-type-choice = { $type -> 
    [TRAFFIC] 🌐 Traffic
    [DEVICES] 📱 Devices
    [BOTH] 🔗 Traffic + Devices
    [UNLIMITED] ♾️ Unlimited
    *[OTHER] { $type }
    }

btn-plan-type-radio = { $selected ->
    [1] 🔘 { $type ->
        [TRAFFIC] 🌐 Traffic
        [DEVICES] 📱 Devices
        [BOTH] 🔗 Traffic + Devices
        [UNLIMITED] ♾️ Unlimited
        *[OTHER] { $type }
        }
    *[0] ⚪ { $type ->
        [TRAFFIC] 🌐 Traffic
        [DEVICES] 📱 Devices
        [BOTH] 🔗 Traffic + Devices
        [UNLIMITED] ♾️ Unlimited
        *[OTHER] { $type }
        }
    }

btn-plan-availability-choice = { $type -> 
    [ALL] 🌍 For Everyone
    [NEW] 🌱 For New Users
    [EXISTING] 👥 For Existing Customers
    [INVITED] ✉️ For Invited Users
    [ALLOWED] 🔐 For Allowed Users
    [TRIAL] 🎁 For Trial
    *[OTHER] { $type }
    }

btn-plan-availability-radio = { $selected ->
    [1] 🔘 { $type ->
        [ALL] 🌍 For Everyone
        [NEW] 🌱 For New Users
        [EXISTING] 👥 For Existing Customers
        [INVITED] ✉️ For Invited Users
        [ALLOWED] 🔐 For Allowed Users
        [TRIAL] 🎁 For Trial
        *[OTHER] { $type }
        }
    *[0] ⚪ { $type ->
        [ALL] 🌍 For Everyone
        [NEW] 🌱 For New Users
        [EXISTING] 👥 For Existing Customers
        [INVITED] ✉️ For Invited Users
        [ALLOWED] 🔐 For Allowed Users
        [TRIAL] 🎁 For Trial
        *[OTHER] { $type }
        }
    }

btn-plan-traffic-strategy-choice = { $selected ->
    [1] 🔘 { traffic-strategy }
    *[0] ⚪ { traffic-strategy }
    }

btn-plan-duration = ⌛ { $value ->
    [-1] { unlimited }
    *[other] { unit-day }
    }

btn-keep-current-duration = ⏸️ Keep Duration ({ $remaining })


# RemnaWave
btn-remnawave-users = 👥 Users
btn-remnawave-hosts = 🌐 Hosts
btn-remnawave-nodes = 🖥️ Nodes
btn-remnawave-inbounds = 🔌 Inbounds


# Importer
btn-importer-from-xui = 💩 Import from 3X-UI Panel
btn-importer-from-xui-shop = 🛒 3xui-shop Bot
btn-importer-sync = 🌀 From Panel to Bot
btn-importer-sync-bot-to-panel = 📤 From Telegram to Panel
btn-importer-squads = 🔗 Internal Squads
btn-importer-import-all = ✅ Import All
btn-importer-import-active = ❇️ Import Active


# Subscription
btn-subscription-new = 💸 Buy Subscription
btn-subscription-buy = 🛒 Buy Subscription
btn-subscription-renew = 🔄 Renew
btn-subscription-change = 🔃 Change
btn-subscription-referral = 📢 Referral Subscription
btn-subscription-upgrade-referral = 📢 Upgrade to Referral
btn-subscription-promocode = 🎟 Activate Promo Code
btn-subscription-payment-method = 
    { $gateway_type ->
    [BALANCE] 💰 From Balance
    [YOOMONEY] 💳 YooMoney
    [YOOKASSA] 💳 YooKassa
    [TELEGRAM_STARS] ⭐ Telegram Stars
    [CRYPTOMUS] 🔐 Cryptomus
    [HELEKET] 💎 Heleket
    [CRYPTOPAY] 🪙 Cryptopay
    [ROBOKASSA] 💳 Robokassa
    *[OTHER] { $gateway_type }
    } | { $has_discount ->
        [1] { $price } ({ $original_price })
        *[0] { $price }
    }
btn-subscription-pay = ✅ Confirm Payment
btn-subscription-confirm-balance = ✅ Confirm Payment
btn-subscription-get = 🎁 Get Free
btn-subscription-back-plans = ⬅️ Back to Plan Selection
btn-subscription-back-duration = ⬅️ Back
btn-subscription-back-payment-method = ⬅️ Change Payment Method
btn-subscription-connect = 🚀 Connect
btn-subscription-duration = { $final_amount -> 
    [0] { $period } | 🎁
    *[HAS] { $has_discount ->
        [1] { $period } | { $final_amount } ({ $original_amount })
        *[0] { $period } | { $final_amount }
        }
    }

# Extra device duration buttons
btn-add-device-duration-full = End of Subscription ({ $days } d.) | { $price } ₽
btn-add-device-duration-month = End of Period ({ $days } d.) | { $price } ₽
btn-add-device-duration-months-1 = 1 Month (30 d.) | { $price } ₽
btn-add-device-duration-months-3 = 3 Months (90 d.) | { $price } ₽
btn-add-device-duration-months-6 = 6 Months (180 d.) | { $price } ₽
btn-add-device-duration-months-12 = 12 Months (365 d.) | { $price } ₽


# Promocodes
btn-promocode-code = 🏷️ Code
btn-promocode-name = 📝 Name
btn-promocode-type = 🔖 Type
btn-promocode-availability = ✴️ Access

btn-promocode-active = { $is_active -> 
    [1] ✅ Disable
    *[0] 🔴 Enable
    }

btn-promocode-reward = 🎁 Reward
btn-promocode-lifetime = ⌛ Lifetime
btn-promocode-allowed = 👥 Allowed Users
btn-promocode-access = 📦 Plan Access
btn-promocode-confirm = ✅ Save
btn-promocode-quantity = 🔢 Quantity
btn-promocode-generate = 🎲 Random Code
btn-lifetime-infinite = Infinite
btn-quantity-infinite = Infinite
btn-manual-input = ✏️ Manual Input

btn-promocode-type-choice = { $selected -> 
    [1] 🔘
    *[0] ⚪
    } { $name }

btn-plan-access-choice = { $selected -> 
    [1] 🔘 { $plan_name }
    *[0] ⚪ { $plan_name }
    }

btn-pay = 💳 Pay

# Devices
btn-device-pending-deletion = ⏳ Deleting
btn-device-marked-for-deletion = ✅ Marked for deletion

# Update snooze
btn-update-now = 🔄 Update now
btn-update-remind-1d = ⏰ In 1 day
btn-update-remind-3d = ⏰ In 3 days
btn-update-remind-7d = ⏰ In 7 days
btn-update-remind-off = 🔕 Don't remind
btn-update-close = ❌ Close
