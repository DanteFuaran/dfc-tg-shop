import { useState, useEffect, useCallback } from 'react';
import { adminApi } from '@dfc/shared';
import type { Settings } from '@dfc/shared';
import { Loader2, Save, ToggleLeft, ToggleRight } from 'lucide-react';

type ToggleKey = keyof Settings;

interface Section {
  title: string;
  items: {
    key: ToggleKey;
    label: string;
    desc?: string;
    urlKey?: ToggleKey;
    urlLabel?: string;
  }[];
}

const SECTIONS: Section[] = [
  {
    title: 'Основные',
    items: [
      { key: 'registration_allowed', label: 'Регистрация', desc: 'Разрешить новым пользователям регистрироваться' },
      { key: 'purchases_allowed', label: 'Покупки', desc: 'Разрешить покупки подписок' },
      { key: 'trial_enabled', label: 'Пробный период', desc: 'Бесплатная пробная подписка' },
    ],
  },
  {
    title: 'Баланс и реферальная',
    items: [
      { key: 'balance_enabled', label: 'Пополнение баланса', desc: 'Разрешить пополнение внутреннего баланса' },
      { key: 'transfers_enabled', label: 'Переводы', desc: 'Переводы между пользователями' },
      { key: 'referral_enabled', label: 'Реферальная программа', desc: 'Вознаграждение за приглашённых пользователей' },
      { key: 'extra_devices_enabled', label: 'Доп. устройства', desc: 'Возможность докупать дополнительные устройства' },
    ],
  },
  {
    title: 'Скидки и промокоды',
    items: [
      { key: 'promocodes_enabled', label: 'Промокоды', desc: 'Активация промокодов пользователями' },
      { key: 'global_discount_enabled', label: 'Глобальная скидка', desc: 'Применить скидку ко всем покупкам' },
    ],
  },
  {
    title: 'Сообщество и политика',
    items: [
      { key: 'community_enabled', label: 'Сообщество', desc: 'Ссылка на Telegram канал/группу', urlKey: 'community_url', urlLabel: 'URL сообщества' },
      { key: 'tos_enabled', label: 'Соглашение (ToS)', desc: 'Пользовательское соглашение', urlKey: 'tos_url', urlLabel: 'URL соглашения' },
    ],
  },
  {
    title: 'Уведомления',
    items: [
      { key: 'notifications_enabled' as ToggleKey, label: 'Уведомления', desc: 'Системные уведомления администратора' },
    ],
  },
];

export default function AdminFeatures() {
  const [settings, setSettings] = useState<Partial<Settings>>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await adminApi.getSettings();
      setSettings(data as Partial<Settings>);
    } catch { /* ignore */ }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { load(); }, [load]);

  const saveField = async (key: ToggleKey, value: unknown) => {
    setSaving(key);
    const updated = { ...settings, [key]: value };
    setSettings(updated);
    try {
      await adminApi.updateSettings({ [key]: value } as Partial<Settings>);
    } catch { /* rollback */
      setSettings(settings);
    } finally {
      setSaving(null);
    }
  };

  const saveUrlField = async (key: ToggleKey, value: string) => {
    setSaving(key);
    const updated = { ...settings, [key]: value };
    setSettings(updated);
    try {
      await adminApi.updateSettings({ [key]: value } as Partial<Settings>);
    } catch {
      setSettings(settings);
    } finally {
      setSaving(null);
    }
  };

  if (loading) return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: 40 }}>
      <Loader2 size={28} className="spinner" />
    </div>
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      {SECTIONS.map(section => (
        <div key={section.title} className="card">
          <div className="fw-600" style={{ fontSize: '0.85rem', color: 'var(--text2)', marginBottom: 10, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            {section.title}
          </div>

          {section.items.map((item, idx) => {
            const toggled = Boolean(settings[item.key]);
            const isSaving = saving === item.key;

            return (
              <div key={item.key}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 10,
                  padding: '10px 0',
                  borderBottom: idx < section.items.length - 1 ? '1px solid var(--border)' : 'none',
                }}>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div className="fw-600" style={{ fontSize: '0.9rem' }}>{item.label}</div>
                    {item.desc && <div className="text-muted" style={{ fontSize: '0.78rem' }}>{item.desc}</div>}
                  </div>
                  {isSaving ? (
                    <Loader2 size={20} className="spinner" />
                  ) : (
                    <button
                      className="btn btn-ghost"
                      style={{ padding: '4px 4px' }}
                      onClick={() => saveField(item.key, !toggled)}
                    >
                      {toggled
                        ? <ToggleRight size={28} style={{ color: 'var(--green)' }} />
                        : <ToggleLeft size={28} style={{ color: 'var(--text3)' }} />
                      }
                    </button>
                  )}
                </div>

                {/* URL field when toggle is on */}
                {item.urlKey && toggled && (() => {
                  const urlKey = item.urlKey!;
                  return (
                    <div style={{ paddingBottom: 10, paddingTop: 4, borderBottom: idx < section.items.length - 1 ? '1px solid var(--border)' : 'none' }}>
                      <label className="form-label">{item.urlLabel}</label>
                      <div style={{ display: 'flex', gap: 8 }}>
                        <input
                          className="input"
                          style={{ flex: 1, fontSize: '0.83rem' }}
                          placeholder="https://t.me/..."
                          value={(settings[urlKey] as string) || ''}
                          onChange={e => setSettings(prev => ({ ...prev, [urlKey]: e.target.value }))}
                        />
                        <button
                          className="btn btn-ghost btn-sm"
                          style={{ flexShrink: 0 }}
                          disabled={saving === urlKey}
                          onClick={() => saveUrlField(urlKey, (settings[urlKey] as string) || '')}
                        >
                          {saving === urlKey ? <Loader2 size={14} className="spinner" /> : <Save size={14} />}
                        </button>
                      </div>
                    </div>
                  );
                })()}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}
