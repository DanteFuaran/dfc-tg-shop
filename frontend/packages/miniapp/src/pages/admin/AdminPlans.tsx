import { useState, useEffect } from 'react';
import { Plus, Pencil, Trash2, X, ToggleLeft, ToggleRight, Wifi, Smartphone, Clock, Tag } from 'lucide-react';
import { useAdminStore, formatPrice, CURRENCY_SYMBOLS } from '@dfc/shared';
import type { Plan, PlanDuration, PlanPrice } from '@dfc/shared';

interface PlanForm {
  name: string;
  description: string;
  type: string;
  tag: string;
  traffic_limit: string;
  device_limit: string;
  durations: { days: string; prices: { currency: string; amount: string }[] }[];
}

const EMPTY_FORM: PlanForm = {
  name: '',
  description: '',
  type: 'default',
  tag: '',
  traffic_limit: '',
  device_limit: '1',
  durations: [{ days: '30', prices: [{ currency: 'RUB', amount: '' }] }],
};

const CURRENCIES = ['RUB', 'USD', 'EUR', 'XTR'];
const PLAN_TYPES = ['default', 'premium', 'trial', 'custom'];

function formFromPlan(plan: Plan): PlanForm {
  return {
    name: plan.name,
    description: plan.description || '',
    type: plan.type || 'default',
    tag: plan.tag || '',
    traffic_limit: plan.traffic_limit != null ? String(plan.traffic_limit) : '',
    device_limit: plan.device_limit != null ? String(plan.device_limit) : '1',
    durations: plan.durations.map((d) => ({
      days: String(d.days),
      prices: d.prices.map((p) => ({ currency: p.currency, amount: String(p.amount) })),
    })),
  };
}

function formToPayload(form: PlanForm) {
  return {
    name: form.name,
    description: form.description || undefined,
    type: form.type,
    tag: form.tag || undefined,
    traffic_limit: form.traffic_limit ? Number(form.traffic_limit) : null,
    device_limit: form.device_limit ? Number(form.device_limit) : 1,
    durations: form.durations.map((d) => ({
      days: Number(d.days),
      prices: d.prices.filter((p) => p.amount).map((p) => ({
        currency: p.currency,
        amount: p.amount,
      })),
    })),
  };
}

