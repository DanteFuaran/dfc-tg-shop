import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { authApi, useUserStore } from '@dfc/shared';
import './styles/global.css';
import './styles/components.css';

/* ─── Telegram WebApp init ─── */
const tgApp = window.Telegram?.WebApp;

async function bootstrap() {
  // If inside Telegram — authenticate with initData
  if (tgApp) {
    tgApp.ready();
    tgApp.expand();

    // Apply Telegram theme
    if (tgApp.colorScheme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
    }

    const initData = tgApp.initData;
    if (initData) {
      try {
        await authApi.loginTelegram(initData);
      } catch (e) {
        console.error('TG auth failed:', e);
      }
    }
  }

  // Fetch user data
  await useUserStore.getState().fetchData();

  // Render
  ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
  );
}

bootstrap();
