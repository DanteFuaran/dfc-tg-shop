import { useEffect, useState } from 'react';
import { useAdminStore } from '@dfc/shared';
import type { Plan } from '@dfc/shared';
import { Plus, Edit3, Trash2, ToggleLeft, ToggleRight } from 'lucide-react';
import toast from 'react-hot-toast';

export default function AdminPlans() {
  const { plans, fetchPlans, createPlan, updatePlan, deletePlan, togglePlan } = useAdminStore();
  const [editing, setEditing] = useState<Partial<Plan> | null>(null);
  const [isNew, setIsNew] = useState(false);

  useEffect(() => { fetchPlans(); }, [fetchPlans]);

  const handleSave = async () => {
    if (!editing) return;
    try {
      if (isNew) {
        await createPlan(editing);
        toast.success('Тариф создан');
      } else {
        await updatePlan(editing.id!, editing);
        toast.success('Тариф обновлён');
      }
      setEditing(null);
    } catch { toast.error('Ошибка'); }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Удалить тариф?')) return;
    try {
      await deletePlan(id);
      toast.success('Удалён');
    } catch { toast.error('Ошибка'); }
  };

  const handleToggle = async (id: number) => {
    try {
      await togglePlan(id);
      toast.success('Статус изменён');
    } catch { toast.error('Ошибка'); }
  };

  if (editing) {
    return (
      <div className="admin-form">
        <button className="back-btn" onClick={() => setEditing(null)}>← Назад</button>
        <div className="card">
          <label className="admin-form-label">Название</label>
          <input
            className="input"
            value={editing.name ?? ''}
            onChange={(e) => setEditing({ ...editing, name: e.target.value })}
          />
          <label className="admin-form-label" style={{ marginTop: 8 }}>Описание</label>
          <textarea
            className="input"
            rows={3}
            value={editing.description ?? ''}
            onChange={(e) => setEditing({ ...editing, description: e.target.value })}
          />
          <label className="admin-form-label" style={{ marginTop: 8 }}>Лимит трафика (GB, 0 = безлимит)</label>
          <input
            className="input"
            type="number"
            value={editing.traffic_limit ?? 0}
            onChange={(e) => setEditing({ ...editing, traffic_limit: Number(e.target.value) || null })}
          />
          <label className="admin-form-label" style={{ marginTop: 8 }}>Лимит устройств (0 = безлимит)</label>
          <input
            className="input"
            type="number"
            value={editing.device_limit ?? 0}
            onChange={(e) => setEditing({ ...editing, device_limit: Number(e.target.value) || null })}
          />
          <label className="admin-form-label" style={{ marginTop: 8 }}>Тег</label>
          <input
            className="input"
            value={editing.tag ?? ''}
            onChange={(e) => setEditing({ ...editing, tag: e.target.value })}
          />
        </div>
        <button className="btn btn-primary btn-full btn-glossy" onClick={handleSave}>
          {isNew ? 'Создать' : 'Сохранить'}
        </button>
      </div>
    );
  }

  return (
    <>
      <button
        className="pill pill-cyan"
        onClick={() => { setEditing({ name: '', description: '' }); setIsNew(true); }}
      >
        <Plus size={14} /> Новый тариф
      </button>

      <div className="admin-list">
        {plans.map((p) => (
          <div key={p.id} className="admin-list-item">
            <div style={{ flex: 1 }}>
              <div className="admin-item-name">
                {p.name}
                {p.is_active === false && <span style={{ color: 'var(--text2)', fontSize: 11 }}> (выкл)</span>}
              </div>
              <div className="admin-item-sub">
                {p.durations.length} период(ов) · {p.device_limit ?? '∞'} устр.
              </div>
            </div>
            <div style={{ display: 'flex', gap: 6 }}>
              <button
                className="pill pill-outline"
                style={{ padding: '4px 8px' }}
                onClick={(e) => { e.stopPropagation(); handleToggle(p.id); }}
              >
                {p.is_active !== false ? <ToggleRight size={16} color="var(--cyan)" /> : <ToggleLeft size={16} />}
              </button>
              <button
                className="pill pill-outline"
                style={{ padding: '4px 8px' }}
                onClick={(e) => { e.stopPropagation(); setEditing(p); setIsNew(false); }}
              >
                <Edit3 size={14} />
              </button>
              <button
                className="pill pill-outline"
                style={{ padding: '4px 8px' }}
                onClick={(e) => { e.stopPropagation(); handleDelete(p.id); }}
              >
                <Trash2 size={14} color="#ef5350" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
