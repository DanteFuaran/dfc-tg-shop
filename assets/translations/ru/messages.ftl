# Database Management
msg-db-main =
    <b>🗄 Управление базой данных</b>

    <blockquote>
    • <b>Сохранить</b> - создать резервную копию базы
    • <b>Загрузить</b> - восстановить базу из бэкапа
    • <b>Очистить всё</b> - удалить все данные из базы
    • <b>Очистить пользователей</b> - удалить только пользователей
    • <b>Синхронизация</b> - синхронизировать данные между ботом и панелью
    </blockquote>

    <b>🔽 Выберите действие:</b>
    
msg-db-clear-all-confirm =
    <b>⚠️ ВНИМАНИЕ!</b>

    <blockquote>
    Вы собираетесь <b>полностью очистить базу данных</b>.
    
    Будут удалены:
    • Все пользователи
    • Все подписки
    • Все транзакции
    • Все промокоды и их активации
    • Все рефералы и награды
    • Все уведомления
    </blockquote>

    <b>⚠️ Это действие необратимо!</b>
    
    <i>Нажмите кнопку повторно для подтверждения очистки.</i>

msg-db-clear-users-confirm =
    <b>⚠️ ВНИМАНИЕ!</b>

    <blockquote>
    Вы собираетесь <b>удалить всех пользователей</b> из базы данных.
    
    Будут удалены:
    • Все пользователи
    • Все подписки пользователей
    • Все транзакции пользователей
    • Все активации промокодов
    • Все рефералы и награды
    </blockquote>

    <b>⚠️ Это действие необратимо!</b>
    
    <i>Нажмите кнопку ниже повторно для подтверждения.</i>

msg-db-clear-users-result =
    <b>✅ Удаление пользователей завершено успешно!</b>

    <blockquote>
    📊 Итого:
    • Пользователи: <b>{ $users }</b>
    • Подписки: <b>{ $subscriptions }</b>
    • Транзакции: <b>{ $transactions }</b>
    • Активации: <b>{ $activations }</b>
    • Рефералы: <b>{ $referrals }</b>
    • Награды: <b>{ $rewards }</b>
    </blockquote>

msg-db-clear-users-failed =
    <b>❌ Ошибка при удалении пользователей</b>

    { $error }

msg-db-imports =
    <b>📥 Импорт</b>

    Выберите источник для импорта пользователей:

msg-db-load =
    <b>📁 Выбор файла загрузки</b>

msg-db-sync =
    <b>🔄 Синхронизация данных</b>

    <blockquote>    
    • <b>Из панели в бота</b>
    Данные пользователей из панели будут обновлены в боте.
    Если пользователя нет в боте, он будет создан.
    
    • <b>Из бота в панель</b>
    Данные пользователей из бота будут обновлены в панели.
    Если пользователя нет в панели, он будет создан.
    </blockquote>

    <i>⚠️ Синхронизация может занять некоторое время. </i>

msg-db-sync-progress =
    <b>🔄 Синхронизация...</b>

    <blockquote>
    Пожалуйста, подождите. Синхронизация выполняется в фоновом режиме.
    Вы получите уведомление по завершении.
    </blockquote>

msg-db-import =
    <b>📥 Импорт из SQLite</b>
    
    Выберите файл для импорта:

msg-db-restore-success =
    <b>✅ База данных успешно восстановлена из загруженного дампа.</b>

msg-db-restore-failed =
    <b>❌ Ошибка при восстановлении базы: { $error }</b>

# Settings
msg-dashboard-settings =
    <b>⚙️ Настройки</b>

    🔽 Выберите интересующий параметр:

msg-dashboard-settings-transfers =
    <b>💸 Настройка переводов</b>

    <blockquote>
    • Статус: { $enabled ->
        [1] ✅ Включено
        *[0] 🔴 Выключено
    }
    • Тип комиссии: { $commission_type_display }
    • Комиссия: { $commission_display }
    • Минимальная сумма: { $min_amount } ₽
    • Максимальная сумма: { $max_amount } ₽
    </blockquote>


msg-dashboard-settings-transfers-commission-type =
    <b>💰 Выбор типа комиссии</b>

    <blockquote>
    • <b>Процентная</b> - комиссия взимается в процентах от суммы перевода
    • <b>Фиксированная</b> - комиссия взимается в фиксированной сумме независимо от суммы перевода
    </blockquote>

    Выберите тип комиссии:

msg-dashboard-settings-transfers-commission-value =
    <b>💵 Значение комиссии</b>

    <blockquote>
    • Тип комиссии: { $commission_type_display }
    • Текущая комиссия: { $db_commission_display }
    • Изменить на: { $selected_display }
    </blockquote>

    Выберите цену или введите свою:

msg-commission-manual-input =
    <b>✏️ Ручной ввод</b>

    <blockquote>
    Введите стоимость комиссии:
    </blockquote>

msg-dashboard-settings-transfers-min-amount =
    <b>📉 Минимальная сумма перевода</b>

    <blockquote>
    • Текущая минимальная сумма: { $db_min_current_display }
    • Изменить на: { $min_selected_display }
    </blockquote>

    Выберите сумму или введите свою:

msg-min-amount-manual-input =
    <b>✏️ Ручной ввод</b>

    <blockquote>
    Введите минимальную сумму перевода (в рублях):
    </blockquote>

msg-dashboard-settings-transfers-max-amount =
    <b>📈 Максимальная сумма перевода</b>

    <blockquote>
    • Текущая максимальная сумма: { $db_max_current_display }
    • Изменить на: { $max_selected_display }
    </blockquote>

    Выберите сумму или введите свою:

msg-max-amount-manual-input =
    <b>✏️ Ручной ввод</b>

    <blockquote>
    Введите максимальную сумму перевода (в рублях):
    </blockquote>

# Balance Settings
msg-dashboard-settings-balance =
    <b>💰 Настройка баланса</b>

    <blockquote>
    { lbl-status } { $enabled ->
        [1] { lbl-enabled }
        *[0] { lbl-disabled }
    }
    { lbl-min-topup-amount } { $balance_min_amount }
    { lbl-max-topup-amount } { $balance_max_amount }
    </blockquote>

    { hdr-balance-mode }
    <blockquote>
    { lbl-balance-mode-combined }
    { lbl-balance-mode-separate }
    </blockquote>

msg-dashboard-settings-balance-min-amount =
    <b>📉 Минимальная сумма пополнения баланса</b>

    <blockquote>
    • Текущая минимальная сумма: { $balance_min_current_display }
    • Изменить на: { $balance_min_selected_display }
    </blockquote>

    Выберите сумму:

msg-dashboard-settings-balance-max-amount =
    <b>📈 Максимальная сумма пополнения баланса</b>

    <blockquote>
    • Текущая максимальная сумма: { $balance_max_current_display }
    • Изменить на: { $balance_max_selected_display }
    </blockquote>

    Выберите сумму:

# Extra Devices Settings
msg-dashboard-extra-devices-settings =
    <b>📱 Настройка доп. устройств</b>

    <blockquote>
    • Статус: { $enabled ->
        [1] ✅ Включено
        *[0] 🔴 Выключено
    }
    • Тип оплаты: { $payment_type_display }
    • Стоимость устройства: { $extra_devices_price } ₽
    • Минимальное количество дней: { $min_days } { $min_days ->
        [1] день
        [2] дня
        [3] дня
        [4] дня
        *[other] дней
    }
    </blockquote>


msg-dashboard-extra-devices-price =
    <b>💵 Стоимость доп. устройства</b>

    <blockquote>
    • Текущая цена: { $current_price } ₽
    • Изменить на: { $selected_price } ₽
    </blockquote>

    Выберите цену или введите свою:

msg-dashboard-extra-devices-price-manual =
    <b>✏️ Ручной ввод цены</b>

    <blockquote>
    Введите цену доп. устройства (в рублях):
    </blockquote>

msg-dashboard-extra-devices-min-days =
    <b>⏳ Минимальное количество дней</b>

    <blockquote>
    • Текущее: { $current_min_days } дней
    • Изменить на: { $selected_min_days } дней
    </blockquote>

    Минимальное количество дней до окончания подписки, при котором разрешена покупка дополнительного слота устройства.

msg-dashboard-extra-devices-min-days-manual =
    <b>⏳ Минимальное количество дней</b>

    Введите минимальное количество дней (от 1 до 365)

    Выберите количество дней:

# Global Discount Settings
msg-dashboard-settings-global-discount =
    <b>🏷️ Настройка глобальной скидки</b>

    <blockquote>
    • Статус: { $enabled ->
        [1] ✅ Включено
        *[0] 🔴 Выключено
    }
    • Тип скидки: { $discount_type_display }
    • Скидка: { $discount_display }
    • Режим: { $stack_mode_display }
    • Влияние: { $apply_to_display }
    </blockquote>

