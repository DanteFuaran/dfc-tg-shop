# Errors
ntf-error-lost-context = <i>⚠️ An error occurred. Dialog restarted.</i>
ntf-error-log-not-found = <i>⚠️ Error: Log file not found.</i>

# Database Export
ntf-db-export-start = <i>💾 Starting database export...</i>
ntf-db-export-success = 
    <i>✅ Database saved successfully!</i>
    
    <b>Path:</b> <code>{ $path }</code>
    
    <i>The file can be opened in DB Browser (SQLite)</i>
ntf-db-export-error = 
    <i>❌ Error exporting database:</i>
    
    <blockquote>{ $error }</blockquote>
ntf-db-save-success = <i>✅ Database backup saved successfully!</i>
ntf-db-save-failed = <i>❌ Error saving database backup.</i>
ntf-db-convert-success = <i>✅ File was converted!</i>
ntf-db-convert-in-progress = ⚠️ Converting to SQL...
ntf-db-convert-in-progress = <i>⚠️ Converting to SQL</i>
ntf-db-restore-success =
    <i>✅ Database successfully restored from uploaded dump.</i>

ntf-db-restore-failed =
    <i>❌ Error restoring database.</i>

ntf-db-sync-completed = <i>✅ Database restore completed!</i>
ntf-db-sync-title = ✅ <b>Restore completed!</b>
ntf-db-sync-skipped-title = <b>⊘ Skipped users without subscriptions:</b>
ntf-db-sync-errors-title = <b>❌ Sync errors:</b>
ntf-db-sync-stats-title = <b>📊 Summary:</b>
ntf-db-sync-stats-total = Total in bot: { $total }
ntf-db-sync-stats-created = Created: { $created }
ntf-db-sync-stats-updated = Updated: { $updated }
ntf-db-sync-stats-skipped = Skipped: { $skipped }
ntf-db-sync-stats-errors = Errors: { $errors }
ntf-db-sync-error = ❌ Sync error: { $error }
ntf-db-import-started = <i>⚠️ Database import in progress. Please wait...</i>
ntf-db-import-failed = <i>❌ Error importing database.</i>
ntf-db-restore-preparing = <i>🔄 Preparing for data restore...</i>

# Database Clear
ntf-db-clear-all-warning = 
    <b>⚠️ Press again to confirm action.</b>

ntf-db-clear-all-start = <i>🗑 Performing full database cleanup...</i>
ntf-db-clear-all-success = 
    <b>✅ Deletion completed!</b>
    
    <blockquote>
    📊 Records deleted:
    • Users: <b>{ $users }</b>
    • Extra device purchases: <b>{ $extra_device_purchases }</b>
    • Referrals: <b>{ $referrals }</b>
    • Pricing plans: <b>{ $plans }</b>
    • Promo codes: <b>{ $promocodes }</b>
    </blockquote>
ntf-db-clear-all-failed = 
    <i>❌ Error clearing database:</i>
    
    <blockquote>{ $error }</blockquote>

ntf-db-clear-users-warning = 
    <b>⚠️ Press again to confirm action.</b>

ntf-db-clear-users-start = <i>🗑 Deleting users...</i>
ntf-db-clear-users-success = 
    <b>✅ Deletion completed!</b>
    
    <blockquote>
    📊 Total:
    • Deleted: <b>{ $users }</b>
    • Skipped: <b>0</b>
    • Errors: <b>0</b>
    </blockquote>
ntf-db-clear-users-failed = 
    <i>❌ Error deleting users:</i>
    
    <blockquote>{ $error }</blockquote>

# Existing subscription import notifications
ntf-existing-subscription-found =
    <i>✅ Existing subscription found!</i>
    
    <blockquote>
    You already have a subscription in the control panel.
    It has been successfully linked to your account.
    
    • <b>Plan:</b> { $plan_name }
    • <b>Tag:</b> { $tag }
    </blockquote>
    
ntf-existing-subscription-no-plan =
    <i>⚠️ Existing subscription found!</i>
    
    <blockquote>
    You already have a subscription in the control panel.
    However, the corresponding plan was not found in the bot.
    
    • <b>Current tag:</b> { $old_tag }
    • <b>New tag:</b> IMPORT
    
    Contact the administrator to configure your subscription.
    </blockquote>

# Sync notifications
ntf-sync-preparing = <i>🔄 Preparing data for import...</i>
ntf-sync-started = <i>🔄 Synchronizing data. Please wait...</i>
ntf-sync-completed =
    <i>✅ Synchronization completed!</i>
    
    <blockquote>
    Direction: <b>{ $direction ->
        [bot_to_panel] Bot → Panel
        *[panel_to_bot] Panel → Bot
    }</b>
    Synchronized: <b>{ $synced }</b>
    Created: <b>{ $created }</b>
    Errors: <b>{ $errors }</b>
    </blockquote>
