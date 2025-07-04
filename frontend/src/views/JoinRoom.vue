<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4">
    <div class="max-w-md w-full">
      <div class="bg-white rounded-lg shadow p-6">
        <div v-if="loading" class="text-center py-8">
          <div class="inline-flex items-center">
            <svg class="animate-spin h-8 w-8 text-indigo-600 mr-3" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="text-lg">Loading room details...</span>
          </div>
        </div>

        <div v-else-if="room">
          <h2 class="text-2xl font-bold mb-4">Join Game Room</h2>
          
          <div class="mb-6 p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center mb-2">
              <span class="text-3xl mr-3">{{ gameEmoji }}</span>
              <div>
                <h3 class="font-semibold">{{ gameTitle }}</h3>
                <p class="text-sm text-gray-600">Hosted by {{ room.host_id }}</p>
              </div>
            </div>
          </div>

          <!-- Guest Join Form -->
          <div v-if="!authStore.isAuthenticated">
            <p class="text-sm text-gray-600 mb-4">
              Enter your name to join as a guest, or 
              <router-link to="/login" class="text-indigo-600 hover:text-indigo-800">
                sign in
              </router-link>
              for full features.
            </p>
            
            <form @submit.prevent="joinAsGuest">
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Your Name
                </label>
                <input
                  v-model="guestName"
                  type="text"
                  required
                  placeholder="Enter your name"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
              
              <button
                type="submit"
                :disabled="joining"
                class="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700 disabled:opacity-50"
              >
                {{ joining ? 'Joining...' : 'Join as Guest' }}
              </button>
            </form>
          </div>

          <!-- Authenticated User Join -->
          <div v-else>
            <p class="text-sm text-gray-600 mb-4">
              Ready to join this game room?
            </p>
            
            <button
              @click="joinAsUser"
              :disabled="joining"
              class="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700 disabled:opacity-50"
            >
              {{ joining ? 'Joining...' : 'Join Room' }}
            </button>
          </div>
        </div>

        <div v-else-if="error" class="text-center py-8">
          <div class="text-red-600 mb-4">
            <svg class="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <p class="text-lg font-semibold">{{ error }}</p>
          </div>
          <router-link 
            to="/"
            class="text-indigo-600 hover:text-indigo-800"
          >
            Return to Home
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRoomStore } from '@/stores/room'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const roomStore = useRoomStore()

const room = ref(null)
const loading = ref(true)
const joining = ref(false)
const error = ref('')
const guestName = ref('')

const gameEmoji = computed(() => {
  const emojis = {
    would_you_rather: '🤔',
    truth_or_dare: '😈',
    sixty_seconds: '⏱️',
    hot_seat: '🔥',
    draw_guess: '🎨'
  }
  return emojis[room.value?.game_slug] || '🎮'
})

const gameTitle = computed(() => {
  const titles = {
    would_you_rather: 'Would You Rather',
    truth_or_dare: 'Truth or Dare',
    sixty_seconds: '60 Seconds',
    hot_seat: 'Hot Seat',
    draw_guess: 'Draw & Guess'
  }
  return titles[room.value?.game_slug] || 'Game'
})

const joinAsGuest = async () => {
  if (!guestName.value.trim()) return
  
  joining.value = true
  
  try {
    await roomStore.joinRoomAsGuest(room.value.id, guestName.value)
    router.push(`/room/${room.value.id}`)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to join room'
  } finally {
    joining.value = false
  }
}

const joinAsUser = async () => {
  joining.value = true
  
  try {
    await roomStore.joinRoom(room.value.id)
    router.push(`/room/${room.value.id}`)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to join room'
  } finally {
    joining.value = false
  }
}

onMounted(async () => {
  const inviteCode = route.params.inviteCode
  
  try {
    room.value = await roomStore.loadRoomByInvite(inviteCode)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Invalid invite code'
  } finally {
    loading.value = false
  }
})
</script>