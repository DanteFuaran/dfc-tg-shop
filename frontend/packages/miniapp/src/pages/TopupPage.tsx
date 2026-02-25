import { useState } from 'react';
import { Wallet, Loader2, ExternalLink, CreditCard } from 'lucide-react';
import { useUserStore, purchaseApi, formatPrice, CURRENCY_SYMBOLS, GATEWAY_LABELS, GATEWAY_DESCRIPTIONS } from '@dfc/shared';

const PRESET_AMOUNTS = [100, 250, 500, 1000];

export default function TopupPage() {
  const { user, features, availableGateways, defaultCurrency } = useUserStore();
  const [amount, setAmount] = useState('');
  const [gateway, setGateway] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const symbol = CURRENCY_SYMBOLS[defaultCurrency] || defaultCurrency;
  const topupGateways = (availableGateways || []).filter((g: any) => g.type !== 'BALANCE');

  if (!features?.balance_enabled) {
    return (
      <div className="animate-in">
        <h2 className="page-title">Пополнение баланса</h2>
        <div className="card empty-state">
          <Wallet size={32} style={{ margin: '0 auto 12px', color: 'var(--text3)' }} />
          <p className="text-muted">Пополнение баланса отключено</p>
        </div>
      </div>
    );
  }

  const handleTopup = async () => {
    const num = parseFloat(amount);
    if (!num || num <= 0 || !gateway || loading) return;
    setLoading(true);
    setError('');
    try {
      const res = await purchaseApi.topup({ amount: num, gateway });
      if (res.data?.payment_url) {
        window.open(res.data.payment_url, '_blank');
      }
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Ошибка при пополнении');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-in" style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      <h2 className="page-title">Пополнение баланса</h2>

      {/* Current balance */}
      <div className="card" style={{ textAlign: 'center' }}>
        <div className="text-muted" style={{ fontSize: '0.85rem', marginBottom: 4 }}>Текущий баланс</div>
        <div className="text-cyan fw-700" style={{ fontSize: '1.6rem' }}>
          {formatPrice(user?.balance ?? 0)} {symbol}
        </div>
      </div>

      {/* Amount input */}
      <div className="form-group">
        <label className="form-label">Сумма пополнения</label>
        <input
          className="input"
          type="number"
          min="1"
          placeholder={`Сумма (${symbol})`}
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
      </div>

      {/* Preset pills */}
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        {PRESET_AMOUNTS.map((v) => (
          <button
            key={v}
            className={`pill ${amount === String(v) ? 'pill-filled' : 'pill-outline'}`}
            onClick={() => setAmount(String(v))}
          >
            {v} {symbol}
          </button>
        ))}
      </div>

      {/* Gateway selector */}
      {topupGateways.length > 0 && (
        <div className="form-group">
          <label className="form-label">Способ оплаты</label>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {topupGateways.map((gw: any) => {
              const key = gw.code || gw.gateway || gw.id;
              const isSelected = gateway === key;
              return (
                <div
                  key={key}
                  className="card"
                  style={{
                    cursor: 'pointer',
                    borderColor: isSelected ? 'var(--cyan)' : undefined,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 12,
                    padding: '14px 16px',
                  }}
                  onClick={() => setGateway(key)}
                >
                  <CreditCard size={20} style={{ color: isSelected ? 'var(--cyan)' : 'var(--text3)', flexShrink: 0 }} />
                  <div style={{ flex: 1 }}>
                    <div className="fw-600" style={{ fontSize: '0.9rem' }}>{GATEWAY_LABELS[key] || key}</div>
                    {GATEWAY_DESCRIPTIONS[key] && (
                      <div className="text-muted" style={{ fontSize: '0.78rem' }}>{GATEWAY_DESCRIPTIONS[key]}</div>
                    )}
                  </div>
                  {isSelected && <div className="badge badge-cyan">✓</div>}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {error && <div className="text-red" style={{ fontSize: '0.85rem' }}>{error}</div>}

      <button
        className="btn btn-primary btn-full"
        disabled={!parseFloat(amount) || !gateway || loading}
        onClick={handleTopup}
      >
        {loading ? <Loader2 size={18} className="spinner" /> : <ExternalLink size={18} />}
        {loading ? 'Обработка...' : 'Пополнить'}
      </button>
    </div>
  );
}
