import { useNavigate } from 'react-router-dom';
import { useUserStore, copyToClipboard } from '@dfc/shared';
import { Gift, Wifi, Smartphone, Link2, ShoppingCart, CreditCard } from 'lucide-react';

export default function HomePage() {
  const navigate = useNavigate();
  const {
    user, subscription, features, trialAvailable, isLoading, refLink,
  } = useUserStore();

  if (isLoading) {
    return (
      <div className="animate-in" style={{ display: 'flex', justifyContent: 'center', paddingTop: 60 }}>
        <div className="spinner" />
      </div>
    );
  }

  const isActive = subscription?.status === 'ACTIVE';
  const isTrial = subscription?.is_trial;
  const subText = isActive ? subscription!.plan_name : 'Нет активной подписки';
  const buyLabel = isActive && !isTrial ? 'Оплатить подписку' : 'Купить подписку';
  const BuyIcon = isActive && !isTrial ? CreditCard : ShoppingCart;

  return (
    <div className="animate-in" style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>

      {/* ── Subscription status ── */}
      <div className="card" style={{ textAlign: 'center', padding: '18px 16px' }}>
        <div style={{ color: isActive ? 'var(--text)' : 'var(--text2)', fontSize: '.95rem' }}>
          {subText}
        </div>
      </div>

      {/* ── Buy / Pay subscription ── */}
      <div className="card" style={{ textAlign: 'center', padding: '14px 16px', cursor: 'pointer' }}
        onClick={() => navigate('/plans')}>
        <span style={{ fontWeight: 600, fontSize: '.95rem', color: 'var(--cyan)', display: 'inline-flex', alignItems: 'center', gap: 8 }}>
          <BuyIcon size={18} /> {buyLabel}
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

      {/* ── Topup ── */}
      {features?.balance_enabled && user && (
        <div className="card" style={{ textAlign: 'center', padding: '14px 16px', cursor: 'pointer' }}
          onClick={() => navigate('/topup')}>
          <span style={{ fontWeight: 600, fontSize: '.95rem', color: 'var(--text)', display: 'inline-flex', alignItems: 'center', gap: 8 }}>
            <CreditCard size={18} style={{ color: 'var(--green)' }} /> Пополнить баланс
          </span>
        </div>
      )}

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
