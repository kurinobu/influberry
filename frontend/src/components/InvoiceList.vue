<script setup>
import { ref, computed, onMounted } from 'vue'
import { useInvoicesStore } from '../stores/invoices.js'
import { useAuthStore } from '../stores/auth.js'
import { trackPdfDownload, trackError } from '@/utils/analytics.js'

// Invoice管理ストア
const invoicesStore = useInvoicesStore()

// ローカル状態
// ローカル状態
const selectedStatus = ref('')
const showDetailModal = ref(false)
const selectedInvoice = ref(null)
const pdfGenerating = ref(false)

// インライン編集状態（ProjectList.vue統一）
const editingInvoice = ref(null)  // null = 表示モード、ID = 編集モード
const editForm = ref({
  customer_name: '',
  amount: '',
  tax_rate: 10,
  status: 'draft',
  due_date: '',
  description: '',
  project_name: ''
})
const editErrors = ref({
  customer_name: '',
  amount: '',
  due_date: '',
  description: ''
})
const isSubmitting = ref(false)

// PDF生成メソッド
const generatePDF = async (invoiceId) => {
  pdfGenerating.value = true
  try {
    const result = await invoicesStore.generatePDF(invoiceId)
    if (!result.success) {
      trackError('pdf_generation', result.error, 'InvoiceList')
      alert(`PDF生成エラー: ${result.error}`)
    } else {
      trackPdfDownload('invoice')
    }
  } catch (error) {
    trackError('pdf_generation', error.message, 'InvoiceList')
    alert(`PDF生成エラー: ${error.message}`)
  } finally {
    pdfGenerating.value = false
  }
}


// 計算プロパティ
const statusCounts = computed(() => ({
  draft: invoicesStore.invoiceStats.draft,
  sent: invoicesStore.invoiceStats.sent,
  paid: invoicesStore.invoiceStats.paid,
  overdue: invoicesStore.invoiceStats.overdue,
  cancelled: invoicesStore.invoiceStats.cancelled
}))

const totalAmount = computed(() => invoicesStore.invoiceStats.total_invoice_amount)
const paidAmount = computed(() => invoicesStore.invoiceStats.paid_amount)
const unpaidAmount = computed(() => invoicesStore.invoiceStats.unpaid_amount)

// 詳細表示関数
const showInvoiceDetail = async (invoice) => {
  try {
    // Invoice詳細データ取得
    const success = await invoicesStore.fetchInvoice(invoice.id)
    if (success) {
      selectedInvoice.value = invoicesStore.currentInvoice
      showDetailModal.value = true
    } else {
      console.error('Invoice詳細取得エラー:', invoicesStore.error)
    }
  } catch (error) {
    console.error('Invoice詳細表示エラー:', error)
  }
}

// 詳細モーダル閉鎖
const closeDetailModal = () => {
  showDetailModal.value = false
  selectedInvoice.value = null
}

// 編集開始（ProjectList.vue統一）
const startEdit = (invoice) => {
  editingInvoice.value = invoice.id
  editForm.value = {
    customer_name: invoice.client_company || invoice.customer_name || '',
    amount: parseFloat(invoice.subtotal || invoice.amount || 0),
    tax_rate: parseFloat(invoice.tax_rate || 10),
    status: invoice.status || 'draft',
    due_date: invoice.due_date || '',
    description: invoice.description || '',
    project_name: invoice.project_name || ''
  }
  editErrors.value = {
    customer_name: '',
    amount: '',
    due_date: '',
    description: ''
  }
}

// 編集キャンセル
const cancelEdit = () => {
  editingInvoice.value = null
  editForm.value = {
    customer_name: '',
    amount: '',
    tax_rate: 10,
    status: 'draft',
    due_date: '',
    description: '',
    project_name: ''
  }
  editErrors.value = {
    customer_name: '',
    amount: '',
    due_date: '',
    description: ''
  }
  isSubmitting.value = false
}

