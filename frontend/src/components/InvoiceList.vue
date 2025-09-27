<script setup>
import { ref, computed, onMounted } from 'vue'
import { useInvoicesStore } from '../stores/invoices.js'
import { useAuthStore } from '../stores/auth.js'
import InvoiceForm from './InvoiceForm.vue'

// Invoice管理ストア
const invoicesStore = useInvoicesStore()

// ローカル状態
const selectedStatus = ref('')
const showDetailModal = ref(false)
const selectedInvoice = ref(null)
const showEditModal = ref(false)
const editingInvoice = ref(null)
// 状態をsetupStateにexport
defineExpose({
  showEditModal,
  editingInvoice
})
// 計算プロパティ
const statusCounts = computed(() => ({
  draft: invoicesStore.invoiceStats.draft,
  sent: invoicesStore.invoiceStats.sent,
  paid: invoicesStore.invoiceStats.paid,
  overdue: invoicesStore.invoiceStats.overdue,
  cancelled: invoicesStore.invoiceStats.cancelled
}))

const totalAmount = computed(() => invoicesStore.invoiceStats.total_amount)
const paidAmount = computed(() => invoicesStore.invoiceStats.paid_amount)
const unpaidAmount = computed(() => totalAmount.value - paidAmount.value)

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

// 編集モーダル開始
const showInvoiceEdit = (invoice) => {
  console.log('=== 編集ボタンクリック開始 ===')
  console.log('1. 受信invoice:', invoice)
  console.log('2. 変更前showEditModal:', showEditModal.value)
  console.log('3. 変更前editingInvoice:', editingInvoice.value)
  
  editingInvoice.value = {
    ...invoice,
    customer_name: invoice.client_company || invoice.customer_name || '',
    amount: parseFloat(invoice.subtotal || invoice.amount || 0)
  }
  showEditModal.value = true
  
  console.log('4. 変更後showEditModal:', showEditModal.value)
  console.log('5. 変更後editingInvoice:', editingInvoice.value)
  console.log('=== 編集ボタンクリック完了 ===')
}

// 編集モーダル閉鎖
const closeEditModal = () => {
  showEditModal.value = false
  editingInvoice.value = null
}

// 編集成功処理
const handleEditSuccess = (result) => {
  console.log('請求書編集成功:', result.message)
  // 一覧とcurrentInvoiceを更新
  if (selectedInvoice.value && selectedInvoice.value.id === result.invoice.id) {
    selectedInvoice.value = result.invoice
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
  }).format(amount || 0)
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
          <h2 class="text-2xl font-bold text-gray-900">📋 請求書管理</h2>
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
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="berry-card">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
            <span class="text-sm">💰</span>
          </div>
        </div>
        <div class="ml-4">
          <p class="text-sm font-medium text-gray-500">総請求額</p>
          <p class="text-xl font-semibold text-gray-900">{{ formatAmount(totalAmount) }}</p>
        </div>
      </div>
    </div>
      
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
            <div class="flex-1 min-w-0">
              <div class="flex items-center space-x-3">
                <h4 class="text-lg font-medium text-gray-900">
                  {{ invoice.invoice_number }}
                </h4>
                <span 
                  :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    getStatusColor(invoice.status)
                  ]"
                >
                  {{ getStatusDisplay(invoice.status) }}
                </span>
              </div>
              
              <div class="mt-2 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
                <div class="space-y-1">
                  <div>
                    <span class="font-medium">顧客:</span>
                    {{ invoice.company_name || '-' }}
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
            
            <div class="flex flex-wrap gap-2 pt-3 border-t border-gray-100">
              <button @click="showInvoiceEdit(invoice)" class="text-blue-600 hover:text-blue-800 text-sm">
                📝 編集
              </button>
              <button 
                @click="showInvoiceDetail(invoice)"
                class="text-green-600 hover:text-green-800 text-sm">
                👁️ 詳細
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
              <p class="text-lg font-semibold text-gray-900">{{ selectedInvoice.customer_name }}</p>
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
              <p class="text-xl font-bold text-gray-900">{{ formatAmount(selectedInvoice.amount) }}</p>
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
        </div>
      </div>
    </div>
  </div>
  <!-- Invoice編集フォーム -->
  <InvoiceForm
    :is-open="showEditModal"
    :invoice="editingInvoice"
    @close="closeEditModal"
    @success="handleEditSuccess"
  />
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


</style>