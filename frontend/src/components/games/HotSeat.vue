<template>
  <div class="text-center">
    <h2 class="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8">Hot Seat</h2>
    
    <div v-if="prompt" class="space-y-6">
      <!-- Hot Seat Player -->
      <div v-if="hotSeatPlayer" class="bg-gradient-to-r from-orange-500 to-red-500 text-white p-4 sm:p-6 rounded-lg max-w-2xl mx-auto">
        <div class="text-4xl sm:text-6xl mb-4">🔥</div>
        <h3 class="text-lg sm:text-xl font-semibold mb-2">In the Hot Seat</h3>
        <p class="text-xl sm:text-2xl font-bold">{{ hotSeatPlayer.name }}</p>
        <p class="text-sm sm:text-base mt-2 opacity-90">Answer rapid-fire questions for 60 seconds!</p>
      </div>

      <!-- Question Display for Hot Seat Player -->
      <div v-if="isHotSeatPlayer && currentQuestion" class="max-w-2xl mx-auto">
        <Card variant="elevated">
          <div class="text-center p-6">
            <div class="text-4xl mb-4">❓</div>
            <p class="text-lg sm:text-xl text-gray-800 leading-relaxed">
              {{ currentQuestion.text }}
            </p>
          </div>
        </Card>
      </div>

      <!-- Question Input for Other Players -->
      <div v-if="!isHotSeatPlayer && !hasSubmittedQuestion" class="max-w-md mx-auto">
        <Card variant="default">
          <template #header>
            <h3 class="text-lg font-semibold">Ask {{ hotSeatPlayer?.name }} a question</h3>
          </template>
          
          <div class="space-y-4">
            <textarea
              v-model="questionText"
              placeholder="Type your question here..."
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-electric-blue focus:border-electric-blue resize-none"
              :disabled="gameStore.timerExpired"
            ></textarea>
            
            <Button
              variant="primary"
              size="md"
              full-width
              @click="submitQuestion"
              :loading="submitting"
              :disabled="!questionText.trim() || gameStore.timerExpired"
            >
              Submit Question
            </Button>
          </div>
        </Card>
      </div>

      <!-- Submitted Questions (for moderator/host) -->
      <div v-if="isHost && submittedQuestions.length > 0" class="max-w-2xl mx-auto">
        <Card variant="default">
          <template #header>
            <h3 class="text-lg font-semibold">Questions Queue ({{ submittedQuestions.length }})</h3>
          </template>
          
          <div class="space-y-2 max-h-64 overflow-y-auto">
            <div
              v-for="(question, index) in submittedQuestions"
              :key="index"
              class="flex items-center justify-between p-3 bg-gray-50 rounded"
            >
              <span class="text-sm">{{ question.text }}</span>
              <Button
                variant="primary"
                size="sm"
                @click="selectQuestion(question)"
              >
                Ask
              </Button>
            </div>
          </div>
        </Card>
      </div>

      <!-- Status Messages -->
      <div class="text-center">
        <div v-if="hasSubmittedQuestion && !isHotSeatPlayer" class="text-green-600 font-medium">
          ✅ Question submitted! Watch {{ hotSeatPlayer?.name }} answer.
        </div>
        
        <div v-if="isHotSeatPlayer" class="text-orange-600 font-medium">
          🔥 You're in the hot seat! Answer as many questions as you can.
        </div>
        
        <div v-if="gameStore.timerExpired" class="text-gray-600 font-medium">
          ⏰ Time's up! Great job everyone.
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else class="py-12">
      <LoadingSpinner size="lg" text="Setting up hot seat..." />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useGameStore } from '@/stores/game'
import { useRoomStore } from '@/stores/room'
import { useAuthStore } from '@/stores/auth'
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
const authStore = useAuthStore()
const toast = useToast()

const questionText = ref('')
const submitting = ref(false)
const hasSubmittedQuestion = ref(false)
const submittedQuestions = ref([])
const currentQuestion = ref(null)

const hotSeatPlayer = computed(() => {
  // This would be determined by the game state
  return {
    id: 1,
    name: 'Hot Seat Player' // Replace with actual player data
  }
})

const isHotSeatPlayer = computed(() => {
  return authStore.user?.id === hotSeatPlayer.value?.id
})

const isHost = computed(() => {
  return authStore.user?.id === roomStore.currentRoom?.host_id
})

const submitQuestion = async () => {
  if (!questionText.value.trim()) {
    toast.warning('Please enter a question')
    return
  }
  
  submitting.value = true
  
  try {
    await emit('action', 'submit_question', {
      question: questionText.value.trim()
    })
    
    hasSubmittedQuestion.value = true
    toast.success('Question submitted!', 'Your question has been added to the queue')
    questionText.value = ''
  } catch (error) {
    console.error('Failed to submit question:', error)
    toast.error('Failed to submit', 'Please try again')
  } finally {
    submitting.value = false
  }
}

const selectQuestion = async (question) => {
  currentQuestion.value = question
  // Remove from queue
  const index = submittedQuestions.value.indexOf(question)
  if (index > -1) {
    submittedQuestions.value.splice(index, 1)
  }
}
</script>