import { useState, useEffect } from 'react';
import { adminApi } from '@dfc/shared';
import type { AdminPromocode } from '@dfc/shared';
import { Plus, Trash2, ToggleLeft, ToggleRight, Loader2, RefreshCw, Tag, Shuffle } from 'lucide-react';

const REWARD_TYPES = [
  { value: 'DURATION', label: 'Дни к подписке' },
  { value: 'TRAFFIC', label: 'Трафик' },
  { value: 'DEVICES', label: 'Устройства' },
  { value: 'SUBSCRIPTION', label: 'Подписка' },
  { value: 'PERSONAL_DISCOUNT', label: 'Персональная скидка %' },
];

const AVAILABILITY = [
  { value: 'ALL', label: 'Все' },
  { value: 'NEW', label: 'Новые' },
  { value: 'EXISTING', label: 'Существующие' },
  { value: 'INVITED', label: 'Приглашённые' },
];

function generateCode(len = 10) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  return Array.from({ length: len }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
}

export default function AdminPromocodes() {
  const [promos, setPromos] = useState<AdminPromocode[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');

  const [code, setCode] = useState('');
  const [name, setName] = useState('');
  const [rewardType, setRewardType] = useState('DURATION');
  const [reward, setReward] = useState(7);
  const [lifetime, setLifetime] = useState(0);
  const [maxActivations, setMaxActivations] = useState(0);
  const [availability2, setAvailability] = useState('ALL');

  const load = async () => {
    setLoading(true);
    try {
      const { data } = await adminApi.adminListPromocodes();
      setPromos(Array.isArray(data) ? data : []);
    } catch { /* ignore */ }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    if (saving) return;
    setSaving(true);
    setError('');
    try {
      await adminApi.adminCreatePromocode({
        code: code.trim() || undefined,
        name: name.trim(),
        reward_type: rewardType,
        reward,
        availability: availability2,
        lifetime: lifetime > 0 ? lifetime : undefined,
        max_activations: maxActivations > 0 ? maxActivations : undefined,
      });
      setShowForm(false);
      setCode('');
      setName('');
      setReward(7);
      setLifetime(0);
      setMaxActivations(0);
      await load();
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Ошибка создания');
    } finally {
      setSaving(false);
    }
  };

  const handleToggle = async (id: number) => {
    try {
      const { data } = await adminApi.adminTogglePromocode(id);
      setPromos(prev => prev.map(p => p.id === id ? data : p));
    } catch { /* ignore */ }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Удалить промокод?')) return;
    try {
      await adminApi.adminDeletePromocode(id);
      setPromos(prev => prev.filter(p => p.id !== id));
    } catch { /* ignore */ }
  };

  const filtered = promos.filter(p =>
    !search || p.code.toLowerCase().includes(search.toLowerCase()) || p.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      {/* Toolbar */}
      <div style={{ display: 'flex', gap: 8 }}>
        <input
          className="input"
          placeholder="Поиск..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{ flex: 1, fontSize: '0.85rem', padding: '8px 12px' }}
        />
        <button className="btn btn-primary btn-sm" onClick={() => setShowForm(!showForm)}>
          <Plus size={16} />
        </button>
        <button className="btn btn-ghost btn-sm" onClick={load}>
          <RefreshCw size={14} />
        </button>
      </div>

      {/* Create form */}
      {showForm && (
        <div className="card">
          <div className="fw-600" style={{ marginBottom: 14 }}>Новый промокод</div>

          <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
            <input
              className="input"
              placeholder="Код (авто)"
              style={{ flex: 1, fontSize: '0.85rem' }}
              value={code}
              onChange={e => setCode(e.target.value.toUpperCase())}
            />
            <button className="btn btn-ghost btn-sm" onClick={() => setCode(generateCode())} title="Сгенерировать">
              <Shuffle size={14} />
            </button>
          </div>

          <div className="form-group">
            <label className="form-label">Название</label>
            <input className="input" placeholder="Название промокода" value={name} onChange={e => setName(e.target.value)} />
          </div>

          <div className="form-group">
            <label className="form-label">Тип награды</label>
            <select className="input" value={rewardType} onChange={e => setRewardType(e.target.value)}>
              {REWARD_TYPES.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">
              Значение {rewardType === 'PERSONAL_DISCOUNT' ? '(%)' : rewardType === 'DURATION' ? '(дней)' : ''}
            </label>
            <input
              className="input"
              type="number"
              min={1}
              value={reward}
              onChange={e => setReward(Number(e.target.value))}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 12 }}>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label">Срок (дней, 0=бессрочно)</label>
              <input className="input" type="number" min={0} value={lifetime} onChange={e => setLifetime(Number(e.target.value))} />
            </div>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label">Макс. активаций (0=∞)</label>
              <input className="input" type="number" min={0} value={maxActivations} onChange={e => setMaxActivations(Number(e.target.value))} />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Доступность</label>
            <select className="input" value={availability2} onChange={e => setAvailability(e.target.value)}>
              {AVAILABILITY.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          </div>

          {error && <div className="text-red" style={{ fontSize: '0.85rem', marginBottom: 10 }}>{error}</div>}

          <div style={{ display: 'flex', gap: 8 }}>
            <button className="btn btn-ghost" onClick={() => { setShowForm(false); setError(''); }}>Отмена</button>
            <button className="btn btn-primary" style={{ flex: 1 }} onClick={handleCreate} disabled={saving}>
              {saving ? <Loader2 size={16} className="spinner" /> : <Plus size={16} />}
              Создать
            </button>
          </div>
        </div>
      )}

      {/* List */}
      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: 32 }}>
          <Loader2 size={24} className="spinner" />
        </div>
      ) : filtered.length === 0 ? (
        <div className="card empty-state" style={{ padding: 32, textAlign: 'center' }}>
          <Tag size={32} style={{ color: 'var(--text3)', marginBottom: 12 }} />
          <div className="text-muted">Нет промокодов</div>
        </div>
      ) : (
        filtered.map(p => (
          <div key={p.id} className="card" style={{ padding: '10px 14px', display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span className="fw-600" style={{ fontSize: '0.9rem', fontFamily: 'var(--font-mono)' }}>{p.code}</span>
                {p.is_expired && <span className="badge" style={{ background: 'var(--red)', fontSize: '0.7rem' }}>истёк</span>}
                {p.is_depleted && <span className="badge" style={{ background: 'var(--orange)', fontSize: '0.7rem' }}>исчерпан</span>}
              </div>
              {p.name && <div className="text-muted" style={{ fontSize: '0.78rem' }}>{p.name}</div>}
              <div style={{ fontSize: '0.75rem', color: 'var(--text3)', marginTop: 2 }}>
                {REWARD_TYPES.find(r => r.value === p.reward_type)?.label} · {p.reward}
                {p.max_activations ? ` · ${p.activations_count}/${p.max_activations}` : ` · ${p.activations_count} активаций`}
              </div>
            </div>
            <button className="btn btn-ghost btn-sm" onClick={() => handleToggle(p.id)} style={{ padding: '4px 6px' }}>
              {p.is_active
                ? <ToggleRight size={22} style={{ color: 'var(--green)' }} />
                : <ToggleLeft size={22} style={{ color: 'var(--text3)' }} />
              }
            </button>
            <button className="btn btn-ghost btn-sm" onClick={() => handleDelete(p.id)} style={{ padding: '4px 6px', color: 'var(--red)' }}>
              <Trash2 size={16} />
            </button>
          </div>
        ))
      )}
    </div>
  );
}
