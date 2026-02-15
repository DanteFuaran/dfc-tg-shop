from src.core.storage.key_builder import StorageKey


class WebhookLockKey(StorageKey, prefix="webhook_lock"):
    bot_id: int
    webhook_hash: str


class LastNotifiedVersionKey(StorageKey, prefix="last_notified_version"): ...


class UpdateSnoozeKey(StorageKey, prefix="update_snooze"): ...


class SyncRunningKey(StorageKey, prefix="sync_running"): ...


class AccessWaitListKey(StorageKey, prefix="access_wait_list"): ...


class RecentActivityUsersKey(StorageKey, prefix="recent_activity_users"): ...


class ShutdownMessagesKey(StorageKey, prefix="shutdown_messages"): ...


class UpdateMessageKey(StorageKey, prefix="update_message"): ...


class UpdateInProgressKey(StorageKey, prefix="update_in_progress"): ...


class CloseableMessagesKey(StorageKey, prefix="closeable_messages"): ...
