import { useState, useEffect } from 'react';
import { adminApi } from '@dfc/shared';
import { RefreshCw, Loader2, Server, Users, AlertCircle } from 'lucide-react';

export default function AdminMonitoring() {
  const [data, setData] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await adminApi.getMonitoring();
      setData(res.data as Record<string, unknown>);
    } catch (e: any) {
      setError(e?.response?.data?.error || e?.message || 'Ошибка соединения с Remnawave');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  if (loading) return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: 40 }}>
      <Loader2 size={28} className="spinner" />
    </div>
  );

  if (error) return (
    <div className="card" style={{ textAlign: 'center', padding: 24 }}>
      <AlertCircle size={32} style={{ color: 'var(--red)', marginBottom: 12 }} />
      <div style={{ color: 'var(--red)', fontSize: '0.9rem', marginBottom: 12 }}>{error}</div>
      <button className="btn btn-outline btn-sm" onClick={load}>
        <RefreshCw size={16} /> Повторить
      </button>
    </div>
  );

  if (!data) return null;

  const renderValue = (v: unknown): string => {
    if (v === null || v === undefined) return '—';
    if (typeof v === 'boolean') return v ? 'Да' : 'Нет';
    if (typeof v === 'object') return JSON.stringify(v, null, 2);
    return String(v);
  };

  const renderSection = (title: string, obj: Record<string, unknown>, icon: React.ReactNode) => (
    <div className="card" key={title} style={{ marginBottom: 12 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
        {icon}
        <span className="fw-600">{title}</span>
      </div>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <tbody>
          {Object.entries(obj).map(([k, v]) => {
            if (typeof v === 'object' && v !== null && !Array.isArray(v)) return null;
            if (Array.isArray(v)) return null;
            return (
              <tr key={k} style={{ borderBottom: '1px solid var(--border)' }}>
                <td style={{ padding: '6px 0', color: 'var(--text2)', fontSize: '0.82rem', width: '50%' }}>{k}</td>
                <td style={{ padding: '6px 0', fontSize: '0.85rem', textAlign: 'right' }}>{renderValue(v)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
        <span className="fw-600" style={{ fontSize: '0.95rem' }}>Remnawave</span>
        <button className="btn btn-ghost btn-sm" onClick={load}>
          <RefreshCw size={14} /> Обновить
        </button>
      </div>

      {/* Render all top-level non-array, non-nested object keys as a single card */}
      {(() => {
        const topLevel: Record<string, unknown> = {};
        const nested: [string, unknown[]][] = [];

        Object.entries(data).forEach(([k, v]) => {
          if (Array.isArray(v)) {
            nested.push([k, v as unknown[]]);
          } else if (typeof v === 'object' && v !== null) {
            // nested object section
            Object.assign(topLevel, { ...topLevel, [k]: v });
          } else {
            topLevel[k] = v;
          }
        });

        return (
          <>
            {Object.keys(topLevel).length > 0 && renderSection(
              'Система',
              topLevel,
              <Server size={18} style={{ color: 'var(--cyan)' }} />,
            )}
            {nested.map(([key, arr]) => (
              <div className="card" key={key} style={{ marginBottom: 12 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
                  <Users size={18} style={{ color: 'var(--gold)' }} />
                  <span className="fw-600">{key} ({arr.length})</span>
                </div>
                {arr.slice(0, 20).map((item, i) => (
                  <div key={i} style={{
                    padding: '8px 0',
                    borderBottom: i < arr.length - 1 ? '1px solid var(--border)' : 'none',
                    fontSize: '0.82rem',
                    color: 'var(--text2)',
                  }}>
                    {typeof item === 'object' ? (
                      Object.entries(item as Record<string, unknown>).map(([k2, v2]) => (
                        <span key={k2} style={{ marginRight: 12 }}>
                          <span style={{ color: 'var(--text3)' }}>{k2}: </span>
                          <span style={{ color: 'var(--text)' }}>{renderValue(v2)}</span>
                        </span>
                      ))
                    ) : String(item)}
                  </div>
                ))}
                {arr.length > 20 && (
                  <div style={{ color: 'var(--text3)', fontSize: '0.8rem', paddingTop: 8 }}>
                    + ещё {arr.length - 20} записей
                  </div>
                )}
              </div>
            ))}
          </>
        );
      })()}
    </div>
  );
}
