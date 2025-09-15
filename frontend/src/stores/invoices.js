// src/stores/invoices.js
/**
 * InfluBerry Invoice ストア
 * 自動請求書発行システム用 Pinia ストア
 * Phase2: Invoice API統合・UI実装
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from './auth'

axios.defaults.baseURL = 'https://influberry.jp'

export const useInvoicesStore = defineStore('invoices', () => {
  // State
  const invoices = ref([])
  const currentInvoice = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    page: 1,
    pages: 0,
    per_page: 10,
    total: 0,
    has_next: false,
    has_prev: false
  })

  // Computed
  const totalInvoices = computed(() => pagination.value.total)
  const hasInvoices = computed(() => invoices.value.length > 0)
  
  // ステータス別統計
  const invoiceStats = computed(() => {
    const stats = {
      draft: 0,
      sent: 0,
      paid: 0,
      overdue: 0,
      cancelled: 0,
      total_amount: 0,
      paid_amount: 0
    }
    
    invoices.value.forEach(invoice => {
      stats[invoice.status] = (stats[invoice.status] || 0) + 1
      stats.total_amount += parseFloat(invoice.total_amount || 0)
      if (invoice.status === 'paid') {
        stats.paid_amount += parseFloat(invoice.total_amount || 0)
      }
    })
    
    return stats
  })

  // Actions
  
  /**
   * 請求書一覧取得
   */
  const fetchInvoices = async (page = 1, per_page = 10) => {
    const authStore = useAuthStore()
    if (!authStore.isAuthenticated) {
      error.value = '認証が必要です'
      return false
    }

    loading.value = true
    error.value = null

    try {
      const response = await axios.get('/api/invoices/', {
        params: { page, per_page },
        withCredentials: true
      })

      if (response.data.success) {
        invoices.value = response.data.invoices || []
        pagination.value = response.data.pagination || {}
        return true
      } else {
        error.value = response.data.error || '請求書一覧の取得に失敗しました'
        return false
      }
    } catch (err) {
      console.error('Invoice fetch error:', err)
      error.value = err.response?.data?.message || err.response?.data?.error || 'ネットワークエラーが発生しました'
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 請求書詳細取得
   */
  const fetchInvoice = async (invoiceId) => {
    const authStore = useAuthStore()
    if (!authStore.isAuthenticated) {
      error.value = '認証が必要です'
      return false
    }

    loading.value = true
    error.value = null

    try {
      const response = await axios.get(`/api/invoices/${invoiceId}`, {
        withCredentials: true
      })

      if (response.data.success) {
        currentInvoice.value = response.data.invoice
        return true
      } else {
        error.value = response.data.error || '請求書の取得に失敗しました'
        return false
      }
    } catch (err) {
      console.error('Invoice detail fetch error:', err)
      error.value = err.response?.data?.message || err.response?.data?.error || 'ネットワークエラーが発生しました'
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * プロジェクトから請求書自動生成
   */
  const createInvoiceFromProject = async (projectId) => {
    const authStore = useAuthStore()
    if (!authStore.isAuthenticated) {
      error.value = '認証が必要です'
      return false
    }

    loading.value = true
    error.value = null

    try {
      const response = await axios.post(`/api/invoices/create-from-project/${projectId}`, {}, {
        withCredentials: true
      })

      if (response.data.success) {
        const newInvoice = response.data.invoice
        // 一覧に新しい請求書を追加
        invoices.value.unshift(newInvoice)
        pagination.value.total += 1
        currentInvoice.value = newInvoice
        return newInvoice
      } else {
        error.value = response.data.error || '請求書の作成に失敗しました'
        return false
      }
    } catch (err) {
      console.error('Invoice creation error:', err)
      error.value = err.response?.data?.message || err.response?.data?.error || 'ネットワークエラーが発生しました'
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 手動請求書作成
   */
  const createInvoice = async (invoiceData) => {
    const authStore = useAuthStore()
    if (!authStore.isAuthenticated) {
      error.value = '認証が必要です'
      return false
    }

    loading.value = true
    error.value = null

    try {
      const response = await axios.post('/api/invoices/', invoiceData, {
        withCredentials: true
      })

      if (response.data.success) {
        const newInvoice = response.data.invoice
        invoices.value.unshift(newInvoice)
        pagination.value.total += 1
        currentInvoice.value = newInvoice
        return newInvoice
      } else {
        error.value = response.data.error || '請求書の作成に失敗しました'
        return false
      }
    } catch (err) {
      console.error('Manual invoice creation error:', err)
      error.value = err.response?.data?.message || err.response?.data?.error || 'ネットワークエラーが発生しました'
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 請求書更新
   */
  const updateInvoice = async (invoiceId, invoiceData) => {
    const authStore = useAuthStore()
    if (!authStore.isAuthenticated) {
      error.value = '認証が必要です'
      return false
    }

    loading.value = true
    error.value = null

    try {
      const response = await axios.put(`/api/invoices/${invoiceId}`, invoiceData, {
        withCredentials: true
      })

      if (response.data.success) {
        const updatedInvoice = response.data.invoice
        // 一覧内の請求書を更新
        const index = invoices.value.findIndex(inv => inv.id === invoiceId)
        if (index !== -1) {
          invoices.value[index] = updatedInvoice
        }
        if (currentInvoice.value && currentInvoice.value.id === invoiceId) {
          currentInvoice.value = updatedInvoice
        }
        return updatedInvoice
      } else {
        error.value = response.data.error || '請求書の更新に失敗しました'
        return false
      }
    } catch (err) {
      console.error('Invoice update error:', err)
      error.value = err.response?.data?.message || err.response?.data?.error || 'ネットワークエラーが発生しました'
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 請求書削除
   */
  const deleteInvoice = async (invoiceId) => {
    const authStore = useAuthStore()
    if (!authStore.isAuthenticated) {
      error.value = '認証が必要です'
      return false
    }

    loading.value = true
    error.value = null

    try {
      const response = await axios.delete(`/api/invoices/${invoiceId}`, {
        withCredentials: true
      })

      if (response.data.success) {
        // 一覧から削除
        invoices.value = invoices.value.filter(inv => inv.id !== invoiceId)
        pagination.value.total -= 1
        if (currentInvoice.value && currentInvoice.value.id === invoiceId) {
          currentInvoice.value = null
        }
        return true
      } else {
        error.value = response.data.error || '請求書の削除に失敗しました'
        return false
      }
    } catch (err) {
      console.error('Invoice deletion error:', err)
      error.value = err.response?.data?.message || err.response?.data?.error || 'ネットワークエラーが発生しました'
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * エラークリア
   */
  const clearError = () => {
    error.value = null
  }

  /**
   * ストアリセット
   */
  const resetStore = () => {
    invoices.value = []
    currentInvoice.value = null
    loading.value = false
    error.value = null
    pagination.value = {
      page: 1,
      pages: 0,
      per_page: 10,
      total: 0,
      has_next: false,
      has_prev: false
    }
  }

  return {
    // State
    invoices,
    currentInvoice,
    loading,
    error,
    pagination,
    
    // Computed
    totalInvoices,
    hasInvoices,
    invoiceStats,
    
    // Actions
    fetchInvoices,
    fetchInvoice,
    createInvoiceFromProject,
    createInvoice,
    updateInvoice,
    deleteInvoice,
    clearError,
    resetStore
  }
})