// バリデーション
const validateForm = () => {
  let isValid = true
  editErrors.value = {
    customer_name: '',
    amount: '',
    due_date: '',
    description: ''
  }

  if (!editForm.value.customer_name.trim()) {
    editErrors.value.customer_name = '顧客名は必須です'
    isValid = false
  }

  if (!editForm.value.amount || editForm.value.amount <= 0) {
    editErrors.value.amount = '金額は1円以上である必要があります'
    isValid = false
  }

  if (!editForm.value.due_date) {
    editErrors.value.due_date = '支払期限は必須です'
    isValid = false
  }

  if (!editForm.value.description.trim()) {
    editErrors.value.description = '説明は必須です'
    isValid = false
  }

  return isValid
}

// 保存処理
const saveEdit = async () => {
  if (!validateForm()) {
    return
  }

  isSubmitting.value = true

  try {
    const submitData = {
      client_company: editForm.value.customer_name.trim(),  // customer_name → client_company
      subtotal: parseFloat(editForm.value.amount),          // amount → subtotal
      tax_rate: parseFloat(editForm.value.tax_rate),
      status: editForm.value.status,
      due_date: editForm.value.due_date,
      description: editForm.value.description.trim(),
      project_name: editForm.value.project_name.trim()
    }

    const result = await invoicesStore.updateInvoice(editingInvoice.value, submitData)

    if (result.success) {
      await invoicesStore.fetchInvoices()
      cancelEdit()
    } else {
      alert(`保存エラー: ${result.error || '不明なエラー'}`)
    }
  } catch (error) {
    console.error('保存エラー:', error)
    trackError('invoice_update', error.message, 'InvoiceList')
    alert(`保存エラー: ${error.message}`)
  } finally {
    isSubmitting.value = false
  }
}

// ステータス表示関数
const getStatusText = (status) => {
  const statusMap = {
    draft: '下書き',
    sent: '送信済み',
    paid: '支払済み',
    overdue: '期限超過',
    cancelled: 'キャンセル'
  }
  return statusMap[status] || status
}

const getStatusBadgeClass = (status) => {
  const classMap = {
    draft: 'bg-gray-100 text-gray-800',
    sent: 'bg-blue-100 text-blue-800',
    paid: 'bg-green-100 text-green-800',
    overdue: 'bg-red-100 text-red-800',
    cancelled: 'bg-yellow-100 text-yellow-800'
  }
  return classMap[status] || 'bg-gray-100 text-gray-800'
}

// フィルタリングされた請求書一覧
const filteredInvoices = computed(() => {
  if (!selectedStatus.value) return invoicesStore.invoices
  return invoicesStore.invoices.filter(invoice => invoice.status === selectedStatus.value)
})

// コンポーネント初期化
onMounted(async () => {
  // 認証状態確認後にfetch実行
  const authStore = useAuthStore()
  if (authStore.isAuthenticated && invoicesStore.invoices.length === 0) {
    await invoicesStore.fetchInvoices()
  }
})

// ステータスフィルター
const handleStatusFilter = (status) => {
  selectedStatus.value = status === selectedStatus.value ? '' : status
}

// ステータス表示名
const getStatusDisplay = (status) => {
  const statusMap = {
    draft: '下書き',
    sent: '送信済み',
    paid: '支払済み',
    overdue: '期限超過',
    cancelled: 'キャンセル'
  }
  return statusMap[status] || status
}

// ステータス色
const getStatusColor = (status) => {
  const colorMap = {
    draft: 'bg-gray-100 text-gray-800',
    sent: 'bg-blue-100 text-blue-800',
    paid: 'bg-green-100 text-green-800',
    overdue: 'bg-red-100 text-red-800',
    cancelled: 'bg-gray-100 text-gray-600'
  }
  return colorMap[status] || 'bg-gray-100 text-gray-800'
}

// 金額フォーマット
const formatAmount = (amount) => {
  return new Intl.NumberFormat('ja-JP', {
    style: 'currency',
    currency: 'JPY'
  }).format(Math.round(amount || 0))
}

// 日付フォーマット
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('ja-JP')
}

</script>

