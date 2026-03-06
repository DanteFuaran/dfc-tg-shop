# Errors
ntf-error-lost-context = <i>⚠️ Произошла ошибка. Диалог перезапущен.</i>
ntf-error-log-not-found = <i>⚠️ Ошибка: Лог файл не найден.</i>

# Database Export
ntf-db-export-start = <i>💾 Начинаю экспорт базы данных...</i>
ntf-db-export-success = 
    <i>✅ База данных успешно сохранена!</i>
    
    <b>Путь:</b> <code>{ $path }</code>
    
    <i>Файл можно открыть в DB Browser (SQLite)</i>
ntf-db-export-error = 
    <i>❌ Ошибка при экспорте базы данных:</i>
    
    <blockquote>{ $error }</blockquote>
ntf-db-save-success = <i>✅ Бэкап базы данных успешно сохранён!</i>
ntf-db-save-failed = <i>❌ Ошибка при сохранении бэкапа базы данных.</i>
ntf-db-convert-success = <i>✅ Файл был сконвертирован!</i>
ntf-db-convert-in-progress = ⚠️ Происходит конвертация в SQL...
ntf-db-convert-in-progress = <i>⚠️ Происходит конвертация в SQL</i>
ntf-db-restore-success =
    <i>✅ База данных успешно восстановлена из загруженного дампа.</i>

ntf-db-restore-failed =
    <i>❌ Ошибка при восстановлении базы данных.</i>

ntf-db-sync-completed = <i>✅ Восстановление базы данных завершено!</i>
ntf-db-sync-title = ✅ <b>Восстановление завершено!</b>
ntf-db-sync-skipped-title = <b>⊘ Пропущены пользователи без подписок:</b>
ntf-db-sync-errors-title = <b>❌ Ошибки синхронизации:</b>
ntf-db-sync-stats-title = <b>📊 Итого:</b>
ntf-db-sync-stats-total = Всего в боте: { $total }
ntf-db-sync-stats-created = Создано: { $created }
ntf-db-sync-stats-updated = Обновлено: { $updated }
ntf-db-sync-stats-skipped = Пропущено: { $skipped }
ntf-db-sync-stats-errors = Ошибок: { $errors }
ntf-db-sync-error = ❌ Ошибка синхронизации: { $error }
ntf-db-import-started = <i>⚠️ Происходит импорт базы данных. Ожидайте...</i>
ntf-db-import-failed = <i>❌ Ошибка при импорте базы данных.</i>
ntf-db-restore-preparing = <i>🔄 Идет подготовка к восстановлению данных...</i>

# Database Clear
ntf-db-clear-all-warning = 
    <b>⚠️ Нажмите еще раз, чтобы подтвердить действие.</b>

ntf-db-clear-all-start = <i>🗑 Производится полная очистка базы данных...</i>
ntf-db-clear-all-success = 
    <b>✅ Удаление завершено!</b>
    
    <blockquote>
    📊 Удалено записей:
    • Пользователи: <b>{ $users }</b>
    • Доп. устройства: <b>{ $extra_device_purchases }</b>
    • Рефералы: <b>{ $referrals }</b>
    • Тарифные планы: <b>{ $plans }</b>
    • Промокоды: <b>{ $promocodes }</b>
    </blockquote>
ntf-db-clear-all-failed = 
    <i>❌ Ошибка при очистке базы данных:</i>
    
    <blockquote>{ $error }</blockquote>

ntf-db-clear-users-warning = 
    <b>⚠️ Нажмите еще раз, чтобы подтвердить действие.</b>

ntf-db-clear-users-start = <i>🗑 Производится удаление пользователей...</i>
ntf-db-clear-users-success = 
    <b>✅ Удаление завершено!</b>
    
    <blockquote>
    📊 Итого:
    • Удалено: <b>{ $users }</b>
    • Пропущено: <b>0</b>
    • Ошибок: <b>0</b>
    </blockquote>
ntf-db-clear-users-failed = 
    <i>❌ Ошибка при удалении пользователей:</i>
    
    <blockquote>{ $error }</blockquote>

# Existing subscription import notifications
ntf-existing-subscription-found =
    <i>✅ Найдена существующая подписка!</i>
    
    <blockquote>
    У вас уже есть подписка в панели управления.
    Она была успешно привязана к вашему аккаунту.
    
    • <b>Тариф:</b> { $plan_name }
    • <b>Тег:</b> { $tag }
    </blockquote>
    
ntf-existing-subscription-no-plan =
    <i>⚠️ Найдена существующая подписка!</i>
    
    <blockquote>
    У вас уже есть подписка в панели управления.
    Однако соответствующий тариф не найден в боте.
    
    • <b>Текущий тег:</b> { $old_tag }
    • <b>Новый тег:</b> IMPORT
    
    Обратитесь к администратору для настройки подписки.
    </blockquote>

# Sync notifications
ntf-sync-preparing = <i>🔄 Подготовка данных к импорту...</i>
ntf-sync-started = <i>🔄 Синхронизация данных. Ожидайте...</i>
ntf-sync-completed =
    <i>✅ Синхронизация завершена!</i>
    
    <blockquote>
    Направление: <b>{ $direction ->
        [bot_to_panel] Бот → Панель
        *[panel_to_bot] Панель → Бот
    }</b>
    Синхронизировано: <b>{ $synced }</b>
    Создано: <b>{ $created }</b>
    Ошибок: <b>{ $errors }</b>
    </blockquote>
ntf-sync-failed =
    <i>❌ Ошибка синхронизации:</i>
    
    <blockquote>{ $error }</blockquote>

