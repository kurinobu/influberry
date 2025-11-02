// frontend/src/stores/monthlyRotation.js
/**
 * Monthly Rotation Store
 * 月次自動切り替え管理用 Pinia ストア
 */

import { defineStore } from 'pinia'
import axios from 'axios'

axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || 'https://influberry.jp'
axios.defaults.withCredentials = true

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
    previousMonth: null
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
        console.error('スケジューラー状態取得エラー:', error)
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
        console.error('手動月次切り替えエラー:', error)
        
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
        console.error('テストスナップショット作成エラー:', error)
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
      
      console.log('月次切り替えが必要です。自動実行を開始します。')
      
      try {
        const success = await this.triggerManualRotation()
        
        if (success) {
          console.log('月次切り替えが完了しました。')
          // フロントエンドのデータを更新
          await this.refreshFrontendData()
          return true
        } else {
          console.error('月次切り替えの実行に失敗しました。')
          return false
        }
      } catch (error) {
        console.error('自動月次切り替えエラー:', error)
        return false
      }
    },
    
    /**
     * フロントエンドデータの更新
     * 根本原因修正: データ同期の確実化
     */
    async refreshFrontendData() {
      try {
        console.log('🔧 根本原因修正: フロントエンドデータの更新を開始')
        
        // 月次管理ストアのデータを更新
        const { useMonthlyStore } = await import('./monthly.js')
        const monthlyStore = useMonthlyStore()
        
        // 根本原因修正: 月次切り替え日時を基準にデータを再取得
        let baseDate
        if (this.lastRotationCheck) {
          baseDate = new Date(this.lastRotationCheck)
          console.log('🔧 月次切り替え日時を基準にデータ取得:', baseDate)
        } else {
          // 根本原因修正: フォールバック時も月次切り替え状態を考慮
          baseDate = new Date()
          console.log('⚠️ 月次切り替え日時が不明 - 現在の日時を使用:', baseDate)
        }
        
        const currentYear = baseDate.getFullYear()
        const currentMonth = baseDate.getMonth() + 1
        
        // 根本原因修正: データ同期の確実化
        await monthlyStore.fetchStats(currentYear, currentMonth)
        await monthlyStore.fetchTargets(currentYear, [currentMonth])
        
        // タブ再生成のトリガー
        await this.triggerTabRegeneration()
        
        console.log('🔧 根本原因修正: フロントエンドデータの更新完了')
      } catch (error) {
        console.error('❌ フロントエンドデータ更新エラー:', error)
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
      
      console.log('月次切り替え状態を設定:', {
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
        
        console.log('タブ再生成をトリガーしました。')
      } catch (error) {
        console.error('タブ再生成トリガーエラー:', error)
      }
    },
    
    /**
     * 月次切り替えの監視を開始
     */
    startRotationMonitoring() {
      // 5分ごとにチェック
      setInterval(() => {
        this.autoRotation()
      }, 5 * 60 * 1000) // 5分 = 5 * 60 * 1000ms
      
      console.log('月次切り替え監視を開始しました。')
    },
    
    /**
     * エラーをクリア
     */
    clearError() {
      this.error = null
    }
  }
})
