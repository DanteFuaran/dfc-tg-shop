import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUserStore, adminApi, formatPrice, copyToClipboard, CURRENCY_SYMBOLS } from '@dfc/shared';
import { Gift, ShoppingCart, Wifi, Smartphone, Link2, CreditCard } from 'lucide-react';

export default function HomePage() {
  const navigate = useNavigate();
  const {
    user, subscription, features, trialAvailable, isLoading,
    defaultCurrency, refLink,
  } = useUserStore();

  const [brand, setBrand] = useState<{ name: string; logo: string; slogan: string }>({
    name: 'VPN Shop', logo: '🔐', slogan: '',
  });

  useEffect(() => {
    adminApi.getBrand()
      .then(({ data }) => setBrand({ name: data.name || 'VPN Shop', logo: data.logo || '🔐', slogan: data.slogan || '' }))
      .catch(() => {});
  }, []);

  const sym = CURRENCY_SYMBOLS[defaultCurrency] || '₽';

  if (isLoading) {
    return (
      <div className="animate-in" style={{ display: 'flex', justifyContent: 'center', paddingTop: 60 }}>
        <div className="spinner" />
      </div>
    );
  }

  const hasSub = subscription && subscription.status;
  const isActive = hasSub && subscription.status === 'ACTIVE';
  const isTrial = hasSub && subscription.is_trial;

  /* Subscription label */
  const subText = isActive
    ? subscription.plan_name
    : 'Нет активной подписки';

  /* Buy button label */
  const buyLabel = isActive && !isTrial ? 'Оплатить подписку' : 'Купить подписку';

  return (
    <div className="animate-in" style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>

      {/* ── Header: brand + balances ── */}
      <div className="card" style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '14px 16px' }}>
        {/* Logo */}
        <div style={{
          width: 44, height: 44, borderRadius: 10,
          background: 'linear-gradient(135deg, var(--cyan), #1AA3CC)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: brand.logo.length <= 2 ? '1.5rem' : '1rem', flexShrink: 0,
        }}>
          {brand.logo}
        </div>

        {/* Name + slogan */}
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontWeight: 700, fontSize: '1rem', lineHeight: 1.2 }}>{brand.name}</div>
          {brand.slogan && (
            <div style={{ color: 'var(--text2)', fontSize: '.75rem', marginTop: 2 }}>{brand.slogan}</div>
          )}
        </div>

        {/* Balances */}
        {features?.balance_enabled && user && (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 2, flexShrink: 0 }}>
            <span style={{ fontSize: '.8rem', color: 'var(--text2)', display: 'flex', alignItems: 'center', gap: 4 }}>
              💰 {formatPrice(user.balance)} {sym}
            </span>
            <span style={{ fontSize: '.8rem', color: 'var(--text2)', display: 'flex', alignItems: 'center', gap: 4 }}>
              🎁 {formatPrice(user.referral_balance)} {sym}
            </span>
          </div>
        )}
      </div>

      {/* ── Subscription status ── */}
      <div className="card" style={{ textAlign: 'center', padding: '18px 16px' }}>
        <div style={{ color: isActive ? 'var(--text)' : 'var(--text2)', fontSize: '.95rem' }}>
          {subText}
        </div>
      </div>

      {/* ── Buy / Pay subscription ── */}
      <div className="card" style={{ textAlign: 'center', padding: '14px 16px', cursor: 'pointer' }}
        onClick={() => navigate('/plans')}>
        <span style={{ fontWeight: 600, fontSize: '.95rem', color: 'var(--cyan)' }}>
          {buyLabel}
        </span>
      </div>

      {/* ── Trial button ── */}
      {trialAvailable && (
        <div className="card" style={{
          textAlign: 'center', padding: '14px 16px', cursor: 'pointer',
          borderColor: 'rgba(25, 195, 125, 0.3)',
        }}
          onClick={() => navigate('/plans')}>
          <span style={{ fontWeight: 600, fontSize: '.95rem', color: 'var(--green)', display: 'inline-flex', alignItems: 'center', gap: 8 }}>
            <Gift size={18} /> Попробовать бесплатно
          </span>
        </div>
      )}

      {/* ── Connect ── */}
      <div className="card" style={{ textAlign: 'center', padding: '14px 16px', cursor: 'pointer' }}
        onClick={() => navigate('/connect')}>
        <span style={{ fontWeight: 600, fontSize: '.95rem', color: 'var(--text)', display: 'inline-flex', alignItems: 'center', gap: 8 }}>
          <Wifi size={18} style={{ color: 'var(--cyan)' }} /> Подключиться
        </span>
      </div>

      {/* ── Promo + Devices row ── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
        {features?.promocodes_enabled && (
          <div className="card" style={{ textAlign: 'center', padding: '14px 12px', cursor: 'pointer' }}
            onClick={() => navigate('/promo')}>
            <span style={{ fontWeight: 600, fontSize: '.85rem', display: 'inline-flex', alignItems: 'center', gap: 6 }}>
              <Gift size={16} style={{ color: 'var(--gold)' }} /> Промокоды
            </span>
          </div>
        )}

        <div className="card" style={{ textAlign: 'center', padding: '14px 12px', cursor: 'pointer' }}
          onClick={() => navigate('/devices')}>
          <span style={{ fontWeight: 600, fontSize: '.85rem', display: 'inline-flex', alignItems: 'center', gap: 6 }}>
            <Smartphone size={16} style={{ color: 'var(--gold)' }} /> Устройства
          </span>
        </div>
      </div>

      {/* ── Invite friend ── */}
      {features?.referral_enabled && refLink && (
        <div className="card" style={{ textAlign: 'center', padding: '14px 16px', cursor: 'pointer' }}
          onClick={() => copyToClipboard(refLink)}>
          <span style={{ fontWeight: 600, fontSize: '.95rem', color: 'var(--text)', display: 'inline-flex', alignItems: 'center', gap: 8 }}>
            <Link2 size={18} style={{ color: 'var(--cyan)' }} /> Пригласить друга
          </span>
        </div>
      )}
    </div>
  );
}
