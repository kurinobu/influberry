/**
 * 認証ストア (Pinia) - Cookie認証統合
 * InfluBerry v2 - Flask-Login認証サービス
 */

import { defineStore } from 'pinia'
import axios from 'axios'

// Axios基本設定
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || (import.meta.env.DEV ? '' : 'https://influberry.jp')
axios.defaults.withCredentials = true // Cookie認証有効化
axios.defaults.headers.common['Content-Type'] = 'application/json'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    isLoading: false,
    error: null
  }),

  getters: {
    /**
     * ユーザー認証状態
     */
    isLoggedIn: (state) => state.isAuthenticated && state.user !== null,
    
    /**
     * ユーザー名表示用
     */
    userName: (state) => state.user?.influencer_name || 'ゲスト',
    
    /**
     * ユーザーID取得
     */
    userId: (state) => state.user?.id || null
  },

  actions: {
    /**
     * ログイン処理
     */
    async login(email, password, remember = false) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await axios.post('/api/auth/login', {
          email,
          password,
          remember
        })
        
        if (response.data.user) {
          this.user = response.data.user
          this.isAuthenticated = true
          return { success: true, message: response.data.message }
        }
        
        throw new Error('ログインレスポンスが不正です')
        
      } catch (error) {
        // 429エラー（レート制限）の専用処理
        if (error.response?.status === 429) {
          this.error = 'リクエスト制限に達しました。しばらく待ってから再試行してください。'
          return { success: false, error: this.error, rateLimited: true }
        }
        
        this.error = error.response?.data?.error || 'ログインに失敗しました'
        this.isAuthenticated = false
        this.user = null
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    /**
     * 新規登録処理
     */
    async register(username, email, password) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await axios.post('/api/auth/register', {
          username,
          email,
          password
        })
        
        if (response.data.user) {
          this.user = response.data.user
          this.isAuthenticated = true
          return { success: true, message: response.data.message }
        }
        
        throw new Error('新規登録レスポンスが不正です')
        
      } catch (error) {
        // 429エラー（レート制限）の専用処理
        if (error.response?.status === 429) {
          this.error = 'リクエスト制限に達しました。しばらく待ってから再試行してください。'
          return { success: false, error: this.error, rateLimited: true }
        }
        
        this.error = error.response?.data?.error || '新規登録に失敗しました'
        this.isAuthenticated = false
        this.user = null
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    /**
     * ログアウト処理
     */
    async logout() {
      this.isLoading = true
      
      try {
        await axios.post('/api/auth/logout')
        this.user = null
        this.isAuthenticated = false
        this.error = null
        return { success: true }
        
      } catch (error) {
        // ログアウトエラーでも状態はクリア
        this.user = null
        this.isAuthenticated = false
        console.log('ログアウト完了（認証状態クリア済み）')
        return { success: true }
      } finally {
        this.isLoading = false
      }
    },

    /**
     * 現在のユーザー情報取得
     */
    async getCurrentUser() {
      this.isLoading = true
      this.error = null // 最初にエラーメッセージをクリア
      
      try {
        const response = await axios.get('/api/auth/me')
        
        if (response.data.user) {
          this.user = response.data.user
          this.isAuthenticated = true
          this.error = null // 成功時もエラーメッセージをクリア
          console.log('認証状態更新完了:', this.isAuthenticated, this.user.email)
          console.log('State check:', this.$state.isAuthenticated, this.$state.user)
          return { success: true }
        }
        
        // 未認証状態（userフィールドなし）は正常な状態として扱う
        this.user = null
        this.isAuthenticated = false
        this.error = null // エラーメッセージをクリア
        return { success: false }
        
      } catch (error) {
        this.user = null
        this.isAuthenticated = false
        // 401エラーは正常（未認証状態）
        if (error.response?.status !== 401) {
          this.error = error.response?.data?.error || 'ユーザー情報の取得に失敗しました'
        } else {
          this.error = null // 401の場合はエラーメッセージをクリア
        }
        return { success: false }
      } finally {
        this.isLoading = false
      }
    },

    /**
     * 認証状態チェック（アプリ初期化時）
     */
    async checkAuthStatus() {
      return await this.getCurrentUser()
    },

    /**
     * エラーメッセージクリア
     */
    clearError() {
      this.error = null
    },

    /**
     * ユーザープロフィール更新
     */
    async updateUserProfile(profileData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await axios.put('/api/users/profile', profileData)
        
        if (response.data.user) {
          this.user = response.data.user
          return { success: true, message: response.data.message }
        }
        
        throw new Error('プロフィール更新レスポンスが不正です')
        
      } catch (error) {
        this.error = error.response?.data?.error || 'プロフィール更新に失敗しました'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    /**
     * パスワード変更
     */
    async changePassword(passwordData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await axios.post('/api/users/change-password', passwordData)
        
        return { success: true, message: response.data.message }
        
      } catch (error) {
        this.error = error.response?.data?.error || 'パスワード変更に失敗しました'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },
    /**
     * 支払い情報取得
     */
    async getPaymentInfo() {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await axios.get('/api/users/payment-info')
        
        return { success: true, data: response.data }
        
      } catch (error) {
        this.error = error.response?.data?.error || '支払い情報取得に失敗しました'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    /**
     * 支払い情報更新
     */
    async updatePaymentInfo(paymentData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await axios.put('/api/users/payment-info', paymentData)
        
        return { success: true, message: response.data.message, data: response.data.payment_info }
        
      } catch (error) {
        this.error = error.response?.data?.error || '支払い情報更新に失敗しました'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    }
  }
})

/**
 * Axios インターセプター設定
 * 401エラー時の自動ログアウト処理
 */
export const setupAxiosInterceptors = () => {
  axios.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        const authStore = useAuthStore()
        // 401エラー時は認証状態をクリア
        authStore.isAuthenticated = false
        authStore.user = null
        // エラーメッセージは設定しない（正常な未ログイン状態のため）
      }
      
      // 429エラー（レート制限）の処理
      if (error.response?.status === 429) {
        console.warn('Rate limit reached:', error.response.data)
        // エラーメッセージは各ストアで個別に処理
      }
      
      return Promise.reject(error)
    }
  )
}