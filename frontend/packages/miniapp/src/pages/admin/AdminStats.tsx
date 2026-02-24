import { useEffect } from 'react';
import { useAdminStore, CURRENCY_SYMBOLS } from '@dfc/shared';
import { TrendingUp, Users, DollarSign } from 'lucide-react';

export default function AdminStats() {
  const { stats, fetchStats } = useAdminStore();

  useEffect(() => { fetchStats(); }, [fetchStats]);

  if (!stats) return <div className="empty-state">Загрузка...</div>;

  return (
    <>
      <div className="stat-grid">
        <div className="stat-card">
          <span className="stat-value">{stats.total_users}</span>
          <span className="stat-label"><Users size={12} /> Пользователей</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{stats.active_subscriptions}</span>
          <span className="stat-label"><TrendingUp size={12} /> Активных</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{stats.revenue_today} ₽</span>
          <span className="stat-label"><DollarSign size={12} /> Сегодня</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{stats.revenue_month} ₽</span>
          <span className="stat-label"><DollarSign size={12} /> За месяц</span>
        </div>
      </div>
      <div className="stat-grid">
        <div className="stat-card">
          <span className="stat-value">{stats.expired_subscriptions}</span>
          <span className="stat-label">Истёкших</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{stats.total_revenue} ₽</span>
          <span className="stat-label">Всего дохода</span>
        </div>
      </div>
    </>
  );
}
