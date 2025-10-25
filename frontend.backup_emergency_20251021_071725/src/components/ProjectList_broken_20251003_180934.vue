<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProjectsStore } from '../stores/projects.js'
import { useInvoicesStore } from '../stores/invoices.js'
import { useAuthStore } from '../stores/auth.js'
import { trackInvoiceCreate, trackError } from '@/utils/analytics.js'
import ProjectForm from './ProjectForm.vue'

// プロジェクト管理ストア
const projectsStore = useProjectsStore()
const invoicesStore = useInvoicesStore()

// ローカル状態
const showCreateForm = ref(false)
const selectedStatus = ref('')
const editingProject = ref(null)

// 計算プロパティ


const totalAmount = computed(() => projectsStore.totalAmount)

// フィルター独立化：統計とフィルター表示の完全分離
const filteredProjects = computed(() => {
  if (!selectedStatus.value) return projectsStore.projects.filter(p => p.is_todo !== 1)
return projectsStore.projects.filter(p => p.is_todo !== 1 && p.status === selectedStatus.value)
})

// コンポーネント初期化
onMounted(async () => {
  projectsStore.clearError()
  // 認証状態確認を待ってからプロジェクト取得
  const authStore = useAuthStore()
  await authStore.getCurrentUser()
  if (projectsStore.projects.length === 0) {
    await projectsStore.fetchProjects()
  }
})

// ステータス変更
const handleStatusFilter = (status) => {
  selectedStatus.value = status === selectedStatus.value ? '' : status
}

// プロジェクト作成フォーム切り替え
// ProjectForm モーダル制御
const openCreateForm = () => {
  editingProject.value = null
  showCreateForm.value = true
}

const openEditForm = (project) => {
  editingProject.value = project
  showCreateForm.value = true
}

const closeProjectForm = () => {
  showCreateForm.value = false
  editingProject.value = null
}

const handleFormSuccess = (result) => {
  console.log(result.message)
  projectsStore.fetchProjects()
}

const deleteProject = async (project) => {
  if (confirm(`「${project.company_name}」を削除しますか？この操作は取り消せません。`)) {
    const result = await projectsStore.deleteProject(project.id)
    if (result.success) {
      console.log('プロジェクトを削除しました')
    } else {
      console.error('削除エラー:', result.error)
      trackError('project_delete', result.error, 'ProjectList')
    }
  }
}

// 請求書作成
const createInvoiceFromProject = async (project) => {
  if (confirm(`「${project.company_name}」の請求書を作成しますか？`)) {
    // デバッグ: 開始通知
    alert('🔄 請求書作成を開始します...')
    
    try {
      const result = await invoicesStore.createInvoiceFromProject(project.id)
      
      if (result) {
        // 成功時の処理
        console.log('請求書を作成しました:', result.invoice_number)
        trackInvoiceCreate(true, project.amount)
        
        // ✅ 成功フィードバック
        alert(`✅ 請求書を作成しました\n請求書番号: ${result.invoice_number}`)
      } else {
        // 失敗時の処理
        console.error('請求書作成エラー:', invoicesStore.error)
        trackError('invoice_create', invoicesStore.error, 'ProjectList')
        
        // ❌ 失敗フィードバック
        alert(`❌ 請求書作成に失敗しました\n${invoicesStore.error || 'エラー内容不明'}`)
      }
    } catch (error) {
      // 例外キャッチ
      console.error('請求書作成例外:', error)
      alert(`🚨 予期しないエラーが発生しました\n${error.message || error}`)
    }
  }
}

