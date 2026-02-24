import { Outlet } from 'react-router-dom';
import BottomNav from '../components/BottomNav';
import ParticleBackground from '../components/ParticleBackground';
import './MainLayout.css';

export default function MainLayout() {
  return (
    <div className="app-layout">
      <ParticleBackground />
      <main className="app-content">
        <Outlet />
      </main>
      <BottomNav />
    </div>
  );
}
