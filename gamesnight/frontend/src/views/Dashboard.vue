<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="mt-2 text-gray-600">Welcome back, {{ authStore.user?.email }}!</p>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <router-link 
          to="/create-room"
          class="bg-white p-6 rounded-lg shadow hover:shadow-lg transition text-center"
        >
          <div class="text-4xl mb-4">🎮</div>
          <h3 class="text-lg font-semibold">Create Room</h3>
          <p class="text-gray-600 mt-2">Start a new game with friends</p>
        </router-link>

        <div class="bg-white p-6 rounded-lg shadow">
          <div class="text-4xl mb-4">🔗</div>
          <h3 class="text-lg font-semibold">Join Room</h3>
          <form @submit.prevent="joinWithCode" class="mt-4">
            <input
              v-model="inviteCode"
              type="text"
              placeholder="Enter invite code"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
            <button
              type="submit"
              class="mt-2 w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700"
            >
              Join
            </button>
          </form>
        </div>

        <router-link 
          v-if="!authStore.isPaidUser"
          to="/subscription"
          class="bg-gradient-to-br from-purple-600 to-indigo-600 text-white p-6 rounded-lg shadow hover:shadow-lg transition text-center"
        >
          <div class="text-4xl mb-4">🌟</div>
          <h3 class="text-lg font-semibold">Go Premium</h3>
          <p class="mt-2">Remove ads & invite guests</p>
        </router-link>

        <div 
          v-else
          class="bg-green-50 border-2 border-green-200 p-6 rounded-lg text-center"
        >
          <div class="text-4xl mb-4">✨</div>
          <h3 class="text-lg font-semibold text-green-800">Premium Member</h3>
          <p class="text-green-600 mt-2">Valid until {{ formatDate(authStore.user?.paid_until) }}</p>
        </div>
      </div>

      <!-- Game Stats -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">Your Stats</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center">
            <div class="text-3xl font-bold text-indigo-600">0</div>
            <div class="text-sm text-gray-600">Games Played</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-green-600">0</div>
            <div class="text-sm text-gray-600">Wins</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-purple-600">0</div>
            <div class="text-sm text-gray-600">Friends</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-yellow-600">0</div>
            <div class="text-sm text-gray-600">Achievements</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRoomStore } from '@/stores/room'

const router = useRouter()
const authStore = useAuthStore()
const roomStore = useRoomStore()

const inviteCode = ref('')

const joinWithCode = async () => {
  if (!inviteCode.value.trim()) return
  
  try {
    const room = await roomStore.loadRoomByInvite(inviteCode.value)
    router.push(`/room/${room.id}`)
  } catch (error) {
    console.error('Failed to join room:', error)
    alert('Invalid invite code')
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}
</script>