import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore()

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        await authStore.refreshToken()
        originalRequest.headers.Authorization = `Bearer ${authStore.token}`
        return api(originalRequest)
      } catch (refreshError) {
        authStore.logout()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api

// Auth endpoints
export const authAPI = {
  login: (data) => api.post('/api/auth/login', data),
  register: (data) => api.post('/api/auth/register', data),
  refresh: () => api.post('/api/auth/refresh'),
  logout: () => api.post('/api/auth/logout')
}

// Room endpoints
export const roomAPI = {
  create: (data) => api.post('/api/rooms', data),
  get: (roomId) => api.get(`/api/rooms/${roomId}`),
  getByInvite: (inviteCode) => api.get(`/api/rooms/invite/${inviteCode}`),
  join: (roomId, data) => api.post(`/api/rooms/${roomId}/join`, data),
  joinAsGuest: (roomId, data) => api.post(`/api/rooms/${roomId}/join-guest`, data),
  approveParticipant: (roomId, participantId) => 
    api.put(`/api/rooms/${roomId}/participants/${participantId}/approve`),
  getParticipants: (roomId) => api.get(`/api/rooms/${roomId}/participants`)
}

// Game endpoints
export const gameAPI = {
  start: (roomId) => api.post(`/api/games/rooms/${roomId}/start`),
  getNextPrompt: (roomId) => api.get(`/api/games/rooms/${roomId}/next-prompt`),
  sendAction: (roomId, data) => api.post(`/api/games/rooms/${roomId}/action`, data),
  end: (roomId) => api.post(`/api/games/rooms/${roomId}/end`)
}

// Payment endpoints
export const paymentAPI = {
  verify: (data) => api.post('/api/payments/verify', data),
  getHistory: () => api.get('/api/payments/history'),
  getConfig: () => api.get('/api/payments/config')
}