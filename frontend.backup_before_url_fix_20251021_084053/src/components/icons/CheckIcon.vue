<template>
  <svg 
    :width="size" 
    :height="size" 
    viewBox="0 0 24 24" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
  >
    <path 
      d="M9 12L11 14L15 10" 
      :stroke="color"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
    <circle 
      cx="12" 
      cy="12" 
      r="10" 
      :stroke="color"
      stroke-width="2"
    />
  </svg>
</template>

<script setup>
defineProps({
  size: {
    type: Number,
    default: 24
  },
  color: {
    type: String,
    default: '#10b981'
  }
})
</script>
