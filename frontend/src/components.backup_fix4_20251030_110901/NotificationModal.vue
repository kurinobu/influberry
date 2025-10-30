<script setup>
import { ref, computed } from 'vue'
import CheckIcon from './icons/CheckIcon.vue'
import AlertIcon from './icons/AlertIcon.vue'
import CloseIcon from './icons/CloseIcon.vue'

// Props
const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'success', // 'success' or 'error'
    validator: (value) => ['success', 'error'].includes(value)
  },
  title: {
    type: String,
    default: ''
  },
  message: {
    type: String,
    default: ''
  },
  actionText: {
    type: String,
    default: ''
  },
  actionUrl: {
    type: String,
    default: ''
  }
})

// Emits
const emit = defineEmits(['close', 'action'])

// Computed
const iconComponent = computed(() => {
  return props.type === 'success' ? CheckIcon : AlertIcon
})

const iconColor = computed(() => {
  return props.type === 'success' ? '#10b981' : '#ef4444'
})

const bgGradient = computed(() => {
  return props.type === 'success' 
    ? 'from-green-500 to-emerald-600' 
    : 'from-red-500 to-rose-600'
})

// Methods
const closeModal = () => {
  emit('close')
}

const handleAction = () => {
  if (props.actionUrl) {
    window.open(props.actionUrl, '_blank')
  }
  emit('action')
  closeModal()
}

// オーバーレイクリックでモーダルを閉じる
const handleOverlayClick = (event) => {
  if (event.target === event.currentTarget) {
    closeModal()
  }
}
</script>

<template>
  <!-- モーダルオーバーレイ -->
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="isVisible"
        class="fixed inset-0 z-[9999] flex items-center justify-center p-4"
        style="background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(4px);"
        @click="handleOverlayClick"
      >
        <!-- モーダルコンテンツ -->
        <div
          class="relative w-full max-w-md rounded-2xl shadow-2xl overflow-hidden bg-white"
        >
          <!-- ヘッダー -->
          <div 
            class="px-6 py-4"
            :class="`bg-gradient-to-r ${bgGradient}`"
          >
            <div class="flex items-center justify-center">
              <component 
                :is="iconComponent" 
                :size="32" 
                :color="'#ffffff'"
                class="mr-3"
              />
              <h3 class="text-lg font-bold text-white">
                {{ title }}
              </h3>
            </div>
          </div>

          <!-- コンテンツ -->
          <div class="p-6">
            <p class="text-gray-700 text-center mb-6">
              {{ message }}
            </p>

            <!-- アクションボタン -->
            <div class="flex justify-center space-x-3">
              <button
                @click="closeModal"
                class="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors flex items-center gap-2"
              >
                <CloseIcon :size="16" color="#ffffff" />
                閉じる
              </button>
              
              <button
                v-if="actionText"
                @click="handleAction"
                class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
              >
                <CheckIcon :size="16" color="#ffffff" v-if="type === 'success'" />
                {{ actionText }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
/* フェードアニメーション */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ホバーエフェクト強化 */
button:hover {
  transform: translateY(-1px);
}

button:active {
  transform: translateY(0);
}
</style>
