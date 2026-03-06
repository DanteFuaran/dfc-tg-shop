# Database Management
msg-db-main =
    <b>🗄 Database Management</b>

    <blockquote>
    • <b>Save</b> - create a backup copy of the database
    • <b>Load</b> - restore database from backup
    • <b>Clear All</b> - delete all data from database
    • <b>Clear Users</b> - delete only users
    • <b>Sync</b> - synchronize data between bot and panel
    </blockquote>

    <b>🔽 Select an action:</b>
    
msg-db-clear-all-confirm =
    <b>⚠️ WARNING!</b>

    <blockquote>
    You are about to <b>completely clear the database</b>.
    
    Will be deleted:
    • All users
    • All subscriptions
    • All transactions
    • All promo codes and their activations
    • All referrals and rewards
    • All notifications
    </blockquote>

    <b>⚠️ This action is irreversible!</b>
    
    <i>Press the button again to confirm clearing.</i>

msg-db-clear-users-confirm =
    <b>⚠️ WARNING!</b>

    <blockquote>
    You are about to <b>delete all users</b> from the database.
    
    Will be deleted:
    • All users
    • All user subscriptions
    • All user transactions
    • All promo code activations
    • All referrals and rewards
    </blockquote>

    <b>⚠️ This action is irreversible!</b>
    
    <i>Press the button below again to confirm.</i>

msg-db-clear-users-result =
    <b>✅ User deletion completed successfully!</b>

    <blockquote>
    📊 Total:
    • Users: <b>{ $users }</b>
    • Subscriptions: <b>{ $subscriptions }</b>
    • Transactions: <b>{ $transactions }</b>
    • Activations: <b>{ $activations }</b>
    • Referrals: <b>{ $referrals }</b>
    • Rewards: <b>{ $rewards }</b>
    </blockquote>

msg-db-clear-users-failed =
    <b>❌ Error deleting users</b>

    { $error }

msg-db-imports =
    <b>📥 Import</b>

    Wählen Sie eine Quelle für den Benutzerimport:

msg-db-load =
    <b>📁 Select file to load</b>

msg-db-sync =
    <b>🔄 Datensynchronisation</b>

    <blockquote>    
    • <b>Vom Panel zum Bot</b>
    Benutzerdaten aus dem Panel werden im Bot aktualisiert.
    Wenn ein Benutzer nicht im Bot existiert, wird er erstellt.
    
    • <b>Vom Bot zum Panel</b>
    Benutzerdaten aus dem Bot werden im Panel aktualisiert.
    Wenn ein Benutzer nicht im Panel existiert, wird er erstellt.
    </blockquote>

    <i>⚠️ Die Synchronisation kann einige Zeit dauern.</i>

msg-db-sync-progress =
    <b>🔄 Synchronizing...</b>

    <blockquote>
    Please wait. Synchronization is running in the background.
    You will receive a notification upon completion.
    </blockquote>

msg-db-import =
    <b>📥 SQLite Import</b>
    
    Select a file for import:

msg-db-restore-success =
    <b>✅ Database successfully restored from uploaded dump.</b>

msg-db-restore-failed =
    <b>❌ Error restoring database: { $error }</b>

# Settings
msg-dashboard-settings =
    <b>⚙️ Settings</b>

    🔽 Select a parameter:

msg-dashboard-settings-transfers =
    <b>💸 Transfer Settings</b>

    <blockquote>
    • Status: { $enabled ->
        [1] ✅ Enabled
        *[0] 🔴 Disabled
    }
    • Commission type: { $commission_type_display }
    • Commission: { $commission_display }
    • Minimum amount: { $min_amount } ₽
    • Maximum amount: { $max_amount } ₽
    </blockquote>


msg-dashboard-settings-transfers-commission-type =
    <b>💰 Commission Type Selection</b>

    <blockquote>
    • <b>Percentage</b> - commission is charged as a percentage of the transfer amount
    • <b>Fixed</b> - commission is charged as a fixed amount regardless of transfer amount
    </blockquote>

    Select commission type:

msg-dashboard-settings-transfers-commission-value =
    <b>💵 Commission Value</b>

    <blockquote>
    • Commission type: { $commission_type_display }
    • Current commission: { $db_commission_display }
    • Change to: { $selected_display }
    </blockquote>

    Select a price or enter your own:

msg-commission-manual-input =
    <b>✏️ Manual Input</b>

    <blockquote>
    Enter commission value:
    </blockquote>

msg-dashboard-settings-transfers-min-amount =
    <b>📉 Minimum Transfer Amount</b>

    <blockquote>
    • Current minimum amount: { $db_min_current_display }
    • Change to: { $min_selected_display }
    </blockquote>

    Select an amount or enter your own:

msg-min-amount-manual-input =
    <b>✏️ Manual Input</b>

    <blockquote>
    Enter minimum transfer amount (in rubles):
    </blockquote>

msg-dashboard-settings-transfers-max-amount =
    <b>📈 Maximum Transfer Amount</b>

    <blockquote>
    • Current maximum amount: { $db_max_current_display }
    • Change to: { $max_selected_display }
    </blockquote>

    Select an amount or enter your own:

msg-max-amount-manual-input =
    <b>✏️ Manual Input</b>

    <blockquote>
    Enter maximum transfer amount (in rubles):
    </blockquote>

# Balance Settings
msg-dashboard-settings-balance =
    <b>💰 Balance Settings</b>

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
    <b>📉 Minimum Balance Top-up Amount</b>

    <blockquote>
    • Current minimum amount: { $balance_min_current_display }
    • Change to: { $balance_min_selected_display }
    </blockquote>

    Select an amount:

msg-dashboard-settings-balance-max-amount =
    <b>📈 Maximum Balance Top-up Amount</b>

    <blockquote>
    • Current maximum amount: { $balance_max_current_display }
    • Change to: { $balance_max_selected_display }
    </blockquote>

    Select an amount:

# Extra Devices Settings
msg-dashboard-extra-devices-settings =
    <b>📱 Extra Devices Settings</b>

    <blockquote>
    • Status: { $enabled ->
        [1] ✅ Enabled
        *[0] 🔴 Disabled
    }
    • Payment type: { $payment_type_display }
    • Device cost: { $extra_devices_price } ₽
    • Minimum days: { $min_days } { $min_days ->
        [1] day
        *[other] days
    }
    </blockquote>


msg-dashboard-extra-devices-price =
    <b>💵 Extra Device Cost</b>

    <blockquote>
    • Current price: { $current_price } ₽
    • Change to: { $selected_price } ₽
    </blockquote>

    Select a price or enter your own:

msg-dashboard-extra-devices-price-manual =
    <b>✏️ Manual Price Entry</b>

    <blockquote>
    Enter extra device price (in rubles):
    </blockquote>

msg-dashboard-extra-devices-min-days =
    <b>⏳ Minimum Days</b>

    <blockquote>
    • Current: { $current_min_days } days
    • Change to: { $selected_min_days } days
    </blockquote>

    Minimum days remaining on subscription to allow purchasing an extra device slot.

msg-dashboard-extra-devices-min-days-manual =
    <b>⏳ Minimum Days</b>

    Enter minimum days (from 1 to 365)

    Select days:

# Global Discount Settings
msg-dashboard-settings-global-discount =
    <b>🏷️ Global Discount Settings</b>

    <blockquote>
    • Status: { $enabled ->
        [1] ✅ Enabled
        *[0] 🔴 Disabled
    }
    • Discount type: { $discount_type_display }
    • Discount: { $discount_display }
    • Mode: { $stack_mode_display }
    • Applies to: { $apply_to_display }
    </blockquote>

msg-global-discount-apply-to =
    <b>📌 What Discount Affects</b>

    <blockquote>
    Operations affected by global discount.
    </blockquote>

