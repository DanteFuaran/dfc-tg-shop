import { useState, useEffect, useCallback, useRef } from 'react';
import { adminApi, formatPrice, useUserStore, CURRENCY_SYMBOLS } from '@dfc/shared';
import { Search, Loader, Ban, ShieldCheck, Wallet, Gift } from 'lucide-react';

interface UserItem {
  telegram_id: number;
  name?: string;
  username?: string;
  role: string;
  balance: number;
  bonus_balance?: number;
  is_blocked: boolean;
}

const ROLE_CLASS: Record<string, string> = { DEV: 'role-dev', ADMIN: 'role-admin', USER: 'role-user' };
const ROLES = ['USER', 'ADMIN', 'DEV'];

export default function AdminUsers() {
  const { defaultCurrency } = useUserStore();
  const currency = defaultCurrency || 'RUB';
  const sym = CURRENCY_SYMBOLS[currency] ?? '₽';

  const [users, setUsers] = useState<UserItem[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState<number | null>(null);
  const [balanceInput, setBalanceInput] = useState('');
  const [bonusInput, setBonusInput] = useState('');
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const load = useCallback(async (q: string) => {
    setLoading(true);
    try {
      const res = await adminApi.listUsers(1, q || undefined);
      setUsers(Array.isArray(res.data) ? res.data : (res.data as any).users ?? []);
    } catch { /* ignore */ }
    setLoading(false);
  }, []);

  useEffect(() => { load(search); }, []);

  const handleSearch = (val: string) => {
    setSearch(val);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => load(val), 400);
  };

  const handleRole = async (tid: number, role: string) => {
    await adminApi.setUserRole(tid, role);
    load(search);
  };

  const handleAddBalance = async (tid: number) => {
    const v = parseFloat(balanceInput);
    if (!v) return;
    await adminApi.addBalance(tid, v);
    setBalanceInput('');
    load(search);
  };

  const handleAddBonus = async (tid: number) => {
    const v = parseFloat(bonusInput);
    if (!v) return;
    await adminApi.addBonusBalance(tid, v);
    setBonusInput('');
    load(search);
  };

  const handleBlock = async (tid: number, is_blocked: boolean) => {
    await adminApi.blockUser(tid, !is_blocked);
    load(search);
  };

  const toggle = (tid: number) => {
    setExpanded(expanded === tid ? null : tid);
    setBalanceInput('');
    setBonusInput('');
  };

  return (
    <div>
      <div className="search-bar">
        <Search size={18} />
        <input
          type="text"
          placeholder="Поиск по имени / username / ID"
          value={search}
          onChange={(e) => handleSearch(e.target.value)}
        />
      </div>

      {loading ? (
        <div className="empty-state"><Loader size={32} className="spinner" /></div>
      ) : users.length === 0 ? (
        <div className="empty-state">Пользователи не найдены</div>
      ) : (
        <div className="card-list">
          {users.map((u) => (
            <div className="card" key={u.telegram_id}>
              <div className="card-row" onClick={() => toggle(u.telegram_id)} style={{ cursor: 'pointer' }}>
                <div>
                  <strong>{u.name || 'Без имени'}</strong>
                  {u.username && <span style={{ opacity: 0.6, marginLeft: 6 }}>@{u.username}</span>}
                  <div style={{ fontSize: 12, opacity: 0.5 }}>ID: {u.telegram_id}</div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span className={ROLE_CLASS[u.role] ?? 'role-user'}>{u.role}</span>
                  {u.is_blocked && <Ban size={14} style={{ color: 'var(--red)' }} />}
                </div>
              </div>

              {expanded === u.telegram_id && (
                <div className="card-detail" style={{ padding: '12px 0 0' }}>
                  <div style={{ marginBottom: 8, fontSize: 13, opacity: 0.7 }}>
                    Баланс: {formatPrice(u.balance)} {sym} &nbsp;|&nbsp; Бонус: {formatPrice(u.bonus_balance ?? 0)} {sym}
                  </div>

                  <div style={{ marginBottom: 10 }}>
                    <label style={{ fontSize: 12, opacity: 0.6 }}>Роль</label>
                    <select
                      className="input"
                      value={u.role}
                      onChange={(e) => handleRole(u.telegram_id, e.target.value)}
                    >
                      {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
                    </select>
                  </div>

                  <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
                    <input
                      className="input"
                      type="number"
                      placeholder={`Баланс (${sym})`}
                      value={balanceInput}
                      onChange={(e) => setBalanceInput(e.target.value)}
                      style={{ flex: 1 }}
                    />
                    <button className="btn btn-sm" onClick={() => handleAddBalance(u.telegram_id)}>
                      <Wallet size={14} /> Начислить
                    </button>
                  </div>

                  <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
                    <input
                      className="input"
                      type="number"
                      placeholder={`Бонус (${sym})`}
                      value={bonusInput}
                      onChange={(e) => setBonusInput(e.target.value)}
                      style={{ flex: 1 }}
                    />
                    <button className="btn btn-sm" onClick={() => handleAddBonus(u.telegram_id)}>
                      <Gift size={14} /> Начислить
                    </button>
                  </div>

                  <button
                    className={`btn btn-sm ${u.is_blocked ? 'btn-success' : 'btn-danger'}`}
                    onClick={() => handleBlock(u.telegram_id, u.is_blocked)}
                    style={{ width: '100%' }}
                  >
                    {u.is_blocked ? <><ShieldCheck size={14} /> Разблокировать</> : <><Ban size={14} /> Заблокировать</>}
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div style={{ fontSize: 12, opacity: 0.5, textAlign: 'center', marginTop: 8 }}>
        Всего: {users.length}
      </div>
    </div>
  );
}
