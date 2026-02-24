import { useState } from 'react';
import { Shield } from 'lucide-react';
import AdminStats from './admin/AdminStats';
import AdminUsers from './admin/AdminUsers';
import AdminPlans from './admin/AdminPlans';
import AdminSettings from './admin/AdminSettings';
import AdminTickets from './admin/AdminTickets';
import AdminBrand from './admin/AdminBrand';
import './AdminPage.css';

const TABS = [
  { id: 'stats', label: 'Статистика' },
  { id: 'users', label: 'Пользователи' },
  { id: 'plans', label: 'Тарифы' },
  { id: 'settings', label: 'Настройки' },
  { id: 'tickets', label: 'Тикеты' },
  { id: 'brand', label: 'Бренд' },
] as const;

type TabId = typeof TABS[number]['id'];

export default function AdminPage() {
  const [tab, setTab] = useState<TabId>('stats');

  return (
    <div className="admin-page animate-in">
      <h2 className="page-title"><Shield size={20} /> Админ-панель</h2>

      <div className="admin-tabs">
        {TABS.map((t) => (
          <button
            key={t.id}
            className={`admin-tab ${tab === t.id ? 'admin-tab-active' : ''}`}
            onClick={() => setTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="admin-content">
        {tab === 'stats' && <AdminStats />}
        {tab === 'users' && <AdminUsers />}
        {tab === 'plans' && <AdminPlans />}
        {tab === 'settings' && <AdminSettings />}
        {tab === 'tickets' && <AdminTickets />}
        {tab === 'brand' && <AdminBrand />}
      </div>
    </div>
  );
}
