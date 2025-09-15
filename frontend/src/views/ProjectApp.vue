<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useProjectsStore } from '../stores/projects.js'
import ProjectList from '../components/ProjectList.vue'

const router = useRouter()
const authStore = useAuthStore()
const projectsStore = useProjectsStore()

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
          <!-- ナビゲーション -->
          <div class="flex items-center space-x-4">
            <button
              @click="backToDashboard"
              class="inline-flex items-center px-3 py-2 text-sm font-medium text-white hover:text-pink-200 transition-colors"
            >
              ← ダッシュボード
            </button>
            <div class="h-6 w-px bg-white/30"></div>
            <h1 class="text-xl font-bold text-white font-poppins">
              🏢 スポンサー案件管理
            </h1>
          </div>
          
          <!-- ユーザー情報 -->
          <div class="flex items-center">
            <span class="text-sm text-white font-poppins">
              {{ authStore.userName }}さん
            </span>
          </div>
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
  </div>
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
}
</style>