import { useNavigate } from 'react-router-dom';
import { Smartphone, Plus, AlertCircle } from 'lucide-react';
import { useUserStore } from '@dfc/shared';

export default function DevicesPage() {
  const navigate = useNavigate();
  const { subscription, features } = useUserStore();

  /* No subscription */
  if (!subscription || subscription.status !== 'ACTIVE') {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <h1 className="page-title animate-in">Устройства</h1>
        <div className="empty-state animate-in">
          <AlertCircle size={36} color="var(--text3)" style={{ margin: '0 auto 12px' }} />
          <p>Нет активной подписки</p>
          <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => navigate('/plans')}>
            Выбрать тариф
          </button>
        </div>
      </div>
    );
  }

  const used = subscription.active_devices_count ?? 0;
  const limit = subscription.device_limit ?? 0;
  const pct = limit > 0 ? Math.min((used / limit) * 100, 100) : 0;
  const isFull = limit > 0 && used >= limit;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      <h1 className="page-title animate-in">Устройства</h1>

      {/* Devices card */}
      <div className="card animate-in">
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
          <Smartphone size={18} color="var(--cyan)" />
          <span className="card-title" style={{ marginBottom: 0 }}>Подключённые устройства</span>
        </div>

        {/* Counter */}
        <div style={{ textAlign: 'center', margin: '8px 0 16px' }}>
          <span style={{ fontSize: '2rem', fontWeight: 700, color: isFull ? 'var(--red)' : 'var(--cyan)' }}>
            {used}
          </span>
          <span style={{ fontSize: '1.1rem', color: 'var(--text2)', fontWeight: 500 }}> / {limit || '∞'}</span>
        </div>

        {/* Progress bar */}
        {limit > 0 && (
          <div
            style={{
              width: '100%',
              height: 8,
              borderRadius: 4,
              background: 'var(--bg-card)',
              border: '1px solid var(--border)',
              overflow: 'hidden',
              marginBottom: 8,
            }}
          >
            <div
              style={{
                width: `${pct}%`,
                height: '100%',
                borderRadius: 4,
                background: isFull
                  ? 'var(--red)'
                  : 'linear-gradient(90deg, var(--cyan), #1AA3CC)',
                transition: 'width 0.4s ease',
              }}
            />
          </div>
        )}

        {isFull && (
          <p style={{ color: 'var(--red)', fontSize: '0.82rem', textAlign: 'center' }}>
            Лимит устройств достигнут
          </p>
        )}
      </div>

      {/* Extra device option */}
      {features?.extra_devices_enabled && (
        <div className="card animate-in">
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
            <Plus size={18} color="var(--green)" />
            <span className="fw-600">Дополнительное устройство</span>
          </div>
          <p style={{ color: 'var(--text2)', fontSize: '0.84rem', marginBottom: 14 }}>
            Вы можете добавить дополнительный слот для ещё одного устройства к текущей подписке.
          </p>
          <button
            className="btn btn-secondary btn-full"
            onClick={() => navigate('/plans')}
          >
            <Plus size={15} /> Купить доп. устройство
          </button>
        </div>
      )}
    </div>
  );
}
