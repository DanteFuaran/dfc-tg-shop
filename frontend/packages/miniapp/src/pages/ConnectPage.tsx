import { useState } from 'react';
import { useUserStore, copyToClipboard } from '@dfc/shared';
import {
  Link2,
  Eye,
  EyeOff,
  Copy,
  Download,
  QrCode,
  CheckCircle,
} from 'lucide-react';
import toast from 'react-hot-toast';
import './ConnectPage.css';

export default function ConnectPage() {
  const { subscription, botUsername } = useUserStore();
  const [showUrl, setShowUrl] = useState(false);
  const [showQR, setShowQR] = useState(false);

  if (!subscription || subscription.status !== 'ACTIVE') {
    return (
      <div className="connect-page animate-in">
        <div className="empty-state">
          <Link2 size={40} />
          <p>У вас нет активной подписки</p>
        </div>
      </div>
    );
  }

  const url = subscription.url;

  const handleCopy = async () => {
    const ok = await copyToClipboard(url);
    toast(ok ? 'Ссылка скопирована' : 'Ошибка копирования');
  };

  const handleDownload = () => {
    const blob = new Blob([url], { type: 'text/plain' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'subscription.txt';
    a.click();
    URL.revokeObjectURL(a.href);
  };

  const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(url)}&bgcolor=111111&color=00BCD4`;

  return (
    <div className="connect-page animate-in">
      <h2 className="page-title"><Link2 size={20} /> Подключение</h2>

      <div className="card">
        <div className="card-title">
          <CheckCircle size={16} color="var(--cyan)" /> Ваша ссылка подключения
        </div>

        <div className="url-box">
          {showUrl ? (
            <code className="url-text">{url}</code>
          ) : (
            <code className="url-text url-hidden">••••••••••••••••••••••••••••••</code>
          )}
          <button
            className="url-toggle"
            onClick={() => setShowUrl((p) => !p)}
            title={showUrl ? 'Скрыть' : 'Показать'}
          >
            {showUrl ? <EyeOff size={16} /> : <Eye size={16} />}
          </button>
        </div>

        <div className="connect-actions">
          <button className="pill pill-outline" onClick={handleCopy}>
            <Copy size={14} /> Копировать
          </button>
          <button className="pill pill-outline" onClick={handleDownload}>
            <Download size={14} /> Скачать
          </button>
          <button className="pill pill-outline" onClick={() => setShowQR((p) => !p)}>
            <QrCode size={14} /> QR
          </button>
        </div>

        {showQR && (
          <div className="qr-box animate-in">
            <img src={qrUrl} alt="QR Code" className="qr-img" />
          </div>
        )}
      </div>

      <div className="card">
        <div className="card-title">Инструкция</div>
        <ol className="instruction-list">
          <li>Скопируйте ссылку подключения</li>
          <li>Откройте приложение VPN (v2rayNG, Hiddify, Streisand и др.)</li>
          <li>Импортируйте ссылку из буфера обмена</li>
          <li>Подключитесь к серверу</li>
        </ol>
      </div>
    </div>
  );
}