# Balance transfer notifications
ntf-balance-transfer-received =
    <i>💸 Вам перевели средства!</i>
    
    <b>📋 Детали перевода:</b>
    <blockquote>• Отправитель: <b>{ $sender }</b>
    • Сумма: <b>{ $amount } ₽</b>
    • Комиссия: С отправителя{ $has_message ->
        [0] {""}
       *[1] {""}
    </blockquote>
    <b>💬 Сообщение:</b>
    <blockquote>• <i>{ $message }</i>
    }
    </blockquote>
ntf-balance-transfer-insufficient = <i>⚠️ Недостаточно средств! Требуется: { $required }, на балансе: { $balance }</i>
ntf-balance-transfer-invalid-id = <i>⚠️ Telegram ID должен содержать только цифры!</i>
ntf-balance-transfer-user-not-found = <i>⚠️ Пользователь не найден!</i>
ntf-balance-transfer-self = <i>⚠️ Нельзя перевести средства самому себе!</i>
ntf-balance-transfer-disabled = <i>⚠️ Функция переводов отключена!</i>
ntf-balance-transfer-amount-range = <i>⚠️ Сумма перевода должна быть от { $min } до { $max } ₽</i>
ntf-balance-transfer-incomplete = <i>⚠️ Необходимо указать получателя и сумму перевода!</i>
ntf-balance-transfer-success =
    <i>✅ Перевод выполнен!</i>
    
    <b>📋 Детали перевода:</b>
    <blockquote>• Получатель: <b>{ $recipient }</b>
    • Сумма: <b>{ $amount } ₽</b>
    • Комиссия: <b>{ $commission } ₽</b>{ $has_message ->
        [0] {""}
       *[1] {""}
    </blockquote>
    <b>💬 Сообщение:</b>
    <blockquote>• <i>{ $message }</i>
    }
    </blockquote>
ntf-balance-transfer-error = <i>⚠️ Ошибка при выполнении перевода!</i>

ntf-balance-invalid-amount = 
    <i>⚠️ Доступна сумма пополнения от { $min_amount } до { $max_amount } ₽.</i>
ntf-bonus-insufficient = <i>⚠️ Недостаточно бонусов!</i>
ntf-bonus-activated = <i>✅ { $amount } ₽ зачислено на баланс!</i>
ntf-balance-withdraw-in-development = 🚧 Автоматическая функция вывода средств находится в разработке. Для вывода средств, обратитесь в поддержку.
ntf-invite-link-copied = <i>⚠️ Ссылка скопирована в буфер обмена.</i>


# Events
ntf-event-error =
    🤖 <b>Система: Произошла ошибка!</b>
    
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
    🤖 <b>Система: Ошибка при подключении к Remnawave!</b>

    <blockquote>
    Без активного подключения корректная работа бота невозможна!
    </blockquote>

    { hdr-error }
    <blockquote>
    { $error }
    </blockquote>

ntf-event-error-webhook =
    🤖 <b>Система: Зафиксирована ошибка вебхука!</b>

    { hdr-error }
    <blockquote>
    { $error }
    </blockquote>

ntf-event-bot-startup =
    🤖 <b>Система: Бот запущен!</b>

    <blockquote>
    • <b>Режим доступа</b>: { access-mode }
    • <b>Покупки</b>: { $purchases_allowed ->
    [0] запрещены
    *[1] разрешены
    }.
    • <b>Регистрация</b>: { $registration_allowed ->
    [0] запрещена
    *[1] разрешена
    }.
    </blockquote>

ntf-event-bot-shutdown =
    🤖 <b>Система: Бот остановлен!</b>

ntf-event-bot-started =
    🤖 <b>Система: Бот включен!</b>

ntf-event-bot-update =
    🤖 <b>Система: Обнаружено обновление DFC Shop!</b>

    <blockquote>
    • <b>Текущая версия</b>: { $local_version }
    • <b>Доступная версия</b>: { $remote_version }
    </blockquote>

ntf-event-new-user =
    🤖 <b>Система: Новый пользователь!</b>

    { hdr-user }
    { frg-user-info }

    { $has_referrer ->
    [0] { empty }
    *[HAS]
    <b>🤝 Реферер:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $referrer_user_id }</code>
    • <b>Имя</b>: { $referrer_user_name } { $referrer_username -> 
        [0] { empty }
        *[HAS] (<a href="tg://user?id={ $referrer_user_id }">@{ $referrer_username }</a>)
    }
    </blockquote>
    }

ntf-event-referral-upgrade =
    🤖 <b>Система: Регистрация в реф.системе!</b>

    { hdr-user }
    { frg-user-info }

    <b>🤝 Реферер:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $referrer_user_id }</code>
    • <b>Имя</b>: { $referrer_user_name } { $referrer_username -> 
        [0] { empty }
        *[HAS] (<a href="tg://user?id={ $referrer_user_id }">@{ $referrer_username }</a>)
    }
    </blockquote>

ntf-event-promocode-activated =
    🤖 <b>Система: Активация промокода!</b>

    { hdr-user }
    { frg-user-info }

    <b>🎟️ Промокод:</b>
    <blockquote>
    • <b>Код</b>: <code>{ $promocode_code }</code>
    • <b>Награда</b>: { $promocode_reward_type ->
        [PURCHASE_DISCOUNT] { $promocode_reward }% скидка на покупку
        [PERSONAL_DISCOUNT] { $promocode_reward }% постоянная скидка
        [DURATION] +{ $promocode_reward } дней к подписке
        *[OTHER] { $promocode_reward } { $promocode_reward_type }
    }
    </blockquote>

