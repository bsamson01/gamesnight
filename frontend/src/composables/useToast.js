import { ref, reactive } from 'vue'

const toasts = ref([])

export function useToast() {
  const showToast = (options) => {
    const id = Math.random().toString(36).substr(2, 9)
    const toast = reactive({
      id,
      show: true,
      type: options.type || 'info',
      title: options.title,
      message: options.message || '',
      duration: options.duration || 5000,
      position: options.position || 'top-right'
    })

    toasts.value.push(toast)

    // Auto-remove toast
    if (toast.duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, toast.duration)
    }

    return id
  }

  const removeToast = (id) => {
    const index = toasts.value.findIndex(toast => toast.id === id)
    if (index > -1) {
      toasts.value[index].show = false
      // Remove from array after animation
      setTimeout(() => {
        toasts.value.splice(index, 1)
      }, 300)
    }
  }

  const success = (title, message, options = {}) => {
    return showToast({ ...options, type: 'success', title, message })
  }

  const error = (title, message, options = {}) => {
    return showToast({ ...options, type: 'error', title, message })
  }

  const warning = (title, message, options = {}) => {
    return showToast({ ...options, type: 'warning', title, message })
  }

  const info = (title, message, options = {}) => {
    return showToast({ ...options, type: 'info', title, message })
  }

  const clear = () => {
    toasts.value.forEach(toast => {
      toast.show = false
    })
    setTimeout(() => {
      toasts.value.length = 0
    }, 300)
  }

  return {
    toasts,
    showToast,
    removeToast,
    success,
    error,
    warning,
    info,
    clear
  }
}