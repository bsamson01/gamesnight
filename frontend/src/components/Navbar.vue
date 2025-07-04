<template>
  <nav class="bg-pure-white shadow-sm border-b border-cool-gray">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <router-link to="/" class="flex items-center">
            <span class="text-2xl font-bold text-electric-blue">🎮 GameNight</span>
          </router-link>
        </div>

        <div class="flex items-center space-x-4">
          <template v-if="authStore.isAuthenticated">
            <router-link 
              to="/dashboard" 
              class="text-jet-black hover:text-electric-blue px-3 py-2 rounded-md text-sm font-medium"
            >
              Dashboard
            </router-link>
            
            <router-link 
              to="/create-room" 
              class="text-jet-black hover:text-electric-blue px-3 py-2 rounded-md text-sm font-medium"
            >
              Create Room
            </router-link>
            
            <router-link 
              v-if="!authStore.isPaidUser"
              to="/subscription" 
              class="bg-bold-red text-pure-white px-4 py-2 rounded-md text-sm font-medium hover:bg-bold-red/90"
            >
              🌟 Go Premium
            </router-link>
            
            <div class="relative">
              <button 
                @click="showDropdown = !showDropdown"
                class="flex items-center text-jet-black hover:text-electric-blue px-3 py-2 rounded-md text-sm font-medium"
              >
                <span>{{ authStore.user?.email }}</span>
                <svg class="ml-2 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
              
              <div 
                v-if="showDropdown"
                class="absolute right-0 mt-2 w-48 bg-pure-white rounded-md shadow-lg py-1 z-50"
              >
                <button 
                  @click="logout"
                  class="block w-full text-left px-4 py-2 text-sm text-jet-black hover:bg-cool-gray/20"
                >
                  Logout
                </button>
              </div>
            </div>
          </template>
          
          <template v-else>
            <router-link 
              to="/login" 
              class="text-jet-black hover:text-electric-blue px-3 py-2 rounded-md text-sm font-medium"
            >
              Login
            </router-link>
            <router-link 
              to="/register" 
              class="bg-electric-blue text-pure-white px-4 py-2 rounded-md text-sm font-medium hover:bg-electric-blue/90"
            >
              Sign Up
            </router-link>
          </template>
        </div>
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

const logout = async () => {
  showDropdown.value = false
  await authStore.logout()
  router.push('/')
}
</script>