import { create } from 'zustand';
import type { Ticket } from '../types';
import { ticketApi } from '../api';

interface TicketState {
  tickets: Ticket[];
  currentTicket: Ticket | null;
  isLoading: boolean;

  fetchTickets: () => Promise<void>;
  fetchTicket: (id: number) => Promise<void>;
  createTicket: (subject: string, message: string, image?: string) => Promise<Ticket>;
  reply: (id: number, text: string, image?: string) => Promise<void>;
  closeTicket: (id: number, resolution: string) => Promise<void>;
  editMessage: (ticketId: number, msgId: number, text: string) => Promise<void>;
  deleteMessage: (ticketId: number, msgId: number) => Promise<void>;
  clear: () => void;
}

export const useTicketStore = create<TicketState>((set, get) => ({
  tickets: [],
  currentTicket: null,
  isLoading: false,

  fetchTickets: async () => {
    set({ isLoading: true });
    try {
      const { data } = await ticketApi.list();
      set({ tickets: data, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },

  fetchTicket: async (id) => {
    set({ isLoading: true });
    try {
      const { data } = await ticketApi.get(id);
      set({ currentTicket: data, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },

  createTicket: async (subject, message, image) => {
    const { data } = await ticketApi.create(subject, message, image);
    set((s) => ({ tickets: [data, ...s.tickets] }));
    return data;
  },

  reply: async (id, text, image) => {
    const { data: msg } = await ticketApi.reply(id, text, image);
    set((s) => {
      if (!s.currentTicket || s.currentTicket.id !== id) return s;
      return {
        currentTicket: {
          ...s.currentTicket,
          messages: [...s.currentTicket.messages, msg],
        },
      };
    });
  },

  closeTicket: async (id, resolution) => {
    await ticketApi.close(id, resolution);
    set((s) => ({
      tickets: s.tickets.map((t) =>
        t.id === id ? { ...t, status: 'CLOSED' as const } : t
      ),
      currentTicket:
        s.currentTicket?.id === id
          ? { ...s.currentTicket, status: 'CLOSED' as const }
          : s.currentTicket,
    }));
  },

  editMessage: async (ticketId, msgId, text) => {
    await ticketApi.editMessage(ticketId, msgId, text);
    set((s) => {
      if (!s.currentTicket || s.currentTicket.id !== ticketId) return s;
      return {
        currentTicket: {
          ...s.currentTicket,
          messages: s.currentTicket.messages.map((m) =>
            m.id === msgId ? { ...m, text } : m
          ),
        },
      };
    });
  },

  deleteMessage: async (ticketId, msgId) => {
    await ticketApi.deleteMessage(ticketId, msgId);
    set((s) => {
      if (!s.currentTicket || s.currentTicket.id !== ticketId) return s;
      return {
        currentTicket: {
          ...s.currentTicket,
          messages: s.currentTicket.messages.filter((m) => m.id !== msgId),
        },
      };
    });
  },

  clear: () => set({ tickets: [], currentTicket: null }),
}));
