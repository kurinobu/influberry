<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useInvoicesStore } from '../stores/invoices.js'
import { useUIStore } from '../stores/ui.js'
import InvoiceList from '../components/InvoiceList.vue'
import HamburgerMenu from '../components/HamburgerMenu.vue'
import BasicDataModal from '../components/BasicDataModal.vue'
import UserSettings from '../components/UserSettings.vue'

const router = useRouter()
const authStore = useAuthStore()
const invoicesStore = useInvoicesStore()
const uiStore = useUIStore()

// アプリ初期化
onMounted(async () => {
  // 未認証の場合は認証ページへリダイレクト
  await authStore.checkAuthStatus()
  if (!authStore.isLoggedIn) {
    router.push('/')
    return
  }
  
  // 請求書データ取得
  await invoicesStore.fetchInvoices()
})

// 設定モーダル表示状態
// const showSettings = ref(false) // UIStoreに移管
// const showBasicData = ref(false) // UIStoreに移管

// 設定モーダル切り替え
// const toggleSettings = () => { // UIStoreに移管
//   showSettings.value = !showSettings.value
// }

// const toggleBasicData = () => { // UIStoreに移管
//   showBasicData.value = !showBasicData.value
// }

// ダッシュボードに戻る
const backToDashboard = () => {
  router.push('/dashboard')
}

</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- ヘッダー -->
    <header class="berry-header">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- アプリタイトルのみ -->
          <div class="flex items-center">
            <h1 class="text-2xl font-bold bg-gradient-to-r from-pink-500 to-purple-600 bg-clip-text text-transparent">
              BerryPay｜請求書管理
            </h1>
          </div>
          
          <!-- ハンバーガーメニュー -->
          <HamburgerMenu />
        </div>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        
        <!-- アプリヘッダー -->
        <div class="mb-6">
          <div class="berry-card">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-2xl font-bold text-gray-900">BerryPay｜請求書管理</h2>
                <p class="mt-1 text-sm text-gray-600">
                  プロジェクトから自動請求書生成・編集・管理を行います
                </p>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <!-- 1行目: 総請求書数・支払済 -->
                <div class="text-center">
                  <div class="text-xl md:text-2xl font-bold text-purple-600">{{ invoicesStore.invoices?.length || 0 }}</div>
                  <div class="text-xs text-gray-500">総請求書数</div>
                </div>
                <div class="text-center">
                  <div class="text-xl md:text-2xl font-bold text-green-600">
                    {{ invoicesStore.invoices?.filter(i => i.status === 'paid').length || 0 }}
                  </div>
                  <div class="text-xs text-gray-500">支払済</div>
                </div>
                
                <!-- 2行目: 未払・下書き -->
                <div class="text-center">
                  <div class="text-xl md:text-2xl font-bold text-yellow-600">
                    {{ invoicesStore.invoiceStats.sent + invoicesStore.invoiceStats.overdue }}
                  </div>
                  <div class="text-xs text-gray-500">未払</div>
                </div>
                <div class="text-center">
                  <div class="text-xl md:text-2xl font-bold text-gray-600">{{ invoicesStore.invoiceStats.draft }}</div>
                  <div class="text-xs text-gray-500">下書き</div>
                </div>
                
                <!-- 3行目: 総金額（2列結合・flexbox右寄せ） -->
                <div class="col-span-2 flex flex-col items-end">
                  <div class="text-xl md:text-2xl font-bold text-pink-600">
                    ¥{{ invoicesStore.invoiceStats.total_invoice_amount.toLocaleString() }}
                  </div>
                  <div class="text-xs text-gray-500">総請求額</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- InvoiceList コンポーネント -->
        <InvoiceList />

      </div>
    </main>
    <!-- 設定モーダル -->
    <div v-if="uiStore.showSettings" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="uiStore.closeSettings()">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="inline-block align-bottom berry-card text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full" @click.stop>
          <div class="berry-card px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">設定</h3>
              <button @click="uiStore.closeSettings()" class="text-gray-400 hover:text-gray-600">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            <UserSettings />
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- 基本データモーダル -->
    <BasicDataModal />
</template>

<style scoped>

/* === Phase 4 Z世代向けカードベースUI === */
.berry-card-form {
  background: linear-gradient(135deg, #fdf2f8 0%, #f3e8ff 100%);
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(244, 114, 182, 0.15);
  border: 2px solid #f9a8d4;
  padding: 2rem;
  transition: all 0.3s ease;
  margin-bottom: 1.5rem;
}

.berry-card-form:hover {
  box-shadow: 0 20px 40px rgba(244, 114, 182, 0.2);
  transform: translateY(-2px);
}

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

.berry-card-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f9a8d4;
}

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

/* InfluBerry カスタムスタイル */
header {
  backdrop-filter: blur(10px);
}

/* ホバーエフェクト */
.hover\:text-purple-200:hover {
  color: rgb(221 214 254);
}

/* スムーズなトランジション */
.transition-colors {
  transition: color 0.2s ease;
}

