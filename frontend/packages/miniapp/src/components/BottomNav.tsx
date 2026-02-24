import { useLocation, useNavigate } from 'react-router-dom';
import { Home, Headphones, User, Shield } from 'lucide-react';
import { useUserStore } from '@dfc/shared';
import './BottomNav.css';

const ITEMS = [
  { path: '/', icon: Home, label: 'Главная' },
  { path: '/support', icon: Headphones, label: 'Поддержка' },
  { path: '/profile', icon: User, label: 'Профиль' },
];

const ADMIN_ITEM = { path: '/admin', icon: Shield, label: 'Админ' };

export default function BottomNav() {
  const location = useLocation();
  const navigate = useNavigate();
  const user = useUserStore((s) => s.user);
  const ticketUnread = useUserStore((s) => s.ticketUnread);

  const isAdmin = user?.role === 'ADMIN' || user?.role === 'OWNER';
  const items = isAdmin ? [...ITEMS, ADMIN_ITEM] : ITEMS;

  return (
    <nav className="bottom-nav">
      {items.map(({ path, icon: Icon, label }) => {
        const active = path === '/'
          ? location.pathname === '/'
          : location.pathname.startsWith(path);

        return (
          <button
            key={path}
            className={`nav-item${active ? ' active' : ''}`}
            onClick={() => navigate(path)}
          >
            <div className="nav-icon-wrap">
              <Icon size={22} strokeWidth={active ? 2.2 : 1.8} />
              {path === '/support' && ticketUnread > 0 && (
                <span className="nav-badge">{ticketUnread}</span>
              )}
            </div>
            <span className="nav-label">{label}</span>
          </button>
        );
      })}
    </nav>
  );
}
