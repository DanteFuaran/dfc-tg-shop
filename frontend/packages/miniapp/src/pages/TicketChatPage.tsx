import { useEffect, useRef, useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTicketStore, formatDate, escapeHtml } from '@dfc/shared';
import type { TicketMessage } from '@dfc/shared';
import {
  ArrowLeft,
  Send,
  Image,
  X,
  Edit3,
  Trash2,
  MoreVertical,
  XCircle,
} from 'lucide-react';
import toast from 'react-hot-toast';
import './TicketChatPage.css';

export default function TicketChatPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const ticketId = Number(id);
  const { currentTicket, fetchTicket, reply, editMessage, deleteMessage, closeTicket } =
    useTicketStore();

  const [text, setText] = useState('');
  const [imageData, setImageData] = useState<string | null>(null);
  const [sending, setSending] = useState(false);
  const [editingMsg, setEditingMsg] = useState<TicketMessage | null>(null);
  const [contextMsg, setContextMsg] = useState<TicketMessage | null>(null);
  const [contextPos, setContextPos] = useState({ x: 0, y: 0 });
  const [showClose, setShowClose] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (ticketId) fetchTicket(ticketId);
  }, [ticketId, fetchTicket]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [currentTicket?.messages]);

  /* ─── Paste image ─── */
  const handlePaste = useCallback((e: React.ClipboardEvent) => {
    const items = e.clipboardData?.items;
    if (!items) return;
    for (const item of items) {
      if (item.type.startsWith('image/')) {
        e.preventDefault();
        const blob = item.getAsFile();
        if (!blob) return;
        const reader = new FileReader();
        reader.onload = () => setImageData(reader.result as string);
        reader.readAsDataURL(blob);
        return;
      }
    }
  }, []);

  /* ─── File picker ─── */
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !file.type.startsWith('image/')) return;
    const reader = new FileReader();
    reader.onload = () => setImageData(reader.result as string);
    reader.readAsDataURL(file);
    e.target.value = '';
  };

  /* ─── Send / Edit ─── */
  const handleSend = async () => {
    const trimmed = text.trim();
    if (!trimmed && !imageData) return;
    setSending(true);
    try {
      if (editingMsg) {
        await editMessage(ticketId, editingMsg.id, trimmed);
        setEditingMsg(null);
        toast.success('Сообщение изменено');
      } else {
        await reply(ticketId, trimmed, imageData ?? undefined);
        setImageData(null);
      }
      setText('');
    } catch (e: any) {
      toast.error(e?.response?.data?.detail ?? 'Ошибка');
    } finally {
      setSending(false);
    }
  };

  /* ─── Context menu ─── */
  const handleContextMenu = (e: React.MouseEvent | React.TouchEvent, msg: TicketMessage) => {
    if (msg.sender !== 'user') return;
    e.preventDefault();
    let clientX: number, clientY: number;
    if ('touches' in e && e.touches.length > 0) {
      clientX = e.touches[0]!.clientX;
      clientY = e.touches[0]!.clientY;
    } else if ('clientX' in e) {
      clientX = e.clientX;
      clientY = e.clientY;
    } else {
      return;
    }
    setContextPos({ x: clientX, y: clientY });
    setContextMsg(msg);
  };

  const handleEdit = () => {
    if (!contextMsg) return;
    setEditingMsg(contextMsg);
    setText(contextMsg.text);
    setContextMsg(null);
    inputRef.current?.focus();
  };

  const handleDelete = async () => {
    if (!contextMsg) return;
    try {
      await deleteMessage(ticketId, contextMsg.id);
      toast.success('Сообщение удалено');
    } catch {
      toast.error('Ошибка удаления');
    }
    setContextMsg(null);
  };

  const handleClose = async () => {
    try {
      await closeTicket(ticketId, 'Закрыто пользователем');
      toast.success('Тикет закрыт');
      navigate('/tickets');
    } catch {
      toast.error('Ошибка');
    }
    setShowClose(false);
  };

  if (!currentTicket) {
    return <div className="ticket-chat-page animate-in"><div className="empty-state">Загрузка...</div></div>;
  }

  const isClosed = currentTicket.status === 'CLOSED';

  return (
    <div className="ticket-chat-page">
      {/* Header */}
      <div className="chat-header">
        <button className="chat-back" onClick={() => navigate('/tickets')}>
          <ArrowLeft size={20} />
        </button>
        <div className="chat-header-info">
          <span className="chat-subject">{currentTicket.subject}</span>
          <span className="chat-status">#{currentTicket.id}</span>
        </div>
        {!isClosed && (
          <button className="chat-close-btn" onClick={() => setShowClose(true)}>
            <XCircle size={20} />
          </button>
        )}
      </div>

      {/* Messages */}
      <div className="chat-messages">
        {currentTicket.messages.map((msg) => (
          <div
            key={msg.id}
            className={`chat-bubble ${msg.sender === 'user' ? 'bubble-user' : 'bubble-admin'}`}
            onContextMenu={(e) => handleContextMenu(e, msg)}
          >
            {msg.image_url && (
              <img src={msg.image_url} alt="" className="bubble-image" />
            )}
            {msg.text && (
              <div
                className="bubble-text"
                dangerouslySetInnerHTML={{ __html: escapeHtml(msg.text).replace(/\n/g, '<br/>') }}
              />
            )}
            <div className="bubble-time">{formatDate(msg.created_at)}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Context menu */}
      {contextMsg && (
        <>
          <div className="ctx-overlay" onClick={() => setContextMsg(null)} />
          <div
            className="ctx-menu"
            style={{ top: contextPos.y, left: Math.min(contextPos.x, window.innerWidth - 160) }}
          >
            <button className="ctx-item" onClick={handleEdit}>
              <Edit3 size={14} /> Изменить
            </button>
            <button className="ctx-item ctx-danger" onClick={handleDelete}>
              <Trash2 size={14} /> Удалить
            </button>
          </div>
        </>
      )}

      {/* Close confirm */}
      {showClose && (
        <div className="modal-overlay" onClick={() => setShowClose(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <p>Закрыть обращение?</p>
            <div style={{ display: 'flex', gap: 8 }}>
              <button className="btn btn-full" onClick={() => setShowClose(false)}>Отмена</button>
              <button className="btn btn-primary btn-full" onClick={handleClose}>Закрыть</button>
            </div>
          </div>
        </div>
      )}

      {/* Image preview */}
      {imageData && (
        <div className="image-preview">
          <img src={imageData} alt="preview" />
          <button className="image-preview-close" onClick={() => setImageData(null)}>
            <X size={16} />
          </button>
        </div>
      )}

      {/* Edit indicator */}
      {editingMsg && (
        <div className="edit-indicator">
          <Edit3 size={14} />
          <span>Редактирование</span>
          <button onClick={() => { setEditingMsg(null); setText(''); }}>
            <X size={14} />
          </button>
        </div>
      )}

      {/* Input */}
      {!isClosed && (
        <div className="chat-input-bar">
          <input
            type="file"
            accept="image/*"
            ref={fileInputRef}
            style={{ display: 'none' }}
            onChange={handleFileSelect}
          />
          <button className="chat-attach" onClick={() => fileInputRef.current?.click()}>
            <Image size={20} />
          </button>
          <textarea
            ref={inputRef}
            className="chat-input"
            placeholder="Сообщение..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            onPaste={handlePaste}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            rows={1}
          />
          <button
            className="chat-send"
            disabled={sending || (!text.trim() && !imageData)}
            onClick={handleSend}
          >
            <Send size={20} />
          </button>
        </div>
      )}
    </div>
  );
}
