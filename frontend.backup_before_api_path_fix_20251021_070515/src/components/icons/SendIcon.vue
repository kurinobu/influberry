<template>
  <svg 
    :width="size" 
    :height="size" 
    viewBox="0 0 24 24" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
  >
    <path 
      d="M3 20L21 12L3 4V11L16 12L3 13V20Z" 
      :fill="color"
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
    default: '#3b82f6'
  }
})
</script>