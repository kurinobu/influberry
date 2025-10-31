<template>
  <div v-if="!monthlyStore.loading" class="monthly-stats-section berry-card rounded-b-lg p-6">
    <!-- 概要タブ -->
    <div v-if="currentTab === 'overview'" class="overview-section">
      <div class="flex items-center mb-6">
        <ChartBarIcon class="w-8 h-8 text-amber-500 mr-3" />
        <h2 class="text-2xl font-bold text-gray-900">{{ personalizedText }}主要な実績</h2>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="stat-card bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-lg">
          <div class="text-sm text-blue-600 font-medium mb-2">{{ personalizedText }}累計活動案件数</div>
          <div class="text-4xl font-bold text-blue-900">
            {{ overviewData?.total_projects || 0 }} 件
          </div>
        </div>
        
        <div class="stat-card bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg">
          <div class="text-sm text-green-600 font-medium mb-2">{{ personalizedText }}累計入金額</div>
          <div class="text-4xl font-bold text-green-900">
            ¥{{ formatCurrency(overviewData?.total_income || 0) }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- 月次タブ -->
    <div v-else class="monthly-section">
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center">
          <h2 class="text-2xl font-bold text-gray-900 flex items-center">
            <ChartBarIcon class="w-8 h-8 text-amber-500 mr-3" />
            {{ monthLabel }}の実績
          </h2>
        </div>
        
        <!-- 目標設定ボタン（当月のみ表示） -->
        <button 
          v-if="isCurrentMonth"
          @click="openTargetSettings"
          class="px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500 transition-colors flex items-center"
        >
          <FlagIcon class="w-5 h-5 mr-2" />
          目標設定
        </button>
      </div>
      
      <!-- 注釈（過去データ） -->
      <div v-if="stats?.note" class="mb-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded">
        <p class="text-sm text-yellow-700 flex items-center">
          <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
          </svg>
          {{ stats.note }}
        </p>
      </div>
      
      <!-- プログレスバー群 -->
      <div class="space-y-6">
        <ProgressBar 
          label="獲得案件"
          :current="stats?.actual.acquired_projects || 0"
          :target="stats?.target?.projects || 0"
          unit="件"
          icon="box"
        />
        
        <ProgressBar 
          label="完了案件"
          :current="stats?.actual.completed_projects || 0"
          :target="stats?.target?.projects || 0"
          unit="件"
          icon="check"
        />
        
        <ProgressBar 
          label="請求額"
          :current="stats?.actual.sent_invoices_amount || 0"
          :target="stats?.target?.income || 0"
          unit="円"
          icon="currency"
        />
      </div>
    </div>
  </div>
  
  <!-- スケルトンローディング -->
  <div v-else-if="monthlyStore.loading" class="monthly-stats-section berry-card rounded-b-lg p-6">
    <!-- 概要タブのスケルトン -->
    <div v-if="currentTab === 'overview'" class="overview-section">
      <div class="flex items-center mb-6">
        <div class="w-8 h-8 bg-gray-300 rounded animate-pulse mr-3"></div>
        <div class="h-8 w-48 bg-gray-300 rounded animate-pulse"></div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- スケルトンカード1 -->
        <div class="stat-card bg-gradient-to-br from-gray-100 to-gray-200 p-6 rounded-lg">
          <div class="h-4 w-32 bg-gray-300 rounded animate-pulse mb-2"></div>
          <div class="h-10 w-24 bg-gray-300 rounded animate-pulse"></div>
        </div>
        
        <!-- スケルトンカード2 -->
        <div class="stat-card bg-gradient-to-br from-gray-100 to-gray-200 p-6 rounded-lg">
          <div class="h-4 w-32 bg-gray-300 rounded animate-pulse mb-2"></div>
          <div class="h-10 w-24 bg-gray-300 rounded animate-pulse"></div>
        </div>
      </div>
    </div>
    
    <!-- 月次タブのスケルトン -->
    <div v-else class="monthly-section">
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center">
          <div class="w-8 h-8 bg-gray-300 rounded animate-pulse mr-3"></div>
          <div class="h-8 w-48 bg-gray-300 rounded animate-pulse"></div>
        </div>
        <div class="w-24 h-10 bg-gray-300 rounded animate-pulse"></div>
      </div>
      
      <!-- スケルトンプログレスバー群 -->
      <div class="space-y-6">
        <!-- スケルトンプログレスバー1 -->
        <div class="space-y-2">
          <div class="flex justify-between items-center">
            <div class="h-5 w-24 bg-gray-300 rounded animate-pulse"></div>
            <div class="h-5 w-16 bg-gray-300 rounded animate-pulse"></div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-6">
            <div class="h-6 w-1/2 bg-gray-300 rounded-full animate-pulse"></div>
          </div>
          <div class="h-4 w-32 bg-gray-300 rounded animate-pulse"></div>
        </div>
        
        <!-- スケルトンプログレスバー2 -->
        <div class="space-y-2">
          <div class="flex justify-between items-center">
            <div class="h-5 w-24 bg-gray-300 rounded animate-pulse"></div>
            <div class="h-5 w-16 bg-gray-300 rounded animate-pulse"></div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-6">
            <div class="h-6 w-1/3 bg-gray-300 rounded-full animate-pulse"></div>
          </div>
          <div class="h-4 w-32 bg-gray-300 rounded animate-pulse"></div>
        </div>
        
        <!-- スケルトンプログレスバー3 -->
        <div class="space-y-2">
          <div class="flex justify-between items-center">
            <div class="h-5 w-24 bg-gray-300 rounded animate-pulse"></div>
            <div class="h-5 w-16 bg-gray-300 rounded animate-pulse"></div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-6">
            <div class="h-6 w-2/3 bg-gray-300 rounded-full animate-pulse"></div>
          </div>
          <div class="h-4 w-32 bg-gray-300 rounded animate-pulse"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useMonthlyStore } from '@/stores/monthly'