msg-global-discount-apply-to =
    <b>📌 На что влияет скидка</b>

    <blockquote>
    Операции на которые влияет глобальная скидка.
    </blockquote>

msg-global-discount-mode =
    <b>⚙️ Режим применения скидок</b>

    <blockquote>
    • <b>Максимальная</b> - использовать наибольшую из примененных скидок
    
    • <b>Сложенная</b> - складывать обе скидки
    </blockquote>

msg-dashboard-settings-global-discount-value =
    <b>💵 Значение скидки</b>

    <blockquote>
    • Тип скидки: { $discount_type_display }
    • Текущая скидка: { $db_discount_display }
    • Изменить на: { $selected_display }
    </blockquote>

    Выберите скидку или введите свою:

msg-global-discount-manual-input =
    <b>✏️ Ручной ввод</b>

    <blockquote>
    Введите значение скидки:
    </blockquote>

# Language Settings
msg-dashboard-settings-language =
    <b>🌐 Настройка языка</b>
    <blockquote>
    • Мультиязычность: { $enabled ->
        [1] 🟢 Включено
        *[0] 🔴 Отключено
    }
    • Текущий язык: { $current_locale }
    </blockquote>

    <i>ℹ️ Мультиязычность:</i>
    🟢 Включено - каждый пользователь видит бота на своём языке
    🔴 Выключено - все пользователи видят выбранный язык

msg-main-menu =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }{ frg-subscription-status-full }

msg-menu-connect =
    <b>📝 Инструкция:</b>
    <blockquote>
    • Скачайте и установите приложение.
    • Нажмите 🔗Подключиться.
    • В приложении нажмите Включить.
    </blockquote>

msg-menu-devices =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { $has_subscription ->
        [0] <blockquote>
    • У вас нет оформленной подписки.
    </blockquote>
        *[other] { frg-subscription }
    }

    📱 <b>Управление устройствами:</b>

msg-add-device =
    <b>➕ Добавить устройство</b>

msg-add-device-select-count =
    { $has_discount ->
    [1] ℹ️<i>Стоимость каждого доп.устройства: { $device_price }₽/мес  <s>{ $device_price_original }₽</s>/мес.</i>
    *[0] ℹ️<i>Стоимость каждого доп.устройства: { $device_price }₽/мес.</i>
    }

    📱 <b>Выберите количество устройств:</b>

msg-add-device-full =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    { $has_discount ->
    [1] ℹ️<i>Стоимость каждого доп.устройства: { $device_price }₽/мес  <s>{ $device_price_original }₽</s>/мес.</i>
    *[0] ℹ️<i>Стоимость каждого доп.устройства: { $device_price }₽/мес.</i>
    }

    📱 <b>Выберите количество устройств:</b>

msg-add-device-duration =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    📱 <b>Покупка:</b>
    <blockquote>
    • <b>Доп. устройства:</b> { $device_count }
    </blockquote>

    📅 <b>Выберите срок действия:</b>

msg-add-device-payment =
    📱 <b>Покупка:</b>
    <blockquote>
    • <b>Доп. устройства:</b> { $device_count }
    </blockquote>

    💳 <b>Выберите способ оплаты:</b>

msg-add-device-payment-full =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    📱 <b>Покупка:</b>
    <blockquote>
    • <b>Доп. устройства:</b> { $device_count }
    </blockquote>

    💳 <b>Выберите способ оплаты:</b>

msg-add-device-confirm-full =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    📱 <b>Покупка:</b>
    <blockquote>
    • <b>Доп. устройства:</b> { $device_count }
    </blockquote>

    📋 <b>Итого:</b>
    <blockquote>
    💳 <b>Способ оплаты:</b> { gateway-type }
    { $is_balance_payment ->
    [1]
    📊 <b>Текущий баланс:</b> { $balance }
    📊 <b>Баланс после:</b> { $new_balance }
    *[0]
    { $has_discount ->
    [1]
    💰 <b>Сумма к оплате:</b> <s>{ $original_price }</s> { $total_price }
    *[0]
    💰 <b>Сумма к оплате:</b> { $total_price }
    }
    }
    </blockquote>

    💳 <b>Подтверждение покупки:</b>

msg-add-device-success-full =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    ℹ️ <i>К вашей подписке добавлено { $device_count } { $device_count_word }.</i>

    ✅ <b>Оплата прошла успешно!</b>

msg-extra-devices-list =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    📱 <b>Дополнительные устройства</b>
    { $purchases_empty ->
        [true] <i>У вас нет активных дополнительных устройств.</i>
        *[false] <blockquote>
    💰 <b>Ежемесячная стоимость:</b> { $total_monthly_cost }
    📱 <b>Всего доп. устройств:</b> { $total_extra_devices }
    <i>Устройства активны до конца месяца подписки.</i>
    </blockquote>
    
    <i>Нажмите ❌ чтобы отменить подписку на устройство.</i>
    }

msg-extra-device-manage =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    📱 <b>Управление дополнительными устройствами</b>
    
    <blockquote>
    • <b>Количество устройств:</b> { $purchase_device_count }
    • <b>Стоимость/мес:</b> { $purchase_price } ₽
    • <b>Истекает:</b> { $purchase_expires_at }
    • <b>Автопродление:</b> { $purchase_auto_renew ->
        [1] ✅ Включено
        *[0] ❌ Отключено
    }
    </blockquote>
    
    { $purchase_auto_renew ->
        [1] <i>При отключении автопродления, устройства будут удалены по истечению срока.</i>
        *[0] <i>Автопродление отключено. Устройства будут удалены через { $purchase_days_remaining } дн.</i>
    }

msg-add-device-confirm-details =
    📱 <b>Покупка:</b>
    <blockquote>
    • <b>Доп. устройства:</b> { $device_count }
    </blockquote>

    📋 <b>Итого:</b>
    <blockquote>
    • <b>Способ оплаты:</b> { $selected_method }
    • <b>Текущий баланс:</b> { $balance }
    • <b>Баланс после:</b> { $new_balance }
    </blockquote>

    💳<b>Подтверждение покупки:</b>

msg-balance-menu =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription-status-full }

    <b>💰 Управление балансом:</b>

msg-balance-select-gateway =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription-conditional }

    <b>💰 Выбор способа оплаты:</b>

msg-balance-select-amount =
    <b>💰 Пополнение баланса</b>

    Способ оплаты: <b>{ $selected_gateway }</b>

    Выберите сумму пополнения:

msg-balance-enter-amount =
    <b>💰 Пополнение баланса</b>

    Способ оплаты: <b>{ $selected_gateway }</b>

    Введите сумму пополнения (от { $min_amount } до { $max_amount } { $currency }):

msg-balance-confirm =
    <b>💰 Подтверждение пополнения</b>

    Способ оплаты: <b>{ $selected_gateway }</b>
    Сумма: <b>{ $topup_amount } { $currency }</b>

    Нажмите кнопку ниже для оплаты.

msg-balance-success =
    <b>✅ Баланс успешно пополнен!</b>
    
    <blockquote>
    На ваш счёт зачислено <b>{ $amount }{ $currency }</b>
    </blockquote>

msg-balance-transfer =
    <b>💸 Перевод баланса</b>

    { hdr-user-profile }
    <blockquote>
    { lbl-your-balance } <b>{ $balance }</b>
    { lbl-commission } { $commission_display }
    </blockquote>

    { hdr-transfer }
    <blockquote>
    { lbl-recipient } { $recipient_display }
    { lbl-transfer-amount } <b>{ $amount_display } ₽</b>
    { lbl-commission } <b>{ $transfer_commission } ₽</b>
    </blockquote>

    { hdr-message }
    <blockquote>
    { $message_display }
    </blockquote>

    { msg-fill-data-and-send }

msg-balance-transfer-recipient =
    <b>💸 Получатель</b>

    <blockquote>
    Введите <b>Telegram ID</b> получателя:
    </blockquote>

msg-balance-transfer-recipient-history =
    <b>📜 История пользователей</b>

    Выберите получателя из списка пользователей, которым вы ранее отправляли переводы:

msg-balance-transfer-no-history = <i>У вас пока нет истории переводов.</i>

msg-balance-transfer-amount-value =
    <b>💸 Сумма перевода</b>

    <blockquote>
    • Текущая сумма: { $current_display }
    • Изменить на: { $selected_display }
    </blockquote>

    Выберите сумму или введите свою:

