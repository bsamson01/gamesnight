<template>
  <div :class="containerClasses">
    <div :class="spinnerClasses"></div>
    <p v-if="text" :class="textClasses">{{ text }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  text: {
    type: String,
    default: ''
  },
  centered: {
    type: Boolean,
    default: false
  },
  color: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'white', 'gray'].includes(value)
  }
})

const containerClasses = computed(() => {
  const base = 'flex flex-col items-center justify-center'
  const center = props.centered ? 'min-h-[200px]' : ''
  return `${base} ${center}`
})

const spinnerClasses = computed(() => {
  const base = 'animate-spin rounded-full border-2 border-t-transparent'
  
  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
    xl: 'h-16 w-16'
  }
  
  const colors = {
    primary: 'border-electric-blue',
    white: 'border-white',
    gray: 'border-gray-400'
  }
  
  return `${base} ${sizes[props.size]} ${colors[props.color]}`
})

const textClasses = computed(() => {
  const base = 'mt-3 text-sm font-medium'
  
  const colors = {
    primary: 'text-gray-600',
    white: 'text-white',
    gray: 'text-gray-500'
  }
  
  return `${base} ${colors[props.color]}`
})
</script>