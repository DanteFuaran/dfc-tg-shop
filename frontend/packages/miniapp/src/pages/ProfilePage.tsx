import { useState } from 'react';
import { useUserStore, formatPrice, copyToClipboard, CURRENCY_SYMBOLS } from '@dfc/shared';
import { Copy, Check, Users, Wallet, Globe } from 'lucide-react';

export default function ProfilePage() {
  const { user, features, refLink, defaultCurrency, botLocale, subscription } = useUserStore();
  const [copied, setCopied] = useState(false);

  if (!user) return null;

  const currSymbol = CURRENCY_SYMBOLS[defaultCurrency] || defaultCurrency;

  const handleCopyRef = async () => {
    if (refLink) {
      const ok = await copyToClipboard(refLink);
      if (ok) {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }
    }
  };

  return (
    <div className="animate-in">
      <h2 className="page-title">Профиль</h2>

      {/* User Info Card */}
      <div className="card" style={{ marginBottom: 12 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 14 }}>
          <div style={{
            width: 48, height: 48, borderRadius: '50%',
            background: 'linear-gradient(135deg, var(--cyan), #1AA3CC)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '1.3rem', fontWeight: 700, color: '#fff'
          }}>
            {user.name?.charAt(0)?.toUpperCase() || '?'}
          </div>
          <div>
            <div style={{ fontWeight: 600, fontSize: '1rem' }}>{user.name}</div>
            {user.username && (
              <div style={{ color: 'var(--text2)', fontSize: '.85rem' }}>@{user.username}</div>
            )}
          </div>
        </div>

        <div className="card-row">
          <span className="card-label">Telegram ID</span>
          <span className="card-value" style={{ fontFamily: 'var(--font-mono)', fontSize: '.85rem' }}>
            {user.telegram_id}
          </span>
        </div>
        <div className="card-row" style={{ marginTop: 8 }}>
          <span className="card-label">Роль</span>
          <span className={`badge ${user.role === 'DEV' ? 'role-dev' : user.role === 'ADMIN' ? 'role-admin' : 'role-user'}`}>
            {user.role}
          </span>
        </div>
        <div className="card-row" style={{ marginTop: 8 }}>
          <span className="card-label">Язык</span>
          <span className="card-value">{botLocale}</span>
        </div>
      </div>

      {/* Balance Card */}
      {features?.balance_enabled && (
        <div className="card" style={{ marginBottom: 12 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
            <Wallet size={18} style={{ color: 'var(--gold)' }} />
            <span style={{ fontWeight: 600 }}>Баланс</span>
          </div>
          <div className="card-row">
            <span className="card-label">Основной</span>
            <span className="card-value" style={{ color: 'var(--cyan)', fontWeight: 600 }}>
              {formatPrice(user.balance)} {currSymbol}
            </span>
          </div>
          <div className="card-row" style={{ marginTop: 8 }}>
            <span className="card-label">Реферальный</span>
            <span className="card-value" style={{ color: 'var(--gold)' }}>
              {formatPrice(user.referral_balance)} {currSymbol}
            </span>
          </div>
        </div>
      )}

      {/* Referral Card */}
      {features?.referral_enabled && refLink && (
        <div className="card" style={{ marginBottom: 12 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
            <Users size={18} style={{ color: 'var(--green)' }} />
            <span style={{ fontWeight: 600 }}>Реферальная программа</span>
          </div>
          
          {features.referral_invite_message && (
            <p style={{ color: 'var(--text2)', fontSize: '.85rem', marginBottom: 12 }}>
              {features.referral_invite_message}
            </p>
          )}
          
          <div style={{
            background: 'var(--bg-input)', border: '1px solid var(--border)',
            borderRadius: 'var(--r-sm)', padding: '10px 12px',
            fontFamily: 'var(--font-mono)', fontSize: '.8rem', color: 'var(--text2)',
            wordBreak: 'break-all', marginBottom: 10
          }}>
            {refLink}
          </div>
          <button className="btn btn-primary btn-full" onClick={handleCopyRef}>
            {copied ? <><Check size={15} /> Скопировано!</> : <><Copy size={15} /> Копировать ссылку</>}
          </button>
        </div>
      )}

      {/* Subscription Info */}
      {subscription && subscription.status && (
        <div className="card">
          <div style={{ fontWeight: 600, marginBottom: 12 }}>Подписка</div>
          <div className="card-row">
            <span className="card-label">Тариф</span>
            <span className="card-value">{subscription.plan_name}</span>
          </div>
          <div className="card-row" style={{ marginTop: 8 }}>
            <span className="card-label">Статус</span>
            <span className={`badge ${subscription.status === 'ACTIVE' ? 'badge-green' : 'badge-red'}`}>
              {subscription.status === 'ACTIVE' ? 'Активна' : subscription.status === 'EXPIRED' ? 'Истекла' : 'Отключена'}
            </span>
          </div>
          {subscription.url && (
            <div className="card-row" style={{ marginTop: 8 }}>
              <span className="card-label">Ссылка подписки</span>
              <button className="btn btn-secondary" style={{ padding: '4px 10px', fontSize: '.8rem' }}
                onClick={() => copyToClipboard(subscription.url)}>
                <Copy size={13} /> Скопировать
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
