<template>
  <svg 
    :width="size" 
    :height="size" 
    viewBox="0 0 24 24" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
  >
    <path 
      d="M12 2L2 20H22L12 2Z" 
      :fill="color"
      fill-opacity="0.2"
    />
    <path 
      d="M12 2L2 20H22L12 2Z" 
      :stroke="color"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
    <path 
      d="M12 9V13" 
      :stroke="color"
      stroke-width="2"
      stroke-linecap="round"
    />
    <circle 
      cx="12" 
      cy="17" 
      r="1" 
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
    default: '#ef4444'
  }
})
</script>