msg-global-discount-mode =
    <b>⚙️ Discount Application Mode</b>

    <blockquote>
    • <b>Maximum</b> - use the highest of the applied discounts
    
    • <b>Stacked</b> - combine both discounts
    </blockquote>

msg-dashboard-settings-global-discount-value =
    <b>💵 Discount Value</b>

    <blockquote>
    • Discount type: { $discount_type_display }
    • Current discount: { $db_discount_display }
    • Change to: { $selected_display }
    </blockquote>

    Select a discount or enter your own:

msg-global-discount-manual-input =
    <b>✏️ Manual Input</b>

    <blockquote>
    Enter discount value:
    </blockquote>

# Language Settings
msg-dashboard-settings-language =
    <b>🌐 Spracheinstellungen</b>
    <blockquote>
    • Mehrsprachigkeit: { $enabled ->
        [1] 🟢 Aktiviert
        *[0] 🔴 Deaktiviert
    }
    • Aktuelle Sprache: { $current_locale }
    </blockquote>

    <i>ℹ️ Mehrsprachigkeit:</i>
    🟢 Aktiviert - jeder Benutzer sieht den Bot in seiner Sprache
    🔴 Deaktiviert - alle Benutzer sehen die ausgewählte Sprache

msg-main-menu =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }{ frg-subscription-status-full }

msg-menu-connect =
    <b>📝 Instructions:</b>
    <blockquote>
    • Download and install the app.
    • Press 🔗Connect.
    • In the app press Enable.
    </blockquote>

msg-menu-devices =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { $has_subscription ->
        [0] <blockquote>
    • Sie haben kein aktives Abonnement.
    </blockquote>
        *[other] { frg-subscription }
    }

    📱 <b>Device Management:</b>

msg-add-device =
    <b>➕ Add Device</b>

msg-add-device-select-count =
    { $has_discount ->
    [1] ℹ️<i>Extra device cost: { $device_price }₽/mo  <s>{ $device_price_original }₽</s>/mo.</i>
    *[0] ℹ️<i>Extra device cost: { $device_price }₽/mo.</i>
    }

    📱 <b>Select number of devices:</b>

msg-add-device-full =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    { $has_discount ->
    [1] ℹ️<i>Extra device cost: { $device_price }₽/mo  <s>{ $device_price_original }₽</s>/mo.</i>
    *[0] ℹ️<i>Extra device cost: { $device_price }₽/mo.</i>
    }

    📱 <b>Select number of devices:</b>

msg-add-device-duration =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    📱 <b>Purchase:</b>
    <blockquote>
    • <b>Extra devices:</b> { $device_count }
    </blockquote>

    📅 <b>Select duration:</b>

msg-add-device-payment =
    📱 <b>Purchase:</b>
    <blockquote>
    • <b>Extra devices:</b> { $device_count }
    </blockquote>

    💳 <b>Select payment method:</b>

msg-add-device-payment-full =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    📱 <b>Purchase:</b>
    <blockquote>
    • <b>Extra devices:</b> { $device_count }
    </blockquote>

    💳 <b>Select payment method:</b>

msg-add-device-confirm-full =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    📱 <b>Purchase:</b>
    <blockquote>
    • <b>Extra devices:</b> { $device_count }
    </blockquote>

    📋 <b>Total:</b>
    <blockquote>
    💳 <b>Payment method:</b> { gateway-type }
    { $is_balance_payment ->
    [1]
    📊 <b>Current balance:</b> { $balance }
    📊 <b>Balance after:</b> { $new_balance }
    *[0]
    { $has_discount ->
    [1]
    💰 <b>Amount to pay:</b> <s>{ $original_price }</s> { $total_price }
    *[0]
    💰 <b>Amount to pay:</b> { $total_price }
    }
    }
    </blockquote>

    💳 <b>Confirm purchase:</b>

msg-add-device-success-full =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    ℹ️ <i>{ $device_count } { $device_count_word } added to your subscription.</i>

    ✅ <b>Payment successful!</b>

msg-extra-devices-list =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    📱 <b>Extra Devices</b>
    { $purchases_empty ->
        [true] <i>You have no active extra devices.</i>
        *[false] <blockquote>
    💰 <b>Monthly cost:</b> { $total_monthly_cost }
    📱 <b>Total extra devices:</b> { $total_extra_devices }
    <i>Devices are active until the end of subscription month.</i>
    </blockquote>
    
    <i>Press ❌ to cancel device subscription.</i>
    }

msg-extra-device-manage =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    📱 <b>Extra Device Management</b>
    
    <blockquote>
    • <b>Device count:</b> { $purchase_device_count }
    • <b>Cost/mo:</b> { $purchase_price } ₽
    • <b>Expires:</b> { $purchase_expires_at }
    • <b>Auto-renewal:</b> { $purchase_auto_renew ->
        [1] ✅ Enabled
        *[0] ❌ Disabled
    }
    </blockquote>
    
    { $purchase_auto_renew ->
        [1] <i>When auto-renewal is disabled, devices will be removed after expiration.</i>
        *[0] <i>Auto-renewal is disabled. Devices will be removed in { $purchase_days_remaining } days.</i>
    }

msg-add-device-confirm-details =
    📱 <b>Purchase:</b>
    <blockquote>
    • <b>Extra devices:</b> { $device_count }
    </blockquote>

    📋 <b>Total:</b>
    <blockquote>
    • <b>Payment method:</b> { $selected_method }
    • <b>Current balance:</b> { $balance }
    • <b>Balance after:</b> { $new_balance }
    </blockquote>

    💳<b>Confirm purchase:</b>

msg-balance-menu =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription-status-full }

    <b>💰 Balance Management:</b>

msg-balance-select-gateway =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription-conditional }

    <b>💰 Select payment method:</b>

msg-balance-select-amount =
    <b>💰 Balance Top-up</b>

    Payment method: <b>{ $selected_gateway }</b>

    Select top-up amount:

msg-balance-enter-amount =
    <b>💰 Balance Top-up</b>

    Payment method: <b>{ $selected_gateway }</b>

    Enter top-up amount (from { $min_amount } to { $max_amount } { $currency }):

msg-balance-confirm =
    <b>💰 Top-up Confirmation</b>

    Payment method: <b>{ $selected_gateway }</b>
    Amount: <b>{ $topup_amount } { $currency }</b>

    Press the button below to pay.

msg-balance-success =
    <b>✅ Balance topped up successfully!</b>
    
    <blockquote>
    <b>{ $amount }{ $currency }</b> credited to your account
    </blockquote>

msg-balance-transfer =
    <b>💸 Balance Transfer</b>

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
    <b>💸 Recipient</b>

    <blockquote>
    Enter recipient's <b>Telegram ID</b>:
    </blockquote>

msg-balance-transfer-recipient-history =
    <b>📜 User History</b>

    Select a recipient from the list of users you've previously transferred to:

msg-balance-transfer-no-history = <i>You don't have any transfer history yet.</i>

msg-balance-transfer-amount-value =
    <b>💸 Transfer Amount</b>

    <blockquote>
    • Current amount: { $current_display }
    • Change to: { $selected_display }
    </blockquote>

    Select an amount or enter your own:

msg-balance-transfer-amount-manual =
    <b>✏️ Manual Input</b>

    <blockquote>
    Enter transfer amount (from { $min_amount } to { $max_amount } ₽):
    </blockquote>

msg-balance-transfer-message =
    <b>💬 Message</b>

    <blockquote>
    { $message_display }
    </blockquote>

    <i>Enter a message for the transfer (max 200 characters):</i>

