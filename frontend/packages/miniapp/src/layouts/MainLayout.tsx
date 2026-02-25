import { Outlet } from 'react-router-dom';
import ParticleBackground from '../components/ParticleBackground';
import BottomNav from '../components/BottomNav';
import './MainLayout.css';

export default function MainLayout() {
  return (
    <div className="app-layout">
      <ParticleBackground />
      <div className="bg-glow" />
      <main className="app-content">
        <Outlet />
      </main>
      <BottomNav />
    </div>
  );
}