ntf-event-test-webhook-success =
    🤖 <b>Система: Тестовый webhook успешен!</b>

    <b>💳 Платёжный шлюз:</b>
    <blockquote>
    • <b>Название</b>: { $gateway_name }
    • <b>Тип</b>: <code>{ $gateway_type }</code>
    </blockquote>

    <i>Тестовое уведомление получено и обработано успешно.</i>

ntf-event-test-webhook-failed =
    🤖 <b>Система: Ошибка тестового webhook!</b>

    <b>💳 Платёжный шлюз:</b>
    <blockquote>
    • <b>Тип</b>: <code>{ $gateway_type }</code>
    </blockquote>

    <b>⚠️ Ошибка:</b>
    <blockquote>
    • <b>Тип</b>: <code>{ $error_type }</code>
    • <b>Сообщение</b>: { $error_message }
    </blockquote>
    
ntf-event-subscription-trial =
    🤖 <b>Система: Получение пробной подписки!</b>

    { hdr-user }
    { frg-user-info }
    
    { hdr-plan }
    { frg-plan-snapshot }

ntf-event-subscription-new =
    🤖 <b>Система: Покупка подписки!</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot }

ntf-event-subscription-renew =
    🤖 <b>Система: Продление подписки!</b>
    
    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot }

    { $has_extra_devices ->
        [1] 

    <b>📱 Доп. устройства:</b>
    <blockquote>
    • <b>Количество</b>: { $extra_devices_count }
    • <b>Стоимость</b>: { $extra_devices_cost }
    </blockquote>
        *[0] {""}
    }

ntf-event-subscription-change =
    🤖 <b>Система: Изменение подписки!</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot-comparison }

ntf-event-balance-topup =
    🤖 <b>Система: Пополнение баланса!</b>

    <blockquote>
    • <b>ID</b>: <code>{ $payment_id }</code>
    • <b>Способ оплаты</b>: { gateway-type }
    • <b>Сумма</b>: { $final_amount }
    </blockquote>

    { hdr-user }
    { frg-user-info }

ntf-event-extra-devices =
    🤖 <b>Система: Покупка дополнительных устройств!</b>

    <blockquote>
    • <b>ID</b>: <code>{ $payment_id }</code>
    • <b>Способ оплаты</b>: { gateway-type }
    • <b>Сумма</b>: { $final_amount }
    • <b>Скидка</b>: { $discount_percent }%
    • <b>Устройств</b>: +{ $device_count } шт.
    </blockquote>

    { hdr-subscription }
    { frg-subscription-details }

    { hdr-user }
    { frg-user-info }

ntf-event-extra-devices-balance =
    🤖 <b>Система: Покупка дополнительных устройств!</b>

    <blockquote>
    • <b>Способ оплаты</b>: 💰 С баланса
    • <b>Сумма</b>: { $price } ₽
    • <b>Скидка</b>: { $discount_percent }%
    • <b>Устройств</b>: +{ $device_count } шт.
    </blockquote>

    { hdr-user }
    { frg-user-info }

ntf-event-extra-devices-deletion =
    🤖 <b>Система: Удаление дополнительных устройств!</b>

    { hdr-user }
    { frg-user-info }

    <blockquote>
    • <b>Устройств</b>: -{ $device_count } шт.
    • <b>Удаление через</b>: { $delete_after }
    </blockquote>

ntf-event-balance-transfer =
    🤖 <b>Система: Финансовый перевод!</b>

    <b>👤 Отправитель:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $sender_id }</code>
    • <b>Имя</b>: { $sender_name }
    • <b>Баланс после</b>: { $sender_balance } ₽
    </blockquote>

    <b>👤 Получатель:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $recipient_id }</code>
    • <b>Имя</b>: { $recipient_name }
    • <b>Баланс после</b>: { $recipient_balance } ₽
    </blockquote>

    <b>💰 Детали перевода:</b>
    <blockquote>
    • <b>Сумма</b>: { $amount } ₽
    • <b>Комиссия</b>: { $commission } ₽
    • <b>Всего списано</b>: { $total } ₽{ $has_message ->
        [0] {""}
       *[1] {""}
    • <b>Сообщение</b>: <i>{ $message }</i>
    }
    </blockquote>

ntf-event-node-connection-lost =
    🤖 <b>Система: Соединение с узлом потеряно!</b>

    { hdr-node }
    { frg-node-info }

ntf-event-node-connection-restored =
    🤖 <b>Система: Cоединение с узлом восстановлено!</b>

    { hdr-node }
    { frg-node-info }

ntf-event-node-traffic =
    🤖 <b>Система: Узел достиг порога лимита трафика!</b>

    { hdr-node }
    { frg-node-info }

# ntf-event-user-sync =
#     #EventUser

#     🤖 <b>Система: Синхронизация пользователя!</b>

#     { hdr-user }
#     { frg-user-info }

#     { hdr-subscription }
#     { frg-subscription-details }

# ntf-event-user-deleted =
#     #EventUser

#     🤖 <b>Система: Пользователь удален из панели!</b>

#     { hdr-user }
#     { frg-user-info }

#     { hdr-subscription }
#     { frg-subscription-details }

ntf-event-user-first-connected =
    🤖 <b>Система: Первое подключение пользователя!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-subscription }
    { frg-subscription-details }

ntf-event-user-not-connected =
    🤖 <b>Система: Пользователь не подключился!</b>

    <blockquote>
    Пользователь зарегистрировался { $hours } ч. назад, но не оформил подписку.
    Возможно, ему нужна помощь.
    </blockquote>

    { hdr-user }
    { frg-user-info }
    
    <b>📅 Дата регистрации:</b> { $registered_at }

