import { create } from 'zustand';
import type { User, Subscription, Features, Plan } from '../types';
import { userApi } from '../api';

interface UserState {
  user: User | null;
  subscription: Subscription | null;
  features: Features | null;
  plans: Plan[];
  botUsername: string;
  refLink: string;
  supportUrl: string;
  trialAvailable: boolean;
  defaultCurrency: string;
  botLocale: string;
  ticketUnread: number;
  hasOpenTickets: boolean;
  availableGateways: { type: string; currency: string }[];
  isLoading: boolean;
  isAuthenticated: boolean;

  fetchData: () => Promise<void>;
  clear: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  subscription: null,
  features: null,
  plans: [],
  botUsername: '',
  refLink: '',
  supportUrl: '',
  trialAvailable: false,
  defaultCurrency: 'RUB',
  botLocale: 'RU',
  ticketUnread: 0,
  hasOpenTickets: false,
  availableGateways: [],
  isLoading: true,
  isAuthenticated: false,

  fetchData: async () => {
    try {
      set({ isLoading: true });
      const { data } = await userApi.getData();
      set({
        user: data.user,
        subscription: data.subscription && Object.keys(data.subscription).length > 0
          ? data.subscription as Subscription
          : null,
        features: data.features,
        plans: data.plans,
        botUsername: data.bot_username,
        refLink: data.ref_link,
        supportUrl: data.support_url,
        trialAvailable: data.trial_available,
        defaultCurrency: data.default_currency,
        botLocale: data.bot_locale,
        ticketUnread: data.ticket_unread,
        hasOpenTickets: data.has_open_tickets,
        availableGateways: data.available_gateways,
        isLoading: false,
        isAuthenticated: true,
      });
    } catch {
      set({ isLoading: false, isAuthenticated: false });
    }
  },

  clear: () =>
    set({
      user: null,
      subscription: null,
      features: null,
      plans: [],
      isLoading: false,
      isAuthenticated: false,
    }),
}));
