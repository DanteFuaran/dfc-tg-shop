# Errors
ntf-error-lost-context = <i>⚠️ Виникла помилка. Діалог перезапущено.</i>
ntf-error-log-not-found = <i>⚠️ Помилка: файл логу не знайдено.</i>

# Database Export
ntf-db-export-start = <i>💾 Починається експорт бази даних...</i>
ntf-db-export-success = 
    <i>✅ Базу даних успішно збережено!</i>
    
    <b>Шлях:</b> <code>{ $path }</code>
    
    <i>Файл можна відкрити в DB Browser (SQLite)</i>
ntf-db-export-error = 
    <i>❌ Помилка експорту бази даних:</i>
    
    <blockquote>{ $error }</blockquote>
ntf-db-save-success = <i>✅ Резервну копію бази даних успішно збережено!</i>
ntf-db-save-failed = <i>❌ Помилка збереження резервної копії бази даних.</i>
ntf-db-convert-success = <i>✅ Файл було сконвертовано!</i>
ntf-db-convert-in-progress = ⚠️ Відбувається конвертація в SQL...
ntf-db-convert-in-progress = <i>⚠️ Відбувається конвертація в SQL</i>
ntf-db-restore-success =
    <i>✅ Базу даних успішно відновлено з завантаженого дампу.</i>

ntf-db-restore-failed =
    <i>❌ Помилка відновлення бази даних.</i>

ntf-db-sync-completed = <i>✅ Відновлення бази даних завершено!</i>
ntf-db-sync-title = ✅ <b>Відновлення завершено!</b>
ntf-db-sync-skipped-title = <b>⊘ Пропущені користувачі без підписок:</b>
ntf-db-sync-errors-title = <b>❌ Помилки синхронізації:</b>
ntf-db-sync-stats-title = <b>📊 Підсумок:</b>
ntf-db-sync-stats-total = Всього в боті: { $total }
ntf-db-sync-stats-created = Створено: { $created }
ntf-db-sync-stats-updated = Оновлено: { $updated }
ntf-db-sync-stats-skipped = Пропущено: { $skipped }
ntf-db-sync-stats-errors = Помилок: { $errors }
ntf-db-sync-error = ❌ Помилка синхронізації: { $error }
ntf-db-import-started = <i>⚠️ Виконується імпорт бази даних. Зачекайте...</i>
ntf-db-import-failed = <i>❌ Помилка імпорту бази даних.</i>
ntf-db-restore-preparing = <i>🔄 Підготовка до відновлення даних...</i>

# Database Clear
ntf-db-clear-all-warning = 
    <b>⚠️ Натисніть ще раз для підтвердження дії.</b>

ntf-db-clear-all-start = <i>🗑 Виконується повне очищення бази даних...</i>
ntf-db-clear-all-success = 
    <b>✅ Видалення завершено!</b>
    
    <blockquote>
    📊 Видалено записів:
    • Користувачі: <b>{ $users }</b>
    • Покупки додаткових пристроїв: <b>{ $extra_device_purchases }</b>
    • Реферали: <b>{ $referrals }</b>
    • Тарифні плани: <b>{ $plans }</b>
    • Промокоди: <b>{ $promocodes }</b>
    </blockquote>
ntf-db-clear-all-failed = 
    <i>❌ Помилка очищення бази даних:</i>
    
    <blockquote>{ $error }</blockquote>

ntf-db-clear-users-warning = 
    <b>⚠️ Натисніть ще раз для підтвердження дії.</b>

ntf-db-clear-users-start = <i>🗑 Видалення користувачів...</i>
ntf-db-clear-users-success = 
    <b>✅ Видалення завершено!</b>
    
    <blockquote>
    📊 Всього:
    • Видалено: <b>{ $users }</b>
    • Пропущено: <b>0</b>
    • Помилок: <b>0</b>
    </blockquote>
ntf-db-clear-users-failed = 
    <i>❌ Помилка видалення користувачів:</i>
    
    <blockquote>{ $error }</blockquote>

# Existing subscription import notifications
ntf-existing-subscription-found =
    <i>✅ Знайдено існуючу підписку!</i>
    
    <blockquote>
    У вас вже є підписка в панелі керування.
    Її успішно прив'язано до вашого облікового запису.
    
    • <b>План:</b> { $plan_name }
    • <b>Тег:</b> { $tag }
    </blockquote>
    
ntf-existing-subscription-no-plan =
    <i>⚠️ Знайдено існуючу підписку!</i>
    
    <blockquote>
    У вас вже є підписка в панелі керування.
    Однак відповідний план не знайдено в боті.
    
    • <b>Поточний тег:</b> { $old_tag }
    • <b>Новий тег:</b> IMPORT
    
    Зверніться до адміністратора для налаштування підписки.
    </blockquote>

# Sync notifications
ntf-sync-preparing = <i>🔄 Підготовка даних для імпорту...</i>
ntf-sync-started = <i>🔄 Синхронізація даних. Зачекайте...</i>
ntf-sync-completed =
    <i>✅ Синхронізацію завершено!</i>
    
    <blockquote>
    Напрямок: <b>{ $direction ->
        [bot_to_panel] Бот → Панель
        *[panel_to_bot] Панель → Бот
    }</b>
    Синхронізовано: <b>{ $synced }</b>
    Створено: <b>{ $created }</b>
    Помилок: <b>{ $errors }</b>
    </blockquote>
ntf-sync-failed =
    <i>❌ Помилка синхронізації:</i>
    
    <blockquote>{ $error }</blockquote>

