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
      // If on website, redirect to login
      if (typeof window !== 'undefined' && !window.location.pathname.includes('/miniapp')) {
        window.location.href = '/web/login';
      }
    }
    return Promise.reject(err);
  },
);

export default api;