ntf-event-user-expiring =
    { $is_trial ->
    [0]
    <b>⚠️ Внимание! Ваша подписка закончится через { unit-day }.</b>
    
    Продлите ее заранее, чтобы не терять доступ к сервису! 
    *[1]
    <b>⚠️ Внимание! Ваш бесплатный пробник закончится через { unit-day }.</b>

    Оформите подписку, чтобы не терять доступ к сервису! 
    }

ntf-event-user-expired =
    <b>⛔ Внимание! Доступ приостановлен.</b>

    { $is_trial ->
    [0] Ваша подписка истекла, продлите ее, чтобы продолжить пользоваться сервисом!
    *[1] Ваш бесплатный пробный период закончился. Оформите подписку, чтобы продолжить пользоваться сервисом!
    }
    
ntf-event-user-expired-ago =
    <b>⛔ Внимание! Доступ приостановлен.</b>

    { $is_trial ->
    [0] Ваша подписка истекла { unit-day } назад, продлите ее, чтобы продолжить пользоваться сервисом!
    *[1] Ваш бесплатный пробный период закончился { unit-day } назад. Оформите подписку, чтобы продолжить пользоваться сервисом!
    }

ntf-event-user-limited =
    <b>⛔ Внимание! Доступ приостановлен - VPN не работает.</b>

    Ваш трафик израсходован. { $is_trial ->
    [0] { $traffic_strategy ->
        [NO_RESET] Продлите подписку, чтобы сбросить трафик и продолжить пользоваться сервисом!
        *[RESET] Трафик будет восстановлен через { $reset_time }. Вы также можете продлить подписку, чтобы сбросить трафик.
        }
    *[1] { $traffic_strategy ->
        [NO_RESET] Оформите подписку, чтобы продолжить пользоваться сервисом!
        *[RESET] Трафик будет восстановлен через { $reset_time }. Вы также можете оформить подписку, чтобы пользоваться сервисом без ограничений.
        }
    }

ntf-event-user-hwid-added =
    🤖 <b>Система: Пользователь добавил новое устройство!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-hwid }
    { frg-user-hwid }

ntf-event-user-hwid-deleted =
    🤖 <b>Система: Пользователь удалил устройство!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-hwid }
    { frg-user-hwid }

ntf-event-user-referral-attached =
    <b>🎉 Вы пригласили друга!</b>
    
    <blockquote>
    Пользователь <b>{ $name }</b> присоединился по вашей пригласительной ссылке! Чтобы получить награду, убедитесь, что он совершит покупку подписки.
    </blockquote>

ntf-event-user-referral-reward =
    <b>💰 Вам начислена награда!</b>
    
    <blockquote>
    Пользователь <b>{ $name }</b> совершил платеж. Вы получили <b>{ $value }{ $reward_type ->
        [MONEY] { space }{ $currency }
        [EXTRA_DAYS] { space }доп. { $value ->
            [one] день
            [few] дня
            *[other] дней
            }
        *[OTHER] { $currency }
    }</b> на реферальный баланс!
    </blockquote>

ntf-event-user-referral-reward-error =
    <b>❌ Не получилось выдать награду!</b>
    
    <blockquote>
    Пользователь <b>{ $name }</b> совершил платеж, но мы не смогли начислить вам вознаграждение из-за того что <b>у вас нет купленной подписки</b>, к которой можно было бы добавить {$value} { $value ->
            [one] доп. день
            [few] доп. дня
            *[more] доп. дней
        }.
    
    <i>Купите подписку, чтобы получать бонусы за приглашенных друзей!</i>
    </blockquote>


ntf-cashback-reward =
    <b>🎉 Поздравляем! Вы получаете кешбек!</b>

    <blockquote>
    Так как вы участвуете в реферальной программе, вы получаете дополнительный бонус к вашему платежу: <b>{ $value }{ $reward_type ->
        [MONEY] { space }{ $currency }
        [EXTRA_DAYS] { space }{ $value ->
            [one] доп. день
            [few] доп. дня
            *[other] доп. дней
            }
        *[OTHER] { $currency }
    }</b>!
    </blockquote>

# Notifications
ntf-command-paysupport = 💸 <b>Чтобы запросить возврат, обратитесь в нашу службу поддержки.</b>
ntf-command-help = 🆘 <b>Нажмите кнопку ниже, чтобы связаться с поддержкой. Мы поможем решить вашу проблему.</b>
ntf-channel-join-required = ❇️ Подпишитесь на наш канал и получайте <b>бесплатные дни, акции и новости</b>! После подписки нажмите кнопку «Подтвердить».
ntf-channel-join-required-left = ⚠️ Вы отписались от нашего канала! Подпишитесь, чтобы иметь возможность пользоваться ботом.
ntf-rules-accept-required = ⚠️ <b>Перед использованием сервиса, пожалуйста, ознакомьтесь и примите <a href="{ $url }">Условия использования</a> сервиса.</b>