msg-balance-transfer-confirm =
    <b>💸 Transfer Confirmation</b>

    <blockquote>
    Recipient: <b>{ $recipient_name }</b> (<code>{ $recipient_id }</code>)
    Transfer amount: <b>{ $amount } ₽</b>
    Commission: <b>{ $commission } ₽</b>
    Total to deduct: <b>{ $total } ₽</b>
    </blockquote>

    ⚠️ <b>Warning:</b> This operation is irreversible!

msg-balance-transfer-success =
    <b>✅ Transfer completed successfully!</b>

    <blockquote>
    Recipient: <b>{ $recipient_name }</b>
    Amount: <b>{ $amount } ₽</b>
    Commission: <b>{ $commission } ₽</b>
    </blockquote>

msg-balance-transfer-error =
    <b>❌ Transfer Error</b>

    { $error }

msg-menu-invite =
    <b>👥 Invite Friends</b>

    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }{ frg-subscription-status-full }

    <b>🏆 Reward:</b>
    <blockquote>
    { $ref_reward_type ->
        [EXTRA_DAYS] • { $ref_reward_level_1_value } days for every 100 { $currency_symbol } topped up by invitee
        [MONEY] • { $ref_reward_level_1_value }% of the amount topped up by invitee
        *[OTHER] • { $ref_reward_level_1_value } { $currency_symbol }
    }{ $ref_max_level ->
        [2] {""}
    
    { $ref_reward_type ->
        [EXTRA_DAYS] • { $ref_reward_level_2_value } days for every 100 { $currency_symbol } topped up by invitee's invitees
        [MONEY] • { $ref_reward_level_2_value }% of the amount topped up by invitee's invitees
        *[OTHER] • { $ref_reward_level_2_value } { $currency_symbol }
    }
        *[1] {""}
    }
    </blockquote>

    <b>📊 Statistics:</b>
    <blockquote>
    👥 Total invited: { $referrals }
    💳 Payments via your link: { $payments }
    💳 Total received: { $total_bonus }{ $ref_reward_type ->
        [EXTRA_DAYS] { " " }days
        *[OTHER] {""}
    }
    </blockquote>

    <i>ℹ️ Rewards are credited when users you invite make payments.</i>

msg-menu-invite-about =
    <b>🎁 More About Rewards</b>

    <b>✨ How to get rewards:</b>
    <blockquote>
    { $accrual_strategy ->
    [ON_FIRST_PAYMENT] Rewards are credited for the first subscription purchase by the invited user.
    [ON_EACH_PAYMENT] Rewards are credited for each purchase or subscription renewal by the invited user.
    *[OTHER] { $accrual_strategy }
    }
    </blockquote>

    <b>💎 What you get:</b>
    <blockquote>
    { $max_level -> 
    [1] For invited friends: { $reward_level_1 }
    *[MORE]
    { $identical_reward ->
    [0]
    1️⃣ For your friends: { $reward_level_1 }
    2️⃣ For friends invited by your friends: { $reward_level_2 }
    *[1]
    For your friends and friends invited by your friends: { $reward_level_1 }
    }
    }
    
    { $reward_strategy_type ->
    [AMOUNT] { $reward_type ->
        [MONEY] { space }
        [EXTRA_DAYS] <i>(All extra days are added to your current subscription)</i>
        *[OTHER] { $reward_type }
    }
    [PERCENT] { $reward_type ->
        [MONEY] <i>(Percentage of their purchased subscription cost)</i>
        [EXTRA_DAYS] <i>(Percentage of extra days from their purchased subscription)</i>
        *[OTHER] { $reward_type }
    }
    *[OTHER] { $reward_strategy_type }
    }
    </blockquote>

msg-invite-reward = { $value }{ $reward_strategy_type ->
    [AMOUNT] { $reward_type ->
        [POINTS] { space }{ $value -> 
            [one] point
            *[other] points
            }
        [EXTRA_DAYS] { space }extra { $value -> 
            [one] day
            *[other] days
            }
        [MONEY] ₽
        *[OTHER] { $reward_type }
    }
    [PERCENT] % { $reward_type ->
        [POINTS] points
        [EXTRA_DAYS] extra days
        [MONEY] of payment amount
        *[OTHER] { $reward_type }
    }
    *[OTHER] { $reward_strategy_type }
    }

msg-menu-invite-edit-code =
    ✏️ <b>Empfehlungscode ändern</b>

    <blockquote>• Aktueller Code: <code>{ $referral_code }</code></blockquote>

    <i>Gib deinen neuen Empfehlungscode ein.</i>
    { $ref_code_error ->
        [invalid]

    ⚠️ <b>Ungültiger Code.</b>
    Erlaubt: A–Z, a–z, 0–9, _ - (Länge 3–32)
        [taken]

    ⚠️ Dieser Code ist bereits vergeben. Wähle einen anderen.
        *[other] {""}
    }


# Dashboard
msg-dashboard-main =
    <b>🛠 Control Panel v{ $bot_version }</b> { $update_available ->
        [1] — 🔔 Update verfügbar: <b>{ $new_version }</b>
        *[0] {""}
    }
msg-bot-management =
    <b>🤖 Bot-Verwaltung</b>
msg-mirror-bots =
    <b>🤖 Zusätzliche Bots</b>

    <blockquote>Hier können Sie Mirror-Bots hinzufügen. Tippen Sie auf einen Bot, um ihn als <b>primär</b> festzulegen - Einladungslinks verweisen dann auf ihn.</blockquote>
msg-mirror-bot-add-token =
    <b>➕ Neuen Bot hinzufügen</b>

    Senden Sie das API-Token des neuen Bots, das Sie von @BotFather erhalten haben.
msg-dashboard-user-management =
    <b>👥 Benutzerverwaltung</b>
msg-dashboard-features =
    <b>⚙️ Features</b>

    <blockquote>
    Here you can enable or disable various bot features.
    </blockquote>

msg-dashboard-extra-devices =
    <b>📱 Extra Devices</b>

    <b>Status:</b> { $enabled ->
        [1] ✅ Enabled
        *[0] ⬜ Disabled
    }
    <b>Cost:</b> { $price } ₽/mo per device

    <blockquote>
    Allows users to add extra devices to their subscription for an additional fee.
    </blockquote>

msg-dashboard-extra-devices-price =
    <b>💰 Change Extra Device Cost</b>

    <b>Current cost:</b> { $current_price } ₽

    Select a cost or enter manually:

msg-dashboard-extra-devices-price-manual =
    <b>💰 Manual Cost Entry</b>

    Enter new cost in rubles (integer from 0 to 100000):

msg-dashboard-extra-devices-settings =
    <b>📱 Extra Device Settings</b>

    <b>Current cost:</b> { $price } ₽ per device
    <b>Payment type:</b> { $is_one_time ->
    [1] One-time
    *[0] Monthly
    }

    <blockquote>
    <b>One-time</b> - user pays for devices once, they remain until deleted.
    
    <b>Monthly</b> - device cost is added with each subscription renewal.
    </blockquote>

msg-users-main = <b>👥 Users</b>
msg-broadcast-main = <b>📢 Broadcast</b>

msg-statistics-main = { $statistics }
    
msg-statistics-users =
    <b>👥 User Statistics</b>

    <blockquote>
    • <b>Total</b>: { $total_users }
    • <b>New today</b>: { $new_users_daily }
    • <b>New this week</b>: { $new_users_weekly }
    • <b>New this month</b>: { $new_users_monthly }

    • <b>With subscription</b>: { $users_with_subscription }
    • <b>Without subscription</b>: { $users_without_subscription }
    • <b>With trial</b>: { $users_with_trial }

    • <b>Blocked</b>: { $blocked_users }
    • <b>Blocked bot</b>: { $bot_blocked_users }

    • <b>User → purchase conversion</b>: { $user_conversion }%
    • <b>Trial → subscription conversion</b>: { $trial_conversion }%
    </blockquote>

