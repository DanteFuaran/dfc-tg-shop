import { useState, useMemo } from 'react';
import {
  useUserStore,
  purchaseApi,
  CURRENCY_SYMBOLS,
  GATEWAY_LABELS,
  GATEWAY_DESCRIPTIONS,
} from '@dfc/shared';
import { Wallet, Check, CreditCard } from 'lucide-react';
import toast from 'react-hot-toast';
import './TopupPage.css';

const QUICK_AMOUNTS = [100, 250, 500, 1000];

export default function TopupPage() {
  const { availableGateways, defaultCurrency } = useUserStore();
  const sym = CURRENCY_SYMBOLS[defaultCurrency] ?? '₽';

  const [amount, setAmount] = useState('');
  const [gateway, setGateway] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const gateways = useMemo(
    () => availableGateways.filter((g) => g.type !== 'BALANCE'),
    [availableGateways],
  );

  const handleTopup = async () => {
    const num = Number(amount);
    if (!num || num <= 0) {
      toast.error('Введите сумму');
      return;
    }
    setLoading(true);
    try {
      const res = await purchaseApi.topup({
        amount: num,
        gateway: gateway ?? gateways[0]?.type ?? '',
      });
      if (res.data.payment_url) {
        window.open(res.data.payment_url, '_blank');
      } else {
        toast.success('Баланс пополнен');
        useUserStore.getState().fetchData();
      }
    } catch (e: any) {
      toast.error(e?.response?.data?.detail ?? 'Ошибка пополнения');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="topup-page animate-in">
      <h2 className="page-title"><Wallet size={20} /> Пополнение баланса</h2>

      <div className="card">
        <label className="topup-label">Сумма ({sym})</label>
        <input
          type="number"
          className="input topup-input"
          placeholder="0"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          min={1}
          autoComplete="off"
        />
        <div className="quick-amounts">
          {QUICK_AMOUNTS.map((a) => (
            <button
              key={a}
              className={`pill ${Number(amount) === a ? 'pill-cyan' : 'pill-outline'}`}
              onClick={() => setAmount(String(a))}
            >
              {a} {sym}
            </button>
          ))}
        </div>
      </div>

      {gateways.length > 1 && (
        <div className="card">
          <div className="card-title"><CreditCard size={16} /> Способ оплаты</div>
          <div className="gateways-list">
            {gateways.map((gw) => (
              <button
                key={gw.type}
                className={`gateway-card ${gateway === gw.type ? 'gateway-active' : ''}`}
                onClick={() => setGateway(gw.type)}
              >
                <div className="gateway-info">
                  <span className="gateway-name">{GATEWAY_LABELS[gw.type] ?? gw.type}</span>
                  <span className="gateway-desc">{GATEWAY_DESCRIPTIONS[gw.type] ?? ''}</span>
                </div>
                {gateway === gw.type && <Check size={18} className="gateway-check" />}
              </button>
            ))}
          </div>
        </div>
      )}

      <button
        className="btn btn-primary btn-full btn-glossy"
        disabled={loading || !amount || Number(amount) <= 0}
        onClick={handleTopup}
      >
        {loading ? 'Обработка...' : `Пополнить ${amount ? amount + ' ' + sym : ''}`}
      </button>
    </div>
  );
}
