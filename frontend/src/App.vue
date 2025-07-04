<template>
  <ErrorBoundary>
    <div id="app" class="min-h-screen bg-pure-white">
      <Navbar v-if="showNavbar" />
      <main class="flex-1">
        <router-view />
      </main>
      <AdBanner v-if="showAds" />
      <ToastContainer />
    </div>
  </ErrorBoundary>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ErrorBoundary from '@/components/ErrorBoundary.vue'
import Navbar from '@/components/Navbar.vue'
import AdBanner from '@/components/AdBanner.vue'
import ToastContainer from '@/components/ToastContainer.vue'

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
  filter: drop-shadow(0 0 2em rgba(0, 118, 219, 0.67)); /* electric-blue with transparency */
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em rgba(142, 207, 139, 0.67)); /* soft-mint with transparency */
}
</style>
