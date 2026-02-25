import { useState, useEffect } from 'react';
import { adminApi } from '@dfc/shared';
import type { AdminBroadcast } from '@dfc/shared';
import { Send, Trash2, Loader2, RefreshCw, Radio, CheckCircle, XCircle, Clock, AlertCircle } from 'lucide-react';

const AUDIENCE_OPTIONS = [
  { value: 'ALL', label: 'Все пользователи' },
  { value: 'SUBSCRIBED', label: 'С активной подпиской' },
  { value: 'UNSUBSCRIBED', label: 'Без подписки' },
  { value: 'EXPIRED', label: 'С истёкшей подпиской' },
  { value: 'TRIAL', label: 'С триальной подпиской' },
];

const STATUS_ICON: Record<string, React.ReactNode> = {
  PROCESSING: <Clock size={14} style={{ color: 'var(--gold)' }} />,
  COMPLETED: <CheckCircle size={14} style={{ color: 'var(--green)' }} />,
  CANCELED: <XCircle size={14} style={{ color: 'var(--text3)' }} />,
  ERROR: <AlertCircle size={14} style={{ color: 'var(--red)' }} />,
  DELETED: <Trash2 size={14} style={{ color: 'var(--text3)' }} />,
};

const STATUS_LABEL: Record<string, string> = {
  PROCESSING: 'В процессе',
  COMPLETED: 'Завершена',
  CANCELED: 'Отменена',
  ERROR: 'Ошибка',
  DELETED: 'Удалена',
};

export default function AdminBroadcast() {
  const [broadcasts, setBroadcasts] = useState<AdminBroadcast[]>([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [text, setText] = useState('');
  const [audience, setAudience] = useState('ALL');
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    try {
      const { data } = await adminApi.listBroadcasts();
      setBroadcasts(Array.isArray(data) ? data : []);
    } catch {
      /* ignore */
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    if (!text.trim() || creating) return;
    setCreating(true);
    setError('');
    try {
      await adminApi.createBroadcast({ text: text.trim(), audience });
      setText('');
      setAudience('ALL');
      setShowForm(false);
      await load();
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Ошибка создания рассылки');
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Удалить рассылку?')) return;
    try {
      await adminApi.deleteBroadcast(id);
      setBroadcasts(prev => prev.filter(b => b.id !== id));
    } catch {
      /* ignore */
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      {/* Toolbar */}
      <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
        <button className="btn btn-primary btn-sm" onClick={() => setShowForm(!showForm)} style={{ flex: 1 }}>
          <Radio size={16} /> Новая рассылка
        </button>
        <button className="btn btn-ghost btn-sm" onClick={load}>
          <RefreshCw size={14} />
        </button>
      </div>

      {/* Create form */}
      {showForm && (
        <div className="card">
          <div className="fw-600" style={{ marginBottom: 12 }}>Новая рассылка</div>

          <div className="form-group">
            <label className="form-label">Аудитория</label>
            <select className="input" value={audience} onChange={e => setAudience(e.target.value)}>
              {AUDIENCE_OPTIONS.map(o => (
                <option key={o.value} value={o.value}>{o.label}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Текст сообщения</label>
            <textarea
              className="input"
              placeholder="Введите текст рассылки..."
              rows={5}
              style={{ resize: 'vertical' }}
              value={text}
              onChange={e => setText(e.target.value)}
            />
          </div>

          {error && <div className="text-red" style={{ fontSize: '0.85rem', marginBottom: 10 }}>{error}</div>}

          <div style={{ display: 'flex', gap: 8 }}>
            <button className="btn btn-ghost" onClick={() => { setShowForm(false); setError(''); }}>
              Отмена
            </button>
            <button
              className="btn btn-primary"
              style={{ flex: 1 }}
              disabled={!text.trim() || creating}
              onClick={handleCreate}
            >
              {creating ? <Loader2 size={16} className="spinner" /> : <Send size={16} />}
              {creating ? 'Отправка...' : 'Запустить'}
            </button>
          </div>
        </div>
      )}

      {/* Broadcasts list */}
      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: 32 }}>
          <Loader2 size={24} className="spinner" />
        </div>
      ) : broadcasts.length === 0 ? (
        <div className="card empty-state" style={{ padding: 32, textAlign: 'center' }}>
          <Radio size={32} style={{ color: 'var(--text3)', marginBottom: 12 }} />
          <div className="text-muted">Нет рассылок</div>
        </div>
      ) : (
        broadcasts.map(b => (
          <div key={b.id} className="card" style={{ padding: '12px 14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6 }}>
              {STATUS_ICON[b.status] || <Clock size={14} />}
              <span className="fw-600" style={{ fontSize: '0.85rem' }}>{STATUS_LABEL[b.status] || b.status}</span>
              <span style={{ flex: 1 }} />
              <span className="text-muted" style={{ fontSize: '0.75rem' }}>{b.created_at}</span>
            </div>

            <div style={{ fontSize: '0.83rem', color: 'var(--text2)', marginBottom: 8 }}>
              Аудитория: {b.audience} · Всего: {b.total_count}
              {b.status !== 'PROCESSING' && (
                <> · ✅ {b.success_count} · ❌ {b.failed_count}</>
              )}
            </div>

            {b.text && (
              <div style={{
                fontSize: '0.82rem',
                color: 'var(--text)',
                background: 'var(--bg-input)',
                borderRadius: 6,
                padding: '6px 10px',
                marginBottom: 8,
                maxHeight: 60,
                overflow: 'hidden',
                textOverflow: 'ellipsis',
              }}>
                {b.text.length > 120 ? b.text.slice(0, 120) + '…' : b.text}
              </div>
            )}

            {b.status !== 'PROCESSING' && (
              <button
                className="btn btn-ghost btn-sm"
                style={{ color: 'var(--red)', padding: '4px 8px' }}
                onClick={() => handleDelete(b.id)}
              >
                <Trash2 size={14} /> Удалить
              </button>
            )}
          </div>
        ))
      )}
    </div>
  );
}
