import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, MessageSquare } from 'lucide-react';
import { useTicketStore, formatDate, TICKET_STATUS_LABELS } from '@dfc/shared';

const statusBadge: Record<string, string> = {
  OPEN: 'badge badge-cyan',
  ANSWERED: 'badge badge-green',
  WAITING: 'badge badge-gold',
  CLOSED: 'badge',
};

export default function TicketsListPage() {
  const navigate = useNavigate();
  const { tickets, isLoading, fetchTickets } = useTicketStore();

  useEffect(() => {
    fetchTickets();
  }, [fetchTickets]);

  return (
    <div style={{ padding: '16px', maxWidth: 'var(--max-w)', margin: '0 auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
        <button className="back-btn" onClick={() => navigate('/support')}>
          <ArrowLeft size={18} />
        </button>
        <h1 className="page-title" style={{ margin: 0 }}>Мои обращения</h1>
      </div>

      {isLoading ? (
        <div className="loading">
          <div className="spinner" />
          <span>Загрузка…</span>
        </div>
      ) : tickets.length === 0 ? (
        <div className="empty-state">
          <MessageSquare size={32} style={{ marginBottom: 8, opacity: 0.5 }} />
          <p>У вас нет обращений</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {tickets.map((ticket, i) => {
            const lastMsg = ticket.messages?.[ticket.messages.length - 1];
            return (
              <div
                key={ticket.id}
                className="card animate-in"
                style={{ cursor: 'pointer', animationDelay: `${i * 0.03}s` }}
                onClick={() => navigate(`/tickets/${ticket.id}`)}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                  <span style={{ fontWeight: 600, fontSize: '0.95rem' }} className="truncate">
                    {ticket.subject}
                  </span>
                  <span className={statusBadge[ticket.status] ?? 'badge'}>
                    {TICKET_STATUS_LABELS[ticket.status] ?? ticket.status}
                  </span>
                </div>
                <div style={{ fontSize: '0.82rem', color: 'var(--text2)', marginBottom: 4 }}>
                  {formatDate(ticket.created_at)}
                </div>
                {lastMsg && (
                  <p className="truncate" style={{ fontSize: '0.84rem', color: 'var(--text3)', margin: 0 }}>
                    {lastMsg.text}
                  </p>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