ntf-double-click-confirm = <i>⚠️ Нажмите еще раз, чтобы подтвердить действие.</i>
ntf-user-referral-bind-not-found = <i>⚠️ Пользователь не найден.</i>
ntf-user-referral-bind-self = <i>⚠️ Нельзя привязать пользователя к самому себе.</i>
ntf-user-referral-bind-already = <i>⚠️ Этот пользователь уже является рефералом другого пользователя.</i>
ntf-user-referral-bind-success = <i>✅ Реферал успешно привязан.</i>
ntf-user-deleted = <i>✅ Пользователь удален.</i>
ntf-channel-join-error = <i>⚠️ Мы не видим вашу подписку на канал. Проверьте, что вы подписались, и попробуйте еще раз.</i>
ntf-throttling-many-requests = <i>⚠️ Вы отправляете слишком много запросов, пожалуйста, подождите немного.</i>
ntf-squads-empty = <i>⚠️ Сквады не найдены. Проверьте их наличие в панели.</i>
ntf-invite-withdraw-points-error = ❌ У вас недостаточно баллов для выполнения обмена.
ntf-invite-withdraw-no-balance = ❌ У вас нет бонусов для перевода на баланс.
ntf-invite-withdraw-success = ✅ { $amount } ₽ успешно переведены на ваш основной баланс!

ntf-connect-not-available =
    ⚠️ { $status ->
    [LIMITED]
    Вы израсходовали весь доступный объем трафика. { $is_trial ->
    [0] { $traffic_strategy ->
        [NO_RESET] Продлите подписку, чтобы сбросить трафик и продолжить пользоваться сервисом!
        *[RESET] Трафик будет восстановлен через { $reset_time }. Вы также можете продлить подписку, чтобы сбросить трафик.
        }
    *[1] { $traffic_strategy ->
        [NO_RESET] Оформите подписку, чтобы продолжить пользоваться сервисом!
        *[RESET] Трафик будет восстановлен через { $reset_time }. Вы также можете оформить подписку, чтобы пользоваться сервисом без ограничений.
        }
    }
    [EXPIRED]  
    { $is_trial ->
    [0] Срок действия вашей подписки истек. Чтобы продолжить пользоваться сервисом, продлите подписку или оформите новую.
    *[1] Ваш бесплатный пробный период закончился. Оформите подписку, чтобы продолжить пользоваться сервисом!
    }
    *[OTHER] Произошла ошибка при проверке статуса или ваша подписка была отключена. Обратитесь в поддержку.
    }

ntf-user-not-found = <i>❌ Пользователь не найден.</i>
ntf-user-transactions-empty = <i>❌ Список транзакций пуст.</i>
ntf-user-subscription-empty = <i>❌ Текущая подписка не найдена.</i>
ntf-user-plans-empty = <i>❌ Нет доступных планов для выдачи.</i>
ntf-user-devices-empty = <i>❌ Список устройств пуст.</i>
ntf-user-invalid-number = <i>❌ Некорректное число.</i>
ntf-user-no-pending-amount = <i>⚠️ Сначала выберите сумму для начисления.</i>
ntf-user-device-limit-exceeded = <i>❌ Количество устройств не может быть больше 100.</i>
ntf-user-allowed-plans-empty = <i>❌ Нет доступных планов для предоставления доступа.</i>
ntf-user-message-success = <i>✅ Сообщение успешно отправлено.</i>
ntf-user-message-not-sent = <i>❌ Не удалось отправить сообщение.</i>
ntf-user-sync-already = <i>✅ Данные подписки совпадают.</i>
ntf-user-sync-missing-data = <i>⚠️ Синхронизация невозможна. Данные подписки отсутствуют и на панели, и в боте.</i>
ntf-user-sync-success = <i>✅ Синхронизация подписки выполнена.</i>

ntf-user-invalid-expire-time = <i>❌ Невозможно { $operation ->
    [ADD] продлить подписку на указанное количество дней
    *[SUB] уменьшить срок подписки на указанное количество дней
    }.</i>

ntf-user-invalid-points = <i>❌ Невозможно { $operation ->
    [ADD] добавить указанное количество баллов
    *[SUB] отнять указанное количество баллов
    }.</i>

ntf-user-invalid-balance = <i>❌ Невозможно { $operation ->
    [ADD] добавить указанную сумму на баланс
    *[SUB] отнять указанную сумму с баланса
    }.</i>

ntf-referral-invalid-reward = <i>❌ Некорректное значение.</i>

ntf-access-denied = <i>🚧 Бот в режиме обслуживания, попробуйте позже.</i>
ntf-access-denied-registration = <i>❌ Регистрация новых пользователей отключена.</i>
ntf-access-denied-only-invited = <i>❌ Регистрация новых пользователей доступна только через приглашение другим пользователем.</i>
ntf-access-denied-purchasing = <i>🚧 Оплата сервиса временно отключена, Вам придет уведомление когда оплаты будут доступны.</i>
ntf-payments-available-again = <i>✅ Оплата сервиса вновь доступна! Спасибо за ожидание!</i>
ntf-access-allowed = <i>❇️ Весь функционал бота снова доступен, спасибо за ожидание.</i>
ntf-access-id-saved = <i>✅ ID канала/группы успешно обновлен.</i>
ntf-access-link-saved = <i>✅ Ссылка на канал/группу успешно обновлена.</i>
ntf-access-channel-invalid = <i>❌ Некорректная ссылка или ID канала/группы.</i>

