import { io } from 'socket.io-client'
import { useAuthStore } from '@/stores/auth'

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

class WebSocketService {
  constructor() {
    this.socket = null
    this.connected = false
    this.listeners = new Map()
  }

  connect() {
    const authStore = useAuthStore()
    
    this.socket = io(WS_URL, {
      auth: {
        token: authStore.token
      },
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    })

    this.setupEventHandlers()
  }

  setupEventHandlers() {
    this.socket.on('connect', () => {
      console.log('WebSocket connected')
      this.connected = true
      this.emit('ws:connected')
    })

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected')
      this.connected = false
      this.emit('ws:disconnected')
    })

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error)
      this.emit('ws:error', error)
    })

    // Game events
    this.socket.on('user_joined', (data) => {
      this.emit('game:userJoined', data)
    })

    this.socket.on('user_left', (data) => {
      this.emit('game:userLeft', data)
    })

    this.socket.on('game_update', (data) => {
      this.emit('game:update', data)
    })

    this.socket.on('timer_sync', (data) => {
      this.emit('game:timerSync', data)
    })

    this.socket.on('stroke_update', (data) => {
      this.emit('game:strokeUpdate', data)
    })
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
      this.connected = false
    }
  }

  // Room management
  joinRoom(roomId) {
    return new Promise((resolve, reject) => {
      this.socket.emit('join_room', { room_id: roomId }, (response) => {
        if (response.error) {
          reject(new Error(response.error))
        } else {
          resolve(response)
        }
      })
    })
  }

  leaveRoom(roomId) {
    return new Promise((resolve, reject) => {
      this.socket.emit('leave_room', { room_id: roomId }, (response) => {
        if (response.error) {
          reject(new Error(response.error))
        } else {
          resolve(response)
        }
      })
    })
  }

  // Game actions
  sendGameAction(type, data) {
    return new Promise((resolve, reject) => {
      this.socket.emit('game_action', { type, data }, (response) => {
        if (response.error) {
          reject(new Error(response.error))
        } else {
          resolve(response)
        }
      })
    })
  }

  startTimer(duration) {
    return new Promise((resolve, reject) => {
      this.socket.emit('start_timer', { duration }, (response) => {
        if (response.error) {
          reject(new Error(response.error))
        } else {
          resolve(response)
        }
      })
    })
  }

  sendDrawingStroke(stroke) {
    this.socket.emit('drawing_stroke', { stroke })
  }

  // Event emitter methods
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event).push(callback)
  }

  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event)
      const index = callbacks.indexOf(callback)
      if (index > -1) {
        callbacks.splice(index, 1)
      }
    }
  }

  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => {
        callback(data)
      })
    }
  }
}

export default new WebSocketService()