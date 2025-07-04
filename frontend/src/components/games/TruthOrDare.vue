<template>
  <div class="text-center">
    <h2 class="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8">Truth or Dare</h2>
    
    <div v-if="prompt" class="space-y-6">
      <!-- Current Player -->
      <div v-if="currentPlayer" class="bg-gradient-to-r from-purple-500 to-pink-500 text-white p-4 sm:p-6 rounded-lg">
        <h3 class="text-lg sm:text-xl font-semibold mb-2">It's your turn!</h3>
        <p class="text-sm sm:text-base">{{ currentPlayer.name }}</p>
      </div>

      <!-- Prompt Display -->
      <Card variant="elevated" class="max-w-2xl mx-auto">
        <div class="text-center p-4 sm:p-6">
          <div class="text-4xl sm:text-6xl mb-4">
            {{ prompt.type === 'truth' ? '🤔' : '😈' }}
          </div>
          <div class="text-lg sm:text-xl font-semibold mb-2 text-gray-800">
            {{ prompt.type === 'truth' ? 'Truth' : 'Dare' }}
          </div>
          <p class="text-base sm:text-lg text-gray-700 leading-relaxed">
            {{ prompt.text }}
          </p>
        </div>
      </Card>

      <!-- Action Buttons -->
      <div v-if="!hasCompleted" class="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center max-w-md mx-auto">
        <Button
          variant="success"
          size="lg"
          @click="completeAction('completed')"
          :loading="submitting"
          full-width
        >
          ✅ Completed
        </Button>
        <Button
          variant="danger"
          size="lg"
          @click="completeAction('skipped')"
          :loading="submitting"
          full-width
        >
          ⏭️ Skip
        </Button>
      </div>

      <!-- Results -->
      <div v-if="hasCompleted" class="text-center">
        <div class="text-lg font-semibold text-green-600 mb-4">
          {{ result === 'completed' ? '🎉 Well done!' : '😅 Maybe next time!' }}
        </div>
        <p class="text-gray-600">Waiting for next round...</p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else class="py-12">
      <LoadingSpinner size="lg" text="Loading truth or dare..." />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useGameStore } from '@/stores/game'
import { useRoomStore } from '@/stores/room'
import { useToast } from '@/composables/useToast'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'

const props = defineProps({
  prompt: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['action'])

const gameStore = useGameStore()
const roomStore = useRoomStore()
const toast = useToast()

const submitting = ref(false)
const result = ref(null)

const hasCompleted = computed(() => result.value !== null)

const currentPlayer = computed(() => {
  // This would be determined by the game state
  return {
    name: 'Current Player' // Replace with actual player data
  }
})

const completeAction = async (actionResult) => {
  submitting.value = true
  
  try {
    await emit('action', 'complete', {
      prompt_id: props.prompt.id,
      result: actionResult
    })
    
    result.value = actionResult
    
    if (actionResult === 'completed') {
      toast.success('Great job!', 'You completed the challenge!')
    } else {
      toast.info('Skipped', 'Maybe next time!')
    }
  } catch (error) {
    console.error('Failed to complete action:', error)
    toast.error('Failed to submit', 'Please try again')
  } finally {
    submitting.value = false
  }
}
</script>