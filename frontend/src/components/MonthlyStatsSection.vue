<template>
  <div v-if="!loading" class="monthly-stats-section berry-card rounded-b-lg p-6">
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
          :target="stats?.target.projects || 0"
          unit="件"
          icon="box"
        />
        
        <ProgressBar 
          label="完了案件"
          :current="stats?.actual.completed_projects || 0"
          :target="stats?.target.projects || 0"
          unit="件"
          icon="check"
        />
        
        <ProgressBar 
          label="請求額"
          :current="stats?.actual.sent_invoices_amount || 0"
          :target="stats?.target.income || 0"
          unit="円"
          icon="currency"
        />
      </div>
    </div>
  </div>
  
  <!-- ローディング -->
  <div v-else class="flex justify-center items-center py-12">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500"></div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useMonthlyStore } from '@/stores/monthly'
import { useUIStore } from '@/stores/ui'
import { useProjectsStore } from '@/stores/projects'
import { useInvoicesStore } from '@/stores/invoices'
import { useMonthlyRotationStore } from '@/stores/monthlyRotation'
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

const loading = ref(false)
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

// 統計データのみ取得（無限ループ防止用）
const loadStatsOnly = async () => {
  if (props.currentTab === 'overview' || isLoadingStats.value) return
  
  isLoadingStats.value = true
  loading.value = true
  
  try {
    const [year, month] = props.currentTab.split('-')
    
    // データ同期の確実化（ステータス変更履歴による複雑な集計処理対応）
    // 1. 統計データを強制的に再取得
    await monthlyStore.fetchStats(parseInt(year), parseInt(month))
    
    // 2. データ同期の確実化（複数のnextTickを使用）
    await nextTick()
    stats.value = monthlyStore.getStatsByMonth(props.currentTab + '-01')
    await nextTick() // 追加のnextTick
    
    // 3. 強制的なUI更新
    await nextTick()
    
    // 4. データ同期の最終確認
    await nextTick()
    stats.value = monthlyStore.getStatsByMonth(props.currentTab + '-01')
    await nextTick()
    
    // デバッグログ追加
    console.log('統計データ更新完了 - データ同期確実化:', {
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
    console.error('統計データ読み込みエラー:', error)
  } finally {
    loading.value = false
    isLoadingStats.value = false
  }
}

const loadData = async () => {
  if (isLoadingTargets.value || isLoadingStats.value) return
  
  loading.value = true
  
  try {
    if (props.currentTab === 'overview') {
      const response = await monthlyStore.fetchOverview()
      overviewData.value = response
    } else {
      const [year, month] = props.currentTab.split('-')
      
      // 目標データと統計データを同時に取得
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
      console.log('月次統計データ:', {
        tab: props.currentTab,
        year: parseInt(year),
        month: parseInt(month),
        stats: stats.value,
        targets: monthlyStore.targets
      })
    }
  } catch (error) {
    console.error('データ読み込みエラー:', error)
  } finally {
    loading.value = false
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

// プロジェクトデータの変更を監視して月次統計を自動更新
watch(() => projectsStore.projects, () => {
  // プロジェクトデータが更新されたら月次統計も再取得
  if (props.currentTab !== 'overview') {
    loadData()
  }
}, { deep: true })

// 請求書データの変更を監視して月次統計を自動更新
watch(() => invoicesStore.invoices, () => {
  // 請求書データが更新されたら月次統計も再取得
  if (props.currentTab !== 'overview') {
    loadData()
  }
}, { deep: true })

// 月次目標データの変更を監視して月次統計を自動更新
watch(() => monthlyStore.targets, async (newTargets, oldTargets) => {
  // 実際にデータが変更された場合のみ実行（無限ループ防止）
  if (props.currentTab !== 'overview' && newTargets !== oldTargets) {
    console.log('目標データ変更検知 - データ同期確実化:', {
      tab: props.currentTab,
      newTargets,
      oldTargets
    })
    
    // データ同期の確実化（ステータス変更履歴による複雑な集計処理対応）
    // 1. 強制的なデータ同期（リアクティブ更新の強制）
    stats.value = null
    await nextTick()
    
    // 2. 統計データを強制的に再取得（target同期問題の解決）
    await new Promise(resolve => setTimeout(resolve, 50))
    await loadStatsOnly()
    
    // 3. 強制的なUI更新（複数のnextTickを使用）
    await nextTick()
    await nextTick()
    
    // 4. データ同期の最終確認
    await nextTick()
    stats.value = monthlyStore.getStatsByMonth(props.currentTab + '-01')
    await nextTick()
    
    console.log('統計データ更新完了 - データ同期確実化:', {
      tab: props.currentTab,
      stats: stats.value,
      targets: monthlyStore.targets,
      targetProjects: stats.value?.target?.projects,
      targetIncome: stats.value?.target?.income,
      statsKeys: Object.keys(monthlyStore.stats),
      currentStats: monthlyStore.stats[props.currentTab + '-01'],
      dataSyncStatus: 'ensured'
    })
  }
}, { deep: true })

// 月次切り替え状態の監視（新規追加）

onMounted(() => {
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
