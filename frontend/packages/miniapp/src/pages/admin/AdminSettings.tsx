import { useState, useEffect, useCallback } from 'react';
import { ChevronDown, ChevronRight, Save, Globe, Shield, CreditCard, Users, Bell, Gift, Percent, Smartphone, MessageSquare, BookOpen, Zap, Languages, ArrowLeftRight } from 'lucide-react';
import { useAdminStore, useUserStore, formatPrice, CURRENCY_SYMBOLS } from '@dfc/shared';
import type { PaymentGateway } from '@dfc/shared';

/* ── Toggle component ── */
function Toggle({ value, onChange }: { value: boolean; onChange: (v: boolean) => void }) {
  return (
    <div className={`toggle-track${value ? ' active' : ''}`} onClick={() => onChange(!value)}>
      <div className="toggle-thumb" />
    </div>
  );
}

/* ── Collapsible section ── */
function Section({ title, icon, children, defaultOpen = false }: {
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
  defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className={`spoiler${open ? ' open' : ''}`}>
      <div className="spoiler-header" onClick={() => setOpen(!open)}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          {icon}
          <span className="fw-600" style={{ fontSize: '0.92rem' }}>{title}</span>
        </div>
        {open ? <ChevronDown size={16} color="var(--text2)" /> : <ChevronRight size={16} color="var(--text2)" />}
      </div>
      <div className="spoiler-body">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12, padding: '4px 0' }}>
          {children}
        </div>
      </div>
    </div>
  );
}

/* ── Setting row ── */
function SettingRow({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="card-row" style={{ padding: '8px 0' }}>
      <span className="card-label">{label}</span>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>{children}</div>
    </div>
  );
}

/* ── Inline text/number input with save ── */
function InlineInput({ value, onSave, type = 'text', placeholder }: {
  value: string;
  onSave: (v: string) => void;
  type?: string;
  placeholder?: string;
}) {
  const [local, setLocal] = useState(value);
  const [dirty, setDirty] = useState(false);

  useEffect(() => { setLocal(value); setDirty(false); }, [value]);

  const handleChange = (v: string) => { setLocal(v); setDirty(v !== value); };
  const handleSave = () => { onSave(local); setDirty(false); };

  return (
    <div style={{ display: 'flex', gap: 6, alignItems: 'center', flex: 1, maxWidth: 240 }}>
      <input
        className="input"
        type={type}
        value={local}
        onChange={(e) => handleChange(e.target.value)}
        onBlur={handleSave}
        onKeyDown={(e) => e.key === 'Enter' && handleSave()}
        placeholder={placeholder}
        style={{ padding: '8px 10px', fontSize: '0.85rem' }}
      />
      {dirty && (
        <button className="btn btn-primary btn-sm" style={{ padding: '6px 8px' }} onClick={handleSave}>
          <Save size={13} />
        </button>
      )}
    </div>
  );
}

