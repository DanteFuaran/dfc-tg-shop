/// <reference types="vite/client" />

interface TelegramWebApp {
  ready: () => void;
  expand: () => void;
  close: () => void;
  initData: string;
  initDataUnsafe: {
    user?: {
      id: number;
      first_name: string;
      last_name?: string;
      username?: string;
      language_code?: string;
    };
  };
  colorScheme: 'light' | 'dark';
  themeParams: Record<string, string>;
  MainButton: {
    text: string;
    color: string;
    textColor: string;
    isVisible: boolean;
    isActive: boolean;
    show: () => void;
    hide: () => void;
    onClick: (cb: () => void) => void;
    offClick: (cb: () => void) => void;
    enable: () => void;
    disable: () => void;
    setParams: (params: Record<string, string>) => void;
  };
  BackButton: {
    isVisible: boolean;
    show: () => void;
    hide: () => void;
    onClick: (cb: () => void) => void;
    offClick: (cb: () => void) => void;
  };
  HapticFeedback: {
    impactOccurred: (style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft') => void;
    notificationOccurred: (type: 'error' | 'success' | 'warning') => void;
    selectionChanged: () => void;
  };
  openLink: (url: string) => void;
  openTelegramLink: (url: string) => void;
  /** Платформа клиента: 'android' | 'ios' | 'android_x' | 'tdesktop' | 'macos' | 'webk' | 'weba' | 'web' | 'unknown' */
  platform: string;
  /** Открывает нативный пикер чатов (аналог SwitchInlineQueryChosenChatButton в боте) */
  switchInlineQuery: (
    query: string,
    choose_chat_types?: Array<'users' | 'bots' | 'groups' | 'channels'>,
  ) => void;
  showPopup: (params: { title?: string; message: string; buttons?: Array<{ type: string; text: string; id: string }> }) => void;
  showConfirm: (message: string, callback: (ok: boolean) => void) => void;
}

interface Window {
  Telegram?: {
    WebApp: TelegramWebApp;
  };
}