msg-statistics-transactions =
    <b>🧾 Transaction Statistics</b>

    <blockquote>
    • <b>Total transactions</b>: { $total_transactions }
    • <b>Completed transactions</b>: { $completed_transactions }
    • <b>Free transactions</b>: { $free_transactions }
    { $popular_gateway ->
    [0] { empty }
    *[HAS] • <b>Popular payment system</b>: { $popular_gateway }
    }
    </blockquote>

    <b>💰 Real money:</b>
    
    { $payment_gateways }

    <b>🎁 User bonuses:</b>
    
    { $bonus_gateways }

msg-statistics-subscriptions =
    <b>💳 Subscription Statistics</b>

    <blockquote>
    • <b>Active</b>: { $total_active_subscriptions }
    • <b>Expired</b>: { $total_expire_subscriptions }
    • <b>Trial</b>: { $active_trial_subscriptions }
    • <b>Expiring (7 days)</b>: { $expiring_subscriptions }
    </blockquote>

    <blockquote>
    • <b>Unlimited</b>: { $total_unlimited }
    • <b>Traffic limited</b>: { $total_traffic }
    • <b>Device limited</b>: { $total_devices }
    </blockquote>

msg-statistics-plans = 
    <b>📦 Plan Statistics</b>

    { $plans }

msg-statistics-promocodes =
    <b>🎁 Promo Code Statistics</b>

    <blockquote>
    • <b>Total activations</b>: { $total_promo_activations }
    • <b>Most popular promo code</b>: { $most_popular_promo ->
    [0] { unknown }
    *[HAS] { $most_popular_promo }
    }
    • <b>Days issued</b>: { $total_promo_days }
    • <b>Traffic issued</b>: { $total_promo_days }
    • <b>Subscriptions issued</b>: { $total_promo_subscriptions }
    • <b>Personal discounts issued</b>: { $total_promo_personal_discounts }
    • <b>One-time discounts issued</b>: { $total_promo_purchase_discounts }
    </blockquote>

msg-statistics-referrals =
    <b>👪 Referral System Statistics</b>
    
    <blockquote>
    • <b></b>:
    </blockquote>

msg-statistics-transactions-gateway =
    <b>{ gateway-type }:</b>
    <blockquote>
    • <b>Total income</b>: { $total_income }{ $currency }
    • <b>Daily income</b>: { $daily_income }{ $currency }
    • <b>Weekly income</b>: { $weekly_income }{ $currency }
    • <b>Monthly income</b>: { $monthly_income }{ $currency }
    • <b>Average check</b>: { $average_check }{ $currency }
    • <b>Total discounts</b>: { $total_discounts }{ $currency }
    </blockquote>

msg-statistics-plan =
    <b>{ $plan_name }:</b> { $popular -> 
    [0] { space }
    *[HAS] (⭐)
    }
    <blockquote>
    • <b>Total subscriptions</b>: { $total_subscriptions }
    • <b>Active subscriptions</b>: { $active_subscriptions }
    • <b>Popular duration</b>: { $popular_duration }

    • <b>Total income</b>: 
    { $all_income }
    </blockquote>

msg-statistics-plan-income = { $income }{ $currency }
    


# Access
msg-access-main =
    <b>🔓 Access Mode</b>
    
    <blockquote>
    • <b>Mode</b>: { access-mode }
    • <b>Purchases</b>: { $purchases_allowed ->
    [0] disabled
    *[1] enabled
    }.
    • <b>Registration</b>: { $registration_allowed ->
    [0] disabled
    *[1] enabled
    }.
    </blockquote>

msg-access-conditions =
    <b>⚙️ Access Conditions</b>

