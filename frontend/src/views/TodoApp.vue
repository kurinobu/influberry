<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useUIStore } from '../stores/ui.js'
import { useTodosStore } from '../stores/todos.js'
import HamburgerMenu from '../components/HamburgerMenu.vue'
import UserSettings from '../components/UserSettings.vue'
import BasicDataModal from '../components/BasicDataModal.vue'

const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()
const todosStore = useTodosStore()
// Todo作成用リアクティブ変数
const newTodo = ref({
  title: '',
  description: '',
  priority: 'medium',
  importance: 3,
  due_date: ''
})

// Todo作成関数
const createNewTodo = async () => {
  try {
    await todosStore.createTodo({
      todo_title: newTodo.value.title,
      todo_description: newTodo.value.description,
      todo_priority: newTodo.value.priority,
      todo_importance: parseInt(newTodo.value.importance),
      todo_due_date: newTodo.value.due_date || null
    })
    
    // フォームリセット
    newTodo.value = {
      title: '',
      description: '',
      priority: 'medium',
      importance: 3,
      due_date: ''
    }
  } catch (error) {
    console.error('Todo作成エラー:', error)
  }
}
// Todo関連の状態
// Todoデータ取得（Store経由）


// アプリ初期化
onMounted(async () => {
  // 未認証の場合は認証ページへリダイレクト
  try {
    await authStore.checkAuthStatus()
  } catch (error) {
    console.warn('認証状態確認エラー:', error)
  }
  
  if (!authStore.isLoggedIn) {
    router.push('/')
    return
  }
  
  // Todoデータ取得
  await todosStore.fetchTodos()
})

// Todoデータ取得（Store経由）


// ダッシュボードに戻る
const backToDashboard = () => {
  router.push('/dashboard')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- ヘッダー -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- アプリタイトル -->
          <div class="flex items-center">
            <button @click="backToDashboard" class="text-gray-600 hover:text-gray-900 mr-4">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
              </svg>
            </button>
            <h1 class="text-xl font-semibold text-gray-900">BerryDo｜タスク管理</h1>
          </div>

          <!-- 右側メニュー -->
          <div class="flex items-center space-x-4">
            <!-- ハンバーガーメニュー -->
            <HamburgerMenu />
          </div>
        </div>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- 読み込み中 -->
        <div v-if="todosStore.loading === true" class="text-center py-8">
          <div class="inline-flex items-center px-4 py-2 font-semibold leading-6 text-sm shadow rounded-md text-white bg-indigo-500 hover:bg-indigo-400 transition ease-in-out duration-150">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            読み込み中...
          </div>
        </div>

        <!-- エラー表示 -->
        <div v-else-if="todosStore.error" class="rounded-md bg-red-50 p-4 mb-6">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">エラーが発生しました</h3>
              <div class="mt-2 text-sm text-red-700">
                <p>{{ todosStore.error }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Todo一覧表示 -->
        <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
          <div class="px-4 py-5 sm:p-6">
            <!-- Todo作成フォーム -->
            <div class="mb-6 p-4 border border-pink-200 rounded-lg bg-pink-50">
              <h3 class="text-md font-medium text-gray-900 mb-4">新しいタスクを作成</h3>
              <form @submit.prevent="createNewTodo" class="space-y-4">
                <!-- タイトル入力 -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">タイトル *</label>
                  <input 
                    v-model="newTodo.title" 
                    type="text" 
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-pink-500 focus:border-pink-500"
                    placeholder="タスクのタイトルを入力"
                  />
                </div>
                
                <!-- 説明入力 -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">説明</label>
                  <textarea 
                    v-model="newTodo.description" 
                    rows="3"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-pink-500 focus:border-pink-500"
                    placeholder="タスクの詳細を入力（任意）"
                  ></textarea>
                </div>
                
                <!-- 優先度・重要度・期限 -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">優先度</label>
                    <select v-model="newTodo.priority" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-pink-500 focus:border-pink-500">
                      <option value="low">低</option>
                      <option value="medium">中</option>
                      <option value="high">高</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">重要度</label>
                    <select v-model="newTodo.importance" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-pink-500 focus:border-pink-500">
                      <option value="1">1 (低)</option>
                      <option value="2">2</option>
                      <option value="3">3 (中)</option>
                      <option value="4">4</option>
                      <option value="5">5 (高)</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">期限</label>
                    <input 
                      v-model="newTodo.due_date" 
                      type="date"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-pink-500 focus:border-pink-500"
                    />
                  </div>
                </div>
                
                <!-- 作成ボタン -->
                <div class="flex justify-end">
                  <button 
                    type="submit" 
                    :disabled="!newTodo.title || todosStore.loading"
                    class="px-4 py-2 bg-pink-600 text-white text-sm font-medium rounded-md hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {{ todosStore.loading ? '作成中...' : 'タスクを作成' }}
                  </button>
                </div>
              </form>
            </div>
            <h2 class="text-lg font-medium text-gray-900 mb-4">タスク一覧</h2>
            
            <!-- Todo項目がない場合 -->
            <div v-if="(todosStore.sortedTodos || []).length === 0" class="text-center py-8">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
              <h3 class="mt-2 text-sm font-medium text-gray-900">タスクがありません</h3>
              <p class="mt-1 text-sm text-gray-500">新しいタスクを作成してください。</p>
            </div>

            <!-- Todo項目一覧 -->
            <div v-else class="space-y-4">
              <div v-for="todo in todosStore.sortedTodos || []" :key="todo.id" class="border border-gray-200 rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-sm font-medium text-gray-900">{{ todo.todo_title || 'タイトルなし' }}</h3>
                    <p class="text-sm text-gray-500 mt-1">{{ todo.todo_description || '説明なし' }}</p>
                    <div class="mt-2 flex items-center space-x-4 text-xs text-gray-500">
                      <span>優先度: {{ todo.todo_priority || 'medium' }}</span>
                      <span>重要度: {{ todo.todo_importance || 3 }}</span>
                      <span v-if="todo.todo_due_date">締切: {{ todo.todo_due_date }}</span>
                    </div>
                  </div>
                  <div class="flex items-center">
                    <span :class="todo.todo_status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'" 
                          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {{ todo.todo_status === 'completed' ? '完了' : '未完了' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
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

    <!-- 基本データモーダル -->
    <BasicDataModal v-if="uiStore.showBasicData" />
  </div>
</template>