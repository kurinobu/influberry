<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useProjectsStore } from '../stores/projects.js'
import { useInvoicesStore } from '../stores/invoices.js'
import UserSettings from '../components/UserSettings.vue'

const router = useRouter()
const authStore = useAuthStore()
const projectsStore = useProjectsStore()
const invoicesStore = useInvoicesStore()

// 設定モーダル表示状態
const showSettings = ref(false)

// 統計データ計算
const stats = computed(() => {
  const invoices = invoicesStore.invoices || []
  
  return {
    totalProjects: projectsStore.totalProjectsCount,
    completedProjects: projectsStore.completedCount,
    pendingProjects: projectsStore.pendingProjectsCount,  // ← 統一修正
    totalInvoices: invoices.length,
    totalRevenue: projectsStore.projects
      .filter(p => p.status === 'completed')
      .reduce((sum, p) => sum + (p.amount || 0), 0)
  }
})

// アプリ初期化
onMounted(async () => {
  // 未認証の場合は認証ページへリダイレクト
  await authStore.checkAuthStatus()
  if (!authStore.isLoggedIn) {
    router.push('/')
    return
  }
  
  // データ取得
  await Promise.all([
    projectsStore.fetchProjects(),
    invoicesStore.fetchInvoices()
  ])
})

// ログアウト処理
const handleLogout = async () => {
  const result = await authStore.logout()
  if (result.success) {
    router.push('/')
  }
}

// プラグインアプリへの遷移
const navigateToApp = (appName) => {
  router.push(`/apps/${appName}`)
}

// 設定モーダル表示切り替え
const toggleSettings = () => {
  showSettings.value = !showSettings.value
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- ヘッダー -->
    <header class="shadow-lg border-b-2" style="background: linear-gradient(to right, var(--influberry-pink-light), var(--influberry-lavender-light)); border-color: var(--influberry-pink);">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <h1 class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-600 font-poppins">
              🍓 InfluBerry
            </h1>
          </div>
          
          <div class="flex items-center">
            <button
              @click="toggleSettings"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-purple-500 hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
            >
              ⚙️ 設定
            </button>
          </div>
        </div>
    </header>

<!-- ユーザー情報バー -->
    <div class="bg-white/10 backdrop-blur-sm border-b border-white/20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-3">
          <span class="text-sm text-white font-poppins">
            こんにちは、{{ authStore.userName }}さん ✨
          </span>
          <button
            @click="handleLogout"
            :disabled="authStore.isLoading"
            class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs leading-4 font-medium rounded-md text-white bg-red-500 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
          >
            {{ authStore.isLoading ? '処理中...' : 'ログアウト' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- メインコンテンツ -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        
        <!-- 統計サマリー -->
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">📊 概要</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
            <div class="bg-white rounded-lg shadow p-6 text-center">
              <div class="text-2xl font-bold text-blue-600">{{ stats.totalProjects }}</div>
              <div class="text-sm text-gray-600">総案件数</div>
            </div>
            <div class="bg-white rounded-lg shadow p-6 text-center">
              <div class="text-2xl font-bold text-green-600">{{ stats.completedProjects }}</div>
              <div class="text-sm text-gray-600">完了案件</div>
            </div>
            <div class="bg-white rounded-lg shadow p-6 text-center">
              <div class="text-2xl font-bold text-yellow-600">{{ stats.pendingProjects }}</div>
              <div class="text-sm text-gray-600">進行中案件</div>
            </div>
            <div class="bg-white rounded-lg shadow p-6 text-center">
              <div class="text-2xl font-bold text-purple-600">{{ stats.totalInvoices }}</div>
              <div class="text-sm text-gray-600">請求書数</div>
            </div>
            <div class="bg-white rounded-lg shadow p-6 text-center">
              <div class="text-2xl font-bold text-pink-600">¥{{ stats.totalRevenue.toLocaleString() }}</div>
              <div class="text-sm text-gray-600">総収益</div>
            </div>
          </div>
        </div>

        <!-- プラグインアプリ選択 -->
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">🚀 アプリケーション</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            
            <!-- スポンサー案件管理アプリ -->
            <div class="bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow cursor-pointer" @click="navigateToApp('projects')">
              <div class="p-6">
                <div class="flex items-center mb-4">
                  <div class="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center text-2xl">
                    🏢
                  </div>
                  <div class="ml-4">
                    <h3 class="text-lg font-semibold text-gray-900">スポンサー案件管理</h3>
                    <p class="text-sm text-gray-600">案件の登録・管理・進捗追跡</p>
                  </div>
                </div>
                <div class="text-right">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-pink-100 text-pink-800">
                    {{ stats.totalProjects }} 件
                  </span>
                </div>
              </div>
            </div>

            <!-- 請求書管理アプリ -->
            <div class="bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow cursor-pointer" @click="navigateToApp('invoices')">
              <div class="p-6">
                <div class="flex items-center mb-4">
                  <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center text-2xl">
                    📋
                  </div>
                  <div class="ml-4">
                    <h3 class="text-lg font-semibold text-gray-900">請求書管理</h3>
                    <p class="text-sm text-gray-600">自動請求書生成・管理</p>
                  </div>
                </div>
                <div class="text-right">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                    {{ stats.totalInvoices }} 件
                  </span>
                </div>
              </div>
            </div>

            <!-- 将来プラグイン（予定） -->
            <div class="bg-gray-100 rounded-lg shadow cursor-not-allowed opacity-75">
              <div class="p-6">
                <div class="flex items-center mb-4">
                  <div class="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center text-2xl">
                    💡
                  </div>
                  <div class="ml-4">
                    <h3 class="text-lg font-semibold text-gray-600">投稿アイデアカレンダー</h3>
                    <p class="text-sm text-gray-500">コンテンツ企画・スケジュール管理</p>
                  </div>
                </div>
                <div class="text-right">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-200 text-gray-600">
                    準備中
                  </span>
                </div>
              </div>
            </div>

          </div>
        </div>

      </div>
    </main>

    <!-- 設定モーダル -->
    <div v-if="showSettings" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="showSettings = false">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white" @click.stop>
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold">⚙️ ユーザー設定</h3>
          <button @click="showSettings = false" class="text-gray-400 hover:text-gray-600">
            <span class="sr-only">閉じる</span>
            ✕
          </button>
        </div>
        <UserSettings />
      </div>
    </div>

  </div>
</template>

<style scoped>
/* InfluBerry カスタムスタイル */
header {
  backdrop-filter: blur(10px);
}

/* ホバーエフェクト */
.hover\:shadow-xl:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* スムーズなトランジション */
.transition-shadow {
  transition: box-shadow 0.3s ease;
}

/* モバイルファースト最適化 */
@media (max-width: 640px) {
  .max-w-7xl {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .grid-cols-5 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  
}

@media (max-width: 480px) {
  .grid-cols-5 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}
</style>