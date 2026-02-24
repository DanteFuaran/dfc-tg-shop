import { useState, useMemo } from 'react';
import {
  useUserStore,
  purchaseApi,
  CURRENCY_SYMBOLS,
  GATEWAY_LABELS,
  GATEWAY_DESCRIPTIONS,
  formatPrice,
} from '@dfc/shared';
import type { Plan, PlanDuration } from '@dfc/shared';
import {
  ShoppingCart,
  Clock,
  Wifi,
  Smartphone,
  Tag,
  CreditCard,
  ChevronRight,
  Sparkles,
  Check,
} from 'lucide-react';
import toast from 'react-hot-toast';
import './PlansPage.css';

export default function PlansPage() {
  const { plans, availableGateways, defaultCurrency, subscription, features } = useUserStore();
  const [selectedPlan, setSelectedPlan] = useState<Plan | null>(null);
  const [selectedDuration, setSelectedDuration] = useState<PlanDuration | null>(null);
  const [selectedGateway, setSelectedGateway] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const sym = CURRENCY_SYMBOLS[defaultCurrency] ?? '₽';

  const getPrice = (duration: PlanDuration): string => {
    const p = duration.prices.find((pr) => pr.currency === defaultCurrency) ?? duration.prices[0];
    if (!p) return '—';
    return `${formatPrice(Number(p.amount))} ${CURRENCY_SYMBOLS[p.currency] ?? p.currency}`;
  };

  const getRawPrice = (duration: PlanDuration): number => {
    const p = duration.prices.find((pr) => pr.currency === defaultCurrency) ?? duration.prices[0];
    return p ? Number(p.amount) : 0;
  };

  const formatDays = (days: number) => {
    if (days === 30) return '1 мес';
    if (days === 60) return '2 мес';
    if (days === 90) return '3 мес';
    if (days === 180) return '6 мес';
    if (days === 365) return '1 год';
    return `${days} дн`;
  };

  /* Gateways matching plan's best price currency */
  const filteredGateways = useMemo(() => {
    if (!selectedDuration) return availableGateways;
    const bestCurrency =
      selectedDuration.prices.find((p) => p.currency === defaultCurrency)?.currency ??
      selectedDuration.prices[0]?.currency;
    if (!bestCurrency) return availableGateways;
    return availableGateways.filter((gw) => gw.currency === bestCurrency || gw.type === 'BALANCE');
  }, [selectedDuration, availableGateways, defaultCurrency]);

  const handleBuy = async () => {
    if (!selectedPlan || !selectedDuration) return;
    setLoading(true);
    try {
      const res = await purchaseApi.buy({
        plan_id: selectedPlan.id,
        duration_days: selectedDuration.days,
        gateway: selectedGateway ?? undefined,
      });
      if (res.data.payment_url) {
        window.open(res.data.payment_url, '_blank');
      } else if (res.data.ok) {
        toast.success('Подписка оформлена!');
        setSelectedPlan(null);
        setSelectedDuration(null);
        setSelectedGateway(null);
        // Refresh user data
        useUserStore.getState().fetchData();
      } else {
        toast.error(res.data.message ?? 'Ошибка покупки');
      }
    } catch (e: any) {
      toast.error(e?.response?.data?.detail ?? 'Ошибка покупки');
    } finally {
      setLoading(false);
    }
  };

  /* ─── Step 1: Plan selection ─── */
  if (!selectedPlan) {
    return (
      <div className="plans-page animate-in">
        <h2 className="page-title">
          <ShoppingCart size={20} /> Тарифы
        </h2>

        {plans.length === 0 && (
          <div className="empty-state">Нет доступных тарифов</div>
        )}

        {plans.map((plan) => (
          <div
            key={plan.id}
            className="plan-card card"
            onClick={() => {
              setSelectedPlan(plan);
              if (plan.durations.length === 1) setSelectedDuration(plan.durations[0] ?? null);
            }}
          >
            <div className="plan-header">
              <div className="plan-name">{plan.name}</div>
              {plan.tag && <span className="plan-tag"><Tag size={12} /> {plan.tag}</span>}
            </div>

            {plan.description && (
              <p className="plan-desc">{plan.description}</p>
            )}

            <div className="plan-meta">
              {plan.traffic_limit && (
                <span className="plan-meta-item">
                  <Wifi size={14} /> {plan.traffic_limit} GB
                </span>
              )}
              {plan.device_limit && (
                <span className="plan-meta-item">
                  <Smartphone size={14} /> {plan.device_limit} устр.
                </span>
              )}
            </div>

            <div className="plan-prices">
              {plan.durations.slice(0, 3).map((d) => (
                <span key={d.days} className="plan-price-chip">
                  <Clock size={12} /> {formatDays(d.days)} — {getPrice(d)}
                </span>
              ))}
              {plan.durations.length > 3 && (
                <span className="plan-price-chip plan-price-more">
                  +{plan.durations.length - 3}
                </span>
              )}
            </div>

            <div className="plan-action">
              <ChevronRight size={18} />
            </div>
          </div>
        ))}
      </div>
    );
  }

  /* ─── Step 2: Duration selection ─── */
  if (!selectedDuration) {
    return (
      <div className="plans-page animate-in">
        <button className="back-btn" onClick={() => setSelectedPlan(null)}>
          ← Назад
        </button>
        <h2 className="page-title">{selectedPlan.name}</h2>
        <p className="step-label">Выберите период</p>

        <div className="duration-grid">
          {selectedPlan.durations.map((d) => (
            <button
              key={d.days}
              className="duration-card"
              onClick={() => setSelectedDuration(d)}
            >
              <span className="duration-days">{formatDays(d.days)}</span>
              <span className="duration-price">{getPrice(d)}</span>
              {d.days >= 90 && (
                <span className="duration-badge">
                  <Sparkles size={10} /> Выгодно
                </span>
              )}
            </button>
          ))}
        </div>
      </div>
    );
  }

  /* ─── Step 3: Gateway selection & confirm ─── */
  return (
    <div className="plans-page animate-in">
      <button
        className="back-btn"
        onClick={() => {
          setSelectedDuration(null);
          setSelectedGateway(null);
        }}
      >
        ← Назад
      </button>

      <h2 className="page-title">Оплата</h2>

      <div className="card summary-card">
        <div className="summary-row">
          <span>Тариф</span>
          <span className="summary-val">{selectedPlan.name}</span>
        </div>
        <div className="summary-row">
          <span>Период</span>
          <span className="summary-val">{formatDays(selectedDuration.days)}</span>
        </div>
        <div className="summary-row summary-total">
          <span>Итого</span>
          <span className="summary-val">{getPrice(selectedDuration)}</span>
        </div>
      </div>

      {filteredGateways.length > 1 && (
        <>
          <p className="step-label"><CreditCard size={16} /> Способ оплаты</p>
          <div className="gateways-list">
            {filteredGateways.map((gw) => (
              <button
                key={gw.type}
                className={`gateway-card ${selectedGateway === gw.type ? 'gateway-active' : ''}`}
                onClick={() => setSelectedGateway(gw.type)}
              >
                <div className="gateway-info">
                  <span className="gateway-name">{GATEWAY_LABELS[gw.type] ?? gw.type}</span>
                  <span className="gateway-desc">{GATEWAY_DESCRIPTIONS[gw.type] ?? ''}</span>
                </div>
                {selectedGateway === gw.type && <Check size={18} className="gateway-check" />}
              </button>
            ))}
          </div>
        </>
      )}

      <button
        className="btn btn-primary btn-full btn-glossy buy-btn"
        disabled={loading || (filteredGateways.length > 1 && !selectedGateway)}
        onClick={handleBuy}
      >
        {loading ? 'Обработка...' : `Оплатить ${getPrice(selectedDuration)}`}
      </button>
    </div>
  );
}
