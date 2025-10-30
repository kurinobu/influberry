<template>
  <div class="progress-bar">
    <div class="flex justify-between items-center mb-2">
      <span class="text-sm font-medium text-gray-700 flex items-center">
        <component :is="iconComponent" class="w-4 h-4 mr-2" />
        {{ label }}
      </span>
      <span class="text-sm font-semibold text-gray-900">
        {{ formatNumber(current) }} / {{ formatNumber(target) }} {{ unit }}
      </span>
    </div>
    
    <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
      <div 
        class="h-3 rounded-full transition-all duration-300"
        :class="progressColor"
        :style="{ width: `${percentage}%` }"
      ></div>
    </div>
    
    <div class="flex justify-between items-center mt-1">
      <span class="text-xs text-gray-500">
        {{ motivationMessage }}
      </span>
      <span class="text-xs font-bold" :class="percentageColor">
        {{ percentage }}%
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: {
    type: String,
    required: true
  },
  current: {
    type: Number,
    default: 0
  },
  target: {
    type: Number,
    default: 0
  },
  unit: {
    type: String,
    default: '件'
  },
  icon: {
    type: String,
    default: 'default'
  }
})

const percentage = computed(() => {
  if (!props.target) return 0
  return Math.min(Math.round((props.current / props.target) * 100), 100)
})

const progressColor = computed(() => {
  const p = percentage.value
  if (p >= 100) return 'bg-gradient-to-r from-green-400 to-green-600'
  if (p >= 80) return 'bg-gradient-to-r from-blue-400 to-blue-600'
  if (p >= 50) return 'bg-gradient-to-r from-yellow-400 to-yellow-600'
  return 'bg-gradient-to-r from-pink-400 to-pink-600'
})

const percentageColor = computed(() => {
  const p = percentage.value
  if (p >= 100) return 'text-green-600'
  if (p >= 80) return 'text-blue-600'
  if (p >= 50) return 'text-yellow-600'
  return 'text-pink-600'
})

const motivationMessage = computed(() => {
  const p = percentage.value
  if (p >= 100) return '🎉 目標達成！'
  if (p >= 80) return '💪 あと少し！'
  if (p >= 50) return '📈 順調です'
  return '🚀 がんばろう'
})

const formatNumber = (num) => {
  if (props.unit === '円') {
    return new Intl.NumberFormat('ja-JP').format(num)
  }
  return num
}

const iconComponent = computed(() => {
  const icons = {
    box: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
    check: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
    currency: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1',
    default: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
  }
  
  return {
    template: `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${icons[props.icon] || icons.default}" />
    </svg>`
  }
})
</script>

<style scoped>
.progress-bar {
  /* スムーズなアニメーション */
  transition: all 0.3s ease-in-out;
}

/* プログレスバーのアニメーション */
.progress-bar .h-3 {
  transition: width 0.5s ease-in-out;
}
</style>