/* ── Select input ── */
function SelectInput({ value, options, onChange }: {
  value: string;
  options: { value: string; label: string }[];
  onChange: (v: string) => void;
}) {
  return (
    <select
      className="input"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      style={{ padding: '8px 10px', fontSize: '0.85rem', maxWidth: 160 }}
    >
      {options.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
    </select>
  );
}

/* ── Textarea with save ── */
function InlineTextarea({ value, onSave, placeholder, rows = 3 }: {
  value: string;
  onSave: (v: string) => void;
  placeholder?: string;
  rows?: number;
}) {
  const [local, setLocal] = useState(value);
  const [dirty, setDirty] = useState(false);

  useEffect(() => { setLocal(value); setDirty(false); }, [value]);

  const handleChange = (v: string) => { setLocal(v); setDirty(v !== value); };
  const handleSave = () => { onSave(local); setDirty(false); };

  return (
    <div style={{ width: '100%', marginTop: 6 }}>
      <textarea
        className="input"
        rows={rows}
        value={local}
        onChange={(e) => handleChange(e.target.value)}
        onBlur={handleSave}
        placeholder={placeholder}
        style={{ resize: 'vertical', fontSize: '0.85rem' }}
      />
      {dirty && (
        <button className="btn btn-primary btn-sm" style={{ marginTop: 6 }} onClick={handleSave}>
          <Save size={13} /> Сохранить
        </button>
      )}
    </div>
  );
}

/* ═══════════════════════════════════════════════════
   AdminSettings — main export
   ═══════════════════════════════════════════════════ */
export default function AdminSettings() {
  const { settings, gateways, isLoading, fetchSettings, fetchGateways, updateSettings, updateGateway } = useAdminStore();

  const [toast, setToast] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  useEffect(() => {
    fetchSettings();
    fetchGateways();
  }, []);

  const showToast = (text: string, type: 'success' | 'error' = 'success') => {
    setToast({ text, type });
    setTimeout(() => setToast(null), 3000);
  };

  const set = useCallback(async (field: string, value: any) => {
    try {
      await updateSettings({ [field]: value });
    } catch {
      showToast('Ошибка сохранения', 'error');
    }
  }, [updateSettings]);

  const toggleField = useCallback((field: string, current: boolean) => {
    set(field, !current);
  }, [set]);

  if (isLoading && !settings) {
    return <div className="loading"><span className="spinner" /> Загрузка настроек…</div>;
  }

  if (!settings) {
    return <div className="empty-state">Настройки недоступны</div>;
  }

  const s = settings;

  return (
    <div className="animate-in" style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      <h2 className="page-title" style={{ margin: 0 }}>Настройки</h2>

      {/* ── Основные ── */}
      <Section title="Основные" icon={<Shield size={16} color="var(--cyan)" />} defaultOpen>
        <SettingRow label="Режим доступа">
          <SelectInput
            value={s.access_mode}
            options={[
              { value: 'public', label: 'Публичный' },
              { value: 'private', label: 'Приватный' },
              { value: 'channel', label: 'Канал' },
            ]}
            onChange={(v) => set('access_mode', v)}
          />
        </SettingRow>
        <SettingRow label="Требуется канал">
          <Toggle value={s.channel_required} onChange={(v) => set('channel_required', v)} />
        </SettingRow>
        {s.channel_required && (
          <SettingRow label="Ссылка на канал">
            <InlineInput value={s.channel_link} onSave={(v) => set('channel_link', v)} placeholder="https://t.me/channel" />
          </SettingRow>
        )}
        <SettingRow label="Требуются правила">
          <Toggle value={s.rules_required} onChange={(v) => set('rules_required', v)} />
        </SettingRow>
        <SettingRow label="Покупки разрешены">
          <Toggle value={s.purchases_allowed} onChange={(v) => set('purchases_allowed', v)} />
        </SettingRow>
        <SettingRow label="Регистрация разрешена">
          <Toggle value={s.registration_allowed} onChange={(v) => set('registration_allowed', v)} />
        </SettingRow>
      </Section>

      {/* ── Валюта и язык ── */}
      <Section title="Валюта и язык" icon={<Languages size={16} color="var(--gold)" />}>
        <SettingRow label="Валюта по умолчанию">
          <SelectInput
            value={s.default_currency}
            options={[
              { value: 'RUB', label: 'RUB ₽' },
              { value: 'USD', label: 'USD $' },
              { value: 'EUR', label: 'EUR €' },
              { value: 'XTR', label: 'XTR ★' },
            ]}
            onChange={(v) => set('default_currency', v)}
          />
        </SettingRow>
        <SettingRow label="Язык бота">
          <SelectInput
            value={s.bot_locale}
            options={[
              { value: 'RU', label: 'Русский' },
              { value: 'EN', label: 'English' },
              { value: 'UK', label: 'Українська' },
              { value: 'DE', label: 'Deutsch' },
            ]}
            onChange={(v) => set('bot_locale', v)}
          />
        </SettingRow>
        <SettingRow label="Выбор языка">
          <Toggle value={s.language_enabled} onChange={(v) => set('language_enabled', v)} />
        </SettingRow>
      </Section>

      {/* ── Баланс ── */}
      <Section title="Баланс" icon={<CreditCard size={16} color="var(--green)" />}>
        <SettingRow label="Баланс включён">
          <Toggle value={s.balance_enabled} onChange={(v) => set('balance_enabled', v)} />
        </SettingRow>
        {s.balance_enabled && (
          <SettingRow label="Режим баланса">
            <SelectInput
              value={s.balance_mode}
              options={[
                { value: 'balance', label: 'Баланс' },
                { value: 'bonus', label: 'Бонус' },
                { value: 'both', label: 'Оба' },
              ]}
              onChange={(v) => set('balance_mode', v)}
            />
          </SettingRow>
        )}
      </Section>

      {/* ── Переводы ── */}
      <Section title="Переводы" icon={<ArrowLeftRight size={16} color="var(--cyan)" />}>
        <SettingRow label="Переводы включены">
          <Toggle value={s.transfers_enabled} onChange={(v) => set('transfers_enabled', v)} />
        </SettingRow>
      </Section>

      {/* ── Доп. устройства ── */}
      <Section title="Доп. устройства" icon={<Smartphone size={16} color="var(--orange)" />}>
        <SettingRow label="Доп. устройства включены">
          <Toggle value={s.extra_devices_enabled} onChange={(v) => set('extra_devices_enabled', v)} />
        </SettingRow>
        {s.extra_devices_enabled && (
          <SettingRow label="Цена за устройство">
            <InlineInput
              value={String(s.extra_devices_price ?? 0)}
              onSave={(v) => set('extra_devices_price', Number(v))}
              type="number"
              placeholder="0"
            />
          </SettingRow>
        )}
      </Section>

      {/* ── Скидка ── */}
      <Section title="Скидка" icon={<Percent size={16} color="var(--red)" />}>
        <SettingRow label="Глобальная скидка">
          <Toggle value={s.global_discount_enabled} onChange={(v) => set('global_discount_enabled', v)} />
        </SettingRow>
        {s.global_discount_enabled && (
          <SettingRow label="Процент скидки">
            <InlineInput
              value={String(s.global_discount_percent ?? 0)}
              onSave={(v) => set('global_discount_percent', Number(v))}
              type="number"
              placeholder="0"
            />
          </SettingRow>
        )}
      </Section>

      {/* ── Реферальная программа ── */}
      <Section title="Реферальная программа" icon={<Users size={16} color="var(--gold)" />}>
        <SettingRow label="Реферальная программа">
          <Toggle value={s.referral_enabled} onChange={(v) => set('referral_enabled', v)} />
        </SettingRow>
        {s.referral_enabled && (
          <>
            <SettingRow label="Тип награды">
              <SelectInput
                value={s.referral_type}
                options={[
                  { value: 'balance', label: 'Баланс' },
                  { value: 'bonus', label: 'Бонус' },
                  { value: 'subscription', label: 'Подписка' },
                ]}
                onChange={(v) => set('referral_type', v)}
              />
            </SettingRow>
            <SettingRow label="Размер награды">
              <InlineInput
                value={String(s.referral_reward ?? 0)}
                onSave={(v) => set('referral_reward', Number(v))}
                type="number"
                placeholder="0"
              />
            </SettingRow>
            <div style={{ padding: '4px 0' }}>
              <span className="card-label" style={{ display: 'block', marginBottom: 6 }}>Сообщение приглашения</span>
              <InlineTextarea
                value={s.referral_invite_message ?? ''}
                onSave={(v) => set('referral_invite_message', v)}
                placeholder="Текст приглашения"
                rows={3}
              />
            </div>
          </>
        )}
      </Section>

      {/* ── Промокоды ── */}
      <Section title="Промокоды" icon={<Gift size={16} color="var(--green)" />}>
        <SettingRow label="Промокоды включены">
          <Toggle value={s.promocodes_enabled} onChange={(v) => set('promocodes_enabled', v)} />
        </SettingRow>
      </Section>

      {/* ── Пробный период ── */}
      <Section title="Пробный период" icon={<Zap size={16} color="var(--green)" />}>
        <SettingRow label="Пробный период включён">
          <Toggle value={s.trial_enabled} onChange={(v) => set('trial_enabled', v)} />
        </SettingRow>
      </Section>

      {/* ── Сообщество ── */}
      <Section title="Сообщество" icon={<MessageSquare size={16} color="var(--cyan)" />}>
        <SettingRow label="Сообщество включено">
          <Toggle value={s.community_enabled} onChange={(v) => set('community_enabled', v)} />
        </SettingRow>
        {s.community_enabled && (
          <SettingRow label="URL сообщества">
            <InlineInput
              value={s.community_url ?? ''}
              onSave={(v) => set('community_url', v)}
              placeholder="https://t.me/community"
            />
          </SettingRow>
        )}
      </Section>

      {/* ── Правила использования ── */}
      <Section title="Правила использования" icon={<BookOpen size={16} color="var(--text2)" />}>
        <SettingRow label="Правила включены">
          <Toggle value={s.tos_enabled} onChange={(v) => set('tos_enabled', v)} />
        </SettingRow>
        {s.tos_enabled && (
          <SettingRow label="URL правил">
            <InlineInput
              value={s.tos_url ?? ''}
              onSave={(v) => set('tos_url', v)}
              placeholder="https://example.com/tos"
            />
          </SettingRow>
        )}
      </Section>

      {/* ── Уведомления ── */}
      <Section title="Уведомления" icon={<Bell size={16} color="var(--orange)" />}>
        <SettingRow label="Уведомления включены">
          <Toggle value={s.notifications_enabled} onChange={(v) => set('notifications_enabled', v)} />
        </SettingRow>
      </Section>

      {/* ── Платёжные шлюзы ── */}
      <Section title="Платёжные шлюзы" icon={<Globe size={16} color="var(--cyan)" />}>
        {gateways.length === 0 && (
          <div className="empty-state" style={{ padding: 16 }}>Нет шлюзов</div>
        )}
        {gateways.map((gw) => (
          <GatewayCard key={gw.id} gateway={gw} onToggle={async (id, active) => {
            try {
              await updateGateway(id, { is_active: active });
            } catch {
              showToast('Ошибка переключения шлюза', 'error');
            }
          }} />
        ))}
      </Section>

      {/* Toast */}
      {toast && (
        <div className={`toast ${toast.type === 'error' ? 'toast-error' : 'toast-success'}`}>
          {toast.text}
        </div>
      )}
    </div>
  );
}

/* ── Gateway card ── */
function GatewayCard({ gateway, onToggle }: {
  gateway: PaymentGateway;
  onToggle: (id: number, active: boolean) => void;
}) {
  return (
    <div className="card" style={{ padding: 14 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <div className="fw-600" style={{ fontSize: '0.9rem', marginBottom: 2 }}>{gateway.type}</div>
          <div style={{ color: 'var(--text2)', fontSize: '0.8rem' }}>
            {gateway.currency} {CURRENCY_SYMBOLS[gateway.currency] ?? ''}
          </div>
        </div>
        <Toggle value={gateway.is_active} onChange={(v) => onToggle(gateway.id, v)} />
      </div>
    </div>
  );
}
