import { defineStore } from 'pinia'
import { authAPI } from '@/services/api'
import wsService from '@/services/websocket'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: false,
    loading: false,
    error: null
  }),

  getters: {
    isPaidUser: (state) => state.user?.is_paid || false,
    userRole: (state) => state.user?.role || 'free',
    showAds: (state) => !state.user?.is_paid
  },

  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null
      
      try {
        const response = await authAPI.login(credentials)
        const { access_token, user } = response.data
        
        this.token = access_token
        this.user = user
        this.isAuthenticated = true
        
        localStorage.setItem('token', access_token)
        
        // Connect WebSocket
        wsService.connect()
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Login failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    async register(userData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await authAPI.register(userData)
        const { access_token, user } = response.data
        
        this.token = access_token
        this.user = user
        this.isAuthenticated = true
        
        localStorage.setItem('token', access_token)
        
        // Connect WebSocket
        wsService.connect()
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Registration failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    async refreshToken() {
      try {
        const response = await authAPI.refresh()
        const { access_token, user } = response.data
        
        this.token = access_token
        this.user = user
        this.isAuthenticated = true
        
        localStorage.setItem('token', access_token)
        
        return response.data
      } catch (error) {
        this.logout()
        throw error
      }
    },

    async logout() {
      try {
        await authAPI.logout()
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.token = null
        this.user = null
        this.isAuthenticated = false
        
        localStorage.removeItem('token')
        
        // Disconnect WebSocket
        wsService.disconnect()
      }
    },

    async checkAuth() {
      if (!this.token) {
        return false
      }
      
      try {
        await this.refreshToken()
        return true
      } catch (error) {
        return false
      }
    },

    updateUserPaymentStatus(isPaid, paidUntil) {
      if (this.user) {
        this.user.is_paid = isPaid
        this.user.paid_until = paidUntil
        this.user.role = isPaid ? 'paid' : 'free'
      }
    }
  }
})