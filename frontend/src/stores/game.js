import { defineStore } from 'pinia'
import { gameAPI } from '@/services/api'
import wsService from '@/services/websocket'
import { useRoomStore } from './room'

export const useGameStore = defineStore('game', {
  state: () => ({
    gameStatus: 'waiting', // waiting, active, ended
    currentPrompt: null,
    promptCount: 0,
    timer: {
      t0: null,
      duration: 0,
      remaining: 0
    },
    gameState: {},
    loading: false,
    error: null
  }),

  getters: {
    isGameActive: (state) => state.gameStatus === 'active',
    timerExpired: (state) => state.timer.remaining <= 0,
    gameType: () => {
      const roomStore = useRoomStore()
      return roomStore.gameSlug
    }
  },

  actions: {
    async startGame() {
      const roomStore = useRoomStore()
      if (!roomStore.roomId || !roomStore.isHost) return
      
      this.loading = true
      this.error = null
      
      try {
        const response = await gameAPI.start(roomStore.roomId)
        this.promptCount = response.data.prompt_count
        this.gameStatus = 'active'
        
        // Get first prompt
        await this.getNextPrompt()
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to start game'
        throw error
      } finally {
        this.loading = false
      }
    },

    async getNextPrompt() {
      const roomStore = useRoomStore()
      if (!roomStore.roomId) return
      
      try {
        const response = await gameAPI.getNextPrompt(roomStore.roomId)
        
        if (response.data.success) {
          this.currentPrompt = response.data.prompt
          return response.data
        } else {
          // No more prompts
          this.currentPrompt = null
          this.gameStatus = 'ended'
          return response.data
        }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to get prompt'
        throw error
      }
    },

    async sendGameAction(action, data) {
      const roomStore = useRoomStore()
      if (!roomStore.roomId) return
      
      try {
        const response = await gameAPI.sendAction(roomStore.roomId, {
          action,
          data
        })
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to send action'
        throw error
      }
    },

    async endGame() {
      const roomStore = useRoomStore()
      if (!roomStore.roomId || !roomStore.isHost) return
      
      try {
        await gameAPI.end(roomStore.roomId)
        this.gameStatus = 'ended'
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to end game'
        throw error
      }
    },

    startTimer(duration) {
      // Request timer start from server
      wsService.startTimer(duration)
    },

    syncTimer(timerData) {
      this.timer.t0 = timerData.t0
      this.timer.duration = timerData.duration
      this.updateTimerRemaining()
    },

    updateTimerRemaining() {
      if (!this.timer.t0) return
      
      const now = Date.now() / 1000
      const elapsed = now - this.timer.t0
      this.timer.remaining = Math.max(0, this.timer.duration - elapsed)
    },

    updateGameState(update) {
      // Handle game state updates from WebSocket
      if (update.type === 'vote_update') {
        this.gameState.votes = update.data.vote_counts
      } else if (update.type === 'player_answer') {
        if (!this.gameState.answers) {
          this.gameState.answers = []
        }
        this.gameState.answers.push(update.data)
      }
      // Add more game-specific updates as needed
    },

    reset() {
      this.gameStatus = 'waiting'
      this.currentPrompt = null
      this.promptCount = 0
      this.timer = {
        t0: null,
        duration: 0,
        remaining: 0
      }
      this.gameState = {}
      this.loading = false
      this.error = null
    }
  }
})