import { useNavigate } from 'react-router-dom';
import { useUserStore } from '@dfc/shared';
import { Ticket, MessageCircle, LifeBuoy, FileText } from 'lucide-react';
import './SupportPage.css';

export default function SupportPage() {
  const navigate = useNavigate();
  const { features, supportUrl, ticketUnread } = useUserStore();

  return (
    <div className="support-page animate-in">
      <h2 className="page-title">Поддержка</h2>

      <div className="card card-clickable" onClick={() => navigate('/tickets')}>
        <div className="card-title">
          <Ticket size={18} /> Тикеты
          {ticketUnread > 0 && <span className="badge">{ticketUnread}</span>}
        </div>
        <span className="pill pill-cyan" style={{ fontSize: '.78rem' }}>Открыть</span>
      </div>

      {features?.community_enabled && features.community_url && (
        <div className="card">
          <div className="card-title"><MessageCircle size={18} /> Сообщество</div>
          <button
            className="pill pill-cyan"
            style={{ fontSize: '.78rem' }}
            onClick={() => window.open(features.community_url, '_blank')}
          >
            Открыть
          </button>
        </div>
      )}

      {supportUrl && (
        <div className="card">
          <div className="card-title"><LifeBuoy size={18} /> Помощь</div>
          <button
            className="pill pill-outline"
            style={{ fontSize: '.78rem' }}
            onClick={() => window.open(supportUrl, '_blank')}
          >
            Написать
          </button>
        </div>
      )}

      {features?.tos_enabled && features.tos_url && (
        <div className="card">
          <div className="card-title"><FileText size={18} /> Соглашение</div>
          <button
            className="pill pill-outline"
            style={{ fontSize: '.78rem' }}
            onClick={() => window.open(features.tos_url, '_blank')}
          >
            Открыть
          </button>
        </div>
      )}
    </div>
  );
}
