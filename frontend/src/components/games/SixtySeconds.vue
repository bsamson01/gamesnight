<template>
  <div class="text-center">
    <h2 class="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8">60 Seconds Challenge</h2>
    
    <div v-if="prompt" class="space-y-6">
      <!-- Category Display -->
      <Card variant="elevated" class="max-w-2xl mx-auto">
        <div class="text-center p-4 sm:p-6">
          <div class="text-4xl sm:text-6xl mb-4">⏱️</div>
          <h3 class="text-lg sm:text-xl font-semibold mb-2 text-gray-800">
            List as many as you can:
          </h3>
          <p class="text-xl sm:text-2xl font-bold text-electric-blue">
            {{ prompt.category }}
          </p>
        </div>
      </Card>

      <!-- Input Area -->
      <div v-if="!gameStore.timerExpired && !hasSubmitted" class="max-w-md mx-auto">
        <Card variant="default">
          <div class="space-y-4">
            <div class="flex gap-2">
              <input
                v-model="currentAnswer"
                @keyup.enter="addAnswer"
                type="text"
                placeholder="Type your answer..."
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-electric-blue focus:border-electric-blue"
                :disabled="gameStore.timerExpired"
              />
              <Button
                variant="primary"
                @click="addAnswer"
                :disabled="!currentAnswer.trim() || gameStore.timerExpired"
              >
                Add
              </Button>
            </div>
            
            <div class="text-sm text-gray-600">
              {{ answers.length }} answers • {{ 60 - answers.length }} remaining
            </div>
          </div>
        </Card>
      </div>

      <!-- Answers List -->
      <div v-if="answers.length > 0" class="max-w-2xl mx-auto">
        <Card variant="default">
          <template #header>
            <h3 class="text-lg font-semibold">Your Answers ({{ answers.length }})</h3>
          </template>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-64 overflow-y-auto">
            <div
              v-for="(answer, index) in answers"
              :key="index"
              class="flex items-center justify-between p-2 bg-gray-50 rounded text-sm"
            >
              <span>{{ answer }}</span>
              <button
                v-if="!gameStore.timerExpired && !hasSubmitted"
                @click="removeAnswer(index)"
                class="text-red-500 hover:text-red-700 ml-2"
              >
                ×
              </button>
            </div>
          </div>
        </Card>
      </div>

      <!-- Submit Button -->
      <div v-if="!hasSubmitted && answers.length > 0" class="max-w-md mx-auto">
        <Button
          variant="success"
          size="lg"
          full-width
          @click="submitAnswers"
          :loading="submitting"
        >
          Submit Answers ({{ answers.length }})
        </Button>
      </div>

      <!-- Results -->
      <div v-if="hasSubmitted || gameStore.timerExpired" class="space-y-4">
        <Card variant="elevated" class="max-w-md mx-auto">
          <div class="text-center p-6">
            <div class="text-4xl mb-4">🎯</div>
            <h3 class="text-xl font-semibold mb-2">Your Score</h3>
            <div class="text-3xl font-bold text-electric-blue">
              {{ answers.length }}
            </div>
            <p class="text-gray-600 mt-2">
              {{ answers.length === 1 ? 'answer' : 'answers' }} submitted
            </p>
          </div>
        </Card>

        <div class="text-center">
          <p class="text-gray-600">Waiting for other players to finish...</p>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else class="py-12">
      <LoadingSpinner size="lg" text="Loading challenge..." />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useGameStore } from '@/stores/game'
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
const toast = useToast()

const currentAnswer = ref('')
const answers = ref([])
const submitting = ref(false)
const hasSubmitted = ref(false)

const addAnswer = () => {
  const answer = currentAnswer.value.trim()
  if (!answer) return
  
  // Check for duplicates (case-insensitive)
  const lowerAnswer = answer.toLowerCase()
  if (answers.value.some(a => a.toLowerCase() === lowerAnswer)) {
    toast.warning('Duplicate answer', 'You already added this answer')
    return
  }
  
  answers.value.push(answer)
  currentAnswer.value = ''
  
  // Auto-submit if timer expired
  if (gameStore.timerExpired && !hasSubmitted.value) {
    submitAnswers()
  }
}

const removeAnswer = (index) => {
  answers.value.splice(index, 1)
}

const submitAnswers = async () => {
  if (answers.value.length === 0) {
    toast.warning('No answers', 'Please add at least one answer')
    return
  }
  
  submitting.value = true
  
  try {
    await emit('action', 'submit_answers', {
      prompt_id: props.prompt.id,
      answers: answers.value
    })
    
    hasSubmitted.value = true
    toast.success('Answers submitted!', `You submitted ${answers.value.length} answers`)
  } catch (error) {
    console.error('Failed to submit answers:', error)
    toast.error('Failed to submit', 'Please try again')
  } finally {
    submitting.value = false
  }
}

// Auto-submit when timer expires
const unwatchTimer = gameStore.$watch(
  () => gameStore.timerExpired,
  (expired) => {
    if (expired && !hasSubmitted.value && answers.value.length > 0) {
      submitAnswers()
    }
  }
)
</script>