msg-access-rules =
    <b>✳️ Change Rules Link</b>

    Enter the link (in format https://telegram.org/tos).
    
    This value is also used in the <b>User Agreement</b> menu.

msg-access-channel =
    <b>❇️ Change Channel/Group Link</b>

    If your group doesn't have a @username, send the group ID and invitation link in separate messages.
    
    If you have a public channel/group, just enter the @username.


# Broadcast
msg-broadcast-list = <b>📄 Broadcast List</b>
msg-broadcast-plan-select = <b>📦 Select plan for broadcast</b>
msg-broadcast-send = <b>📢 Send Broadcast ({ audience-type })</b>

    { $audience_count } { $audience_count ->
    [one] user
    *[other] users
    } will receive the broadcast

msg-broadcast-content =
    <b>✉️ Broadcast-Inhalt</b>

    <b>Aktueller Inhalt:</b>

    { $has_content ->
        [1] <blockquote>{ $current_content }</blockquote>
        *[other] <blockquote>• Nicht ausgefüllt</blockquote>
    }

    <i>Senden Sie eine Nachricht: Text, Bild oder beides zusammen (HTML wird unterstützt).</i>

msg-broadcast-buttons = <b>✳️ Broadcast Buttons</b>

msg-broadcast-view =
    <b>📢 Broadcast</b>

    <blockquote>
    • <b>ID</b>: <code>{ $broadcast_id }</code>
    • <b>Status</b>: { broadcast-status }
    • <b>Audience</b>: { audience-type }
    • <b>Created</b>: { $created_at }
    </blockquote>

    <blockquote>
    • <b>Total messages</b>: { $total_count }
    • <b>Successful</b>: { $success_count }
    • <b>Failed</b>: { $failed_count }
    </blockquote>


# Users
msg-users-recent-registered = <b>🆕 Recently Registered</b>
msg-users-recent-activity = <b>📝 Recently Active</b>
msg-users-all = <b>👥 All Users</b>
msg-user-transactions = <b>🧾 User Transactions</b>
msg-user-devices = <b>📱 User Devices ({ $current_count } / { $max_count })</b>
msg-user-give-access = <b>🔑 Grant Plan Access</b>

msg-users-search =
    <b>🔍 User Search</b>

    Enter user ID, part of name, or forward any message from them.

msg-users-search-results =
    <b>🔍 User Search</b>

    Found <b>{ $count }</b> { $count ->
    [one] user
    *[other] users
    } matching the query

msg-user-main = 
    <b>📝 User Information</b>

    { hdr-user-profile }
    { frg-user-details }

    <b>💸 Discount:</b>
    <blockquote>
    • <b>Personal</b>: { $personal_discount }%
    • <b>Next purchase</b>: { $purchase_discount }%
    </blockquote>
    
    { hdr-subscription }
    { frg-subscription-status-short }

msg-user-referrals = 
    <b>👥 Empfehlungen des Benutzers</b>

    <b>Anzahl der Empfehlungen:</b> { $referral_count }
    <b>Gesamtbonus:</b> { $total_bonus } ₽

msg-user-referrals-list =
    <b>📋 Empfehlungsliste</b>

msg-user-referral-bind = 
    <b>🔗 Empfehlung zuweisen</b>

    Geben Sie die Telegram-ID oder @username des Benutzers ein, den Sie als Empfehlung zuweisen möchten.

msg-user-delete-confirm =
    <b>❌ Benutzer löschen</b>

    <i>Sind Sie sicher? Diese Aktion kann nicht rückgängig gemacht werden.</i>

msg-user-sync = 
    <b>🌀 Synchronize User</b>

    <b>🛍 Telegram:</b>
    <blockquote>
    { $has_bot_subscription -> 
    [0] No data
    *[HAS]{ $bot_subscription }
    }
    </blockquote>

    <b>🌊 Panel:</b> { $remna_version }
    <blockquote>
    { $has_remna_subscription -> 
    [0] No data
    *[HAS] { $remna_subscription }
    }
    </blockquote>

    Select current data for synchronization.

msg-user-sync-version = { $version ->
    [NEWER] (newer)
    [OLDER] (older)
    *[UNKNOWN] { empty }
    }

msg-user-sync-subscription =
    • <b>ID</b>: <code>{ $id }</code>
    • Status: { $status -> 
    [ACTIVE] Active
    [DISABLED] Disabled
    [LIMITED] Traffic exhausted
    [EXPIRED] Expired
    [DELETED] Deleted
    *[OTHER] { $status }
    }
    • Link: <a href="{ $url }">*********</a>

    • Traffic limit: { $traffic_limit }
    • Device limit: { $device_limit }
    • Remaining: { $expire_time }

    • Internal squads: { $internal_squads ->
    [0] { unknown }
    *[HAS] { $internal_squads }
    }
    • External squad: { $external_squad ->
    [0] { unknown }
    *[HAS] { $external_squad }
    }
    • Traffic reset: { $traffic_limit_strategy -> 
    [NO_RESET] On payment
    [DAY] Every day
    [WEEK] Every week
    [MONTH] Every month
    *[OTHER] { $traffic_limit_strategy }
    }
    • Tag: { $tag -> 
    [0] { unknown }
    *[HAS] { $tag }
    }

msg-user-sync-waiting =
    <b>🌀 User Synchronization</b>

    Please wait... User data synchronization in progress. You will automatically return to the user editor upon completion.

msg-user-give-subscription =
    <b>🎁 Grant Subscription</b>

    Select the plan you want to grant to the user.

msg-user-give-subscription-duration =
    <b>⏳ Select Duration</b>

    Select the duration of the subscription to grant.

msg-user-discount =
    <b>💸 Change Personal Discount</b>

    Select from button or enter your own value.

msg-user-balance-menu =
    <b>💰 User Balance</b>

    <b>Main balance:</b> { $current_balance } ₽
    <b>Referral balance:</b> { $referral_balance } ₽

    Select balance type to edit:

msg-user-finance-menu-full =
    <b>💰 Finanzverwaltung</b>

    { $is_balance_enabled ->
        [1] <b>Hauptguthaben:</b> { $current_balance } ₽
        *[0] {""}
    }
    { $is_referral_enable ->
        [1] <b>Bonusguthaben:</b> { $referral_balance } ₽
        *[0] {""}
    }
    <b>Dauerrabatt:</b> { $discount_value }%

    Wählen Sie einen Punkt zum Bearbeiten:

msg-user-finance-menu-short =
    <b>💰 Finanzverwaltung</b>

    <b>Dauerrabatt:</b> { $discount_value }%

    Wählen Sie einen Punkt zum Bearbeiten:

msg-user-main-balance =
    <b>💰 Main Balance</b>

    <b>Current balance: { $current_balance } ₽</b>
    { $has_pending_balance ->
        [1] <b>Pending: { $pending_balance_amount } ₽</b>
        *[0] {""}
    }

    Select an amount or enter your own value.
    Press <b>✅ Accept</b> to confirm.

msg-user-referral-balance =
    <b>🎁 Bonus Balance</b>

    <b>Current balance: { $current_referral_balance } ₽</b>
    { $has_pending_referral ->
        [1] <b>Pending: { $pending_referral_amount } ₽</b>
        *[0] {""}
    }

    Select an amount or enter your own value.
    Press <b>✅ Accept</b> to confirm.

msg-user-points =
    <b>💎 Change Balance</b>

    <b>Current balance: { $current_balance } ₽</b>

    Select from button or enter your own value to add or subtract.

msg-user-subscription-traffic-limit =
    <b>🌐 Change Traffic Limit</b>

    Select from button or enter your own value (in GB) to change traffic limit.

msg-user-subscription-device-limit =
    <b>📱 Bonus Devices</b>

    • Select number of bonus devices for the user, or enter a number from 0 to 100

msg-user-subscription-expire-time =
    <b>⏳ Change Expiration Time</b>

    <b>Expires in: { $expire_time }</b>

    Select from button or enter your own value (in days) to add or subtract.

msg-user-subscription-squads =
    <b>🔗 Squads</b>

    • Internal squad: { $internal_squads ->
    [0] not selected
    *[HAS] { $internal_squads }
    }
    • External squad: { $external_squad ->
    [0] not selected
    *[HAS] { $external_squad }
    }

    ✏️ Select squads:

msg-user-subscription-internal-squads =
    <b>⏺️ Change Internal Squads List</b>

    Select which internal groups will be assigned to this user.

msg-user-subscription-external-squads =
    <b>⏹️ Change External Squad</b>

    Select which external group will be assigned to this user.

msg-user-subscription-empty =
    <b>💳 Subscription Information</b>

    This user has no active subscription.

msg-user-subscription-info =
    <b>💳 Current Subscription Information</b>
    
    { hdr-subscription }
    { frg-subscription-details }

    <blockquote>
    • <b>Squads</b>: { $squads -> 
    [0] { unknown }
    *[HAS] { $squads }
    }
    • <b>First connected</b>: { $first_connected_at -> 
    [0] { unknown }
    *[HAS] { $first_connected_at }
    }
    • <b>Last connected</b>: { $last_connected_at ->
    [0] { unknown }
    *[HAS] { $last_connected_at } ({ $node_name })
    } 
    </blockquote>

    { hdr-plan }
    { frg-plan-snapshot }

msg-user-transaction-info =
    <b>🧾 Transaction Information</b>

    { hdr-payment }
    <blockquote>
    • <b>ID</b>: <code>{ $payment_id }</code>
    • <b>Type</b>: { purchase-type }
    • <b>Status</b>: { transaction-status }
    • <b>Payment method</b>: { gateway-type }
    • <b>Amount</b>: { frg-payment-amount }
    • <b>Created</b>: { $created_at }
    </blockquote>

    { $is_test -> 
    [1] ⚠️ Test transaction
    *[0]
    { hdr-plan }
    { frg-plan-snapshot }
    }
    
msg-user-role = 
    <b>👮‍♂️ Change Role</b>
    
    Select a new role for the user.

msg-users-blacklist =
    <b>🚫 Blacklist</b>

    Blocked: <b>{ $count_blocked }</b> / <b>{ $count_users }</b> ({ $percent }%).

msg-user-message =
    <b>📩 Send Message to User</b>

    Send any message: text, image or both together (HTML supported).
    

# Panel
msg-monitoring =
    <b>📡 Monitoring</b>

    <b>👥 Benutzer</b>
    <blockquote>
    • <b>Gesamt</b>: { $users_total }
    • <b>Aktiv</b>: { $users_active }
    • <b>Deaktiviert</b>: { $users_disabled }
    • <b>Eingeschränkt</b>: { $users_limited }
    • <b>Abgelaufen</b>: { $users_expired }
    • <b>Gesamt online</b>: { $total_online }
    </blockquote>

    <b>📊 Statistiken:</b>
    <blockquote>
    • <b>Server gesamt</b>: { $total_servers }
    • <b>Verfügbar</b>: { $available_servers }
    </blockquote>

    <b>📋 Serverliste:</b>
    <blockquote>
    { $servers_list }
    </blockquote>

msg-monitoring-no-servers = Keine Server verfügbar


# Telegram
msg-remnashop-main = <b>🛍 Telegram</b>
msg-admins-main = <b>👮‍♂️ Administrators</b>


# Gateways
msg-gateways-main = <b>🌐 Payment Systems</b>
msg-gateways-settings = <b>🌐 { gateway-type } Configuration</b>
msg-gateways-settings-detail =
    <b>⚙️ Systemeinstellungen: { gateway-type }</b>

    { $settings_display }

    Wählen Sie was geändert werden soll:
msg-gateways-default-currency = <b>💸 Default Currency</b>
msg-gateways-placement = <b>🔢 Change Positioning</b>

msg-gateways-field =
    <b>🌐 { gateway-type } Configuration</b>

    Enter a new value for { $field }.


# Referral
msg-referral-main =
    <b>👥 Referral System</b>

    <blockquote>
    • <b>Status</b>: { $is_enable -> 
        [1] 🟢 Enabled
        *[0] 🔴 Disabled
        }
    • <b>Reward type</b>: { reward-type }
    • <b>Number of levels</b>: { $level_text }
    • <b>Accrual condition</b>: { accrual-strategy }
    • <b>Accrual form</b>: { reward-strategy }
    • <b>Reward</b>: { $reward_display }
    </blockquote>

    🔽 Select item to change.

msg-referral-level =
    <b>🔢 Change Level</b>

    Select number of referral system levels.

msg-referral-reward-type =
    <b>🎀 Change Reward Type</b>

    Select reward type for invited users.
    
msg-referral-accrual-strategy =
    <b>📍 Change Accrual Condition</b>

    Select the condition under which rewards will be credited.


msg-referral-reward-strategy =
    <b>⚖️ Change Accrual Form</b>

    Select reward calculation method.
    
    <i>When selecting "Days" type: N days are credited for every 100 rubles topped up/purchased.</i>


msg-referral-reward-level = { $level } level: { $value }{ $reward_strategy_type ->
    [AMOUNT] { $reward_type ->
        [POINTS] { space }{ $value -> 
            [one] point
            *[other] points
            }
        [EXTRA_DAYS] { space }extra { $value -> 
            [one] day
            *[other] days
            }
        [MONEY] ₽
        *[OTHER] { $reward_type }
    }
    [PERCENT] % { $reward_type ->
        [POINTS] points
        [EXTRA_DAYS] extra days
        [MONEY] of payment amount
        *[OTHER] { $reward_type }
    }
    *[OTHER] { $reward_strategy_type }
    }
    
msg-referral-reward =
    <b>🎁 Change Reward</b>

    <blockquote>
    { $reward }
    </blockquote>

    { $reward_type ->
        [EXTRA_DAYS] Select number of days per every 100₽ topped up/purchased, or enter value manually.
        *[OTHER] Select reward amount or enter value manually.
    }

msg-referral-reward-manual =
    <b>✏️ Manual Reward Entry</b>

msg-referral-invite-message =
    <b>✉️ Invitation Message Settings</b>

    🔽 Select an action:

msg-referral-invite-edit =
    <b>✉️ Invitation Message Settings</b>

    ℹ️ Available variables:
    <blockquote>
    • <code>{"{url}"}</code> - referral link
    • <code>{"{space}"}</code> - empty line at the beginning (not visible in preview)
    </blockquote>

    <i>✏️ Enter your invitation:</i>

msg-referral-invite-preview =

    { $preview_message }

# Plans
msg-plans-main = <b>📦 Plans</b>

msg-plan-configurator =
    <b>📦 Plan Configurator</b>

    <blockquote>
    • <b>Name</b>: { $name }
    • <b>Tag</b>: { $tag }
    • <b>Internal squad</b>: { $internal_squads }
    • <b>External squad</b>: { $external_squad }
    • <b>Access</b>: { availability-type }
    </blockquote>
    
    <blockquote>
    • <b>Type</b>: { plan-type }
    • <b>Traffic limit</b>: { $is_unlimited_traffic ->
        [1] { unlimited }
        *[0] { $traffic_limit }
    }
    • <b>Device limit</b>: { $is_unlimited_devices ->
        [1] { unlimited }
        *[0] { $device_limit }
    }
    </blockquote>
    
    <blockquote>
    • <b>Status</b>: { $is_active ->
        [1] 🟢 Enabled
        *[0] 🔴 Disabled
    }
    </blockquote>

    Select item to change.

msg-plan-name =
    <b>🏷️ Change Name</b>

    { $name ->
    [0] { space }
    *[HAS]
    <blockquote>
    { $name }
    </blockquote>
    }

    Enter new plan name.

msg-plan-description =
    <b>💬 Change Description</b>

    <blockquote>
    Description: { $description }
    </blockquote>

    Enter new plan description.

msg-plan-tag =
    <b>📌 Change Tag</b>

    <blockquote>
    Tag: { $tag }
    </blockquote>

    <i>ℹ️ Use uppercase Latin letters, numbers and underscore.</i>

    ✏️ Enter tag for the plan:

msg-plan-type =
    <b>🔖 Change Type</b>

    Select new plan type.

msg-plan-availability =
    <b>✴️ Change Availability</b>

    Select plan availability.

msg-plan-traffic =
    <b>🌐 Change Traffic Limit and Reset Strategy</b>

    Enter new plan traffic limit (in GB) and select reset strategy.

msg-plan-devices =
    <b>📱 Change Device Limit</b>

    Enter new plan device limit.

msg-plan-durations =
    <b>⏳ Plan Durations</b>

    Select duration to change price.

msg-plan-duration =
    <b>⏳ Add Plan Duration</b>

    Enter new duration (in days).

msg-plan-prices =
    <b>💰 Change Tariff Price for ({ $value ->
            [-1] { unlimited }
            *[other] { unit-day }
        })</b>

    Specify price in rubles.
    Prices in other currencies will be calculated automatically based on exchange rate.

msg-plan-price =
    <b>💰 Change Price for Tariff ({ $value ->
            [-1] { unlimited }
            *[other] { unit-day }
        })</b>

    Enter new price in rubles (₽).

msg-plan-allowed-users = 
    <b>👥 Change Allowed Users List</b>

    Enter user ID to add to the list.

msg-plan-squads =
    <b>🔗 Squads</b>

    <blockquote>
    • <b>Internal</b>: { $internal_squads ->
    [0] { lbl-not-set }
    *[HAS] { $internal_squads }
    }
    • <b>External</b>: { $external_squad ->
    [0] { lbl-not-set }
    *[HAS] { $external_squad }
    }
    </blockquote>

    ✏️ Select required squads:

msg-plan-internal-squads =
    <b>⏺️ Change Internal Squads List</b>

    Select which internal groups will be assigned to this plan.

msg-plan-external-squads =
    <b>⏹️ Change External Squad</b>

    Select which external group will be assigned to this plan.


# Notifications
msg-notifications-main = <b>🔔 Notification Settings</b>
msg-notifications-user = <b>👥 User Notifications</b>
msg-notifications-system = <b>⚙️ System Notifications</b>


# Subscription
msg-subscription-key-title = 
    🔑 <b>Ihr Abonnementschlüssel:</b>

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
    [1] <i>📢 A free referral subscription is available for you.</i>
    *[0] {""}
    }
    *[0]
    <i>🎁 A free trial subscription is available for you.</i>
    }
    *[0]
    <b>💳 Subscription Management:</b>
    }