<template>
  <div class="space-y-6">
    <!-- ページヘッダー -->
    <div class="berry-card">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-lg font-bold text-gray-900">📋 請求書管理</h2>
          <p class="mt-1 text-sm text-gray-600">
            作成済み請求書の一覧・管理
          </p>
        </div>
        <div class="text-right">
          <p class="text-sm text-gray-500">総請求書数</p>
          <p class="text-2xl font-bold text-gray-900">
            {{ invoicesStore.totalInvoices }}件
          </p>
        </div>
      </div>
    </div>

    <!-- 統計カード -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- ステータス別統計 -->
      <div class="berry-card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
              <span class="text-sm">📝</span>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">下書き</p>
            <p class="text-xl font-semibold text-gray-900">{{ statusCounts.draft }}</p>
          </div>
        </div>
      </div>

      <div class="berry-card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
              <span class="text-sm">📤</span>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">送信済み</p>
            <p class="text-xl font-semibold text-gray-900">{{ statusCounts.sent }}</p>
          </div>
        </div>
      </div>

      <div class="berry-card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
              <span class="text-sm">✅</span>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">支払済み</p>
            <p class="text-xl font-semibold text-gray-900">{{ statusCounts.paid }}</p>
          </div>
        </div>
      </div>

      <div class="berry-card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
              <span class="text-sm">⚠️</span>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">期限超過</p>
            <p class="text-xl font-semibold text-gray-900">{{ statusCounts.overdue }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 金額サマリー -->
    <!-- 総請求額: 全幅カード -->
    <div class="berry-card mb-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
              <span class="text-sm">💰</span>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">総請求額</p>
          </div>
        </div>
        <div class="text-right">
          <p class="text-xl font-semibold text-gray-900">{{ formatAmount(totalAmount) }}</p>
        </div>
      </div>
    </div>

    <!-- 支払済み・未収金額: 2カラムGrid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      
      <div class="berry-card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
              <span class="text-sm">✨</span>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">支払済み</p>
            <p class="text-xl font-semibold text-gray-900">{{ formatAmount(paidAmount) }}</p>
          </div>
        </div>
      </div>
      
      <div class="berry-card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center">
              <span class="text-sm">📊</span>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">未収金額</p>
            <p class="text-xl font-semibold text-gray-900">{{ formatAmount(unpaidAmount) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- ステータスフィルター -->
    <div class="berry-card">
      <h3 class="text-lg font-medium text-gray-900 mb-3">📋 ステータス別フィルター</h3>
      <div class="flex flex-wrap gap-2">
        <button
          @click="handleStatusFilter('')"
          :class="[
            'px-3 py-1 rounded-full text-sm font-medium transition-colors',
            selectedStatus === '' 
              ? 'bg-purple-100 text-purple-800 border-2 border-purple-500' 
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          ]"
        >
          すべて ({{ invoicesStore.totalInvoices }})
        </button>
        
        <button
          v-for="(count, status) in statusCounts"
          :key="status"
          @click="handleStatusFilter(status)"
          :class="[
            'px-3 py-1 rounded-full text-sm font-medium transition-colors',
            selectedStatus === status 
              ? 'bg-purple-100 text-purple-800 border-2 border-purple-500' 
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          ]"
        >
          {{ getStatusDisplay(status) }} ({{ count }})
        </button>
      </div>
    </div>

    <!-- 請求書一覧 -->
    <div class="berry-card">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">📄 請求書一覧</h3>
      </div>
      
      <!-- ローディング状態 -->
      <div v-if="invoicesStore.loading" class="p-8 text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500 mx-auto"></div>
        <p class="mt-2 text-gray-500">読み込み中...</p>
      </div>
      
      <!-- エラー状態 -->
      <div v-else-if="invoicesStore.error" class="p-8 text-center">
        <p class="text-red-600">{{ invoicesStore.error }}</p>
        <button 
          @click="invoicesStore.fetchInvoices()" 
          class="mt-2 text-purple-600 hover:text-purple-800"
        >
          再試行
        </button>
      </div>
      
      <!-- 請求書なし -->
      <div v-else-if="!invoicesStore.hasInvoices" class="p-8 text-center">
        <p class="text-gray-500">📋 請求書がまだありません</p>
        <p class="text-sm text-gray-400 mt-1">
          プロジェクト管理画面から請求書を作成してください
        </p>
      </div>
      
      <!-- 請求書リスト -->
      <div v-else class="divide-y divide-gray-200">
        <div 
          v-for="invoice in filteredInvoices" 
          :key="invoice.id"
          class="p-6 hover:bg-gray-50 transition-colors"
        >
          <div class="flex flex-col space-y-4">
            <!-- 編集モード（ProjectList.vue統一） -->
            <div v-if="editingInvoice === invoice.id" class="space-y-4 bg-gradient-to-br from-white to-pink-50 border-2 border-pink-300 rounded-lg p-4">
              <div class="berry-input-group">
                <label class="berry-label">顧客名 *</label>
                <input v-model="editForm.customer_name" class="berry-input" placeholder="顧客名を入力" />
                <p v-if="editErrors.customer_name" class="text-red-500 text-sm mt-1">{{ editErrors.customer_name }}</p>
              </div>

              <div class="berry-input-group">
                <label class="berry-label">プロジェクト名</label>
                <input v-model="editForm.project_name" class="berry-input" placeholder="プロジェクト名（任意）" />
              </div>

              <div class="berry-input-group">
                <label class="berry-label">税抜金額 *</label>
                <input v-model="editForm.amount" type="number" class="berry-input" placeholder="金額を入力" />
                <p v-if="editErrors.amount" class="text-red-500 text-sm mt-1">{{ editErrors.amount }}</p>
              </div>

              <div class="berry-input-group">
                <label class="berry-label">消費税率（%）</label>
                <input v-model="editForm.tax_rate" type="number" step="0.1" class="berry-input" placeholder="10" />
              </div>

              <div class="berry-input-group">
                <label class="berry-label">支払期限 *</label>
                <input v-model="editForm.due_date" type="date" class="berry-input" />
                <p v-if="editErrors.due_date" class="text-red-500 text-sm mt-1">{{ editErrors.due_date }}</p>
              </div>

              <div class="berry-input-group">
                <label class="berry-label">説明 *</label>
                <textarea v-model="editForm.description" rows="3" class="berry-input resize-none" placeholder="説明を入力"></textarea>
                <p v-if="editErrors.description" class="text-red-500 text-sm mt-1">{{ editErrors.description }}</p>
              </div>

              <div class="berry-input-group">
                <label class="berry-label">ステータス</label>
                <select v-model="editForm.status" class="berry-select">
                  <option value="draft">下書き</option>
                  <option value="sent">送信済み</option>
                  <option value="paid">支払済み</option>
                  <option value="overdue">期限超過</option>
                  <option value="cancelled">キャンセル</option>
                </select>
              </div>

              <div class="flex justify-end space-x-4 mt-6">
                <button @click="cancelEdit" class="berry-secondary-button" :disabled="isSubmitting">
                  キャンセル
                </button>
                <button @click="saveEdit" class="berry-primary-button" :disabled="isSubmitting">
                  {{ isSubmitting ? '保存中...' : '保存' }}
                </button>
              </div>
            </div>

            <!-- 通常表示モード -->
            <div v-else class="flex-1 min-w-0">
              <!-- ステータスバッジ（最上部） -->
              <div class="mb-2">
                <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium', getStatusColor(invoice.status)]">
                  {{ getStatusDisplay(invoice.status) }}
                </span>
              </div>
              
              <!-- 請求書番号 -->
              <h4 class="text-lg font-medium text-gray-900">
                {{ invoice.invoice_number }}
              </h4>
              
              <div class="mt-2 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
                <div class="space-y-1">
                  <div>
                    <span class="font-medium">顧客:</span>
                    {{ invoice.client_company || '-' }}
                  </div>
                  <div v-if="invoice.project_name" class="text-sm text-gray-600">
                    {{ invoice.project_name }}
                  </div>
                </div>
                <div>
                  <span class="font-medium">発行日:</span>
                  {{ formatDate(invoice.issue_date) }}
                </div>
                <div>
                  <span class="font-medium">支払期限:</span>
                  {{ formatDate(invoice.due_date) }}
                </div>
              </div>
              
              <div class="mt-2 text-right">
                <p class="text-lg font-bold text-gray-900">
                  {{ formatAmount(invoice.total_amount) }}
                </p>
                <p class="text-xs text-gray-500">
                  (税抜: {{ formatAmount(invoice.amount) }})
                </p>
              </div>
            </div>
            
            <div class="flex items-center pt-3 border-t border-gray-100" style="gap: 1rem;">
              <button @click.stop="startEdit(invoice)" 
                      class="berry-action-button edit"
                      title="編集">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
              </button>
              <button @click.stop="showInvoiceDetail(invoice)" 
                      class="berry-action-button view"
                      title="詳細表示">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Invoice詳細モーダル -->
  <div v-if="showDetailModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="berry-card max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
      <!-- モーダルヘッダー -->
      <div class="bg-gradient-to-r from-purple-600 to-pink-600 text-white p-6 rounded-t-lg">
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-bold">📋 請求書詳細</h2>
          <button @click="closeDetailModal" class="text-white hover:text-gray-200 text-2xl">
            ×
          </button>
        </div>
        <p class="text-purple-100 mt-2">{{ selectedInvoice?.invoice_number }}</p>
      </div>

      <!-- モーダル内容 -->
      <div class="p-6" v-if="selectedInvoice">
        <!-- 基本情報 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div class="space-y-4">
            <div>
              <label class="text-sm font-medium text-gray-600">請求書番号</label>
              <p class="text-lg font-semibold text-gray-900">{{ selectedInvoice.invoice_number }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-600">顧客名</label>
              <p class="text-lg font-semibold text-gray-900">{{ selectedInvoice.client_company }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-600">ステータス</label>
              <span :class="getStatusBadgeClass(selectedInvoice.status)" class="inline-block px-3 py-1 rounded-full text-sm font-medium">
                {{ getStatusText(selectedInvoice.status) }}
              </span>
            </div>
          </div>
          
          <div class="space-y-4">
            <div>
              <label class="text-sm font-medium text-gray-600">発行日</label>
              <p class="text-lg font-semibold text-gray-900">{{ formatDate(selectedInvoice.issue_date) }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-600">支払期限</label>
              <p class="text-lg font-semibold text-gray-900">{{ formatDate(selectedInvoice.due_date) }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-600">プロジェクト名</label>
              <p class="text-lg font-semibold text-gray-900">{{ selectedInvoice.project_name || '-' }}</p>
            </div>
          </div>
        </div>

        <!-- 金額情報 -->
        <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 mb-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">💰 金額詳細</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="text-sm font-medium text-gray-600">税抜金額</label>
              <p class="text-xl font-bold text-gray-900">{{ formatAmount(selectedInvoice.subtotal) }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-600">消費税</label>
              <p class="text-xl font-bold text-gray-900">{{ formatAmount(selectedInvoice.tax_amount) }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-600">請求合計</label>
              <p class="text-2xl font-bold text-purple-600">{{ formatAmount(selectedInvoice.total_amount) }}</p>
            </div>
          </div>
        </div>

        <!-- 説明・備考 -->
        <div v-if="selectedInvoice.description" class="mb-6">
          <label class="text-sm font-medium text-gray-600">説明・備考</label>
          <p class="mt-2 p-4 bg-gray-50 rounded-lg text-gray-900">{{ selectedInvoice.description }}</p>
        </div>

        <!-- アクションボタン -->
        <div class="flex justify-end space-x-3 pt-4 border-t">
          <button @click="closeDetailModal" class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600">
            閉じる
          </button>
          <button @click="showInvoiceEdit(selectedInvoice)" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            📝 編集
          </button>
          <button @click="generatePDF(selectedInvoice.id)" class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors" :disabled="pdfGenerating">
            {{ pdfGenerating ? '生成中...' : '📄 PDF' }}
          </button>
        </div>
      </div>
    </div>
  </div>
  <!-- Invoice編集フォーム -->
  
</template>



<style scoped>
/* === Phase 4 Z世代向けカードベースUI === */
.berry-card {
  background: linear-gradient(135deg, #ffffff 0%, #fdf2f8 100%);
  border-radius: 1rem;
  box-shadow: 0 8px 20px rgba(244, 114, 182, 0.12);
  border: 2px solid #f9a8d4;
  padding: 1.5rem;
  transition: all 0.3s ease;
  margin-bottom: 1rem;
  transform: scale(1);
}

/* === テキストサイズ統一（3アプリ統一） === */
.text-2xl {
  font-size: 1.25rem; /* 20px統一 */
}
.berry-card:hover {
  box-shadow: 0 12px 30px rgba(244, 114, 182, 0.2);
  transform: scale(1.02) translateY(-2px);
}

/* InfluBerry カスタムスタイル - 請求書管理画面 */
.transition-colors {
  transition: background-color 0.2s ease, color 0.2s ease;
}

/* アニメーション */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.bg-white {
  animation: fadeIn 0.3s ease-out;
}

/* ホバーエフェクト */
.hover\:bg-gray-50:hover {
  background-color: #f9fafb;
}

/* グラデーション強化 */
.bg-gradient-to-r {
  background-image: linear-gradient(to right, var(--tw-gradient-stops));
}

/* berry-action-button（TodoAppパターン統一） */
.berry-action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  transition: all 0.3s ease;
  transform: scale(1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  border: 2px solid transparent;
}

.berry-action-button:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.berry-action-button.edit {
  color: #3b82f6;
  background: #dbeafe;
  border-color: #93c5fd;
}

.berry-action-button.edit:hover {
  background: #bfdbfe;
  border-color: #60a5fa;
}

.berry-action-button.view {
  color: #22c55e;
  background: #f0fdf4;
  border-color: #86efac;
}

.berry-action-button.view:hover {
  background: #dcfce7;
  border-color: #4ade80;
}

/* モバイル最適化 */
@media (max-width: 640px) {
  .berry-action-button {
    width: 2.75rem;
    height: 2.75rem;
  }
}

/* === Phase 4 berry化デザイン（TodoApp.vue統一） === */

/* 入力フィールド（視認性最優先） */
.berry-input-group {
  margin-bottom: 1.5rem;
}

.berry-label {
  display: block;
  font-size: 1rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.5rem;
  text-shadow: none;
}

.berry-input {
  width: 100%;
  padding: 1rem 1.25rem;
  border-radius: 0.75rem;
  border: 2px solid #f9a8d4;
  background: #ffffff;
  font-size: 1rem;
  font-weight: 500;
  color: #111827;
  line-height: 1.5;
  transition: all 0.2s ease;
}

.berry-input:focus {
  outline: none;
  border-color: #ec4899;
  box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.1);
  background: #ffffff;
}

.berry-select {
  width: 100%;
  padding: 1rem 1.25rem;
  border-radius: 0.75rem;
  border: 2px solid #f9a8d4;
  background: #ffffff;
  font-size: 1rem;
  font-weight: 500;
  color: #111827;
  transition: all 0.2s ease;
  cursor: pointer;
}

.berry-select:focus {
  outline: none;
  border-color: #ec4899;
  box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.1);
}

/* ボタンデザイン */
.berry-primary-button {
  display: inline-flex;
  align-items: center;
  padding: 1rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 700;
  color: #ffffff;
  background: linear-gradient(45deg, #ec4899, #be185d);
  border: none;
  font-size: 1rem;
  transition: all 0.2s ease;
  transform: scale(1);
  box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
  cursor: pointer;
}

.berry-primary-button:hover {
  background: linear-gradient(45deg, #be185d, #9d174d);
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(236, 72, 153, 0.4);
}

.berry-primary-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: scale(1);
}

.berry-secondary-button {
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  font-weight: 600;
  color: #374151;
  background: #ffffff;
  border: 2px solid #d1d5db;
  font-size: 1rem;
  transition: all 0.2s ease;
  cursor: pointer;
}

.berry-secondary-button:hover {
  background: #f9fafb;
  border-color: #9ca3af;
  color: #111827;
}

.berry-secondary-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* アクションボタン（丸型・TikTokライク） */
.berry-action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  transition: all 0.3s ease;
  transform: scale(1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  border: 2px solid transparent;
}

.berry-action-button.edit {
  color: #3b82f6;
  background: #dbeafe;
  border-color: #93c5fd;
}

.berry-action-button.edit:hover {
  background: #bfdbfe;
  border-color: #60a5fa;
}

.berry-action-button.view {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
}

.berry-action-button.view:hover {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
}
</style>