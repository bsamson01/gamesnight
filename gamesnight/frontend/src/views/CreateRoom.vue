<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="bg-white rounded-lg shadow p-6">
        <h1 class="text-2xl font-bold mb-6">Create a Game Room</h1>
        
        <form @submit.prevent="createRoom">
          <!-- Game Selection -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Select Game
            </label>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <label 
                v-for="game in games" 
                :key="game.slug"
                class="relative flex items-center p-4 border rounded-lg cursor-pointer transition"
                :class="{
                  'border-indigo-500 bg-indigo-50': selectedGame === game.slug,
                  'border-gray-300 hover:border-gray-400': selectedGame !== game.slug
                }"
              >
                <input
                  type="radio"
                  v-model="selectedGame"
                  :value="game.slug"
                  class="sr-only"
                />
                <div class="flex-1">
                  <div class="flex items-center">
                    <span class="text-2xl mr-3">{{ game.emoji }}</span>
                    <div>
                      <div class="font-medium">{{ game.name }}</div>
                      <div class="text-sm text-gray-600">{{ game.players }}</div>
                    </div>
                  </div>
                </div>
              </label>
            </div>
          </div>

          <!-- Theme Selection -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Select Themes (optional)
            </label>
            <div class="space-y-2">
              <label 
                v-for="theme in themes" 
                :key="theme.id"
                class="flex items-center"
              >
                <input
                  type="checkbox"
                  v-model="selectedThemes"
                  :value="theme.id"
                  class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                />
                <span class="ml-2 text-sm">{{ theme.label }}</span>
              </label>
            </div>
            <p class="mt-2 text-xs text-gray-500">
              If no themes are selected, all safe prompts will be used
            </p>
          </div>

          <!-- Submit Button -->
          <div class="flex justify-end space-x-4">
            <router-link 
              to="/dashboard"
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </router-link>
            <button
              type="submit"
              :disabled="!selectedGame || loading"
              class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? 'Creating...' : 'Create Room' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRoomStore } from '@/stores/room'

const router = useRouter()
const roomStore = useRoomStore()

const selectedGame = ref('')
const selectedThemes = ref([])
const loading = ref(false)

const games = [
  { slug: 'would_you_rather', name: 'Would You Rather', emoji: '🤔', players: '2+ players' },
  { slug: 'truth_or_dare', name: 'Truth or Dare', emoji: '😈', players: '2+ players' },
  { slug: 'sixty_seconds', name: '60 Seconds', emoji: '⏱️', players: '2+ players' },
  { slug: 'hot_seat', name: 'Hot Seat', emoji: '🔥', players: '3+ players' },
  { slug: 'draw_guess', name: 'Draw & Guess', emoji: '🎨', players: '3+ players' }
]

// Mock themes - in production, fetch from API
const themes = [
  { id: 1, label: 'General' },
  { id: 2, label: 'Funny' },
  { id: 3, label: 'Deep' },
  { id: 4, label: 'Family Friendly' },
  { id: 5, label: 'Party' },
  { id: 6, label: 'Icebreaker' }
]

const createRoom = async () => {
  if (!selectedGame.value) return
  
  loading.value = true
  
  try {
    const room = await roomStore.createRoom({
      game_slug: selectedGame.value,
      theme_ids: selectedThemes.value
    })
    
    router.push(`/room/${room.id}`)
  } catch (error) {
    console.error('Failed to create room:', error)
    alert('Failed to create room. Please try again.')
  } finally {
    loading.value = false
  }
}
</script>