// 日付フォーマット
const formatDeadline = (deadline) => {
  const date = new Date(deadline)
  return date.toLocaleDateString('ja-JP', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// ステータス表示色
const getStatusColor = (status) => {
  const colors = {
    proposed: 'bg-yellow-100 text-yellow-800',
    contracted: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}
</script>

<template>
  <div class="space-y-6">
    <!-- ダッシュボード統計 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <!-- 総案件数 -->
      <div class="berry-card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-pink-100 rounded-lg flex items-center justify-center">
              📊
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">総案件数</p>
            <p class="text-2xl font-bold text-gray-900">
              {{ projectsStore.projects.length }}
            </p>
          </div>
        </div>
      </div>

      <!-- 合計金額 -->
      <div class="berry-card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
              💰
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">合計金額</p>
            <p class="text-2xl font-bold text-gray-900">
              ¥{{ totalAmount.toLocaleString() }}
            </p>
          </div>
        </div>
      </div>

      <!-- 進行中案件 -->
      <div class="berry-card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              🔄
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">進行中</p>
            <p class="text-2xl font-bold text-gray-900">
              {{ projectsStore.pendingProjectsCount }}
            </p>
          </div>
        </div>
      </div>

      <!-- 完了案件 -->
      <div class="berry-card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
              ✅
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">完了</p>
            <p class="text-2xl font-bold text-gray-900">
              {{ projectsStore.completedCount }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- 操作バー -->
    <div class="berry-card">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-3 sm:space-y-0">
        <!-- ステータスフィルター -->
        <div class="flex items-center space-x-2">
          <span class="text-sm font-medium text-gray-700">フィルター:</span>
          <div class="flex space-x-2">
            <button
              @click="handleStatusFilter('proposed')"
              :class="[
                'px-3 py-1 rounded-full text-xs font-medium transition-colors',
                selectedStatus === 'proposed' 
                  ? 'bg-yellow-200 text-yellow-800' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              ]"
            >
              提案中 ({{ projectsStore.proposedCount }})
            </button>
            <button
              @click="handleStatusFilter('contracted')"
              :class="[
                'px-3 py-1 rounded-full text-xs font-medium transition-colors',
                selectedStatus === 'contracted' 
                  ? 'bg-blue-200 text-blue-800' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              ]"
            >
              契約中 ({{ projectsStore.contractedCount }})
            </button>
            <button
              @click="handleStatusFilter('completed')"
              :class="[
                'px-3 py-1 rounded-full text-xs font-medium transition-colors',
                selectedStatus === 'completed' 
                  ? 'bg-green-200 text-green-800' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              ]"
            >
              完了 ({{ projectsStore.completedCount }})
            </button>
          </div>
        </div>

        <!-- 新規作成ボタン -->
        <button
          @click="openCreateForm"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-pink-500 hover:bg-pink-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500 transition-colors"
        >
          ➕ 新規案件作成
        </button>
      </div>
    </div>

    <!-- ローディング状態 -->
    <div v-if="projectsStore.isLoading" class="text-center py-8">
      <div class="inline-flex items-center px-4 py-2 font-semibold leading-6 text-sm shadow rounded-md text-white bg-pink-500 transition ease-in-out duration-150">
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        読み込み中...
      </div>
    </div>

    <!-- エラー表示 -->
    <div v-else-if="projectsStore.error" class="bg-red-50 border border-red-200 rounded-md p-4">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">エラーが発生しました</h3>
          <div class="mt-2 text-sm text-red-700">
            <p>{{ projectsStore.error }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- プロジェクト一覧 -->
    <div v-else-if="projectsStore.projects.length > 0" class="berry-card overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">案件一覧</h3>
      </div>
      
      <div class="divide-y divide-gray-200">
        <div
          v-for="project in filteredProjects"
          :key="project.id"
          class="p-6 hover:bg-gray-50 transition-colors"
        >
          <div class="flex flex-col space-y-4">
            <div class="flex-1 min-w-0">
              <div class="flex items-center space-x-3">
                <div class="space-y-1">
                <h4 class="text-sm font-medium text-gray-900 truncate">
                  {{ project.company_name }}
                </h4>
                <div v-if="project.project_name" class="text-sm text-gray-600">
                  {{ project.project_name }}
                </div>
              </div>
                <span
                  :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    getStatusColor(project.status)
                  ]"
                >
                  {{ project.status_display }}
                </span>
              </div>
              
              <div class="mt-2 flex items-center space-x-6 text-sm text-gray-500">
                <div class="flex items-center">
                  <span class="font-medium">金額:</span>
                  <span class="ml-1 text-gray-900">{{ project.amount_formatted }}</span>
                </div>
                <div class="flex items-center">
                  <span class="font-medium">納期:</span>
                  <span class="ml-1">{{ project.deadline_formatted }}</span>
                </div>
                <div v-if="project.days_until_deadline !== null" class="flex items-center">
                  <span class="font-medium">残り:</span>
                  <span 
                    :class="[
                      'ml-1',
                      project.days_until_deadline <= 7 ? 'text-red-600 font-medium' : 'text-gray-900'
                    ]"
                  >
                    {{ project.days_until_deadline }}日
                  </span>
                </div>
              </div>
              
              <p class="mt-2 text-sm text-gray-600 line-clamp-2">
                {{ project.description }}
              </p>
            </div>
            
            <div class="flex flex-wrap gap-2 pt-3 border-t border-gray-100">
              <button @click="openEditForm(project)" class="text-blue-600 hover:text-blue-800 text-sm">
                📝 編集
              </button>
              <button @click="deleteProject(project)" class="text-red-600 hover:text-red-800 text-sm">
                🗑️ 削除
              </button>
              <button @click="createInvoiceFromProject(project)" class="text-green-600 hover:text-green-800 text-sm">
                📄 請求書
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状態 -->
    <div v-else class="text-center py-12">
      <div class="w-24 h-24 mx-auto mb-4 text-gray-300">
        📋
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">案件がありません</h3>
      <p class="text-gray-500 mb-6">新しい案件を作成して始めましょう。</p>
      <button
        @click="openCreateForm"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-pink-500 hover:bg-pink-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500"
      >
        ➕ 最初の案件を作成
      </button>
    </div>
  </div>
  <!-- ProjectForm モーダル -->
  <ProjectForm
    :is-open="showCreateForm"
    :project="editingProject"
    @close="closeProjectForm"
    @success="handleFormSuccess"
  />
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* スムーズなアニメーション */
.transition-colors {
  transition: background-color 0.2s ease, color 0.2s ease;
}

/* ホバーエフェクト */
.hover\:bg-gray-50:hover {
  background-color: #f9fafb;
}

/* フォーカス状態 */
.focus\:ring-2:focus {
  box-shadow: 0 0 0 2px rgba(ec, 4a, 99, 0.5);
}
/* === Phase 4 Z世代向けカードベースUI === */
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
</style>