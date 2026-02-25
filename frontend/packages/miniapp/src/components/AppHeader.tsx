import { useNavigate } from 'react-router-dom';
import { useUserStore, formatPrice, CURRENCY_SYMBOLS } from '@dfc/shared';

export default function AppHeader() {
  const navigate = useNavigate();
  const { brand, user, features, defaultCurrency } = useUserStore();

  const sym = CURRENCY_SYMBOLS[defaultCurrency] || '₽';
  const isUrl = brand.logo.startsWith('http') || brand.logo.startsWith('/');
  const showBonusBalance = features?.balance_mode === 'SEPARATE';

  return (
    <header className="app-header">
      {/* Logo */}
      <div className="app-header-logo">
        {isUrl ? (
          <img src={brand.logo} alt={brand.name} className="app-header-logo-img" />
        ) : (
          <span className="app-header-logo-emoji">{brand.logo || '🔐'}</span>
        )}
      </div>

      {/* Brand info */}
      <div className="app-header-brand">
        <span className="app-header-name">{brand.name}</span>
        {brand.slogan && (
          <span className="app-header-slogan">{brand.slogan}</span>
        )}
      </div>

      {/* Balances — click → profile */}
      {features?.balance_enabled && user && (
        <div
          className="app-header-balances"
          onClick={() => navigate('/profile')}
          role="button"
          tabIndex={0}
        >
          <span className="app-header-badge">
            💰 {formatPrice(user.balance)} {sym}
          </span>
          {showBonusBalance && (
            <span className="app-header-badge app-header-badge-bonus">
              🎁 {formatPrice(user.referral_balance)} {sym}
            </span>
          )}
        </div>
      )}
    </header>
  );
}
