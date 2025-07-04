<template>
  <div class="flex items-center space-x-2">
    <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
    </svg>
    <span 
      class="font-mono text-lg"
      :class="{
        'text-red-600': remaining <= 10,
        'text-yellow-600': remaining > 10 && remaining <= 30,
        'text-gray-800': remaining > 30
      }"
    >
      {{ formattedTime }}
    </span>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useGameStore } from '@/stores/game'

const gameStore = useGameStore()
const remaining = ref(0)
let intervalId = null

const formattedTime = computed(() => {
  const seconds = Math.max(0, Math.floor(remaining.value))
  return `0:${seconds.toString().padStart(2, '0')}`
})

const updateTimer = () => {
  gameStore.updateTimerRemaining()
  remaining.value = gameStore.timer.remaining
  
  if (remaining.value <= 0 && intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
}

onMounted(() => {
  updateTimer()
  intervalId = setInterval(updateTimer, 100) // Update every 100ms for smooth countdown
})

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})
</script>