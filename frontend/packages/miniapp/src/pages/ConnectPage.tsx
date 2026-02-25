import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Copy, Check, ExternalLink, Smartphone, Monitor, ChevronDown, ChevronUp, Download, Link2 } from 'lucide-react';
import { useUserStore, copyToClipboard } from '@dfc/shared';

interface SpoilerProps {
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
}

function Spoiler({ title, icon, children }: SpoilerProps) {
  const [open, setOpen] = useState(false);
  return (
    <div className={`spoiler${open ? ' open' : ''}`}>
      <div className="spoiler-header" onClick={() => setOpen(!open)}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          {icon}
          <span className="fw-600" style={{ fontSize: '0.9rem' }}>{title}</span>
        </div>
        {open ? <ChevronUp size={16} color="var(--text2)" /> : <ChevronDown size={16} color="var(--text2)" />}
      </div>
      <div className="spoiler-body">
        <div style={{ padding: '12px 14px', fontSize: '0.85rem', color: 'var(--text2)', lineHeight: 1.7 }}>
          {children}
        </div>
      </div>
    </div>
  );
}

export default function ConnectPage() {
  const navigate = useNavigate();
  const { subscription } = useUserStore();
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    if (!subscription?.url) return;
    const ok = await copyToClipboard(subscription.url);
    if (ok) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  /* No subscription — empty state */
  if (!subscription || subscription.status !== 'ACTIVE') {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <h1 className="page-title animate-in">Подключение</h1>
        <div className="empty-state animate-in">
          <Link2 size={36} color="var(--text3)" style={{ margin: '0 auto 12px' }} />
          <p>У вас нет активной подписки</p>
          <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => navigate('/plans')}>
            Выбрать тариф
          </button>
        </div>
      </div>
    );
  }

  const subUrl = subscription.url;
  const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&bgcolor=080C14&color=24C4F1&data=${encodeURIComponent(subUrl)}`;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      <h1 className="page-title animate-in">Подключение</h1>

      {/* Subscription URL */}
      <div className="card animate-in">
        <div className="card-title">Ссылка подписки</div>
        <div
          className="mono"
          style={{
            background: 'var(--bg-input)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--r-sm)',
            padding: '10px 12px',
            fontSize: '0.78rem',
            wordBreak: 'break-all',
            color: 'var(--cyan)',
            marginBottom: 12,
          }}
        >
          {subUrl}
        </div>
        <button className="btn btn-primary btn-full" onClick={handleCopy}>
          {copied ? <><Check size={16} /> Скопировано</> : <><Copy size={16} /> Копировать ссылку</>}
        </button>
      </div>

      {/* QR */}
      <div className="card animate-in" style={{ textAlign: 'center' }}>
        <div className="card-title">QR-код</div>
        <img
          src={qrUrl}
          alt="QR"
          width={180}
          height={180}
          style={{ margin: '0 auto', borderRadius: 8 }}
        />
        <p style={{ color: 'var(--text2)', fontSize: '0.8rem', marginTop: 10 }}>
          Отсканируйте в приложении для подключения
        </p>
      </div>

      {/* Instructions */}
      <h2 className="page-title animate-in" style={{ fontSize: '0.95rem', marginTop: 8 }}>
        Инструкции по подключению
      </h2>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        <Spoiler title="V2RayNG — Android" icon={<Smartphone size={16} color="var(--green)" />}>
          <ol style={{ paddingLeft: 18 }}>
            <li>
              Скачайте{' '}
              <a href="https://play.google.com/store/apps/details?id=com.v2ray.ang" target="_blank" rel="noreferrer">
                V2RayNG <ExternalLink size={12} style={{ verticalAlign: -1 }} />
              </a>
            </li>
            <li>Скопируйте ссылку подписки выше</li>
            <li>Откройте приложение → <b>+</b> → <b>Импорт из буфера</b></li>
            <li>Нажмите кнопку подключения ▶</li>
          </ol>
        </Spoiler>

        <Spoiler title="Streisand — iOS" icon={<Smartphone size={16} color="var(--cyan)" />}>
          <ol style={{ paddingLeft: 18 }}>
            <li>
              Установите{' '}
              <a href="https://apps.apple.com/app/streisand/id6450534064" target="_blank" rel="noreferrer">
                Streisand <ExternalLink size={12} style={{ verticalAlign: -1 }} />
              </a>
            </li>
            <li>Скопируйте ссылку подписки</li>
            <li>Откройте приложение → перейдите на вкладку подписок</li>
            <li>Нажмите <b>+</b>, вставьте ссылку и сохраните</li>
            <li>Включите VPN на главном экране</li>
          </ol>
        </Spoiler>

        <Spoiler title="Hiddify — Windows / macOS" icon={<Monitor size={16} color="var(--gold)" />}>
          <ol style={{ paddingLeft: 18 }}>
            <li>
              Скачайте{' '}
              <a href="https://github.com/hiddify/hiddify-app/releases" target="_blank" rel="noreferrer">
                Hiddify <ExternalLink size={12} style={{ verticalAlign: -1 }} />
              </a>
            </li>
            <li>Скопируйте ссылку подписки</li>
            <li>Откройте Hiddify → <b>New Profile</b> → вставьте ссылку</li>
            <li>Нажмите <b>Connect</b></li>
          </ol>
        </Spoiler>
      </div>
    </div>
  );
}
