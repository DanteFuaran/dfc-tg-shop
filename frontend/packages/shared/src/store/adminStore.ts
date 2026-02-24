import { create } from 'zustand';
import type { Settings, PaymentGateway, Plan, AdminStats } from '../types';
import { adminApi } from '../api';

interface AdminState {
  stats: AdminStats | null;
  settings: Settings | null;
  gateways: PaymentGateway[];
  plans: Plan[];
  isLoading: boolean;

  fetchStats: () => Promise<void>;
  fetchSettings: () => Promise<void>;
  updateSettings: (data: Partial<Settings>) => Promise<void>;
  fetchGateways: () => Promise<void>;
  updateGateway: (id: number, data: Partial<PaymentGateway>) => Promise<void>;
  fetchPlans: () => Promise<void>;
  createPlan: (data: Partial<Plan>) => Promise<Plan>;
  updatePlan: (id: number, data: Partial<Plan>) => Promise<void>;
  deletePlan: (id: number) => Promise<void>;
  togglePlan: (id: number) => Promise<void>;
}

export const useAdminStore = create<AdminState>((set) => ({
  stats: null,
  settings: null,
  gateways: [],
  plans: [],
  isLoading: false,

  fetchStats: async () => {
    const { data } = await adminApi.getStats();
    set({ stats: data });
  },

  fetchSettings: async () => {
    const { data } = await adminApi.getSettings();
    set({ settings: data });
  },

  updateSettings: async (partial) => {
    await adminApi.updateSettings(partial);
    set((s) => ({
      settings: s.settings ? { ...s.settings, ...partial } : null,
    }));
  },

  fetchGateways: async () => {
    const { data } = await adminApi.listGateways();
    set({ gateways: data });
  },

  updateGateway: async (id, data) => {
    await adminApi.updateGateway(id, data);
    set((s) => ({
      gateways: s.gateways.map((g) => (g.id === id ? { ...g, ...data } : g)),
    }));
  },

  fetchPlans: async () => {
    const { data } = await adminApi.listPlans();
    set({ plans: data });
  },

  createPlan: async (data) => {
    const { data: plan } = await adminApi.createPlan(data);
    set((s) => ({ plans: [...s.plans, plan] }));
    return plan;
  },

  updatePlan: async (id, data) => {
    await adminApi.updatePlan(id, data);
    set((s) => ({
      plans: s.plans.map((p) => (p.id === id ? { ...p, ...data } : p)),
    }));
  },

  deletePlan: async (id) => {
    await adminApi.deletePlan(id);
    set((s) => ({ plans: s.plans.filter((p) => p.id !== id) }));
  },

  togglePlan: async (id) => {
    await adminApi.togglePlan(id);
    set((s) => ({
      plans: s.plans.map((p) =>
        p.id === id ? { ...p, is_active: !p.is_active } : p
      ),
    }));
  },
}));
