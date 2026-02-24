import { useEffect, useState } from 'react';
import { adminApi } from '@dfc/shared';
import { Search, User, ChevronRight, Shield, Ban, Wallet } from 'lucide-react';
import toast from 'react-hot-toast';

interface UserItem {
  telegram_id: number;
  name: string;
  username: string;
  role: string;
  is_blocked: boolean;
  balance: number;
}

export default function AdminUsers() {
  const [users, setUsers] = useState<UserItem[]>([]);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [selected, setSelected] = useState<UserItem | null>(null);
  const [loading, setLoading] = useState(false);

  const load = async (p = 1, q = '') => {
    setLoading(true);
    try {
      const { data } = await adminApi.listUsers(p, q || undefined);
      setUsers(data.users ?? data);
    } catch { /* ignore */ } finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const handleSearch = () => {
    setPage(1);
    load(1, search);
  };

  const handleBlock = async (u: UserItem) => {
    try {
      await adminApi.blockUser(u.telegram_id, !u.is_blocked);
      toast.success(u.is_blocked ? 'Разблокирован' : 'Заблокирован');
      setSelected({ ...u, is_blocked: !u.is_blocked });
      load(page, search);
    } catch { toast.error('Ошибка'); }
  };

  const handleRole = async (u: UserItem, role: string) => {
    try {
      await adminApi.setUserRole(u.telegram_id, role);
      toast.success(`Роль: ${role}`);
      setSelected({ ...u, role });
      load(page, search);
    } catch { toast.error('Ошибка'); }
  };

  if (selected) {
    return (
      <div className="admin-form">
        <button className="back-btn" onClick={() => setSelected(null)}>← Назад</button>
        <div className="card">
          <div className="card-row">
            <span className="card-label">ID</span>
            <span className="card-value">{selected.telegram_id}</span>
          </div>
          <div className="card-row">
            <span className="card-label">Имя</span>
            <span className="card-value">{selected.name}</span>
          </div>
          <div className="card-row">
            <span className="card-label">Роль</span>
            <span className="card-value">{selected.role}</span>
          </div>
          <div className="card-row">
            <span className="card-label">Баланс</span>
            <span className="card-value">{selected.balance} ₽</span>
          </div>
          <div className="card-row">
            <span className="card-label">Заблокирован</span>
            <span className="card-value">{selected.is_blocked ? 'Да' : 'Нет'}</span>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <button className="pill pill-outline" onClick={() => handleBlock(selected)}>
            <Ban size={14} /> {selected.is_blocked ? 'Разблокировать' : 'Заблокировать'}
          </button>
          {selected.role !== 'ADMIN' && (
            <button className="pill pill-outline" onClick={() => handleRole(selected, 'ADMIN')}>
              <Shield size={14} /> Сделать админом
            </button>
          )}
          {selected.role !== 'USER' && (
            <button className="pill pill-outline" onClick={() => handleRole(selected, 'USER')}>
              <User size={14} /> Сделать юзером
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="search-bar">
        <input
          type="text"
          className="input"
          placeholder="Поиск по имени или ID..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
        />
        <button className="pill pill-cyan" onClick={handleSearch}>
          <Search size={14} />
        </button>
      </div>

      {loading && <div className="empty-state">Загрузка...</div>}

      <div className="admin-list">
        {users.map((u) => (
          <div key={u.telegram_id} className="admin-list-item" onClick={() => setSelected(u)}>
            <div>
              <div className="admin-item-name">{u.name}</div>
              <div className="admin-item-sub">
                {u.telegram_id} · {u.role} {u.is_blocked ? '· 🚫' : ''}
              </div>
            </div>
            <ChevronRight size={16} color="var(--text2)" />
          </div>
        ))}
      </div>

      {users.length >= 20 && (
        <div style={{ display: 'flex', gap: 8, justifyContent: 'center' }}>
          {page > 1 && (
            <button className="pill pill-outline" onClick={() => { setPage(page - 1); load(page - 1, search); }}>
              ← Назад
            </button>
          )}
          <button className="pill pill-outline" onClick={() => { setPage(page + 1); load(page + 1, search); }}>
            Далее →
          </button>
        </div>
      )}
    </>
  );
}
