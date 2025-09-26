<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTodosStore } from '@/stores/todos'
import { useUIStore } from '@/stores/ui'
import UserSettings from '@/components/UserSettings.vue'
import BasicDataModal from '@/components/BasicDataModal.vue'

const router = useRouter()
const todosStore = useTodosStore()
const uiStore = useUIStore()

// Todo作成フォーム
const newTodo = ref({
  title: '',
  description: '',
  due_date: '',
  priority: 'medium',
  importance: 3,
  project_id: null,
  invoice_id: null
})

// プロジェクト・請求書選択肢
const projectOptions = ref([])
const invoiceOptions = ref([])

onMounted(async () => {
  await todosStore.fetchTodos()
  await fetchProjectOptions()
  await fetchInvoiceOptions()
})

const fetchProjectOptions = async () => {
  try {
    await todosStore.fetchProjectOptions()
    projectOptions.value = todosStore.projectOptions
  } catch (error) {
    console.error('プロジェクト選択肢取得エラー:', error)
  }
}

const fetchInvoiceOptions = async () => {
  try {
    await todosStore.fetchInvoiceOptions() 
    invoiceOptions.value = todosStore.invoiceOptions
  } catch (error) {
    console.error('請求書選択肢取得エラー:', error)
  }
}

// Todo作成
const createNewTodo = async () => {
  try {
    const todoData = {
      todo_title: newTodo.value.title,
      todo_description: newTodo.value.description,
      todo_due_date: newTodo.value.due_date,
      todo_priority: newTodo.value.priority,
      todo_importance: parseInt(newTodo.value.importance),
      project_id: newTodo.value.project_id,
      invoice_id: newTodo.value.invoice_id
    }
    
    await todosStore.createTodo(todoData)
    await todosStore.fetchTodos() // 表示問題根本解決パターン適用
    
    // フォームリセット
    newTodo.value = {
      title: '',
      description: '',
      due_date: '',
      priority: 'medium',
      importance: 3,
      project_id: null,
      invoice_id: null
    }
  } catch (error) {
    console.error('Todo作成エラー:', error)
  }
}

// Todo完了切り替え
const toggleComplete = async (todoId) => {
  try {
    await todosStore.completeTodo(todoId)
    await todosStore.fetchTodos()
  } catch (error) {
    console.error('完了切り替えエラー:', error)
  }
}

// Todo編集
const editTodo = ref(null)
const editForm = ref({
  title: '',
  description: '',
  due_date: '',
  priority: 'medium',
  importance: 3
})

const startEdit = (todo) => {
  editTodo.value = todo.id
  editForm.value = {
    title: todo.todo_title,
    description: todo.todo_description,
    due_date: todo.todo_due_date,
    priority: todo.todo_priority,
    importance: todo.todo_importance
  }
}

const cancelEdit = () => {
  editTodo.value = null
  editForm.value = {
    title: '',
    description: '',
    due_date: '',
    priority: 'medium',
    importance: 3
  }
}

const saveEdit = async () => {
  try {
    const updateData = {
      todo_title: editForm.value.title,
      todo_description: editForm.value.description,
      todo_due_date: editForm.value.due_date,
      todo_priority: editForm.value.priority,
      todo_importance: parseInt(editForm.value.importance)
    }
    
    await todosStore.updateTodo(editTodo.value, updateData)
    await todosStore.fetchTodos()
    cancelEdit()
  } catch (error) {
    console.error('編集エラー:', error)
  }
}

// Todo削除
const deleteTodoConfirm = async (todoId, todoTitle) => {
  if (confirm(`「${todoTitle}」を削除しますか？`)) {
    try {
      await todosStore.deleteTodo(todoId)
      await todosStore.fetchTodos()
    } catch (error) {
      console.error('削除エラー:', error)
    }
  }
}

// 優先度表示色
const getPriorityColor = (priority) => {
  switch (priority) {
    case 'high': return 'from-red-300 to-pink-400'
    case 'medium': return 'from-amber-300 to-yellow-400'
    case 'low': return 'from-green-300 to-emerald-400'
    default: return 'from-gray-300 to-gray-400'
  }
}

