import { useEffect, useState } from 'react';
import { useAdminStore } from '@dfc/shared';
import type { Settings } from '@dfc/shared';
import { Save } from 'lucide-react';
import toast from 'react-hot-toast';

const BOOL_FIELDS: { key: keyof Settings; label: string }[] = [
  { key: 'registration_allowed', label: 'Регистрация' },
  { key: 'purchases_allowed', label: 'Покупки' },
  { key: 'balance_enabled', label: 'Баланс' },
  { key: 'referral_enabled', label: 'Реферальная система' },
  { key: 'community_enabled', label: 'Сообщество' },
  { key: 'tos_enabled', label: 'Правила (ToS)' },
  { key: 'promocodes_enabled', label: 'Промокоды' },
  { key: 'notifications_enabled', label: 'Уведомления' },
  { key: 'extra_devices_enabled', label: 'Расширение устройств' },
  { key: 'transfers_enabled', label: 'Переводы баланса' },
  { key: 'global_discount_enabled', label: 'Глобальная скидка' },
  { key: 'language_enabled', label: 'Выбор языка' },
  { key: 'trial_enabled', label: 'Пробный период' },
  { key: 'channel_required', label: 'Подписка на канал' },
  { key: 'rules_required', label: 'Согласие с правилами' },
];

export default function AdminSettings() {
  const { settings, fetchSettings, updateSettings: saveSettings } = useAdminStore();
  const [local, setLocal] = useState<Partial<Settings>>({});
  const [saving, setSaving] = useState(false);

  useEffect(() => { fetchSettings(); }, [fetchSettings]);
  useEffect(() => { if (settings) setLocal(settings); }, [settings]);

  const toggle = (key: keyof Settings) => {
    setLocal((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await saveSettings(local);
      toast.success('Настройки сохранены');
    } catch {
      toast.error('Ошибка сохранения');
    } finally { setSaving(false); }
  };

  if (!settings) return <div className="empty-state">Загрузка...</div>;

  return (
    <div className="admin-form">
      <div className="card">
        {BOOL_FIELDS.map(({ key, label }) => (
          <div key={key} className="admin-form-row">
            <span className="admin-form-label">{label}</span>
            <button
              className="toggle-switch"
              data-on={!!local[key]}
              onClick={() => toggle(key)}
            >
              <span className="toggle-knob" />
            </button>
          </div>
        ))}
      </div>

      <div className="card">
        <label className="admin-form-label">Ссылка на сообщество</label>
        <input
          className="input"
          value={(local as any).community_url ?? ''}
          onChange={(e) => setLocal({ ...local, community_url: e.target.value })}
        />
        <label className="admin-form-label" style={{ marginTop: 8 }}>Ссылка на правила</label>
        <input
          className="input"
          value={(local as any).tos_url ?? ''}
          onChange={(e) => setLocal({ ...local, tos_url: e.target.value })}
        />
        <label className="admin-form-label" style={{ marginTop: 8 }}>Цена за доп. устройство</label>
        <input
          className="input"
          type="number"
          value={(local as any).extra_devices_price ?? 0}
          onChange={(e) => setLocal({ ...local, extra_devices_price: Number(e.target.value) })}
        />
        <label className="admin-form-label" style={{ marginTop: 8 }}>Скидка (%)</label>
        <input
          className="input"
          type="number"
          value={(local as any).global_discount_percent ?? 0}
          onChange={(e) => setLocal({ ...local, global_discount_percent: Number(e.target.value) })}
        />
        <label className="admin-form-label" style={{ marginTop: 8 }}>Реферальный бонус</label>
        <input
          className="input"
          type="number"
          value={(local as any).referral_reward ?? 0}
          onChange={(e) => setLocal({ ...local, referral_reward: Number(e.target.value) })}
        />
      </div>

      <button className="btn btn-primary btn-full btn-glossy" disabled={saving} onClick={handleSave}>
        <Save size={16} /> {saving ? 'Сохранение...' : 'Сохранить'}
      </button>
    </div>
  );
}
