import { useEffect } from 'react';
import { useAdminStore, useUserStore, formatPrice, CURRENCY_SYMBOLS } from '@dfc/shared';
import { Loader } from 'lucide-react';

export default function AdminStats() {
  const { stats, isLoading, fetchStats } = useAdminStore();
  const { defaultCurrency } = useUserStore();
  const currency = defaultCurrency ?? 'RUB';
  const sym = CURRENCY_SYMBOLS[currency] ?? '₽';

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  if (isLoading || !stats) {
    return (
      <div className="empty-state">
        <Loader size={32} className="spinner" />
      </div>
    );
  }

  const items = [
    { label: 'Пользователей', value: stats.total_users, color: 'var(--cyan)' },
    { label: 'Активные', value: stats.active_subscriptions, color: 'var(--green)' },
    { label: 'Истёкшие', value: stats.expired_subscriptions, color: 'var(--red)' },
    { label: 'Доход (сегодня)', value: formatPrice(stats.revenue_today) + ' ' + sym, color: 'var(--gold)' },
    { label: 'Доход (месяц)', value: formatPrice(stats.revenue_month) + ' ' + sym, color: 'var(--gold)' },
    { label: 'Общий доход', value: formatPrice(stats.total_revenue) + ' ' + sym, color: 'var(--cyan)' },
  ];

  return (
    <div className="stat-grid">
      {items.map((item) => (
        <div className="stat-card" key={item.label}>
          <div className="stat-value" style={{ color: item.color }}>
            {item.value}
          </div>
          <div className="stat-label">{item.label}</div>
        </div>
      ))}
    </div>
  );
}
