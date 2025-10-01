// /Users/kurinobu/projects/influberry_v2/frontend/src/stores/todos.js
// Todo管理ストア - Pinia状態管理・CRUD操作・認証統合・緊急度×重要度マトリックス

import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth.js'

// Axios設定（projects.js完全統一）
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || 'https://influberry.jp'
axios.defaults.withCredentials = true
axios.defaults.headers.common['Content-Type'] = 'application/json'

export const useTodosStore = defineStore('todos', {
  state: () => ({
    // Todo一覧
    todos: [],
    
    // 現在選択中のTodo
    currentTodo: null,
    
    // 読み込み状態
    loading: false,
    
    // エラー状態
    error: null,
    
    // 統計データ
    stats: {
      pending_todos: 0,
      upcoming_todos: 0
    },
    
    // 連動データ（ProjectApp・InvoiceApp選択肢）
    projectOptions: [],
    invoiceOptions: []
  }),

  getters: {
    // 緊急度×重要度マトリックス（4段階ソート）
    sortedTodos: (state) => {
      return [...(state.todos || [])].sort((a, b) => {
        // Priority値の変換（high=3, medium=2, low=1）
        const getPriorityValue = (priority) => {
          switch(priority) {
            case 'high': return 3
            case 'medium': return 2  
            case 'low': return 1
            default: return 2
          }
        }
        
        const aPriority = getPriorityValue(a.todo_priority)
        const bPriority = getPriorityValue(b.todo_priority)
        const aImportance = a.todo_importance || 3
        const bImportance = b.todo_importance || 3
        
        // 緊急度×重要度マトリックス計算
        const aScore = aPriority * aImportance
        const bScore = bPriority * bImportance
        
        // 降順ソート（高スコア優先）
        return bScore - aScore
      })
    },
    
    // ステータス別フィルター
    pendingTodos: (state) => (state.todos || []).filter(todo => todo.todo_status === 'pending'),
    completedTodos: (state) => (state.todos || []).filter(todo => todo.todo_status === 'completed'),
    
    // 優先度別カウント
    highPriorityTodos: (state) => (state.todos || []).filter(todo => todo.todo_priority === 'high'),
    
    // 期限間近Todos（3日以内）
    upcomingTodos: (state) => {
      const today = new Date()
      const threeDaysLater = new Date(today.getTime() + (3 * 24 * 60 * 60 * 1000))
      
      return (state.todos || []).filter(todo => {
        if (!todo.todo_due_date) return false
        const dueDate = new Date(todo.todo_due_date)
        return dueDate >= today && dueDate <= threeDaysLater && todo.todo_status === 'pending'
      })
    }
  },

  actions: {
    // Todo一覧取得
    async fetchTodos() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('/api/todos/')
        this.todos = response.data.todos || []
        
        // 統計データ同時取得
        await this.fetchStats()
        
      } catch (error) {
        console.error('Todo一覧取得エラー:', error)
        this.error = 'Todo一覧の取得に失敗しました'
        
        if (error.response?.status === 401) {
          const authStore = useAuthStore()
          await authStore.logout()
        }
      } finally {
        this.loading = false
      }
    },

    // Todo統計取得
    async fetchStats() {
      try {
        const response = await axios.get('/api/todos/stats')
        this.stats = response.data || { pending_todos: 0, upcoming_todos: 0 }
      } catch (error) {
        console.error('Todo統計取得エラー:', error)
        this.stats = { pending_todos: 0, upcoming_todos: 0 }
      }
    },

    // Todo作成
    async createTodo(todoData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('/api/todos/', todoData)
        const newTodo = response.data
        
        this.todos.push(newTodo)
        await this.fetchStats()
        
        return newTodo
        
      } catch (error) {
        console.error('Todo作成エラー:', error)
        this.error = error.response?.data?.error || 'Todoの作成に失敗しました'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Todo更新
    async updateTodo(todoId, todoData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.put(`/api/todos/${todoId}`, todoData)
        const updatedTodo = response.data
        
        // ローカル状態更新
        const index = this.todos.findIndex(todo => todo.id === todoId)
        if (index !== -1) {
          this.todos[index] = updatedTodo
        }
        
        await this.fetchStats()
        
        return updatedTodo
        
      } catch (error) {
        console.error('Todo更新エラー:', error)
        this.error = error.response?.data?.error || 'Todoの更新に失敗しました'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Todo完了
    async completeTodo(todoId) {
      try {
        const response = await axios.put(`/api/todos/${todoId}/complete`)
        const completedTodo = response.data
        
        // ローカル状態更新
        const index = this.todos.findIndex(todo => todo.id === todoId)
        if (index !== -1) {
          this.todos[index] = completedTodo
        }
        
        await this.fetchStats()
        
        return completedTodo
        
      } catch (error) {
        console.error('Todo完了エラー:', error)
        this.error = error.response?.data?.error || 'Todoの完了に失敗しました'
        throw error
      }
    },

    // Todo削除
    async deleteTodo(todoId) {
      this.loading = true
      this.error = null
      
      try {
        await axios.delete(`/api/todos/${todoId}`)
        
        // ローカル状態更新
        this.todos = this.todos.filter(todo => todo.id !== todoId)
        await this.fetchStats()
        
      } catch (error) {
        console.error('Todo削除エラー:', error)
        this.error = error.response?.data?.error || 'Todoの削除に失敗しました'
        throw error
      } finally {
        this.loading = false
      }
    },

    // ProjectApp連動選択肢取得
    async fetchProjectOptions() {
      try {
        const response = await axios.get('/api/projects/options')
        this.projectOptions = response.data || []
      } catch (error) {
        console.error('プロジェクト選択肢取得エラー:', error)
        this.projectOptions = []
      }
    },

    // InvoiceApp連動選択肢取得
    async fetchInvoiceOptions() {
      try {
        const response = await axios.get('/api/invoices/options')
        this.invoiceOptions = response.data || []
      } catch (error) {
        console.error('請求書選択肢取得エラー:', error)
        this.invoiceOptions = []
      }
    },

    // 現在のTodo設定
    setCurrentTodo(todo) {
      this.currentTodo = todo
    },

    // エラークリア
    clearError() {
      this.error = null
    },

    // 状態リセット
    resetState() {
      this.todos = []
      this.currentTodo = null
      this.loading = false
      this.error = null
      this.stats = { pending_todos: 0, upcoming_todos: 0 }
      this.projectOptions = []
      this.invoiceOptions = []
    }
  }
})