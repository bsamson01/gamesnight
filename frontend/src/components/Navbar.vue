<template>
  <nav class="bg-pure-white shadow-sm border-b border-cool-gray">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <router-link to="/" class="flex items-center">
            <span class="text-xl sm:text-2xl font-bold text-electric-blue">🎮 GameNight</span>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-4">
          <template v-if="authStore.isAuthenticated">
            <router-link 
              to="/dashboard" 
              class="text-jet-black hover:text-electric-blue px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Dashboard
            </router-link>
            
            <router-link 
              to="/create-room" 
              class="text-jet-black hover:text-electric-blue px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Create Room
            </router-link>
            
            <router-link 
              v-if="!authStore.isPaidUser"
              to="/subscription" 
              class="bg-bold-red text-pure-white px-4 py-2 rounded-md text-sm font-medium hover:bg-bold-red/90 transition-colors"
            >
              🌟 Go Premium
            </router-link>
            
            <div class="relative">
              <button 
                @click="showDropdown = !showDropdown"
                class="flex items-center text-jet-black hover:text-electric-blue px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                <span class="truncate max-w-32">{{ authStore.user?.email }}</span>
                <svg class="ml-2 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
              
              <div 
                v-if="showDropdown"
                class="absolute right-0 mt-2 w-48 bg-pure-white rounded-md shadow-lg py-1 z-50 border border-gray-200"
              >
                <button 
                  @click="logout"
                  class="block w-full text-left px-4 py-2 text-sm text-jet-black hover:bg-cool-gray/20 transition-colors"
                >
                  Logout
                </button>
              </div>
            </div>
          </template>
          
          <template v-else>
            <router-link 
              to="/login" 
              class="text-jet-black hover:text-electric-blue px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Login
            </router-link>
            <router-link 
              to="/register" 
              class="bg-electric-blue text-pure-white px-4 py-2 rounded-md text-sm font-medium hover:bg-electric-blue/90 transition-colors"
            >
              Sign Up
            </router-link>
          </template>
        </div>

        <!-- Mobile menu button -->
        <div class="md:hidden flex items-center">
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-electric-blue"
          >
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-200 bg-white">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <template v-if="authStore.isAuthenticated">
          <router-link 
            to="/dashboard"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
          >
            Dashboard
          </router-link>
          
          <router-link 
            to="/create-room"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
          >
            Create Room
          </router-link>
          
          <router-link 
            v-if="!authStore.isPaidUser"
            to="/subscription"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium text-bold-red hover:text-bold-red/90 hover:bg-gray-50"
          >
            🌟 Go Premium
          </router-link>
          
          <div class="border-t border-gray-200 pt-4">
            <div class="px-3 py-2">
              <div class="text-base font-medium text-gray-800">{{ authStore.user?.email }}</div>
              <div class="text-sm text-gray-500">{{ authStore.isPaidUser ? 'Premium Member' : 'Free Account' }}</div>
            </div>
            <button 
              @click="logout"
              class="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
            >
              Logout
            </button>
          </div>
        </template>
        
        <template v-else>
          <router-link 
            to="/login"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
          >
            Login
          </router-link>
          <router-link 
            to="/register"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium bg-electric-blue text-white hover:bg-electric-blue/90 mx-3"
          >
            Sign Up
          </router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const showDropdown = ref(false)
const mobileMenuOpen = ref(false)

const logout = async () => {
  showDropdown.value = false
  await authStore.logout()
  router.push('/')
}
</script>