import { useNavigate } from 'react-router-dom';
import { useUserStore, CURRENCY_SYMBOLS } from '@dfc/shared';
import {
  Zap, Link, Gift, Smartphone, Share2,
  Download, BarChart3, Clock, Wifi,
} from 'lucide-react';
import './HomePage.css';

export default function HomePage() {
  const navigate = useNavigate();
  const {
    user, subscription, trialAvailable, defaultCurrency,
    features, botUsername, refLink,
  } = useUserStore();

  const sym = CURRENCY_SYMBOLS[defaultCurrency] ?? '₽';

  const handleInvite = () => {
    if (!refLink) return;

    // Формируем текст приглашения (логика invite_getter из бота)
    const rawTemplate = features?.referral_invite_message ?? '';
    let inviteText: string;

    if (rawTemplate) {
      if (rawTemplate.includes('{url}')) {
        inviteText = rawTemplate
          .replace(/\{url\}/g, refLink)
          .replace(/\{name\}/g, 'VPN')
          .replace(/\{space\}/g, '\n');
      } else {
        inviteText = rawTemplate
          .replace(/\$url/g, refLink)
          .replace(/\$name/g, 'VPN');
      }
      if (inviteText.startsWith('\n')) inviteText = inviteText.slice(1);
    } else {
      inviteText = refLink;
    }

    const tg = window.Telegram?.WebApp;
    const platform = tg?.platform ?? '';
    // На мобильных openTelegramLink открывает нативный чат-пикер.
    // На Telegram Desktop этот метод НЕ открывает чат-пикер (ограничение платформы).
    const isMobile = ['android', 'ios', 'android_x'].includes(platform);

    if (tg && isMobile) {
      // Мобильные: открывает диалог выбора чата
      const shareUrl = `https://t.me/share/url?url=${encodeURIComponent(refLink)}&text=${encodeURIComponent(inviteText)}`;
      tg.openTelegramLink(shareUrl);
    } else if (tg) {
      // ПК (desktop/macos/webk/weba): копируем приглашение в буфер + подсказка
      navigator.clipboard.writeText(inviteText).then(() => {
        tg.showPopup({
          title: '📋 Сообщение скопировано',
          message: 'Пригласительное сообщение скопировано в буфер обмена.\n\nОткройте нужный чат в Telegram и вставьте его (Ctrl+V или ⌘+V).',
          buttons: [{ type: 'ok', text: 'Понятно', id: 'ok' }],
        });
      }).catch(() => {
        // Clipboard недоступен — показываем саму ссылку
        tg.showPopup({
          title: 'Пригласить друга',
          message: `Скопируйте ссылку и отправьте другу:\n\n${refLink}`,
          buttons: [{ type: 'ok', text: 'Понятно', id: 'ok' }],
        });
      });
    } else {
      // Браузер без Telegram
      const shareUrl = `https://t.me/share/url?url=${encodeURIComponent(refLink)}&text=${encodeURIComponent(inviteText)}`;
      window.open(shareUrl, '_blank');
    }
  };

  return (
    <div className="home-page animate-in">
      {/* ── Subscription status ── */}
      {subscription ? (
        <div className="card sub-card">
          <div className="sub-status-row">
            <div className="sub-status-dot active" />
            <span className="sub-plan-name">{subscription.plan_name}</span>
            <span className={`sub-status-badge ${subscription.status.toLowerCase()}`}>
              {subscription.status === 'ACTIVE' ? 'Активна' : 'Истекла'}
            </span>
          </div>
          <div className="sub-meta">
            <div className="sub-meta-item">
              <Clock size={14} />
              <span>{subscription.expire_at}</span>
            </div>
            <div className="sub-meta-item">
              <Wifi size={14} />
              <span>{subscription.traffic_limit ?? '∞'} GB</span>
            </div>
            <div className="sub-meta-item">
              <Smartphone size={14} />
              <span>{subscription.active_devices_count}/{subscription.device_limit ?? '∞'}</span>
            </div>
          </div>
        </div>
      ) : (
        <div className="card sub-card sub-card-empty">
          <div className="sub-empty-text">Нет подписки</div>
        </div>
      )}

      {/* ── Quick actions ── */}
      <div className="quick-actions">
        {trialAvailable && (
          <button className="pill pill-cyan" onClick={() => navigate('/plans?trial=1')}>
            <Gift size={16} /> Попробовать бесплатно
          </button>
        )}
        {subscription && (
          <button className="pill pill-cyan" onClick={() => navigate('/connect')}>
            <Zap size={16} /> Подключиться
          </button>
        )}
        {features?.promocodes_enabled && (
          <button className="pill pill-outline" onClick={() => navigate('/promo')}>
            <Gift size={16} /> Промокоды
          </button>
        )}
        <button className="pill pill-outline" onClick={() => navigate('/devices')}>
          <Smartphone size={16} /> Устройства
        </button>
        {features?.referral_enabled && (
          <button className="pill pill-outline" onClick={handleInvite}>
            <Share2 size={16} /> Пригласить друга
          </button>
        )}
      </div>

      {/* ── Buy / Renew ── */}
      <button className="btn btn-primary btn-full" onClick={() => navigate('/plans')}>
        {subscription ? 'Продлить подписку' : 'Купить подписку'}
      </button>

      {/* ── App download ── */}
      {subscription && (
        <button
          className="btn btn-secondary btn-full"
          style={{ marginTop: 8 }}
          onClick={() => window.open('/api/v1/download', '_blank')}
        >
          <Download size={16} /> Скачать приложение
        </button>
      )}
    </div>
  );
}
