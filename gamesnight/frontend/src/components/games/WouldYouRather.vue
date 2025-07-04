<template>
  <div class="text-center">
    <h2 class="text-3xl font-bold mb-8">Would You Rather...</h2>
    
    <div v-if="prompt" class="space-y-6">
      <!-- Options -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <button
          @click="vote('a')"
          :disabled="hasVoted || gameStore.timerExpired"
          class="p-6 rounded-lg border-2 transition-all"
          :class="{
            'border-blue-500 bg-blue-50': myVote === 'a',
            'border-gray-300 hover:border-gray-400': !hasVoted && myVote !== 'a',
            'border-gray-200 cursor-not-allowed': hasVoted || gameStore.timerExpired
          }"
        >
          <div class="text-lg font-medium mb-2">Option A</div>
          <div class="text-gray-700">{{ prompt.option_a }}</div>
          <div v-if="showResults" class="mt-4">
            <div class="text-2xl font-bold text-blue-600">{{ votePercentage('a') }}%</div>
            <div class="text-sm text-gray-600">{{ voteCount('a') }} votes</div>
          </div>
        </button>
        
        <button
          @click="vote('b')"
          :disabled="hasVoted || gameStore.timerExpired"
          class="p-6 rounded-lg border-2 transition-all"
          :class="{
            'border-purple-500 bg-purple-50': myVote === 'b',
            'border-gray-300 hover:border-gray-400': !hasVoted && myVote !== 'b',
            'border-gray-200 cursor-not-allowed': hasVoted || gameStore.timerExpired
          }"
        >
          <div class="text-lg font-medium mb-2">Option B</div>
          <div class="text-gray-700">{{ prompt.option_b }}</div>
          <div v-if="showResults" class="mt-4">
            <div class="text-2xl font-bold text-purple-600">{{ votePercentage('b') }}%</div>
            <div class="text-sm text-gray-600">{{ voteCount('b') }} votes</div>
          </div>
        </button>
      </div>
      
      <!-- Status -->
      <div v-if="hasVoted && !showResults" class="text-gray-600">
        Waiting for other players to vote...
      </div>
      
      <div v-if="showResults" class="mt-8">
        <button 
          v-if="roomStore.isHost"
          @click="nextRound"
          class="bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700"
        >
          Next Question
        </button>
      </div>
    </div>
    
    <div v-else class="py-12">
      <p class="text-gray-600">Waiting for next question...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useGameStore } from '@/stores/game'
import { useRoomStore } from '@/stores/room'

const props = defineProps({
  prompt: Object
})

const emit = defineEmits(['action'])

const gameStore = useGameStore()
const roomStore = useRoomStore()

const myVote = ref(null)
const hasVoted = ref(false)

const votes = computed(() => gameStore.gameState.votes || { a: 0, b: 0 })
const totalVotes = computed(() => votes.value.a + votes.value.b)

const showResults = computed(() => {
  return gameStore.timerExpired || totalVotes.value === roomStore.approvedParticipants.length
})

const voteCount = (option) => {
  return votes.value[option] || 0
}

const votePercentage = (option) => {
  if (totalVotes.value === 0) return 0
  return Math.round((voteCount(option) / totalVotes.value) * 100)
}

const vote = (option) => {
  if (hasVoted.value || gameStore.timerExpired) return
  
  myVote.value = option
  hasVoted.value = true
  
  emit('action', 'vote', {
    choice: option,
    prompt_id: props.prompt.id
  })
}

const nextRound = () => {
  gameStore.getNextPrompt()
}

// Reset when new prompt arrives
watch(() => props.prompt?.id, () => {
  myVote.value = null
  hasVoted.value = false
})
</script>