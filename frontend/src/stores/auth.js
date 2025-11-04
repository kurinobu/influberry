/**
 * 認証ストア (Pinia) - Cookie認証統合
 * InfluBerry v2 - Flask-Login認証サービス
 */

import { defineStore } from 'pinia'
import axios from 'axios'

// Axios基本設定
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5001'
axios.defaults.withCredentials = true // Cookie認証有効化
axios.defaults.headers.common['Content-Type'] = 'application/json'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,
    lastAuthCheck: null,  // 最後に認証状態を確認した時刻（キャッシュ用）
    authCheckCacheTime: 5 * 60 * 1000  // キャッシュ有効期限（5分）
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
          this.lastAuthCheck = Date.now()  // ログイン成功時もキャッシュ時刻を更新
          return { success: true, message: response.data.message }
        }
        
        throw new Error('ログインレスポンスが不正です')
        
      } catch (error) {
        // 429エラー（レート制限）の専用処理
        if (error.response?.status === 429) {
          this.error = 'リクエスト制限に達しました。しばらく待ってから再試行してください。'
          return { success: false, error: this.error, rateLimited: true }
        }
        
        // ネットワークエラーやサーバーエラーの場合は詳細をログに記録
        console.error('ログインエラー詳細:', error.response?.status, error.response?.data, error.message)
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
          this.lastAuthCheck = Date.now()  // 新規登録成功時もキャッシュ時刻を更新
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
        this.lastAuthCheck = null  // ログアウト時はキャッシュをクリア
        return { success: true }
        
      } catch (error) {
        // ログアウトエラーでも状態はクリア
        this.user = null
        this.isAuthenticated = false
        this.lastAuthCheck = null  // ログアウト時はキャッシュをクリア
        console.log('ログアウト完了（認証状態クリア済み）')
        return { success: true }
      } finally {
        this.isLoading = false
      }
    },

    /**
     * 現在のユーザー情報取得（パフォーマンス最適化版）
     */
    async getCurrentUser(forceRefresh = false) {
      // キャッシュチェック: 既に認証状態が確認済みで、キャッシュが有効な場合はスキップ
      if (!forceRefresh && this.lastAuthCheck && this.isAuthenticated && this.user) {
        const now = Date.now()
        const cacheAge = now - this.lastAuthCheck
        
        // キャッシュが有効期限内の場合は、API呼び出しをスキップ
        if (cacheAge < this.authCheckCacheTime) {
          console.log('認証状態キャッシュ使用:', { cacheAge, cacheTime: this.authCheckCacheTime })
          return { success: true, fromCache: true }
        }
      }
      
      this.isLoading = true
      
      try {
        const response = await axios.get('/api/auth/me')
        
        if (response.data.user) {
          this.user = response.data.user
          this.isAuthenticated = true
          this.lastAuthCheck = Date.now()  // キャッシュ時刻を更新
          console.log('認証状態更新完了:', this.isAuthenticated, this.user.email)
          console.log('State check:', this.$state.isAuthenticated, this.$state.user)
          return { success: true }
        }
        
        throw new Error('ユーザー情報の取得に失敗')
        
      } catch (error) {
        this.user = null
        this.isAuthenticated = false
        this.lastAuthCheck = Date.now()  // エラー時もキャッシュ時刻を更新（再試行防止）
        // 401エラーは正常（未認証状態）
        if (error.response?.status !== 401) {
          // ネットワークエラーやサーバーエラーの場合は詳細をログに記録
          console.error('認証エラー詳細:', error.response?.status, error.response?.data, error.message)
          this.error = null // ユーザーにはエラーメッセージを表示しない
        } else {
          this.error = null // 401の場合はエラーメッセージをクリア
        }
        return { success: false }
      } finally {
        this.isLoading = false
      }
    },

    /**
     * 認証状態チェック（アプリ初期化時・パフォーマンス最適化版）
     */
    async checkAuthStatus(forceRefresh = false) {
      // isLoggedIn が null の場合は強制的に確認（初回アクセス時）
      if (this.isLoggedIn === null) {
        return await this.getCurrentUser(true)
      }
      
      // それ以外の場合は、キャッシュを活用
      return await this.getCurrentUser(forceRefresh)
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