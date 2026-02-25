import { useState, useEffect } from 'react';
import { adminApi } from '@dfc/shared';
import { Bot, FileText, RefreshCw, Loader2, Info, ChevronDown, ChevronUp } from 'lucide-react';

interface BotInfo {
  version: string;
  access_mode: string;
  registration_allowed: boolean;
  purchases_allowed: boolean;
  notifications_enabled: boolean;
  default_currency: string;
  bot_locale: string;
}

export default function AdminBotManagement() {
  const [info, setInfo] = useState<BotInfo | null>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [logsExpanded, setLogsExpanded] = useState(false);
  const [loading, setLoading] = useState(true);
  const [logsLoading, setLogsLoading] = useState(false);
  const [logsError, setLogsError] = useState('');

  const loadInfo = async () => {
    setLoading(true);
    try {
      const { data } = await adminApi.getBotInfo();
      setInfo(data as BotInfo);
    } catch { /* ignore */ }
    finally { setLoading(false); }
  };

  const loadLogs = async () => {
    setLogsLoading(true);
    setLogsError('');
    try {
      const { data } = await adminApi.getBotLogs(200) as { data: { lines: string[]; error?: string } };
      if (data.error) {
        setLogsError(data.error);
      } else {
        setLogs(data.lines || []);
      }
    } catch (e: any) {
      setLogsError(e?.message || 'Ошибка загрузки логов');
    } finally {
      setLogsLoading(false);
    }
  };

  useEffect(() => { loadInfo(); }, []);

  const handleLogsToggle = () => {
    if (!logsExpanded && logs.length === 0) loadLogs();
    setLogsExpanded(!logsExpanded);
  };

  if (loading) return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: 40 }}>
      <Loader2 size={28} className="spinner" />
    </div>
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>

      {/* Bot info card */}
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
          <Bot size={20} style={{ color: 'var(--cyan)' }} />
          <span className="fw-600">Информация о боте</span>
          <span style={{ flex: 1 }} />
          <button className="btn btn-ghost btn-sm" onClick={loadInfo}>
            <RefreshCw size={14} />
          </button>
        </div>

        {info ? (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <tbody>
              {[
                ['Версия', info.version],
                ['Режим доступа', info.access_mode],
                ['Регистрация', info.registration_allowed ? '✅ Разрешена' : '❌ Закрыта'],
                ['Покупки', info.purchases_allowed ? '✅ Разрешены' : '❌ Закрыты'],
                ['Уведомления', info.notifications_enabled ? '✅ Вкл' : '❌ Выкл'],
                ['Валюта', info.default_currency],
                ['Язык бота', info.bot_locale],
              ].map(([k, v]) => (
                <tr key={k} style={{ borderBottom: '1px solid var(--border)' }}>
                  <td style={{ padding: '7px 0', color: 'var(--text2)', fontSize: '0.83rem', width: '50%' }}>{k}</td>
                  <td style={{ padding: '7px 0', fontSize: '0.85rem', textAlign: 'right' }}>{v}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="text-muted" style={{ fontSize: '0.85rem' }}>Нет данных</div>
        )}
      </div>

      {/* Logs */}
      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        <button
          style={{
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            padding: '12px 14px',
            background: 'none',
            cursor: 'pointer',
          }}
          onClick={handleLogsToggle}
        >
          <FileText size={18} style={{ color: 'var(--text2)' }} />
          <span className="fw-600" style={{ flex: 1, textAlign: 'left' }}>Логи</span>
          {logsLoading && <Loader2 size={14} className="spinner" />}
          {logsExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
        </button>

        {logsExpanded && (
          <div style={{ padding: '0 14px 14px' }}>
            {logsError ? (
              <div className="text-muted" style={{ fontSize: '0.82rem' }}>{logsError}</div>
            ) : (
              <>
                <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 8 }}>
                  <button className="btn btn-ghost btn-sm" onClick={loadLogs}>
                    <RefreshCw size={12} /> Обновить
                  </button>
                </div>
                <div style={{
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.72rem',
                  color: 'var(--text2)',
                  background: 'var(--bg)',
                  borderRadius: 6,
                  padding: '8px 10px',
                  maxHeight: 320,
                  overflowY: 'auto',
                  overflowX: 'hidden',
                  wordBreak: 'break-all',
                }}>
                  {logs.length > 0 ? logs.map((line, i) => (
                    <div key={i} style={{
                      borderBottom: '1px solid rgba(255,255,255,0.03)',
                      padding: '2px 0',
                      color: line.includes('ERROR') ? 'var(--red)' : line.includes('WARNING') ? 'var(--gold)' : undefined,
                    }}>{line || ' '}</div>
                  )) : (
                    <div className="text-muted">Нет записей</div>
                  )}
                </div>
              </>
            )}
          </div>
        )}
      </div>

      {/* Info note */}
      <div className="card" style={{ padding: '10px 14px', display: 'flex', gap: 8, alignItems: 'flex-start' }}>
        <Info size={16} style={{ color: 'var(--text3)', flexShrink: 0, marginTop: 2 }} />
        <div style={{ fontSize: '0.78rem', color: 'var(--text3)' }}>
          Для перезапуска бота используйте команду через SSH или Docker. Функция перезапуска через интерфейс будет добавлена в следующем обновлении.
        </div>
      </div>
    </div>
  );
}
