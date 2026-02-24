import { useEffect, useState } from 'react';
import { useTicketStore, TICKET_STATUS_LABELS, formatDate } from '@dfc/shared';
import { useNavigate } from 'react-router-dom';
import {
  MessageSquare,
  Plus,
  Clock,
  CheckCircle2,
  AlertCircle,
  X,
} from 'lucide-react';
import './TicketsListPage.css';

const STATUS_ICONS: Record<string, React.ReactNode> = {
  OPEN: <AlertCircle size={14} />,
  ANSWERED: <CheckCircle2 size={14} />,
  WAITING: <Clock size={14} />,
  CLOSED: <X size={14} />,
};

export default function TicketsListPage() {
  const { tickets, fetchTickets } = useTicketStore();
  const navigate = useNavigate();
  const [showCreate, setShowCreate] = useState(false);
  const [subject, setSubject] = useState('');
  const [message, setMessage] = useState('');
  const [creating, setCreating] = useState(false);
  const { createTicket } = useTicketStore();

  useEffect(() => {
    fetchTickets();
  }, [fetchTickets]);

  const handleCreate = async () => {
    if (!subject.trim() || !message.trim()) return;
    setCreating(true);
    try {
      const ticket = await createTicket(subject.trim(), message.trim());
      if (ticket) {
        setShowCreate(false);
        setSubject('');
        setMessage('');
        navigate(`/tickets/${ticket.id}`);
      }
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="tickets-list-page animate-in">
      <div className="tickets-header">
        <h2 className="page-title"><MessageSquare size={20} /> Обращения</h2>
        <button
          className="pill pill-cyan"
          onClick={() => setShowCreate(true)}
        >
          <Plus size={14} /> Новое
        </button>
      </div>

      {/* Create modal */}
      {showCreate && (
        <div className="modal-overlay" onClick={() => setShowCreate(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <span>Новое обращение</span>
              <button className="modal-close" onClick={() => setShowCreate(false)}>
                <X size={18} />
              </button>
            </div>
            <input
              type="text"
              className="input"
              placeholder="Тема"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              autoComplete="off"
            />
            <textarea
              className="input ticket-textarea"
              placeholder="Опишите проблему..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows={4}
            />
            <button
              className="btn btn-primary btn-full btn-glossy"
              disabled={creating || !subject.trim() || !message.trim()}
              onClick={handleCreate}
            >
              {creating ? 'Создание...' : 'Создать'}
            </button>
          </div>
        </div>
      )}

      {/* Ticket list */}
      {tickets.length === 0 ? (
        <div className="empty-state">
          <MessageSquare size={40} />
          <p>Нет обращений</p>
        </div>
      ) : (
        <div className="tickets-list">
          {tickets.map((t) => (
            <div
              key={t.id}
              className="ticket-item card"
              onClick={() => navigate(`/tickets/${t.id}`)}
            >
              <div className="ticket-item-top">
                <span className="ticket-subject">{t.subject}</span>
                <span className={`ticket-status status-${t.status.toLowerCase()}`}>
                  {STATUS_ICONS[t.status]}
                  {TICKET_STATUS_LABELS[t.status]}
                </span>
              </div>
              <div className="ticket-item-meta">
                <span>#{t.id}</span>
                <span>{formatDate(t.created_at)}</span>
                <span>{t.messages.length} сообщ.</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
