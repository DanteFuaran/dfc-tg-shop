import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { userApi } from '@dfc/shared';
import type { UserBroadcastMessage } from '@dfc/shared';
import { ArrowLeft, Mail, Loader2, Megaphone } from 'lucide-react';

export default function MessagesPage() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState<UserBroadcastMessage[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await userApi.getMessages();
      setMessages(Array.isArray(data) ? data : []);
    } catch { /* ignore */ }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { load(); }, [load]);

  const sentMessages = messages.filter(m => m.status === 'SENT');

  return (
    <div className="animate-in" style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <button className="btn btn-ghost btn-sm" onClick={() => navigate('/support')} style={{ padding: 4 }}>
          <ArrowLeft size={20} />
        </button>
        <h2 className="page-title" style={{ margin: 0 }}>Сообщения</h2>
      </div>

      {loading ? (
        <div className="empty-state"><Loader2 size={28} className="spinner" /></div>
      ) : sentMessages.length === 0 ? (
        <div className="empty-state">
          <Mail size={40} style={{ color: 'var(--text3)', marginBottom: 12 }} />
          <div>Нет сообщений</div>
          <div className="text-muted" style={{ fontSize: '0.8rem', marginTop: 4 }}>
            Здесь будут отображаться рассылки от администрации
          </div>
        </div>
      ) : (
        <div className="card-list">
          {sentMessages.map(m => (
            <div className="card" key={m.id} style={{ padding: '14px 16px' }}>
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: 10 }}>
                <Megaphone size={18} style={{ color: 'var(--cyan)', flexShrink: 0, marginTop: 2 }} />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{
                    fontSize: '0.88rem',
                    lineHeight: 1.5,
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                  }}>
                    {m.text}
                  </div>
                  <div className="text-muted" style={{ fontSize: '0.72rem', marginTop: 6 }}>
                    {m.created_at}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
