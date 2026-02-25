import { useLocation, useNavigate } from 'react-router-dom';
import { Home, MessageCircle, User, Shield } from 'lucide-react';
import { useUserStore } from '@dfc/shared';
import './BottomNav.css';

interface NavItem {
  path: string;
  label: string;
  icon: React.ElementType;
  adminOnly?: boolean;
}

const navItems: NavItem[] = [
  { path: '/', label: 'Home', icon: Home },
  { path: '/support', label: 'Support', icon: MessageCircle },
  { path: '/profile', label: 'Profile', icon: User },
  { path: '/admin', label: 'Admin', icon: Shield, adminOnly: true },
];

export default function BottomNav() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, ticketUnread } = useUserStore();

  const role = user?.role;
  const isAdmin = role === 'ADMIN' || role === 'OWNER';

  return (
    <nav className="bottom-nav">
      {navItems.map((item) => {
        if (item.adminOnly && !isAdmin) return null;

        const isActive =
          item.path === '/'
            ? location.pathname === '/'
            : location.pathname.startsWith(item.path);

        const Icon = item.icon;

        return (
          <div
            key={item.path}
            className={`nav-item${isActive ? ' active' : ''}`}
            onClick={() => navigate(item.path)}
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
