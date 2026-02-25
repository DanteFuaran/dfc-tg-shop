import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import MainLayout from './layouts/MainLayout';
import HomePage from './pages/HomePage';
import SupportPage from './pages/SupportPage';
import ProfilePage from './pages/ProfilePage';
import PlansPage from './pages/PlansPage';
import ConnectPage from './pages/ConnectPage';
import DevicesPage from './pages/DevicesPage';
import PromoPage from './pages/PromoPage';
import TopupPage from './pages/TopupPage';
import TicketsListPage from './pages/TicketsListPage';
import TicketChatPage from './pages/TicketChatPage';
import AdminPage from './pages/AdminPage';
import { useUserStore } from '@dfc/shared';

export default function App() {
  const isAdmin = useUserStore((s) =>
    s.user?.role === 'ADMIN' || s.user?.role === 'OWNER',
  );

  return (
    <>
      <Toaster
        position="top-center"
        toastOptions={{
          style: {
            background: '#1e1e1e',
            color: '#e0e0e0',
            border: '1px solid #2a2a2a',
            borderRadius: '12px',
            fontSize: '13px',
          },
        }}
      />
      <BrowserRouter basename="/web/miniapp">
        <Routes>
          <Route element={<MainLayout />}>
            <Route index element={<HomePage />} />
            <Route path="plans" element={<PlansPage />} />
            <Route path="connect" element={<ConnectPage />} />
            <Route path="devices" element={<DevicesPage />} />
            <Route path="promo" element={<PromoPage />} />
            <Route path="topup" element={<TopupPage />} />
            <Route path="support" element={<SupportPage />} />
            <Route path="profile" element={<ProfilePage />} />
            <Route path="tickets" element={<TicketsListPage />} />
            <Route path="tickets/:id" element={<TicketChatPage />} />
            {isAdmin && <Route path="admin" element={<AdminPage />} />}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}
