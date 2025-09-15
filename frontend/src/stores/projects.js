// /Users/kurinobu/projects/influberry_v2/frontend/src/stores/projects.js
// Project管理ストア - Pinia状態管理・CRUD操作・認証統合

import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth.js'

// Axios設定（auth.jsと同一設定）
axios.defaults.baseURL = 'https://influberry.jp'
axios.defaults.withCredentials = true
axios.defaults.headers.common['Content-Type'] = 'application/json'

export const useProjectsStore = defineStore('projects', {
  state: () => ({
    // プロジェクト一覧
    projects: [],
    
    // 現在選択中のプロジェクト
    currentProject: null,
    
    // ローディング状態
    isLoading: false,
    
    // エラー状態
    error: null,
    
    // ページネーション
    pagination: {
      current_page: 1,
      total_pages: 1,
      total_count: 0,
      per_page: 10
    },
    
    // フィルター・検索
    filters: {
      status: '',
      search: '',
      sort_by: 'created_at',
      order: 'desc'
    }
  }),

  getters: {
    // ステータス別プロジェクト数
    projectsByStatus: (state) => {
      return (status) => state.projects.filter(project => project.status === status)
    },
    
    // 合計金額
    totalAmount: (state) => {
      return state.projects.reduce((sum, project) => sum + (project.amount || 0), 0)
    },
    
    // 完了プロジェクト数
    completedCount: (state) => {
      return state.projects.filter(project => project.status === 'completed').length
    },
    
    // 進行中プロジェクト数
    activeCount: (state) => {
      return state.projects.filter(project => 
        project.status === 'proposed' || project.status === 'contracted'
      ).length
    },
    // === 統計システム統一：追加統計getter ===
    // 提案中プロジェクト数
    proposedCount: (state) => {
      return state.projects.filter(project => project.status === 'proposed').length
    },
    
    // 契約中プロジェクト数
    contractedCount: (state) => {
      return state.projects.filter(project => project.status === 'contracted').length
    },
    
    // 統一「進行中案件」数（proposed + contracted）
    pendingProjectsCount: (state) => {
      return state.projects.filter(project => 
        project.status === 'proposed' || project.status === 'contracted'
      ).length
    },
    
    // 総案件数
    totalProjectsCount: (state) => {
      return state.projects.length
    }
  },

  actions: {
    // プロジェクト一覧取得
    async fetchProjects(params = {}) {
      this.isLoading = true
      this.error = null
      
      try {
        const authStore = useAuthStore()
        
        // 認証チェック
        if (!authStore.isLoggedIn) {
          throw new Error('認証が必要です')
        }

        // APIパラメータ構築
        const queryParams = {
          page: this.pagination.current_page,
          per_page: this.pagination.per_page,
          ...this.filters,
          ...params
        }

        const response = await axios.get('/api/projects', {
          params: queryParams,
          withCredentials: true
        })

        if (response.status === 200) {
          this.projects = response.data.projects || []
          
          // ページネーション情報更新
          if (response.data.pagination) {
            this.pagination = {
              ...this.pagination,
              ...response.data.pagination
            }
          }
          
          return { success: true, data: response.data }
        }
      } catch (error) {
        console.error('プロジェクト取得エラー:', error)
        this.error = error.response?.data?.message || error.message || 'プロジェクトの取得に失敗しました'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    // プロジェクト詳細取得
    async fetchProject(projectId) {
      this.isLoading = true
      this.error = null

      try {
        const authStore = useAuthStore()
        
        if (!authStore.isLoggedIn) {
          throw new Error('認証が必要です')
        }

        const response = await axios.get(`/api/projects/${projectId}`, {
          withCredentials: true
        })

        if (response.status === 200) {
          this.currentProject = response.data.project
          return { success: true, data: response.data.project }
        }
      } catch (error) {
        console.error('プロジェクト詳細取得エラー:', error)
        this.error = error.response?.data?.message || error.message || 'プロジェクトの詳細取得に失敗しました'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    // プロジェクト作成
    async createProject(projectData) {
      this.isLoading = true
      this.error = null

      try {
        const authStore = useAuthStore()
        
        if (!authStore.isLoggedIn) {
          throw new Error('認証が必要です')
        }

        const response = await axios.post('/api/projects', projectData, {
          withCredentials: true,
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (response.status === 201) {
          // 一覧を再取得してリストを更新
          await this.fetchProjects()
          return { success: true, data: response.data.project }
        }
      } catch (error) {
        console.error('プロジェクト作成エラー:', error)
        this.error = error.response?.data?.message || error.message || 'プロジェクトの作成に失敗しました'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    // プロジェクト更新
    async updateProject(projectId, projectData) {
      this.isLoading = true
      this.error = null

      try {
        const authStore = useAuthStore()
        
        if (!authStore.isLoggedIn) {
          throw new Error('認証が必要です')
        }

        const response = await axios.put(`/api/projects/${projectId}`, projectData, {
          withCredentials: true,
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (response.status === 200) {
          // 一覧を再取得してリストを更新
          await this.fetchProjects()
          this.currentProject = response.data.project
          return { success: true, data: response.data.project }
        }
      } catch (error) {
        console.error('プロジェクト更新エラー:', error)
        this.error = error.response?.data?.message || error.message || 'プロジェクトの更新に失敗しました'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    // プロジェクト削除
    async deleteProject(projectId) {
      this.isLoading = true
      this.error = null

      try {
        const authStore = useAuthStore()
        
        if (!authStore.isLoggedIn) {
          throw new Error('認証が必要です')
        }

        const response = await axios.delete(`/api/projects/${projectId}`, {
          withCredentials: true
        })

        if (response.status === 200 || response.status === 204) {
          // 一覧を再取得してリストを更新
          await this.fetchProjects()
          
          // 現在選択中のプロジェクトをクリア
          if (this.currentProject?.id === projectId) {
            this.currentProject = null
          }
          
          return { success: true }
        }
      } catch (error) {
        console.error('プロジェクト削除エラー:', error)
        this.error = error.response?.data?.message || error.message || 'プロジェクトの削除に失敗しました'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    // フィルター更新
    updateFilters(newFilters) {
      this.filters = { ...this.filters, ...newFilters }
      this.pagination.current_page = 1 // ページをリセット
    },

    // ページ変更
    changePage(page) {
      this.pagination.current_page = page
    },

    // 検索実行
    async search(searchTerm) {
      this.filters.search = searchTerm
      this.pagination.current_page = 1
      return await this.fetchProjects()
    },

    // ステータス別フィルター
    async filterByStatus(status) {
      this.filters.status = status
      this.pagination.current_page = 1
      return await this.fetchProjects()
    },

    // ソート変更
    async changeSort(sortBy, order = 'desc') {
      this.filters.sort_by = sortBy
      this.filters.order = order
      this.pagination.current_page = 1
      return await this.fetchProjects()
    },

    // エラークリア
    clearError() {
      this.error = null
    },

    // ストアリセット
    resetStore() {
      this.projects = []
      this.currentProject = null
      this.isLoading = false
      this.error = null
      this.pagination = {
        current_page: 1,
        total_pages: 1,
        total_count: 0,
        per_page: 10
      }
      this.filters = {
        status: '',
        search: '',
        sort_by: 'created_at',
        order: 'desc'
      }
    }
  }
})