msg-balance-transfer-amount-manual =
    <b>✏️ Ручной ввод</b>

    <blockquote>
    Введите сумму перевода (от { $min_amount } до { $max_amount } ₽):
    </blockquote>

msg-balance-transfer-message =
    <b>💬 Сообщение</b>

    <blockquote>
    { $message_display }
    </blockquote>

    <i>Введите сообщение для перевода (макс. 200 символов):</i>

msg-balance-transfer-confirm =
    <b>💸 Подтверждение перевода</b>

    <blockquote>
    Получатель: <b>{ $recipient_name }</b> (<code>{ $recipient_id }</code>)
    Сумма перевода: <b>{ $amount } ₽</b>
    Комиссия: <b>{ $commission } ₽</b>
    Итого к списанию: <b>{ $total } ₽</b>
    </blockquote>

    ⚠️ <b>Внимание:</b> Операция необратима!

msg-balance-transfer-success =
    <b>✅ Перевод выполнен успешно!</b>

    <blockquote>
    Получатель: <b>{ $recipient_name }</b>
    Сумма: <b>{ $amount } ₽</b>
    Комиссия: <b>{ $commission } ₽</b>
    </blockquote>

msg-balance-transfer-error =
    <b>❌ Ошибка перевода</b>

    { $error }

msg-menu-invite =
    <b>👥 Пригласить друзей</b>

    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }{ frg-subscription-status-full }

    <b>🏆 Награда:</b>
    <blockquote>
    { $ref_reward_type ->
        [EXTRA_DAYS] • { $ref_reward_level_1_value } дн. за каждые 100 { $currency_symbol } пополнения приглашенным
        [MONEY] • { $ref_reward_level_1_value }% от суммы пополнения приглашенным
        *[OTHER] • { $ref_reward_level_1_value } { $currency_symbol }
    }{ $ref_max_level ->
        [2] {""}
    
    { $ref_reward_type ->
        [EXTRA_DAYS] • { $ref_reward_level_2_value } дн. за каждые 100 { $currency_symbol } пополнения приглашенным приглашенными
        [MONEY] • { $ref_reward_level_2_value }% от суммы пополнения приглашенным приглашенными
        *[OTHER] • { $ref_reward_level_2_value } { $currency_symbol }
    }
        *[1] {""}
    }
    </blockquote>

    <b>📊 Статистика:</b>
    <blockquote>
    👥 Всего приглашенных: { $referrals }
    💳 Платежей по вашей ссылке: { $payments }
    💳 Получено всего: { $total_bonus }{ $ref_reward_type ->
        [EXTRA_DAYS] { " " }дн.
        *[OTHER] {""}
    }
    </blockquote>

    <i>ℹ️ Награда начисляется при оплатах приведенных вами пользователей.</i>

msg-menu-invite-about =
    <b>🎁 Подробнее о вознаграждении</b>

    <b>✨ Как получить награду:</b>
    <blockquote>
    { $accrual_strategy ->
    [ON_FIRST_PAYMENT] Награда начисляется за первую покупку подписки приглашенным пользователем.
    [ON_EACH_PAYMENT] Награда начисляется за каждую покупку, или продление подписки приглашенным пользователем.
    *[OTHER] { $accrual_strategy }
    }
    </blockquote>

    <b>💎 Что вы получаете:</b>
    <blockquote>
    { $max_level -> 
    [1] За приглашенных друзей: { $reward_level_1 }
    *[MORE]
    { $identical_reward ->
    [0]
    1️⃣ За ваших друзей: { $reward_level_1 }
    2️⃣ За приглашенных вашими друзьями: { $reward_level_2 }
    *[1]
    За ваших друзей и приглашенных вашими друзьями: { $reward_level_1 }
    }
    }
    
    { $reward_strategy_type ->
    [AMOUNT] { $reward_type ->
        [MONEY] { space }
        [EXTRA_DAYS] <i>(Все дополнительные дни начисляются к вашей текущей подписке)</i>
        *[OTHER] { $reward_type }
    }
    [PERCENT] { $reward_type ->
        [MONEY] <i>(Процент от стоимости их приобретенной подписки)</i>
        [EXTRA_DAYS] <i>(Процент доп. дней от их приобретенной подписки)</i>
        *[OTHER] { $reward_type }
    }
    *[OTHER] { $reward_strategy_type }
    }
    </blockquote>

msg-invite-reward = { $value }{ $reward_strategy_type ->
    [AMOUNT] { $reward_type ->
        [MONEY] { space }₽
        [EXTRA_DAYS] { space }доп. { $value -> 
            [one] день
            [few] дня
            *[more] дней
            }
        *[OTHER] { $reward_type }
    }
    [PERCENT] % { $reward_type ->
        [MONEY] 
        [EXTRA_DAYS] доп. дней
        *[OTHER] { $reward_type }
    }
    *[OTHER] { $reward_strategy_type }
    }

msg-menu-invite-edit-code =
    ✏️ <b>Смена реферального кода</b>

    • Ваш текущий код: <code>{ $referral_code }</code>

    <i>Введите новый реферальный код.</i>
    { $ref_code_error ->
        [invalid]

    ⚠️ <b>Недопустимые символы.</b>
    Разрешены: A–Z, a–z, 0–9, _ - (длина 3–32)
        [taken]

    ⚠️ Этот код уже занят. Выберите другой.
        *[other] {""}
    }

# Dashboard
msg-dashboard-main =
    <b>🛠 Панель управления v{ $bot_version }</b> { $update_available ->
        [1] — 🔔 Доступно обновление: <b>{ $new_version }</b>
        *[0] {""}
    }
msg-bot-management =
    <b>🤖 Управление ботом</b>
msg-mirror-bots =
    <b>🤖 Дополнительные боты</b>

    <blockquote>Здесь вы можете добавить дополнительных ботов-зеркал. Нажмите на бота, чтобы назначить его <b>основным</b> - тогда пригласительные ссылки будут вести именно на него.</blockquote>
msg-mirror-bot-add-token =
    <b>➕ Добавление нового бота</b>

    Отправьте API-токен нового бота, полученный от @BotFather.
msg-dashboard-user-management =
    <b>👥 Управление пользователями</b>
msg-dashboard-features =
    <b>⚙️ Функционал</b>

    <blockquote>
    Здесь вы можете включить или выключить различные функции бота.
    </blockquote>

msg-dashboard-extra-devices =
    <b>📱 Дополнительные устройства</b>

    <b>Статус:</b> { $enabled ->
        [1] ✅ Включено
        *[0] ⬜ Выключено
    }
    <b>Стоимость:</b> { $price } ₽/мес за устройство

    <blockquote>
    Позволяет пользователям добавлять дополнительные устройства к подписке за отдельную плату.
    </blockquote>

msg-dashboard-extra-devices-price =
    <b>💰 Изменение стоимости доп. устройств</b>

    <b>Текущая стоимость:</b> { $current_price } ₽

    Выберите стоимость или введите вручную:

msg-dashboard-extra-devices-price-manual =
    <b>💰 Ручной ввод стоимости</b>

    Введите новую стоимость в рублях (целое число от 0 до 100000):

msg-dashboard-extra-devices-settings =
    <b>📱 Настройка доп. устройств</b>

    <b>Текущая стоимость:</b> { $price } ₽ за устройство
    <b>Тип оплаты:</b> { $is_one_time ->
    [1] Единоразово
    *[0] Ежемесячно
    }

    <blockquote>
    <b>Единоразово</b> - пользователь оплачивает устройства один раз, они сохраняются до удаления.
    
    <b>Ежемесячно</b> - стоимость устройств добавляется при каждом продлении подписки.
    </blockquote>

msg-users-main = <b>👥 Пользователи</b>
msg-broadcast-main = <b>📢 Рассылка</b>
msg-statistics-main = { $statistics }
    
msg-statistics-users =
    <b>👥 Статистика по пользователям</b>

    <blockquote>
    • <b>Всего</b>: { $total_users }
    • <b>Новые за день</b>: { $new_users_daily }
    • <b>Новые за неделю</b>: { $new_users_weekly }
    • <b>Новые за месяц</b>: { $new_users_monthly }

    • <b>С подпиской</b>: { $users_with_subscription }
    • <b>Без подписки</b>: { $users_without_subscription }
    • <b>С пробным периодом</b>: { $users_with_trial }

    • <b>Заблокированные</b>: { $blocked_users }
    • <b>Заблокировали бота</b>: { $bot_blocked_users }

    • <b>Конверсия пользователей → покупка</b>: { $user_conversion }%
    • <b>Конверсия пробников → подписка</b>: { $trial_conversion }%
    </blockquote>

