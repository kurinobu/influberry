<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useProjectsStore } from '../stores/projects.js'
import { useUIStore } from '../stores/ui.js'
import ProjectList from '../components/ProjectList.vue'
import HamburgerMenu from '../components/HamburgerMenu.vue'
import UserSettings from '../components/UserSettings.vue'
import BasicDataModal from '../components/BasicDataModal.vue'

const router = useRouter()
const authStore = useAuthStore()
const projectsStore = useProjectsStore()
const uiStore = useUIStore()

// アプリ初期化
onMounted(async () => {
  // 未認証の場合は認証ページへリダイレクト
  await authStore.checkAuthStatus()
  if (!authStore.isLoggedIn) {
    router.push('/')
    return
  }
  
  // プロジェクトデータ取得
  await projectsStore.fetchProjects()
})

// 設定モーダル表示状態
// const showSettings = ref(false) // UIStoreに移管
// const showBasicData = ref(false) // UIStoreに移管

// 設定モーダル切り替え
// const toggleSettings = () => { // UIStoreに移管
//   showSettings.value = !showSettings.value
// }

// const toggleBasicData = () => { // UIStoreに移管
//   showBasicData.value = !showBasicData.value
// }
// ダッシュボードに戻る
const backToDashboard = () => {
  router.push('/dashboard')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- ヘッダー -->
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
          <HamburgerMenu />
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
                <h2 class="text-2xl font-bold text-gray-900">スポンサー案件管理</h2>
                <p class="mt-1 text-sm text-gray-600">
                  案件の登録・編集・削除・進捗管理を行います
                </p>
              </div>
              <div class="flex items-center space-x-4">
                <div class="text-center">
                  <div class="text-2xl font-bold text-pink-600">{{ projectsStore.projects?.length || 0 }}</div>
                  <div class="text-xs text-gray-500">総案件数</div>
                </div>
                <div class="text-center">
                  <div class="text-2xl font-bold text-green-600">
                    {{ projectsStore.projects?.filter(p => p.status === 'completed').length || 0 }}
                  </div>
                  <div class="text-xs text-gray-500">完了</div>
                </div>
                <div class="text-center">
                  <div class="text-2xl font-bold text-yellow-600">
                    {{ projectsStore.pendingProjectsCount || 0 }}
                  </div>
                  <div class="text-xs text-gray-500">進行中</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ProjectList コンポーネント -->
        <ProjectList />

      </div>
    </main>
    <!-- 設定モーダル -->
    <div v-if="uiStore.showSettings" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="uiStore.closeSettings()">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full" @click.stop>
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">設定</h3>
              <button @click="uiStore.closeSettings()" class="text-gray-400 hover:text-gray-600">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            <UserSettings />
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- 基本データモーダル -->
    <BasicDataModal />
</template>

<style scoped>
/* InfluBerry カスタムスタイル */
header {
  backdrop-filter: blur(10px);
}

/* ホバーエフェクト */
.hover\:text-pink-200:hover {
  color: rgb(251 207 232);
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
}
</style>