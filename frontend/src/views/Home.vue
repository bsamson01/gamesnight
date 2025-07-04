<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <div class="bg-gradient-to-br from-indigo-600 to-purple-700 text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div class="text-center">
          <h1 class="text-5xl font-bold mb-6">
            🎮 Welcome to GameNight
          </h1>
          <p class="text-xl mb-8 text-indigo-100">
            Play exciting mini-games with friends in real-time!
          </p>
          <div class="space-x-4">
            <router-link 
              v-if="!authStore.isAuthenticated"
              to="/register" 
              class="bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
            >
              Get Started Free
            </router-link>
            <router-link 
              v-else
              to="/create-room" 
              class="bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
            >
              Create a Room
            </router-link>
            <router-link 
              to="/dashboard" 
              class="bg-indigo-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-indigo-400 transition"
            >
              Browse Games
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Games Section -->
    <div class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-center mb-12">Our Games</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div 
            v-for="game in games" 
            :key="game.slug"
            class="bg-gray-50 rounded-lg p-6 hover:shadow-lg transition"
          >
            <div class="text-4xl mb-4">{{ game.emoji }}</div>
            <h3 class="text-xl font-semibold mb-2">{{ game.name }}</h3>
            <p class="text-gray-600">{{ game.description }}</p>
            <div class="mt-4 text-sm text-indigo-600">
              {{ game.duration }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-center mb-12">Why GameNight?</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center">
            <div class="text-4xl mb-4">🚀</div>
            <h3 class="text-xl font-semibold mb-2">Real-time Gameplay</h3>
            <p class="text-gray-600">
              Synchronized timers and instant updates for all players
            </p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-4">🎨</div>
            <h3 class="text-xl font-semibold mb-2">Multiple Themes</h3>
            <p class="text-gray-600">
              Choose from various themes to customize your game experience
            </p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-4">👥</div>
            <h3 class="text-xl font-semibold mb-2">Guest Invites</h3>
            <p class="text-gray-600">
              Premium users can invite guests without requiring sign-up
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="py-16 bg-indigo-600 text-white">
      <div class="max-w-4xl mx-auto text-center px-4">
        <h2 class="text-3xl font-bold mb-4">Ready to Start Playing?</h2>
        <p class="text-xl mb-8 text-indigo-100">
          Join thousands of players having fun together
        </p>
        <router-link 
          v-if="!authStore.isAuthenticated"
          to="/register" 
          class="bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition inline-block"
        >
          Sign Up Now - It's Free!
        </router-link>
        <router-link 
          v-else
          to="/create-room" 
          class="bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition inline-block"
        >
          Create Your First Room
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const games = [
  {
    slug: 'would_you_rather',
    name: 'Would You Rather',
    emoji: '🤔',
    description: 'Choose between two interesting options and see what others pick!',
    duration: '60 seconds per round'
  },
  {
    slug: 'truth_or_dare',
    name: 'Truth or Dare',
    emoji: '😈',
    description: 'Classic party game with truths to reveal and dares to complete.',
    duration: '60 seconds per turn'
  },
  {
    slug: 'sixty_seconds',
    name: '60 Seconds',
    emoji: '⏱️',
    description: 'List as many unique items as you can in the given category!',
    duration: '60 seconds per round'
  },
  {
    slug: 'hot_seat',
    name: 'Hot Seat',
    emoji: '🔥',
    description: 'One player answers rapid-fire questions from everyone else.',
    duration: '60 seconds in the hot seat'
  },
  {
    slug: 'draw_guess',
    name: 'Draw & Guess',
    emoji: '🎨',
    description: 'Draw the word while others try to guess what it is!',
    duration: '90s draw, 60s guess'
  }
]
</script>