import { useUIStore } from '@/stores/ui'
import { useProjectsStore } from '@/stores/projects'
import { useInvoicesStore } from '@/stores/invoices'
import { useMonthlyRotationStore } from '@/stores/monthlyRotation'

// Step 2 Phase 1: 環境変数による条件付きログ出力
const isDevelopment = import.meta.env.DEV

// デバッグログ関数（開発環境でのみ出力）
const debugLog = (...args) => {
  if (isDevelopment) {
    console.log(...args)
  }
}

// エラーログ関数（常に出力）
const errorLog = (...args) => {
  console.error(...args)
}
import { useAuthStore } from '@/stores/auth'
import ProgressBar from './ProgressBar.vue'
import { ChartBarIcon, CalendarIcon, FlagIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  currentTab: {
    type: String,
    required: true
  }
})

const monthlyStore = useMonthlyStore()
const uiStore = useUIStore()
const projectsStore = useProjectsStore()
const invoicesStore = useInvoicesStore()
const rotationStore = useMonthlyRotationStore()
const authStore = useAuthStore()

// Phase 3: ローディング状態管理の統一（シンプル構造 > 複雑構造）
// ローカルloadingを削除し、ストアloadingのみを使用
const stats = ref(null)
const overviewData = ref(null)

// 重複実行防止フラグ
const isLoadingTargets = ref(false)
const isLoadingStats = ref(false)

const monthLabel = computed(() => {
  if (props.currentTab === 'overview') return ''
  
  // 動的にタイトルを生成
  const [year, month] = props.currentTab.split('-')
  return `${year}年${parseInt(month)}月`
})

// パーソナライズドテキスト生成
const personalizedText = computed(() => {
  const influencerName = authStore.user?.influencer_name
  if (influencerName && influencerName.trim()) {
    return `${influencerName}さんの`
  }
  return 'あなたの'
})

// 当月判定ロジック
const isCurrentMonth = computed(() => {
  if (props.currentTab === 'overview') return false
  
  const [year, month] = props.currentTab.split('-')
  const now = new Date()
  const currentYear = now.getFullYear()
  const currentMonth = now.getMonth() + 1
  
  return parseInt(year) === currentYear && parseInt(month) === currentMonth
})

// Phase 3: 統計データのみ取得（無限ループ防止用）- ローディング状態管理を統一
const loadStatsOnly = async () => {
  if (props.currentTab === 'overview' || isLoadingStats.value) return
  
  isLoadingStats.value = true
  
  try {
    const [year, month] = props.currentTab.split('-')
    
    // データ同期の確実化（ステータス変更履歴による複雑な集計処理対応）
    // 1. 統計データを強制的に再取得
    await monthlyStore.fetchStats(parseInt(year), parseInt(month))
    
    // 🔧 修正: データ同期の確実化（シンプル化）
    await nextTick()
    stats.value = monthlyStore.getStatsByMonth(props.currentTab + '-01')
    await nextTick()
    
    // デバッグログ追加
    debugLog('統計データ更新完了 - データ同期確実化:', {
      tab: props.currentTab,
      stats: stats.value,
      targets: monthlyStore.targets,
      targetProjects: stats.value?.target?.projects,
      targetIncome: stats.value?.target?.income,
      statsKeys: Object.keys(monthlyStore.stats),
      currentStats: monthlyStore.stats[props.currentTab + '-01'],
      dataSyncStatus: 'ensured'
    })
  } catch (error) {
    errorLog('統計データ読み込みエラー:', error)
  } finally {
    isLoadingStats.value = false
  }
}

