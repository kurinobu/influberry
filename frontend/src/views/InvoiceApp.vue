<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useInvoicesStore } from '../stores/invoices.js'
import InvoiceList from '../components/InvoiceList.vue'
import HamburgerMenu from '../components/HamburgerMenu.vue'
import UserSettings from '../components/UserSettings.vue'

const router = useRouter()
const authStore = useAuthStore()
const invoicesStore = useInvoicesStore()

// アプリ初期化
onMounted(async () => {
  // 未認証の場合は認証ページへリダイレクト
  await authStore.checkAuthStatus()
  if (!authStore.isLoggedIn) {
    router.push('/')
    return
  }
  
  // 請求書データ取得
  await invoicesStore.fetchInvoices()
})

// 設定モーダル表示状態
const showSettings = ref(false)

// 設定モーダル切り替え
const toggleSettings = () => {
  showSettings.value = !showSettings.value
}

// ダッシュボードに戻る
const backToDashboard = () => {
  router.push('/dashboard')
}

</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- ヘッダー -->
    <header class="shadow-lg border-b-2" style="background: linear-gradient(to right, var(--influberry-pink-light), var(--influberry-lavender-light)); border-color: var(--influberry-pink);">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- InfluBerry ロゴ -->
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-600 font-poppins">
              🍓 InfluBerry
            </h1>
          </div>
          
          <!-- ハンバーガーメニュー -->
          <HamburgerMenu @openSettings="toggleSettings" />
        </div>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        
        <!-- アプリヘッダー -->
        <div class="mb-6">
          <div class="bg-white rounded-lg shadow-sm p-6">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-2xl font-bold text-gray-900">請求書管理</h2>
                <p class="mt-1 text-sm text-gray-600">
                  プロジェクトから自動請求書生成・編集・管理を行います
                </p>
              </div>
              <div class="flex items-center space-x-4">
                <div class="text-center">
                  <div class="text-2xl font-bold text-purple-600">{{ invoicesStore.invoices?.length || 0 }}</div>
                  <div class="text-xs text-gray-500">総請求書数</div>
                </div>
                <div class="text-center">
                  <div class="text-2xl font-bold text-green-600">
                    {{ invoicesStore.invoices?.filter(i => i.status === 'paid').length || 0 }}
                  </div>
                  <div class="text-xs text-gray-500">支払済</div>
                </div>
                <div class="text-center">
                  <div class="text-2xl font-bold text-yellow-600">
                    {{ invoicesStore.invoices?.filter(i => i.status === 'pending').length || 0 }}
                  </div>
                  <div class="text-xs text-gray-500">未払</div>
                </div>
                <div class="text-center">
                  <div class="text-2xl font-bold text-pink-600">
                    ¥{{ invoicesStore.invoices?.reduce((sum, i) => sum + (i.total_amount || 0), 0).toLocaleString() || 0 }}
                  </div>
                  <div class="text-xs text-gray-500">総金額</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- InvoiceList コンポーネント -->
        <InvoiceList />

      </div>
    </main>
    <!-- ユーザー設定モーダル -->
    <UserSettings v-if="showSettings" @close="showSettings = false" />
  </div>
</template>

<style scoped>
/* InfluBerry カスタムスタイル */
header {
  backdrop-filter: blur(10px);
}

/* ホバーエフェクト */
.hover\:text-purple-200:hover {
  color: rgb(221 214 254);
}

/* スムーズなトランジション */
.transition-colors {
  transition: color 0.2s ease;
}

/* モバイルファースト最適化 */
@media (max-width: 640px) {
  .max-w-7xl {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .flex.items-center.space-x-4 {
    flex-direction: column;
    align-items: flex-end;
    gap: 0.5rem;
  }
  
  .flex.items-center.justify-between {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .text-xl {
    font-size: 1rem;
    line-height: 1.5rem;
  }
  
  .text-2xl {
    font-size: 1.25rem;
    line-height: 1.75rem;
  }
  
  .flex.items-center.space-x-4:last-child {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    display: grid;
    gap: 0.5rem;
  }
}
</style>