// ステータス表示色
const getStatusColor = (status) => {
  switch (status) {
    case 'completed': return 'from-green-300 to-emerald-400'
    case 'cancelled': return 'from-gray-300 to-gray-400'
    default: return 'from-amber-300 to-yellow-400'
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 via-white to-purple-50">
    <!-- ヘッダー（Berry統一ブランド） -->
    <header class="berry-header">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">

          <div class="flex items-center justify-between h-16">
            <!-- アプリタイトルのみ -->
            <div class="flex items-center">
              <h1 class="text-2xl font-bold bg-gradient-to-r from-pink-500 to-purple-600 bg-clip-text text-transparent">
                BerryDo｜タスク管理
              </h1>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-24">
      <!-- ローディング状態 -->
      <div v-if="todosStore.loading" class="text-center py-12">
        <div class="berry-loading">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500 mx-auto"></div>
          <p class="mt-4 text-gray-600">タスクを読み込んでいます...</p>
        </div>
      </div>

      <!-- エラー状態 -->
      <div v-else-if="todosStore.error" class="berry-error">
        <div class="bg-red-50 border border-red-200 rounded-2xl p-6">
          <p class="text-red-700 font-medium">エラーが発生しました</p>
          <p class="text-red-600">{{ todosStore.error }}</p>
        </div>
      </div>

      <!-- Todo管理メイン -->
      <div v-else class="space-y-8">
        
        <!-- Todo作成フォーム（Phase 4デザイン改革完了） -->
        <div class="berry-card-form">
          <div class="berry-card-header">
            <h2 class="text-xl font-bold text-gray-900">新しいタスクを作成</h2>
          </div>
          
          <form @submit.prevent="createNewTodo" class="space-y-6">
            <!-- タイトル入力 -->
            <div class="berry-input-group">
              <label class="berry-label">タスクタイトル *</label>
              <input 
                v-model="newTodo.title" 
                type="text" 
                required
                class="berry-input"
                placeholder="何をしますか？"
              />
            </div>

            <!-- 説明入力 -->
            <div class="berry-input-group">
              <label class="berry-label">詳細説明</label>
              <textarea 
                v-model="newTodo.description" 
                rows="3"
                class="berry-input resize-none"
                placeholder="詳細があれば入力してください"
              ></textarea>
            </div>

            <!-- 優先度・重要度・期限 -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="berry-input-group">
                <label class="berry-label">優先度</label>
                <select v-model="newTodo.priority" class="berry-select">
                  <option value="low">🟢 低</option>
                  <option value="medium">🟡 中</option>
                  <option value="high">🔴 高</option>
                </select>
              </div>

              <div class="berry-input-group">
                <label class="berry-label">重要度</label>
                <select v-model="newTodo.importance" class="berry-select">
                  <option value="1">⭐ 1 (低)</option>
                  <option value="2">⭐⭐ 2</option>
                  <option value="3">⭐⭐⭐ 3 (中)</option>
                  <option value="4">⭐⭐⭐⭐ 4</option>
                  <option value="5">⭐⭐⭐⭐⭐ 5 (高)</option>
                </select>
              </div>

              <div class="berry-input-group">
                <label class="berry-label">期限</label>
                <input 
                  v-model="newTodo.due_date" 
                  type="date"
                  class="berry-input"
                />
              </div>
            </div>

            <!-- BerryWork・BerryPay連動機能 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="berry-input-group">
                <label class="berry-label">
                  <span class="flex items-center">
                    📁 関連案件（BerryWork連動）
                  </span>
                </label>
                <select v-model="newTodo.project_id" class="berry-select">
                  <option value="">案件を選択（任意）</option>
                  <option v-for="project in projectOptions" :key="project.id" :value="project.id">
                    {{ project.company_name }} - {{ project.project_name || '名称未設定' }}
                  </option>
                </select>
              </div>

              <div class="berry-input-group">
                <label class="berry-label">
                  <span class="flex items-center">
                    💰 関連請求書（BerryPay連動）
                  </span>
                </label>
                <select v-model="newTodo.invoice_id" class="berry-select">
                  <option value="">請求書を選択（任意）</option>
                  <option v-for="invoice in invoiceOptions" :key="invoice.id" :value="invoice.id">
                    {{ invoice.client_company }} - ¥{{ Number(invoice.subtotal).toLocaleString() }}
                  </option>
                </select>
              </div>
            </div>

            <!-- 作成ボタン -->
            <div class="flex justify-end">
              <button type="submit" class="berry-primary-button">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
                タスクを作成
              </button>
            </div>
          </form>
        </div>

        <!-- Todoリスト（Phase 4カードベースUI完全実装） -->
        <div v-if="todosStore.sortedTodos?.length" class="space-y-4">
          <h2 class="text-xl font-bold text-gray-900 mb-6">タスク一覧</h2>
          
          <div v-for="todo in todosStore.sortedTodos" :key="todo.id" 
               class="berry-todo-card"
               :class="getStatusColor(todo.todo_status)">
            
            <!-- 編集モード -->
            <div v-if="editTodo === todo.id" class="space-y-4">
              <div class="berry-input-group">
                <input v-model="editForm.title" 
                       class="berry-input" 
                       placeholder="タスクタイトル" />
              </div>
              
              <div class="berry-input-group">
                <textarea v-model="editForm.description" 
                          rows="2"
                          class="berry-input resize-none" 
                          placeholder="詳細説明"></textarea>
              </div>
              
              <div class="grid grid-cols-3 gap-4">
                <select v-model="editForm.priority" class="berry-select">
                  <option value="low">🟢 低</option>
                  <option value="medium">🟡 中</option>
                  <option value="high">🔴 高</option>
                </select>
                
                <select v-model="editForm.importance" class="berry-select min-w-48">
                  <option value="1">⭐ 1</option>
                  <option value="2">⭐⭐ 2</option>
                  <option value="3">⭐⭐⭐ 3</option>
                  <option value="4">⭐⭐⭐⭐ 4</option>
                  <option value="5">⭐⭐⭐⭐⭐ 5</option>
                </select>
                
                </div>

                <div class="berry-input-group">
                  <label class="berry-label">期限</label>
                  <input v-model="editForm.due_date" 
                        type="date" 
                        class="berry-input" />
                </div>

                <div class="flex justify-between items-center mt-6">
                <div></div>
                <div class="flex space-x-4">
                  <button @click="cancelEdit" class="berry-secondary-button">
                    キャンセル
                  </button>
                  <button @click="saveEdit" class="berry-primary-button">
                    保存
                  </button>
                </div>
              </div>
            </div>

            <!-- 表示モード -->
            <div v-else class="flex items-start justify-between">
              <!-- 完了チェックボックス + コンテンツ -->
              <div class="flex items-start space-x-4 flex-1">
                <!-- 大型完了ボタン（Phase 4改革） -->
                <button @click="toggleComplete(todo.id)" 
                        class="berry-complete-button"
                        :class="todo.todo_status === 'completed' ? 'completed' : 'pending'">
                  <svg v-if="todo.todo_status === 'completed'" 
                       class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <div v-else class="w-6 h-6 rounded-full border-2 border-gray-300"></div>
                </button>

                <!-- タスク情報 -->
                <div class="flex-1 min-w-0">
                  <h3 class="font-bold text-gray-900 text-lg mb-2"
                      :class="todo.todo_status === 'completed' ? 'line-through opacity-60' : ''">
                    {{ todo.todo_title }}
                  </h3>
                  
                  <p v-if="todo.todo_description" 
                     class="text-gray-600 mb-3"
                     :class="todo.todo_status === 'completed' ? 'line-through opacity-60' : ''">
                    {{ todo.todo_description }}
                  </p>
                  
                  <!-- メタ情報 -->
                  <div class="flex flex-wrap gap-3 text-sm">
                    <span class="berry-badge" :class="getPriorityColor(todo.todo_priority)">
                      優先度: {{ todo.todo_priority }}
                    </span>
                    <span class="berry-badge bg-gradient-to-r from-blue-300 to-indigo-400">
                      重要度: {{ '⭐'.repeat(todo.todo_importance) }} {{ todo.todo_importance }}
                    </span>
                    <span v-if="todo.todo_due_date" class="berry-badge bg-gradient-to-r from-purple-300 to-pink-400">
                      期限: {{ todo.todo_due_date }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- 操作ボタン（Phase 4モダン化） -->
              <div class="flex items-center space-x-2 ml-4">
                <button @click="startEdit(todo)" 
                        class="berry-action-button edit"
                        title="編集">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                </button>
                
                <button @click="deleteTodoConfirm(todo.id, todo.todo_title)" 
                        class="berry-action-button delete"
                        title="削除">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- タスクなし状態 -->
        <div v-else class="berry-empty-state">
          <div class="text-center py-16">
            <div class="berry-empty-icon">
              📝
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">タスクがありません</h3>
            <p class="text-gray-600 mb-8">新しいタスクを作成してください。</p>
          </div>
        </div>
      </div>
    </main>

    <!-- 設定モーダル -->
    <div v-if="uiStore.showSettings" 
         class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" 
         @click="uiStore.closeSettings()">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="berry-modal" @click.stop>
          <div class="berry-modal-header">
            <h3 class="text-lg font-medium text-gray-900">設定</h3>
            <button @click="uiStore.closeSettings()" class="berry-close-button">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <UserSettings />
        </div>
      </div>
    </div>

    <!-- 基本データモーダル -->
    <BasicDataModal v-if="uiStore.showBasicData" />
  </div>
</template>

<style scoped>
/* Phase 4 デザインシステム完全実装 */

/* ヘッダー */
.berry-header {
  @apply bg-gradient-to-r from-pink-50 via-white to-purple-50 backdrop-blur-sm;
  @apply border-b border-pink-100 shadow-sm;
}

/* ナビゲーションボタン */
.berry-nav-button {
  @apply px-4 py-2 text-sm font-medium text-gray-700;
  @apply bg-white rounded-xl border border-gray-200;
  @apply hover:bg-pink-50 hover:text-pink-600 hover:border-pink-300;
  @apply transition-all duration-200 transform hover:scale-105;
}

.berry-icon-button {
  @apply p-2 text-gray-600 bg-white rounded-xl border border-gray-200;
  @apply hover:bg-pink-50 hover:text-pink-600 hover:border-pink-300;
  @apply transition-all duration-200 transform hover:scale-105;
}

/* カードシステム */
.berry-card-form {
  @apply bg-gradient-to-br from-pink-50 to-purple-50;
  @apply rounded-2xl shadow-lg hover:shadow-xl;
  @apply border border-pink-100 p-8;
  @apply transition-all duration-300;
}

.berry-card-header {
  @apply mb-6 pb-4 border-b border-pink-200;
}

.berry-todo-card {
  @apply bg-gradient-to-br rounded-2xl shadow-lg hover:shadow-xl;
  @apply border border-pink-100 p-6;
  @apply transition-all duration-300 transform hover:scale-[1.02];
}

/* 入力要素 */
.berry-input-group {
  @apply space-y-2;
}

.berry-label {
  @apply block text-sm font-bold text-gray-700;
}

.berry-input {
  @apply w-full px-4 py-3 rounded-xl border border-pink-200;
  @apply bg-white/80 backdrop-blur-sm;
  @apply focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-transparent;
  @apply placeholder-gray-400 transition-all duration-200;
}

.berry-select {
  @apply w-full px-4 py-3 rounded-xl border border-pink-200;
  @apply bg-white/80 backdrop-blur-sm;
  @apply focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-transparent;
  @apply transition-all duration-200;
}

/* ボタンシステム */
.berry-primary-button {
  @apply flex items-center px-6 py-3 rounded-xl font-bold text-white;
  @apply bg-gradient-to-r from-pink-400 to-purple-500;
  @apply hover:from-pink-500 hover:to-purple-600;
  @apply transform hover:scale-105 transition-all duration-200;
  @apply shadow-lg hover:shadow-xl;
}

.berry-secondary-button {
  @apply px-4 py-2 rounded-xl font-medium text-gray-700;
  @apply bg-white border border-gray-300;
  @apply hover:bg-gray-50 hover:border-gray-400;
  @apply transition-all duration-200;
}

/* 完了ボタン（大型化・タップ体験向上） */
.berry-complete-button {
  @apply flex items-center justify-center w-12 h-12 rounded-full;
  @apply transition-all duration-300 transform hover:scale-110;
  @apply shadow-md hover:shadow-lg;
}

.berry-complete-button.completed {
  @apply bg-gradient-to-br from-green-400 to-emerald-500 text-white;
  @apply shadow-green-200;
}

.berry-complete-button.pending {
  @apply bg-white border-2 border-gray-300;
  @apply hover:border-pink-400 hover:bg-pink-50;
}

/* アクションボタン（モダン化・ホバーエフェクト） */
.berry-action-button {
  @apply p-3 rounded-xl transition-all duration-200;
  @apply transform hover:scale-110;
}

.berry-action-button.edit {
  @apply text-blue-600 bg-blue-50 hover:bg-blue-100;
  @apply border border-blue-200 hover:border-blue-300;
}

.berry-action-button.delete {
  @apply text-red-600 bg-red-50 hover:bg-red-100;
  @apply border border-red-200 hover:border-red-300;
}

/* バッジ */
.berry-badge {
  @apply inline-flex items-center px-3 py-1 rounded-full text-xs font-bold text-white;
  @apply shadow-sm;
}

/* 空状態 */
.berry-empty-state {
  @apply bg-gradient-to-br from-pink-50 to-purple-50;
  @apply rounded-2xl border border-pink-100;
}

.berry-empty-icon {
  @apply text-6xl mb-6 opacity-60;
}

/* ローディング */
.berry-loading {
  @apply text-center;
}

/* エラー */
.berry-error {
  @apply mb-8;
}

/* モーダル */
.berry-modal {
  @apply inline-block align-bottom bg-white rounded-2xl text-left overflow-hidden;
  @apply shadow-xl transform transition-all;
  @apply sm:my-8 sm:align-middle sm:max-w-lg sm:w-full;
  @apply border border-pink-100;
}

.berry-modal-header {
  @apply bg-gradient-to-r from-pink-50 to-purple-50 px-6 pt-6 pb-4;
  @apply flex items-center justify-between border-b border-pink-100;
}

.berry-close-button {
  @apply text-gray-400 hover:text-gray-600 transition-colors duration-200;
}
</style>