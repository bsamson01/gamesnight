<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          🌟 Upgrade to Premium
        </h1>
        <p class="text-xl text-gray-600">
          Enjoy GameNight without limits
        </p>
      </div>

      <!-- Benefits -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-2xl font-semibold mb-4">Free Plan</h2>
          <ul class="space-y-3">
            <li class="flex items-start">
              <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              <span>Access to all 5 games</span>
            </li>
            <li class="flex items-start">
              <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              <span>Create unlimited rooms</span>
            </li>
            <li class="flex items-start">
              <svg class="w-5 h-5 text-red-500 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
              </svg>
              <span class="text-gray-500">Ads displayed</span>
            </li>
            <li class="flex items-start">
              <svg class="w-5 h-5 text-red-500 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
              </svg>
              <span class="text-gray-500">No guest invites</span>
            </li>
          </ul>
        </div>

        <div class="bg-gradient-to-br from-purple-600 to-indigo-600 text-white rounded-lg shadow p-6">
          <h2 class="text-2xl font-semibold mb-4">Premium Plan</h2>
          <ul class="space-y-3">
            <li class="flex items-start">
              <svg class="w-5 h-5 text-white mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              <span>Everything in Free</span>
            </li>
            <li class="flex items-start">
              <svg class="w-5 h-5 text-white mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              <span>No advertisements</span>
            </li>
            <li class="flex items-start">
              <svg class="w-5 h-5 text-white mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              <span>Invite guests without signup</span>
            </li>
            <li class="flex items-start">
              <svg class="w-5 h-5 text-white mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              <span>Priority support</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- Pricing -->
      <div class="bg-white rounded-lg shadow p-8 mb-8">
        <h2 class="text-2xl font-semibold mb-6 text-center">Choose Your Plan</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Day Pass -->
          <div class="border-2 border-gray-200 rounded-lg p-6 text-center">
            <h3 class="text-xl font-semibold mb-2">Day Pass</h3>
            <div class="text-4xl font-bold mb-4">$1.99</div>
            <p class="text-gray-600 mb-6">24 hours of premium access</p>
            <div id="paypal-button-day" class="min-h-[45px]"></div>
          </div>

          <!-- Monthly Pass -->
          <div class="border-2 border-indigo-500 rounded-lg p-6 text-center relative">
            <div class="absolute -top-3 left-1/2 transform -translate-x-1/2">
              <span class="bg-indigo-500 text-white px-3 py-1 rounded-full text-sm">
                Best Value
              </span>
            </div>
            <h3 class="text-xl font-semibold mb-2">Monthly Pass</h3>
            <div class="text-4xl font-bold mb-4">$9.99</div>
            <p class="text-gray-600 mb-6">30 days of premium access</p>
            <div id="paypal-button-month" class="min-h-[45px]"></div>
          </div>
        </div>
      </div>

      <!-- FAQ -->
      <div class="bg-white rounded-lg shadow p-8">
        <h2 class="text-2xl font-semibold mb-6">Frequently Asked Questions</h2>
        
        <div class="space-y-4">
          <div>
            <h3 class="font-medium mb-2">Can I cancel anytime?</h3>
            <p class="text-gray-600">Yes! Your premium access will remain active until the end of your current billing period.</p>
          </div>
          
          <div>
            <h3 class="font-medium mb-2">How do guest invites work?</h3>
            <p class="text-gray-600">As a premium member, you can invite guests to your rooms without requiring them to create an account.</p>
          </div>
          
          <div>
            <h3 class="font-medium mb-2">Is my payment secure?</h3>
            <p class="text-gray-600">Yes! All payments are processed securely through PayPal. We never store your payment information.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { loadScript } from '@paypal/paypal-js'
import { useAuthStore } from '@/stores/auth'
import { paymentAPI } from '@/services/api'

const authStore = useAuthStore()
const loading = ref(false)

const handlePaymentSuccess = async (orderID, paymentType) => {
  loading.value = true
  
  try {
    const response = await paymentAPI.verify({
      order_id: orderID,
      payment_type: paymentType
    })
    
    // Update user's payment status
    authStore.updateUserPaymentStatus(true, response.data.expires_at)
    
    // Show success message
    alert('Payment successful! You now have premium access.')
  } catch (error) {
    console.error('Payment verification failed:', error)
    alert('Payment verification failed. Please contact support.')
  } finally {
    loading.value = false
  }
}

const initializePayPal = async () => {
  try {
    // Get payment config from backend
    const config = await paymentAPI.getConfig()
    const { client_id } = config.data
    
    // Load PayPal script
    const paypal = await loadScript({
      clientId: client_id,
      currency: 'USD'
    })
    
    // Day Pass Button
    paypal.Buttons({
      createOrder: (data, actions) => {
        return actions.order.create({
          purchase_units: [{
            amount: {
              value: '1.99'
            },
            description: 'GameNight Day Pass'
          }]
        })
      },
      onApprove: async (data, actions) => {
        const order = await actions.order.capture()
        await handlePaymentSuccess(order.id, 'day_pass')
      },
      onError: (err) => {
        console.error('PayPal error:', err)
        alert('Payment failed. Please try again.')
      }
    }).render('#paypal-button-day')
    
    // Monthly Pass Button
    paypal.Buttons({
      createOrder: (data, actions) => {
        return actions.order.create({
          purchase_units: [{
            amount: {
              value: '9.99'
            },
            description: 'GameNight Monthly Pass'
          }]
        })
      },
      onApprove: async (data, actions) => {
        const order = await actions.order.capture()
        await handlePaymentSuccess(order.id, 'month_pass')
      },
      onError: (err) => {
        console.error('PayPal error:', err)
        alert('Payment failed. Please try again.')
      }
    }).render('#paypal-button-month')
    
  } catch (error) {
    console.error('Failed to initialize PayPal:', error)
  }
}

onMounted(() => {
  initializePayPal()
})
</script>