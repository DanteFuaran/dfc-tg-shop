import { useState } from 'react';
import { useUserStore } from '@dfc/shared';
import { Shield } from 'lucide-react';
import AdminStats from './admin/AdminStats';
import AdminMonitoring from './admin/AdminMonitoring';
import AdminBroadcast from './admin/AdminBroadcast';
import AdminUsers from './admin/AdminUsers';
import AdminPlans from './admin/AdminPlans';
import AdminBotManagement from './admin/AdminBotManagement';
import AdminFeatures from './admin/AdminFeatures';
import AdminBrand from './admin/AdminBrand';

const tabs = [
  { id: 'stats', label: 'Статистика' },
  { id: 'monitoring', label: 'Мониторинг' },
  { id: 'broadcast', label: 'Рассылка' },
  { id: 'users', label: 'Пользователи' },
  { id: 'plans', label: 'Тарифы' },
  { id: 'bot', label: 'Управление ботом' },
  { id: 'features', label: 'Функционал' },
  { id: 'brand', label: 'Брендирование' },
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
      {activeTab === 'monitoring' && <AdminMonitoring />}
      {activeTab === 'broadcast' && <AdminBroadcast />}
      {activeTab === 'users' && <AdminUsers />}
      {activeTab === 'plans' && <AdminPlans />}
      {activeTab === 'bot' && <AdminBotManagement />}
      {activeTab === 'features' && <AdminFeatures />}
      {activeTab === 'brand' && <AdminBrand />}
    </div>
  );
}
