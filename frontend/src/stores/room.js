import { defineStore } from 'pinia'
import { roomAPI } from '@/services/api'
import wsService from '@/services/websocket'
import { useAuthStore } from './auth'

export const useRoomStore = defineStore('room', {
  state: () => ({
    currentRoom: null,
    participants: [],
    isHost: false,
    loading: false,
    error: null
  }),

  getters: {
    roomId: (state) => state.currentRoom?.id,
    roomStatus: (state) => state.currentRoom?.status,
    inviteCode: (state) => state.currentRoom?.invite_code,
    gameSlug: (state) => state.currentRoom?.game_slug,
    approvedParticipants: (state) => 
      state.participants.filter(p => p.is_approved),
    pendingParticipants: (state) => 
      state.participants.filter(p => !p.is_approved)
  },

  actions: {
    async createRoom(data) {
      this.loading = true
      this.error = null
      
      try {
        const response = await roomAPI.create(data)
        this.currentRoom = response.data
        this.isHost = true
        
        // Join WebSocket room
        await wsService.joinRoom(this.currentRoom.id)
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create room'
        throw error
      } finally {
        this.loading = false
      }
    },

    async joinRoom(roomId) {
      this.loading = true
      this.error = null
      
      try {
        const response = await roomAPI.join(roomId, {})
        await this.loadRoom(roomId)
        
        // Join WebSocket room
        await wsService.joinRoom(roomId)
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to join room'
        throw error
      } finally {
        this.loading = false
      }
    },

    async joinRoomAsGuest(roomId, guestName) {
      this.loading = true
      this.error = null
      
      try {
        const response = await roomAPI.joinAsGuest(roomId, { guest_name: guestName })
        await this.loadRoom(roomId)
        
        // Join WebSocket room
        await wsService.joinRoom(roomId)
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to join room as guest'
        throw error
      } finally {
        this.loading = false
      }
    },

    async loadRoom(roomId) {
      try {
        const response = await roomAPI.get(roomId)
        this.currentRoom = response.data
        
        // Check if current user is host
        const authStore = useAuthStore()
        this.isHost = this.currentRoom.host_id === authStore.user?.id
        
        // Load participants
        await this.loadParticipants()
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to load room'
        throw error
      }
    },

    async loadRoomByInvite(inviteCode) {
      this.loading = true
      this.error = null
      
      try {
        const response = await roomAPI.getByInvite(inviteCode)
        this.currentRoom = response.data
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Invalid invite code'
        throw error
      } finally {
        this.loading = false
      }
    },

    async loadParticipants() {
      if (!this.currentRoom) return
      
      try {
        const response = await roomAPI.getParticipants(this.currentRoom.id)
        this.participants = response.data
      } catch (error) {
        console.error('Failed to load participants:', error)
      }
    },

    async approveParticipant(participantId) {
      if (!this.currentRoom || !this.isHost) return
      
      try {
        await roomAPI.approveParticipant(this.currentRoom.id, participantId)
        
        // Update local state
        const participant = this.participants.find(p => p.id === participantId)
        if (participant) {
          participant.is_approved = true
        }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to approve participant'
        throw error
      }
    },

    addParticipant(participant) {
      const exists = this.participants.find(p => p.id === participant.id)
      if (!exists) {
        this.participants.push(participant)
      }
    },

    removeParticipant(userId) {
      this.participants = this.participants.filter(p => p.user_id !== userId)
    },

    updateRoomStatus(status) {
      if (this.currentRoom) {
        this.currentRoom.status = status
      }
    },

    async leaveRoom() {
      if (this.currentRoom) {
        try {
          await wsService.leaveRoom(this.currentRoom.id)
        } catch (error) {
          console.error('Failed to leave room:', error)
        }
        
        this.currentRoom = null
        this.participants = []
        this.isHost = false
      }
    },

    reset() {
      this.currentRoom = null
      this.participants = []
      this.isHost = false
      this.loading = false
      this.error = null
    }
  }
})