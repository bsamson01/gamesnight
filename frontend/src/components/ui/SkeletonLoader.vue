<template>
  <div :class="containerClasses">
    <div v-if="type === 'card'" class="space-y-4">
      <div class="h-4 bg-gray-200 rounded animate-pulse w-3/4"></div>
      <div class="h-4 bg-gray-200 rounded animate-pulse w-1/2"></div>
      <div class="h-4 bg-gray-200 rounded animate-pulse w-5/6"></div>
    </div>
    
    <div v-else-if="type === 'avatar'" class="flex items-center space-x-4">
      <div class="h-10 w-10 bg-gray-200 rounded-full animate-pulse"></div>
      <div class="space-y-2">
        <div class="h-4 bg-gray-200 rounded animate-pulse w-24"></div>
        <div class="h-3 bg-gray-200 rounded animate-pulse w-16"></div>
      </div>
    </div>
    
    <div v-else-if="type === 'list'" class="space-y-3">
      <div v-for="i in count" :key="i" class="flex items-center space-x-3">
        <div class="h-8 w-8 bg-gray-200 rounded animate-pulse"></div>
        <div class="space-y-2 flex-1">
          <div class="h-4 bg-gray-200 rounded animate-pulse w-3/4"></div>
          <div class="h-3 bg-gray-200 rounded animate-pulse w-1/2"></div>
        </div>
      </div>
    </div>
    
    <div v-else-if="type === 'text'" class="space-y-2">
      <div v-for="i in count" :key="i" :class="textClasses"></div>
    </div>
    
    <div v-else :class="skeletonClasses"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'card', 'avatar', 'list', 'text'].includes(value)
  },
  width: {
    type: String,
    default: 'w-full'
  },
  height: {
    type: String,
    default: 'h-4'
  },
  count: {
    type: Number,
    default: 3
  },
  rounded: {
    type: String,
    default: 'rounded',
    validator: (value) => ['rounded', 'rounded-full', 'rounded-lg', 'rounded-none'].includes(value)
  }
})

const containerClasses = computed(() => {
  return 'animate-pulse'
})

const skeletonClasses = computed(() => {
  return `bg-gray-200 ${props.width} ${props.height} ${props.rounded}`
})

const textClasses = computed(() => {
  const widths = ['w-full', 'w-3/4', 'w-1/2', 'w-5/6', 'w-2/3']
  const randomWidth = widths[Math.floor(Math.random() * widths.length)]
  return `h-4 bg-gray-200 rounded ${randomWidth}`
})
</script>