<template>
  <div class="fixed inset-0 pointer-events-none z-50">
    <Toast
      v-for="toast in toasts"
      :key="toast.id"
      :show="toast.show"
      :type="toast.type"
      :title="toast.title"
      :message="toast.message"
      :position="toast.position"
      :duration="0"
      @close="removeToast(toast.id)"
    />
  </div>
</template>

<script setup>
import { useToast } from '@/composables/useToast'
import Toast from '@/components/ui/Toast.vue'

const { toasts, removeToast } = useToast()
</script>