ntf-sync-failed =
    <i>❌ Synchronization error:</i>
    
    <blockquote>{ $error }</blockquote>

# Balance transfer notifications
ntf-balance-transfer-received =
    <i>💸 You received a transfer!</i>
    
    <b>📋 Transfer details:</b>
    <blockquote>• Sender: <b>{ $sender }</b>
    • Amount: <b>{ $amount } ₽</b>
    • Commission: Paid by sender{ $has_message ->
        [0] {""}
       *[1] {""}
    </blockquote>
    <b>💬 Message:</b>
    <blockquote>• <i>{ $message }</i>
    }
    </blockquote>
ntf-balance-transfer-insufficient = <i>⚠️ Insufficient funds! Required: { $required }, balance: { $balance }</i>
ntf-balance-transfer-invalid-id = <i>⚠️ Telegram ID must contain only digits!</i>
ntf-balance-transfer-user-not-found = <i>⚠️ User not found!</i>
ntf-balance-transfer-self = <i>⚠️ You cannot transfer funds to yourself!</i>
ntf-balance-transfer-disabled = <i>⚠️ Transfer feature is disabled!</i>
ntf-balance-transfer-amount-range = <i>⚠️ Transfer amount must be between { $min } and { $max } ₽</i>
ntf-balance-transfer-incomplete = <i>⚠️ You need to specify recipient and transfer amount!</i>
ntf-balance-transfer-success =
    <i>✅ Transfer completed!</i>
    
    <b>📋 Transfer details:</b>
    <blockquote>• Recipient: <b>{ $recipient }</b>
    • Amount: <b>{ $amount } ₽</b>
    • Commission: <b>{ $commission } ₽</b>{ $has_message ->
        [0] {""}
       *[1] {""}
    </blockquote>
    <b>💬 Message:</b>
    <blockquote>• <i>{ $message }</i>
    }
    </blockquote>
ntf-balance-transfer-error = <i>⚠️ Error processing transfer!</i>

ntf-balance-invalid-amount = 
    <i>⚠️ Top-up amount available from { $min_amount } to { $max_amount } ₽.</i>
ntf-bonus-insufficient = <i>⚠️ Insufficient bonuses!</i>
ntf-bonus-activated = <i>✅ { $amount } ₽ credited to balance!</i>
ntf-balance-withdraw-in-development = 🚧 Automatic withdrawal feature is under development. To withdraw funds, contact support.
ntf-invite-link-copied = <i>⚠️ Link copied to clipboard.</i>


# Events
ntf-event-error =
    🤖 <b>System: An error occurred!</b>
    
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
    🤖 <b>System: Error connecting to Remnawave!</b>

    <blockquote>
    Without an active connection, the bot cannot work properly!
    </blockquote>

    { hdr-error }
    <blockquote>
    { $error }
    </blockquote>

ntf-event-error-webhook =
    🤖 <b>System: Webhook error detected!</b>

    { hdr-error }
    <blockquote>
    { $error }
    </blockquote>

ntf-event-bot-startup =
    🤖 <b>System: Bot started!</b>

    <blockquote>
    • <b>Access mode</b>: { access-mode }
    • <b>Purchases</b>: { $purchases_allowed ->
    [0] disabled
    *[1] enabled
    }.
    • <b>Registration</b>: { $registration_allowed ->
    [0] disabled
    *[1] enabled
    }.
    </blockquote>

ntf-event-bot-shutdown =
    🤖 <b>System: Bot stopped!</b>

ntf-event-bot-started =
    🤖 <b>System: Bot enabled!</b>

ntf-event-bot-update =
    🤖 <b>System: DFC Shop update detected!</b>

    <blockquote>
    • <b>Current version</b>: { $local_version }
    • <b>Available version</b>: { $remote_version }
    </blockquote>

ntf-event-new-user =
    🤖 <b>System: New user!</b>

    { hdr-user }
    { frg-user-info }

    { $has_referrer ->
    [0] { empty }
    *[HAS]
    <b>🤝 Referrer:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $referrer_user_id }</code>
    • <b>Name</b>: { $referrer_user_name } { $referrer_username -> 
        [0] { empty }
        *[HAS] (<a href="tg://user?id={ $referrer_user_id }">@{ $referrer_username }</a>)
    }
    </blockquote>
    }

ntf-event-referral-upgrade =
    🤖 <b>System: Subscription upgraded to referral!</b>

    { hdr-user }
    { frg-user-info }

    <b>🤝 Referrer:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $referrer_user_id }</code>
    • <b>Name</b>: { $referrer_user_name } { $referrer_username -> 
        [0] { empty }
        *[HAS] (<a href="tg://user?id={ $referrer_user_id }">@{ $referrer_username }</a>)
    }
    </blockquote>

