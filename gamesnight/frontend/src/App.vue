<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <Navbar v-if="showNavbar" />
    <main class="flex-1">
      <router-view />
    </main>
    <AdBanner v-if="showAds" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Navbar from '@/components/Navbar.vue'
import AdBanner from '@/components/AdBanner.vue'

const route = useRoute()
const authStore = useAuthStore()

const showNavbar = computed(() => {
  const hideNavbarRoutes = ['GameRoom']
  return !hideNavbarRoutes.includes(route.name)
})

const showAds = computed(() => {
  return authStore.showAds && authStore.isAuthenticated
})
</script>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