ntf-plan-invalid-name = <i>❌ Некорректное имя.</i>
ntf-plan-invalid-description = <i>❌ Некорректное описание.</i>
ntf-plan-invalid-tag = <i>❌ Некорректный тег.</i>
ntf-plan-invalid-number = <i>❌ Некорректное число.</i>
ntf-plan-trial-once-duration = <i>❌ Пробный план может иметь только одну длительность.</i>
ntf-plan-trial-already-exists = <i>❌ Пробный план уже существует.</i>
ntf-plan-duration-already-exists = <i>❌ Такая длительность уже существует.</i>
ntf-plan-duration-last = <i>❌ Нельзя удалить последнюю длительность.</i>
ntf-plan-save-error = <i>❌ Ошибка сохранения плана.</i>
ntf-plan-name-already-exists = <i>❌ План с таким именем уже существует.</i>
ntf-plan-invalid-user-id = <i>❌ Некорректный ID пользователя.</i>
ntf-plan-no-user-found = <i>❌ Пользователь не найден.</i>
ntf-plan-user-already-allowed = <i>❌ Пользователь уже добавлен в список разрешенных.</i>
ntf-plan-confirm-delete = <i>⚠️ Нажмите еще раз, чтобы удалить.</i>
ntf-plan-updated-success = <i>✅ План успешно обновлен.</i>
ntf-plan-created-success = <i>✅ План успешно создан.</i>
ntf-plan-deleted-success = <i>✅ План успешно удален.</i>
ntf-plan-tag-updated = <i>✅ Тег плана обновлен.</i>
ntf-plan-internal-squads-empty = <i>❌ Выберите хотя бы один внутренний сквад.</i>

ntf-gateway-not-configured = <i>❌ Платежный шлюз не настроен.</i>
ntf-gateway-not-configurable = <i>❌ Платежный шлюз не имеет настроек.</i>
ntf-gateway-field-wrong-value = <i>❌ Некорректное значение.</i>
ntf-gateway-test-payment-created = <i>✅ <a href="{ $url }">Тестовый платеж</a> успешно создан.</i>
ntf-gateway-test-payment-error = <i>❌ Произошла ошибка при создании тестового платежа.</i>
ntf-gateway-test-payment-confirmed = <i>✅ Тестовый платеж успешно обработан.</i>

ntf-subscription-plans-not-available = <i>❌ Нет доступных планов.</i>
ntf-subscription-gateways-not-available = <i>❌ Нет доступных платежных систем.</i>
ntf-subscription-renew-plan-unavailable = <i>❌ Ваш план устарел и не доступен для продления.</i>
ntf-subscription-change-plans-not-available = <i>❌ Нет доступных подписок для изменения. У вас уже активирована единственная доступная подписка.</i>
ntf-subscription-payment-creation-failed = <i>❌ Произошла ошибка при создании платежа, попробуйте позже.</i>
ntf-payment-gateway-not-configured = <i>❌ Не настроены данные мерчанта { $gateway_name }</i>
ntf-subscription-insufficient-balance = <i>❌ Недостаточно средств на балансе для оплаты подписки.</i>
ntf-check-payment-pending = <i>⏳ Оплата ещё не поступила. Если вы уже оплатили, подождите немного и попробуйте снова.</i>
ntf-check-payment-no-id = <i>❌ Не удалось найти данные платежа. Попробуйте создать платёж заново.</i>
ntf-check-payment-not-found = <i>❌ Транзакция не найдена. Попробуйте создать платёж заново.</i>

ntf-balance-payment-link = 
    <b>💳 Ссылка для оплаты</b>
    
    Перейдите по ссылке для оплаты:
    <a href="{ $payment_url }">Оплатить</a>

ntf-balance-topup-success = 
    ✅ <b>Баланс успешно пополнен!</b>
    
    На ваш баланс зачислено: <b>{ $amount } { $currency }</b>

ntf-broadcast-list-empty = <i>❌ Список рассылок пуст.</i>
ntf-broadcast-audience-not-available = <i>❌ Нет доступных пользователей для выбранной аудитории.</i>
ntf-broadcast-audience-not-active = <i>❌ Нет пользователей у которых есть АКТИВНАЯ подписка с данным планом.</i>
ntf-broadcast-plans-not-available = <i>❌ Нет доступных планов.</i>
ntf-broadcast-empty-content = <i>❌ Контент пустой.</i>
ntf-broadcast-wrong-content = <i>❌ Некорректный контент.</i>
ntf-broadcast-content-saved = <i>✅ Контент сообщения успешно сохранен.</i>
ntf-broadcast-preview = { $content }
ntf-invite-preview = { $content }
ntf-broadcast-not-cancelable = <i>❌ Рассылка не может быть отменена.</i>
ntf-broadcast-canceled = <i>✅ Рассылка успешно отменена.</i>
ntf-broadcast-deleting = <i>⚠️ Идет удаление всех отправленных сообщений.</i>
ntf-broadcast-already-deleted = <i>❌ Рассылка находится в процессе удаления или уже удалена.</i>

ntf-broadcast-deleted-success =
    ✅ Рассылка <code>{ $task_id }</code> успешно удалена.

    <blockquote>
    • <b>Всего сообщений</b>: { $total_count }
    • <b>Успешно удалено</b>: { $deleted_count }
    • <b>Не удалось удалить</b>: { $failed_count }
    </blockquote>

ntf-trial-unavailable = <i>❌ Пробная подписка временно недоступна.</i>
ntf-trial-already-used = <i>❌ Вы уже использовали пробную подписку.</i>
ntf-referral-code-invalid = <i>❌ Неверный реферальный код. Попробуйте еще раз.</i>
ntf-referral-code-self = <i>❌ Вы не можете использовать собственный реферальный код.</i>
ntf-referral-code-own-referral = <i>❌ Вы не можете использовать реферальный код приглашённого вами пользователя.</i>
ntf-referral-code-already-used = <i>❌ Вы уже использовали реферальную подписку.</i>
ntf-referral-code-already-has = <i>❌ Вы уже привязаны к рефереру. Повторная привязка невозможна.</i>
ntf-referral-code-success-promo = <i>✅ Вы успешно привязались к рефереру!</i>

