import api from './client';
import type {
  AuthCheckResponse,
  UserData,
  AppConfig,
  Ticket,
  TicketMessage,
  Plan,
  Settings,
  PaymentGateway,
  AdminStats,
  PurchaseRequest,
  PurchaseResponse,
  TopupRequest,
  BrandSettings,
} from '../types';

/* ═══ Auth ═══ */
export const authApi = {
  loginTelegram: (initData: string) =>
    api.post<{ ok: boolean; telegram_id: number }>('/web/api/auth/tg', { initData }),

  checkTelegramId: (telegram_id: number) =>
    api.post<AuthCheckResponse>('/web/api/auth/check', { telegram_id }),

  register: (telegram_id: number, web_username: string, password: string) =>
    api.post<{ ok: boolean }>('/web/api/auth/register', { telegram_id, web_username, password }),

  login: (web_username: string, password: string) =>
    api.post<{ ok: boolean }>('/web/api/auth/login', { web_username, password }),

  logout: () => api.post('/web/api/auth/logout'),
};

/* ═══ User ═══ */
export const userApi = {
  getData: () => api.get<UserData>('/web/api/user/data'),

  getSubscription: () => api.get('/web/api/user/subscription'),

  getConfig: () => api.get<AppConfig>('/web/api/config'),

  setCredentials: (web_username: string, password: string) =>
    api.post('/web/api/user/credentials', { web_username, password }),

  changePassword: (current_password: string, new_password: string) =>
    api.post('/web/api/user/credentials/password', { current_password, new_password }),
};

/* ═══ Purchase ═══ */
export const purchaseApi = {
  buy: (data: PurchaseRequest) => api.post<PurchaseResponse>('/web/api/purchase', data),

  activateTrial: () => api.post('/web/api/trial/activate'),

  topup: (data: TopupRequest) => api.post('/web/api/topup', data),

  activatePromocode: (code: string) =>
    api.post('/web/api/promocode/activate', { code }),
};

/* ═══ Tickets ═══ */
export const ticketApi = {
  list: () => api.get<Ticket[]>('/web/api/tickets'),

  get: (id: number) => api.get<Ticket>(`/web/api/tickets/${id}`),

  create: (subject: string, message: string, image_data?: string) =>
    api.post<Ticket>('/web/api/tickets', { subject, message, image_data }),

  reply: (id: number, text: string, image_data?: string) =>
    api.post<TicketMessage>(`/web/api/tickets/${id}/reply`, { text, image_data }),

  close: (id: number, resolution: string) =>
    api.post(`/web/api/tickets/${id}/close`, { resolution }),

  editMessage: (ticketId: number, msgId: number, text: string) =>
    api.patch(`/web/api/tickets/${ticketId}/messages/${msgId}`, { text }),

  deleteMessage: (ticketId: number, msgId: number) =>
    api.delete(`/web/api/tickets/${ticketId}/messages/${msgId}`),

  status: () => api.get<{ unread: number; has_open: boolean }>('/web/api/tickets/status'),
};

/* ═══ Admin ═══ */
export const adminApi = {
  // Stats
  getStats: () => api.get<AdminStats>('/web/api/admin/stats'),

  // Users
  listUsers: (page?: number, search?: string) =>
    api.get('/web/api/admin/users', { params: { page, search } }),

  getUser: (tid: number) => api.get('/web/api/admin/users/' + tid),

  setUserRole: (tid: number, role: string) =>
    api.post(`/web/api/admin/users/${tid}/role`, { role }),

  addBalance: (tid: number, amount: number) =>
    api.post(`/web/api/admin/users/${tid}/balance`, { amount }),

  addBonusBalance: (tid: number, amount: number) =>
    api.post(`/web/api/admin/users/${tid}/bonus-balance`, { amount }),

  blockUser: (tid: number, blocked: boolean) =>
    api.post(`/web/api/admin/users/${tid}/block`, { blocked }),

  // Plans
  listPlans: () => api.get<Plan[]>('/web/api/admin/plans'),

  createPlan: (data: Partial<Plan>) => api.post<Plan>('/web/api/admin/plans', data),

  updatePlan: (id: number, data: Partial<Plan>) =>
    api.put<Plan>(`/web/api/admin/plans/${id}`, data),

  deletePlan: (id: number) => api.delete(`/web/api/admin/plans/${id}`),

  togglePlan: (id: number) => api.patch(`/web/api/admin/plans/${id}/toggle`),

  // Settings
  getSettings: () => api.get<Settings>('/web/api/admin/settings'),

  updateSettings: (data: Partial<Settings>) =>
    api.patch('/web/api/admin/settings', data),

  // Gateways
  listGateways: () => api.get<PaymentGateway[]>('/web/api/admin/gateways'),

  updateGateway: (id: number, data: Partial<PaymentGateway>) =>
    api.patch(`/web/api/admin/gateways/${id}`, data),

  // Tickets
  listTickets: () => api.get<Ticket[]>('/web/api/admin/tickets'),

  getTicket: (id: number) => api.get<Ticket>(`/web/api/admin/tickets/${id}`),

  replyTicket: (id: number, text: string, image_data?: string) =>
    api.post(`/web/api/admin/tickets/${id}/reply`, { text, image_data }),

  closeTicket: (id: number) =>
    api.post(`/web/api/admin/tickets/${id}/close`),

  deleteTicket: (id: number) =>
    api.delete(`/web/api/admin/tickets/${id}`),

  editTicketMessage: (ticketId: number, msgId: number, text: string) =>
    api.patch(`/web/api/admin/tickets/${ticketId}/messages/${msgId}`, { text }),

  deleteTicketMessage: (ticketId: number, msgId: number) =>
    api.delete(`/web/api/admin/tickets/${ticketId}/messages/${msgId}`),

  // Brand
  getBrand: () => api.get<BrandSettings>('/web/api/settings/brand'),

  saveBrand: (data: BrandSettings) => api.post('/web/api/settings/brand', data),
};
