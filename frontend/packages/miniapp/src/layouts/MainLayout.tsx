import { Outlet } from 'react-router-dom';
import ParticleBackground from '../components/ParticleBackground';
import BottomNav from '../components/BottomNav';
import AppHeader from '../components/AppHeader';
import './MainLayout.css';

export default function MainLayout() {
  return (
    <div className="app-layout">
      <ParticleBackground />
      <div className="bg-glow" />
      <AppHeader />
      <main className="app-content">
        <Outlet />
      </main>
      <BottomNav />
    </div>
  );
}
