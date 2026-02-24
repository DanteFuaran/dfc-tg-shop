import { useUserStore } from '@dfc/shared';
import { Smartphone, Plus, Monitor, AlertCircle } from 'lucide-react';
import './DevicesPage.css';

export default function DevicesPage() {
  const { subscription, features } = useUserStore();

  if (!subscription || subscription.status !== 'ACTIVE') {
    return (
      <div className="devices-page animate-in">
        <div className="empty-state">
          <Smartphone size={40} />
          <p>Нет активной подписки</p>
        </div>
      </div>
    );
  }

  const used = subscription.active_devices_count ?? 0;
  const limit = subscription.device_limit ?? 0;
  const atLimit = limit > 0 && used >= limit;
  const percent = limit > 0 ? Math.min((used / limit) * 100, 100) : 0;

  return (
    <div className="devices-page animate-in">
      <h2 className="page-title"><Monitor size={20} /> Устройства</h2>

      <div className="card">
        <div className="device-meter">
          <div className="device-meter-label">
            <span>Подключено</span>
            <span className="device-meter-count">
              {used} / {limit > 0 ? limit : '∞'}
            </span>
          </div>
          {limit > 0 && (
            <div className="device-bar">
              <div
                className={`device-bar-fill ${atLimit ? 'device-bar-full' : ''}`}
                style={{ width: `${percent}%` }}
              />
            </div>
          )}
        </div>

        {atLimit && (
          <div className="device-warning">
            <AlertCircle size={14} />
            <span>Достигнут лимит устройств</span>
          </div>
        )}
      </div>

      {features?.extra_devices_enabled !== false && (
        <div className="card extra-devices-card">
          <div className="card-title"><Plus size={16} /> Дополнительные устройства</div>
          <p className="extra-desc">
            Вы можете расширить количество устройств для текущей подписки.
          </p>
          <button className="btn btn-primary btn-full btn-glossy">
            Расширить
          </button>
        </div>
      )}
    </div>
  );
}