msg-subscription-plans =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription-conditional }

    <b>📦 Tarifplan-Auswahl:</b>
msg-subscription-new-success = ✅ <i>Tarifplan { $plan_name } wurde aktiviert.</i>
msg-subscription-renew-success = ✅ <i>Ihr Abonnement wurde um { $added_duration } verlängert.</i>

msg-subscription-details =
    <b>💳 Zu kaufendes Abonnement:</b>
    <blockquote>
    • <b>Tarif:</b> { $plan_name }
    • <b>Datenvolumen-Limit</b>: { $traffic }
    { $devices ->
    [0] { empty }
    *[HAS] • <b>Geräte-Limit</b>: { $devices }
    }{ $has_planned_extra_devices ->
        [1] {""}
    • <b>Zusätzliche Geräte:</b> { $planned_extra_devices }
        *[0] {""}
    }
    { $period ->
    [0] { empty }
    *[HAS] • <b>Dauer</b>: { $period }
    }
    { $final_amount ->
    [0] { empty }
    *[HAS] • <b>Preis</b>: { frg-payment-amount }
    }
    </blockquote>

msg-subscription-duration =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription-conditional }

    <b>💳 Zu kaufendes Abonnement:</b>
    <blockquote>
    • <b>Tarif:</b> { $plan_name }
    • <b>Datenvolumen-Limit</b>: { $traffic }
    • <b>Geräte-Limit</b>: { $devices }
    </blockquote>
    { $description ->
    [0] {""}
    *[HAS] {""}
    
    ℹ️ <b>Detaillierte Beschreibung:</b>
    <blockquote>
    { $description }
    </blockquote>
    }

    <b>⏳ Wählen Sie die Dauer:</b>