# Balance transfer notifications
ntf-balance-transfer-received =
    <i>💸 Ви отримали переказ!</i>
    
    <b>📋 Деталі переказу:</b>
    <blockquote>• Відправник: <b>{ $sender }</b>
    • Сума: <b>{ $amount } ₽</b>
    • Комісія: Сплачена відправником{ $has_message ->
        [0] {""}
       *[1] {""}
    </blockquote>
    <b>💬 Повідомлення:</b>
    <blockquote>• <i>{ $message }</i>
    }
    </blockquote>
ntf-balance-transfer-insufficient = <i>⚠️ Недостатньо коштів! Потрібно: { $required }, баланс: { $balance }</i>
ntf-balance-transfer-invalid-id = <i>⚠️ Telegram ID повинен містити лише цифри!</i>
ntf-balance-transfer-user-not-found = <i>⚠️ Користувача не знайдено!</i>
ntf-balance-transfer-self = <i>⚠️ Ви не можете переказати кошти самому собі!</i>
ntf-balance-transfer-disabled = <i>⚠️ Функцію переказу вимкнено!</i>
ntf-balance-transfer-amount-range = <i>⚠️ Сума переказу повинна бути від { $min } до { $max } ₽</i>
ntf-balance-transfer-incomplete = <i>⚠️ Потрібно вказати отримувача і суму переказу!</i>
ntf-balance-transfer-success =
    <i>✅ Переказ виконано!</i>
    
    <b>📋 Деталі переказу:</b>
    <blockquote>• Отримувач: <b>{ $recipient }</b>
    • Сума: <b>{ $amount } ₽</b>
    • Комісія: <b>{ $commission } ₽</b>{ $has_message ->
        [0] {""}
       *[1] {""}
    </blockquote>
    <b>💬 Повідомлення:</b>
    <blockquote>• <i>{ $message }</i>
    }
    </blockquote>
ntf-balance-transfer-error = <i>⚠️ Помилка обробки переказу!</i>

ntf-balance-invalid-amount = 
    <i>⚠️ Сума поповнення доступна від { $min_amount } до { $max_amount } ₽.</i>
ntf-bonus-insufficient = <i>⚠️ Недостатньо бонусів!</i>
ntf-bonus-activated = <i>✅ { $amount } ₽ зараховано на баланс!</i>
ntf-balance-withdraw-in-development = 🚧 Функція автоматичного виведення коштів знаходиться в розробці. Для виведення зверніться до служби підтримки.
ntf-invite-link-copied = <i>⚠️ Посилання скопійовано в буфер обміну.</i>


# Events
ntf-event-error =
    🤖 <b>Система: Виникла помилка!</b>
    
    { $user -> 
    [1]
    { hdr-user }
    { frg-user-info }
    *[0] { space }
    }

    { hdr-error }
    <blockquote>
    { $error }
    </blockquote>

ntf-event-error-remnawave =
    🤖 <b>Система: Помилка підключення до Remnawave!</b>

    <blockquote>
    Без активного підключення бот не може працювати коректно!
    </blockquote>

    { hdr-error }
    <blockquote>
    { $error }
    </blockquote>

ntf-event-error-webhook =
    🤖 <b>Система: Виявлено помилку webhook!</b>

    { hdr-error }
    <blockquote>
    { $error }
    </blockquote>

ntf-event-bot-startup =
    🤖 <b>Система: Бот запущено!</b>

    <blockquote>
    • <b>Режим доступу</b>: { access-mode }
    • <b>Покупки</b>: { $purchases_allowed ->
    [0] вимкнено
    *[1] увімкнено
    }.
    • <b>Реєстрація</b>: { $registration_allowed ->
    [0] вимкнено
    *[1] увімкнено
    }.
    </blockquote>

ntf-event-bot-shutdown =
    🤖 <b>Система: Бот зупинено!</b>

ntf-event-bot-started =
    🤖 <b>Система: Бот увімкнено!</b>

ntf-event-bot-update =
    🤖 <b>Система: Виявлено оновлення DFC Shop!</b>

    <blockquote>
    • <b>Поточна версія</b>: { $local_version }
    • <b>Доступна версія</b>: { $remote_version }
    </blockquote>

ntf-event-new-user =
    🤖 <b>Система: Новий користувач!</b>

    { hdr-user }
    { frg-user-info }

    { $has_referrer ->
    [0] { empty }
    *[HAS]
    <b>🤝 Реферер:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $referrer_user_id }</code>
    • <b>Ім'я</b>: { $referrer_user_name } { $referrer_username -> 
        [0] { empty }
        *[HAS] (<a href="tg://user?id={ $referrer_user_id }">@{ $referrer_username }</a>)
    }
    </blockquote>
    }

ntf-event-referral-upgrade =
    🤖 <b>Система: Реєстрація в реф.системі!</b>

    { hdr-user }
    { frg-user-info }

    <b>🤝 Реферер:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $referrer_user_id }</code>
    • <b>Ім'я</b>: { $referrer_user_name } { $referrer_username -> 
        [0] { empty }
        *[HAS] (<a href="tg://user?id={ $referrer_user_id }">@{ $referrer_username }</a>)
    }
    </blockquote>

ntf-event-promocode-activated =
    🤖 <b>Система: Промокод активовано!</b>

    { hdr-user }
    { frg-user-info }

    <b>🎟️ Промокод:</b>
    <blockquote>
    • <b>Код</b>: <code>{ $promocode_code }</code>
    • <b>Винагорода</b>: { $promocode_reward_type ->
        [PURCHASE_DISCOUNT] { $promocode_reward }% знижка на покупку
        [PERSONAL_DISCOUNT] { $promocode_reward }% постійна знижка
        [DURATION] +{ $promocode_reward } днів до підписки
        *[OTHER] { $promocode_reward } { $promocode_reward_type }
    }
    </blockquote>