export default function AdminPlans() {
  const { plans, isLoading, fetchPlans, createPlan, updatePlan, deletePlan, togglePlan } = useAdminStore();

  const [modalOpen, setModalOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState<PlanForm>(EMPTY_FORM);
  const [confirmDeleteId, setConfirmDeleteId] = useState<number | null>(null);
  const [toast, setToast] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  useEffect(() => { fetchPlans(); }, []);

  const showToast = (text: string, type: 'success' | 'error' = 'success') => {
    setToast({ text, type });
    setTimeout(() => setToast(null), 3000);
  };

  /* ── modal helpers ── */
  const openCreate = () => {
    setEditingId(null);
    setForm(EMPTY_FORM);
    setModalOpen(true);
  };

  const openEdit = (plan: Plan) => {
    setEditingId(plan.id);
    setForm(formFromPlan(plan));
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setEditingId(null);
  };

  /* ── form handlers ── */
  const setField = (key: keyof PlanForm, val: string) =>
    setForm((prev) => ({ ...prev, [key]: val }));

  const setDurationDays = (idx: number, val: string) =>
    setForm((prev) => {
      const durations = [...prev.durations];
      durations[idx] = { ...durations[idx]!, days: val };
      return { ...prev, durations };
    });

  const setDurationPrice = (dIdx: number, pIdx: number, key: 'currency' | 'amount', val: string) =>
    setForm((prev) => {
      const durations = [...prev.durations];
      const prices = [...durations[dIdx]!.prices];
      prices[pIdx] = { ...prices[pIdx]!, [key]: val };
      durations[dIdx] = { ...durations[dIdx]!, prices };
      return { ...prev, durations };
    });

  const addDuration = () =>
    setForm((prev) => ({
      ...prev,
      durations: [...prev.durations, { days: '30', prices: [{ currency: 'RUB', amount: '' }] }],
    }));

  const removeDuration = (idx: number) =>
    setForm((prev) => ({
      ...prev,
      durations: prev.durations.filter((_, i) => i !== idx),
    }));

  const addPrice = (dIdx: number) =>
    setForm((prev) => {
      const durations = [...prev.durations];
      durations[dIdx] = {
        ...durations[dIdx]!,
        prices: [...durations[dIdx]!.prices, { currency: 'USD', amount: '' }],
      };
      return { ...prev, durations };
    });

  const removePrice = (dIdx: number, pIdx: number) =>
    setForm((prev) => {
      const durations = [...prev.durations];
      durations[dIdx] = {
        ...durations[dIdx]!,
        prices: durations[dIdx]!.prices.filter((_, i) => i !== pIdx),
      };
      return { ...prev, durations };
    });

  /* ── CRUD ── */
  const handleSave = async () => {
    try {
      const payload = formToPayload(form);
      if (editingId) {
        await updatePlan(editingId, payload);
        showToast('Тариф обновлён');
      } else {
        await createPlan(payload);
        showToast('Тариф создан');
      }
      closeModal();
    } catch {
      showToast('Ошибка сохранения', 'error');
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deletePlan(id);
      setConfirmDeleteId(null);
      showToast('Тариф удалён');
    } catch {
      showToast('Ошибка удаления', 'error');
    }
  };

  const handleToggle = async (id: number) => {
    try {
      await togglePlan(id);
    } catch {
      showToast('Ошибка переключения', 'error');
    }
  };

  const formatTraffic = (limit: number | null | undefined) => {
    if (limit == null || limit === 0) return '∞';
    if (limit >= 1024) return `${(limit / 1024).toFixed(limit % 1024 === 0 ? 0 : 1)} ТБ`;
    return `${limit} ГБ`;
  };

  /* ── render ── */
  if (isLoading && plans.length === 0) {
    return <div className="loading"><span className="spinner" /> Загрузка тарифов…</div>;
  }

  return (
    <div className="animate-in" style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 className="page-title" style={{ margin: 0 }}>Тарифы</h2>
        <button className="btn btn-primary btn-sm" onClick={openCreate}>
          <Plus size={15} /> Создать тариф
        </button>
      </div>

      {/* Plan list */}
      {plans.map((plan) => (
        <div key={plan.id} className="card">
          {/* Name + badge */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
            <span className="fw-600" style={{ fontSize: '1rem' }}>{plan.name}</span>
            <span className={`badge ${plan.is_active !== false ? 'badge-green' : 'badge-red'}`}>
              {plan.is_active !== false ? 'Активен' : 'Неактивен'}
            </span>
            {plan.tag && <span className="badge badge-gold"><Tag size={10} style={{ marginRight: 2 }} />{plan.tag}</span>}
          </div>

          {/* Description */}
          {plan.description && (
            <p className="truncate" style={{ color: 'var(--text2)', fontSize: '0.83rem', marginBottom: 10, maxWidth: '100%' }}>
              {plan.description}
            </p>
          )}

          {/* Info */}
          <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap', fontSize: '0.83rem', color: 'var(--text2)', marginBottom: 10 }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <Wifi size={13} /> {formatTraffic(plan.traffic_limit)}
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <Smartphone size={13} /> {plan.device_limit ?? '∞'}
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <Clock size={13} /> {plan.durations.length} период{plan.durations.length > 1 ? 'ов' : ''}
            </span>
            <span style={{ color: 'var(--text3)' }}>тип: {plan.type || 'default'}</span>
          </div>

          {/* Actions */}
          <div style={{ display: 'flex', gap: 8 }}>
            <button className="btn btn-secondary btn-sm" onClick={() => handleToggle(plan.id)} title="Вкл/Выкл">
              {plan.is_active !== false
                ? <ToggleRight size={16} color="var(--green)" />
                : <ToggleLeft size={16} color="var(--text3)" />}
            </button>
            <button className="btn btn-secondary btn-sm" onClick={() => openEdit(plan)}>
              <Pencil size={14} /> Изменить
            </button>
            {confirmDeleteId === plan.id ? (
              <>
                <button className="btn btn-danger btn-sm" onClick={() => handleDelete(plan.id)}>Да, удалить</button>
                <button className="btn btn-secondary btn-sm" onClick={() => setConfirmDeleteId(null)}>Отмена</button>
              </>
            ) : (
              <button className="btn btn-secondary btn-sm" onClick={() => setConfirmDeleteId(plan.id)} style={{ color: 'var(--red)' }}>
                <Trash2 size={14} />
              </button>
            )}
          </div>
        </div>
      ))}

      {plans.length === 0 && <div className="empty-state">Нет тарифов. Создайте первый!</div>}

      {/* Create / Edit Modal */}
      {modalOpen && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxHeight: '85vh', overflowY: 'auto' }}>
            <div className="modal-header">
              <h3>{editingId ? 'Редактировать тариф' : 'Новый тариф'}</h3>
              <button className="modal-close" onClick={closeModal}><X size={20} /></button>
            </div>

            {/* Name */}
            <div className="form-group">
              <label className="form-label">Название</label>
              <input className="input" value={form.name} onChange={(e) => setField('name', e.target.value)} placeholder="Название тарифа" />
            </div>

            {/* Description */}
            <div className="form-group">
              <label className="form-label">Описание</label>
              <textarea className="input" value={form.description} onChange={(e) => setField('description', e.target.value)} placeholder="Описание" rows={2} style={{ resize: 'vertical' }} />
            </div>

            {/* Type */}
            <div className="form-group">
              <label className="form-label">Тип</label>
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                {PLAN_TYPES.map((t) => (
                  <button key={t} className={`pill ${form.type === t ? 'pill-filled' : 'pill-outline'}`} onClick={() => setField('type', t)}>
                    {t}
                  </button>
                ))}
              </div>
            </div>

            {/* Tag */}
            <div className="form-group">
              <label className="form-label">Тег (опционально)</label>
              <input className="input" value={form.tag} onChange={(e) => setField('tag', e.target.value)} placeholder="Например: HOT" />
            </div>

            {/* Traffic limit */}
            <div className="form-group">
              <label className="form-label">Лимит трафика (ГБ, пусто = безлимит)</label>
              <input className="input" type="number" value={form.traffic_limit} onChange={(e) => setField('traffic_limit', e.target.value)} placeholder="Безлимит" />
            </div>

            {/* Device limit */}
            <div className="form-group">
              <label className="form-label">Лимит устройств</label>
              <input className="input" type="number" value={form.device_limit} onChange={(e) => setField('device_limit', e.target.value)} placeholder="1" />
            </div>

            {/* Durations */}
            <div className="form-group">
              <label className="form-label" style={{ marginBottom: 10 }}>Периоды</label>
              {form.durations.map((dur, dIdx) => (
                <div key={dIdx} className="card" style={{ marginBottom: 10, padding: 12 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                    <input className="input" type="number" value={dur.days} onChange={(e) => setDurationDays(dIdx, e.target.value)} placeholder="Дней" style={{ width: 90 }} />
                    <span className="text-muted" style={{ fontSize: '0.83rem' }}>дней</span>
                    {form.durations.length > 1 && (
                      <button className="btn btn-secondary btn-sm" style={{ marginLeft: 'auto', color: 'var(--red)', padding: '4px 8px' }} onClick={() => removeDuration(dIdx)}>
                        <X size={14} />
                      </button>
                    )}
                  </div>

                  {/* Prices */}
                  {dur.prices.map((pr, pIdx) => (
                    <div key={pIdx} className="form-row" style={{ marginBottom: 6 }}>
                      <select className="input" value={pr.currency} onChange={(e) => setDurationPrice(dIdx, pIdx, 'currency', e.target.value)} style={{ width: 80 }}>
                        {CURRENCIES.map((c) => <option key={c} value={c}>{c}</option>)}
                      </select>
                      <input className="input" type="number" value={pr.amount} onChange={(e) => setDurationPrice(dIdx, pIdx, 'amount', e.target.value)} placeholder="Цена" style={{ flex: 1 }} />
                      {dur.prices.length > 1 && (
                        <button className="btn btn-secondary btn-sm" style={{ color: 'var(--red)', padding: '4px 8px' }} onClick={() => removePrice(dIdx, pIdx)}>
                          <X size={12} />
                        </button>
                      )}
                    </div>
                  ))}
                  <button className="btn btn-outline btn-sm" style={{ marginTop: 4, fontSize: '0.78rem' }} onClick={() => addPrice(dIdx)}>
                    <Plus size={12} /> Валюта
                  </button>
                </div>
              ))}
              <button className="btn btn-outline btn-sm" onClick={addDuration}>
                <Plus size={14} /> Добавить период
              </button>
            </div>

            {/* Save */}
            <button className="btn btn-primary btn-full" onClick={handleSave} disabled={!form.name || form.durations.length === 0}>
              {editingId ? 'Сохранить изменения' : 'Создать тариф'}
            </button>
          </div>
        </div>
      )}

      {/* Toast */}
      {toast && (
        <div className={`toast ${toast.type === 'error' ? 'toast-error' : 'toast-success'}`}>
          {toast.text}
        </div>
      )}
    </div>
  );
}
