<template>
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    :width="size" 
    :height="size" 
    viewBox="0 0 24 24" 
    fill="none" 
    :stroke="color" 
    stroke-width="2" 
    stroke-linecap="round" 
    stroke-linejoin="round"
  >
    <line x1="12" y1="3" x2="12" y2="21"></line>
    <path d="M8 9l-4 4 4 4"></path>
    <path d="M16 9l4 4-4 4"></path>
  </svg>
</template>

<script setup>
defineProps({
  size: {
    type: [Number, String],
    default: 24
  },
  color: {
    type: String,
    default: '#6b7280'
  }
})
</script>