<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Game Header -->
    <div class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-2xl font-bold">{{ gameTitle }}</h1>
            <p class="text-sm text-gray-600">Room Code: {{ roomStore.inviteCode }}</p>
          </div>
          <div class="flex items-center space-x-4">
            <Timer v-if="gameStore.isGameActive" />
            <button 
              v-if="roomStore.isHost && !gameStore.isGameActive"
              @click="startGame"
              class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
              :disabled="roomStore.approvedParticipants.length < 2"
            >
              Start Game
            </button>
            <button 
              @click="leaveRoom"
              class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700"
            >
              Leave Room
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Game Area -->
        <div class="lg:col-span-3">
          <div class="bg-white rounded-lg shadow p-6">
            <!-- Waiting State -->
            <div v-if="!gameStore.isGameActive" class="text-center py-12">
              <h2 class="text-xl font-semibold mb-4">Waiting for players...</h2>
              <p class="text-gray-600 mb-8">
                Share the room code with your friends: 
                <span class="font-mono bg-gray-100 px-2 py-1 rounded">{{ roomStore.inviteCode }}</span>
              </p>
              <div v-if="roomStore.pendingParticipants.length > 0" class="mt-8">
                <h3 class="text-lg font-medium mb-4">Pending Approvals</h3>
                <div v-for="participant in roomStore.pendingParticipants" :key="participant.id" class="flex justify-between items-center mb-2">
                  <span>{{ participant.guest_name || participant.user?.email }}</span>
                  <button 
                    v-if="roomStore.isHost"
                    @click="approveParticipant(participant.id)"
                    class="bg-green-500 text-white px-3 py-1 rounded text-sm"
                  >
                    Approve
                  </button>
                </div>
              </div>
            </div>

            <!-- Game Content -->
            <component 
              v-else
              :is="gameComponent" 
              :prompt="gameStore.currentPrompt"
              @action="handleGameAction"
            />
          </div>
        </div>

        <!-- Participants Sidebar -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow p-4">
            <h3 class="font-semibold mb-4">Players ({{ roomStore.approvedParticipants.length }})</h3>
            <div class="space-y-2">
              <div 
                v-for="participant in roomStore.approvedParticipants" 
                :key="participant.id"
                class="flex items-center space-x-2"
              >
                <div class="w-8 h-8 bg-indigo-500 rounded-full flex items-center justify-center text-white text-sm">
                  {{ getInitial(participant) }}
                </div>
                <span class="text-sm">
                  {{ participant.guest_name || participant.user?.email }}
                  <span v-if="isHost(participant)" class="text-xs text-gray-500">(Host)</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRoomStore } from '@/stores/room'
import { useGameStore } from '@/stores/game'
import { useAuthStore } from '@/stores/auth'
import wsService from '@/services/websocket'

// Game Components
import Timer from '@/components/Timer.vue'
import WouldYouRather from '@/components/games/WouldYouRather.vue'

const route = useRoute()
const router = useRouter()
const roomStore = useRoomStore()
const gameStore = useGameStore()
const authStore = useAuthStore()

const gameComponents = {
  would_you_rather: WouldYouRather,
  // Add other game components here
}

const gameComponent = computed(() => {
  return gameComponents[roomStore.gameSlug] || null
})

const gameTitle = computed(() => {
  const titles = {
    would_you_rather: 'Would You Rather',
    truth_or_dare: 'Truth or Dare',
    sixty_seconds: '60 Seconds',
    hot_seat: 'Hot Seat',
    draw_guess: 'Draw & Guess'
  }
  return titles[roomStore.gameSlug] || 'Game Room'
})

const getInitial = (participant) => {
  const name = participant.guest_name || participant.user?.email || '?'
  return name[0].toUpperCase()
}

const isHost = (participant) => {
  return participant.user_id === roomStore.currentRoom?.host_id
}

const startGame = async () => {
  try {
    await gameStore.startGame()
  } catch (error) {
    console.error('Failed to start game:', error)
  }
}

const approveParticipant = async (participantId) => {
  try {
    await roomStore.approveParticipant(participantId)
  } catch (error) {
    console.error('Failed to approve participant:', error)
  }
}

const handleGameAction = async (action, data) => {
  try {
    await gameStore.sendGameAction(action, data)
  } catch (error) {
    console.error('Failed to send game action:', error)
  }
}

const leaveRoom = async () => {
  await roomStore.leaveRoom()
  router.push('/dashboard')
}

// WebSocket event handlers
const handleUserJoined = (data) => {
  roomStore.loadParticipants()
}

const handleUserLeft = (data) => {
  roomStore.removeParticipant(data.user_id)
}

const handleGameUpdate = (data) => {
  gameStore.updateGameState(data)
}

const handleTimerSync = (data) => {
  gameStore.syncTimer(data)
}

onMounted(async () => {
  const roomId = parseInt(route.params.roomId)
  
  try {
    await roomStore.loadRoom(roomId)
    await wsService.joinRoom(roomId)
    
    // Subscribe to WebSocket events
    wsService.on('game:userJoined', handleUserJoined)
    wsService.on('game:userLeft', handleUserLeft)
    wsService.on('game:update', handleGameUpdate)
    wsService.on('game:timerSync', handleTimerSync)
  } catch (error) {
    console.error('Failed to load room:', error)
    router.push('/dashboard')
  }
})

onUnmounted(() => {
  // Unsubscribe from WebSocket events
  wsService.off('game:userJoined', handleUserJoined)
  wsService.off('game:userLeft', handleUserLeft)
  wsService.off('game:update', handleGameUpdate)
  wsService.off('game:timerSync', handleTimerSync)
  
  // Reset stores
  roomStore.reset()
  gameStore.reset()
})
</script>