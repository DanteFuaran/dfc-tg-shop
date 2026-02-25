import { useNavigate } from 'react-router-dom';
import { useUserStore } from '@dfc/shared';
import { Zap, ShoppingCart, Wifi, Monitor, Gift, Wallet, MessageCircle, ExternalLink } from 'lucide-react';

export default function HomePage() {
  const navigate = useNavigate();
  const { user, subscription, features, trialAvailable, isLoading } = useUserStore();

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

  const daysLeft = hasSub && subscription.expire_at
    ? Math.max(0, Math.ceil((new Date(subscription.expire_at).getTime() - Date.now()) / 86400000))
    : 0;

  return (
    <div className="animate-in">
      {/* Greeting */}
      <div style={{ marginBottom: 20 }}>
        <h1 style={{ fontSize: '1.3rem', fontWeight: 700, margin: 0 }}>
          Привет, {user?.name || 'друг'} 👋
        </h1>
        <p style={{ color: 'var(--text2)', fontSize: '.9rem', marginTop: 4 }}>
          Ваш личный кабинет
        </p>
      </div>

      {/* Subscription Card */}
      <div className="card" style={{ marginBottom: 16 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
          <span style={{ fontSize: '.95rem', fontWeight: 600 }}>Подписка</span>
          {isActive ? (
            <span className={`badge ${isTrial ? 'badge-gold' : 'badge-green'}`}>
              {isTrial ? '🎁 Пробная' : '✓ Активна'}
            </span>
          ) : hasSub ? (
            <span className="badge badge-red">Истекла</span>
          ) : (
            <span className="badge" style={{ background: 'rgba(141,160,174,.12)', color: 'var(--text2)' }}>
              Нет подписки
            </span>
          )}
        </div>

        {isActive && (
          <>
            <div className="card-row">
              <span className="card-label">Тариф</span>
              <span className="card-value">{subscription.plan_name}</span>
            </div>
            <div className="card-row" style={{ marginTop: 8 }}>
              <span className="card-label">Осталось дней</span>
              <span className="card-value" style={{ color: daysLeft <= 3 ? 'var(--red)' : 'var(--cyan)' }}>
                {daysLeft}
              </span>
            </div>
            {subscription.device_limit && (
              <div className="card-row" style={{ marginTop: 8 }}>
                <span className="card-label">Устройства</span>
                <span className="card-value">
                  {subscription.active_devices_count} / {subscription.device_limit}
                </span>
              </div>
            )}
          </>
        )}

        {!hasSub && trialAvailable && (
          <div style={{ marginTop: 12 }}>
            <button className="btn btn-full" style={{ background: 'var(--green)', color: '#fff' }}
              onClick={() => navigate('/plans')}>
              <Zap size={16} /> Активировать пробный период
            </button>
          </div>
        )}

        {isActive && (
          <div style={{ display: 'flex', gap: 8, marginTop: 14 }}>
            <button className="btn btn-primary btn-full" onClick={() => navigate('/connect')}>
              <Wifi size={15} /> Подключить
            </button>
            <button className="btn btn-secondary btn-full" onClick={() => navigate('/devices')}>
              <Monitor size={15} /> Устройства
            </button>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
        <button className="card" style={{ cursor: 'pointer', textAlign: 'center', padding: 16 }}
          onClick={() => navigate('/plans')}>
          <ShoppingCart size={24} style={{ color: 'var(--cyan)', marginBottom: 8 }} />
          <div style={{ fontSize: '.85rem', fontWeight: 500 }}>Тарифы</div>
        </button>

        {features?.balance_enabled && (
          <button className="card" style={{ cursor: 'pointer', textAlign: 'center', padding: 16 }}
            onClick={() => navigate('/topup')}>
            <Wallet size={24} style={{ color: 'var(--gold)', marginBottom: 8 }} />
            <div style={{ fontSize: '.85rem', fontWeight: 500 }}>Пополнить</div>
          </button>
        )}

        {features?.promocodes_enabled && (
          <button className="card" style={{ cursor: 'pointer', textAlign: 'center', padding: 16 }}
            onClick={() => navigate('/promo')}>
            <Gift size={24} style={{ color: 'var(--green)', marginBottom: 8 }} />
            <div style={{ fontSize: '.85rem', fontWeight: 500 }}>Промокод</div>
          </button>
        )}

        <button className="card" style={{ cursor: 'pointer', textAlign: 'center', padding: 16 }}
          onClick={() => navigate('/support')}>
          <MessageCircle size={24} style={{ color: 'var(--orange)', marginBottom: 8 }} />
          <div style={{ fontSize: '.85rem', fontWeight: 500 }}>Поддержка</div>
        </button>

        {features?.community_enabled && features.community_url && (
          <button className="card" style={{ cursor: 'pointer', textAlign: 'center', padding: 16 }}
            onClick={() => window.open(features.community_url, '_blank')}>
            <ExternalLink size={24} style={{ color: 'var(--cyan)', marginBottom: 8 }} />
            <div style={{ fontSize: '.85rem', fontWeight: 500 }}>Сообщество</div>
          </button>
        )}
      </div>
    </div>
  );
}
