import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import HomePage from './pages/HomePage';
import PlansPage from './pages/PlansPage';
import ConnectPage from './pages/ConnectPage';
import DevicesPage from './pages/DevicesPage';
import PromoPage from './pages/PromoPage';
import TopupPage from './pages/TopupPage';
import SupportPage from './pages/SupportPage';
import ProfilePage from './pages/ProfilePage';
import TicketsListPage from './pages/TicketsListPage';
import TicketChatPage from './pages/TicketChatPage';
import AdminPage from './pages/AdminPage';

export default function App() {
  return (
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
          <Route path="admin/*" element={<AdminPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