ntf-event-promocode-activated =
    🤖 <b>System: Promo code activated!</b>

    { hdr-user }
    { frg-user-info }

    <b>🎟️ Promo code:</b>
    <blockquote>
    • <b>Code</b>: <code>{ $promocode_code }</code>
    • <b>Reward</b>: { $promocode_reward_type ->
        [PURCHASE_DISCOUNT] { $promocode_reward }% purchase discount
        [PERSONAL_DISCOUNT] { $promocode_reward }% permanent discount
        [DURATION] +{ $promocode_reward } days to subscription
        *[OTHER] { $promocode_reward } { $promocode_reward_type }
    }
    </blockquote>

ntf-event-test-webhook-success =
    🤖 <b>System: Test webhook successful!</b>

    <b>💳 Payment Gateway:</b>
    <blockquote>
    • <b>Name</b>: { $gateway_name }
    • <b>Type</b>: <code>{ $gateway_type }</code>
    </blockquote>

    <i>Test notification received and processed successfully.</i>

ntf-event-test-webhook-failed =
    🤖 <b>System: Test webhook error!</b>

    <b>💳 Payment Gateway:</b>
    <blockquote>
    • <b>Type</b>: <code>{ $gateway_type }</code>
    </blockquote>

    <b>⚠️ Error:</b>
    <blockquote>
    • <b>Type</b>: <code>{ $error_type }</code>
    • <b>Message</b>: { $error_message }
    </blockquote>
    
ntf-event-subscription-trial =
    🤖 <b>System: Trial subscription received!</b>

    { hdr-user }
    { frg-user-info }
    
    { hdr-plan }
    { frg-plan-snapshot }

ntf-event-subscription-new =
    🤖 <b>System: Subscription purchased!</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot }

ntf-event-subscription-renew =
    🤖 <b>System: Subscription renewed!</b>
    
    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot }

    { $has_extra_devices ->
        [1] 

    <b>📱 Extra Devices:</b>
    <blockquote>
    • <b>Count</b>: { $extra_devices_count }
    • <b>Price</b>: { $extra_devices_cost }
    </blockquote>
        *[0] {""}
    }

ntf-event-subscription-change =
    🤖 <b>System: Subscription changed!</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot-comparison }

ntf-event-balance-topup =
    🤖 <b>System: Balance topped up!</b>

    <blockquote>
    • <b>ID</b>: <code>{ $payment_id }</code>
    • <b>Payment method</b>: { gateway-type }
    • <b>Amount</b>: { $final_amount }
    </blockquote>

    { hdr-user }
    { frg-user-info }

ntf-event-extra-devices =
    🤖 <b>System: Extra devices purchased!</b>

    <blockquote>
    • <b>ID</b>: <code>{ $payment_id }</code>
    • <b>Payment method</b>: { gateway-type }
    • <b>Amount</b>: { $final_amount }
    • <b>Discount</b>: { $discount_percent }%
    • <b>Devices</b>: +{ $device_count } pcs.
    </blockquote>

    { hdr-subscription }
    { frg-subscription-details }

    { hdr-user }
    { frg-user-info }

ntf-event-extra-devices-balance =
    🤖 <b>System: Extra devices purchased!</b>

    <blockquote>
    • <b>Payment method</b>: 💰 From Balance
    • <b>Amount</b>: { $price } ₽
    • <b>Discount</b>: { $discount_percent }%
    • <b>Devices</b>: +{ $device_count } pcs.
    </blockquote>

    { hdr-user }
    { frg-user-info }

ntf-event-extra-devices-deletion =
    🤖 <b>System: Extra Devices Deletion!</b>

    { hdr-user }
    { frg-user-info }

    <blockquote>
    • <b>Devices</b>: -{ $device_count } pcs.
    • <b>Delete after</b>: { $delete_after }
    </blockquote>

ntf-event-balance-transfer =
    🤖 <b>System: Financial transfer!</b>

    <b>👤 Sender:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $sender_id }</code>
    • <b>Name</b>: { $sender_name }
    • <b>Balance after</b>: { $sender_balance } ₽
    </blockquote>

    <b>👤 Recipient:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $recipient_id }</code>
    • <b>Name</b>: { $recipient_name }
    • <b>Balance after</b>: { $recipient_balance } ₽
    </blockquote>

    <b>💰 Transfer details:</b>
    <blockquote>
    • <b>Amount</b>: { $amount } ₽
    • <b>Commission</b>: { $commission } ₽
    • <b>Total deducted</b>: { $total } ₽{ $has_message ->
        [0] {""}
       *[1] {""}
    • <b>Message</b>: <i>{ $message }</i>
    }
    </blockquote>

ntf-event-node-connection-lost =
    🤖 <b>System: Node connection lost!</b>

    { hdr-node }
    { frg-node-info }

ntf-event-node-connection-restored =
    🤖 <b>System: Node connection restored!</b>

    { hdr-node }
    { frg-node-info }

