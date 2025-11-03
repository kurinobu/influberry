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
    <path d="M9 21h6"></path>
    <path d="M12 3a6 6 0 0 0 0 12c.83 0 1.64-.17 2.38-.47a5 5 0 0 1-1.56 1.82 3.5 3.5 0 1 1-5.64 0 5 5 0 0 1-1.56-1.82c.74.3 1.55.47 2.38.47z"></path>
    <path d="M9 18v.01"></path>
    <path d="M15 18v.01"></path>
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
    default: '#fbbf24'
  }
})
</script>