ntf-event-test-webhook-success =
    🤖 <b>Система: Тестовий webhook успішний!</b>

    <b>💳 Платіжний шлюз:</b>
    <blockquote>
    • <b>Назва</b>: { $gateway_name }
    • <b>Тип</b>: <code>{ $gateway_type }</code>
    </blockquote>

    <i>Тестове повідомлення отримано та оброблено успішно.</i>

ntf-event-test-webhook-failed =
    🤖 <b>Система: Помилка тестового webhook!</b>

    <b>💳 Платіжний шлюз:</b>
    <blockquote>
    • <b>Тип</b>: <code>{ $gateway_type }</code>
    </blockquote>

    <b>⚠️ Помилка:</b>
    <blockquote>
    • <b>Тип</b>: <code>{ $error_type }</code>
    • <b>Повідомлення</b>: { $error_message }
    </blockquote>
    
ntf-event-subscription-trial =
    🤖 <b>Система: Отримано пробну підписку!</b>

    { hdr-user }
    { frg-user-info }
    
    { hdr-plan }
    { frg-plan-snapshot }

ntf-event-subscription-new =
    🤖 <b>Система: Підписку придбано!</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot }

ntf-event-subscription-renew =
    🤖 <b>Система: Підписку продовжено!</b>
    
    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot }

    { $has_extra_devices ->
        [1] 

    <b>📱 Дод. пристрої:</b>
    <blockquote>
    • <b>Кількість</b>: { $extra_devices_count }
    • <b>Вартість</b>: { $extra_devices_cost }
    </blockquote>
        *[0] {""}
    }

ntf-event-subscription-change =
    🤖 <b>Система: Підписку змінено!</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot-comparison }

ntf-event-balance-topup =
    🤖 <b>Система: Баланс поповнено!</b>

    <blockquote>
    • <b>ID</b>: <code>{ $payment_id }</code>
    • <b>Спосіб оплати</b>: { gateway-type }
    • <b>Сума</b>: { $final_amount }
    </blockquote>

    { hdr-user }
    { frg-user-info }

ntf-event-extra-devices =
    🤖 <b>Система: Придбано додаткові пристрої!</b>

    <blockquote>
    • <b>ID</b>: <code>{ $payment_id }</code>
    • <b>Спосіб оплати</b>: { gateway-type }
    • <b>Сума</b>: { $final_amount }
    • <b>Знижка</b>: { $discount_percent }%
    • <b>Пристрої</b>: +{ $device_count } шт.
    </blockquote>

    { hdr-subscription }
    { frg-subscription-details }

    { hdr-user }
    { frg-user-info }

ntf-event-extra-devices-balance =
    🤖 <b>Система: Придбано додаткові пристрої!</b>

    <blockquote>
    • <b>Спосіб оплати</b>: 💰 З балансу
    • <b>Сума</b>: { $price } ₽
    • <b>Знижка</b>: { $discount_percent }%
    • <b>Пристрої</b>: +{ $device_count } шт.
    </blockquote>

    { hdr-user }
    { frg-user-info }
ntf-event-extra-devices-deletion =
    🤖 <b>Система: Видалення додаткових пристроїв!</b>

    { hdr-user }
    { frg-user-info }

    <blockquote>
    • <b>Пристроїв</b>: -{ $device_count } шт.
    • <b>Видалення через</b>: { $delete_after }
    </blockquote>
ntf-event-balance-transfer =
    🤖 <b>Система: Фінансовий переказ!</b>

    <b>👤 Відправник:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $sender_id }</code>
    • <b>Ім'я</b>: { $sender_name }
    • <b>Баланс після</b>: { $sender_balance } ₽
    </blockquote>

    <b>👤 Отримувач:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $recipient_id }</code>
    • <b>Ім'я</b>: { $recipient_name }
    • <b>Баланс після</b>: { $recipient_balance } ₽
    </blockquote>

    <b>💰 Деталі переказу:</b>
    <blockquote>
    • <b>Сума</b>: { $amount } ₽
    • <b>Комісія</b>: { $commission } ₽
    • <b>Всього списано</b>: { $total } ₽{ $has_message ->
        [0] {""}
       *[1] {""}
    • <b>Повідомлення</b>: <i>{ $message }</i>
    }
    </blockquote>

ntf-event-node-connection-lost =
    🤖 <b>Система: Втрачено з'єднання з нодою!</b>

    { hdr-node }
    { frg-node-info }

ntf-event-node-connection-restored =
    🤖 <b>Система: З'єднання з нодою відновлено!</b>

    { hdr-node }
    { frg-node-info }

ntf-event-node-traffic =
    🤖 <b>Система: Нода досягла порогу ліміту трафіку!</b>

    { hdr-node }
    { frg-node-info }

ntf-event-user-first-connected =
    🤖 <b>Система: Перше підключення користувача!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-subscription }
    { frg-subscription-details }

ntf-event-user-not-connected =
    🤖 <b>Система: Користувач не підключився!</b>

    <blockquote>
    Користувач зареєструвався { $hours } год. тому, але не оформив підписку.
    Можливо, йому потрібна допомога.
    </blockquote>

    { hdr-user }
    { frg-user-info }
    
    <b>📅 Дата реєстрації:</b> { $registered_at }

