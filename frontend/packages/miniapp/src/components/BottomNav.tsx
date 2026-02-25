import { useLocation, useNavigate } from 'react-router-dom';
import { Home, MessageCircle, User, Shield, Users } from 'lucide-react';
import { useUserStore } from '@dfc/shared';
import './BottomNav.css';

interface NavItem {
  path: string;
  label: string;
  icon: React.ElementType;
  adminOnly?: boolean;
  external?: boolean;
}

export default function BottomNav() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, features, ticketUnread } = useUserStore();

  const role = user?.role;
  const isAdmin = role === 'ADMIN' || role === 'DEV';

  const navItems: NavItem[] = [
    { path: '/', label: 'Главная', icon: Home },
    { path: '/profile', label: 'Профиль', icon: User },
    ...(features?.community_enabled && features.community_url
      ? [{ path: features.community_url, label: 'Группа', icon: Users, external: true } as NavItem]
      : []),
    { path: '/support', label: 'Поддержка', icon: MessageCircle },
    { path: '/admin', label: 'Админ', icon: Shield, adminOnly: true },
  ];

  return (
    <nav className="bottom-nav">
      {navItems.map((item) => {
        if (item.adminOnly && !isAdmin) return null;

        const isActive = !item.external && (
          item.path === '/'
            ? location.pathname === '/'
            : location.pathname.startsWith(item.path)
        );

        const Icon = item.icon;

        const handleClick = () => {
          if (item.external) {
            window.open(item.path, '_blank');
          } else {
            navigate(item.path);
          }
        };

        return (
          <div
            key={item.path}
            className={`nav-item${isActive ? ' active' : ''}`}
            onClick={handleClick}
          >
            <Icon size={22} />
            {item.path === '/support' && ticketUnread > 0 && (
              <span className="nav-badge">
                {ticketUnread > 99 ? '99+' : ticketUnread}
              </span>
            )}
            <span className="nav-label">{item.label}</span>
          </div>
        );
      })}
    </nav>
  );
}
