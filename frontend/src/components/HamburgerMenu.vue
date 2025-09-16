<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// メニュー開閉状態
const isOpen = ref(false)

// メニュー開閉
const toggleMenu = () => {
  isOpen.value = !isOpen.value
}

// メニューを閉じる
const closeMenu = () => {
  isOpen.value = false
}

// ナビゲーション
const navigateTo = (path) => {
  router.push(path)
  closeMenu()
}

// ログアウト処理
const handleLogout = async () => {
  const result = await authStore.logout()
  if (result.success) {
    router.push('/')
  }
  closeMenu()
}

// プラン情報（仮実装 - 将来的にストアから取得）
const planInfo = computed(() => {
  const planType = authStore.user?.plan_type || 'free'
  if (planType === 'free') {
    return {
      name: 'Freeプラン',
      invoiceLimit: '請求書(月1/1枚)',
      canUpgrade: true
    }
  } else {
    return {
      name: 'Proプラン',
      invoiceLimit: '請求書(無制限)',
      canUpgrade: false
    }
  }
})

// メニュー項目定義
const menuItems = [
  {
    icon: '📊',
    name: 'ダッシュボード',
    path: '/dashboard',
    available: true
  },
  {
    icon: '🏢',
    name: 'スポンサー案件管理',
    path: '/apps/projects',
    available: true
  },
  {
    icon: '📋',
    name: '請求書管理',
    path: '/apps/invoices',
    available: true
  },
  {
    icon: '💡',
    name: 'ブランド提案文',
    path: '/apps/brand-generator',
    available: false,
    isPro: true,
    comingSoon: false
  },
  {
    icon: '📝',
    name: 'Todoリスト',
    path: '/apps/todo',
    available: false,
    isPro: false,
    comingSoon: true
  }
]

const settingsItems = [
  {
    icon: '⚙️',
    name: '設定',
    action: 'settings'
  },
  {
    icon: '💎',
    name: 'プラン管理',
    action: 'plan'
  },
  {
    icon: '🚪',
    name: 'ログアウト',
    action: 'logout'
  }
]

// アクション処理
const handleAction = (action) => {
  switch (action) {
    case 'settings':
      // 設定モーダル表示（親コンポーネントに通知）
      emit('openSettings')
      closeMenu()
      break
    case 'plan':
      // プラン管理ページへ（将来実装）
      console.log('プラン管理（未実装）')
      closeMenu()
      break
    case 'logout':
      handleLogout()
      break
  }
}

// 親コンポーネントへのイベント通知
const emit = defineEmits(['openSettings'])

// 現在のページかどうかの判定
const isCurrentPage = (path) => {
  return route.path === path
}

// オーバーレイクリックでメニューを閉じる
const handleOverlayClick = (event) => {
  if (event.target === event.currentTarget) {
    closeMenu()
  }
}
</script>