ntf-event-user-expiring =
    { $is_trial ->
    [0]
    <b>⚠️ Увага! Ваша підписка закінчується через { unit-day }.</b>
    
    Продовжте її заздалегідь, щоб не втратити доступ до сервісу! 
    *[1]
    <b>⚠️ Увага! Ваш безкоштовний пробний період закінчується через { unit-day }.</b>

    Оформіть підписку, щоб не втратити доступ до сервісу! 
    }

ntf-event-user-expired =
    <b>⛔ Увага! Доступ призупинено.</b>

    { $is_trial ->
    [0] Термін дії вашої підписки закінчився, продовжте її, щоб продовжити користуватися сервісом!
    *[1] Ваш безкоштовний пробний період закінчився. Оформіть підписку, щоб продовжити користуватися сервісом!
    }
    
ntf-event-user-expired-ago =
    <b>⛔ Увага! Доступ призупинено.</b>

    { $is_trial ->
    [0] Термін дії вашої підписки закінчився { unit-day } тому, продовжте її, щоб продовжити користуватися сервісом!
    *[1] Ваш безкоштовний пробний період закінчився { unit-day } тому. Оформіть підписку, щоб продовжити користуватися сервісом!
    }

ntf-event-user-limited =
    <b>⛔ Увага! Доступ призупинено - VPN не працює.</b>

    Ваш трафік вичерпано. { $is_trial ->
    [0] { $traffic_strategy ->
        [NO_RESET] Продовжте підписку, щоб скинути трафік і продовжити користуватися сервісом!
        *[RESET] Трафік буде відновлено через { $reset_time }. Ви також можете продовжити підписку для скидання трафіку.
        }
    *[1] { $traffic_strategy ->
        [NO_RESET] Оформіть підписку, щоб продовжити користуватися сервісом!
        *[RESET] Трафік буде відновлено через { $reset_time }. Ви також можете оформити підписку для користування сервісом без обмежень.
        }
    }

ntf-event-user-hwid-added =
    🤖 <b>Система: Користувач додав новий пристрій!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-hwid }
    { frg-user-hwid }

ntf-event-user-hwid-deleted =
    🤖 <b>Система: Користувач видалив пристрій!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-hwid }
    { frg-user-hwid }

ntf-event-user-referral-attached =
    <b>🎉 Ви запросили друга!</b>
    
    <blockquote>
    Користувач <b>{ $name }</b> приєднався за вашим посиланням-запрошенням! Щоб отримати винагороду, переконайтеся, що він придбав підписку.
    </blockquote>

ntf-event-user-referral-reward =
    <b>💰 Ви отримали винагороду!</b>
    
    <blockquote>
    Користувач <b>{ $name }</b> здійснив оплату. Ви отримали <b>{ $value }{ $reward_type ->
        [MONEY] { space }{ $currency }
        [EXTRA_DAYS] { space }додаткових { $value ->
            [one] день
            *[other] днів
            }
        *[OTHER] { $currency }
    }</b> на ваш реферальний баланс!
    </blockquote>

ntf-event-user-referral-reward-error =
    <b>❌ Не вдалося нарахувати винагороду!</b>
    
    <blockquote>
    Користувач <b>{ $name }</b> здійснив оплату, але ми не змогли нарахувати вашу винагороду, тому що <b>у вас немає придбаної підписки</b>, до якої можна додати {$value} { $value ->
            [one] додатковий день
            *[other] додаткових днів
        }.
    
    <i>Придбайте підписку, щоб отримувати бонуси за запрошених друзів!</i>
    </blockquote>


ntf-cashback-reward =
    <b>🎉 Вітаємо! Ви отримуєте кешбек!</b>

    <blockquote>
    Оскільки ви берете участь у реферальній програмі, ви отримуєте додатковий бонус до вашого платежу: <b>{ $value }{ $reward_type ->
        [MONEY] { space }{ $currency }
        [EXTRA_DAYS] { space }додаткових { $value ->
            [one] день
            *[other] днів
            }
        *[OTHER] { $currency }
    }</b>!
    </blockquote>

# Notifications
ntf-command-paysupport = 💸 <b>Для запиту на повернення коштів зверніться до служби підтримки.</b>
ntf-command-help = 🆘 <b>Натисніть кнопку нижче, щоб зв'язатися з підтримкою. Ми допоможемо вирішити вашу проблему.</b>
ntf-channel-join-required = ❇️ Підпишіться на наш канал і отримайте <b>безкоштовні дні, акції та новини</b>! Після підписки натисніть "Підтвердити".
ntf-channel-join-required-left = ⚠️ Ви відписалися від нашого каналу! Підпишіться, щоб мати можливість користуватися ботом.
ntf-rules-accept-required = ⚠️ <b>Перед використанням сервісу, будь ласка, прочитайте та прийміть <a href="{ $url }">Умови використання</a>.</b>

ntf-double-click-confirm = <i>⚠️ Натисніть ще раз для підтвердження дії.</i>
ntf-user-referral-bind-not-found = <i>⚠️ Користувача не знайдено.</i>
ntf-user-referral-bind-self = <i>⚠️ Неможливо прив'язати користувача до самого себе.</i>
ntf-user-referral-bind-already = <i>⚠️ Цей користувач вже є рефералом іншого користувача.</i>
ntf-user-referral-bind-success = <i>✅ Реферал успішно прив'язаний.</i>
ntf-user-deleted = <i>✅ Користувача видалено.</i>
ntf-channel-join-error = <i>⚠️ Ми не бачимо вашу підписку на канал. Переконайтеся, що ви підписалися, і спробуйте ще раз.</i>
ntf-throttling-many-requests = <i>⚠️ Ви надсилаєте занадто багато запитів, будь ласка, зачекайте.</i>
ntf-squads-empty = <i>⚠️ Сквади не знайдено. Перевірте їх наявність у панелі.</i>
ntf-invite-withdraw-points-error = ❌ У вас недостатньо балів для здійснення обміну.
ntf-invite-withdraw-no-balance = ❌ У вас немає бонусів для переведення на баланс.
ntf-invite-withdraw-success = ✅ { $amount } ₽ успішно переведено на ваш основний баланс!

