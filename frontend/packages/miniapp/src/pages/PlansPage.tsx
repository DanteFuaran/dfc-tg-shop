import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShoppingCart, Zap, Wifi, Smartphone, X, CreditCard, ChevronDown } from 'lucide-react';
import {
  useUserStore,
  purchaseApi,
  formatPrice,
  copyToClipboard,
  CURRENCY_SYMBOLS,
  GATEWAY_LABELS,
  GATEWAY_DESCRIPTIONS,
} from '@dfc/shared';
import type { Plan, PlanDuration } from '@dfc/shared';

export default function PlansPage() {
  const navigate = useNavigate();
  const { plans, trialAvailable, availableGateways, defaultCurrency } = useUserStore();

  const [selectedPlan, setSelectedPlan] = useState<Plan | null>(null);
  const [durIdx, setDurIdx] = useState<Record<number, number>>({});
  const [modalOpen, setModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  /* ── helpers ── */
  const showToast = (text: string, type: 'success' | 'error' = 'success') => {
    setToast({ text, type });
    setTimeout(() => setToast(null), 3000);
  };

  const getDurIndex = (planId: number) => durIdx[planId] ?? 0;

  const getPrice = (dur: PlanDuration) => {
    const p = dur.prices.find((pr) => pr.currency === defaultCurrency) ?? dur.prices[0];
    if (!p) return '—';
    const sym = CURRENCY_SYMBOLS[p.currency] ?? p.currency;
    return `${formatPrice(p.amount)} ${sym}`;
  };

  const formatTraffic = (limit: number | null) => {
    if (limit === null || limit === 0) return 'Безлимит';
    if (limit >= 1024) return `${(limit / 1024).toFixed(limit % 1024 === 0 ? 0 : 1)} ТБ`;
    return `${limit} ГБ`;
  };

  const daysLabel = (days: number) => {
    if (days === 1) return '1 день';
    if (days >= 2 && days <= 4) return `${days} дня`;
    if (days === 30) return '1 мес';
    if (days === 60) return '2 мес';
    if (days === 90) return '3 мес';
    if (days === 180) return '6 мес';
    if (days === 365) return '1 год';
    return `${days} дн`;
  };

  /* ── trial ── */
  const handleTrial = async () => {
    setLoading(true);
    try {
      await purchaseApi.activateTrial();
      showToast('Пробный период активирован!');
      await useUserStore.getState().fetchData();
      navigate('/connect');
    } catch {
      showToast('Не удалось активировать пробный период', 'error');
    } finally {
      setLoading(false);
    }
  };

  /* ── buy ── */
  const openGatewayModal = (plan: Plan) => {
    setSelectedPlan(plan);
    setModalOpen(true);
  };

  const handleBuy = async (gatewayType: string) => {
    if (!selectedPlan) return;
    const idx = getDurIndex(selectedPlan.id);
    const dur = selectedPlan.durations[idx];
    if (!dur) return;

    setLoading(true);
    try {
      const { data } = await purchaseApi.buy({
        plan_id: selectedPlan.id,
        duration_days: dur.days,
        gateway: gatewayType,
      });
      setModalOpen(false);

      if (data.payment_url) {
        window.open(data.payment_url, '_blank');
        showToast('Перенаправление на оплату…');
      } else if (data.ok) {
        showToast(data.message || 'Подписка оформлена!');
        await useUserStore.getState().fetchData();
        navigate('/connect');
      } else {
        showToast(data.message || 'Ошибка покупки', 'error');
      }
    } catch {
      showToast('Ошибка при оформлении покупки', 'error');
    } finally {
      setLoading(false);
    }
  };

  /* ── render ── */
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      <h1 className="page-title animate-in">Тарифы</h1>

      {/* Trial card */}
      {trialAvailable && (
        <div className="card animate-in" style={{ borderColor: 'var(--green)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
            <Zap size={18} color="var(--green)" />
            <span className="fw-600">Пробный период</span>
            <span className="pill pill-green" style={{ marginLeft: 'auto' }}>FREE</span>
          </div>
          <p style={{ color: 'var(--text2)', fontSize: '0.85rem', marginBottom: 14 }}>
            Попробуйте VPN бесплатно — активируйте пробный доступ прямо сейчас.
          </p>
          <button className="btn btn-primary btn-full" onClick={handleTrial} disabled={loading}>
            {loading ? <span className="spinner" /> : 'Активировать бесплатно'}
          </button>
        </div>
      )}

      {/* Plan cards */}
      {plans.map((plan) => {
        const idx = getDurIndex(plan.id);
        const dur = plan.durations[idx];
        return (
          <div key={plan.id} className="card animate-in">
            {/* Header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
              <span className="fw-600" style={{ fontSize: '1rem' }}>{plan.name}</span>
              {plan.tag && <span className="badge badge-gold">{plan.tag}</span>}
            </div>

            {plan.description && (
              <p style={{ color: 'var(--text2)', fontSize: '0.83rem', marginBottom: 12 }}>
                {plan.description}
              </p>
            )}

            {/* Info rows */}
            <div className="card-row">
              <span className="card-label"><Wifi size={14} style={{ verticalAlign: -2, marginRight: 4 }} />Трафик</span>
              <span className="card-value">{formatTraffic(plan.traffic_limit)}</span>
            </div>
            <div className="card-row">
              <span className="card-label"><Smartphone size={14} style={{ verticalAlign: -2, marginRight: 4 }} />Устройства</span>
              <span className="card-value">{plan.device_limit ?? '∞'}</span>
            </div>

            {/* Duration selector */}
            {plan.durations.length > 1 && (
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', margin: '12px 0 4px' }}>
                {plan.durations.map((d, i) => (
                  <button
                    key={d.days}
                    className={`pill ${i === idx ? 'pill-filled' : 'pill-outline'}`}
                    onClick={() => setDurIdx((prev) => ({ ...prev, [plan.id]: i }))}
                  >
                    {daysLabel(d.days)}
                  </button>
                ))}
              </div>
            )}

            {/* Price + buy */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 14 }}>
              <span style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--cyan)' }}>
                {dur ? getPrice(dur) : '—'}
              </span>
              <button
                className="btn btn-primary btn-sm"
                onClick={() => openGatewayModal(plan)}
                disabled={loading}
              >
                <ShoppingCart size={15} /> Купить
              </button>
            </div>
          </div>
        );
      })}

      {plans.length === 0 && (
        <div className="empty-state animate-in">Нет доступных тарифов</div>
      )}

      {/* Gateway selection modal */}
      {modalOpen && selectedPlan && (
        <div className="modal-overlay" onClick={() => setModalOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Способ оплаты</h3>
              <button className="modal-close" onClick={() => setModalOpen(false)}>
                <X size={20} />
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {availableGateways.map((gw) => (
                <button
                  key={gw.type}
                  className="card"
                  style={{ cursor: 'pointer', textAlign: 'left' }}
                  onClick={() => handleBuy(gw.type)}
                  disabled={loading}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                    <CreditCard size={18} color="var(--cyan)" />
                    <div>
                      <div className="fw-600" style={{ fontSize: '0.9rem' }}>
                        {GATEWAY_LABELS[gw.type] ?? gw.type}
                      </div>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text2)' }}>
                        {GATEWAY_DESCRIPTIONS[gw.type] ?? ''}
                      </div>
                    </div>
                  </div>
                </button>
              ))}
            </div>

            {loading && (
              <div style={{ display: 'flex', justifyContent: 'center', padding: 16 }}>
                <span className="spinner spinner-lg" />
              </div>
            )}
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