msg-statistics-transactions =
    <b>🧾 Статистика по транзакциям</b>

    <blockquote>
    • <b>Всего транзакций</b>: { $total_transactions }
    • <b>Завершенных транзакций</b>: { $completed_transactions }
    • <b>Бесплатных транзакций</b>: { $free_transactions }
    { $popular_gateway ->
    [0] { empty }
    *[HAS] • <b>Популярная платежная система</b>: { $popular_gateway }
    }
    </blockquote>

    <b>💰 Реальные деньги:</b>
    
    { $payment_gateways }

    <b>🎁 Бонусы пользователей:</b>
    
    { $bonus_gateways }

msg-statistics-subscriptions =
    <b>💳 Статистика по подпискам</b>

    <blockquote>
    • <b>Активные</b>: { $total_active_subscriptions }
    • <b>Истекшие</b>: { $total_expire_subscriptions }
    • <b>Пробные</b>: { $active_trial_subscriptions }
    • <b>Истекающие (7 дней)</b>: { $expiring_subscriptions }
    </blockquote>

    <blockquote>
    • <b>С безлимитом</b>: { $total_unlimited }
    • <b>С лимитом трафика</b>: { $total_traffic }
    • <b>С лимитом устройств</b>: { $total_devices }
    </blockquote>

msg-statistics-plans = 
    <b>📦 Статистика по планам</b>

    { $plans }

msg-statistics-promocodes =
    <b>🎁 Статистика по промокодам</b>

    <blockquote>
    • <b>Общее кол-во активаций</b>: { $total_promo_activations }
    • <b>Самый популярный промокод</b>: { $most_popular_promo ->
    [0] { unknown }
    *[HAS] { $most_popular_promo }
    }
    • <b>Выдано дней</b>: { $total_promo_days }
    • <b>Выдано трафика</b>: { $total_promo_days }
    • <b>Выдано подписок</b>: { $total_promo_subscriptions }
    • <b>Выдано личных скидок</b>: { $total_promo_personal_discounts }
    • <b>Выдано одноразовых скидок</b>: { $total_promo_purchase_discounts }
    </blockquote>

msg-statistics-referrals =
    <b>👪 Статистика по реферальной системе</b>
    
    <blockquote>
    • <b></b>:
    </blockquote>

msg-statistics-transactions-gateway =
    <b>{ gateway-type }:</b>
    <blockquote>
    • <b>Общий доход</b>: { $total_income }{ $currency }
    • <b>Доход за день</b>: { $daily_income }{ $currency }
    • <b>Доход за неделю</b>: { $weekly_income }{ $currency }
    • <b>Доход за месяц</b>: { $monthly_income }{ $currency }
    • <b>Средний чек</b>: { $average_check }{ $currency }
    • <b>Сумма скидок</b>: { $total_discounts }{ $currency }
    </blockquote>

msg-statistics-plan =
    <b>{ $plan_name }:</b> { $popular -> 
    [0] { space }
    *[HAS] (⭐)
    }
    <blockquote>
    • <b>Всего подписок</b>: { $total_subscriptions }
    • <b>Активных подписок</b>: { $active_subscriptions }
    • <b>Популярная длительность</b>: { $popular_duration }

    • <b>Общий доход</b>: 
    { $all_income }
    </blockquote>

msg-statistics-plan-income = { $income }{ $currency }
    


# Access
msg-access-main =
    <b>🔓 Режим доступа</b>
    
    <blockquote>
    • <b>Режим</b>: { access-mode }
    • <b>Покупки</b>: { $purchases_allowed ->
    [0] запрещены
    *[1] разрешены
    }.
    • <b>Регистрация</b>: { $registration_allowed ->
    [0] запрещена
    *[1] разрешена
    }.
    </blockquote>

msg-access-conditions =
    <b>⚙️ Условия доступа</b>