ntf-importer-not-file = <i>⚠️ Отправьте базу данных в виде файла.</i>
ntf-importer-db-invalid = <i>❌ Этот файл не может быть импортирован.</i>
ntf-importer-db-failed = <i>❌ Ошибка при импорте базы данных.</i>
ntf-importer-exported-users-empty =  <i>❌ Список пользователей в базе данных пуст.</i>
ntf-importer-internal-squads-empty = <i>❌ Выберите хотя бы один внутренний сквад.</i>
ntf-importer-import-started = <i>✅ Импорт пользователей запущен, ожидайте...</i>
ntf-importer-sync-started = <i>🔄 Происходит синхронизация данных...</i>
ntf-importer-users-not-found = <i>❌ Не удалось найти пользователей для синхронизации.</i>
ntf-importer-not-support = <i>⚠️ Импорт всех данных из 3xui-shop временно недоступен. Вы можете воспользоваться импортом из панели 3X-UI!</i>
ntf-importer-sync-already-running = <i>⚠️ Синхронизация пользователей уже была запущена, ожидайте...</i>

ntf-importer-sync-bot-to-panel-completed =
    <b>📤 Синхронизация завершена</b>

    <blockquote>
    <b>Всего в боте:</b> { $total_bot_users }
    <b>Создано:</b> { $created }
    <b>Обновлено:</b> { $updated }
    <b>Пропущено:</b> { $skipped }
    <b>Ошибок:</b> { $errors }
    </blockquote>

ntf-sync-panel-to-bot-completed =
    <b>📥 Синхронизация завершена</b>

    <blockquote>
    <b>Всего в панели:</b> { $total_panel_users }
    <b>Создано:</b> { $created }
    <b>Синхронизировано:</b> { $synced }
    <b>Пропущено:</b> { $skipped }
    <b>Ошибок:</b> { $errors }
    </blockquote>

# Remnawave Sync notifications
ntf-remnawave-sync-confirm = <i>⚠️ Нажмите еще раз для подтверждения импорта.</i>
ntf-remnawave-sync-preparing = <i>🔄 Подготовка данных к импорту...</i>
ntf-remnawave-sync-started = <i>🔄 Синхронизация данных...</i>
ntf-remnawave-sync-no-users = <i>❌ Не найдено пользователей для импорта.</i>
ntf-remnawave-sync-failed =
    <i>❌ Ошибка импорта:</i>

    <blockquote>{ $error }</blockquote>
ntf-remnawave-sync-bot-to-panel-completed =
    <b>✅ Синхронизация из Бота в панель завершена</b>

    <blockquote>
    <b>Всего в боте:</b> { $total_bot_users }
    <b>Создано:</b> { $created }
    <b>Обновлено:</b> { $updated }
    <b>Пропущено:</b> { $skipped }
    <b>Ошибок:</b> { $errors }
    </blockquote>
ntf-remnawave-sync-panel-to-bot-completed =
    <b>✅ Синхронизация из Remnawave в Бота завершена</b>

    <blockquote>
    <b>Всего в панели:</b> { $total_panel_users }
    <b>Создано:</b> { $created }
    <b>Синхронизировано:</b> { $synced }
    <b>Пропущено:</b> { $skipped }
    <b>Ошибок:</b> { $errors }
    </blockquote>

ntf-remnawave-import-completed =
    <b>✅ Импорт из Remnawave завершен</b>

    <blockquote>
    <b>Всего в панели:</b> { $total_panel_users }
    <b>Всего в боте:</b> { $total_bot_users }
    <b>Добавлено пользователей:</b> { $added_users }
    <b>Добавлено подписок:</b> { $added_subscription }
    <b>Обновлено:</b> { $updated }
    <b>Без Telegram ID:</b> { $missing_telegram }
    <b>Ошибок:</b> { $errors }
    </blockquote>

ntf-subscription-processing = <i>⏳ Оформляем вашу подписку, пожалуйста подождите...</i>

# Promocodes
ntf-promocode-not-found = <i>❌ Промокод не найден.</i>
ntf-promocode-inactive = <i>⚠️ Промокод неактивен.</i>
ntf-promocode-already-activated = <i>⚠️ Вы уже использовали этот промокод.</i>
ntf-promocode-limit-exceeded = <i>⚠️ Промокод исчерпан.</i>
ntf-promocode-plan-unavailable = <i>⚠️ Промокод недоступен для вашего тарифа.</i>
ntf-promocode-activation-error = <i>❌ Ошибка при активации промокода.</i>
ntf-promocode-activated = <i>✅ Промокод <code>{$promocode}</code> успешно активирован!</i>
ntf-promocode-invalid-name = <i>❌ Название промокода должно быть от 1 до 50 символов.</i>
ntf-promocode-already-exists = <i>❌ Промокод с таким кодом уже существует.</i>
ntf-promocode-invalid-code = <i>❌ Код промокода должен быть от 3 до 20 символов.</i>
ntf-promocode-invalid-reward = <i>❌ Введите корректное значение награды (положительное число).</i>
ntf-promocode-invalid-lifetime = <i>❌ Введите корректный срок действия (0 = неограничено).</i>
ntf-promocode-invalid-quantity = <i>❌ Введите корректное количество активаций (0 = неограничено).</i>
ntf-promocode-created = <i>✅ Промокод успешно создан.</i>
ntf-promocode-updated = <i>✅ Промокод успешно обновлён.</i>
ntf-promocode-save-error = <i>❌ Ошибка при сохранении промокода.</i>
ntf-promocode-delete-error = <i>❌ Ошибка при удалении промокода.</i>
ntf-promocode-delete-success = <i>✅ Промокод был успешно удален!</i>

