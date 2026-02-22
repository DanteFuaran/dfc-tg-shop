# Dashboard
btn-dashboard-broadcast = 📢 Рассылка
btn-dashboard-statistics = 📊 Статистика
btn-dashboard-users = 👥 Пользователи
btn-dashboard-plans = 📦 Тарифные планы
btn-dashboard-promocodes = 🎟 Промокоды
btn-dashboard-remnawave = 🌊 Мониторинг панели
btn-dashboard-remnashop = 🛍 Телеграм
btn-dashboard-access = 🔓 Режим доступа
btn-dashboard-features = ⚙️ Функционал
btn-dashboard-importer = 📥 X-UI Импорт
btn-dashboard-bot-management = 🤖 Управление ботом
btn-dashboard-payment-settings = 💳 Настройки платежей
btn-dashboard-user-management = 👥 Пользователи

# Bot Management
btn-bot-check-update = 🔍 Проверить обновления
btn-bot-restart = 🔁 Перезапустить
btn-mirror-bots = 🤖 Дополнительный бот
btn-mirror-bot-add = ➕ Добавить нового бота

# Database Management
btn-dashboard-db = 🗄 Управление БД
btn-db-save = 💾 Сохранить
btn-db-load = 📦 Загрузить
btn-db-close = ❌ Закрыть
btn-db-sync-from-panel = 📥 Remnawave Импорт
btn-db-clear-all = 🗑 Очистить всё
btn-db-clear-users = 👥 Очистить пользователей
btn-db-imports = 📥 Импорт
btn-db-sync = 🔄 Синхронизация
btn-db-remnawave-import = 📥 Remnawave Импорт
btn-db-xui-import = 💩 X-UI Импорт
btn-db-sync-remnawave-to-bot = 📥 Из панели в бота
btn-db-sync-bot-to-remnawave = 📤 Из бота в панель

# Settings
btn-dashboard-settings = ⚙️ Функционал
btn-settings-extra-devices = 📱 Доп. устройства
btn-settings-balance = 💰 Баланс
btn-settings-transfers = 💸 Переводы
btn-settings-notifications = 🔔 Уведомления
btn-settings-access = 🔓 Режим доступа
btn-settings-referral = 👥 Реф. система
btn-settings-promocodes = 🏷️ Промокоды
btn-settings-community = 👥 Сообщество
btn-settings-community-set-url = 📝 Назначить группу
btn-settings-tos = 📜 Соглашение
btn-tos-set-url = Назначить источник
btn-settings-global-discount = 🏷️ Глобальная скидка
btn-settings-finances = 💰 Финансы
btn-settings-currency-rates = 💱 Курс валют
btn-settings-language = 🌐 Язык
btn-language-multilang = { $enabled ->
    [1] 🟢 Мультиязычность
    *[0] 🔴 Мультиязычность
}
btn-language-ru = 🇷🇺 Русский
btn-language-uk = 🇺🇦 Українська
btn-language-en = 🇬🇧 English
btn-language-de = 🇩🇪 Deutsch
btn-language-cancel = ❌ Отмена
btn-language-apply = ✅ Принять
btn-finances-sync = { $enabled ->
    [1] 🟢 Синхронизация курса
    *[0] 🔴 Синхронизация курса
    }
btn-finances-currency-rates = 💱 Курс валют
btn-finances-gateways = 🌐 Платежные системы
btn-balance-mode-combined = { $selected ->
    [1] 🔘 Сумма
    *[0] ⚪ Сумма
    }
btn-balance-mode-separate = { $selected ->
    [1] 🔘 Раздельно
    *[0] ⚪ Раздельно
    }
btn-currency-auto-toggle = { $enabled ->
    [1] 🟢 Автоматически
    *[0] 🔴 Автоматически
    }
btn-settings-toggle = { $enabled ->
    [1] 🟢
    *[0] 🔴
    }
btn-toggle-setting = { $name }: { $enabled ->
    [1] ✅ Включены
    *[0] 🔴 Выключены
    }
btn-setting-value = { $name }: { $value }
btn-commission-type-percent = 
    { $selected ->
    [1] 🔘 Процентная
    *[0] ⚪ Процентная
    }
btn-commission-type-fixed = 
    { $selected ->
    [1] 🔘 Фиксированная
    *[0] ⚪ Фиксированная
    }
