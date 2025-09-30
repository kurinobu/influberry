<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useProjectsStore } from '../stores/projects.js'
import ProjectList from '../components/ProjectList.vue'
import HamburgerMenu from '../components/HamburgerMenu.vue'
import UserSettings from '../components/UserSettings.vue'
import BasicDataModal from '../components/BasicDataModal.vue'

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

// 設定モーダル表示状態
const showSettings = ref(false)
const showBasicData = ref(false)

// 設定モーダル切り替え
const toggleSettings = () => {
  showSettings.value = !showSettings.value
}

// 基本データモーダル切り替え
const toggleBasicData = () => {
  showBasicData.value = !showBasicData.value
}
// ダッシュボードに戻る
const backToDashboard = () => {
  router.push('/dashboard')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- ヘッダー -->
    <header class="berry-header">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- アプリタイトルのみ -->
          <div class="flex items-center">
            <h1 class="text-2xl font-bold bg-gradient-to-r from-pink-500 to-purple-600 bg-clip-text text-transparent">
              BerryWork｜案件管理
            </h1>
          </div>
          
          <!-- ハンバーガーメニュー -->
          <HamburgerMenu @openSettings="toggleSettings" @openBasicData="toggleBasicData" />
        </div>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        
        <!-- アプリヘッダー -->
        <div class="mb-6">
          <div class="berry-card">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-2xl font-bold text-gray-900">BerryWork｜案件管理</h2>
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
    <div v-if="showSettings" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="showSettings = false">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full" @click.stop>
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">設定</h3>
              <button @click="showSettings = false" class="text-gray-400 hover:text-gray-600">
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
    <BasicDataModal :show="showBasicData" @close="showBasicData = false" />
</template>

<style scoped>
/* === Phase 4 Z世代向けカードベースUI === */
.berry-card-form {
  background: linear-gradient(135deg, #fdf2f8 0%, #f3e8ff 100%);
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(244, 114, 182, 0.15);
  border: 2px solid #f9a8d4;
  padding: 2rem;
  transition: all 0.3s ease;
  margin-bottom: 1.5rem;
}

.berry-card-form:hover {
  box-shadow: 0 20px 40px rgba(244, 114, 182, 0.2);
  transform: translateY(-2px);
}

.berry-card {
  background: linear-gradient(135deg, #ffffff 0%, #fdf2f8 100%);
  border-radius: 1rem;
  box-shadow: 0 8px 20px rgba(244, 114, 182, 0.12);
  border: 2px solid #f9a8d4;
  padding: 1.5rem;
  transition: all 0.3s ease;
  margin-bottom: 1rem;
  transform: scale(1);
}

.berry-card:hover {
  box-shadow: 0 12px 30px rgba(244, 114, 182, 0.2);
  transform: scale(1.02) translateY(-2px);
}

.berry-card-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f9a8d4;
}

/* === Phase 4 入力フィールドスタイル === */
.berry-input {
  width: 100%;
  padding: 1rem 1.25rem;
  border-radius: 0.75rem;
  border: 2px solid #f9a8d4;
  background: #ffffff;
  font-size: 1rem;
  font-weight: 500;
  color: #111827;
  line-height: 1.5;
  transition: all 0.2s ease;
}

.berry-input:focus {
  outline: none;
  border-color: #ec4899;
  box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.1);
  background: #ffffff;
}

.berry-select {
  width: 100%;
  padding: 1rem 1.25rem;
  border-radius: 0.75rem;
  border: 2px solid #f9a8d4;
  background: #ffffff;
  font-size: 1rem;
  font-weight: 500;
  color: #111827;
  transition: all 0.2s ease;
}

.berry-select:focus {
  outline: none;
  border-color: #ec4899;
  box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.1);
}

.berry-textarea {
  width: 100%;
  padding: 1rem 1.25rem;
  border-radius: 0.75rem;
  border: 2px solid #f9a8d4;
  background: #ffffff;
  font-size: 1rem;
  font-weight: 500;
  color: #111827;
  line-height: 1.6;
  min-height: 120px;
  resize: vertical;
  transition: all 0.2s ease;
}

.berry-textarea:focus {
  outline: none;
  border-color: #ec4899;
  box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.1);
}

/* === Phase 4 ラベルスタイル === */
.berry-label {
  display: block;
  font-size: 1rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.5rem;
  text-shadow: none;
}

.berry-input-group {
  margin-bottom: 1.5rem;
}