// Phase 3: データ取得ロジック - ローディング状態管理を統一（ストアloadingのみ使用）
const loadData = async () => {
  if (isLoadingTargets.value || isLoadingStats.value) return
  
  try {
    if (props.currentTab === 'overview') {
      // overviewタブ: 既存の方法を維持
      const response = await monthlyStore.fetchOverview()
      // Step 1-3修正: undefinedの場合のデフォルト値設定
      overviewData.value = response || {
        total_projects: 0,
        total_income: 0,
        recent_months: []
      }
    } else if (monthlyStore.USE_NEW_API) {
      // Phase 2: 新API使用時 - 既存データから取得（3ヶ月分は初期化時に取得済み）
      const monthKey = props.currentTab + '-01'
      stats.value = monthlyStore.getStatsByMonth(monthKey)
      
      // データがない場合のみAPI呼び出し（フォールバック）
      if (!stats.value) {
        debugLog('🔧 データ未取得のため、fetchCurrentMonthlyData()を呼び出し')
        await monthlyStore.fetchCurrentMonthlyData()
        stats.value = monthlyStore.getStatsByMonth(monthKey)
      }
      
      // デバッグログ追加
      debugLog('月次統計データ（新API）:', {
        tab: props.currentTab,
        monthKey,
        stats: stats.value,
        targets: monthlyStore.targets
      })
    } else {
      // 旧API使用時: 既存の方法を維持（後方互換性）
      const [year, month] = props.currentTab.split('-')
      
      isLoadingTargets.value = true
      await monthlyStore.fetchTargets(parseInt(year), [parseInt(month)])
      isLoadingTargets.value = false
      
      isLoadingStats.value = true
      await monthlyStore.fetchStats(parseInt(year), parseInt(month))
      isLoadingStats.value = false
      
      // nextTickを使用してリアクティブ更新を確実にする
      await nextTick()
      stats.value = monthlyStore.getStatsByMonth(props.currentTab + '-01')
      
      // デバッグログ追加
      debugLog('月次統計データ（旧API）:', {
        tab: props.currentTab,
        year: parseInt(year),
        month: parseInt(month),
        stats: stats.value,
        targets: monthlyStore.targets
      })
    }
  } catch (error) {
    errorLog('データ読み込みエラー:', error)
  } finally {
    // Phase 3: ローディング状態管理を統一（ストアloadingのみ使用）
    isLoadingTargets.value = false
    isLoadingStats.value = false
  }
}

const openTargetSettings = () => {
  // 設定モーダルを開き、月次目標タブを選択
  uiStore.openSettings()
  uiStore.setSettingsTab('monthly-target')
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ja-JP').format(amount)
}

watch(() => props.currentTab, () => {
  loadData()
})

// Phase 3: 不要なwatchを削除（根本解決）
// 月次統計は履歴ベースで計算されるため、プロジェクト・請求書の変更時に再取得する必要はない
// ステータス変更時にバックエンドで自動更新される（monthly_summary_updater.py）
// 削除: watch(() => projectsStore.projects) - 不要な再取得を防止
// 削除: watch(() => invoicesStore.invoices) - 不要な再取得を防止

// 月次目標データ（当該月キー）の変更を監視し、統計を強制再取得
watch(
  () => {
    if (props.currentTab === 'overview') return null
    const monthKey = props.currentTab + '-01'
    return monthlyStore.targets[monthKey] || null
  },
  async (newVal, oldVal) => {
    if (props.currentTab === 'overview') return
    // 値の変化（作成・更新）時のみ再取得
    if (newVal) {
      debugLog('目標データ（当該月）変更検知 - 統計を強制再取得:', {
        tab: props.currentTab,
        monthKey: props.currentTab + '-01',
        newTarget: newVal
      })
      const [year, month] = props.currentTab.split('-')
      await monthlyStore.fetchStats(parseInt(year), parseInt(month), true)
      await nextTick()
      stats.value = monthlyStore.getStatsByMonth(props.currentTab + '-01')
      debugLog('統計データ更新完了（目標即時反映）:', {
        targetProjects: stats.value?.target?.projects,
        targetIncome: stats.value?.target?.income
      })
    }
  },
  { deep: false }
)

// 月次切り替え状態の監視（新規追加）

// Phase 3: 初期化時のデータ取得を最適化（統一・同一化 > 特殊独自）
// 新API (`/api/monthly/current`) の使用を徹底し、初期化時の重複呼び出しを削減
onMounted(async () => {
  // Phase 3: 新API使用時は初期化時に1回のみ取得（重複呼び出しを削減）
  if (monthlyStore.USE_NEW_API) {
    // fetchCurrentMonthlyData()は既にストアのloadingを管理
    // loadData()でデータが取得済みか確認し、必要時のみAPI呼び出し
    if (!monthlyStore.stats || Object.keys(monthlyStore.stats).length === 0) {
      await monthlyStore.fetchCurrentMonthlyData()
    }
  }
  // loadData()は既存データから取得を試み、データがない場合のみAPI呼び出し（フォールバック）
  loadData()
})
</script>

<style scoped>
.monthly-stats-section {
  /* スムーズなトランジション */
  transition: all 0.3s ease-in-out;
}

.stat-card {
  /* カードのホバーエフェクト */
  transition: transform 0.2s ease-in-out;
}

.stat-card:hover {
  transform: translateY(-2px);
}
</style>
