import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Mail, MessageSquare, PenLine, Send, Loader2, ExternalLink,
  ChevronRight, Paperclip, X, LifeBuoy, FileText, MessageCircle,
} from 'lucide-react';
import { useUserStore, userApi } from '@dfc/shared';
import { useTicketStore } from '@dfc/shared';
import type { UserBroadcastMessage } from '@dfc/shared';

export default function SupportPage() {
  const navigate = useNavigate();
  const { features, supportUrl, ticketUnread, hasOpenTickets } = useUserStore();
  const { createTicket } = useTicketStore();

  /* ── Messages (broadcasts) ── */
  const [messages, setMessages] = useState<UserBroadcastMessage[]>([]);
  const [msgsLoading, setMsgsLoading] = useState(true);

  const loadMessages = useCallback(async () => {
    setMsgsLoading(true);
    try {
      const { data } = await userApi.getMessages();
      setMessages(Array.isArray(data) ? data : []);
    } catch { /* ignore */ }
    finally { setMsgsLoading(false); }
  }, []);

  useEffect(() => { loadMessages(); }, [loadMessages]);

  /* ── Create appeal form ── */
  const [showForm, setShowForm] = useState(false);
  const [subject, setSubject] = useState('');
  const [message, setMessage] = useState('');
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [imageData, setImageData] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) {
      setError('Файл слишком большой (макс. 5 МБ)');
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      const base64 = reader.result as string;
      setImagePreview(base64);
      setImageData(base64);
    };
    reader.readAsDataURL(file);
  };

  const clearImage = () => { setImagePreview(null); setImageData(null); };

  const handleCreateTicket = async () => {
    if (!subject.trim() || !message.trim() || loading) return;
    setLoading(true);
    setError('');
    try {
      const ticket = await createTicket(subject.trim(), message.trim(), imageData || undefined);
      navigate(`/tickets/${ticket.id}`);
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Не удалось создать обращение');
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

  const sentMessages = messages.filter(m => m.status === 'SENT');

  return (
    <div className="animate-in" style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      <h2 className="page-title">Поддержка</h2>

      {/* ── Сообщения (Broadcasts) ── */}
      <div
        className="card card-compact"
        style={{ display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer' }}
        onClick={() => navigate('/messages')}
      >
        <Mail size={22} style={{ color: 'var(--cyan)', flexShrink: 0 }} />
        <div style={{ flex: 1 }}>
          <div className="fw-600" style={{ fontSize: '0.95rem' }}>Сообщения</div>
          <div className="text-muted" style={{ fontSize: '0.8rem' }}>
            {msgsLoading ? 'Загрузка...' : sentMessages.length > 0 ? `${sentMessages.length} сообщ.` : 'Нет сообщений'}
          </div>
        </div>
        {sentMessages.length > 0 && (
          <span className="badge badge-cyan">{sentMessages.length > 99 ? '99+' : sentMessages.length}</span>
        )}
        <ChevronRight size={16} style={{ color: 'var(--text3)', flexShrink: 0 }} />
      </div>

      {/* ── Обращения (Tickets) ── */}
      <div
        className="card card-compact"
        style={{ display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer' }}
        onClick={() => navigate('/tickets')}
      >
        <MessageSquare size={22} style={{ color: 'var(--gold)', flexShrink: 0 }} />
        <div style={{ flex: 1 }}>
          <div className="fw-600" style={{ fontSize: '0.95rem' }}>Обращения</div>
          <div className="text-muted" style={{ fontSize: '0.8rem' }}>
            {hasOpenTickets ? 'Есть открытые обращения' : 'История обращений'}
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

      {/* ── Create Appeal Form ── */}
      {!showForm ? (
        <button className="btn btn-outline btn-full" onClick={() => setShowForm(true)}
          style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <PenLine size={18} /> Создать обращение
        </button>
      ) : (
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
            <PenLine size={18} style={{ color: 'var(--green)' }} />
            <span className="fw-600" style={{ fontSize: '0.95rem' }}>Создать обращение</span>
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

          {/* Screenshot attach */}
          <div className="form-group">
            <label className="form-label">Скриншот (необязательно)</label>
            {!imagePreview ? (
              <label className="btn btn-ghost btn-sm" style={{ display: 'inline-flex', alignItems: 'center', gap: 6, cursor: 'pointer' }}>
                <Paperclip size={14} /> Прикрепить
                <input type="file" accept="image/*" style={{ display: 'none' }} onChange={handleFileSelect} />
              </label>
            ) : (
              <div style={{ position: 'relative', display: 'inline-block' }}>
                <img src={imagePreview} alt="" style={{ maxHeight: 120, borderRadius: 8, border: '1px solid var(--border)' }} />
                <button
                  className="btn btn-ghost btn-sm"
                  style={{ position: 'absolute', top: 4, right: 4, padding: 2, background: 'rgba(0,0,0,0.5)', borderRadius: '50%' }}
                  onClick={clearImage}
                >
                  <X size={14} />
                </button>
              </div>
            )}
          </div>

          {error && <div className="text-red" style={{ fontSize: '0.85rem', marginBottom: 10 }}>{error}</div>}

          <div style={{ display: 'flex', gap: 10 }}>
            <button
              className="btn btn-ghost"
              onClick={() => { setShowForm(false); setError(''); setSubject(''); setMessage(''); clearImage(); }}
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
