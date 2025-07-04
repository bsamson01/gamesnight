<template>
  <div class="min-h-screen flex items-center justify-center bg-pure-white py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-jet-black">
          Create a new account
        </h2>
        <p class="mt-2 text-center text-sm text-cool-gray">
          Or
          <router-link to="/login" class="font-medium text-electric-blue hover:text-electric-blue/80">
            sign in to your existing account
          </router-link>
        </p>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div v-if="error" class="bg-bold-red/10 border border-bold-red/20 text-bold-red px-4 py-3 rounded">
          {{ error }}
        </div>
        
        <div class="space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-jet-black">
              Email address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autocomplete="email"
              required
              v-model="form.email"
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-cool-gray placeholder-cool-gray text-jet-black rounded-md focus:outline-none focus:ring-electric-blue focus:border-electric-blue focus:z-10 sm:text-sm"
              placeholder="you@example.com"
            >
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-jet-black">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autocomplete="new-password"
              required
              v-model="form.password"
              minlength="8"
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-cool-gray placeholder-cool-gray text-jet-black rounded-md focus:outline-none focus:ring-electric-blue focus:border-electric-blue focus:z-10 sm:text-sm"
              placeholder="Minimum 8 characters"
            >
          </div>
          
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-jet-black">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              autocomplete="new-password"
              required
              v-model="form.confirmPassword"
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-cool-gray placeholder-cool-gray text-jet-black rounded-md focus:outline-none focus:ring-electric-blue focus:border-electric-blue focus:z-10 sm:text-sm"
              placeholder="Re-enter your password"
            >
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-pure-white bg-electric-blue hover:bg-electric-blue/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-electric-blue disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Creating account...</span>
            <span v-else>Create account</span>
          </button>
        </div>
        
        <div class="text-xs text-cool-gray text-center">
          By creating an account, you agree to our terms and conditions.
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref('')

const handleSubmit = async () => {
  error.value = ''
  
  // Validate passwords match
  if (form.password !== form.confirmPassword) {
    error.value = 'Passwords do not match'
    return
  }
  
  // Validate password length
  if (form.password.length < 8) {
    error.value = 'Password must be at least 8 characters'
    return
  }
  
  loading.value = true
  
  try {
    await authStore.register({
      email: form.email,
      password: form.password
    })
    
    // Redirect to dashboard after successful registration
    router.push('/dashboard')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>