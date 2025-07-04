<template>
  <div v-if="hasError" class="min-h-screen flex items-center justify-center bg-gray-50">
    <Card variant="elevated" class="max-w-md mx-4">
      <div class="text-center p-8">
        <div class="text-6xl mb-4">😵</div>
        <h2 class="text-2xl font-bold text-gray-900 mb-4">Oops! Something went wrong</h2>
        <p class="text-gray-600 mb-6">
          We're sorry, but something unexpected happened. Please try refreshing the page.
        </p>
        
        <div class="space-y-3">
          <Button variant="primary" size="lg" full-width @click="reload">
            🔄 Refresh Page
          </Button>
          <Button variant="outline" size="md" full-width @click="goHome">
            🏠 Go Home
          </Button>
        </div>
        
        <details v-if="error && isDev" class="mt-6 text-left">
          <summary class="cursor-pointer text-sm text-gray-500 hover:text-gray-700">
            Show Error Details
          </summary>
          <pre class="mt-2 text-xs bg-gray-100 p-3 rounded overflow-auto max-h-32">{{ error.stack || error.message }}</pre>
        </details>
      </div>
    </Card>
  </div>
  
  <slot v-else />
</template>

<script setup>
import { ref, onErrorCaptured } from 'vue'
import { useRouter } from 'vue-router'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'

const router = useRouter()

const hasError = ref(false)
const error = ref(null)
const isDev = import.meta.env.DEV

onErrorCaptured((err, instance, info) => {
  console.error('Error captured by ErrorBoundary:', err)
  console.error('Component info:', info)
  
  hasError.value = true
  error.value = err
  
  // Prevent the error from propagating further
  return false
})

const reload = () => {
  window.location.reload()
}

const goHome = () => {
  hasError.value = false
  error.value = null
  router.push('/')
}

// Global error handler for unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason)
  hasError.value = true
  error.value = new Error(event.reason)
})

// Global error handler for JavaScript errors
window.addEventListener('error', (event) => {
  console.error('Global error:', event.error)
  hasError.value = true
  error.value = event.error
})
</script>