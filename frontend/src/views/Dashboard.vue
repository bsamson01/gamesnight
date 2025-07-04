<template>
  <div class="min-h-screen bg-gray-50 py-4 sm:py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-6 sm:mb-8">
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="mt-2 text-gray-600">Welcome back, {{ authStore.user?.email }}!</p>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-8 sm:mb-12">
        <Card variant="default" hoverable>
          <router-link 
            to="/create-room"
            class="block text-center p-2"
          >
            <div class="text-4xl mb-4">🎮</div>
            <h3 class="text-lg font-semibold">Create Room</h3>
            <p class="text-gray-600 mt-2">Start a new game with friends</p>
          </router-link>
        </Card>

        <Card variant="default">
          <div class="text-center">
            <div class="text-4xl mb-4">🔗</div>
            <h3 class="text-lg font-semibold mb-4">Join Room</h3>
            <form @submit.prevent="joinWithCode" class="space-y-3">
              <input
                v-model="inviteCode"
                type="text"
                placeholder="Enter invite code"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-electric-blue focus:border-electric-blue text-center"
              />
              <Button
                type="submit"
                variant="primary"
                size="md"
                full-width
                :loading="joining"
              >
                Join Game
              </Button>
            </form>
          </div>
        </Card>

        <Card 
          v-if="!authStore.isPaidUser"
          variant="default"
          hoverable
        >
          <router-link 
            to="/subscription"
            class="block text-center p-2 bg-gradient-to-br from-purple-600 to-indigo-600 text-white rounded-md -m-6"
          >
            <div class="p-6">
              <div class="text-4xl mb-4">🌟</div>
              <h3 class="text-lg font-semibold">Go Premium</h3>
              <p class="mt-2">Remove ads & invite guests</p>
            </div>
          </router-link>
        </Card>

        <Card 
          v-else
          variant="filled"
          class="border-2 border-green-200 bg-green-50"
        >
          <div class="text-center">
            <div class="text-4xl mb-4">✨</div>
            <h3 class="text-lg font-semibold text-green-800">Premium Member</h3>
            <p class="text-green-600 mt-2">Valid until {{ formatDate(authStore.user?.paid_until) }}</p>
          </div>
        </Card>
      </div>

      <!-- Recent Activity -->
      <div class="mb-8">
        <Card variant="default">
          <template #header>
            <h2 class="text-xl font-semibold">Recent Activity</h2>
          </template>
          
          <EmptyState
            title="No recent games"
            description="Start playing to see your game history here"
            icon="🎮"
          >
            <template #action>
              <Button variant="primary" @click="$router.push('/create-room')">
                Create Your First Room
              </Button>
            </template>
          </EmptyState>
        </Card>
      </div>

      <!-- Game Stats -->
      <Card variant="default">
        <template #header>
          <h2 class="text-xl font-semibold">Your Stats</h2>
        </template>
        
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 sm:gap-6">
          <div class="text-center p-4 bg-gray-50 rounded-lg">
            <div class="text-2xl sm:text-3xl font-bold text-indigo-600">0</div>
            <div class="text-xs sm:text-sm text-gray-600 mt-1">Games Played</div>
          </div>
          <div class="text-center p-4 bg-gray-50 rounded-lg">
            <div class="text-2xl sm:text-3xl font-bold text-green-600">0</div>
            <div class="text-xs sm:text-sm text-gray-600 mt-1">Wins</div>
          </div>
          <div class="text-center p-4 bg-gray-50 rounded-lg">
            <div class="text-2xl sm:text-3xl font-bold text-purple-600">0</div>
            <div class="text-xs sm:text-sm text-gray-600 mt-1">Friends</div>
          </div>
          <div class="text-center p-4 bg-gray-50 rounded-lg">
            <div class="text-2xl sm:text-3xl font-bold text-yellow-600">0</div>
            <div class="text-xs sm:text-sm text-gray-600 mt-1">Achievements</div>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRoomStore } from '@/stores/room'
import { useToast } from '@/composables/useToast'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import EmptyState from '@/components/ui/EmptyState.vue'

const router = useRouter()
const authStore = useAuthStore()
const roomStore = useRoomStore()
const toast = useToast()

const inviteCode = ref('')
const joining = ref(false)

const joinWithCode = async () => {
  if (!inviteCode.value.trim()) {
    toast.warning('Please enter an invite code')
    return
  }
  
  joining.value = true
  
  try {
    const room = await roomStore.loadRoomByInvite(inviteCode.value)
    toast.success('Joined room successfully!')
    router.push(`/room/${room.id}`)
  } catch (error) {
    console.error('Failed to join room:', error)
    toast.error('Invalid invite code', 'Please check the code and try again')
  } finally {
    joining.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}
</script>