ntf-event-node-traffic =
    🤖 <b>System: Node reached traffic limit threshold!</b>

    { hdr-node }
    { frg-node-info }

ntf-event-user-first-connected =
    🤖 <b>System: User first connection!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-subscription }
    { frg-subscription-details }

ntf-event-user-not-connected =
    🤖 <b>System: User not connected!</b>

    <blockquote>
    User registered { $hours } h. ago but hasn't subscribed.
    They might need help.
    </blockquote>

    { hdr-user }
    { frg-user-info }
    
    <b>📅 Registration date:</b> { $registered_at }

ntf-event-user-expiring =
    { $is_trial ->
    [0]
    <b>⚠️ Attention! Your subscription expires in { unit-day }.</b>
    
    Renew it in advance to avoid losing access to the service! 
    *[1]
    <b>⚠️ Attention! Your free trial expires in { unit-day }.</b>

    Subscribe to avoid losing access to the service! 
    }

ntf-event-user-expired =
    <b>⛔ Attention! Access suspended.</b>

    { $is_trial ->
    [0] Your subscription has expired, renew it to continue using the service!
    *[1] Your free trial period has ended. Subscribe to continue using the service!
    }
    
ntf-event-user-expired-ago =
    <b>⛔ Attention! Access suspended.</b>

    { $is_trial ->
    [0] Your subscription expired { unit-day } ago, renew it to continue using the service!
    *[1] Your free trial period ended { unit-day } ago. Subscribe to continue using the service!
    }

ntf-event-user-limited =
    <b>⛔ Attention! Access suspended - VPN not working.</b>

    Your traffic is exhausted. { $is_trial ->
    [0] { $traffic_strategy ->
        [NO_RESET] Renew your subscription to reset traffic and continue using the service!
        *[RESET] Traffic will be restored in { $reset_time }. You can also renew your subscription to reset traffic.
        }
    *[1] { $traffic_strategy ->
        [NO_RESET] Subscribe to continue using the service!
        *[RESET] Traffic will be restored in { $reset_time }. You can also subscribe to use the service without restrictions.
        }
    }

ntf-event-user-hwid-added =
    🤖 <b>System: User added new device!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-hwid }
    { frg-user-hwid }

ntf-event-user-hwid-deleted =
    🤖 <b>System: User deleted device!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-hwid }
    { frg-user-hwid }

ntf-event-user-referral-attached =
    <b>🎉 You invited a friend!</b>
    
    <blockquote>
    User <b>{ $name }</b> joined using your invite link! To receive a reward, make sure they purchase a subscription.
    </blockquote>

ntf-event-user-referral-reward =
    <b>💰 You received a reward!</b>
    
    <blockquote>
    User <b>{ $name }</b> made a payment. You received <b>{ $value }{ $reward_type ->
        [MONEY] { space }{ $currency }
        [EXTRA_DAYS] { space }extra { $value ->
            [one] day
            *[other] days
            }
        *[OTHER] { $currency }
    }</b> to your referral balance!
    </blockquote>

ntf-event-user-referral-reward-error =
    <b>❌ Failed to issue reward!</b>
    
    <blockquote>
    User <b>{ $name }</b> made a payment, but we couldn't credit your reward because <b>you don't have a purchased subscription</b> to add {$value} { $value ->
            [one] extra day
            *[other] extra days
        } to.
    
    <i>Purchase a subscription to receive bonuses for invited friends!</i>
    </blockquote>


ntf-cashback-reward =
    <b>🎉 Congratulations! You receive cashback!</b>

    <blockquote>
    Since you participate in the referral program, you receive an additional bonus to your payment: <b>{ $value }{ $reward_type ->
        [MONEY] { space }{ $currency }
        [EXTRA_DAYS] { space }extra { $value ->
            [one] day
            *[other] days
            }
        *[OTHER] { $currency }
    }</b>!
    </blockquote>

# Notifications
ntf-command-paysupport = 💸 <b>To request a refund, contact our support team.</b>
ntf-command-help = 🆘 <b>Click the button below to contact support. We will help solve your problem.</b>
ntf-channel-join-required = ❇️ Subscribe to our channel and get <b>free days, promotions, and news</b>! After subscribing, click "Confirm".
ntf-channel-join-required-left = ⚠️ You unsubscribed from our channel! Subscribe to be able to use the bot.
ntf-rules-accept-required = ⚠️ <b>Before using the service, please read and accept the <a href="{ $url }">Terms of Service</a>.</b>

