/* ═══ User ═══ */
export interface User {
  telegram_id: number;
  name: string;
  username: string;
  balance: number;
  referral_balance: number;
  referral_code: string;
  role: UserRole;
  language: string;
  is_blocked: boolean;
}

export type UserRole = 'USER' | 'ADMIN' | 'DEV';

/* ═══ Subscription ═══ */
export interface Subscription {
  status: SubscriptionStatus;
  plan_name: string;
  plan_id: number | null;
  expire_at: string;
  traffic_limit: number | null;
  device_limit: number | null;
  is_trial: boolean;
  url: string;
  active_devices_count: number;
}

export type SubscriptionStatus = 'ACTIVE' | 'EXPIRED' | 'DISABLED';

/* ═══ Plan ═══ */
export interface Plan {
  id: number;
  name: string;
  description: string;
  type: string;
  tag?: string;
  traffic_limit: number | null;
  device_limit: number | null;
  durations: PlanDuration[];
  is_active?: boolean;
  availability?: string;
}

export interface PlanDuration {
  days: number;
  prices: PlanPrice[];
}

export interface PlanPrice {
  currency: string;
  amount: string;
}

/* ═══ Ticket ═══ */
export interface Ticket {
  id: number;
  subject: string;
  status: TicketStatus;
  created_at: string;
  updated_at: string;
  messages: TicketMessage[];
  user_telegram_id?: number;
}

export type TicketStatus = 'OPEN' | 'ANSWERED' | 'WAITING' | 'CLOSED';

export interface TicketMessage {
  id: number;
  text: string;
  sender: 'user' | 'admin';
  created_at: string;
  image_url?: string;
}

/* ═══ Payment Gateway ═══ */
export interface PaymentGateway {
  id: number;
  type: GatewayType;
  currency: string;
  is_active: boolean;
  config?: Record<string, string>;
}

export type GatewayType =
  | 'TELEGRAM_STARS'
  | 'YOOKASSA'
  | 'YOOMONEY'
  | 'CRYPTOMUS'
  | 'HELEKET'
  | 'CRYPTOPAY'
  | 'ROBOKASSA'
  | 'BALANCE';

/* ═══ Settings ═══ */
export interface Settings {
  access_mode: string;
  channel_required: boolean;
  channel_link: string;
  rules_required: boolean;
  purchases_allowed: boolean;
  registration_allowed: boolean;
  default_currency: string;
  bot_locale: string;
  balance_enabled: boolean;
  balance_mode: string;
  referral_enabled: boolean;
  referral_type: string;
  referral_reward: number;
  referral_invite_message: string;
  community_enabled: boolean;
  community_url: string;
  tos_enabled: boolean;
  tos_url: string;
  promocodes_enabled: boolean;
  notifications_enabled: boolean;
  extra_devices_enabled: boolean;
  extra_devices_price: number;
  transfers_enabled: boolean;
  global_discount_enabled: boolean;
  global_discount_percent: number;
  language_enabled: boolean;
  trial_enabled: boolean;
}

/* ═══ Features (client-visible subset) ═══ */
export interface Features {
  balance_enabled: boolean;
  balance_mode: string;
  community_enabled: boolean;
  community_url: string;
  tos_enabled: boolean;
  tos_url: string;
  referral_enabled: boolean;
  referral_invite_message: string;
  promocodes_enabled: boolean;
  extra_devices_enabled?: boolean;
  trial_enabled?: boolean;
}

/* ═══ Admin Stats ═══ */
export interface AdminStats {
  total_users: number;
  active_subscriptions: number;
  expired_subscriptions: number;
  revenue_today: number;
  revenue_month: number;
  total_revenue: number;
}

/* ═══ User Data (full dashboard response) ═══ */
export interface UserData {
  user: User;
  subscription: Subscription | Record<string, never>;
  plans: Plan[];
  bot_username: string;
  ref_link: string;
  features: Features;
  support_url: string;
  trial_available: boolean;
  default_currency: string;
  bot_locale: string;
  ticket_unread: number;
  has_open_tickets: boolean;
  available_gateways: { type: GatewayType; currency: string }[];
}

/* ═══ Config ═══ */
export interface AppConfig {
  domain: string;
  support_url: string;
  bot_username: string;
}

/* ═══ Purchase ═══ */
export interface PurchaseRequest {
  plan_id: number;
  duration_days: number;
  gateway?: string;
}

export interface PurchaseResponse {
  ok?: boolean;
  payment_url?: string;
  message?: string;
}

/* ═══ Auth ═══ */
export interface AuthCheckResponse {
  has_credentials: boolean;
  name: string;
  web_username: string | null;
}

/* ═══ Brand Settings ═══ */
export interface BrandSettings {
  name: string;
  logo: string;
  slogan: string;
  [key: string]: unknown;
}

/* ═══ Topup ═══ */
export interface TopupRequest {
  amount: number;
  gateway: string;
}

/* ═══ Promocode ═══ */
export interface PromocodeActivateRequest {
  code: string;
}

/* ═══ Admin Promocode ═══ */
export interface AdminPromocode {
  id: number;
  code: string;
  name: string;
  is_active: boolean;
  reward_type: PromocodeRewardType;
  reward: number | null;
  availability: string;
  lifetime: number | null;
  max_activations: number | null;
  activations_count: number;
  is_expired: boolean;
  is_depleted: boolean;
  created_at: string;
}

export type PromocodeRewardType = 'DURATION' | 'TRAFFIC' | 'DEVICES' | 'SUBSCRIPTION' | 'PERSONAL_DISCOUNT';
export type PromocodeAvailability = 'ALL' | 'NEW' | 'EXISTING' | 'INVITED' | 'ALLOWED';

/* ═══ Broadcast ═══ */
export interface AdminBroadcast {
  id: number;
  task_id: string;
  status: BroadcastStatus;
  audience: BroadcastAudience;
  total_count: number;
  success_count: number;
  failed_count: number;
  created_at: string;
  text: string;
}

export type BroadcastStatus = 'PROCESSING' | 'COMPLETED' | 'CANCELED' | 'DELETED' | 'ERROR';
export type BroadcastAudience = 'ALL' | 'SUBSCRIBED' | 'UNSUBSCRIBED' | 'EXPIRED' | 'TRIAL' | 'PLAN';

/* ═══ User Broadcast Message ═══ */
export interface UserBroadcastMessage {
  id: number;
  broadcast_id: number;
  text: string;
  status: string;
  created_at: string;
}

/* ═══ Monitoring ═══ */
export interface MonitoringStats {
  [key: string]: unknown;
}
