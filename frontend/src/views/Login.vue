<template>
  <div class="min-h-screen flex items-center justify-center bg-pure-white py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-jet-black">
          Sign in to your account
        </h2>
        <p class="mt-2 text-center text-sm text-cool-gray">
          Or
          <router-link to="/register" class="font-medium text-electric-blue hover:text-electric-blue/80">
            create a new account
          </router-link>
        </p>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email" class="sr-only">Email address</label>
            <input
              id="email"
              v-model="form.email"
              name="email"
              type="email"
              autocomplete="email"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-cool-gray placeholder-cool-gray text-jet-black rounded-t-md focus:outline-none focus:ring-electric-blue focus:border-electric-blue focus:z-10 sm:text-sm"
              placeholder="Email address"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Password</label>
            <input
              id="password"
              v-model="form.password"
              name="password"
              type="password"
              autocomplete="current-password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-cool-gray placeholder-cool-gray text-jet-black rounded-b-md focus:outline-none focus:ring-electric-blue focus:border-electric-blue focus:z-10 sm:text-sm"
              placeholder="Password"
            />
          </div>
        </div>

        <div>
          <Button
            type="submit"
            variant="primary"
            size="lg"
            full-width
            :loading="loading"
          >
            Sign in
          </Button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import Button from '@/components/ui/Button.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const toast = useToast()

const form = reactive({
  email: '',
  password: ''
})

const loading = ref(false)

const handleSubmit = async () => {
  loading.value = true
  
  try {
    await authStore.login(form)
    
    toast.success('Welcome back!', 'Successfully signed in')
    
    // Redirect to intended page or dashboard
    const redirect = route.query.redirect || '/dashboard'
    router.push(redirect)
  } catch (err) {
    const errorMessage = err.response?.data?.detail || 'Login failed. Please check your credentials.'
    toast.error('Sign in failed', errorMessage)
  } finally {
    loading.value = false
  }
}
</script>