/* モバイルファースト最適化 */
@media (max-width: 640px) {
  .max-w-7xl {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .grid.grid-cols-2.md\\:grid-cols-4 .flex.items-center.space-x-4 {
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}
  
  
}

@media (max-width: 480px) {
  .text-xl {
    font-size: 1rem;
    line-height: 1.5rem;
  }
  
  .text-2xl {
    font-size: 1.25rem;
    line-height: 1.75rem;
  }
  
  .flex.items-center.space-x-4:last-child {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    display: grid;
    gap: 0.5rem;
  }
}

/* === Z世代向けカードベースUI === */
.berry-card-form {
  background: linear-gradient(135deg, #fdf2f8 0%, #f3e8ff 100%);
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(244, 114, 182, 0.15);
  border: 2px solid #f9a8d4;
  padding: 2rem;
  transition: all 0.3s ease;
  margin-bottom: 1.5rem;
}

.berry-card-form:hover {
  box-shadow: 0 20px 40px rgba(244, 114, 182, 0.2);
  transform: translateY(-2px);
}

.berry-card-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f9a8d4;
}

.berry-card {
  background: linear-gradient(135deg, #ffffff 0%, #fdf2f8 100%);
  border-radius: 1rem;
  box-shadow: 0 8px 20px rgba(244, 114, 182, 0.12);
  border: 2px solid #f9a8d4;
  padding: 1.5rem;
  transition: all 0.3s ease;
  transform: scale(1);
  margin-bottom: 1rem;
}

.berry-card:hover {
  box-shadow: 0 12px 30px rgba(244, 114, 182, 0.2);
  transform: scale(1.02) translateY(-2px);
}

/* === 入力フィールド（視認性最優先） === */
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

.berry-input::placeholder {
  color: #9ca3af;
  font-weight: 400;
}

.berry-select {
  width: 100%;
  min-width: 12rem;
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

/* === ボタンデザイン（Instagram/TikTokライク） === */
.berry-button {
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

.berry-button:hover {
  background: linear-gradient(45deg, #be185d, #9d174d);
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(236, 72, 153, 0.4);
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

/* === アクションボタン（丸型・TikTokライク） === */
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

.berry-action-button.complete {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
}

.berry-action-button.incomplete {
  background: #ffffff;
  border-color: #d1d5db;
  color: #6b7280;
}

.berry-action-button.incomplete:hover {
  border-color: #ec4899;
  background: #fdf2f8;
  color: #ec4899;
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

.berry-action-button.delete {
  color: #ef4444;
  background: #fef2f2;
  border-color: #fca5a5;
}

.berry-action-button.delete:hover {
  background: #fee2e2;
  border-color: #f87171;
}

/* === バッジ・ステータス表示 === */
.berry-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  color: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* === 空状態・エラー表示 === */
.berry-empty-state {
  background: linear-gradient(135deg, #fdf2f8, #f3e8ff);
  border-radius: 1rem;
  border: 2px solid #f9a8d4;
  padding: 3rem 2rem;
  text-align: center;
}

.berry-empty-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  opacity: 0.6;
  color: #ec4899;
}

.berry-loading {
  text-align: center;
  color: #ec4899;
  font-weight: 600;
}

.berry-error {
  margin-bottom: 2rem;
}

/* === モーダル（高品質） === */
.berry-modal {
  display: inline-block;
  vertical-align: bottom;
  background: #ffffff;
  border-radius: 1rem;
  text-align: left;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
  transform: translateY(0);
  transition: all 0.3s ease;
  border: 2px solid #f9a8d4;
}

@media (min-width: 640px) {
  .berry-modal {
    margin: 2rem auto;
    vertical-align: middle;
    max-width: 32rem;
    width: 100%;
  }
}

.berry-modal-header {
  background: linear-gradient(to right, #fdf2f8, #f3e8ff);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 2px solid #f9a8d4;
}

.berry-close-button {
  color: #9ca3af;
  transition: color 0.2s ease;
  cursor: pointer;
}

.berry-close-button:hover {
  color: #6b7280;
}

/* === レスポンシブ・モバイル最適化 === */
@media (max-width: 640px) {
  .berry-card-form {
    padding: 1.5rem;
    margin: 0 0.5rem 1rem;
  }
  
  .berry-card {
    padding: 1rem;
    margin: 0 0.5rem 0.75rem;
  }
  
  .berry-input, .berry-select {
    padding: 0.875rem 1rem;
    font-size: 1rem;
  }
  
  .berry-button {
    padding: 0.875rem 1.25rem;
    font-size: 1rem;
    width: 100%;
    justify-content: center;
  }
  
  .berry-action-button {
    width: 2.75rem;
    height: 2.75rem;
  }
}

/* === アニメーション・マイクロインタラクション === */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.berry-card {
  animation: fadeIn 0.3s ease-out;
}

.berry-button:active {
  animation: pulse 0.2s ease-in-out;
}

/* === 高コントラスト・視認性確保 === */
h1, h2, h3, h4, h5, h6 {
  color: #111827 !important;
  font-weight: 700 !important;
  text-shadow: none !important;
}

p, span, div {
  color: #374151 !important;
  font-weight: 500 !important;
  line-height: 1.6 !important;
}

/* Todo項目テキスト強化 */
.todo-title {
  color: #111827 !important;
  font-size: 1.125rem !important;
  font-weight: 700 !important;
  margin-bottom: 0.5rem !important;
}

.todo-description {
  color: #4b5563 !important;
  font-size: 1rem !important;
  font-weight: 500 !important;
  line-height: 1.5 !important;
}

.todo-meta {
  color: #6b7280 !important;
  font-size: 0.875rem !important;
  font-weight: 600 !important;
}

/* ヘッダータイトル強制カラフル表示 */
h1.text-2xl.font-bold {
  background: linear-gradient(to right, #ec4899, #8b5cf6) !important;
  -webkit-background-clip: text !important;
  background-clip: text !important;
  color: transparent !important;
}

/* 3並びフィールド着色統一 */
select[v-model="editForm.priority"] {
  background: linear-gradient(135deg, #fef3c7, #fbbf24) !important;
  border-color: #f59e0b !important;
}

/* berry-header統一スタイル（TodoApp.vue成功パターン） */
.berry-header {
  background: linear-gradient(to right, #fdf2f8, #ffffff, #f3e8ff);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid #f9a8d4;
  box-shadow: 0 1px 3px rgba(244, 114, 182, 0.1);
}

</style>