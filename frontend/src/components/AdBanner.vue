<template>
  <div class="fixed bottom-0 left-0 right-0 bg-gray-100 border-t border-gray-300 p-4 z-40">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <div class="flex-1 text-center">
        <!-- Ad placeholder - Replace with actual ad code -->
        <div class="bg-gray-200 h-20 flex items-center justify-center text-gray-500">
          <span>Advertisement Space</span>
        </div>
      </div>
      <router-link 
        to="/subscription"
        class="ml-4 text-sm text-indigo-600 hover:text-indigo-800 whitespace-nowrap"
      >
        Remove ads →
      </router-link>
    </div>
  </div>
</template>

<script setup>
// In production, integrate with Google AdSense or similar
// This is just a placeholder component
</script>