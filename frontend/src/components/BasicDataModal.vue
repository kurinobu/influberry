<script setup>
// モーダル表示制御
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

// モーダルを閉じる
const closeModal = () => {
  emit('close')
}

// 外部ページを開く
const openPage = (path) => {
  window.open(path, '_blank')
  closeModal()
}

// オーバーレイクリックでモーダルを閉じる
const handleOverlayClick = (event) => {
  if (event.target === event.currentTarget) {
    closeModal()
  }
}

// 基本データメニュー項目
const dataItems = [
  {
    icon: '🔒',
    name: 'プライバシーポリシー',
    description: '個人情報の取扱いについて',
    path: '/privacy'
  },
  {
    icon: '📋',
    name: 'ご利用規約',
    description: 'サービス利用条件',
    path: '/terms'
  },
  {
    icon: '🏢',
    name: '運営会社情報',
    description: 'Air Edison（エアエジソン）について',
    path: '/company'
  },
  {
    icon: '⚖️',
    name: '特定商取引法に基づく表記',
    description: '法的事項・返品条件等',
    path: '/tokusho'
  }
]
</script>

<template>
  <!-- モーダルオーバーレイ -->
  <div
    v-if="show"
    class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-[60]"
    @click="handleOverlayClick"
  >
    <!-- モーダルコンテンツ -->
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div
        class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
        @click.stop
      >
        <!-- モーダルヘッダー -->
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg leading-6 font-medium text-gray-900 flex items-center">
              <span class="text-2xl mr-2">📋</span>
              基本データ
            </h3>
            <button
              @click="closeModal"
              class="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <!-- データ項目一覧 -->
          <div class="space-y-3">
            <div
              v-for="item in dataItems"
              :key="item.path"
              class="border border-gray-200 rounded-lg hover:border-pink-300 hover:bg-pink-50 transition-colors cursor-pointer"
              @click="openPage(item.path)"
            >
              <div class="p-4">
                <div class="flex items-center">
                  <span class="text-2xl mr-3">{{ item.icon }}</span>
                  <div class="flex-1">
                    <h4 class="text-sm font-medium text-gray-900">{{ item.name }}</h4>
                    <p class="text-xs text-gray-500 mt-1">{{ item.description }}</p>
                  </div>
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- モーダルフッター -->
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            @click="closeModal"
            class="w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm transition-colors"
          >
            閉じる
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Z世代向けカジュアルなホバーエフェクト */
.hover\:border-pink-300:hover {
  border-color: #f9a8d4;
}

.hover\:bg-pink-50:hover {
  background-color: #fdf2f8;
}

/* スムーズなトランジション */
.transition-colors {
  transition-property: color, background-color, border-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* モーダルアニメーション */
.transform {
  transform: translateY(0);
}

/* フォーカス時のアウトライン */
.focus\:ring-2:focus {
  box-shadow: 0 0 0 2px rgba(236, 72, 153, 0.5);
}

.focus\:ring-offset-2:focus {
  box-shadow: 0 0 0 2px #fff, 0 0 0 4px rgba(236, 72, 153, 0.5);
}
</style>