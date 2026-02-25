import { useState } from 'react';
import { useUserStore } from '@dfc/shared';
import { Shield } from 'lucide-react';
import AdminStats from './admin/AdminStats';
import AdminUsers from './admin/AdminUsers';
import AdminPlans from './admin/AdminPlans';
import AdminSettings from './admin/AdminSettings';
import AdminTickets from './admin/AdminTickets';
import AdminBrand from './admin/AdminBrand';

const tabs = [
  { id: 'stats', label: 'Статистика' },
  { id: 'users', label: 'Пользователи' },
  { id: 'plans', label: 'Тарифы' },
  { id: 'settings', label: 'Настройки' },
  { id: 'tickets', label: 'Тикеты' },
  { id: 'brand', label: 'Бренд' },
];

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState('stats');
  const { user } = useUserStore();

  if (!user || (user.role !== 'ADMIN' && user.role !== 'DEV')) {
    return (
      <div className="animate-in empty-state">
        <Shield size={48} style={{ color: 'var(--red)', marginBottom: 16 }} />
        <div>Доступ запрещён</div>
      </div>
    );
  }

  return (
    <div className="animate-in">
      <h2 className="page-title">Панель управления</h2>
      <div className="admin-tabs">
        {tabs.map((t) => (
          <button
            key={t.id}
            className={`admin-tab${activeTab === t.id ? ' active' : ''}`}
            onClick={() => setActiveTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>
      {activeTab === 'stats' && <AdminStats />}
      {activeTab === 'users' && <AdminUsers />}
      {activeTab === 'plans' && <AdminPlans />}
      {activeTab === 'settings' && <AdminSettings />}
      {activeTab === 'tickets' && <AdminTickets />}
      {activeTab === 'brand' && <AdminBrand />}
    </div>
  );
}