ntf-double-click-confirm = <i>⚠️ Press again to confirm action.</i>
ntf-user-referral-bind-not-found = <i>⚠️ User not found.</i>
ntf-user-referral-bind-self = <i>⚠️ Cannot bind a user to themselves.</i>
ntf-user-referral-bind-already = <i>⚠️ This user is already a referral of another user.</i>
ntf-user-referral-bind-success = <i>✅ Referral successfully bound.</i>
ntf-user-deleted = <i>✅ User deleted.</i>
ntf-channel-join-error = <i>⚠️ We don't see your channel subscription. Make sure you subscribed and try again.</i>
ntf-throttling-many-requests = <i>⚠️ You're sending too many requests, please wait a moment.</i>
ntf-squads-empty = <i>⚠️ Squads not found. Check their availability in the panel.</i>
ntf-invite-withdraw-points-error = ❌ You don't have enough points to perform the exchange.
ntf-invite-withdraw-no-balance = ❌ You have no bonuses to transfer to balance.
ntf-invite-withdraw-success = ✅ { $amount } ₽ successfully transferred to your main balance!

ntf-connect-not-available =
    ⚠️ { $status ->
    [LIMITED]
    You have used all available traffic. { $is_trial ->
    [0] { $traffic_strategy ->
        [NO_RESET] Renew your subscription to reset traffic and continue using the service!
        *[RESET] Traffic will be restored in { $reset_time }. You can also renew your subscription to reset traffic.
        }
    *[1] { $traffic_strategy ->
        [NO_RESET] Subscribe to continue using the service!
        *[RESET] Traffic will be restored in { $reset_time }. You can also subscribe to use the service without restrictions.
        }
    }
    [EXPIRED]  
    { $is_trial ->
    [0] Your subscription has expired. To continue using the service, renew your subscription or purchase a new one.
    *[1] Your free trial period has ended. Subscribe to continue using the service!
    }
    *[OTHER] An error occurred while checking status or your subscription was disabled. Contact support.
    }

ntf-user-not-found = <i>❌ User not found.</i>
ntf-user-transactions-empty = <i>❌ Transaction list is empty.</i>
ntf-user-subscription-empty = <i>❌ Current subscription not found.</i>
ntf-user-plans-empty = <i>❌ No available plans to grant.</i>
ntf-user-devices-empty = <i>❌ Device list is empty.</i>
ntf-user-invalid-number = <i>❌ Invalid number.</i>
ntf-user-device-limit-exceeded = <i>❌ Device count cannot exceed 100.</i>
ntf-user-allowed-plans-empty = <i>❌ No available plans to grant access.</i>
ntf-user-message-success = <i>✅ Message sent successfully.</i>
ntf-user-message-not-sent = <i>❌ Failed to send message.</i>
ntf-user-sync-already = <i>✅ Subscription data matches.</i>
ntf-user-sync-missing-data = <i>⚠️ Sync not possible. Subscription data missing from both panel and bot.</i>
ntf-user-sync-success = <i>✅ Subscription sync completed.</i>

ntf-user-invalid-expire-time = <i>❌ Cannot { $operation ->
    [ADD] extend subscription by the specified number of days
    *[SUB] reduce subscription by the specified number of days
    }.</i>

ntf-user-invalid-points = <i>❌ Cannot { $operation ->
    [ADD] add the specified amount of points
    *[SUB] deduct the specified amount of points
    }.</i>

ntf-user-invalid-balance = <i>❌ Cannot { $operation ->
    [ADD] add the specified amount to balance
    *[SUB] deduct the specified amount from balance
    }.</i>

ntf-referral-invalid-reward = <i>❌ Invalid value.</i>

ntf-access-denied = <i>🚧 Bot is in maintenance mode, try later.</i>
ntf-access-denied-registration = <i>❌ New user registration is disabled.</i>
ntf-access-denied-only-invited = <i>❌ New user registration is only available through invitation by another user.</i>
ntf-access-denied-purchasing = <i>🚧 Service payment is temporarily disabled. You will be notified when payments are available.</i>
ntf-payments-available-again = <i>✅ Service payment is available again! Thank you for waiting!</i>
ntf-access-allowed = <i>❇️ All bot functions are available again, thank you for waiting.</i>
ntf-access-id-saved = <i>✅ Channel/group ID updated successfully.</i>
ntf-access-link-saved = <i>✅ Channel/group link updated successfully.</i>
ntf-access-channel-invalid = <i>❌ Invalid link or channel/group ID.</i>

ntf-plan-invalid-name = <i>❌ Invalid name.</i>
ntf-plan-invalid-description = <i>❌ Invalid description.</i>
ntf-plan-invalid-tag = <i>❌ Invalid tag.</i>
ntf-plan-invalid-number = <i>❌ Invalid number.</i>
ntf-plan-trial-once-duration = <i>❌ Trial plan can only have one duration.</i>
ntf-plan-trial-already-exists = <i>❌ Trial plan already exists.</i>
ntf-plan-duration-already-exists = <i>❌ This duration already exists.</i>
ntf-plan-duration-last = <i>❌ Cannot delete the last duration.</i>
ntf-plan-save-error = <i>❌ Error saving plan.</i>
ntf-plan-name-already-exists = <i>❌ Plan with this name already exists.</i>
ntf-plan-invalid-user-id = <i>❌ Invalid user ID.</i>
ntf-plan-no-user-found = <i>❌ User not found.</i>
ntf-plan-user-already-allowed = <i>❌ User already added to allowed list.</i>
ntf-plan-confirm-delete = <i>⚠️ Press again to delete.</i>
ntf-plan-updated-success = <i>✅ Plan updated successfully.</i>
ntf-plan-created-success = <i>✅ Plan created successfully.</i>
ntf-plan-deleted-success = <i>✅ Plan deleted successfully.</i>
ntf-plan-tag-updated = <i>✅ Plan tag updated.</i>
ntf-plan-internal-squads-empty = <i>❌ Select at least one internal squad.</i>