ntf-connect-not-available =
    ⚠️ { $status ->
    [LIMITED]
    Ви використали весь доступний трафік. { $is_trial ->
    [0] { $traffic_strategy ->
        [NO_RESET] Продовжте підписку, щоб скинути трафік і продовжити користуватися сервісом!
        *[RESET] Трафік буде відновлено через { $reset_time }. Ви також можете продовжити підписку для скидання трафіку.
        }
    *[1] { $traffic_strategy ->
        [NO_RESET] Оформіть підписку, щоб продовжити користуватися сервісом!
        *[RESET] Трафік буде відновлено через { $reset_time }. Ви також можете оформити підписку для користування сервісом без обмежень.
        }
    }
    [EXPIRED]  
    { $is_trial ->
    [0] Термін дії вашої підписки закінчився. Щоб продовжити користуватися сервісом, продовжте підписку або придбайте нову.
    *[1] Ваш безкоштовний пробний період закінчився. Оформіть підписку, щоб продовжити користуватися сервісом!
    }
    *[OTHER] Виникла помилка при перевірці статусу або вашу підписку було вимкнено. Зверніться до служби підтримки.
    }

ntf-user-not-found = <i>❌ Користувача не знайдено.</i>
ntf-user-transactions-empty = <i>❌ Список транзакцій порожній.</i>
ntf-user-subscription-empty = <i>❌ Поточну підписку не знайдено.</i>
ntf-user-plans-empty = <i>❌ Немає доступних планів для надання.</i>
ntf-user-devices-empty = <i>❌ Список пристроїв порожній.</i>
ntf-user-invalid-number = <i>❌ Неправильне число.</i>
ntf-user-no-pending-amount = <i>⚠️ Спочатку оберіть суму для нарахування.</i>
ntf-user-device-limit-exceeded = <i>❌ Кількість пристроїв не може перевищувати 100.</i>
ntf-user-allowed-plans-empty = <i>❌ Немає доступних планів для надання доступу.</i>
ntf-user-message-success = <i>✅ Повідомлення успішно надіслано.</i>
ntf-user-message-not-sent = <i>❌ Не вдалося надіслати повідомлення.</i>
ntf-user-sync-already = <i>✅ Дані підписки збігаються.</i>
ntf-user-sync-missing-data = <i>⚠️ Синхронізація неможлива. Дані підписки відсутні як у панелі, так і в боті.</i>
ntf-user-sync-success = <i>✅ Синхронізацію підписки завершено.</i>

ntf-user-invalid-expire-time = <i>❌ Неможливо { $operation ->
    [ADD] продовжити підписку на вказану кількість днів
    *[SUB] зменшити підписку на вказану кількість днів
    }.</i>

ntf-user-invalid-points = <i>❌ Неможливо { $operation ->
    [ADD] додати вказану кількість балів
    *[SUB] списати вказану кількість балів
    }.</i>

ntf-user-invalid-balance = <i>❌ Неможливо { $operation ->
    [ADD] додати вказану суму на баланс
    *[SUB] списати вказану суму з балансу
    }.</i>

ntf-referral-invalid-reward = <i>❌ Неправильне значення.</i>

ntf-access-denied = <i>🚧 Бот знаходиться на технічному обслуговуванні, спробуйте пізніше.</i>
ntf-access-denied-registration = <i>❌ Реєстрацію нових користувачів вимкнено.</i>
ntf-access-denied-only-invited = <i>❌ Реєстрація нових користувачів доступна лише за запрошенням іншого користувача.</i>
ntf-access-denied-purchasing = <i>🚧 Оплата сервісу тимчасово відключена, Вам прийде сповіщення коли оплати будуть доступні.</i>
ntf-payments-available-again = <i>✅ Оплата сервісу знову доступна! Дякуємо за очікування!</i>
ntf-access-allowed = <i>❇️ Всі функції бота знову доступні, дякуємо за очікування.</i>
ntf-access-id-saved = <i>✅ ID каналу/групи успішно оновлено.</i>
ntf-access-link-saved = <i>✅ Посилання на канал/групу успішно оновлено.</i>
ntf-access-channel-invalid = <i>❌ Неправильне посилання або ID каналу/групи.</i>

