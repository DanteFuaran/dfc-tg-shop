import { useEffect, useState } from 'react';
import { adminApi, TICKET_STATUS_LABELS, formatDate } from '@dfc/shared';
import type { Ticket, TicketMessage } from '@dfc/shared';
import {
  MessageSquare,
  Send,
  Trash2,
  X,
  Edit3,
  ArrowLeft,
  XCircle,
  Image,
} from 'lucide-react';
import toast from 'react-hot-toast';

export default function AdminTickets() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [selected, setSelected] = useState<Ticket | null>(null);
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);
  const [editingMsg, setEditingMsg] = useState<TicketMessage | null>(null);

  const load = async () => {
    try {
      const { data } = await adminApi.listTickets();
      setTickets(data);
    } catch { /* */ }
  };

  const loadTicket = async (id: number) => {
    try {
      const { data } = await adminApi.getTicket(id);
      setSelected(data);
    } catch { /* */ }
  };

  useEffect(() => { load(); }, []);

  const handleReply = async () => {
    if (!selected || !text.trim()) return;
    setSending(true);
    try {
      if (editingMsg) {
        await adminApi.editTicketMessage(selected.id, editingMsg.id, text.trim());
        setEditingMsg(null);
        toast.success('Изменено');
      } else {
        await adminApi.replyTicket(selected.id, text.trim());
      }
      setText('');
      loadTicket(selected.id);
    } catch { toast.error('Ошибка'); } finally { setSending(false); }
  };

  const handleClose = async (id: number) => {
    try {
      await adminApi.closeTicket(id);
      toast.success('Тикет закрыт');
      setSelected(null);
      load();
    } catch { toast.error('Ошибка'); }
  };

  const handleDeleteTicket = async (id: number) => {
    if (!confirm('Удалить тикет?')) return;
    try {
      await adminApi.deleteTicket(id);
      toast.success('Тикет удалён');
      setSelected(null);
      load();
    } catch { toast.error('Ошибка'); }
  };

  const handleDeleteMsg = async (msgId: number) => {
    if (!selected) return;
    try {
      await adminApi.deleteTicketMessage(selected.id, msgId);
      toast.success('Удалено');
      loadTicket(selected.id);
    } catch { toast.error('Ошибка'); }
  };

  /* ─── Detail view ─── */
  if (selected) {
    return (
      <div className="admin-form">
        <button className="back-btn" onClick={() => setSelected(null)}>
          <ArrowLeft size={14} /> Назад
        </button>
        <div className="card">
          <div className="card-row">
            <span className="card-label">Тема</span>
            <span className="card-value">{selected.subject}</span>
          </div>
          <div className="card-row">
            <span className="card-label">Статус</span>
            <span className="card-value">{TICKET_STATUS_LABELS[selected.status]}</span>
          </div>
          <div className="card-row">
            <span className="card-label">Пользователь</span>
            <span className="card-value">{selected.user_telegram_id}</span>
          </div>
        </div>

        <div style={{ display: 'flex', gap: 8 }}>
          {selected.status !== 'CLOSED' && (
            <button className="pill pill-outline" onClick={() => handleClose(selected.id)}>
              <XCircle size={14} /> Закрыть
            </button>
          )}
          <button className="pill pill-outline" onClick={() => handleDeleteTicket(selected.id)}>
            <Trash2 size={14} color="#ef5350" /> Удалить
          </button>
        </div>

        <div className="admin-messages">
          {selected.messages.map((msg) => (
            <div key={msg.id} className={`admin-msg ${msg.sender}`}>
              {msg.image_url && <img src={msg.image_url} alt="" style={{ maxWidth: '100%', borderRadius: 8, marginBottom: 4 }} />}
              <div className="admin-msg-text">{msg.text}</div>
              <div className="admin-msg-meta">
                <span>{formatDate(msg.created_at)}</span>
                <span>{msg.sender === 'admin' ? 'Админ' : 'Пользователь'}</span>
                {msg.sender === 'admin' && (
                  <span className="admin-msg-actions">
                    <button onClick={() => { setEditingMsg(msg); setText(msg.text); }}>
                      <Edit3 size={12} />
                    </button>
                    <button onClick={() => handleDeleteMsg(msg.id)}>
                      <Trash2 size={12} />
                    </button>
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>

        {selected.status !== 'CLOSED' && (
          <div style={{ display: 'flex', gap: 8 }}>
            <input
              className="input"
              style={{ flex: 1 }}
              placeholder={editingMsg ? 'Новый текст...' : 'Ответ...'}
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleReply()}
            />
            {editingMsg && (
              <button className="pill pill-outline" onClick={() => { setEditingMsg(null); setText(''); }}>
                <X size={14} />
              </button>
            )}
            <button className="pill pill-cyan" disabled={sending} onClick={handleReply}>
              <Send size={14} />
            </button>
          </div>
        )}
      </div>
    );
  }

  /* ─── List view ─── */
  return (
    <>
      {tickets.length === 0 ? (
        <div className="empty-state"><MessageSquare size={32} /> Нет тикетов</div>
      ) : (
        <div className="admin-list">
          {tickets.map((t) => (
            <div key={t.id} className="admin-list-item" onClick={() => loadTicket(t.id)}>
              <div>
                <div className="admin-item-name">{t.subject}</div>
                <div className="admin-item-sub">
                  #{t.id} · {TICKET_STATUS_LABELS[t.status]} · {formatDate(t.created_at)}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </>
  );
}
