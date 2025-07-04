<template>
  <div :class="containerClasses">
    <div class="text-center">
      <div v-if="icon" class="text-6xl mb-4">{{ icon }}</div>
      <svg
        v-else
        class="mx-auto h-12 w-12 text-gray-400"
        stroke="currentColor"
        fill="none"
        viewBox="0 0 48 48"
      >
        <path
          d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">{{ title }}</h3>
      <p class="mt-1 text-sm text-gray-500">{{ description }}</p>
      <div v-if="$slots.action" class="mt-6">
        <slot name="action" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
})

const containerClasses = computed(() => {
  const base = 'flex items-center justify-center'
  
  const sizes = {
    sm: 'py-8',
    md: 'py-12',
    lg: 'py-16'
  }
  
  return `${base} ${sizes[props.size]}`
})
</script>