ntf-plan-invalid-name = <i>❌ Неправильна назва.</i>
ntf-plan-invalid-description = <i>❌ Неправильний опис.</i>
ntf-plan-invalid-tag = <i>❌ Неправильний тег.</i>
ntf-plan-invalid-number = <i>❌ Неправильне число.</i>
ntf-plan-trial-once-duration = <i>❌ Пробний план може мати лише одну тривалість.</i>
ntf-plan-trial-already-exists = <i>❌ Пробний план вже існує.</i>
ntf-plan-duration-already-exists = <i>❌ Ця тривалість вже існує.</i>
ntf-plan-duration-last = <i>❌ Неможливо видалити останню тривалість.</i>
ntf-plan-save-error = <i>❌ Помилка збереження плану.</i>
ntf-plan-name-already-exists = <i>❌ План з такою назвою вже існує.</i>
ntf-plan-invalid-user-id = <i>❌ Неправильний ID користувача.</i>
ntf-plan-no-user-found = <i>❌ Користувача не знайдено.</i>
ntf-plan-user-already-allowed = <i>❌ Користувача вже додано до списку дозволених.</i>
ntf-plan-confirm-delete = <i>⚠️ Натисніть ще раз для видалення.</i>
ntf-plan-updated-success = <i>✅ План успішно оновлено.</i>
ntf-plan-created-success = <i>✅ План успішно створено.</i>
ntf-plan-deleted-success = <i>✅ План успішно видалено.</i>
ntf-plan-tag-updated = <i>✅ Тег плану оновлено.</i>
ntf-plan-internal-squads-empty = <i>❌ Виберіть хоча б один внутрішній сквад.</i>

ntf-gateway-not-configured = <i>❌ Платіжний шлюз не налаштовано.</i>
ntf-gateway-not-configurable = <i>❌ Платіжний шлюз не має налаштувань.</i>
ntf-gateway-field-wrong-value = <i>❌ Неправильне значення.</i>
ntf-gateway-test-payment-created = <i>✅ <a href="{ $url }">Тестовий платіж</a> успішно створено.</i>
ntf-gateway-test-payment-error = <i>❌ Помилка створення тестового платежу.</i>
ntf-gateway-test-payment-confirmed = <i>✅ Тестовий платіж успішно оброблено.</i>

ntf-subscription-plans-not-available = <i>❌ Немає доступних планів.</i>
ntf-subscription-gateways-not-available = <i>❌ Немає доступних платіжних систем.</i>
ntf-subscription-renew-plan-unavailable = <i>❌ Ваш план застарів і недоступний для продовження.</i>
ntf-subscription-change-plans-not-available = <i>❌ Немає доступних підписок для зміни. У вас вже активовано єдину доступну підписку.</i>
ntf-subscription-payment-creation-failed = <i>❌ Помилка створення платежу, спробуйте пізніше.</i>
ntf-payment-gateway-not-configured = <i>❌ Не налаштовані дані мерчанта { $gateway_name }</i>
ntf-subscription-insufficient-balance = <i>❌ Недостатньо коштів на балансі для оплати підписки.</i>
ntf-check-payment-pending = <i>⏳ Оплата ще не надійшла. Якщо ви вже оплатили, зачекайте трохи та спробуйте знову.</i>
ntf-check-payment-no-id = <i>❌ Не вдалося знайти дані платежу. Спробуйте створити платіж заново.</i>
ntf-check-payment-not-found = <i>❌ Транзакцію не знайдено. Спробуйте створити платіж заново.</i>

ntf-balance-payment-link = 
    <b>💳 Посилання для оплати</b>
    
    Перейдіть за посиланням для оплати:
    <a href="{ $payment_url }">Сплатити</a>

ntf-balance-topup-success = 
    ✅ <b>Баланс успішно поповнено!</b>
    
    Зараховано на ваш баланс: <b>{ $amount } { $currency }</b>

ntf-broadcast-list-empty = <i>❌ Список розсилок порожній.</i>
ntf-broadcast-audience-not-available = <i>❌ Немає користувачів для обраної аудиторії.</i>
ntf-broadcast-audience-not-active = <i>❌ Немає користувачів з АКТИВНОЮ підпискою для цього плану.</i>
ntf-broadcast-plans-not-available = <i>❌ Немає доступних планів.</i>
ntf-broadcast-empty-content = <i>❌ Вміст порожній.</i>
ntf-broadcast-wrong-content = <i>❌ Неправильний вміст.</i>
ntf-broadcast-content-saved = <i>✅ Вміст повідомлення успішно збережено.</i>
ntf-broadcast-preview = { $content }
ntf-invite-preview = { $content }
ntf-broadcast-not-cancelable = <i>❌ Розсилку неможливо скасувати.</i>
ntf-broadcast-canceled = <i>✅ Розсилку успішно скасовано.</i>
ntf-broadcast-deleting = <i>⚠️ Видалення всіх надісланих повідомлень.</i>
ntf-broadcast-already-deleted = <i>❌ Розсилка видаляється або вже видалена.</i>

ntf-broadcast-deleted-success =
    ✅ Розсилку <code>{ $task_id }</code> успішно видалено.

    <blockquote>
    • <b>Всього повідомлень</b>: { $total_count }
    • <b>Успішно видалено</b>: { $deleted_count }
    • <b>Не вдалося видалити</b>: { $failed_count }
    </blockquote>

ntf-trial-unavailable = <i>❌ Пробна підписка тимчасово недоступна.</i>ntf-trial-already-used = <i>❌ Ви вже використовували пробну підписку.</i>ntf-referral-code-invalid = <i>❌ Неправильний реферальний код. Спробуйте ще раз.</i>
ntf-referral-code-self = <i>❌ Ви не можете використати свій власний реферальний код.</i>
ntf-referral-code-own-referral = <i>❌ Ви не можете використати реферальний код користувача, якого ви запросили.</i>
ntf-referral-code-already-used = <i>❌ Ви вже використали реферальну підписку.</i>
ntf-referral-code-already-has = <i>❌ Ви вже прив'язані до реферера. Повторна прив'язка неможлива.</i>
ntf-referral-code-success-promo = <i>✅ Ви успішно прив'язалися до реферера!</i>

