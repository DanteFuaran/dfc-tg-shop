import axios from 'axios';

const api = axios.create({
  baseURL: '',
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
});

// Response interceptor — handle 401 globally
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      // Only redirect to login on the web dashboard (non-miniapp pages)
      const path = typeof window !== 'undefined' ? window.location.pathname : '';
      const isMiniapp = path.includes('/miniapp') || path.includes('/dashboard');
      if (!isMiniapp) {
        window.location.href = '/web/login';
      }
    }
    return Promise.reject(err);
  },
);

export default api;
