import { useState } from 'react';
import { Tag, Loader2, CheckCircle, XCircle } from 'lucide-react';
import { useUserStore, purchaseApi } from '@dfc/shared';

export default function PromoPage() {
  const { features } = useUserStore();
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ ok: boolean; message: string } | null>(null);

  if (!features?.promocodes_enabled) {
    return (
      <div className="animate-in">
        <h2 className="page-title">Промокод</h2>
        <div className="card empty-state">
          <XCircle size={32} style={{ margin: '0 auto 12px', color: 'var(--text3)' }} />
          <p className="text-muted">Промокоды отключены</p>
        </div>
      </div>
    );
  }

  const handleActivate = async () => {
    if (!code.trim() || loading) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await purchaseApi.activatePromocode(code.trim());
      setResult({ ok: true, message: res.data?.message || 'Промокод активирован!' });
      setCode('');
    } catch (e: any) {
      setResult({ ok: false, message: e?.response?.data?.detail || 'Не удалось активировать промокод' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-in" style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      <h2 className="page-title">Промокод</h2>

      <input
        className="input"
        placeholder="Введите промокод"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleActivate()}
      />

      <button className="btn btn-primary btn-full" disabled={!code.trim() || loading} onClick={handleActivate}>
        {loading ? <Loader2 size={18} className="spinner" /> : <Tag size={18} />}
        {loading ? 'Проверка...' : 'Активировать'}
      </button>

      {result && (
        <div className={`card animate-in`} style={{ borderColor: result.ok ? 'var(--green)' : 'var(--red)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            {result.ok ? <CheckCircle size={20} style={{ color: 'var(--green)' }} /> : <XCircle size={20} style={{ color: 'var(--red)' }} />}
            <span style={{ color: result.ok ? 'var(--green)' : 'var(--red)' }}>{result.message}</span>
          </div>
        </div>
      )}
    </div>
  );
}
