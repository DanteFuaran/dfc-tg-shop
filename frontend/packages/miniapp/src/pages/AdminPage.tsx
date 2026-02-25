import { useState, useEffect, useCallback } from 'react';
import { useUserStore, adminApi } from '@dfc/shared';
import {
  Shield, BarChart3, Activity, Megaphone, Users, CreditCard,
  Bot, Sliders, Palette, MessageSquare,
} from 'lucide-react';
import AdminStats from './admin/AdminStats';
import AdminMonitoring from './admin/AdminMonitoring';
import AdminBroadcast from './admin/AdminBroadcast';
import AdminUsers from './admin/AdminUsers';
import AdminPlans from './admin/AdminPlans';
import AdminBotManagement from './admin/AdminBotManagement';
import AdminFeatures from './admin/AdminFeatures';
import AdminBrand from './admin/AdminBrand';
import AdminTickets from './admin/AdminTickets';

const ICON_SIZE = 16;

const tabs = [
  { id: 'stats',      label: 'Статистика',       icon: <BarChart3 size={ICON_SIZE} /> },
  { id: 'monitoring', label: 'Мониторинг',        icon: <Activity size={ICON_SIZE} /> },
  { id: 'broadcast',  label: 'Рассылка',          icon: <Megaphone size={ICON_SIZE} /> },
  { id: 'users',      label: 'Пользователи',      icon: <Users size={ICON_SIZE} /> },
  { id: 'plans',      label: 'Тарифы',            icon: <CreditCard size={ICON_SIZE} /> },
  { id: 'bot',        label: 'Управление',         icon: <Bot size={ICON_SIZE} /> },
  { id: 'features',   label: 'Функционал',        icon: <Sliders size={ICON_SIZE} /> },
  { id: 'brand',      label: 'Брендирование',     icon: <Palette size={ICON_SIZE} /> },
  { id: 'tickets',    label: 'Обращения',          icon: <MessageSquare size={ICON_SIZE} /> },
];

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState('stats');
  const [ticketBadge, setTicketBadge] = useState(0);
  const { user } = useUserStore();

  const loadBadge = useCallback(async () => {
    try {
      const { data } = await adminApi.listTickets();
      const unread = (data as any[]).filter(
        (t: any) => !t.is_read_by_admin && t.status !== 'CLOSED',
      ).length;
      setTicketBadge(unread);
    } catch { /* ignore */ }
  }, []);

  useEffect(() => { loadBadge(); }, [loadBadge]);

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
            <span className="tab-icon">{t.icon}</span>
            <span className="tab-label">{t.label}</span>
            {t.id === 'tickets' && ticketBadge > 0 && (
              <span className="admin-tab-badge">{ticketBadge > 99 ? '99+' : ticketBadge}</span>
            )}
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
      {activeTab === 'tickets' && <AdminTickets />}
    </div>
  );
}
