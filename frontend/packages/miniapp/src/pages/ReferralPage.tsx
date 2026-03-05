import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, Share2, Copy, Check, ChevronLeft } from 'lucide-react';
import { useUserStore, copyToClipboard } from '@dfc/shared';

export default function ReferralPage() {
  const navigate = useNavigate();
  const { user, features, refLink } = useUserStore();
  const [copied, setCopied] = useState(false);

  if (!features?.referral_enabled || !refLink) {
    return (
      <div className="animate-in">
        <h2 className="page-title">Пригласить друга</h2>
        <div className="card empty-state" style={{ textAlign: 'center', padding: '32px 16px' }}>
          <Users size={32} style={{ margin: '0 auto 12px', color: 'var(--text3)' }} />
          <p style={{ color: 'var(--text2)' }}>Реферальная программа недоступна</p>
        </div>
      </div>
    );
  }

  const handleCopy = () => {
    copyToClipboard(refLink);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleShare = () => {
    const tg = (window as any).Telegram?.WebApp;
    if (tg?.switchInlineQuery) {
      tg.switchInlineQuery(refLink, ['users', 'groups', 'channels', 'bots']);
    } else {
      // Fallback: copy to clipboard
      handleCopy();
    }
  };

  return (
    <div className="animate-in" style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <button
          onClick={() => navigate('/')}
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--text2)',
            cursor: 'pointer',
            padding: '4px',
            display: 'flex',
            alignItems: 'center',
          }}
        >
          <ChevronLeft size={20} />
        </button>
        <h2 className="page-title" style={{ margin: 0 }}>Пригласить друга</h2>
      </div>

      {/* Info card */}
      <div className="card" style={{ padding: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
          <Users size={20} style={{ color: 'var(--text2)', flexShrink: 0, marginTop: 2 }} />
          <p style={{ color: 'var(--text2)', fontSize: '.9rem', lineHeight: 1.5 }}>
            Поделитесь ссылкой с другом. Когда он купит подписку, вы получите вознаграждение.
          </p>
        </div>
      </div>

      {/* Ref link card */}
      <div
        className="card"
        onClick={handleCopy}
        style={{
          padding: '14px 16px',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 10,
        }}
      >
        <span
          style={{
            fontSize: '.85rem',
            color: 'var(--text2)',
            overflowX: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            fontFamily: 'var(--font-mono)',
          }}
        >
          {refLink}
        </span>
        {copied
          ? <Check size={16} style={{ color: 'var(--green)', flexShrink: 0 }} />
          : <Copy size={16} style={{ color: 'var(--text3)', flexShrink: 0 }} />
        }
      </div>

      {/* Action buttons */}
      <button className="btn btn-primary btn-full" onClick={handleShare}>
        <Share2 size={18} />
        Поделиться
      </button>

      <button
        className="btn btn-full"
        onClick={handleCopy}
        style={{ background: 'var(--bg-card)', border: '1px solid var(--border)' }}
      >
        {copied ? <Check size={18} /> : <Copy size={18} />}
        {copied ? 'Скопировано!' : 'Скопировать ссылку'}
      </button>
    </div>
  );
}