btn-commission-value = 💵 Комиссия: { $value } { $unit }

unit-percent-or-rub = { $commission_type ->
    [percent] %
    *[fixed] ₽
    }

# Глобальная скидка
btn-discount-type-percent = 
    { $selected ->
    [1] 🔘 Процентная
    *[0] ⚪ Процентная
    }
btn-discount-type-fixed = 
    { $selected ->
    [1] 🔘 Фиксированная
    *[0] ⚪ Фиксированная
    }
btn-discount-value = 🏷️ Скидка: { $value } { $unit }

unit-discount-percent-or-rub = { $discount_type ->
    [percent] %
    *[fixed] ₽
    }

# Режим складывания скидок
btn-global-discount-mode = ⚙️ Режим
btn-global-discount-apply-to = 📌 Влияние

# Режимы в подменю (радиокнопки)
btn-discount-mode-max = { $selected ->
    [1] 🔘 Максимальная
    *[0] ⚪ Максимальная
    }
btn-discount-mode-stack = { $selected ->
    [1] 🔘 Сложенная
    *[0] ⚪ Сложенная
    }

# На что влияет скидка (чекбоксы)
btn-apply-to-subscription = { $enabled ->
    [1] ✅ Подписка
    *[0] ⬜ Подписка
    }
btn-apply-to-extra-devices = { $enabled ->
    [1] ✅ Доп.устройства
    *[0] ⬜ Доп.устройства
    }
btn-apply-to-transfer-commission = { $enabled ->
    [1] ✅ Комиссия переводов
    *[0] ⬜ Комиссия переводов
    }

btn-discount-free = { $selected ->
    [1] [🚫 Нет скидки]
    *[0] 🚫 Нет скидки
    }

# Скидка - Процентные значения
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

# Скидка - Фиксированные значения (рубли)
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
btn-back = ⬅️ Назад
btn-main-menu = 🏠 Главное меню
btn-back-main-menu = 🏠 Главное меню
btn-back-dashboard = ⚙️ Панель управления
btn-back-users = 👥 Пользователи
btn-done = ✅ Готово


# Телеграм
btn-remnashop-release-latest = 👀 Посмотреть
btn-remnashop-how-upgrade = ❓ Как обновить
btn-remnashop-github = ⭐ GitHub
btn-remnashop-telegram = 👪 Telegram
btn-remnashop-donate = 💰 Поддержать разработчика
btn-remnashop-guide = ❓ Инструкция