msg-access-rules =
    <b>✳️ Изменить ссылку на правила</b>

    Введите ссылку (в формате https://telegram.org/tos).
    
    Это же значение используется в меню <b>Соглашение с пользователем</b>.

msg-access-channel =
    <b>❇️ Изменить ссылку на канал/группу</b>

    Если ваша группа не имеет @username, отправьте ID группы и ссылку-приглашение отдельными сообщениями.
    
    Если у вас публичный канал/группа, введите только @username.


# Broadcast
msg-broadcast-list = <b>📄 Список рассылок</b>
msg-broadcast-plan-select = <b>📦 Выберите план для рассылки</b>
msg-broadcast-send = <b>📢 Отправить рассылку ({ audience-type })</b>

    { $audience_count } { $audience_count ->
    [one] пользователю
    [few] пользователям
    *[more] пользователей
    } будет отправлена рассылка

msg-broadcast-content =
    <b>✉️ Содержимое рассылки</b>

    <b>Текущее содержимое:</b>

    { $has_content ->
        [1] <blockquote>{ $current_content }</blockquote>
        *[other] <blockquote>• Не заполнено</blockquote>
    }

    <i>Отправьте любое сообщение: текст, изображение или все вместе (поддерживается HTML).</i>

msg-broadcast-buttons = <b>✳️ Кнопки рассылки</b>

msg-broadcast-view =
    <b>📢 Рассылка</b>

    <blockquote>
    • <b>ID</b>: <code>{ $broadcast_id }</code>
    • <b>Статус</b>: { broadcast-status }
    • <b>Аудитория</b>: { audience-type }
    • <b>Создано</b>: { $created_at }
    </blockquote>

    <blockquote>
    • <b>Всего сообщений</b>: { $total_count }
    • <b>Успешных</b>: { $success_count }
    • <b>Неудачных</b>: { $failed_count }
    </blockquote>


# Users
msg-users-recent-registered = <b>🆕 Последние зарегистрированные</b>
msg-users-recent-activity = <b>📝 Последние взаимодействующие</b>
msg-users-all = <b>👥 Все пользователи</b>
msg-user-transactions = <b>🧾 Транзакции пользователя</b>
msg-user-devices = <b>📱 Устройства пользователя ({ $current_count } / { $max_count })</b>
msg-user-give-access = <b>🔑 Предоставить доступ к плану</b>

msg-users-search =
    <b>🔍 Поиск пользователя</b>

    Введите ID пользователя, часть имени или перешлите любое его сообщение.

msg-users-search-results =
    <b>🔍 Поиск пользователя</b>

    Найдено <b>{ $count }</b> { $count ->
    [one] пользователь
    [few] пользователя
    *[more] пользователей
    }, { $count ->
    [one] соответствующий
    *[more] соответствующих
    } запросу

msg-user-main = 
    <b>📝 Информация о пользователе</b>

    { hdr-user-profile }
    { frg-user-details }

    <b>💸 Скидка:</b>
    <blockquote>
    • <b>Персональная</b>: { $personal_discount }%
    • <b>На следующую покупку</b>: { $purchase_discount }%
    </blockquote>
    
    { hdr-subscription }
    { frg-subscription-status-short }

msg-user-referrals = 
    <b>👥 Рефералы пользователя</b>

    <b>Количество рефералов:</b> { $referral_count }
    <b>Общая сумма бонусов:</b> { $total_bonus } ₽

msg-user-referrals-list =
    <b>📋 Список рефералов</b>

msg-user-referral-bind = 
    <b>🔗 Привязать реферала</b>

    Введите Telegram ID или @username пользователя, которого хотите привязать как реферала.

msg-user-delete-confirm =
    <b>❌ Удаление пользователя</b>

    <i>Вы уверены? Это действие нельзя отменить.</i>

msg-user-sync = 
    <b>🌀 Синхронизировать пользователя</b>

    <b>🛍 Телеграм:</b>
    <blockquote>
    { $has_bot_subscription -> 
    [0] Данные отсутствуют
    *[HAS]{ $bot_subscription }
    }
    </blockquote>

    <b>🌊 Панель:</b> { $remna_version }
    <blockquote>
    { $has_remna_subscription -> 
    [0] Данные отсутствуют
    *[HAS] { $remna_subscription }
    }
    </blockquote>

    Выберите актуальные данные для синхронизации.

msg-user-sync-version = { $version ->
    [NEWER] (новее)
    [OLDER] (старее)
    *[UNKNOWN] { empty }
    }

msg-user-sync-subscription =
    • <b>ID</b>: <code>{ $id }</code>
    • Статус: { $status -> 
    [ACTIVE] Активна
    [DISABLED] Отключена
    [LIMITED] Исчерпан трафик
    [EXPIRED] Истекла
    [DELETED] Удалена
    *[OTHER] { $status }
    }
    • Ссылка: <a href="{ $url }">*********</a>

    • Лимит трафика: { $traffic_limit }
    • Лимит устройств: { $device_limit }
    • Осталось: { $expire_time }

    • Внутренние сквады: { $internal_squads ->
    [0] { unknown }
    *[HAS] { $internal_squads }
    }
    • Внешний сквад: { $external_squad ->
    [0] { unknown }
    *[HAS] { $external_squad }
    }
    • Сброс трафика: { $traffic_limit_strategy -> 
    [NO_RESET] При оплате
    [DAY] Каждый день
    [WEEK] Каждую неделю
    [MONTH] Каждый месяц
    *[OTHER] { $traffic_limit_strategy }
    }
    • Тег: { $tag -> 
    [0] { unknown }
    *[HAS] { $tag }
    }

msg-user-sync-waiting =
    <b>🌀 Синхронизация пользователя</b>

    Пожалуйста, подождите... Идет процесс синхронизации данных пользователя. Вы автоматически вернетесь к редактору пользователя по завершении.

msg-user-give-subscription =
    <b>🎁 Выдать подписку</b>

    Выберите план, который хотите выдать пользователю.

msg-user-give-subscription-duration =
    <b>⏳ Выберите длительность</b>

    Выберите длительность выдаваемой подписки.

msg-user-discount =
    <b>💸 Изменить персональную скидку</b>

    Выберите по кнопке или введите свой вариант.

msg-user-balance-menu =
    <b>💰 Баланс пользователя</b>

    <b>Основной баланс:</b> { $current_balance } ₽
    <b>Реферальный баланс:</b> { $referral_balance } ₽

    Выберите тип баланса для редактирования:

msg-user-finance-menu-full =
    <b>💰 Управление финансами</b>

    { $is_balance_enabled ->
        [1] <b>Основной баланс:</b> { $current_balance } ₽
        *[0] {""}
    }
    { $is_referral_enable ->
        [1] <b>Бонусный баланс:</b> { $referral_balance } ₽
        *[0] {""}
    }
    <b>Постоянная скидка:</b> { $discount_value }%

    Выберите пункт для редактирования:

msg-user-finance-menu-short =
    <b>💰 Управление финансами</b>

    <b>Постоянная скидка:</b> { $discount_value }%

    Выберите пункт для редактирования:

msg-user-main-balance =
    <b>💰 Основной баланс</b>

    <b>Текущий баланс: { $current_balance } ₽</b>

    Выберите по кнопке или введите свой вариант, чтобы добавить или отнять.

msg-user-referral-balance =
    <b>🎁 Реферальный баланс</b>

    <b>Текущий баланс: { $current_referral_balance } ₽</b>

    Выберите по кнопке или введите свой вариант, чтобы добавить.

msg-user-points =
    <b>� Изменить баланс</b>

    <b>Текущий баланс: { $current_balance } ₽</b>

    Выберите по кнопке или введите свой вариант, чтобы добавить или отнять.

msg-user-subscription-traffic-limit =
    <b>🌐 Изменить лимит трафика</b>

    Выберите по кнопке или введите свой вариант (в ГБ), чтобы изменить лимит трафика.

msg-user-subscription-device-limit =
    <b>📱 Бонусные устройства</b>

    • Выберите количество бонусных устройств для пользователя, или введите количество от 0 до 100

msg-user-subscription-expire-time =
    <b>⏳ Изменить срок действия</b>

    <b>Закончится через: { $expire_time }</b>

    Выберите по кнопке или введите свой вариант (в днях), чтобы добавить или отнять.

msg-user-subscription-squads =
    <b>🔗 Сквады</b>

    • Внутренний сквад: { $internal_squads ->
    [0] не выбран
    *[HAS] { $internal_squads }
    }
    • Внешний сквад: { $external_squad ->
    [0] не выбран
    *[HAS] { $external_squad }
    }

    ✏️ Выберите сквады:

msg-user-subscription-internal-squads =
    <b>⏺️ Изменить список внутренних сквадов</b>

    Выберите, какие внутренние группы будут присвоены этому пользователю.

msg-user-subscription-external-squads =
    <b>⏹️ Изменить внешний сквад</b>

    Выберите, какая внешняя группа будет присвоена этому пользователю.

msg-user-subscription-empty =
    <b>💳 Информация о подписке</b>

    У данного пользователя нет активной подписки.

msg-user-subscription-info =
    <b>💳 Информация о текущей подписке</b>
    
    { hdr-subscription }
    { frg-subscription-details }

    <blockquote>
    • <b>Сквады</b>: { $squads -> 
    [0] { unknown }
    *[HAS] { $squads }
    }
    • <b>Первое подключение</b>: { $first_connected_at -> 
    [0] { unknown }
    *[HAS] { $first_connected_at }
    }
    • <b>Последнее подключение</b>: { $last_connected_at ->
    [0] { unknown }
    *[HAS] { $last_connected_at } ({ $node_name })
    } 
    </blockquote>

    { hdr-plan }
    { frg-plan-snapshot }

msg-user-transaction-info =
    <b>🧾 Информация о транзакции</b>

    { hdr-payment }
    <blockquote>
    • <b>ID</b>: <code>{ $payment_id }</code>
    • <b>Тип</b>: { purchase-type }
    • <b>Статус</b>: { transaction-status }
    • <b>Способ оплаты</b>: { gateway-type }
    • <b>Сумма</b>: { frg-payment-amount }
    • <b>Создано</b>: { $created_at }
    </blockquote>

    { $is_test -> 
    [1] ⚠️ Тестовая транзакция
    *[0]
    { hdr-plan }
    { frg-plan-snapshot }
    }
    
msg-user-role = 
    <b>👮‍♂️ Изменить роль</b>
    
    Выберите новую роль для пользователя.

msg-users-blacklist =
    <b>🚫 Черный список</b>

    Заблокировано: <b>{ $count_blocked }</b> / <b>{ $count_users }</b> ({ $percent }%).

msg-user-message =
    <b>📩 Отправить сообщение пользователю</b>

    Отправьте любое сообщение: текст, изображение или все вместе (поддерживается HTML).
    

# Панель
msg-remnawave-main =
    <b>🌊 Панель</b>
    
    <b>🖥️ Система:</b>
    <blockquote>
    • <b>ЦПУ</b>: { $cpu_cores } { $cpu_cores ->
    [one] ядро
    [few] ядра
    *[more] ядер
    } { $cpu_threads } { $cpu_threads ->
    [one] поток
    [few] потока
    *[more] потоков
    }
    • <b>ОЗУ</b>: { $ram_used } / { $ram_total } ({ $ram_used_percent }%)
    • <b>Аптайм</b>: { $uptime }
    </blockquote>

msg-remnawave-users =
    <b>👥 Пользователи</b>

    <b>📊 Статистика:</b>
    <blockquote>
    • <b>Всего</b>: { $users_total }
    • <b>Активные</b>: { $users_active }
    • <b>Отключенные</b>: { $users_disabled }
    • <b>Ограниченные</b>: { $users_limited }
    • <b>Истекшие</b>: { $users_expired }
    </blockquote>

    <b>🟢 Онлайн:</b>
    <blockquote>
    • <b>За день</b>: { $online_last_day }
    • <b>За неделю</b>: { $online_last_week }
    • <b>Никогда не заходили</b>: { $online_never }
    • <b>Сейчас онлайн</b>: { $online_now }
    </blockquote>

msg-remnawave-host-details =
    <b>{ $remark } ({ $status ->
    [ON] включен
    *[OFF] выключен
    }):</b>
    <blockquote>
    • <b>Адрес</b>: <code>{ $address }:{ $port }</code>
    { $inbound_uuid ->
    [0] { empty }
    *[HAS] • <b>Инбаунд</b>: <code>{ $inbound_uuid }</code>
    }
    </blockquote>

msg-remnawave-node-details =
    <b>{ $country } { $name } ({ $status ->
    [ON] подключено
    *[OFF] отключено
    }):</b>
    <blockquote>
    • <b>Адрес</b>: <code>{ $address }{ $port -> 
    [0] { empty }
    *[HAS]:{ $port }
    }</code>
    • <b>Аптайм (xray)</b>: { $xray_uptime }
    • <b>Пользователей онлайн</b>: { $users_online }
    • <b>Трафик</b>: { $traffic_used } / { $traffic_limit }
    </blockquote>

msg-remnawave-inbound-details =
    <b>🔗 { $tag }</b>
    <blockquote>
    • <b>ID</b>: <code>{ $inbound_id }</code>
    • <b>Протокол</b>: { $type } ({ $network })
    { $port ->
    [0] { empty }
    *[HAS] • <b>Порт</b>: { $port }
    }
    { $security ->
    [0] { empty }
    *[HAS] • <b>Безопасность</b>: { $security } 
    }
    </blockquote>

msg-remnawave-hosts =
    <b>🌐 Хосты</b>
    
    { $host }

msg-remnawave-nodes = 
    <b>🖥️ Ноды</b>

    { $node }

msg-remnawave-inbounds =
    <b>🔌 Инбаунды</b>

    { $inbound }


# Телеграм
msg-remnashop-main = <b>🛍 Телеграм</b>
msg-admins-main = <b>👮‍♂️ Администраторы</b>


# Gateways
msg-gateways-main = <b>🌐 Платежные системы</b>
msg-gateways-settings = <b>🌐 Конфигурация { gateway-type }</b>
msg-gateways-settings-detail =
    <b>⚙️ Настрока системы: { gateway-type }</b>

    { $settings_display }

    Выберите что изменить:
msg-gateways-default-currency = <b>💸 Валюта по умолчанию</b>
msg-gateways-placement = <b>🔢 Изменить позиционирование</b>

msg-gateways-field =
    <b>🌐 Конфигурация { gateway-type }</b>

    Введите новое значение для { $field }.


# Referral
msg-referral-main =
    <b>👥 Реферальная система</b>

    <blockquote>
    • <b>Статус</b>: { $is_enable -> 
        [1] 🟢 Включено
        *[0] 🔴 Выключено
        }
    • <b>Тип награды</b>: { reward-type }
    • <b>Количество уровней</b>: { $level_text }
    • <b>Условие начисления</b>: { accrual-strategy }
    • <b>Форма начисления</b>: { reward-strategy }
    • <b>Награда</b>: { $reward_display }
    </blockquote>

    🔽 Выберите пункт для изменения.

msg-referral-level =
    <b>🔢 Изменить уровень</b>

    Выберите количество уровней реферальной системы.

msg-referral-reward-type =
    <b>🎀 Изменить тип награды</b>

    Выберите тип награды за приглашенных пользователей.
    
msg-referral-accrual-strategy =
    <b>📍 Изменить условие начисления</b>

    Выберите, при каком условии будет начисляться награда.


msg-referral-reward-strategy =
    <b>⚖️ Изменить форму начисления</b>

    Выберите способ расчета награды.
    
    <i>При выборе типа "Дни": начисляется N дней за каждые 100 рублей пополнения/покупки.</i>


msg-referral-reward-level = { $level } уровень: { $value }{ $reward_strategy_type ->
    [AMOUNT] { $reward_type ->
        [POINTS] { space }{ $value -> 
            [one] балл
            [few] балла
            *[more] баллов
            }
        [EXTRA_DAYS] { space }доп. { $value -> 
            [one] день
            [few] дня
            *[more] дней
            }
        [MONEY] ₽
        *[OTHER] { $reward_type }
    }
    [PERCENT] % { $reward_type ->
        [POINTS] баллов
        [EXTRA_DAYS] доп. дней
        [MONEY] от суммы платежа
        *[OTHER] { $reward_type }
    }
    *[OTHER] { $reward_strategy_type }
    }
    
msg-referral-reward =
    <b>🎁 Изменить награду</b>

    <blockquote>
    { $reward }
    </blockquote>

    { $reward_type ->
        [EXTRA_DAYS] Выберите количество дней за каждые 100₽ пополнения/покупки, или введите значение вручную.
        *[OTHER] Выберите размер награды или введите значение вручную.
    }

msg-referral-reward-manual =
    <b>✏️ Ручной ввод награды</b>

msg-referral-invite-message =
    <b>✉️ Настройка сообщения приглашения</b>

    🔽 Выберите действие:

msg-referral-invite-edit =
    <b>✉️ Настройка сообщения приглашения</b>

    ℹ️ Доступные переменные:
    <blockquote>
    • <code>{"{url}"}</code> - реферальная ссылка
    • <code>{"{space}"}</code> - пустая строка в начале (не видна в превью)
    </blockquote>

    <i>✏️ Введите ваше приглашение:</i>

msg-referral-invite-preview =

    { $preview_message }

# Plans
msg-plans-main = <b>📦 Планы</b>

msg-plan-configurator =
    <b>📦 Конфигуратор плана</b>

    <blockquote>
    • <b>Название</b>: { $name }
    • <b>Тег</b>: { $tag }
    • <b>Внутренний сквад</b>: { $internal_squads }
    • <b>Внешний сквад</b>: { $external_squad }
    • <b>Доступ</b>: { availability-type }
    </blockquote>
    
    <blockquote>
    • <b>Тип</b>: { plan-type }
    • <b>Лимит трафика</b>: { $is_unlimited_traffic ->
        [1] { unlimited }
        *[0] { $traffic_limit }
    }
    • <b>Лимит устройств</b>: { $is_unlimited_devices ->
        [1] { unlimited }
        *[0] { $device_limit }
    }
    </blockquote>
    
    <blockquote>
    • <b>Статус</b>: { $is_active ->
        [1] 🟢 Включен
        *[0] 🔴 Выключен
    }
    </blockquote>

    Выберите пункт для изменения.

msg-plan-name =
    <b>🏷️ Изменить название</b>

    { $name ->
    [0] { space }
    *[HAS]
    <blockquote>
    { $name }
    </blockquote>
    }

    Введите новое название плана.

msg-plan-description =
    <b>💬 Изменить описание</b>

    <blockquote>
    Описание: { $description }
    </blockquote>

    Введите новое описание плана.

msg-plan-tag =
    <b>📌 Изменить тег</b>

    <blockquote>
    Тег: { $tag }
    </blockquote>

    <i>ℹ️ Используйте латинские заглавные буквы, цифры и символ подчеркивания.</i>

    ✏️ Введите тег для плана:

msg-plan-type =
    <b>🔖 Изменить тип</b>

    Выберите новый тип плана.

msg-plan-availability =
    <b>✴️ Изменить доступность</b>

    Выберите доступность плана.

msg-plan-traffic =
    <b>🌐 Изменить лимит и стратегию сброса трафика</b>

    Введите новый лимит трафика плана (в ГБ) и выберите стратегию его сброса.

msg-plan-devices =
    <b>📱 Изменить лимит устройств</b>

    Введите новый лимит устройств плана.

msg-plan-durations =
    <b>⏳ Длительности плана</b>

    Выберите длительность для изменения цены.

msg-plan-duration =
    <b>⏳ Добавить длительность плана</b>

    Введите новую длительность (в днях).

msg-plan-prices =
    <b>💰 Изменить цену тарифа на ({ $value ->
            [-1] { unlimited }
            *[other] { unit-day }
        })</b>

    Укажите цену в рублях.
    Цены в других валютах будут рассчитаны автоматически по курсу.

msg-plan-price =
    <b>💰 Изменить цену для тарифа на ({ $value ->
            [-1] { unlimited }
            *[other] { unit-day }
        })</b>

    Введите новую цену в рублях (₽).

msg-plan-allowed-users = 
    <b>👥 Изменить список разрешенных пользователей</b>

    Введите ID пользователя для добавления в список.

msg-plan-squads =
    <b>🔗 Сквады</b>

    <blockquote>
    • <b>Внутренние</b>: { $internal_squads ->
    [0] { lbl-not-set }
    *[HAS] { $internal_squads }
    }
    • <b>Внешний</b>: { $external_squad ->
    [0] { lbl-not-set }
    *[HAS] { $external_squad }
    }
    </blockquote>

    ✏️ Выберите необходимые сквады:

msg-plan-internal-squads =
    <b>⏺️ Изменить список внутренних сквадов</b>

    Выберите, какие внутренние группы будут присвоены этому плану.

msg-plan-external-squads =
    <b>⏹️ Изменить внешний сквад</b>

    Выберите, какая внешняя группа будет присвоена этому плану.


# Notifications
msg-notifications-main = <b>🔔 Настройка уведомлений</b>
msg-notifications-user = <b>👥 Пользовательские уведомления</b>
msg-notifications-system = <b>⚙️ Системные уведомления</b>


# Subscription
msg-subscription-key-title = 
    🔑 <b>Ваш ключ подписки:</b>

msg-subscription-main =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription-conditional }

    { $trial_available ->
    [1]
    { $is_referral_trial ->
    [1]
    { $is_referral_enable ->
    [1] <i>📢 Для вас доступна бесплатная реферальная подписка.</i>
    *[0] {""}
    }
    *[0]
    <i>🎁 Для вас доступна бесплатная пробная подписка.</i>
    }
    *[0]
    <b>💳 Управление подпиской:</b>
    }
