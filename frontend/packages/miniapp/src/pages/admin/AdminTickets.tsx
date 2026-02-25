import { useEffect, useRef, useState } from 'react';
import { ArrowLeft, Send, Trash2, XCircle, Ticket as TicketIcon, MessageSquare } from 'lucide-react';
import { adminApi, formatDate, TICKET_STATUS_LABELS } from '@dfc/shared';
import type { Ticket } from '@dfc/shared';

const statusBadge: Record<string, string> = {
  OPEN: 'badge badge-cyan',
  ANSWERED: 'badge badge-green',
  WAITING: 'badge badge-gold',
  CLOSED: 'badge',
};

type Tab = 'ALL' | 'OPEN' | 'WAITING' | 'CLOSED';
const tabs: { key: Tab; label: string }[] = [
  { key: 'ALL', label: 'Все' },
  { key: 'OPEN', label: 'Открытые' },
  { key: 'WAITING', label: 'Ожидающие' },
  { key: 'CLOSED', label: 'Закрытые' },
];

const bubbleAdmin: React.CSSProperties = {
  alignSelf: 'flex-end',
  background: 'var(--bg-raised)',
  border: '1px solid var(--border-accent)',
  borderRadius: '12px 12px 4px 12px',
  padding: '10px 14px',
  maxWidth: '80%',
};

const bubbleUser: React.CSSProperties = {
  alignSelf: 'flex-start',
  background: 'var(--bg-card)',
  border: '1px solid var(--border)',
  borderRadius: '12px 12px 12px 4px',
  padding: '10px 14px',
  maxWidth: '80%',
};

