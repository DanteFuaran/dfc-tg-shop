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
    // Never redirect to login — miniapp handles auth via Telegram initData automatically
    return Promise.reject(err);
  },
);

export default api;