ntf-gateway-not-configured = <i>❌ Payment gateway not configured.</i>
ntf-gateway-not-configurable = <i>❌ Payment gateway has no settings.</i>
ntf-gateway-field-wrong-value = <i>❌ Invalid value.</i>
ntf-gateway-test-payment-created = <i>✅ <a href="{ $url }">Test payment</a> created successfully.</i>
ntf-gateway-test-payment-error = <i>❌ Error creating test payment.</i>
ntf-gateway-test-payment-confirmed = <i>✅ Test payment processed successfully.</i>

ntf-subscription-plans-not-available = <i>❌ No available plans.</i>
ntf-subscription-gateways-not-available = <i>❌ No available payment systems.</i>
ntf-subscription-renew-plan-unavailable = <i>❌ Your plan is outdated and not available for renewal.</i>
ntf-subscription-change-plans-not-available = <i>❌ No available subscriptions to change. You already have the only available subscription activated.</i>
ntf-subscription-payment-creation-failed = <i>❌ Error creating payment, try later.</i>
ntf-payment-gateway-not-configured = <i>❌ Merchant data for { $gateway_name } is not configured</i>
ntf-subscription-insufficient-balance = <i>❌ Insufficient balance to pay for subscription.</i>
ntf-check-payment-pending = <i>⏳ Payment has not been received yet. If you have already paid, please wait a moment and try again.</i>
ntf-check-payment-no-id = <i>❌ Unable to find payment data. Please try creating a new payment.</i>
ntf-check-payment-not-found = <i>❌ Transaction not found. Please try creating a new payment.</i>

ntf-balance-payment-link = 
    <b>💳 Payment link</b>
    
    Follow the link to pay:
    <a href="{ $payment_url }">Pay</a>

ntf-balance-topup-success = 
    ✅ <b>Balance topped up successfully!</b>
    
    Credited to your balance: <b>{ $amount } { $currency }</b>

ntf-broadcast-list-empty = <i>❌ Broadcast list is empty.</i>
ntf-broadcast-audience-not-available = <i>❌ No users available for selected audience.</i>
ntf-broadcast-audience-not-active = <i>❌ No users with ACTIVE subscription for this plan.</i>
ntf-broadcast-plans-not-available = <i>❌ No available plans.</i>
ntf-broadcast-empty-content = <i>❌ Content is empty.</i>
ntf-broadcast-wrong-content = <i>❌ Invalid content.</i>
ntf-broadcast-content-saved = <i>✅ Message content saved successfully.</i>
ntf-broadcast-preview = { $content }
ntf-invite-preview = { $content }
ntf-broadcast-not-cancelable = <i>❌ Broadcast cannot be canceled.</i>
ntf-broadcast-canceled = <i>✅ Broadcast canceled successfully.</i>
ntf-broadcast-deleting = <i>⚠️ Deleting all sent messages.</i>
ntf-broadcast-already-deleted = <i>❌ Broadcast is being deleted or already deleted.</i>

ntf-broadcast-deleted-success =
    ✅ Broadcast <code>{ $task_id }</code> deleted successfully.

    <blockquote>
    • <b>Total messages</b>: { $total_count }
    • <b>Successfully deleted</b>: { $deleted_count }
    • <b>Failed to delete</b>: { $failed_count }
    </blockquote>

ntf-trial-unavailable = <i>❌ Trial subscription is temporarily unavailable.</i>
ntf-trial-already-used = <i>❌ You have already used the trial subscription.</i>
ntf-referral-code-invalid = <i>❌ Invalid referral code. Try again.</i>
ntf-referral-code-self = <i>❌ You cannot use your own referral code.</i>
ntf-referral-code-own-referral = <i>❌ You cannot use the referral code of a user you invited.</i>
ntf-referral-code-already-used = <i>❌ You already used a referral subscription.</i>
ntf-referral-code-already-has = <i>❌ You are already linked to a referrer. Re-linking is not possible.</i>
ntf-referral-code-success-promo = <i>✅ You have been successfully linked to a referrer!</i>

