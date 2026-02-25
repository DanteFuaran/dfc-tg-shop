import { useEffect, useRef, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Send } from 'lucide-react';
import { useTicketStore, formatDate, TICKET_STATUS_LABELS } from '@dfc/shared';

const statusBadge: Record<string, string> = {
  OPEN: 'badge badge-cyan',
  ANSWERED: 'badge badge-green',
  WAITING: 'badge badge-gold',
  CLOSED: 'badge',
};

const bubbleUser: React.CSSProperties = {
  alignSelf: 'flex-end',
  background: 'var(--bg-raised)',
  border: '1px solid var(--border-accent)',
  borderRadius: '12px 12px 4px 12px',
  padding: '10px 14px',
  maxWidth: '80%',
};

const bubbleAdmin: React.CSSProperties = {
  alignSelf: 'flex-start',
  background: 'var(--bg-card)',
  border: '1px solid var(--border)',
  borderRadius: '12px 12px 12px 4px',
  padding: '10px 14px',
  maxWidth: '80%',
};

export default function TicketChatPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { currentTicket, isLoading, fetchTicket, reply } = useTicketStore();
  const bottomRef = useRef<HTMLDivElement>(null);
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);

  useEffect(() => {
    if (id) fetchTicket(Number(id));
  }, [id, fetchTicket]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [currentTicket?.messages]);

  const isClosed = currentTicket?.status === 'CLOSED';

  const handleSend = async () => {
    if (!text.trim() || !id || sending) return;
    setSending(true);
    try {
      await reply(Number(id), text.trim());
      setText('');
    } finally {
      setSending(false);
    }
  };

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (isLoading || !currentTicket) {
    return (
      <div style={{ padding: 16, maxWidth: 'var(--max-w)', margin: '0 auto' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
          <button className="back-btn" onClick={() => navigate('/tickets')}>
            <ArrowLeft size={18} />
          </button>
          <span className="page-title" style={{ margin: 0 }}>Загрузка…</span>
        </div>
        <div className="loading">
          <div className="spinner" />
        </div>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100dvh', maxWidth: 'var(--max-w)', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: 10, flexShrink: 0 }}>
        <button className="back-btn" onClick={() => navigate('/tickets')}>
          <ArrowLeft size={18} />
        </button>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div className="truncate" style={{ fontWeight: 600, fontSize: '0.95rem' }}>
            {currentTicket.subject}
          </div>
        </div>
        <span className={statusBadge[currentTicket.status] ?? 'badge'}>
          {TICKET_STATUS_LABELS[currentTicket.status] ?? currentTicket.status}
        </span>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: 'auto', padding: 16, display: 'flex', flexDirection: 'column', gap: 10 }}>
        {currentTicket.messages.map((msg) => {
          const isUser = msg.sender === 'user';
          return (
            <div key={msg.id} className="animate-fade" style={isUser ? bubbleUser : bubbleAdmin}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text3)', marginBottom: 4 }}>
                {isUser ? 'Вы' : 'Поддержка'}
              </div>
              {msg.image_url && (
                <img
                  src={msg.image_url}
                  alt=""
                  style={{ borderRadius: 8, marginBottom: 6, maxWidth: '100%' }}
                />
              )}
              <div style={{ fontSize: '0.9rem', whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                {msg.text}
              </div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text3)', marginTop: 4, textAlign: isUser ? 'right' : 'left' }}>
                {formatDate(msg.created_at)}
              </div>
            </div>
          );
        })}
        <div ref={bottomRef} />
      </div>

      {/* Input / Closed */}
      <div style={{ padding: '10px 16px', borderTop: '1px solid var(--border)', flexShrink: 0, paddingBottom: 'calc(10px + var(--safe-bottom))' }}>
        {isClosed ? (
          <div style={{ textAlign: 'center', color: 'var(--text3)', fontSize: '0.88rem', padding: '6px 0' }}>
            Тикет закрыт
          </div>
        ) : (
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <input
              className="input"
              placeholder="Написать сообщение…"
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={handleKey}
              style={{ flex: 1 }}
            />
            <button
              className="btn btn-primary btn-sm"
              disabled={!text.trim() || sending}
              onClick={handleSend}
              style={{ padding: '10px 14px' }}
            >
              <Send size={18} />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
