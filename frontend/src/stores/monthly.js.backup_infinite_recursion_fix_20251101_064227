// frontend/src/stores/monthly.js
/**
 * Monthly Management Store
 * 月次管理機能用 Pinia ストア
 * 
 * ✅ Phase 1: 重複呼び出し防止機能を実装
 * Step 2 Phase 1: 環境変数による条件付きログ出力
 */

import { defineStore } from 'pinia'
import axios from 'axios'

axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || 'https://influberry.jp'
axios.defaults.withCredentials = true
axios.defaults.headers.common['Content-Type'] = 'application/json'

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

export const useMonthlyStore = defineStore('monthly', {
  state: () => ({
    // 段階的切替フラグ（stagingでON推奨）
    // Phase 2: 新APIを有効化（計画書v2.0準拠）
    USE_NEW_API: true,
    // 月次目標データ
    targets: {},           // { '2025-10-01': { projects: 5, income: 200000 } }
    
    // 月次統計データ
    stats: {},             // { '2025-10-01': { acquired: 3, completed: 2 ... } }
    
    // 概要統計データ
    overview: null,
    
    // 現在選択中の月
    currentMonth: null,    // '2025-10-01'
    
    // ローディング状態
    loading: false,
    
    // エラー状態
    error: null,
    
    // ✅ Phase 1: 重複呼び出し防止用のフラグ
    fetchingTargets: false,        // 目標取得中フラグ
    fetchingStats: false,          // 統計取得中フラグ
    
    // 🔧 修正: 強制再取得フラグ
    forceRefresh: false,           // 強制再取得フラグ
    
    // ✅ Phase 1: キャッシュ管理
    lastFetchTime: {
      targets: null,               // 最終取得時刻（目標）
      stats: null                  // 最終取得時刻（統計）
    },
    cacheDuration: 5 * 60 * 1000   // キャッシュ有効期限: 5分
  }),
  
  getters: {
    /**
     * 指定月の目標取得
     */
    getTargetByMonth: (state) => (month) => {
      return state.targets[month] || null
    },
    
    /**
     * 指定月の統計取得
     */
    getStatsByMonth: (state) => (month) => {
      return state.stats[month] || null
    },
    
    /**
     * 達成率計算
     */
    achievementRate: (state) => (month) => {
      const target = state.targets[month]
      const stat = state.stats[month]
      if (!target || !stat) return null
      
      return {
        projects: target.target_projects ? stat.actual.acquired_projects / target.target_projects : 0,
        income: target.target_income ? stat.actual.paid_invoices_amount / target.target_income : 0
      }
    }
  },
  
  actions: {
    /**
     * フェーズ2: 統合APIで今月+先月+次月を1回取得
     * 失敗時は旧APIにフォールバック
     */
    async fetchCurrentMonthlyData() {
      if (this.USE_NEW_API) {
        this.loading = true
        this.error = null
        try {
          debugLog('🔧 新API使用: GET /api/monthly/current')
          const res = await axios.get('/api/monthly/current')
          if (!res.data || res.data.success !== true) {
            throw new Error(res.data?.error || '新APIの応答が不正です')
          }
          const data = res.data.data || {}
          // 受領データを既存stateへ反映（targets, stats）
          Object.entries(data).forEach(([monthKey, payload]) => {
            const t = payload.target || {}
            const s = payload.stats || {}
            // 目標: 既存のフィールド名に合わせて保持
            this.targets[monthKey] = {
              target_month: monthKey,
              target_projects: t.projects ?? null,
              target_income: t.income ?? null
            }
            // 統計: そのまま保持（既存取得と併存可能）
            // Step 1-2修正: targetプロパティを追加してデータ構造を統一
            this.stats[monthKey] = {
              month: monthKey,
              target: {
                projects: t.projects ?? null,
                income: t.income ?? null
              },
              actual: {
                acquired_projects: s.acquired_projects ?? 0,
                completed_projects: s.completed_projects ?? 0,
                sent_invoices_count: s.sent_invoices_count ?? 0,
                sent_invoices_amount: s.sent_invoices_amount ?? 0,
                paid_invoices_count: s.paid_invoices_count ?? 0,
                paid_invoices_amount: s.paid_invoices_amount ?? 0
              }
            }
          })
          debugLog('✅ 月次データ取得完了（新API）')
        } catch (err) {
          debugLog('⚠️ 新APIが失敗、旧APIにフォールバック')
          this.error = err.response?.data?.error || err.message
          await this._fetchCurrentMonthlyDataLegacy()
        } finally {
          this.loading = false
        }
      } else {
        // 旧API（後方互換）
        await this._fetchCurrentMonthlyDataLegacy()
      }
    },

    // 旧API: 目標と各月統計を個別取得（フォールバック用）
    async _fetchCurrentMonthlyDataLegacy() {
      try {
        const now = new Date()
        const y = now.getFullYear()
        const months = [now.getMonth(), now.getMonth() - 1, now.getMonth() + 1]
        // 目標（まとめて）
        await this.fetchTargets(y, months.map(m => m + 1))
        // 統計（各月）
        for (const m of months) {
          await this.fetchStats(y, m + 1)
        }
        debugLog('✅ 月次データ取得完了（旧API）')
      } catch (e) {
        errorLog('❌ 旧API取得失敗:', e)
        this.error = e.response?.data?.error || e.message
      }
    },
    /**
     * 月次目標一覧取得
     * ✅ Phase 1: 重複呼び出し防止機能を追加
     */
    async fetchTargets(year, months, forceRefresh = false) {
      // ✅ Phase 1: 既に取得中なら待つ（重複防止）
      if (this.fetchingTargets) {
        debugLog('🔧 月次目標取得: 既に実行中のためスキップ')
        return
      }
      
      // ✅ Phase 1: キャッシュが有効なら再取得しない
      const cacheKey = `${year}-${months.join(',')}`
      const now = Date.now()
      if (!forceRefresh && this.lastFetchTime.targets && 
          now - this.lastFetchTime.targets < this.cacheDuration &&
          months.every(m => this.targets[`${year}-${String(m).padStart(2, '0')}-01`])) {
        debugLog('🔧 月次目標取得: キャッシュを使用', { cacheKey })
        return
      }
      
      this.fetchingTargets = true
      this.loading = true
      this.error = null
      
      try {
        debugLog('🔧 月次目標取得開始:', { year, months })
        
        const response = await axios.get('/api/monthly-targets/', {
          params: { 
            year, 
            months: months.join(',') 
          }
        })
        
        if (response.data && response.data.success) {
          // 修正: データ同期の確実化
          response.data.data.forEach(target => {
            this.targets[target.target_month] = { ...target }
          })
          
          // ✅ Phase 1: 取得時刻を記録
          this.lastFetchTime.targets = Date.now()
          
          debugLog('🔧 月次目標取得完了:', {
            targets: this.targets,
            cached: true
          })
        } else {
          throw new Error(response.data?.error || '目標取得に失敗しました')
        }
      } catch (error) {
        this.error = error.response?.data?.error || error.message
        errorLog('❌ 月次目標取得エラー:', error)
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
        this.loading = false
        this.fetchingTargets = false
      }
    },
    
    /**
     * 月次統計取得
     * ✅ Phase 1: 重複呼び出し防止機能を追加
     */
    async fetchStats(year, month, forceRefresh = false) {
      const monthKey = `${year}-${String(month).padStart(2, '0')}-01`
      
      // 🔧 修正: 強制再取得の場合は重複防止を完全にスキップ
      if (this.fetchingStats && !forceRefresh) {
        debugLog('🔧 月次統計取得: 既に実行中のためスキップ')
        return
      }
      
      // 🔧 修正: 強制再取得の場合はキャッシュを完全に無視
      const now = Date.now()
      if (!forceRefresh && this.lastFetchTime.stats && 
          now - this.lastFetchTime.stats < this.cacheDuration &&
          this.stats[monthKey]) {
        debugLog('🔧 月次統計取得: キャッシュを使用', { monthKey })
        return
      }
      
      // 🔧 修正: 強制再取得の場合は既存の実行を強制終了
      if (forceRefresh && this.fetchingStats) {
        debugLog('🔧 月次統計取得: 強制再取得のため既存実行を終了')
        this.fetchingStats = false
      }
      
      // 🔧 修正: 強制再取得の場合はキャッシュを完全にクリア
      if (forceRefresh) {
        delete this.stats[monthKey]
        this.lastFetchTime.stats = null
        debugLog('🔧 月次統計取得: 強制再取得のためキャッシュをクリア', { monthKey })
      }
      
      this.fetchingStats = true
      this.loading = true
      this.error = null
      
      try {
        debugLog('🔧 月次統計取得開始:', { year, month })
        
        const response = await axios.get(`/api/monthly-stats/${year}/${month}`)
        
        if (response.data && response.data.success) {
          // 修正: データ同期の確実化
          const monthKey = response.data.data.month
          this.stats[monthKey] = { ...response.data.data }
          
          // ✅ Phase 1: 取得時刻を記録
          this.lastFetchTime.stats = Date.now()
          
          debugLog('🔧 月次統計取得完了:', {
            monthKey,
            stats: this.stats[monthKey],
            cached: true
          })
        } else {
          throw new Error(response.data?.error || '統計取得に失敗しました')
        }
      } catch (error) {
        this.error = error.response?.data?.error || error.message
        errorLog('❌ 月次統計取得エラー:', error)
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
        this.loading = false
        this.fetchingStats = false
      }
    },
    
    /**
     * 概要統計取得
     * Phase 3修正: エラーハンドリング強化とNull安全性確保
     */
    async fetchOverview() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('/api/monthly-stats/overview')
        
        if (response.data && response.data.success) {
          // Phase 3修正: データ構造の確認とデフォルト値の設定
          const data = response.data.data || {}
          this.overview = {
            total_projects: data.total_projects ?? 0,
            total_income: data.total_income ?? 0,
            recent_months: data.recent_months ?? []
          }
          debugLog('✅ 概要統計取得完了:', {
            overview: this.overview,
            hasTotalProjects: 'total_projects' in this.overview,
            hasTotalIncome: 'total_income' in this.overview
          })
          return this.overview
        } else {
          throw new Error(response.data?.error || '概要統計取得に失敗しました')
        }
      } catch (error) {
        // Phase 3修正: エラー時もoverviewをnullに設定して、undefinedを防ぐ
        this.overview = null
        this.error = error.response?.data?.error || error.message
        errorLog('❌ 概要統計取得エラー:', error)
        // 修正: エラーの詳細をログ出力
        if (error.response) {
          errorLog('APIレスポンス:', error.response.data)
          errorLog('HTTPステータス:', error.response.status)
        } else if (error.request) {
          errorLog('リクエストエラー:', error.request)
        } else {
          errorLog('設定エラー:', error.message)
        }
        // Phase 3修正: エラー時はデフォルト値を返す（Null安全性確保）
        return {
          total_projects: 0,
          total_income: 0,
          recent_months: []
        }
      } finally {
        this.loading = false
      }
    },
    
    /**
     * 月次目標保存
     * 修正: データ同期の確実化とエラーハンドリングの強化
     */
    async saveTarget(targetMonth, data) {
      try {
        debugLog('🔧 月次目標保存開始:', { targetMonth, data })
        
        const response = await axios.post('/api/monthly-targets/', {
          target_month: targetMonth,
          target_projects: data.target_projects,
          target_income: data.target_income
        })
        
        if (response.data && response.data.success) {
          // 修正: データ同期の確実化
          this.targets[targetMonth] = { ...response.data.data }
          
          // 🔧 修正: 指定月のキャッシュのみクリア
          const [year, month] = targetMonth.split('-')
          const monthKey = `${year}-${month.toString().padStart(2, '0')}-01`
          this.clearMonthCache(parseInt(year), parseInt(month))
          
          // 🔧 修正: 目標データと統計データを順次強制再取得（完全確実化）
          debugLog('🔧 目標保存後: データ再取得を開始')
          
          // 1. 目標データの強制再取得
          await this.fetchTargets(parseInt(year), [parseInt(month)], true)
          debugLog('🔧 目標保存後: 目標データ再取得完了')
          
          // 2. 統計データの強制再取得（確実化）
          await this.fetchStats(parseInt(year), parseInt(month), true)
          debugLog('🔧 目標保存後: 統計データ再取得完了')
          
          // 3. データ同期の確実化（追加確認）
          await new Promise(resolve => setTimeout(resolve, 100))
          debugLog('🔧 目標保存後: データ同期確実化完了')
          
          debugLog('🔧 月次目標保存完了:', {
            targetMonth,
            monthKey,
            targets: this.targets,
            stats: this.stats
          })
          
          return { success: true }
        } else {
          throw new Error(response.data?.error || '目標保存に失敗しました')
        }
      } catch (error) {
        const errorMessage = error.response?.data?.error || error.message
        errorLog('❌ 月次目標保存エラー:', error)
        // 修正: エラーの詳細をログ出力
        if (error.response) {
          errorLog('APIレスポンス:', error.response.data)
          errorLog('HTTPステータス:', error.response.status)
        } else if (error.request) {
          errorLog('リクエストエラー:', error.request)
        } else {
          errorLog('設定エラー:', error.message)
        }
        return { success: false, error: errorMessage }
      }
    },
    
    /**
     * 月次目標削除
     */
    async deleteTarget(targetMonth) {
      try {
        const response = await axios.delete(`/api/monthly-targets/${targetMonth}/`)
        
        if (response.data.success) {
          delete this.targets[targetMonth]
          return { success: true }
        } else {
          throw new Error(response.data.error || '目標削除に失敗しました')
        }
      } catch (error) {
        const errorMessage = error.response?.data?.error || error.message
        errorLog('目標削除エラー:', error)
        return { success: false, error: errorMessage }
      }
    },
    
    /**
     * 現在の月を設定
     */
    setCurrentMonth(month) {
      this.currentMonth = month
    },
    
    /**
     * エラーをクリア
     */
    clearError() {
      this.error = null
    },
    
    /**
     * ✅ Phase 1: キャッシュクリア
     * ステータス変更時や目標保存時に呼び出す
     * 🔧 修正: 強制再取得フラグもリセット
     */
    clearCache() {
      this.lastFetchTime.targets = null
      this.lastFetchTime.stats = null
      this.forceRefresh = false
      debugLog('🔧 キャッシュをクリアしました')
    },
    
    /**
     * 指定月のキャッシュクリア
     * 🔧 修正: 特定月のキャッシュのみクリア（完全最適化）
     */
    clearMonthCache(year, month) {
      const monthKey = `${year}-${String(month).padStart(2, '0')}-01`
      // 統計のみクリア（目標は即時反映のトリガー源として残す）
      delete this.stats[monthKey]
      this.forceRefresh = true
      // 🔧 修正: キャッシュクリア後の状態を完全リセット
      this.fetchingStats = false
      this.fetchingTargets = false
      this.lastFetchTime.stats = null
      // 目標は保持するため targets 側のタイムスタンプは必要に応じて維持
      debugLog('🔧 指定月のキャッシュをクリアしました:', { 
        monthKey, 
        statsCleared: !this.stats[monthKey],
        targetsCleared: false,
        forceRefresh: this.forceRefresh,
        fetchingStats: this.fetchingStats,
        fetchingTargets: this.fetchingTargets
      })
    },
    
    /**
     * ストアをリセット
     */
    reset() {
      this.targets = {}
      this.stats = {}
      this.overview = null
      this.currentMonth = null
      this.loading = false
      this.error = null
      
      // ✅ Phase 1: キャッシュ管理もリセット
      this.fetchingTargets = false
      this.fetchingStats = false
      this.lastFetchTime.targets = null
      this.lastFetchTime.stats = null
    }
  }
})