ntf-importer-not-file = <i>⚠️ Надішліть базу даних як файл.</i>
ntf-importer-db-invalid = <i>❌ Цей файл неможливо імпортувати.</i>
ntf-importer-db-failed = <i>❌ Помилка імпорту бази даних.</i>
ntf-importer-exported-users-empty =  <i>❌ Список користувачів у базі даних порожній.</i>
ntf-importer-internal-squads-empty = <i>❌ Виберіть хоча б один внутрішній сквад.</i>
ntf-importer-import-started = <i>✅ Імпорт користувачів розпочато, зачекайте...</i>
ntf-importer-sync-started = <i>🔄 Виконується синхронізація даних...</i>
ntf-importer-users-not-found = <i>❌ Не вдалося знайти користувачів для синхронізації.</i>
ntf-importer-not-support = <i>⚠️ Імпорт усіх даних з 3xui-shop тимчасово недоступний. Ви можете використати імпорт з панелі 3X-UI!</i>
ntf-importer-sync-already-running = <i>⚠️ Синхронізацію користувачів вже розпочато, зачекайте...</i>

ntf-importer-sync-bot-to-panel-completed =
    <b>📤 Синхронізацію завершено</b>

    <blockquote>
    <b>Всього в боті:</b> { $total_bot_users }
    <b>Створено:</b> { $created }
    <b>Оновлено:</b> { $updated }
    <b>Пропущено:</b> { $skipped }
    <b>Помилок:</b> { $errors }
    </blockquote>

ntf-sync-panel-to-bot-completed =
    <b>📥 Синхронізацію завершено</b>

    <blockquote>
    <b>Всього в панелі:</b> { $total_panel_users }
    <b>Створено:</b> { $created }
    <b>Синхронізовано:</b> { $synced }
    <b>Пропущено:</b> { $skipped }
    <b>Помилок:</b> { $errors }
    </blockquote>

# Remnawave Sync notifications
ntf-remnawave-sync-confirm = <i>⚠️ Натисніть ще раз для підтвердження імпорту.</i>
ntf-remnawave-sync-preparing = <i>🔄 Підготовка даних для імпорту...</i>
ntf-remnawave-sync-started = <i>🔄 Синхронізація даних...</i>
ntf-remnawave-sync-no-users = <i>❌ Користувачів для імпорту не знайдено.</i>
ntf-remnawave-sync-failed =
    <i>❌ Помилка імпорту:</i>

    <blockquote>{ $error }</blockquote>
ntf-remnawave-sync-bot-to-panel-completed =
    <b>✅ Імпорт з Бота в Remnawave завершено</b>

    <blockquote>
    <b>Всього в боті:</b> { $total_bot_users }
    <b>Створено:</b> { $created }
    <b>Оновлено:</b> { $updated }
    <b>Пропущено:</b> { $skipped }
    <b>Помилок:</b> { $errors }
    </blockquote>
ntf-remnawave-sync-panel-to-bot-completed =
    <b>✅ Синхронізація з Remnawave в Бота завершена</b>

    <blockquote>
    <b>Всього в панелі:</b> { $total_panel_users }
    <b>Створено:</b> { $created }
    <b>Синхронізовано:</b> { $synced }
    <b>Пропущено:</b> { $skipped }
    <b>Помилок:</b> { $errors }
    </blockquote>

ntf-remnawave-import-completed =
    <b>✅ Імпорт з Remnawave завершено</b>

    <blockquote>
    <b>Всього в панелі:</b> { $total_panel_users }
    <b>Всього в боті:</b> { $total_bot_users }
    <b>Додано користувачів:</b> { $added_users }
    <b>Додано підписок:</b> { $added_subscription }
    <b>Оновлено:</b> { $updated }
    <b>Без Telegram ID:</b> { $missing_telegram }
    <b>Помилок:</b> { $errors }
    </blockquote>

ntf-subscription-processing = <i>⏳ Обробка вашої підписки, зачекайте...</i>

# Promocodes
ntf-promocode-not-found = <i>❌ Промокод не знайдено.</i>
ntf-promocode-inactive = <i>⚠️ Промокод неактивний.</i>
ntf-promocode-already-activated = <i>⚠️ Ви вже використали цей промокод.</i>
ntf-promocode-limit-exceeded = <i>⚠️ Ліміт промокоду вичерпано.</i>
ntf-promocode-plan-unavailable = <i>⚠️ Промокод недоступний для вашого плану.</i>
ntf-promocode-activation-error = <i>❌ Помилка активації промокоду.</i>
ntf-promocode-activated = <i>✅ Промокод <code>{$promocode}</code> успішно активовано!</i>
ntf-promocode-invalid-name = <i>❌ Назва промокоду повинна бути від 1 до 50 символів.</i>
ntf-promocode-already-exists = <i>❌ Промокод з таким кодом вже існує.</i>
ntf-promocode-invalid-code = <i>❌ Промокод повинен бути від 3 до 20 символів.</i>
ntf-promocode-invalid-reward = <i>❌ Введіть правильне значення винагороди (додатне число).</i>
ntf-promocode-invalid-lifetime = <i>❌ Введіть правильний термін дії (0 = необмежено).</i>
ntf-promocode-invalid-quantity = <i>❌ Введіть правильну кількість активацій (0 = необмежено).</i>
ntf-promocode-created = <i>✅ Промокод успішно створено.</i>
ntf-promocode-updated = <i>✅ Промокод успішно оновлено.</i>
ntf-promocode-save-error = <i>❌ Помилка збереження промокоду.</i>
ntf-promocode-delete-error = <i>❌ Помилка видалення промокоду.</i>
ntf-promocode-delete-success = <i>✅ Промокод успішно видалено!</i>