# Other
btn-rules-accept = ✅ Принять правила
btn-channel-join = ❤️ Перейти в канал
btn-channel-confirm = ✅ Подтвердить
btn-notification-close = ❌ Закрыть
btn-notification-close-success = ✅ Закрыть
btn-goto-main-menu = 🏠 В главное меню
btn-contact-support = 📩 Перейти в поддержку
btn-cancel = ❌ Отмена
btn-accept = ✅ Принять
btn-confirm = ✅ Подтвердить
btn-confirm-payment = ✅ Подтвердить оплату
btn-select-all = 📋 Все подписки
btn-select-all-toggle =
    { $all_selected ->
    [1] ✅ Все подписки
    *[0] ⬜ Все подписки
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
btn-menu-connect = 🚀 Подключиться
btn-menu-connect-open = 🔗 Подключиться
btn-menu-connect-subscribe = 📄 Страница подписки
btn-menu-connect-qr = 📱 QR Код
btn-menu-connect-key = 🔑 Показать ключ
btn-menu-download = 📥 Скачать приложение
btn-menu-download-android = 📱 Android
btn-menu-download-windows = 🖥 Windows
btn-menu-download-iphone = 🍎 iPhone
btn-menu-download-macos = 💻 macOS

btn-menu-connect-not-available = 🚀 Подключиться

btn-menu-trial = { $is_referral_trial ->
    [1] 📢 Реферальная подписка
    *[0] 🎁 Пробная подписка
    }
btn-menu-devices = 📱 Мои устройства
btn-menu-devices-empty = ⚠️ Нет привязанных устройств
btn-menu-add-device = ➕ Увеличить лимит устройств
btn-menu-extra-devices = 📱 Управление доп. устройствами
btn-extra-device-item = { $device_count } шт. • { $price } ₽/мес • { $expires_at }
btn-extra-device-disable-auto-renew = ❌ Отключить автопродление
btn-extra-device-delete = 🗑 Удалить сейчас
btn-menu-try-free = 🎁 Попробовать бесплатно
btn-menu-balance = 💰 Баланс: { $balance }
btn-menu-subscription = 💳 Подписка
btn-menu-connect-subscribe = 🔗 Подключиться
btn-menu-topup = ➕ Пополнить
btn-menu-invite = 👥 Пригласить
btn-menu-invite-about = ❓ Подробнее о наградах
btn-menu-invite-copy = 🔗 Ссылка приглашения
btn-menu-invite-send = 📩 Пригласить
btn-menu-invite-qr = 🧾 QR-код
btn-menu-invite-withdraw-points = 💰 Вывести баланс
btn-menu-invite-withdraw-balance = 💸 Активировать бонусы
btn-menu-promocode = 🎟 Промокод
btn-menu-support = 🆘 Помощь
btn-menu-tos = 📋 Соглашение
btn-menu-community = 👥 Сообщество
btn-menu-dashboard = 🧰 Панель управления

# Balance
btn-balance-topup = ➕ Пополнить
btn-balance-withdraw = ➖ Вывести
btn-balance-transfer = 💸 Перевести
btn-balance-gateway = 
    { $gateway_type ->
    [YOOMONEY] 💳 ЮMoney
    [YOOKASSA] 💳 ЮKassa
    [CRYPTOMUS] 🔐 Cryptomus
    [HELEKET] 💎 Heleket
    [TELEGRAM_STARS] ⭐ Телеграм
    *[OTHER] 💳 { $gateway_type }
    }

# Subscription Key
btn-subscription-key-close = ❌ Закрыть
btn-balance-custom-amount = ✏️ Своя сумма
btn-balance-pay = ✅ Оплатить
btn-balance-transfer-recipient = 👤 Получатель
btn-balance-transfer-amount = 💵 Сумма: { $amount } ₽
btn-balance-transfer-message = 💬 Сообщение
btn-balance-transfer-send = ✅ Отправить
btn-balance-transfer-history = 📜 История пользователей
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
btn-bonus-custom-amount = ✏️ Своя сумма

# Dashboard
btn-dashboard-statistics = 📊 Статистика
btn-dashboard-users = 👥 Пользователи
btn-dashboard-broadcast = 📢 Рассылка
btn-dashboard-promocodes = 🎟 Промокоды
btn-dashboard-access = 🔓 Режим доступа
btn-dashboard-features = ⚙️ Функционал
btn-dashboard-remnawave = 🌊 Мониторинг панели
btn-dashboard-remnashop = 🛍 Телеграм
btn-dashboard-importer = 📥 Импорт пользователей
btn-dashboard-save-db = 💾 Сохранить БД
btn-db-export = 📤 Экспорт
btn-db-import = 📥 Импорт

# Features
btn-feature-toggle =
    { $enabled ->
    [1] ✅ { $name }
    *[0] ⬜ { $name }
    }

btn-extra-devices-menu = 📱 Доп. устройства
btn-extra-devices-price = 💰 Стоимость: { $price } ₽
btn-extra-devices-min-days = ⏳ Минимум дней: { $days }
btn-extra-devices-one-time = 
    { $selected ->
    [1] 🔘 Единоразово
    *[0] ⚪ Единоразово
    }
btn-extra-devices-monthly = 
    { $selected ->
    [1] 🔘 Ежемесячно
    *[0] ⚪ Ежемесячно
    }

# Дни для минимального срока
btn-days-1 = { $selected ->
    [1] [1 день]
    *[0] 1 день
}
btn-days-3 = { $selected ->
    [1] [3 дня]
    *[0] 3 дня
}
btn-days-5 = { $selected ->
    [1] [5 дней]
    *[0] 5 дней
}
btn-days-7 = { $selected ->
    [1] [7 дней]
    *[0] 7 дней
}
btn-days-10 = { $selected ->
    [1] [10 дней]
    *[0] 10 дней
}
btn-days-14 = { $selected ->
    [1] [14 дней]
    *[0] 14 дней
}
btn-days-30 = { $selected ->
    [1] [30 дней]
    *[0] 30 дней
}

# Цены доп. устройств
btn-price-free = { $selected ->
    [1] [Бесплатно]
    *[0] Бесплатно
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
btn-manual-input = ✏️ Ручной ввод
btn-commission-free = { $selected ->
    [1] [🆓 Бесплатно]
    *[0] 🆓 Бесплатно
    }
btn-commission-cancel = ❌ Отмена
btn-commission-accept = ✅ Принять

# Комиссия в переводах - Процентные значения
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

# Комиссия в переводах - Фиксированные значения
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

# Минимум и максимум в переводах
btn-amount-no-limit = { $selected ->
    [1] [🔓 Без ограничений]
    *[0] 🔓 Без ограничений
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
btn-amount-cancel = ❌ Отмена
btn-amount-accept = ✅ Принять


# Бонусы активации
btn-bonus-activate-all = { $selected ->
    [true] [Активировать всё ({ $referral_balance })]
    *[other] Активировать всё ({ $referral_balance })
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
btn-users-search = 🔍 Поиск пользователя
btn-users-recent-registered = 🆕 Последние зарегистрированные
btn-users-recent-activity = 📝 Последние взаимодействующие
btn-users-all = 👥 Все пользователи
btn-users-blacklist = 🚫 Черный список
btn-users-unblock-all = 🔓 Разблокировать всех


# User
btn-user-discount = 💸 Постоянная скидка
btn-user-points = 💰 Изменить баланс
btn-user-main-balance = 💰 Основной баланс
btn-user-referral-balance = 🎁 Бонусный баланс
btn-user-balance = 💳 Финансы
btn-user-subscription = 📋 Подписка
btn-user-statistics = 📊 Статистика
btn-user-message = 📩 Написать сообщение
btn-user-role = 👮‍♂️ Изменить роль
btn-user-transactions = 🧾 Оплаты
btn-user-give-access = 🔑 Доступ к планам
btn-user-current-subscription = 💳 Текущая подписка
btn-user-change-subscription = 🎁 Изменить подписку
btn-user-subscription-traffic-limit = 🌐 Лимит трафика
btn-user-subscription-device-limit = 📱 Добавить устройства
btn-user-subscription-expire-time = ⏳ Время истечения
btn-user-subscription-squads = 🔗 Сквады
btn-user-subscription-traffic-reset = 🔄 Сбросить трафик
btn-user-subscription-devices = 🧾 Список устройств
btn-user-subscription-url = 📋 Скопировать ссылку
btn-user-subscription-set = ✅ Установить подписку
btn-user-subscription-delete = ❌ Удалить
btn-user-message-preview = 👀 Предпросмотр
btn-user-message-confirm = ✅ Отправить
btn-user-sync = 🌀 Синхронизировать
btn-user-sync-remnawave = 🌊 Использовать данные Remnawave
btn-user-sync-remnashop = 🛍 Использовать данные DFC Shop
btn-user-give-subscription = 🎁 Выдать подписку
btn-user-subscription-internal-squads = ⏺️ Внутренние сквады
btn-user-subscription-external-squads = ⏹️ Внешний сквад

btn-user-allowed-plan-choice = { $selected ->
    [1] 🔘
    *[0] ⚪
    } { $plan_name }

btn-user-subscription-active-toggle = { $is_active ->
    [1] 🔴 Выключить
    *[0] 🟢 Включить
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
    [1] 🔓 Разблокировать
    *[0] 🔒 Заблокировать
    }

btn-user-referrals = 👥 Рефералы
btn-user-referrals-list = 📋 Список рефералов
btn-user-referral-item = { $telegram_id } ({ $name }) | { $total_spent } ₽
btn-user-referral-bind = 🔗 Привязать реферала
btn-user-delete = ❌ Удалить пользователя


# Broadcast
btn-broadcast-list = 📄 Список всех рассылок
btn-broadcast-all = 👥 Всем
btn-broadcast-plan = 📦 По плану
btn-broadcast-subscribed = ✅ С подпиской
btn-broadcast-unsubscribed = ❌ Без подписки
btn-broadcast-expired = ⌛ Просроченным
btn-broadcast-trial = ✳️ С пробником
btn-broadcast-content = ✉️ Редактировать содержимое
btn-broadcast-buttons = ✳️ Редактировать кнопки
btn-broadcast-preview = 👀 Предпросмотр
btn-broadcast-confirm = ✅ Запустить рассылку
btn-broadcast-refresh = 🔄 Обновить данные
btn-broadcast-viewing = 👀 Просмотр
btn-broadcast-cancel = ⛔ Остановить рассылку
btn-broadcast-delete = ❌ Удалить отправленное
btn-broadcast-accept = ✅ Принять
btn-broadcast-cancel-edit = Отмена

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
btn-goto-subscription = 💳 Купить подписку
btn-goto-promocode = 🎟 Активировать промокод
btn-goto-invite = 👥 Пригласить
btn-goto-subscription-renew = 🔄 Продлить подписку
btn-goto-user-profile = 👤 Перейти к пользователю


# Promocodes
btn-promocodes-list = 📃 Список промокодов
btn-promocodes-search = 🔍 Поиск промокода
btn-promocodes-create = 🆕 Создать
btn-promocodes-delete = 🗑️ Удалить
btn-promocodes-edit = ✏️ Редактировать


# Access
btn-access-mode = { access-mode }

btn-access-purchases-toggle = { $enabled ->
    [1] 🔘
    *[0] ⚪
    } Покупки

btn-access-registration-toggle = { $enabled ->
    [1] 🔘
    *[0] ⚪
    } Регистрация

btn-access-conditions = ⚙️ Условия доступа
btn-access-rules = ✳️ Принятие правил
btn-access-channel = ❇️ Подписка на канал

btn-access-condition-toggle = { $enabled ->
    [1] 🔘 Включено
    *[0] ⚪ Выключено
    }

# Features
feature-community = Сообщество
feature-tos = Соглашение
feature-balance = Баланс
feature-extra-devices = Доп. устройства
feature-transfers = Переводы


# RemnaShop
btn-remnashop-admins = 👮‍♂️ Администраторы
btn-remnashop-gateways = 🌐 Платежные системы
btn-remnashop-referral = 👥 Реф. система
btn-remnashop-advertising = 🎯 Реклама
btn-remnashop-plans = 📦 Планы
btn-remnashop-notifications = 🔔 Уведомления
btn-remnashop-logs = 📄 Логи
btn-remnashop-audit = 🔍 Аудит
btn-remnashop-extra-devices = 📱 Доп. устройства


# Gateways
btn-gateway-title = { gateway-type }
btn-gateways-setting = { $field }
btn-gateways-webhook-copy = 📋 Скопировать вебхук

btn-gateway-active = { $is_active ->
    [1] 🟢 Включено
    *[0] 🔴 Выключено
    }

btn-gateway-test = 🐞 Тест
btn-gateways-default-currency = 💸 Валюта по умолчанию
btn-gateways-placement = 🔢 Изменить позиционирование

btn-gateways-default-currency-choice = { $enabled -> 
    [1] 🔘
    *[0] ⚪
    } { $symbol } { $currency }


# Referral
btn-referral-level = 🔢 Уровень
btn-referral-reward-type = 🎀 Тип награды
btn-referral-accrual-strategy = 📍 Условие начисления
btn-referral-reward-strategy = ⚖️ Форма начисления
btn-referral-reward = 🎁 Награда
btn-referral-invite-message = ✉️ Настройка приглашения
btn-reset-default = 🔄 Сбросить по умолчанию
btn-invite-edit = ✏️ Редактировать содержимое
btn-invite-preview = 👁 Предпросмотр
btn-invite-close-preview = ❌ Закрыть

btn-referral-enable = { $is_enable -> 
    [1] 🟢 Включена
    *[0] 🔴 Выключена
    }

# Кнопки уровня с радио-переключателем
btn-referral-level-one = { $selected ->
    [1] 🔘 Один уровень
    *[0] ⚪ Один уровень
    }

btn-referral-level-two = { $selected ->
    [1] 🔘 Два уровня
    *[0] ⚪ Два уровня
    }

# Кнопки переключателя редактируемого уровня в меню награды
btn-reward-level-one = { $selected ->
    [1] 🔘 Первый уровень
    *[0] ⚪ Первый уровень
    }

btn-reward-level-two = { $selected ->
    [1] 🔘 Второй уровень
    *[0] ⚪ Второй уровень
    }

# Кнопки типа награды с радио-переключателем
btn-referral-type-money = { $selected ->
    [1] 🔘 Деньги
    *[0] ⚪ Деньги
    }

btn-referral-type-days = { $selected ->
    [1] 🔘 Дни
    *[0] ⚪ Дни
    }

# Кнопки условия начисления с радио-переключателем  
btn-referral-accrual-first = { $selected ->
    [1] 🔘 Первый платеж
    *[0] ⚪ Первый платеж
    }

btn-referral-accrual-each = { $selected ->
    [1] 🔘 Каждый платеж
    *[0] ⚪ Каждый платеж
    }

# Кнопки формы начисления с радио-переключателем
btn-referral-strategy-fixed = { $selected ->
    [1] 🔘 Фиксированная
    *[0] ⚪ Фиксированная
    }

btn-referral-strategy-percent = { $selected ->
    [1] 🔘 Процентная
    *[0] ⚪ Процентная
    }

# Кнопка "Без награды"
btn-reward-free = { $selected ->
    [1] [ Без награды ]
    *[0] Без награды
    }

# Кнопки награды для процентной формы (в стиле комиссии)
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

# Кнопки награды для фиксированной формы (в стиле комиссии)
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

# Кнопки награды для дней (Экстра дни)
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

# Старые кнопки (оставлены для совместимости)
btn-referral-level-choice = { $type -> 
    [1] 1️⃣
    [2] 2️⃣
    [3] 3️⃣
    *[OTHER] { $type }
    }

btn-referral-reward-choice = { $type -> 
    [POINTS] 💎 Баллы
    [EXTRA_DAYS] ⏳ Дни
    [MONEY] 💰 Деньги
    *[OTHER] { $type }
    }

btn-referral-accrual-strategy-choice = { $type -> 
    [ON_FIRST_PAYMENT] 💳 Первый платеж
    [ON_EACH_PAYMENT] 💸 Каждый платеж
    *[OTHER] { $type }
    }

btn-referral-reward-strategy-choice = { $type -> 
    [AMOUNT] 🔸 Фиксированная
    [PERCENT] 🔹 Процентная
    *[OTHER] { $type }
    }


# Notifications
btn-notifications-user = 👥 Пользовательские

btn-notifications-user-choice = { $enabled ->
    [1] 🔘
    *[0] ⚪
    } { $type ->
    [EXPIRES_IN_3_DAYS] Подписка истекает (3 дня)
    [EXPIRES_IN_2_DAYS] Подписка истекает (2 дня)
    [EXPIRES_IN_1_DAYS] Подписка истекает (1 день)
    [EXPIRED] Подписка истекла
    [LIMITED] Трафик исчерпан
    [EXPIRED_1_DAY_AGO] Подписка истекла (1 день)
    [REFERRAL_ATTACHED] Реферал закреплен
    [REFERRAL_REWARD] Получено вознаграждение
    *[OTHER] { $type }
    }

btn-notifications-system = ⚙️ Системные

btn-notifications-system-choice = { $enabled -> 
    [1] 🔘
    *[0] ⚪
    } { $type ->
    [BOT_LIFETIME] Жизненный цикл бота
    [BOT_UPDATE] Обновления бота
    [USER_REGISTERED] Регистрация пользователя
    [SUBSCRIPTION] Оформление подписки
    [PROMOCODE_ACTIVATED] Активация промокода
    [TRIAL_GETTED] Получение пробника
    [NODE_STATUS] Статус узла
    [USER_FIRST_CONNECTED] Первое подключение
    [USER_HWID] Устройства пользователя
    [BILLING] Финансовые операции
    [BALANCE_TRANSFER] Финансовые переводы
    *[OTHER] { $type }
    }


# Plans
btn-plans-statistics = 📊 Статистика
btn-plans-create = 🆕 Создать
btn-plan-save = ✅ Сохранить
btn-plan-create = ✅ Создать план
btn-plan-delete = ❌ Удалить
btn-plan-name = 🏷️ Название
btn-plan-description = 💬 Описание
btn-plan-description-remove = ❌ Удалить текущее описание
btn-plan-tag = 📌 Тег
btn-plan-tag-remove = ❌ Удалить текущий тег
btn-plan-type = 🔖 Тип
btn-plan-availability = ✴️ Доступ
btn-plan-durations-prices = 💰 Тарифы
btn-plan-traffic = 🌐 Трафик
btn-plan-devices = 📱 Устройства
btn-plan-allowed = 👥 Разрешенные пользователи
btn-plan-squads = 🔗 Сквады
btn-plan-internal-squads = ⏺️ Внутренние сквады
btn-plan-external-squads = ⏹️ Внешний сквад
btn-allowed-user = { $id }
btn-plan-duration-add = 🆕 Добавить
btn-plan-price-choice = 💸 { $price } { $currency }

btn-plan = { $is_active ->
    [1] 🟢
    *[0] 🔴 
    } { $name }

btn-plan-active = { $is_active -> 
    [1] 🟢 Включен
    *[0] 🔴 Выключен
    }

btn-plan-type-choice = { $type -> 
    [TRAFFIC] 🌐 Трафик
    [DEVICES] 📱 Устройства
    [BOTH] 🔗 Трафик + устройства
    [UNLIMITED] ♾️ Безлимит
    *[OTHER] { $type }
    }

btn-plan-type-radio = { $selected ->
    [1] 🔘 { $type ->
        [TRAFFIC] 🌐 Трафик
        [DEVICES] 📱 Устройства
        [BOTH] 🔗 Трафик + устройства
        [UNLIMITED] ♾️ Безлимит
        *[OTHER] { $type }
        }
    *[0] ⚪ { $type ->
        [TRAFFIC] 🌐 Трафик
        [DEVICES] 📱 Устройства
        [BOTH] 🔗 Трафик + устройства
        [UNLIMITED] ♾️ Безлимит
        *[OTHER] { $type }
        }
    }

btn-plan-availability-choice = { $type -> 
    [ALL] 🌍 Для всех
    [NEW] 🌱 Для новых
    [EXISTING] 👥 Для клиентов
    [INVITED] ✉️ Для приглашенных
    [ALLOWED] 🔐 Для разрешенных
    [TRIAL] 🎁 Для пробника
    *[OTHER] { $type }
    }

btn-plan-availability-radio = { $selected ->
    [1] 🔘 { $type ->
        [ALL] 🌍 Для всех
        [NEW] 🌱 Для новых
        [EXISTING] 👥 Для клиентов
        [INVITED] ✉️ Для приглашенных
        [ALLOWED] 🔐 Для разрешенных
        [TRIAL] 🎁 Для пробника
        *[OTHER] { $type }
        }
    *[0] ⚪ { $type ->
        [ALL] 🌍 Для всех
        [NEW] 🌱 Для новых
        [EXISTING] 👥 Для клиентов
        [INVITED] ✉️ Для приглашенных
        [ALLOWED] 🔐 Для разрешенных
        [TRIAL] 🎁 Для пробника
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

btn-keep-current-duration = ⏸️ Не менять длительность ({ $remaining })


# RemnaWave
btn-remnawave-users = 👥 Пользователи
btn-remnawave-hosts = 🌐 Хосты
btn-remnawave-nodes = 🖥️ Ноды
btn-remnawave-inbounds = 🔌 Инбаунды


# Importer
btn-importer-from-xui = 💩 Импорт из панели 3X-UI
btn-importer-from-xui-shop = 🛒 Бот 3xui-shop
btn-importer-sync = 🌀 Из панели в бот
btn-importer-sync-bot-to-panel = 📤 Из телеграма в панель
btn-importer-squads = 🔗 Внутренние сквады
btn-importer-import-all = ✅ Импортировать всех
btn-importer-import-active = ❇️ Импортировать активных


# Subscription
btn-subscription-new = 💸 Купить подписку
btn-subscription-buy = 🛒 Купить подписку
btn-subscription-renew = 🔄 Продлить
btn-subscription-change = 🔃 Изменить
btn-subscription-referral = 📢 Реферальная подписка
btn-subscription-upgrade-referral = 📢 Улучшить до реферальной
btn-subscription-promocode = 🎟 Активировать промокод
btn-subscription-payment-method = 
    { $gateway_type ->
    [BALANCE] 💰 С баланса
    [YOOMONEY] 💳 ЮMoney
    [YOOKASSA] 💳 ЮKassa
    [TELEGRAM_STARS] ⭐ Звёзды телеграм
    [CRYPTOMUS] 🔐 Cryptomus
    [HELEKET] 💎 Heleket
    [CRYPTOPAY] 🪙 Cryptopay
    [ROBOKASSA] 💳 Robokassa
    *[OTHER] { $gateway_type }
    } | { $has_discount ->
        [1] { $price } ({ $original_price })
        *[0] { $price }
    }
btn-subscription-pay = 💳 Оплатить
btn-check-payment = 🔄 Я оплатил
btn-subscription-confirm-balance = ✅ Подтвердить оплату
btn-subscription-get = 🎁 Получить бесплатно
btn-subscription-back-plans = ⬅️ Назад к выбору плана
btn-subscription-back-duration = ⬅️ Назад
btn-subscription-back-payment-method = ⬅️ Изменить способ оплаты
btn-subscription-connect = 🚀 Подключиться
btn-subscription-duration = { $final_amount -> 
    [0] { $period } | 🎁
    *[HAS] { $has_discount ->
        [1] { $period } | { $final_amount } ({ $original_amount })
        *[0] { $period } | { $final_amount }
        }
    }

# Extra device duration buttons
btn-add-device-duration-full = Конец подписки ({ $days } д.) | { $price } ₽
btn-add-device-duration-month = Конец периода ({ $days } д.) | { $price } ₽
btn-add-device-duration-months-1 = 1 месяц (30 д.) | { $price } ₽
btn-add-device-duration-months-3 = 3 месяца (90 д.) | { $price } ₽
btn-add-device-duration-months-6 = 6 месяцев (180 д.) | { $price } ₽
btn-add-device-duration-months-12 = 12 месяцев (365 д.) | { $price } ₽


# Promocodes
btn-promocode-code = 🏷️ Код
btn-promocode-name = 📝 Название
btn-promocode-type = 🔖 Тип
btn-promocode-availability = ✴️ Доступ

btn-promocode-active = { $is_active -> 
    [1] ✅ Выключить
    *[0] 🔴 Включить
    }

btn-promocode-reward = 🎁 Награда
btn-promocode-lifetime = ⌛ Время жизни
btn-promocode-allowed = 👥 Разрешенные пользователи
btn-promocode-access = 📦 Доступ к тарифам
btn-promocode-confirm = ✅ Сохранить
btn-promocode-quantity = 🔢 Количество
btn-promocode-generate = 🎲 Случайный код
btn-lifetime-infinite = Бесконечно
btn-quantity-infinite = Бесконечно
btn-manual-input = ✏️ Ручной ввод

btn-promocode-type-choice = { $selected -> 
    [1] 🔘
    *[0] ⚪
    } { $name }

btn-plan-access-choice = { $selected -> 
    [1] 🔘 { $plan_name }
    *[0] ⚪ { $plan_name }
    }

btn-pay = 💳 Оплатить

# Devices
btn-device-pending-deletion = ⏳ Удаляется
btn-device-marked-for-deletion = ✅ Помечено на удаление
btn-device-count = { $device_count } шт.
btn-pending-deletion-label = 🗑 На удалении

# Alerts (callback.answer)
alert-active-subscription-required = ❌ Требуется активная подписка
alert-active-subscription-required-for-devices = ❌ Требуется активная подписка для покупки дополнительных устройств
alert-trial-subscription-not-allowed = ❌ Пробная подписка не подходит. Требуется платная подписка
alert-referral-subscription-not-allowed = ❌ Реферальная подписка не подходит. Требуется платная подписка
alert-trial-subscription-not-suitable = ❌ Пробная подписка не подходит
alert-referral-subscription-not-suitable = ❌ Реферальная подписка не подходит
alert-slot-empty = Слот пустой
frg-empty-slot = Пустой слот

# Update snooze
btn-update-now = 🔄 Обновить сейчас
btn-update-remind-1d = ⏰ Через 1 день
btn-update-remind-3d = ⏰ Через 3 дня
btn-update-remind-7d = ⏰ Через 7 дней
btn-update-remind-off = 🔕 Не напоминать
btn-update-close = ❌ Закрыть