msg-subscription-payment-method =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription-conditional }

    <b>💳 Zu kaufendes Abonnement:</b>
    <blockquote>
    • <b>Tarif:</b> { $plan_name }
    • <b>Datenvolumen-Limit</b>: { $traffic }
    • <b>Geräte-Limit</b>: { $device_limit }
    • <b>Dauer:</b> { $period }
    </blockquote>

    { $description ->
    [0] {""}
    *[HAS] {""}
    ℹ️ <b>Detaillierte Beschreibung:</b>
    <blockquote>
    { $description }
    </blockquote>

    }

    <b>💳 Zahlungsmethode wählen</b>

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

    <b>📋 Gesamt:</b>
    <blockquote>
    • <b>Zahlungsmethode:</b> Vom Guthaben
    { $purchase_type ->
        [RENEW] { $has_extra_devices_cost ->
            [1] • <b>Abonnement:</b> { $original_amount }
    • <b>Zusätzliche Geräte:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/Mon)
            *[0] • <b>Abonnement:</b> { $original_amount }
        }
        [CHANGE] { $has_extra_devices_cost ->
            [1] • <b>Abonnement:</b> { $original_amount }
    • <b>Zusätzliche Geräte:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/Mon)
            *[0] • <b>Abonnement:</b> { $original_amount }
        }
        *[OTHER] • <b>Abonnement:</b> { $original_amount }
    }
    • <b>Zu zahlender Betrag:</b> { $total_payment }
    </blockquote>

    { $has_extra_devices_cost ->
    }
    { $purchase_type ->
        [CHANGE] 
    ⚠️ <i>Das aktuelle Abonnement wird ohne Neuberechnung der verbleibenden Zeit ersetzt.</i>
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

    <b>📋 Gesamt:</b>
    <blockquote>
    • <b>Zahlungsmethode:</b> Bankkarte
    { $purchase_type ->
        [RENEW] { $has_extra_devices_cost ->
            [1] • <b>Abonnement:</b> { $original_amount }
    • <b>Zusätzliche Geräte:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/Mon)
            *[0] • <b>Abonnement:</b> { $original_amount }
        }
        [CHANGE] { $has_extra_devices_cost ->
            [1] • <b>Abonnement:</b> { $original_amount }
    • <b>Zusätzliche Geräte:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/Mon)
            *[0] • <b>Abonnement:</b> { $original_amount }
        }
        *[OTHER] • <b>Abonnement:</b> { $original_amount }
    }
    • <b>Zu zahlender Betrag:</b> { $total_payment }
    </blockquote>

    { $has_extra_devices_cost ->
    }
    { $purchase_type ->
        [CHANGE] 
    ⚠️ <i>Das aktuelle Abonnement wird ohne Neuberechnung der verbleibenden Zeit ersetzt.</i>
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

    <b>📋 Gesamt:</b>
    <blockquote>
    • <b>Zahlungsmethode:</b> Bankkarte
    { $purchase_type ->
        [RENEW] { $has_extra_devices_cost ->
            [1] • <b>Abonnement:</b> { $original_amount }
    • <b>Zusätzliche Geräte:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/Mon)
            *[0] • <b>Abonnement:</b> { $original_amount }
        }
        [CHANGE] { $has_extra_devices_cost ->
            [1] • <b>Abonnement:</b> { $original_amount }
    • <b>Zusätzliche Geräte:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/Mon)
            *[0] • <b>Abonnement:</b> { $original_amount }
        }
        *[OTHER] • <b>Abonnement:</b> { $original_amount }
    }
    • <b>Zu zahlender Betrag:</b> { $total_payment }
    </blockquote>

    { $has_extra_devices_cost ->

    { $purchase_type ->
        [CHANGE] 
    ⚠️ <i>Das aktuelle Abonnement wird ohne Neuberechnung der verbleibenden Zeit ersetzt.</i>
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

    <b>📋 Gesamt:</b>
    <blockquote>
    • <b>Zahlungsmethode:</b> { gateway-type }
    { $purchase_type ->
        [RENEW] { $has_extra_devices_cost ->
            [1] • <b>Abonnement:</b> { $original_amount }
    • <b>Zusätzliche Geräte:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/Mon)
            *[0] • <b>Abonnement:</b> { $original_amount }
        }
        [CHANGE] { $has_extra_devices_cost ->
            [1] • <b>Abonnement:</b> { $original_amount }
    • <b>Zusätzliche Geräte:</b> { $extra_devices_cost } ({ $extra_devices_monthly_cost }/Mon)
            *[0] • <b>Abonnement:</b> { $original_amount }
        }
        *[OTHER] • <b>Abonnement:</b> { $original_amount }
    }
    • <b>Zu zahlender Betrag:</b> { $total_payment }
    </blockquote>

    { $has_extra_devices_cost ->
    }
    { $purchase_type ->
        [CHANGE] 
    ⚠️ <i>Das aktuelle Abonnement wird ohne Neuberechnung der verbleibenden Zeit ersetzt.</i>
        *[OTHER] {""}
    }

msg-subscription-trial =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    <b>✅ Trial subscription successfully received!</b>

msg-subscription-referral-code =
    <b>📢 Referral Subscription</b>

    Enter the referral code of the user who invited you:

msg-subscription-referral-success =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    <b>🎉 Subscription successfully upgraded to Referral!</b>

msg-subscription-promocode =
    <b>🎟 Enter Promo Code</b>

    Send the promo code to activate bonuses or discounts.
    You can also enter another user's <b>referral code</b> to link to them.

msg-subscription-success =
    { hdr-user-profile }
    { frg-user }

    { hdr-subscription }
    { frg-subscription }

    { $purchase_type ->
    [ADD_DEVICE] ✅<i>{ $device_count } { $device_count ->
        [1] Gerät
        *[other] Geräte
    } zu Ihrem Abonnement hinzugefügt!</i>
    [NEW] { msg-subscription-new-success }
    [RENEW] { msg-subscription-renew-success }
    [CHANGE] { msg-subscription-change-success }
    *[OTHER] {""}
    }

msg-subscription-new-success = ✅ <i>Der Tarif { $plan_name } wurde aktiviert.</i>
msg-subscription-renew-success = ✅ <i>Ihr Abonnement wurde um { $added_duration } verlängert.</i>
msg-subscription-change-success = ✅<i>Ihr Abonnement wurde geändert.</i>

msg-subscription-failed = 
    <b>❌ An error occurred!</b>

    Don't worry, support has been notified and will contact you soon. We apologize for the inconvenience.


# Importer
msg-importer-main =
    <b>📥 User Import</b>

    Starting synchronization: checking all users in the Panel. If a user is not in the bot database, they will be created and receive a temporary subscription. If user data differs, it will be automatically updated.

msg-importer-from-xui =
    <b>📥 User Import (3X-UI)</b>
    
    { $has_exported -> 
    [1]
    <b>🔍 Found:</b>
    <blockquote>
    Total users: { $total }
    With active subscription: { $active }
    With expired subscription: { $expired }
    </blockquote>
    *[0]
    All active users with numeric email are imported.

    It is recommended to disable users who don't have a Telegram ID in the email field beforehand. The operation may take considerable time depending on the number of users.

    Send the database file (in .db format).
    }

msg-importer-squads =
    <b>🔗 Internal Squads List</b>

    Select which internal groups will be available to imported users.

msg-importer-import-completed =
    <b>📥 User Import Completed</b>
    
    <b>📃 Information:</b>
    <blockquote>
    • <b>Total users</b>: { $total_count }
    • <b>Successfully imported</b>: { $success_count }
    • <b>Failed to import</b>: { $failed_count }
    </blockquote>

msg-importer-sync-completed =
    <b>📥 User Synchronization Completed</b>

    <b>📃 Information:</b>
    <blockquote>
    Total users in panel: { $total_panel_users }
    Total users in bot: { $total_bot_users }

    New users: { $added_users }
    Subscriptions added: { $added_subscription }
    Subscriptions updated: { $updated}
    
    Users without Telegram ID: { $missing_telegram }
    Synchronization errors: { $errors }
    </blockquote>

msg-importer-sync-bot-to-panel-completed =
    <b>📤 Synchronization from Telegram to Panel Completed</b>

    <b>📃 Information:</b>
    <blockquote>
    Total users in bot: { $total_bot_users }

    Created in panel: { $created }
    Updated in panel: { $updated }
    Skipped (no subscription): { $skipped }
    Synchronization errors: { $errors }
    </blockquote>


# Promocodes
msg-promocodes-main = <b>🎟 Promo Codes</b>

    Create and manage promo codes for users.

msg-promocodes-search = <b>🔍 Promo Code Search</b>

    Enter promo code to search.

msg-promocodes-list = <b>📃 Promo Code List</b>

    { $count ->
        [0] No promo codes created.
        [1] Found { $count } promo code.
        *[other] Found { $count } promo codes.
    }

msg-promocode-view =
    <b>🎟 View Promo Code</b>

    <blockquote>
    • <b>Code</b>: <code>{ $code }</code>
    • <b>Type</b>: { promocode-type }
    • <b>Status</b>: { $is_active -> 
        [1] 🟢 Enabled
        *[0] 🔴 Disabled
        }
    </blockquote>

    <blockquote>
    { $promocode_type ->
    [DURATION] • <b>Bonus</b>: +{ $reward }
    [PERSONAL_DISCOUNT] • <b>Permanent discount</b>: { $reward }%
    [PURCHASE_DISCOUNT] • <b>One-time discount</b>: { $reward }%
    *[OTHER] • <b>Reward</b>: { $reward }
    }
    • <b>Validity</b>: { $lifetime }
    • <b>Used</b>: { $activations_count } / { $max_activations }
    </blockquote>

msg-promocode-configurator =
    <b>🎟 Create Promo Code</b>

    <blockquote>
    • <b>Name</b>: { $name }
    • <b>Code</b>: <code>{ $code }</code>
    • <b>Reward type</b>: { promocode-type }
    </blockquote>

    <blockquote>
    { $promocode_type ->
    [DURATION] • <b>Bonus</b>: +{ $reward }
    [PERSONAL_DISCOUNT] • <b>Permanent discount</b>: { $reward }%
    [PURCHASE_DISCOUNT] • <b>One-time discount</b>: { $reward }%
    *[OTHER] • <b>Reward</b>: { $reward }
    }
    • <b>Validity</b>: { $lifetime }
    • <b>Activation limit</b>: { $max_activations }
    </blockquote>

    Select item to change.

msg-promocode-name = <b>📝 Promo Code Name</b>

    Enter promo code name (1-50 characters).

msg-promocode-code = <b>🏷️ Promo Code</b>

    Enter promo code (3-20 characters) or press button to generate random code.

msg-promocode-type = <b>🔖 Select Promo Code Type:</b>

    <blockquote>
    • <b>One-time discount</b> - discount will expire after first purchase, or when promo code validity ends.

    • <b>Permanent discount</b> - permanent discount for the user.

    • <b>Days to subscription</b> - Adding days to user's subscription.
    </blockquote>

msg-promocode-reward = <b>🎁 Reward</b>

    <b>Reward type</b>: { promocode-type }

    { $promocode_type ->
    [DURATION] Enter <b>number of days</b> for subscription bonus.
    [PERSONAL_DISCOUNT] Enter <b>discount percentage</b> (1-100) for permanent discount.
    [PURCHASE_DISCOUNT] Enter <b>discount percentage</b> (1-100) for purchase discount.
    *[OTHER] Enter reward value.
    }

msg-promocode-lifetime = <b>⌛ Validity Period</b>

    Select promo code validity period in days.

msg-promocode-lifetime-input = ⌛️Enter promo code validity period in days.

msg-promocode-quantity = <b>🔢 Activation Count</b>

    Select maximum promo code activation count.

msg-promocode-quantity-input = 🔢 Enter promo code activation count.
msg-promocode-access = <b>📦 Plan Access</b>

# Bonus Activation
msg-bonus-activate =
    <b>💎 Bonus Activation</b>

    Available bonuses: <b>{ $referral_balance }</b>
    Selected amount: <b>{ $current_bonus_amount } ₽</b>

msg-bonus-activate-custom =
    <b>💎 Bonus Activation</b>

    Available bonuses: <b>{ $referral_balance }</b>

    Enter amount to activate (from 1 to { $referral_balance }):

# Terms of Service Settings
msg-dashboard-settings-tos =
    <b>📋 User Agreement</b>
    
    <blockquote>
    • Status: { $status }
    • Source: { $source }
    </blockquote>

    🔽 Specify link to the rules document.

msg-dashboard-settings-tos-url =
    <b>🔗 Agreement Link</b>

    <blockquote>
    Enter the link (in format https://telegram.org/tos).
    </blockquote>

# Community Settings
msg-dashboard-settings-community =
    <b>👥 Community</b>
    
    <blockquote>
    • Status: { $status }
    • Telegram group: { $url_display }
    </blockquote>

    🔽 Specify link to Telegram group.

msg-dashboard-settings-community-url =
    <b>🔗 Telegram Group Link</b>

    <blockquote>
    Enter the link (in format https://t.me/+code or https://t.me/group_name).
    </blockquote>

# Finances Settings
msg-dashboard-settings-finances =
    <b>💰 Finances</b>
    
    <blockquote>
    • <b>Default currency:</b> { $default_currency } ({ $default_currency_name })
    </blockquote>

    <i>ℹ️ When sync is enabled, exchange rates are automatically synchronized with the Central Bank of Russia rate.</i>

# Currency Rates Settings
msg-dashboard-settings-currency-rates =
    <b>💱 Exchange Rates</b>

    Specify exchange rate relative to ruble.
    Plan prices will be automatically recalculated.

msg-dashboard-settings-currency-rate-input =
    <b>💱 { $currency } Rate</b>

    Enter { $symbol } to ruble rate (e.g.: 90.5).
    1 { $symbol } = X ₽

# Payment Link for Extra Devices
msg-add-device-payment-link = <b>💳 Zahlungslink</b>

Klicken Sie auf die Schaltfläche unten, um zur Zahlung für zusätzliche Geräte zu gelangen.

# Device Deletion Warning
msg-device-deletion-warning = ⚠️ Drücken Sie die Löschtaste erneut zur Bestätigung.
    Das Gerät funktioniert bis zum Ende des bezahlten Zeitraums.
msg-extra-device-deletion-confirm = ⚠️ Zusätzliche Geräte werden am { $expires_date } entfernt.
    Sie funktionieren bis zum Ende des bezahlten Zeitraums und werden bei der Abonnementverlängerung nicht berücksichtigt.
    Drücken Sie die Löschtaste erneut zur Bestätigung.g.
    Das Gerät funktioniert bis zum Ende des bezahlten Zeitraums.