msg-subscription-plans =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription-conditional }

    <b>📦 Выбор тарифного плана:</b>
msg-subscription-new-success = ✅ <i>Был подключен тарифный план { $plan_name }.</i>
msg-subscription-renew-success = ✅ <i>Ваша подписка продлена на { $added_duration }.</i>
msg-subscription-change-success = ✅ <i>Ваша подписка была изменена.</i>

msg-subscription-details =
    <b>💳 Покупаемая подписка:</b>
    <blockquote>
    • <b>Тариф:</b> { $plan_name }
    • <b>Лимит трафика</b>: { $traffic }
    { $devices ->
    [0] { empty }
    *[HAS] • <b>Лимит устройств</b>: { $devices }
    }{ $has_planned_extra_devices ->
        [1] {""}
    • <b>Доп. устройства:</b> { $planned_extra_devices }
        *[0] {""}
    }
    { $period ->
    [0] { empty }
    *[HAS] • <b>Длительность</b>: { $period }
    }
    { $original_amount ->
    [0] { empty }
    *[HAS] • <b>Стоимость</b>: { $original_amount }
    }
    </blockquote>

msg-subscription-duration =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription-conditional }

    <b>💳 Покупаемая подписка:</b>
    <blockquote>
    • <b>Тариф:</b> { $plan_name }
    • <b>Лимит трафика</b>: { $traffic }
    • <b>Лимит устройств</b>: { $devices }
    </blockquote>
    { $description ->
    [0] {""}
    *[HAS] {""}
    
    ℹ️ <b>Подробное описание:</b>
    <blockquote>
    { $description }
    </blockquote>
    }

    <b>⏳ Выберите длительность:</b>