ntf-importer-not-file = <i>⚠️ Send the database as a file.</i>
ntf-importer-db-invalid = <i>❌ This file cannot be imported.</i>
ntf-importer-db-failed = <i>❌ Error importing database.</i>
ntf-importer-exported-users-empty =  <i>❌ User list in database is empty.</i>
ntf-importer-internal-squads-empty = <i>❌ Select at least one internal squad.</i>
ntf-importer-import-started = <i>✅ User import started, please wait...</i>
ntf-importer-sync-started = <i>🔄 Data synchronization in progress...</i>
ntf-importer-users-not-found = <i>❌ Failed to find users for synchronization.</i>
ntf-importer-not-support = <i>⚠️ Importing all data from 3xui-shop is temporarily unavailable. You can use import from 3X-UI panel!</i>
ntf-importer-sync-already-running = <i>⚠️ User synchronization already started, please wait...</i>

ntf-importer-sync-bot-to-panel-completed =
    <b>📤 Synchronization completed</b>

    <blockquote>
    <b>Total in bot:</b> { $total_bot_users }
    <b>Created:</b> { $created }
    <b>Updated:</b> { $updated }
    <b>Skipped:</b> { $skipped }
    <b>Errors:</b> { $errors }
    </blockquote>

ntf-sync-panel-to-bot-completed =
    <b>📥 Synchronization completed</b>

    <blockquote>
    <b>Total in panel:</b> { $total_panel_users }
    <b>Created:</b> { $created }
    <b>Synchronized:</b> { $synced }
    <b>Skipped:</b> { $skipped }
    <b>Errors:</b> { $errors }
    </blockquote>

# Remnawave Sync notifications
ntf-remnawave-sync-confirm = <i>⚠️ Press again to confirm import.</i>
ntf-remnawave-sync-preparing = <i>🔄 Preparing data for import...</i>
ntf-remnawave-sync-started = <i>🔄 Synchronizing data...</i>
ntf-remnawave-sync-no-users = <i>❌ No users found for import.</i>
ntf-remnawave-sync-failed =
    <i>❌ Import error:</i>

    <blockquote>{ $error }</blockquote>
ntf-remnawave-sync-bot-to-panel-completed =
    <b>✅ Import from Bot to Remnawave completed</b>

    <blockquote>
    <b>Total in bot:</b> { $total_bot_users }
    <b>Created:</b> { $created }
    <b>Updated:</b> { $updated }
    <b>Skipped:</b> { $skipped }
    <b>Errors:</b> { $errors }
    </blockquote>
ntf-remnawave-sync-panel-to-bot-completed =
    <b>✅ Sync from Remnawave to Bot completed</b>

    <blockquote>
    <b>Total in panel:</b> { $total_panel_users }
    <b>Created:</b> { $created }
    <b>Synchronized:</b> { $synced }
    <b>Skipped:</b> { $skipped }
    <b>Errors:</b> { $errors }
    </blockquote>

ntf-remnawave-import-completed =
    <b>✅ Remnawave Import completed</b>

    <blockquote>
    <b>Total in panel:</b> { $total_panel_users }
    <b>Total in bot:</b> { $total_bot_users }
    <b>Users added:</b> { $added_users }
    <b>Subscriptions added:</b> { $added_subscription }
    <b>Updated:</b> { $updated }
    <b>Without Telegram ID:</b> { $missing_telegram }
    <b>Errors:</b> { $errors }
    </blockquote>

ntf-subscription-processing = <i>⏳ Processing your subscription, please wait...</i>

# Promocodes
ntf-promocode-not-found = <i>❌ Promo code not found.</i>
ntf-promocode-inactive = <i>⚠️ Promo code is inactive.</i>
ntf-promocode-already-activated = <i>⚠️ You already used this promo code.</i>
ntf-promocode-limit-exceeded = <i>⚠️ Promo code limit reached.</i>
ntf-promocode-plan-unavailable = <i>⚠️ Promo code not available for your plan.</i>
ntf-promocode-activation-error = <i>❌ Error activating promo code.</i>
ntf-promocode-activated = <i>✅ Promo code <code>{$promocode}</code> activated successfully!</i>
ntf-promocode-invalid-name = <i>❌ Promo code name must be 1-50 characters.</i>
ntf-promocode-already-exists = <i>❌ Promo code with this code already exists.</i>
ntf-promocode-invalid-code = <i>❌ Promo code must be 3-20 characters.</i>
ntf-promocode-invalid-reward = <i>❌ Enter a valid reward value (positive number).</i>
ntf-promocode-invalid-lifetime = <i>❌ Enter a valid lifetime (0 = unlimited).</i>
ntf-promocode-invalid-quantity = <i>❌ Enter a valid activation count (0 = unlimited).</i>
ntf-promocode-created = <i>✅ Promo code created successfully.</i>
ntf-promocode-updated = <i>✅ Promo code updated successfully.</i>
ntf-promocode-save-error = <i>❌ Error saving promo code.</i>
ntf-promocode-delete-error = <i>❌ Error deleting promo code.</i>
ntf-promocode-delete-success = <i>✅ Promo code deleted successfully!</i>

