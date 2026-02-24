import { useState } from 'react';
import { purchaseApi } from '@dfc/shared';
import { Gift, Send, CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import './PromoPage.css';

export default function PromoPage() {
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleActivate = async () => {
    const trimmed = code.trim();
    if (!trimmed) {
      toast.error('Введите промокод');
      return;
    }
    setLoading(true);
    try {
      await purchaseApi.activatePromocode(trimmed);
      setSuccess(true);
      toast.success('Промокод активирован!');
    } catch (e: any) {
      toast.error(e?.response?.data?.detail ?? 'Неверный промокод');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="promo-page animate-in">
      <h2 className="page-title"><Gift size={20} /> Промокод</h2>

      {success ? (
        <div className="card promo-success">
          <CheckCircle size={48} className="promo-success-icon" />
          <div className="promo-success-text">Промокод успешно активирован!</div>
          <button
            className="btn btn-primary btn-full"
            onClick={() => { setSuccess(false); setCode(''); }}
          >
            Ввести ещё
          </button>
        </div>
      ) : (
        <div className="card">
          <p className="promo-hint">
            Введите промокод, чтобы получить бонус или скидку
          </p>
          <div className="promo-input-row">
            <input
              type="text"
              className="input promo-input"
              placeholder="PROMO-CODE"
              value={code}
              onChange={(e) => setCode(e.target.value.toUpperCase())}
              onKeyDown={(e) => e.key === 'Enter' && handleActivate()}
              autoComplete="off"
              autoCapitalize="characters"
            />
            <button
              className="btn btn-primary btn-glossy promo-btn"
              disabled={loading || !code.trim()}
              onClick={handleActivate}
            >
              {loading ? '...' : <Send size={18} />}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
