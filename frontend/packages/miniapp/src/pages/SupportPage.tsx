import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Ticket, MessageCircle, LifeBuoy, FileText, PenLine, Send, Loader2, ExternalLink, ChevronRight,
} from 'lucide-react';
import { useUserStore } from '@dfc/shared';
import { useTicketStore } from '@dfc/shared';

export default function SupportPage() {
  const navigate = useNavigate();
  const { features, supportUrl, ticketUnread, hasOpenTickets } = useUserStore();
  const { createTicket } = useTicketStore();

  const [showForm, setShowForm] = useState(false);
  const [subject, setSubject] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCreateTicket = async () => {
    if (!subject.trim() || !message.trim() || loading) return;
    setLoading(true);
    setError('');
    try {
      const ticket = await createTicket(subject.trim(), message.trim());
      navigate(`/tickets/${ticket.id}`);
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Не удалось создать тикет');
    } finally {
      setLoading(false);
    }
  };

  const openLink = (url: string) => {
    if (typeof window !== 'undefined' && (window as any).Telegram?.WebApp) {
      (window as any).Telegram.WebApp.openLink(url);
    } else {
      window.open(url, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <div className="animate-in" style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      <h2 className="page-title">Поддержка</h2>

      {/* ── Tickets ── */}
      <div
        className="card card-compact"
        style={{ display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer' }}
        onClick={() => navigate('/tickets')}
      >
        <Ticket size={22} style={{ color: 'var(--gold)', flexShrink: 0 }} />
        <div style={{ flex: 1 }}>
          <div className="fw-600" style={{ fontSize: '0.95rem' }}>Тикеты</div>
          <div className="text-muted" style={{ fontSize: '0.8rem' }}>
            {hasOpenTickets ? 'Есть открытые тикеты' : 'История обращений'}
          </div>
        </div>
        {ticketUnread > 0 && (
          <span className="badge badge-cyan">{ticketUnread > 99 ? '99+' : ticketUnread}</span>
        )}
        <ChevronRight size={16} style={{ color: 'var(--text3)', flexShrink: 0 }} />
      </div>

      {/* ── Community ── */}
      {features?.community_enabled && features.community_url && (
        <div
          className="card card-compact"
          style={{ display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer' }}
          onClick={() => openLink(features.community_url)}
        >
          <MessageCircle size={22} style={{ color: 'var(--cyan)', flexShrink: 0 }} />
          <div style={{ flex: 1 }}>
            <div className="fw-600" style={{ fontSize: '0.95rem' }}>Сообщество</div>
            <div className="text-muted" style={{ fontSize: '0.8rem' }}>Открыть в Telegram</div>
          </div>
          <ExternalLink size={16} style={{ color: 'var(--text3)', flexShrink: 0 }} />
        </div>
      )}

      {/* ── Support URL ── */}
      {supportUrl && (
        <div
          className="card card-compact"
          style={{ display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer' }}
          onClick={() => openLink(supportUrl)}
        >
          <LifeBuoy size={22} style={{ color: 'var(--green)', flexShrink: 0 }} />
          <div style={{ flex: 1 }}>
            <div className="fw-600" style={{ fontSize: '0.95rem' }}>Помощь</div>
            <div className="text-muted" style={{ fontSize: '0.8rem' }}>Написать в поддержку</div>
          </div>
          <ExternalLink size={16} style={{ color: 'var(--text3)', flexShrink: 0 }} />
        </div>
      )}

      {/* ── Terms of Service ── */}
      {features?.tos_enabled && features.tos_url && (
        <div
          className="card card-compact"
          style={{ display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer' }}
          onClick={() => openLink(features.tos_url)}
        >
          <FileText size={22} style={{ color: 'var(--text2)', flexShrink: 0 }} />
          <div style={{ flex: 1 }}>
            <div className="fw-600" style={{ fontSize: '0.95rem' }}>Соглашение</div>
            <div className="text-muted" style={{ fontSize: '0.8rem' }}>Пользовательское соглашение</div>
          </div>
          <ExternalLink size={16} style={{ color: 'var(--text3)', flexShrink: 0 }} />
        </div>
      )}

      {/* ── Create ticket (toggle-form) ── */}
      {!showForm ? (
        <button className="btn btn-outline btn-full" onClick={() => setShowForm(true)}
          style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <PenLine size={18} /> Создать тикет
        </button>
      ) : (
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
            <PenLine size={18} style={{ color: 'var(--green)' }} />
            <span className="fw-600" style={{ fontSize: '0.95rem' }}>Создать тикет</span>
          </div>

          <div className="form-group">
            <label className="form-label">Тема</label>
            <input
              className="input"
              placeholder="Тема обращения"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Сообщение</label>
            <textarea
              className="input"
              placeholder="Опишите проблему..."
              rows={4}
              style={{ resize: 'vertical' }}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />
          </div>

          {error && <div className="text-red" style={{ fontSize: '0.85rem', marginBottom: 10 }}>{error}</div>}

          <div style={{ display: 'flex', gap: 10 }}>
            <button
              className="btn btn-ghost"
              onClick={() => { setShowForm(false); setError(''); setSubject(''); setMessage(''); }}
            >
              Отмена
            </button>
            <button
              className="btn btn-primary"
              style={{ flex: 1 }}
              disabled={!subject.trim() || !message.trim() || loading}
              onClick={handleCreateTicket}
            >
              {loading ? <Loader2 size={18} className="spinner" /> : <Send size={18} />}
              {loading ? 'Отправка...' : 'Отправить'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
