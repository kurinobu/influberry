// frontend/src/stores/monthlyRotation.js
/**
 * Monthly Rotation Store
 * 月次自動切り替え管理用 Pinia ストア
 * Step 2 Phase 1: 環境変数による条件付きログ出力
 */

import { defineStore } from 'pinia'
import axios from 'axios'

axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || 'https://influberry.jp'
axios.defaults.withCredentials = true

// Step 2 Phase 1: 環境変数による条件付きログ出力
const isDevelopment = import.meta.env.DEV

// デバッグログ関数（開発環境でのみ出力）
const debugLog = (...args) => {
  if (isDevelopment) {
    debugLog(...args)
  }
}

// エラーログ関数（常に出力）
const errorLog = (...args) => {
  errorLog(...args)
}

export const useMonthlyRotationStore = defineStore('monthlyRotation', {
  state: () => ({
    // スケジューラー状態
    schedulerStatus: null,
    
    // 月次切り替え状態
    lastRotationCheck: null,
    rotationPending: false,
    
    // ローディング状態
    loading: false,
    
    // エラー状態
    error: null,
    
    // 月次切り替え状態管理（新規追加）
    rotationState: 'idle', // 'idle', 'running', 'completed'
    currentMonth: null,
    previousMonth: null,
    
    // 根本原因修正: 重複実行防止のためのフラグ
    monitoringInterval: null,
    refreshing: false
  }),
  
  getters: {
    /**
     * スケジューラーが稼働中かどうか
     */
    isSchedulerRunning: (state) => {
      return state.schedulerStatus?.status === 'running'
    },
    
    /**
     * 月次切り替えが必要かどうか
     */
    needsRotation: (state) => {
      if (!state.lastRotationCheck) return false
      
      const now = new Date()
      const lastCheck = new Date(state.lastRotationCheck)
      const daysDiff = Math.floor((now - lastCheck) / (1000 * 60 * 60 * 24))
      
      // 1日以上経過している場合は切り替えが必要
      return daysDiff >= 1
    }
  },
  
  actions: {
    /**
     * スケジューラー状態を取得
     */
    async fetchSchedulerStatus() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('/api/scheduler/status')
        
        if (response.data.success) {
          this.schedulerStatus = response.data.data
        } else {
          throw new Error(response.data.error || 'スケジューラー状態取得に失敗しました')
        }
      } catch (error) {
        this.error = error.response?.data?.error || error.message
        errorLog('スケジューラー状態取得エラー:', error)
      } finally {
        this.loading = false
      }
    },
    
    /**
     * 手動で月次切り替えを実行
     */
    async triggerManualRotation() {
      this.loading = true
      this.error = null
      
      // 月次切り替え状態を 'running' に設定
      this.setRotationState('running')
      
      try {
        const response = await axios.post('/api/scheduler/trigger-rotation')
        
        if (response.data.success) {
          // 最後のチェック時刻を更新
          this.lastRotationCheck = new Date().toISOString()
          this.rotationPending = false
          
          // 月次切り替え状態を 'completed' に設定
          this.setRotationState('completed')
          
          // フロントエンドデータの更新（修正追加）
          await this.refreshFrontendData()
          
          return true
        } else {
          throw new Error(response.data.error || '月次切り替えの実行に失敗しました')
        }
      } catch (error) {
        this.error = error.response?.data?.error || error.message
        errorLog('手動月次切り替えエラー:', error)
        
        // エラー時は状態を 'idle' に戻す
        this.setRotationState('idle')
        
        return false
      } finally {
        this.loading = false
      }
    },
    
    /**
     * テストスナップショット作成
     */
    async createTestSnapshot(year, month) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('/api/scheduler/test-snapshot', {
          year: year,
          month: month
        })
        
        if (response.data.success) {
          return response.data.data
        } else {
          throw new Error(response.data.error || 'テストスナップショット作成に失敗しました')
        }
      } catch (error) {
        this.error = error.response?.data?.error || error.message
        errorLog('テストスナップショット作成エラー:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    /**
     * 月次切り替えの必要性をチェック
     */
    checkRotationNeeded() {
      const now = new Date()
      const currentMonth = now.getMonth() + 1
      const currentYear = now.getFullYear()
      
      // 月初日かどうかをチェック
      const isFirstDayOfMonth = now.getDate() === 1
      
      if (isFirstDayOfMonth && !this.rotationPending) {
        this.rotationPending = true
        return true
      }
      
      return false
    },
    
    /**
     * 月次切り替えの自動実行
     */
    async autoRotation() {
      if (!this.checkRotationNeeded()) {
        return false
      }
      
      debugLog('月次切り替えが必要です。自動実行を開始します。')
      
      try {
        const success = await this.triggerManualRotation()
        
        if (success) {
          debugLog('月次切り替えが完了しました。')
          // フロントエンドのデータを更新
          await this.refreshFrontendData()
          return true
        } else {
          errorLog('月次切り替えの実行に失敗しました。')
          return false
        }
      } catch (error) {
        errorLog('自動月次切り替えエラー:', error)
        return false
      }
    },
    
    /**
     * フロントエンドデータの更新
     * 修正: データ同期の確実化と重複実行防止
     */
    async refreshFrontendData() {
      try {
        debugLog('🔧 フロントエンドデータの更新を開始')
        
        // 修正: 重複実行防止のためのフラグ
        if (this.refreshing) {
          debugLog('⚠️ 既にデータ更新中です - 重複実行を防止')
          return
        }
        
        this.refreshing = true
        
        // 月次管理ストアのデータを更新
        const { useMonthlyStore } = await import('./monthly.js')
        const monthlyStore = useMonthlyStore()
        
        // 修正: 月次切り替え日時を基準にデータを再取得
        let baseDate
        if (this.lastRotationCheck) {
          baseDate = new Date(this.lastRotationCheck)
          debugLog('🔧 月次切り替え日時を基準にデータ取得:', baseDate)
        } else {
          // 修正: フォールバック時も月次切り替え状態を考慮
          baseDate = new Date()
          debugLog('⚠️ 月次切り替え日時が不明 - 現在の日時を使用:', baseDate)
        }
        
        const currentYear = baseDate.getFullYear()
        const currentMonth = baseDate.getMonth() + 1
        
        // 修正: データ同期の確実化（1回のみ）
        await monthlyStore.fetchStats(currentYear, currentMonth)
        await monthlyStore.fetchTargets(currentYear, [currentMonth])
        
        // タブ再生成はcheckRotationStatusで実行済み（重複削除）
        // await this.triggerTabRegeneration()
        
        debugLog('🔧 フロントエンドデータの更新完了')
      } catch (error) {
        errorLog('❌ フロントエンドデータ更新エラー:', error)
        // 修正: エラーの詳細をログ出力
        if (error.response) {
          errorLog('APIレスポンス:', error.response.data)
          errorLog('HTTPステータス:', error.response.status)
        } else if (error.request) {
          errorLog('リクエストエラー:', error.request)
        } else {
          errorLog('設定エラー:', error.message)
        }
      } finally {
        this.refreshing = false
      }
    },
    
    /**
     * 月次切り替え状態の設定（新規追加）
     */
    setRotationState(state) {
      this.rotationState = state
      
      // 根本原因修正: 月次切り替え状態に基づく適切な日時計算
      let baseDate
      if (this.lastRotationCheck) {
        baseDate = new Date(this.lastRotationCheck)
      } else {
        baseDate = new Date()
      }
      
      this.currentMonth = baseDate.getMonth() + 1
      this.previousMonth = this.currentMonth - 1
      
      debugLog('月次切り替え状態を設定:', {
        state,
        currentMonth: this.currentMonth,
        previousMonth: this.previousMonth
      })
    },
    
    /**
     * タブ再生成のトリガー（新規追加）
     */
    async triggerTabRegeneration() {
      try {
        // 月次切り替えイベントを発火
        const event = new CustomEvent('monthly-rotation-completed', {
          detail: {
            timestamp: new Date().toISOString(),
            message: '月次切り替えが完了しました'
          }
        })
        window.dispatchEvent(event)
        
        debugLog('タブ再生成をトリガーしました。')
      } catch (error) {
        errorLog('タブ再生成トリガーエラー:', error)
      }
    },
    
    /**
     * バックエンドの月次切り替え状態をチェック
     * 修正: エラーハンドリングの強化とレスポンス形式の確認を強化
     */
    async checkRotationStatus() {
      try {
        debugLog('🔍 バックエンドの月次切り替え状態をチェック中...')
        
        const response = await axios.get('/api/scheduler/rotation-status')
        
        // 修正: レスポンス形式の確認を強化
        if (response.data && response.data.success) {
          const data = response.data.data
          debugLog('📊 月次切り替え状態:', data)
          
          // 修正: データの存在確認を強化
          if (data.rotation_completed && data.snapshot_exists && data.last_rotation_date) {
            debugLog('🎉 月次切り替え完了を検知 - タブ更新をトリガー')
            
            // 月次切り替え状態を更新
            this.setRotationState('completed')
            this.lastRotationCheck = data.last_rotation_date
            
            // タブ再生成をトリガー
            await this.triggerTabRegeneration()
            
            // フロントエンドデータを更新
            await this.refreshFrontendData()
            
            return true
          } else {
            debugLog('⏳ 月次切り替え未完了 - 継続監視', {
              rotation_completed: data.rotation_completed,
              snapshot_exists: data.snapshot_exists,
              last_rotation_date: data.last_rotation_date
            })
            return false
          }
        } else {
          errorLog('❌ 月次切り替え状態取得失敗:', response.data?.error || 'Unknown error')
          return false
        }
      } catch (error) {
        errorLog('❌ 月次切り替え状態チェックエラー:', error)
        // 修正: エラーの詳細をログ出力
        if (error.response) {
          errorLog('APIレスポンス:', error.response.data)
          errorLog('HTTPステータス:', error.response.status)
          errorLog('レスポンスヘッダー:', error.response.headers)
        } else if (error.request) {
          errorLog('リクエストエラー:', error.request)
        } else {
          errorLog('設定エラー:', error.message)
        }
        return false
      }
    },
    
    /**
     * 月次切り替えの監視を開始（ポーリング機能付き）
     * 根本原因修正: 重複実行防止とシンプル化
     */
    startRotationMonitoring() {
      debugLog('🔄 月次切り替え監視を開始（ポーリング機能付き）')
      
      // 根本原因修正: 重複実行防止のためのフラグ
      if (this.monitoringInterval) {
        debugLog('⚠️ 既に監視中です - 重複実行を防止')
        return
      }
      
      // 5分ごとにバックエンドの状態をチェック
      this.monitoringInterval = setInterval(async () => {
        debugLog('⏰ 定期チェック: バックエンドの月次切り替え状態を確認')
        await this.checkRotationStatus()
      }, 5 * 60 * 1000) // 5分 = 5 * 60 * 1000ms
      
      // 初回チェックを即座に実行（1秒待機を削除）
      Promise.resolve().then(async () => {
        debugLog('🚀 初回チェック: バックエンドの月次切り替え状態を確認')
        await this.checkRotationStatus()
      })
      
      debugLog('✅ 月次切り替え監視を開始しました（ポーリング機能付き）')
    },
    
    /**
     * エラーをクリア
     */
    clearError() {
      this.error = null
    }
  }
})