msg-subscription-payment-method =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription-conditional }

    <b>💳 Покупаемая подписка:</b>
    <blockquote>
    • <b>Тариф:</b> { $plan_name }
    • <b>Лимит трафика</b>: { $traffic }
    • <b>Лимит устройств</b>: { $device_limit }
    • <b>Длительность:</b> { $period }
    </blockquote>

    { $description ->
    [0] {""}
    *[HAS] {""}
    ℹ️ <b>Подробное описание:</b>
    <blockquote>
    { $description }
    </blockquote>

    }

    <b>💳 Выберите способ оплаты</b>

msg-subscription-confirm-balance =
    { hdr-user-profile }
    <blockquote>
    { frg-user-info-inline }
    </blockquote>

    { hdr-subscription }
    <blockquote>
    { frg-subscription-inline }
    </blockquote>

    { msg-subscription-details }

    <b>📋 Итого:</b>
    <blockquote>
    • <b>Метод оплаты:</b> С баланса
    { $purchase_type ->
        [RENEW] { $has_extra_devices_cost ->
            [1] • <b>Подписка:</b> { $original_amount }
    • <b>Доп. устройства:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/мес)
            *[0] • <b>Подписка:</b> { $original_amount }
        }
        [CHANGE] { $has_extra_devices_cost ->
            [1] • <b>Подписка:</b> { $original_amount }
    • <b>Доп. устройства:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/мес)
            *[0] • <b>Подписка:</b> { $original_amount }
        }
        *[OTHER] • <b>Подписка:</b> { $original_amount }
    }
    • <b>Сумма к оплате:</b> { $total_payment }
    </blockquote>

    { $purchase_type ->
        [CHANGE] 
    ⚠️ <i>Текущая подписка будет заменена без пересчета оставшегося срока.</i>
        *[OTHER] {""}
    }

msg-subscription-confirm-yoomoney =
    { hdr-user-profile }
    <blockquote>
    { frg-user-info-inline }
    </blockquote>

    { hdr-subscription }
    <blockquote>
    { frg-subscription-inline }
    </blockquote>

    { msg-subscription-details }

    <b>📋 Итого:</b>
    <blockquote>
    • <b>Метод оплаты:</b> ЮMoney
    { $purchase_type ->
        [RENEW] { $has_extra_devices_cost ->
            [1] • <b>Подписка:</b> { $original_amount }
    • <b>Доп. устройства:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/мес)
            *[0] • <b>Подписка:</b> { $original_amount }
        }
        [CHANGE] { $has_extra_devices_cost ->
            [1] • <b>Подписка:</b> { $original_amount }
    • <b>Доп. устройства:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/мес)
            *[0] • <b>Подписка:</b> { $original_amount }
        }
        *[OTHER] • <b>Подписка:</b> { $original_amount }
    }
    • <b>Сумма к оплате:</b> { $total_payment }
    </blockquote>

    { $purchase_type ->
        [CHANGE] 
    ⚠️ <i>Текущая подписка будет заменена без пересчета оставшегося срока.</i>
        *[OTHER] {""}
    }

msg-subscription-confirm-yookassa =
    { hdr-user-profile }
    <blockquote>
    { frg-user-info-inline }
    </blockquote>

    { hdr-subscription }
    <blockquote>
    { frg-subscription-inline }
    </blockquote>

    { msg-subscription-details }

    <b>📋 Итого:</b>
    <blockquote>
    • <b>Метод оплаты:</b> ЮKassa
    { $purchase_type ->
        [RENEW] { $has_extra_devices_cost ->
            [1] • <b>Подписка:</b> { $original_amount }
    • <b>Доп. устройства:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/мес)
            *[0] • <b>Подписка:</b> { $original_amount }
        }
        [CHANGE] { $has_extra_devices_cost ->
            [1] • <b>Подписка:</b> { $original_amount }
    • <b>Доп. устройства:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/мес)
            *[0] • <b>Подписка:</b> { $original_amount }
        }
        *[OTHER] • <b>Подписка:</b> { $original_amount }
    }
    • <b>Сумма к оплате:</b> { $total_payment }
    </blockquote>

    { $purchase_type ->
        [CHANGE] 
    ⚠️ <i>Текущая подписка будет заменена без пересчета оставшегося срока.</i>
        *[OTHER] {""}
    }

msg-subscription-confirm =
    { hdr-user-profile }
    <blockquote>
    { frg-user-info-inline }
    </blockquote>

    { hdr-subscription }
    <blockquote>
    { frg-subscription-inline }
    </blockquote>

    { msg-subscription-details }

    <b>📋 Итого:</b>
    <blockquote>
    • <b>Метод оплаты:</b> { gateway-type }
    { $purchase_type ->
        [RENEW] { $has_extra_devices_cost ->
            [1] • <b>Подписка:</b> { $original_amount }
    • <b>Доп. устройства:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/мес)
            *[0] • <b>Подписка:</b> { $original_amount }
        }
        [CHANGE] { $has_extra_devices_cost ->
            [1] • <b>Подписка:</b> { $original_amount }
    • <b>Доп. устройства:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/мес)
            *[0] • <b>Подписка:</b> { $original_amount }
        }
        *[OTHER] • <b>Подписка:</b> { $original_amount }
    }
    { $discount_percent ->
        [0] • <b>Сумма к оплате:</b> { $total_payment }
        *[OTHER] • <b>Сумма к оплате:</b> { $total_payment } <i>({ $discount_percent }% скидка)</i>
    }
    </blockquote>

    { $purchase_type ->
        [CHANGE] 
    ⚠️ <i>Текущая подписка будет заменена без пересчета оставшегося срока.</i>
        *[OTHER] {""}
    }

msg-subscription-trial =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    <b>✅ Пробная подписка успешно получена!</b>

msg-subscription-referral-code =
    <b>📢 Реферальная подписка</b>

    Введите реферальный код пользователя, который вас пригласил:

msg-subscription-referral-success =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    <b>🎉 Подписка успешно улучшена до Реферальной!</b>

msg-subscription-promocode =
    <b>🎟 Введите промокод</b>

    Отправьте код промокода для активации бонусов или скидок.

msg-subscription-success =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    { $purchase_type ->
    [ADD_DEVICE] ✅<i>К вашей подписке добавлено { $device_count } { $device_count ->
        [1] устройство
        [2] устройства
        [3] устройства
        [4] устройства
        *[other] устройств
    }!</i>
    [NEW] { msg-subscription-new-success }
    [RENEW] { msg-subscription-renew-success }
    [CHANGE] { msg-subscription-change-success }
    *[OTHER] {""}
    }

msg-subscription-failed = 
    <b>❌ Произошла ошибка!</b>

    Не волнуйтесь, техподдержка уже уведомлена и свяжется с вами в ближайшее время. Приносим извинения за неудобства.


# Importer
msg-importer-main =
    <b>📥 Импорт пользователей</b>

    Запуск синхронизации: проверка всех пользователей в Панели. Если пользователя нет в базе бота, он будет создан и получит временную подписку. Если данные пользователя отличаются, они будут автоматически обновлены.