<template>
  <div class="relative">
    <!-- ハンバーガーボタン -->
    <button
      @click="toggleMenu"
      class="inline-flex items-center justify-center p-2 rounded-md text-gray-800 hover:text-gray-600 hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white transition-colors"
      aria-label="メニューを開く"
    >
      <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>

    <!-- メニューオーバーレイ -->
    <div
      v-if="isOpen"
      class="fixed inset-0 bg-black bg-opacity-50 menu-overlay"
      style="background-color: rgba(0, 0, 0, 0.5) !important; z-index: 9998 !important;"
      @click="handleOverlayClick"
    >
    </div>

    <!-- メニューパネルを独立配置 -->
    <div 
      v-if="isOpen"
      class="fixed top-0 right-0 h-full w-80 bg-white shadow-xl transform transition-transform duration-300 ease-in-out menu-panel" 
      style="background-color: #ffffff !important; background-image: none !important; z-index: 9999 !important;"
    >
        <!-- メニューヘッダー -->
        <div class="flex items-center justify-between p-4 border-b border-gray-200">
          <div class="flex items-center">
            <h2 class="text-lg font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-600 font-poppins">
              🍓 InfluBerry
            </h2>
          </div>
          <button
            @click="closeMenu"
            class="p-2 rounded-md text-gray-500 hover:text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-500"
            aria-label="メニューを閉じる"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- ユーザー情報 -->
        <div class="p-4 border-b border-gray-200 bg-gray-50">
          <div class="text-sm text-gray-600">こんにちは</div>
          <div class="text-lg font-semibold text-gray-900">{{ authStore.userName }}さん</div>
        </div>

        <!-- メニュー項目 -->
        <div class="flex-1 py-4 overflow-y-auto">
          <!-- ナビゲーションメニュー -->
          <nav class="px-4 space-y-2">
            <div v-for="item in menuItems" :key="item.path" class="relative">
              <button
                v-if="item.available"
                @click="navigateTo(item.path)"
                :class="[
                  'w-full flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors',
                  isCurrentPage(item.path)
                    ? 'bg-pink-100 text-pink-700 border-l-4 border-pink-500'
                    : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
                ]"
              >
                <span class="text-lg mr-3">{{ item.icon }}</span>
                {{ item.name }}
              </button>
              
              <!-- 利用不可メニュー -->
              <div
                v-else
                :class="[
                  'w-full flex items-center px-3 py-2 text-sm font-medium rounded-md',
                  'text-gray-400 cursor-not-allowed relative'
                ]"
              >
                <span class="text-lg mr-3 grayscale">{{ item.icon }}</span>
                {{ item.name }}
                <span v-if="item.isPro" class="ml-auto text-xs bg-purple-100 text-purple-600 px-2 py-1 rounded">
                  🔒 Pro限定
                </span>
                <span v-else-if="item.comingSoon" class="ml-auto text-xs bg-gray-100 text-gray-500 px-2 py-1 rounded">
                  準備中
                </span>
              </div>
            </div>
          </nav>

          <!-- 区切り線 -->
          <div class="my-4 px-4">
            <div class="border-t border-gray-200"></div>
          </div>

          <!-- 設定・管理メニュー -->
          <nav class="px-4 space-y-2">
            <div v-for="item in settingsItems" :key="item.action">
              <button
                @click="handleAction(item.action)"
                class="w-full flex items-center px-3 py-2 text-sm font-medium text-gray-700 rounded-md hover:bg-gray-100 hover:text-gray-900 transition-colors"
              >
                <span class="text-lg mr-3">{{ item.icon }}</span>
                {{ item.name }}
              </button>
            </div>
          </nav>
        </div>

        <!-- プラン情報フッター -->
        <div class="border-t border-gray-200 p-4 bg-gray-50">
          <div class="text-xs text-gray-600 mb-2">
            {{ planInfo.name }} {{ planInfo.invoiceLimit }}
          </div>
          <button
            v-if="planInfo.canUpgrade"
            @click="handleAction('plan')"
            class="w-full py-2 px-4 bg-gradient-to-r from-pink-500 to-purple-600 text-white text-sm font-medium rounded-md hover:from-pink-600 hover:to-purple-700 transition-colors"
          >
            💎 アップグレード
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* メニューパネル背景色強制指定 - Tailwind v4対応 */
.menu-panel {
  background-color: #ffffff !important;
  background-image: none !important;
  background: solid #ffffff !important;
  backdrop-filter: none !important;
}

/* オーバーレイ背景確実指定 - Tailwind v4対応 */
.menu-overlay {
  background-color: rgba(0, 0, 0, 0.5) !important;
  background: rgba(0, 0, 0, 0.5) !important;
}

/* オーバーレイ背景確実指定 */
.menu-overlay {
  background-color: rgba(0, 0, 0, 0.5) !important;
}

/* スムーズなアニメーション */
.transition-transform {
  transition-property: transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

/* メニューパネルのスライドイン */
.transform {
  transform: translateX(0);
}

/* グレースケールエフェクト */
.grayscale {
  filter: grayscale(100%);
}

/* モバイル最適化 */
@media (max-width: 640px) {
  .w-80 {
    width: 100%;
    max-width: 320px;
  }
}
</style>