# Devices
ntf-add-device-info = <i>ℹ️ Добавление устройства увеличит стоимость подписки на <b>{ $price } ₽/мес</b>.</i>
ntf-add-device-success = <i>✅ Новый лимит устройст применен!</i>
ntf-add-device-payment-pending = <i>⏳ Оплата через выбранную платёжную систему временно недоступна для добавления устройств. Используйте баланс.</i>
ntf-payment-link = <i>💳 <a href="{ $payment_url }">Перейти к оплате</a></i>
ntf-payment-creation-failed = <i>❌ Произошла ошибка при создании платежа, попробуйте позже.</i>
ntf-payment-gateway-not-available = <i>❌ Выбранная платёжная система временно недоступна. Попробуйте позже.</i>
ntf-subscription-required = <i>❌ Для добавления устройства необходима активная подписка.</i>
ntf-extra-device-auto-renew-disabled = <i>✅ Автопродление дополнительных устройств отключено. Устройства будут удалены по истечению срока.</i>
ntf-extra-device-deleted = <i>✅ Дополнительные устройства удалены. Лимит устройств обновлён.</i>
ntf-extra-device-decreased = <i>✅ Дополнительное устройство удалено. Лимит устройств уменьшен.</i>
ntf-extra-device-marked-deletion = <i>🗑 Устройство поставлено на удаление и не будет учитываться при продлении подписки.</i>
ntf-extra-slot-deleted = <i>✅ Дополнительный слот удалён. Лимит устройств уменьшен.</i>
ntf-device-deleted = <i>✅ Устройство было успешно удалено из списка!</i>
ntf-device-connected = <i>✅ Устройство успешно подключено к подписке!</i>
ntf-extra-device-expired = <i>⚠️ Срок действия { $device_count } доп. устройств истёк. Лимит устройств уменьшен.</i>
ntf-extra-device-renewed = <i>✅ Автопродление { $device_count } доп. устройств успешно! Списано { $price } ₽ с баланса.</i>

# Bonus Activation
ntf-bonus-activated = <i>✅ Бонусы активированы! На ваш баланс добавлено { $amount } ₽.</i>
ntf-bonus-activate-no-balance = <i>❌ У вас недостаточно бонусов для активации этой суммы.</i>
ntf-bonus-activate-failed = <i>❌ Ошибка при активации бонусов. Попробуйте снова.</i>
ntf-bonus-invalid-amount = <i>❌ Сумма должна быть больше нуля.</i>
ntf-bonus-amount-exceeds = <i>❌ Сумма не может быть больше доступного баланса ({ $available } ₽).</i>
ntf-bonus-invalid-format = <i>❌ Пожалуйста, введите корректное число.</i>
ntf-extra-device-expired-no-balance = <i>⚠️ Недостаточно средств для продления { $device_count } доп. устройств (нужно { $price } ₽). Устройства деактивированы.</i>
ntf-bonus-activate-no-selection = <i>⚠️ Выберите сумму для активации.</i>

# Hardcoded strings - UI notifications
ntf-click-start = Нажмите /start для продолжения.
ntf-delete-msg-error = Не удалось удалить сообщение
ntf-import-in-dev = Импорт в разработке.
ntf-convert-in-dev = Функция конвертации пока не реализована.
ntf-file-not-found = Файл не найден
ntf-backup-deleted = Бэкап удален
ntf-delete-error = Ошибка удаления
ntf-in-development = Находится в разработке...

# System - Update notification
ntf-system-update-available =
    ✅ Текущая версия: <code>{ $current_version }</code>
    ⬆️ Доступна версия: <code>{ $new_version }</code>

    Нажмите <b>«Обновить сейчас»</b> или запустите обновление через меню управления ботом.

ntf-no-subscription-for-devices = <i>⚠️ Вам необходимо получить подписку.</i>

ntf-no-subscription-for-connect = <i>⚠️ Вам необходимо получить подписку.</i>


# Referral code change
ntf-ref-code-invalid =
    ❌ <b>Недопустимый код.</b>
    Используйте только: A–Z, a–z, 0–9, _ -
    Длина: 3–32 символа.
ntf-ref-code-taken = ❌ Этот код уже занят другим пользователем. Выберите другой.
ntf-ref-code-success = ✅ Реферальный код изменён на <code>{ $referral_code }</code>

# Admin balance change notification
ntf-event-admin-balance-change =
    🧑‍💻 <b>Система: Изменение баланса администратором!</b>

    <b>👤 Администратор:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $admin_id }</code>
    • <b>Имя</b>: { $admin_name }
    { $admin_username ->
        [false] {""}
        *[other] • <b>Username</b>: @{ $admin_username }
    }
    </blockquote>

    <b>👤 Пользователь:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $target_id }</code>
    • <b>Имя</b>: { $target_name }
    { $target_username ->
        [false] {""}
        *[other] • <b>Username</b>: @{ $target_username }
    }
    </blockquote>

    <b>💰 Детали:</b>
    <blockquote>
    • <b>Баланс</b>: { $balance_type ->
        [MAIN] 💰 Основной
        *[REFERRAL] 🎁 Бонусный
    }
    • <b>Операция</b>: { $operation ->
        [ADD] ➕ Начисление
        *[SUB] ➖ Списание
    }
    • <b>Сумма</b>: { $amount } ₽
    • <b>Баланс после</b>: { $new_balance } ₽
    </blockquote>