# Devices
ntf-add-device-info = <i>ℹ️ Додавання пристрою збільшить вартість підписки на <b>{ $price } ₽/міс</b>.</i>
ntf-add-device-success = <i>✅ Новий ліміт пристроїв застосовано!</i>
ntf-add-device-payment-pending = <i>⏳ Оплата через обраний шлюз тимчасово недоступна для додавання пристроїв. Використовуйте баланс.</i>
ntf-payment-link = <i>💳 <a href="{ $payment_url }">Перейти до оплати</a></i>
ntf-payment-creation-failed = <i>❌ Помилка створення платежу, спробуйте пізніше.</i>
ntf-payment-gateway-not-available = <i>❌ Обраний платіжний шлюз тимчасово недоступний. Спробуйте пізніше.</i>
ntf-subscription-required = <i>❌ Для додавання пристроїв потрібна активна підписка.</i>
ntf-extra-device-auto-renew-disabled = <i>✅ Автопродовження для додаткових пристроїв вимкнено. Пристрої буде видалено після закінчення терміну дії.</i>
ntf-extra-device-deleted = <i>✅ Додаткові пристрої видалено. Ліміт пристроїв оновлено.</i>ntf-extra-device-decreased = <i>✅ Додатковий пристрій видалено. Ліміт пристроїв зменшено.</i>ntf-extra-device-marked-deletion = <i>🗑 Пристрій позначено на видалення та не буде враховуватися при продовженні підписки.</i>
ntf-extra-slot-deleted = <i>✅ Додатковий слот видалено. Ліміт пристроїв зменшено.</i>
ntf-device-deleted = <i>✅ Пристрій успішно видалено зі списку!</i>
ntf-device-connected = <i>✅ Пристрій успішно підключено до підписки!</i>
ntf-extra-device-expired = <i>⚠️ Термін дії { $device_count } додаткових пристроїв закінчився. Ліміт пристроїв зменшено.</i>
ntf-extra-device-renewed = <i>✅ Автопродовження { $device_count } додаткових пристроїв успішне! { $price } ₽ списано з балансу.</i>

# Bonus Activation
ntf-bonus-activated = <i>✅ Бонуси активовано! { $amount } ₽ додано на ваш баланс.</i>
ntf-bonus-activate-no-balance = <i>❌ У вас недостатньо бонусів для активації цієї суми.</i>
ntf-bonus-activate-failed = <i>❌ Помилка активації бонусів. Спробуйте ще раз.</i>
ntf-bonus-invalid-amount = <i>❌ Сума повинна бути більше нуля.</i>
ntf-bonus-amount-exceeds = <i>❌ Сума не може перевищувати доступний баланс ({ $available } ₽).</i>
ntf-bonus-invalid-format = <i>❌ Будь ласка, введіть правильне число.</i>
ntf-extra-device-expired-no-balance = <i>⚠️ Недостатньо коштів для продовження { $device_count } додаткових пристроїв (потрібно { $price } ₽). Пристрої деактивовано.</i>
ntf-bonus-activate-no-selection = <i>⚠️ Виберіть суму для активації.</i>

# Hardcoded strings - UI notifications
ntf-click-start = Натисніть /start для продовження.
ntf-delete-msg-error = Не вдалося видалити повідомлення
ntf-import-in-dev = Імпорт в розробці.
ntf-convert-in-dev = Функція конвертації ще не реалізована.
ntf-file-not-found = Файл не знайдено
ntf-backup-deleted = Резервну копію видалено
ntf-delete-error = Помилка видалення
ntf-in-development = В розробці...

# System - Update notification
ntf-system-update-available =
    ✅ Поточна версія: <code>{ $current_version }</code>
    ⬆️ Доступна версія: <code>{ $new_version }</code>

    Натисніть <b>«Оновити зараз»</b> або запустіть оновлення через меню керування ботом.

ntf-no-subscription-for-devices = <i>⚠️ Вам необхідно отримати підписку.</i>

ntf-no-subscription-for-connect = <i>⚠️ Вам необхідно отримати підписку.</i>


# Referral code change
ntf-ref-code-invalid =
    ❌ <b>Недопустимий код.</b>
    Використовуйте лише: A–Z, a–z, 0–9, _ -
    Довжина: 3–32 символи.
ntf-ref-code-taken = ❌ Цей код вже зайнятий іншим користувачем. Оберіть інший.
ntf-ref-code-success = ✅ Реферальний код змінено на <code>{ $referral_code }</code>

# Admin balance change notification
ntf-event-admin-balance-change =
    🧑‍💻 <b>Система: Зміна балансу адміністратором!</b>

    <b>👤 Адміністратор:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $admin_id }</code>
    • <b>Ім'я</b>: { $admin_name }
    { $admin_username ->
        [false] {""}
        *[other] • <b>Username</b>: @{ $admin_username }
    }
    </blockquote>

    <b>👤 Користувач:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $target_id }</code>
    • <b>Ім'я</b>: { $target_name }
    { $target_username ->
        [false] {""}
        *[other] • <b>Username</b>: @{ $target_username }
    }
    </blockquote>

    <b>💰 Деталі:</b>
    <blockquote>
    • <b>Баланс</b>: { $balance_type ->
        [MAIN] 💰 Основний
        *[REFERRAL] 🎁 Бонусний
    }
    • <b>Операція</b>: { $operation ->
        [ADD] ➕ Нарахування
        *[SUB] ➖ Списання
    }
    • <b>Сума</b>: { $amount } ₽
    • <b>Баланс після</b>: { $new_balance } ₽
    </blockquote>