/* === Phase 4 ボタンスタイル === */
.berry-button {
  background: linear-gradient(45deg, #ec4899, #be185d);
  color: white;
  border-radius: 0.75rem;
  padding: 1rem 1.5rem;
  font-weight: 700;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  transform: scale(1);
  box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
  text-shadow: none;
}

.berry-button:hover {
  background: linear-gradient(45deg, #be185d, #9d174d);
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(236, 72, 153, 0.4);
}

.berry-button:active {
  transform: scale(0.98);
}

.berry-button-secondary {
  background: linear-gradient(45deg, #8b5cf6, #7c3aed);
  color: white;
  border-radius: 0.75rem;
  padding: 0.75rem 1.25rem;
  font-weight: 600;
  font-size: 0.875rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  transform: scale(1);
  box-shadow: 0 3px 10px rgba(139, 92, 246, 0.3);
}

.berry-button-secondary:hover {
  background: linear-gradient(45deg, #7c3aed, #6d28d9);
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.4);
}

.berry-button-danger {
  background: linear-gradient(45deg, #ef4444, #dc2626);
  color: white;
  border-radius: 0.75rem;
  padding: 0.75rem 1.25rem;
  font-weight: 600;
  font-size: 0.875rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  transform: scale(1);
  box-shadow: 0 3px 10px rgba(239, 68, 68, 0.3);
}

.berry-button-danger:hover {
  background: linear-gradient(45deg, #dc2626, #b91c1c);
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(239, 68, 68, 0.4);
}

/* === Phase 4 高コントラスト視認性確保 === */
h1, h2, h3, h4, h5, h6 {
  color: #111827 !important;
  font-weight: 700 !important;
  text-shadow: none !important;
}

p, span, div {
  color: #374151 !important;
  font-weight: 500 !important;
  line-height: 1.6 !important;
}

/* ヘッダータイトル強制カラフル表示 */
h1.text-2xl.font-bold {
  background: linear-gradient(to right, #ec4899, #8b5cf6) !important;
  -webkit-background-clip: text !important;
  background-clip: text !important;
  color: transparent !important;
}

/* === InfluBerry ヘッダースタイル統合 === */
header {
  backdrop-filter: blur(10px);
  background: linear-gradient(to right, #fdf2f8, #f3e8ff) !important;
  border-color: #ec4899 !important;
}

/* === Phase 4 レスポンシブ・モバイル最適化 === */
@media (max-width: 640px) {
  .berry-card-form {
    padding: 1.5rem;
    margin: 0 0.5rem 1rem;
  }
  
  .berry-card {
    padding: 1rem;
    margin: 0 0.5rem 0.75rem;
  }
  
  .berry-input, .berry-select, .berry-textarea {
    padding: 0.875rem 1rem;
    font-size: 1rem;
  }
  
  .berry-button {
    padding: 0.875rem 1.25rem;
    font-size: 1rem;
    width: 100%;
    justify-content: center;
  }
  
  .berry-button-secondary, .berry-button-danger {
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
    width: 100%;
    justify-content: center;
  }
  
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
  .berry-card-form {
    padding: 1rem;
    margin: 0 0.25rem 0.75rem;
  }
  
  .berry-card {
    padding: 0.75rem;
    margin: 0 0.25rem 0.5rem;
  }
  
  .text-xl {
    font-size: 1rem;
    line-height: 1.5rem;
  }
  
  .text-2xl {
    font-size: 1.25rem;
    line-height: 1.75rem;
  }
}

/* === アニメーション・マイクロインタラクション === */
@keyframes fadeIn {
  from { 
    opacity: 0; 
    transform: translateY(10px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.berry-card {
  animation: fadeIn 0.3s ease-out;
}

.berry-button:active {
  animation: pulse 0.2s ease-in-out;
}

/* === ステータスカラー（案件管理特化） === */
.status-proposed {
  background: linear-gradient(135deg, #fef3c7, #fbbf24) !important;
  color: #92400e !important;
  border-color: #f59e0b !important;
}

.status-contracted {
  background: linear-gradient(135deg, #dcfce7, #22c55e) !important;
  color: #15803d !important;
  border-color: #16a34a !important;
}

.status-completed {
  background: linear-gradient(135deg, #e0e7ff, #6366f1) !important;
  color: #3730a3 !important;
  border-color: #4f46e5 !important;
}

/* berry-header統一スタイル（TodoApp.vue成功パターン） */
.berry-header {
  background: linear-gradient(to right, #fdf2f8, #ffffff, #f3e8ff);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid #f9a8d4;
  box-shadow: 0 1px 3px rgba(244, 114, 182, 0.1);
}
</style>