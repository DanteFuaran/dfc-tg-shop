import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUserStore, CURRENCY_SYMBOLS } from '@dfc/shared';
import {
  Zap, Link, Gift, Smartphone, Share2,
  Download, BarChart3, Clock, Wifi, Copy, Check, X,
} from 'lucide-react';
import './HomePage.css';

export default function HomePage() {
  const navigate = useNavigate();
  const {
    user, subscription, trialAvailable, defaultCurrency,
    features, botUsername, refLink,
  } = useUserStore();

  const [inviteModal, setInviteModal] = useState(false);
  const [copied, setCopied] = useState(false);
  const [inviteText, setInviteText] = useState('');

  const sym = CURRENCY_SYMBOLS[defaultCurrency] ?? '₽';

  const handleInvite = () => {
    console.log('🔘 Invite button clicked');
    
    if (!refLink) {
      console.warn('❌ refLink is empty');
      return;
    }

    console.log('✅ refLink:', refLink);
    console.log('✅ features:', features);

    // Формируем текст приглашения (логика invite_getter из бота)
    const rawTemplate = features?.referral_invite_message ?? '';
    let msgText: string;

    if (rawTemplate) {
      if (rawTemplate.includes('{url}')) {
        msgText = rawTemplate
          .replace(/\{url\}/g, refLink)
          .replace(/\{name\}/g, 'VPN')
          .replace(/\{space\}/g, '\n');
      } else {
        msgText = rawTemplate
          .replace(/\$url/g, refLink)
          .replace(/\$name/g, 'VPN');
      }
      if (msgText.startsWith('\n')) msgText = msgText.slice(1);
    } else {
      msgText = refLink;
    }

    console.log('📝 msgText:', msgText);

    const tg = window.Telegram?.WebApp;
    const platform = tg?.platform ?? '';
    const isMobile = ['android', 'ios', 'android_x'].includes(platform);

    console.log('📱 platform:', platform, '| isMobile:', isMobile);

    if (tg && isMobile) {
      // Мобильные: открывает нативный диалог выбора чата
      console.log('📱 Using native chat picker');
      const shareUrl = `https://t.me/share/url?url=${encodeURIComponent(refLink)}&text=${encodeURIComponent(msgText)}`;
      tg.openTelegramLink(shareUrl);
    } else {
      // ПК и браузер: показываем кастомный модал с копированием
      console.log('🖥️ Showing custom modal');
      setInviteText(msgText);
      setInviteModal(true);
      setCopied(false);
    }
  };

  const handleCopy = () => {
    if (!inviteText) return;
    navigator.clipboard.writeText(inviteText).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 3000);
    }).catch(() => {
      // fallback: select text
    });
  };

  return (
    <div className="home-page animate-in">

      {/* ── Invite modal (desktop) ── */}
      {inviteModal && (
        <div className="invite-modal-overlay" onClick={() => setInviteModal(false)}>
          <div className="invite-modal" onClick={e => e.stopPropagation()}>
            <div className="invite-modal-header">
              <div className="invite-modal-title">
                <Share2 size={18} className="invite-modal-icon" />
                Пригласить друга
              </div>
              <button className="invite-modal-close" onClick={() => setInviteModal(false)}>
                <X size={18} />
              </button>
            </div>

            <p className="invite-modal-desc">
              Отправьте это сообщение другу — он присоединится как ваш реферал и вы получите бонус.
            </p>

            <div className="invite-modal-text-box">
              <pre className="invite-modal-text">{inviteText}</pre>
            </div>

            <button
              className={`btn btn-primary btn-full invite-modal-copy-btn${copied ? ' copied' : ''}`}
              onClick={handleCopy}
            >
              {copied
                ? <><Check size={16} /> Скопировано!</>
                : <><Copy size={16} /> Скопировать сообщение</>
              }
            </button>

            {copied && (
              <p className="invite-modal-hint">
                Вставьте сообщение в нужный чат (Ctrl+V или ⌘+V)
              </p>
            )}
          </div>
        </div>
      )}
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