msg-importer-from-xui =
    <b>📥 Импорт пользователей (3X-UI)</b>
    
    { $has_exported -> 
    [1]
    <b>🔍 Найдено:</b>
    <blockquote>
    Всего пользователей: { $total }
    С активной подпиской: { $active }
    С истекшей подпиской: { $expired }
    </blockquote>
    *[0]
    Импортируются все активные пользователи с числовым email.

    Рекомендуется заранее отключить пользователей, у которых в поле email отсутствует Telegram ID. Операция может занять значительное время в зависимости от количества пользователей.

    Отправьте файл базы данных (в формате .db).
    }

msg-importer-squads =
    <b>🔗 Список внутренних сквадов</b>

    Выберите, какие внутренние группы будут доступны импортированным пользователям.

msg-importer-import-completed =
    <b>📥 Импорт пользователей завершен</b>
    
    <b>📃 Информация:</b>
    <blockquote>
    • <b>Всего пользователей</b>: { $total_count }
    • <b>Успешно импортированы</b>: { $success_count }
    • <b>Не удалось импортировать</b>: { $failed_count }
    </blockquote>

msg-importer-sync-completed =
    <b>📥 Синхронизация пользователей завершена</b>

    <b>📃 Информация:</b>
    <blockquote>
    Всего пользователей в панели: { $total_panel_users }
    Всего пользователей в боте: { $total_bot_users }

    Новые пользователи: { $added_users }
    Добавлены подписки: { $added_subscription }
    Обновлены подписки: { $updated}
    
    Пользователи без Telegram ID: { $missing_telegram }
    Ошибки при синхронизации: { $errors }
    </blockquote>

msg-importer-sync-bot-to-panel-completed =
    <b>📤 Синхронизация из телеграма в панель завершена</b>

    <b>📃 Информация:</b>
    <blockquote>
    Всего пользователей в боте: { $total_bot_users }

    Создано в панели: { $created }
    Обновлено в панели: { $updated }
    Пропущено (без подписки): { $skipped }
    Ошибки при синхронизации: { $errors }
    </blockquote>


# Promocodes
msg-promocodes-main = <b>🎟 Промокоды</b>

    Создавайте и управляйте промокодами для пользователей.

msg-promocodes-search = <b>🔍 Поиск промокода</b>

    Введите код промокода для поиска.

msg-promocodes-list = <b>📃 Список промокодов</b>

    { $count ->
        [0] Нет созданных промокодов.
        [1] Найден { $count } промокод.
        [2] Найдено { $count } промокода.
        [3] Найдено { $count } промокода.
        [4] Найдено { $count } промокода.
        *[other] Найдено { $count } промокодов.
    }

msg-promocode-view =
    <b>🎟 Просмотр промокода</b>

    <blockquote>
    • <b>Код</b>: <code>{ $code }</code>
    • <b>Тип</b>: { promocode-type }
    • <b>Статус</b>: { $is_active -> 
        [1] 🟢 Включен
        *[0] 🔴 Выключен
        }
    </blockquote>

    <blockquote>
    { $promocode_type ->
    [DURATION] • <b>Бонус</b>: +{ $reward }
    [PERSONAL_DISCOUNT] • <b>Постоянная скидка</b>: { $reward }%
    [PURCHASE_DISCOUNT] • <b>Одноразовая скидка</b>: { $reward }%
    *[OTHER] • <b>Награда</b>: { $reward }
    }
    • <b>Срок действия</b>: { $lifetime }
    • <b>Использовано</b>: { $activations_count } / { $max_activations }
    </blockquote>

msg-promocode-configurator =
    <b>🎟 Создание промокода</b>

    <blockquote>
    • <b>Название</b>: { $name }
    • <b>Код</b>: <code>{ $code }</code>
    • <b>Тип награды</b>: { promocode-type }
    </blockquote>

    <blockquote>
    { $promocode_type ->
    [DURATION] • <b>Бонус</b>: +{ $reward }
    [PERSONAL_DISCOUNT] • <b>Постоянная скидка</b>: { $reward }%
    [PURCHASE_DISCOUNT] • <b>Одноразовая скидка</b>: { $reward }%
    *[OTHER] • <b>Награда</b>: { $reward }
    }
    • <b>Срок действия</b>: { $lifetime }
    • <b>Лимит активаций</b>: { $max_activations }
    </blockquote>

    Выберите пункт для изменения.

msg-promocode-name = <b>📝 Название промокода</b>

    Введите название промокода (1-50 символов).

msg-promocode-code = <b>🏷️ Код промокода</b>

    Введите код промокода (3-20 символов) или нажмите кнопку для генерации случайного кода.

msg-promocode-type = <b>🔖 Выберите тип промокода:</b>

    <blockquote>
    • <b>Одноразовая скидка</b> - скидка исчезнет после первой покупки, или по истечению срока действия промокода.

    • <b>Постоянная скидка</b> - постоянная скидка для пользователя.

    • <b>Дни к подписке</b> - Добавление дней к подписке пользователя.
    </blockquote>

msg-promocode-reward = <b>🎁 Награда</b>

    <b>Тип награды</b>: { promocode-type }

    { $promocode_type ->
    [DURATION] Введите <b>количество дней</b> для бонуса к подписке.
    [PERSONAL_DISCOUNT] Введите <b>процент скидки</b> (1-100) для постоянной скидки.
    [PURCHASE_DISCOUNT] Введите <b>процент скидки</b> (1-100) для скидки на покупку.
    *[OTHER] Введите значение награды.
    }

msg-promocode-lifetime = <b>⌛ Срок действия</b>

    Выберите срок действия промокода в днях.

msg-promocode-lifetime-input = ⌛️Введите срок действия промокода в днях.

msg-promocode-quantity = <b>🔢 Количество активаций</b>

    Выберите максимальное количество активаций промокода.

msg-promocode-quantity-input = 🔢 Введите количество активаций промокода.
msg-promocode-access = <b>📦 Доступ к тарифам</b>

# Bonus Activation
msg-bonus-activate =
    <b>💎 Активация бонусов</b>

    Доступно бонусов: <b>{ $referral_balance }</b>
    Выбранная сумма: <b>{ $current_bonus_amount } ₽</b>

msg-bonus-activate-custom =
    <b>💎 Активация бонусов</b>

    Доступно бонусов: <b>{ $referral_balance }</b>

    Введите сумму для активации (от 1 до { $referral_balance }):

# Terms of Service Settings
msg-dashboard-settings-tos =
    <b>📋 Соглашение с пользователем</b>
    
    <blockquote>
    • Статус: { $status }
    • Источник: { $source }
    </blockquote>

    🔽 Укажите ссылку на документ с правилами.

msg-dashboard-settings-tos-url =
    <b>🔗 Ссылка на Соглашение</b>

    <blockquote>
    Введите ссылку (в формате https://telegram.org/tos).
    </blockquote>

# Community Settings
msg-dashboard-settings-community =
    <b>👥 Сообщество</b>
    
    <blockquote>
    • Статус: { $status }
    • Телеграм группа: { $url_display }
    </blockquote>

    🔽 Укажите ссылку на Telegram группу.

msg-dashboard-settings-community-url =
    <b>🔗 Ссылка на Telegram группу</b>

    <blockquote>
    Введите ссылку (в формате https://t.me/+код или https://t.me/название_группы).
    </blockquote>

# Finances Settings
msg-dashboard-settings-finances =
    <b>💰 Финансы</b>
    
    <blockquote>
    • <b>Валюта по умолчанию:</b> { $default_currency } ({ $default_currency_name })
    </blockquote>

    <i>ℹ️ При включении синхронизации курс валют автоматически синхронизируются с курсом центрабанка РФ.</i>

# Currency Rates Settings
msg-dashboard-settings-currency-rates =
    <b>💱 Курс валют</b>

    Укажите курс обмена относительно рубля.
    Цены в тарифах будут автоматически пересчитываться.

msg-dashboard-settings-currency-rate-input =
    <b>💱 Курс { $currency }</b>

    Введите курс { $symbol } к рублю (например: 90.5).
    1 { $symbol } = X ₽

# Payment Link for Extra Devices
msg-add-device-payment-link = <b>💳 Ссылка для оплаты</b>

Нажмите на кнопку ниже, чтобы перейти к оплате за дополнительные устройства.

# Device Deletion Warning
msg-device-deletion-warning = ⚠️ Для удаления нажмите еще раз на кнопку удалить.
    Устройство будет работать до конца оплаченного срока.
msg-extra-device-deletion-confirm = ⚠️ Дополнительные устройства будут удалены { $expires_date }.
    Они будут работать до конца оплаченного срока и не будут учитываться при продлении подписки.
    Нажмите кнопку удаления повторно для подтверждения.