# Devices
ntf-add-device-info = <i>ℹ️ Adding a device will increase subscription cost by <b>{ $price } ₽/mo</b>.</i>
ntf-add-device-success = <i>✅ New device limit applied!</i>
ntf-add-device-payment-pending = <i>⏳ Payment via selected gateway is temporarily unavailable for adding devices. Use balance.</i>
ntf-payment-link = <i>💳 <a href="{ $payment_url }">Proceed to payment</a></i>
ntf-payment-creation-failed = <i>❌ Error creating payment, try later.</i>
ntf-payment-gateway-not-available = <i>❌ Selected payment gateway is temporarily unavailable. Try later.</i>
ntf-subscription-required = <i>❌ Active subscription required to add devices.</i>
ntf-extra-device-auto-renew-disabled = <i>✅ Auto-renewal for extra devices disabled. Devices will be removed after expiration.</i>
ntf-extra-device-deleted = <i>✅ Extra devices deleted. Device limit updated.</i>
ntf-extra-device-decreased = <i>✅ Extra device removed. Device limit decreased.</i>
ntf-extra-device-marked-deletion = <i>🗑 Device marked for deletion and won't be charged on subscription renewal.</i>
ntf-extra-slot-deleted = <i>✅ Extra slot deleted. Device limit decreased.</i>
ntf-device-deleted = <i>✅ Device successfully removed from list!</i>
ntf-device-connected = <i>✅ Device successfully connected to subscription!</i>
ntf-extra-device-expired = <i>⚠️ { $device_count } extra device(s) expired. Device limit decreased.</i>
ntf-extra-device-renewed = <i>✅ Auto-renewal of { $device_count } extra device(s) successful! { $price } ₽ deducted from balance.</i>

# Bonus Activation
ntf-bonus-activated = <i>✅ Bonuses activated! { $amount } ₽ added to your balance.</i>
ntf-bonus-activate-no-balance = <i>❌ You don't have enough bonuses to activate this amount.</i>
ntf-bonus-activate-failed = <i>❌ Error activating bonuses. Try again.</i>
ntf-bonus-invalid-amount = <i>❌ Amount must be greater than zero.</i>
ntf-bonus-amount-exceeds = <i>❌ Amount cannot exceed available balance ({ $available } ₽).</i>
ntf-bonus-invalid-format = <i>❌ Please enter a valid number.</i>
ntf-extra-device-expired-no-balance = <i>⚠️ Insufficient funds to renew { $device_count } extra device(s) (need { $price } ₽). Devices deactivated.</i>
ntf-bonus-activate-no-selection = <i>⚠️ Select an amount to activate.</i>

# Hardcoded strings - UI notifications
ntf-click-start = Press /start to continue.
ntf-delete-msg-error = Failed to delete message
ntf-import-in-dev = Import is under development.
ntf-convert-in-dev = Conversion feature is not yet implemented.
ntf-file-not-found = File not found
ntf-backup-deleted = Backup deleted
ntf-delete-error = Delete error
ntf-in-development = Under development...

# System - Update notification
ntf-system-update-available =
    ✅ Current version: <code>{ $current_version }</code>
    ⬆️ Available version: <code>{ $new_version }</code>

    Press <b>"Update now"</b> or run the update from the bot management menu.

ntf-no-subscription-for-devices = <i>⚠️ You need to get a subscription first.</i>

ntf-no-subscription-for-connect = <i>⚠️ You need to get a subscription first.</i>


# Referral code change
ntf-ref-code-invalid =
    ❌ <b>Invalid code.</b>
    Use only: A–Z, a–z, 0–9, _ -
    Length: 3–32 characters.
ntf-ref-code-taken = ❌ This code is already taken. Please choose another one.
ntf-ref-code-success = ✅ Referral code changed to <code>{ $referral_code }</code>

# Admin balance change notification
ntf-event-admin-balance-change =
    🧑‍💻 <b>System: Balance changed by admin!</b>

    <b>👤 Admin:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $admin_id }</code>
    • <b>Name</b>: { $admin_name }
    { $admin_username ->
        [false] {""}
        *[other] • <b>Username</b>: @{ $admin_username }
    }
    </blockquote>

    <b>👤 User:</b>
    <blockquote>
    • <b>ID</b>: <code>{ $target_id }</code>
    • <b>Name</b>: { $target_name }
    { $target_username ->
        [false] {""}
        *[other] • <b>Username</b>: @{ $target_username }
    }
    </blockquote>

    <b>💰 Details:</b>
    <blockquote>
    • <b>Operation</b>: { $operation ->
        [ADD] ➕ Added
        *[SUB] ➖ Subtracted
    }
    • <b>Amount</b>: { $amount } ₽
    • <b>Balance after</b>: { $new_balance } ₽
    </blockquote>
