import { create } from 'zustand';
import type { User, Subscription, Features, Plan, BrandSettings } from '../types';
import { userApi, adminApi } from '../api';

interface UserState {
  user: User | null;
  subscription: Subscription | null;
  features: Features | null;
  plans: Plan[];
  brand: BrandSettings;
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
  setBrand: (brand: BrandSettings) => void;
  clear: () => void;
}

const DEFAULT_BRAND: BrandSettings = { name: 'DFC Online', logo: '🔐', slogan: 'Работает из упаковки' };

export const useUserStore = create<UserState>((set) => ({
  user: null,
  subscription: null,
  features: null,
  plans: [],
  brand: DEFAULT_BRAND,
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
      const [userResp, brandResp] = await Promise.allSettled([
        userApi.getData(),
        adminApi.getBrand(),
      ]);
      if (userResp.status === 'rejected') throw userResp.reason;
      const data = userResp.value.data;
      const brand: BrandSettings = brandResp.status === 'fulfilled'
        ? {
            name: brandResp.value.data.name || DEFAULT_BRAND.name,
            logo: brandResp.value.data.logo || DEFAULT_BRAND.logo,
            slogan: brandResp.value.data.slogan || '',
          }
        : DEFAULT_BRAND;
      set({
        user: data.user,
        subscription: data.subscription && Object.keys(data.subscription).length > 0
          ? data.subscription as Subscription
          : null,
        features: data.features,
        plans: data.plans,
        brand,
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

  setBrand: (brand: BrandSettings) => set({ brand }),

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
