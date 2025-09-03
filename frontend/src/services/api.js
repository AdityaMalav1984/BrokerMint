import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
};

export const complianceAPI = {
  getDashboard: () => api.get('/dashboard'),
  detectAnomalies: (tickers) => api.post('/anomalies/detect', { tickers }),
  verifyIdentity: (data) => api.post('/ekyc/verify', data),
  getAuditTrail: (limit) => api.get(`/audit/trail?limit=${limit}`),
  generateReport: () => api.get('/reports/compliance'),
};

export default api;