import { useUserStore, CURRENCY_SYMBOLS, copyToClipboard } from '@dfc/shared';
import { User as UserIcon, Wallet, Share2, Link, Key, Globe } from 'lucide-react';
import toast from 'react-hot-toast';
import './ProfilePage.css';

export default function ProfilePage() {
  const { user, subscription, features, refLink, defaultCurrency } = useUserStore();
  const sym = CURRENCY_SYMBOLS[defaultCurrency] ?? '₽';

  if (!user) return null;

  const handleCopyRef = async () => {
    if (!refLink) return;
    const ok = await copyToClipboard(refLink);
    toast(ok ? 'Ссылка скопирована' : 'Ошибка');
  };

  const handleInvite = () => {
    if (!refLink) return;
    const shareUrl = `https://t.me/share/url?text=${encodeURIComponent(refLink)}`;
    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.openTelegramLink(shareUrl);
    } else {
      window.open(shareUrl, '_blank');
    }
  };

  return (
    <div className="profile-page animate-in">
      <h2 className="page-title">Профиль</h2>

      {/* Profile card */}
      <div className="card">
        <div className="card-title"><UserIcon size={18} /> Профиль</div>
        <div className="card-row">
          <span className="card-label">ID</span>
          <span className="card-value">{user.telegram_id}</span>
        </div>
        <div className="card-row">
          <span className="card-label">Имя</span>
          <span className="card-value">{user.name}</span>
        </div>
      </div>

      {/* Balance */}
      {features?.balance_enabled && (
        <div className="card">
          <div className="card-title"><Wallet size={18} /> Баланс</div>
          <div className="card-row">
            <span className="card-label">Основной</span>
            <span className="card-value">{user.balance} {sym}</span>
          </div>
          {features.referral_enabled && (
            <div className="card-row">
              <span className="card-label">Реферальный</span>
              <span className="card-value">{user.referral_balance} {sym}</span>
            </div>
          )}
          <button className="btn btn-primary btn-full" style={{ marginTop: 8 }}>
            Пополнить
          </button>
        </div>
      )}

      {/* Referral */}
      {features?.referral_enabled && refLink && (
        <div className="card">
          <div className="card-title"><Share2 size={18} /> Реферальная программа</div>
          <div className="ref-link-box">
            <code className="ref-link-text">{refLink}</code>
          </div>
          <div className="ref-actions">
            <button className="pill pill-outline" onClick={handleCopyRef}>
              <Link size={14} /> Копировать
            </button>
            <button className="pill pill-cyan" onClick={handleInvite}>
              <Share2 size={14} /> Пригласить
            </button>
          </div>
        </div>
      )}

      {/* Language */}
      <div className="card">
        <div className="card-row">
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <Globe size={16} color="var(--text2)" />
            <span className="card-label">Язык</span>
          </div>
          <span className="card-value">{user.language}</span>
        </div>
      </div>
    </div>
  );
}