export default function AdminTickets() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<Tab>('ALL');
  const [selected, setSelected] = useState<Ticket | null>(null);
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  const load = async () => {
    setLoading(true);
    try {
      const { data } = await adminApi.listTickets();
      setTickets(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [selected?.messages]);

  const filtered = tab === 'ALL' ? tickets : tickets.filter((t) => t.status === tab);

  const openTicket = async (t: Ticket) => {
    const { data: full } = await adminApi.getTicket(t.id);
    setSelected(full);
    setConfirmDelete(false);
  };

  const handleReply = async () => {
    if (!text.trim() || !selected || sending) return;
    setSending(true);
    try {
      await adminApi.replyTicket(selected.id, text.trim());
      const { data: updated } = await adminApi.getTicket(selected.id);
      setSelected(updated);
      setTickets((prev) => prev.map((t) => (t.id === updated.id ? updated : t)));
      setText('');
    } finally {
      setSending(false);
    }
  };

  const handleClose = async () => {
    if (!selected) return;
    await adminApi.closeTicket(selected.id);
    const { data: updated } = await adminApi.getTicket(selected.id);
    setSelected(updated);
    setTickets((prev) => prev.map((t) => (t.id === updated.id ? updated : t)));
  };

  const handleDelete = async () => {
    if (!selected) return;
    await adminApi.deleteTicket(selected.id);
    setTickets((prev) => prev.filter((t) => t.id !== selected.id));
    setSelected(null);
  };

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleReply(); }
  };

  /* ── Detail view ─────────────────────────────── */
  if (selected) {
    const isClosed = selected.status === 'CLOSED';
    return (
      <div style={{ display: 'flex', flexDirection: 'column', height: '100dvh', maxWidth: 'var(--max-w)', margin: '0 auto' }}>
        <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: 10, flexShrink: 0 }}>
          <button className="back-btn" onClick={() => setSelected(null)}><ArrowLeft size={18} /></button>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div className="truncate" style={{ fontWeight: 600, fontSize: '0.95rem' }}>{selected.subject}</div>
            {selected.user_telegram_id && (
              <div style={{ fontSize: '0.78rem', color: 'var(--text3)' }}>TG: {selected.user_telegram_id}</div>
            )}
          </div>
          <span className={statusBadge[selected.status] ?? 'badge'}>
            {TICKET_STATUS_LABELS[selected.status] ?? selected.status}
          </span>
        </div>

        <div style={{ flex: 1, overflowY: 'auto', padding: 16, display: 'flex', flexDirection: 'column', gap: 10 }}>
          {selected.messages.map((msg) => {
            const isAdmin = msg.sender === 'admin';
            return (
              <div key={msg.id} className="animate-fade" style={isAdmin ? bubbleAdmin : bubbleUser}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text3)', marginBottom: 4 }}>
                  {isAdmin ? 'Вы (админ)' : 'Пользователь'}
                </div>
                {msg.image_url && <img src={msg.image_url} alt="" style={{ borderRadius: 8, marginBottom: 6, maxWidth: '100%' }} />}
                <div style={{ fontSize: '0.9rem', whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>{msg.text}</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text3)', marginTop: 4, textAlign: isAdmin ? 'right' : 'left' }}>
                  {formatDate(msg.created_at)}
                </div>
              </div>
            );
          })}
          <div ref={bottomRef} />
        </div>

        <div style={{ padding: '10px 16px', borderTop: '1px solid var(--border)', flexShrink: 0, paddingBottom: 'calc(10px + var(--safe-bottom))' }}>
          {!isClosed && (
            <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 8 }}>
              <input className="input" placeholder="Ответить…" value={text} onChange={(e) => setText(e.target.value)} onKeyDown={handleKey} style={{ flex: 1 }} />
              <button className="btn btn-primary btn-sm" disabled={!text.trim() || sending} onClick={handleReply} style={{ padding: '10px 14px' }}>
                <Send size={18} />
              </button>
            </div>
          )}
          <div style={{ display: 'flex', gap: 8 }}>
            {!isClosed && (
              <button className="btn btn-secondary btn-sm" onClick={handleClose} style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6 }}>
                <XCircle size={16} /> Закрыть тикет
              </button>
            )}
            {!confirmDelete ? (
              <button className="btn btn-danger btn-sm" onClick={() => setConfirmDelete(true)} style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6 }}>
                <Trash2 size={16} /> Удалить
              </button>
            ) : (
              <button className="btn btn-danger btn-sm" onClick={handleDelete} style={{ flex: 1 }}>
                Подтвердить удаление
              </button>
            )}
          </div>
        </div>
      </div>
    );
  }

  /* ── List view ───────────────────────────────── */
  return (
    <div style={{ padding: 16, maxWidth: 'var(--max-w)', margin: '0 auto' }}>
      <h1 className="page-title" style={{ marginBottom: 12 }}>Тикеты</h1>

      <div style={{ display: 'flex', gap: 6, marginBottom: 14, overflowX: 'auto' }}>
        {tabs.map((t) => (
          <button key={t.key} className={`btn btn-sm ${tab === t.key ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setTab(t.key)}>
            {t.label}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="loading"><div className="spinner" /><span>Загрузка…</span></div>
      ) : filtered.length === 0 ? (
        <div className="empty-state">
          <TicketIcon size={32} style={{ marginBottom: 8, opacity: 0.5 }} />
          <p>Нет тикетов</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {filtered.map((ticket, i) => (
            <div key={ticket.id} className="card animate-in" style={{ cursor: 'pointer', animationDelay: `${i * 0.03}s` }} onClick={() => openTicket(ticket)}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                <span style={{ fontWeight: 600, fontSize: '0.95rem' }} className="truncate">{ticket.subject}</span>
                <span className={statusBadge[ticket.status] ?? 'badge'}>
                  {TICKET_STATUS_LABELS[ticket.status] ?? ticket.status}
                </span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', color: 'var(--text2)' }}>
                <span>{ticket.user_telegram_id ? `TG: ${ticket.user_telegram_id}` : '—'}</span>
                <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                  <MessageSquare size={13} /> {ticket.messages?.length ?? 0}
                </span>
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text3)', marginTop: 4 }}>{formatDate(ticket.created_at)}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
