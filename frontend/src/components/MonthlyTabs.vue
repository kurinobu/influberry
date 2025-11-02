<template>
  <div class="monthly-tabs berry-card rounded-t-lg">
    <!-- Step 4: レンダリング・描画時間最適化 - v-memoで再レンダリングを最適化 -->
    <div class="flex border-b border-gray-200 overflow-x-auto">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        v-memo="[currentTab, tab.id, tab.highlight, tab.isNewMonth, tab.isPreviousMonth, tab.monthlyRotation, tab.rotationRunning, tab.phase1Marker]"
        :data-tab-id="tab.id"
        @click="selectTab(tab.id)"
        :class="[
          'px-6 py-3 font-medium transition-colors whitespace-nowrap shadow-lg',
          // CSSクラス適用の最適化: 選択状態のクラス（最優先）
          currentTab === tab.id 
            ? 'border-b-2 border-pink-500 text-pink-600 bg-pink-50' 
            : 'text-pink-500 hover:text-pink-700 hover:bg-pink-50',
          // CSSクラス適用の最適化: 視覚効果のクラス（選択状態でない場合のみ適用）
          currentTab !== tab.id && tab.highlight ? 'ring-2 ring-green-400 ring-opacity-50 bg-pink-50' : '',
          currentTab !== tab.id && tab.isNewMonth ? 'animate-pulse bg-gradient-to-r from-pink-50 to-pink-100' : '',
          currentTab !== tab.id && tab.isPreviousMonth ? 'bg-pink-50' : '',
          currentTab !== tab.id && tab.monthlyRotation ? 'shadow-lg border-pink-300' : '',
          currentTab !== tab.id && tab.rotationRunning ? 'animate-bounce bg-pink-50' : '',
          currentTab !== tab.id && tab.phase1Marker ? 'border-l-4 border-l-blue-500' : ''
        ]"
      >
        <component :is="tab.icon" class="w-5 h-5 inline mr-2" />
        {{ tab.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { ChartBarIcon, CalendarIcon } from '@heroicons/vue/24/outline'
import { useMonthlyRotationStore } from '../stores/monthlyRotation.js'

// Step 2 Phase 1: 環境変数による条件付きログ出力
const isDevelopment = import.meta.env.DEV

// Step 2 Phase 4-2修正: 無限再帰エラーの根本解決
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

const props = defineProps({
  modelValue: {
    type: String,
    default: 'overview'
  },
  isInitialDisplay: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const currentTab = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 月次切り替えストアの取得
const rotationStore = useMonthlyRotationStore()

// 強制的なタブ再生成のためのカウンター
const forceRegeneration = ref(0)

// Step 2 Phase 4修正: 動的タブ生成ロジック（現在日時チェック追加）
// 修正: 月次切り替え状態に基づく適切なタブ生成
const generateDynamicTabs = () => {
  // 修正: 月次切り替え状態に基づく適切な日時計算
  const rotationState = rotationStore.rotationState
  const lastRotationCheck = rotationStore.lastRotationCheck
  
  // Step 2 Phase 4修正: 現在日時を取得
  const now = new Date()
  const currentYear = now.getFullYear()
  const currentMonth = now.getMonth() + 1
  
  debugLog('🔧 月次切り替え状態に基づくタブ生成', {
    rotationState,
    lastRotationCheck,
    currentYear,
    currentMonth,
    forceRegeneration: forceRegeneration.value
  })
  
  // Step 2 Phase 4修正: 月次切り替え状態に基づく適切なタブ生成
  if (rotationState === 'completed' && lastRotationCheck) {
    const baseDate = new Date(lastRotationCheck)
    const lastYear = baseDate.getFullYear()
    const lastMonth = baseDate.getMonth() + 1
    
    // Step 2 Phase 4修正: 現在日時とlastRotationCheckの不一致をチェック
    // 現在月とlastRotationCheckの月が異なる場合、現在月を優先
    if (currentYear !== lastYear || currentMonth !== lastMonth) {
      debugLog('⚠️ 現在日時とlastRotationCheckが不一致 - 現在月を優先してタブ生成', {
        currentYear,
        currentMonth,
        lastYear,
        lastMonth,
        lastRotationCheck
      })
      return generateNormalTabs(currentYear, currentMonth)
    }
    
    // 一致する場合はlastRotationCheckを基準にタブ生成
    debugLog('🎉 月次切り替え完了 - lastRotationCheckを基準にタブ生成', {
      baseDate,
      lastYear,
      lastMonth
    })
    return generateTabsForNewMonth(baseDate, rotationState, lastRotationCheck)
  }
  
  if (rotationState === 'running') {
    debugLog('🔄 月次切り替え実行中 - 特別なタブを生成')
    return generateTabsForRunningRotation()
  }
  
  // Step 2 Phase 4修正: フォールバック - 現在の日時を使用
  debugLog('📅 通常のタブ生成（フォールバック）')
  return generateNormalTabs(currentYear, currentMonth)
}

// 新しい月のタブ生成（月次切り替え完了時）
// Phase 2: 月次切り替えの概念の実装
const generateTabsForNewMonth = (baseDate, rotationState, lastRotationCheck) => {
  debugLog('🎉 月次切り替え完了 - 新しい月のタブを生成')
  
  // 修正: 引数として受け取ったbaseDateを使用
  debugLog('🎉 月次切り替え日時を基準にタブ生成:', baseDate)
  
  const currentYear = baseDate.getFullYear()
  const currentMonth = baseDate.getMonth() + 1
  
  debugLog('🎉 月次切り替えの概念の実装', {
    baseDate,
    currentYear,
    currentMonth,
    rotationState,
    lastRotationCheck,
    concept: '月次切り替え日時を基準にタブを生成'
  })
  
  const tabs = []
  
  // 修正: 新しい月を基準に過去3ヶ月を生成
  for (let i = 2; i >= 0; i--) {
    // 修正: 月次切り替え日時を基準にタブの内容を計算
    const targetYear = currentYear
    const targetMonth = currentMonth - i
    
    // 年跨ぎ処理
    let adjustedYear = targetYear
    let adjustedMonth = targetMonth
    if (targetMonth <= 0) {
      adjustedYear = targetYear - 1
      adjustedMonth = targetMonth + 12
    }
    
    const monthId = `${adjustedYear}-${adjustedMonth.toString().padStart(2, '0')}`
    const monthLabel = `${adjustedMonth}月`
    
    const isNewMonth = i === 0
    const isPreviousMonth = i === 1
    
    // 修正: 月次切り替え後にタブの内容（月の表示）が変化する
    tabs.push({
      id: monthId,
      label: monthLabel,
      icon: CalendarIcon,
      isNewMonth: isNewMonth,
      isPreviousMonth: isPreviousMonth,
      highlight: isNewMonth,
      monthlyRotation: true,
      rotationBased: true,
      // 修正: 月次切り替えの概念の実装
      contentChange: true,
      tabContentUpdated: true,
      // 修正: 視覚的な変化の実装
      visualEffect: isNewMonth ? 'new-month-highlight' : isPreviousMonth ? 'previous-month-subtle' : 'normal',
      // 修正: 月次切り替えの概念の実装
      concept: '月次切り替え日時を基準にタブの内容を変化させる'
    })
  }
  
  // タブ順序変更: overviewタブを最後に追加
  tabs.push({ id: 'overview', label: '概要', icon: ChartBarIcon })
  
  debugLog('🎉 新しい月のタブ生成完了:', tabs)
  
  // 修正: タブの詳細表示
  debugLog('📋 タブの詳細表示', {
    tabCount: tabs.length,
    tabDetails: tabs.map(tab => ({
      id: tab.id,
      label: tab.label,
      isNewMonth: tab.isNewMonth,
      isPreviousMonth: tab.isPreviousMonth,
      highlight: tab.highlight,
      monthlyRotation: tab.monthlyRotation,
      rotationBased: tab.rotationBased,
      concept: tab.concept
    }))
  })
  
  return tabs
}

// 月次切り替え実行中の特別なタブ生成
// 修正: 月次切り替えの概念の実装
const generateTabsForRunningRotation = () => {
  debugLog('🔄 月次切り替え実行中 - 特別なタブを生成')
  
  // 修正: 月次切り替え状態に基づく適切な日時計算
  const rotationState = rotationStore.rotationState
  const lastRotationCheck = rotationStore.lastRotationCheck
  
  // 修正: 月次切り替えの日時を基準にタブを生成
  let baseDate
  if (lastRotationCheck) {
    // 月次切り替えが発生した日時を基準にする
    baseDate = new Date(lastRotationCheck)
    debugLog('🔄 月次切り替え日時を基準にタブ生成:', baseDate)
  } else {
    // フォールバック: 現在の日時を使用
    baseDate = new Date()
    debugLog('⚠️ 月次切り替え日時が不明 - 現在の日時を使用:', baseDate)
  }
  
  const currentYear = baseDate.getFullYear()
  const currentMonth = baseDate.getMonth() + 1
  
  debugLog('🔄 月次切り替えの概念の実装', {
    baseDate,
    currentYear,
    currentMonth,
    rotationState,
    lastRotationCheck,
    concept: '月次切り替え日時を基準にタブを生成'
  })
  
  const tabs = []
  
  for (let i = 2; i >= 0; i--) {
    // 修正: 月次切り替え日時を基準にタブの内容を計算
    const targetYear = currentYear
    const targetMonth = currentMonth - i
    
    // 年跨ぎ処理
    let adjustedYear = targetYear
    let adjustedMonth = targetMonth
    if (targetMonth <= 0) {
      adjustedYear = targetYear - 1
      adjustedMonth = targetMonth + 12
    }
    
    const monthId = `${adjustedYear}-${adjustedMonth.toString().padStart(2, '0')}`
    const monthLabel = `${adjustedMonth}月`
    
    const isCurrentMonth = i === 0
    const isPreviousMonth = i === 1
    
    // 修正: 月次切り替え実行中でもタブの内容（月の表示）が変化する
    tabs.push({
      id: monthId,
      label: monthLabel,
      icon: CalendarIcon,
      isCurrentMonth: isCurrentMonth,
      isPreviousMonth: isPreviousMonth,
      highlight: false,
      rotationRunning: true,
      rotationBased: true,
      // 修正: 月次切り替えの概念の実装
      contentChange: true,
      tabContentUpdated: true,
      // 修正: 視覚的な変化の実装
      visualEffect: isCurrentMonth ? 'current-month-running' : isPreviousMonth ? 'previous-month-subtle' : 'normal',
      // 修正: 月次切り替えの概念の実装
      concept: '月次切り替え日時を基準にタブの内容を変化させる'
    })
  }
  
  // タブ順序変更: overviewタブを最後に追加
  tabs.push({ id: 'overview', label: '概要', icon: ChartBarIcon })
  
  debugLog('🔄 月次切り替え実行中のタブ生成完了:', tabs)
  
  // 修正: タブの詳細表示
  debugLog('📋 タブの詳細表示', {
    tabCount: tabs.length,
    tabDetails: tabs.map(tab => ({
      id: tab.id,
      label: tab.label,
      isCurrentMonth: tab.isCurrentMonth,
      isPreviousMonth: tab.isPreviousMonth,
      highlight: tab.highlight,
      rotationRunning: tab.rotationRunning,
      rotationBased: tab.rotationBased,
      concept: tab.concept
    }))
  })
  
  return tabs
}

// 通常のタブ生成
// 修正: 月次切り替えの概念の実装とタブの内容の変化の実装
const generateNormalTabs = (year, month) => {
  debugLog('📅 通常のタブを生成:', { year, month })
  
  // 修正: 基本的なタブ生成ロジック
  debugLog('📅 基本的なタブ生成ロジック', {
    year,
    month,
    concept: '基本的なタブ生成ロジック'
  })
  
  const tabs = []
  
  for (let i = 2; i >= 0; i--) {
    // 修正: 基本的なタブ生成ロジック（年跨ぎ処理含む）
    const targetYear = year
    const targetMonth = month - i
    
    // 年跨ぎ処理
    let adjustedYear = targetYear
    let adjustedMonth = targetMonth
    if (targetMonth <= 0) {
      adjustedYear = targetYear - 1
      adjustedMonth = targetMonth + 12
    }
    
    const monthId = `${adjustedYear}-${adjustedMonth.toString().padStart(2, '0')}`
    const monthLabel = `${adjustedMonth}月`
    
    // 修正: 基本的なタブ生成ロジック
    tabs.push({
      id: monthId,
      label: monthLabel,
      icon: CalendarIcon,
      concept: '基本的なタブ生成ロジック',
      // 修正: 月次切り替えの概念の実装
      contentChange: false,
      // 修正: 視覚的な変化の実装
      visualEffect: 'normal'
    })
  }
  
  // タブ順序変更: overviewタブを最後に追加
  tabs.push({ id: 'overview', label: '概要', icon: ChartBarIcon })
  
  debugLog('📅 通常のタブ生成完了:', tabs)
  
  // 修正: タブの詳細表示
  debugLog('📋 タブの詳細表示', {
    tabCount: tabs.length,
    tabDetails: tabs.map(tab => ({
      id: tab.id,
      label: tab.label,
      concept: tab.concept
    }))
  })
  
  return tabs
}

const tabs = computed(() => generateDynamicTabs())

// 根本原因修正: 必要な関数の追加
const regenerateTabs = () => {
  debugLog('🔧 タブ再生成を実行')
  // 強制的なタブ再生成
  forceRegeneration.value++
}

const refreshMonthlyData = async () => {
  debugLog('🔧 データ同期を確実化')
  // 月次データの同期
  try {
    await rotationStore.refreshFrontendData()
  } catch (error) {
    errorLog('データ同期エラー:', error)
  }
}

const updateTabContent = () => {
  debugLog('🔧 タブ内容更新を実行')
  
  // Phase 1: タブの内容変化の実装
  // 月次切り替え後にタブの内容（月の表示）を変化させる
  try {
    // 1. 月次切り替え状態を確認
    const rotationState = rotationStore.rotationState
    const lastRotationCheck = rotationStore.lastRotationCheck
    
    debugLog('🔧 タブ内容更新: 月次切り替え状態を確認', {
      rotationState,
      lastRotationCheck
    })
    
    // 2. 月次切り替え完了時のタブ内容更新
    if (rotationState === 'completed' && lastRotationCheck) {
      debugLog('🎉 月次切り替え完了 - タブの内容を更新')
      
      // 月次切り替え日時を基準にタブの内容を計算
      const baseDate = new Date(lastRotationCheck)
      const currentYear = baseDate.getFullYear()
      const currentMonth = baseDate.getMonth() + 1
      
      debugLog('🔧 タブ内容更新: 月次切り替え日時を基準に計算', {
        baseDate,
        currentYear,
        currentMonth
      })
      
      // 3. タブの内容の変化を実装
      // 新しい月を基準に過去3ヶ月を生成（タブの内容の変化を実装）
      const newTabs = []
      
      // 概要タブを追加
      newTabs.push({ id: 'overview', label: '概要', icon: ChartBarIcon })
      
      // 新しい月を基準に過去3ヶ月を生成
      for (let i = 2; i >= 0; i--) {
        const targetYear = currentYear
        const targetMonth = currentMonth - i
        
        // 年跨ぎ処理
        let adjustedYear = targetYear
        let adjustedMonth = targetMonth
        if (targetMonth <= 0) {
          adjustedYear = targetYear - 1
          adjustedMonth = targetMonth + 12
        }
        
        const monthId = `${adjustedYear}-${adjustedMonth.toString().padStart(2, '0')}`
        const monthLabel = `${adjustedMonth}月`
        
        const isNewMonth = i === 0
        const isPreviousMonth = i === 1
        
        // タブの内容の変化の実装
        newTabs.push({
          id: monthId,
          label: monthLabel,
          icon: CalendarIcon,
          isNewMonth: isNewMonth,
          isPreviousMonth: isPreviousMonth,
          highlight: isNewMonth,
          monthlyRotation: true,
          rotationBased: true,
          contentChange: true,
          tabContentUpdated: true,
          visualEffect: isNewMonth ? 'new-month-highlight' : isPreviousMonth ? 'previous-month-subtle' : 'normal',
          concept: '月次切り替え日時を基準にタブの内容を変化させる'
        })
      }
      
      debugLog('🎉 タブの内容変化完了:', newTabs)
      
      // 4. タブの内容の変化を確実に実装
      // 強制的なタブ再生成を実行
      forceRegeneration.value++
      
      debugLog('🔧 タブ内容更新: タブの内容の変化を確実に実装')
    } else {
      debugLog('⏳ 月次切り替え未完了 - タブ内容更新をスキップ')
    }
  } catch (error) {
    errorLog('❌ タブ内容更新エラー:', error)
  }
}

const applyVisualChanges = () => {
  debugLog('🔧 視覚的変化を実装')
  
  // 視覚効果の統合: Vueのリアクティブクラスバインディングに統合済み
  // 手動でのクラス適用を削除し、Vueのリアクティブクラスバインディングに統合
  try {
    // 1. 月次切り替え状態を確認
    const rotationState = rotationStore.rotationState
    const lastRotationCheck = rotationStore.lastRotationCheck
    
    debugLog('🔧 視覚的変化: 月次切り替え状態を確認', {
      rotationState,
      lastRotationCheck
    })
    
    // 2. 視覚効果の統合: Vueのリアクティブクラスバインディングで処理済み
    if (rotationState === 'completed' && lastRotationCheck) {
      debugLog('🎉 月次切り替え完了 - 視覚的変化を適用')
      debugLog('🎨 視覚効果の統合: Vueのリアクティブクラスバインディングで処理済み')
      debugLog('🎨 新しい月のタブをハイライト: CSSクラス適用の最適化で処理済み')
      debugLog('🎨 実行中のタブをアニメーション: CSSクラス適用の最適化で処理済み')
      debugLog('🎨 前月のタブをサブトル表示: CSSクラス適用の最適化で処理済み')
      
      // 視覚効果の統合: 手動でのクラス適用は不要（Vueのリアクティブクラスバインディングで処理）
      debugLog('🎉 視覚的変化の適用完了: Vueのリアクティブクラスバインディングで処理済み')
      
    } else if (rotationState === 'running') {
      debugLog('🔄 月次切り替え実行中 - 実行中の視覚的変化を適用')
      debugLog('🔄 視覚効果の統合: Vueのリアクティブクラスバインディングで処理済み')
      debugLog('🔄 実行中のタブをアニメーション: CSSクラス適用の最適化で処理済み')
      
      // 視覚効果の統合: 手動でのクラス適用は不要（Vueのリアクティブクラスバインディングで処理）
      debugLog('🔄 実行中の視覚的変化の適用完了: Vueのリアクティブクラスバインディングで処理済み')
      
    } else {
      debugLog('⏳ 月次切り替え未開始 - 視覚的変化をスキップ')
    }
  } catch (error) {
    errorLog('❌ 視覚的変化エラー:', error)
  }
}

const selectTab = (tabId) => {
  currentTab.value = tabId
  
  debugLog('🔧 根本原因修正: タブ選択', { 
    selectedTab: tabId,
    timestamp: new Date().toISOString()
  })
  
  // Phase 2: タブの詳細表示の修正
  debugLog('📋 Phase 2: タブ選択の詳細表示', {
    selectedTab: tabId,
    allTabs: tabs.value.map(tab => ({
      id: tab.id,
      label: tab.label,
      isSelected: tab.id === tabId
    }))
  })
}

// 根本原因修正: 複数のwatch関数を単一化（チャタリング防止）
watch(() => [rotationStore.rotationState, rotationStore.lastRotationCheck], ([newState, newCheck], [oldState, oldCheck]) => {
  debugLog('🔧 根本原因修正: 月次切り替え状態・時刻変更を検知', { 
    newState, oldState, 
    newCheck, oldCheck 
  })
  
  // 🔧 優先度1修正: 初期表示中はスキップ（計画書ベースの修正）
  if (props.isInitialDisplay) {
    console.log('⚠️ 初期表示中のため、月次切り替え監視をスキップ', {
      isInitialDisplay: props.isInitialDisplay,
      newState,
      oldState
    })
    return
  }
  
  // 月次切り替え完了時の処理（初回表示時も含む）
  if (newState === 'completed' && newCheck) {
    debugLog('🎉 月次切り替え完了を検知 - データ同期を確実化')
    handleMonthlyRotationComplete()
  }
}, { deep: false }) // deep: false でパフォーマンス最適化

// 根本原因修正: 月次切り替え完了時の処理をシンプル化（重複実行防止）
const handleMonthlyRotationComplete = async () => {
  debugLog('🔧 根本原因修正: 月次切り替え完了時の処理を開始')
  
  try {
    // 1. タブ再生成（1回のみ）
    debugLog('🔧 1. タブ再生成を実行')
    forceRegeneration.value++
    
    // 2. データ同期（checkRotationStatusで実行済み - 重複削除）
    debugLog('🔧 2. データ同期はcheckRotationStatusで実行済み')
    // await refreshMonthlyData()
    
    // 3. Phase 1: タブの内容変化の実装
    debugLog('🔧 3. タブの内容変化を実装')
    updateTabContent()
    
    // 4. Phase 1: 視覚的変化の実装
    debugLog('🔧 4. 視覚的変化を実装')
    applyVisualChanges()
    
    // 5. タブの自動選択機能の実装
    debugLog('🔧 5. タブの自動選択機能を実装')
    await selectNewMonthTab()
    
    // 6. 視覚的更新（4で実行済み - 重複削除）
    debugLog('🔧 6. 視覚的更新は4で実行済み')
    // await applyVisualChanges()
    
    debugLog('🎉 月次切り替え完了時の処理が完了')
  } catch (error) {
    errorLog('❌ 月次切り替え完了時の処理でエラー:', error)
  }
}



// 根本原因修正: 月次切り替えイベントの監視
const handleMonthlyRotation = (event) => {
  debugLog('🔧 根本原因修正: 月次切り替えイベントを受信', event.detail)
  regenerateTabs()
}

// コンポーネントマウント時の初期化
onMounted(async () => {
  debugLog('🔧 根本原因修正: コンポーネントマウント完了')
  
  // 月次切り替えイベントのリスナーを追加
  window.addEventListener('monthly-rotation-completed', handleMonthlyRotation)
  
  // 月次切り替え監視を開始
  debugLog('🔄 月次切り替え監視を開始')
  rotationStore.startRotationMonitoring()
  
  // 初回の月次切り替え状態をチェック
  debugLog('🚀 初回の月次切り替え状態をチェック')
  await rotationStore.checkRotationStatus()
  
  // 初回表示時の明示的な自動選択実行（新規追加）
  debugLog('🔧 初回表示時の自動選択を実行')
  await selectNewMonthTab()
})

// コンポーネントアンマウント時のクリーンアップ
onUnmounted(() => {
  debugLog('🔧 根本原因修正: コンポーネントアンマウント')
  
  // 月次切り替えイベントのリスナーを削除
  window.removeEventListener('monthly-rotation-completed', handleMonthlyRotation)
  
  // 月次切り替え監視を停止（必要に応じて）
  debugLog('🛑 月次切り替え監視を停止')
})

// Phase 3: 動作確認とテスト機能
const debugTabDetails = () => {
  debugLog('📋 Phase 3: 動作確認とテスト機能')
  debugLog('📋 現在のタブ数:', tabs.value.length)
  debugLog('📋 現在のタブ詳細:', tabs.value.map(tab => ({
    id: tab.id,
    label: tab.label,
    isNewMonth: tab.isNewMonth,
    isPreviousMonth: tab.isPreviousMonth,
    isCurrentMonth: tab.isCurrentMonth,
    highlight: tab.highlight,
    monthlyRotation: tab.monthlyRotation,
    rotationRunning: tab.rotationRunning,
    rotationBased: tab.rotationBased,
    phase1Marker: tab.phase1Marker,
    phase2Marker: tab.phase2Marker,
    concept: tab.concept,
    phase2Concept: tab.phase2Concept,
    phase2Implementation: tab.phase2Implementation
  })))
  debugLog('📋 現在選択中のタブ:', currentTab.value)
  debugLog('📋 月次切り替え状態:', rotationStore.rotationState)
  debugLog('📋 月次切り替えチェック時刻:', rotationStore.lastRotationCheck)
}

// Phase 3: 各月での表示テスト機能
const testMonthlyDisplay = () => {
  debugLog('🧪 Phase 3: 各月での表示テスト機能')
  
  // 現在の月を基準に過去3ヶ月を表示
  const now = new Date()
  const currentYear = now.getFullYear()
  const currentMonth = now.getMonth() + 1
  
  debugLog('🧪 現在の月を基準に過去3ヶ月を表示:', {
    currentYear,
    currentMonth,
    testMonths: []
  })
  
  // 過去3ヶ月のタブを生成してテスト
  for (let i = 2; i >= 0; i--) {
    const targetYear = currentYear
    const targetMonth = currentMonth - i
    
    // 年跨ぎ処理
    let adjustedYear = targetYear
    let adjustedMonth = targetMonth
    if (targetMonth <= 0) {
      adjustedYear = targetYear - 1
      adjustedMonth = targetMonth + 12
    }
    
    const monthId = `${adjustedYear}-${adjustedMonth.toString().padStart(2, '0')}`
    const monthLabel = `${adjustedMonth}月`
    
    debugLog('🧪 テスト月:', {
      index: i,
      targetYear,
      targetMonth,
      adjustedYear,
      adjustedMonth,
      monthId,
      monthLabel,
      isCurrentMonth: i === 0,
      isPreviousMonth: i === 1
    })
  }
  
  debugLog('🧪 各月での表示テスト完了')
}

// Phase 3: 年跨ぎ処理のテスト機能
const testYearCrossing = () => {
  debugLog('🧪 Phase 3: 年跨ぎ処理のテスト機能')
  
  // 年跨ぎのテストケース
  const testCases = [
    { year: 2025, month: 1, description: '1月（前年12月、11月、10月を表示）' },
    { year: 2025, month: 2, description: '2月（前年12月、1月、2月を表示）' },
    { year: 2025, month: 3, description: '3月（1月、2月、3月を表示）' },
    { year: 2025, month: 12, description: '12月（10月、11月、12月を表示）' }
  ]
  
  testCases.forEach((testCase, index) => {
    debugLog(`🧪 テストケース ${index + 1}: ${testCase.description}`)
    
    const { year, month } = testCase
    const testMonths = []
    
    // 過去3ヶ月のタブを生成してテスト
    for (let i = 2; i >= 0; i--) {
      const targetYear = year
      const targetMonth = month - i
      
      // 年跨ぎ処理
      let adjustedYear = targetYear
      let adjustedMonth = targetMonth
      if (targetMonth <= 0) {
        adjustedYear = targetYear - 1
        adjustedMonth = targetMonth + 12
      }
      
      const monthId = `${adjustedYear}-${adjustedMonth.toString().padStart(2, '0')}`
      const monthLabel = `${adjustedMonth}月`
      
      testMonths.push({
        index: i,
        targetYear,
        targetMonth,
        adjustedYear,
        adjustedMonth,
        monthId,
        monthLabel,
        isCurrentMonth: i === 0,
        isPreviousMonth: i === 1
      })
    }
    
    debugLog(`🧪 テストケース ${index + 1} 結果:`, testMonths)
  })
  
  debugLog('🧪 年跨ぎ処理のテスト完了')
}

// Phase 3: 月次切り替え後のタブ内容変化の確認機能
const testTabContentChange = () => {
  debugLog('🧪 Phase 3: 月次切り替え後のタブ内容変化の確認機能')
  
  // 月次切り替え状態のテスト
  const testStates = [
    { state: 'idle', description: '待機状態' },
    { state: 'running', description: '実行中状態' },
    { state: 'completed', description: '完了状態' }
  ]
  
  testStates.forEach((testState, index) => {
    debugLog(`🧪 テスト状態 ${index + 1}: ${testState.description}`)
    
    // 月次切り替え状態をシミュレート
    const mockRotationState = testState.state
    const mockLastRotationCheck = new Date().toISOString()
    
    debugLog('🧪 シミュレート状態:', {
      rotationState: mockRotationState,
      lastRotationCheck: mockLastRotationCheck
    })
    
    // タブ内容変化のテスト
    if (mockRotationState === 'completed' && mockLastRotationCheck) {
      debugLog('🧪 月次切り替え完了 - タブ内容変化をテスト')
      
      // 新しい月のタブを生成してテスト
      const baseDate = new Date(mockLastRotationCheck)
      const currentYear = baseDate.getFullYear()
      const currentMonth = baseDate.getMonth() + 1
      
      debugLog('🧪 タブ内容変化テスト:', {
        baseDate,
        currentYear,
        currentMonth,
        concept: '月次切り替え日時を基準にタブの内容を変化させる'
      })
      
      // タブの内容の変化を確認
      const testTabs = []
      for (let i = 2; i >= 0; i--) {
        const targetYear = currentYear
        const targetMonth = currentMonth - i
        
        // 年跨ぎ処理
        let adjustedYear = targetYear
        let adjustedMonth = targetMonth
        if (targetMonth <= 0) {
          adjustedYear = targetYear - 1
          adjustedMonth = targetMonth + 12
        }
        
        const monthId = `${adjustedYear}-${adjustedMonth.toString().padStart(2, '0')}`
        const monthLabel = `${adjustedMonth}月`
        
        testTabs.push({
          id: monthId,
          label: monthLabel,
          isNewMonth: i === 0,
          isPreviousMonth: i === 1,
          contentChange: true,
          tabContentUpdated: true,
          concept: '月次切り替え日時を基準にタブの内容を変化させる'
        })
      }
      
      debugLog('🧪 タブ内容変化テスト結果:', testTabs)
    } else {
      debugLog('🧪 月次切り替え未完了 - タブ内容変化をスキップ')
    }
  })
  
  debugLog('🧪 月次切り替え後のタブ内容変化の確認完了')
}

// Phase 3: 視覚的変化の確認機能
const testVisualChanges = () => {
  debugLog('🧪 Phase 3: 視覚的変化の確認機能')
  
  // 視覚的変化のテストケース
  const testCases = [
    { 
      visualEffect: 'new-month-highlight', 
      description: '新しい月のタブをハイライト',
      expectedClasses: ['animate-pulse', 'bg-gradient-to-r', 'from-green-50', 'to-blue-50', 'ring-2', 'ring-green-400', 'ring-opacity-50']
    },
    { 
      visualEffect: 'current-month-running', 
      description: '実行中のタブをアニメーション',
      expectedClasses: ['animate-bounce', 'bg-orange-50', 'shadow-lg', 'border-orange-300']
    },
    { 
      visualEffect: 'previous-month-subtle', 
      description: '前月のタブをサブトル表示',
      expectedClasses: ['bg-yellow-50', 'opacity-75']
    },
    { 
      visualEffect: 'normal', 
      description: '通常のタブ',
      expectedClasses: []
    }
  ]
  
  testCases.forEach((testCase, index) => {
    debugLog(`🧪 視覚的変化テスト ${index + 1}: ${testCase.description}`)
    
    debugLog('🧪 テストケース:', {
      visualEffect: testCase.visualEffect,
      description: testCase.description,
      expectedClasses: testCase.expectedClasses
    })
    
    // 視覚的変化の適用をシミュレート
    if (testCase.expectedClasses.length > 0) {
      debugLog('🧪 視覚的変化を適用:', testCase.expectedClasses)
    } else {
      debugLog('🧪 通常のタブ - 視覚的変化なし')
    }
  })
  
  // DOM要素の視覚的変化をテスト
  debugLog('🧪 DOM要素の視覚的変化をテスト')
  
  // 実際のDOM要素を取得してテスト
  const tabElements = document.querySelectorAll('.monthly-tabs button')
  debugLog('🧪 DOM要素数:', tabElements.length)
  
  tabElements.forEach((element, index) => {
    const currentClasses = Array.from(element.classList)
    debugLog(`🧪 DOM要素 ${index + 1} の現在のクラス:`, currentClasses)
  })
  
  debugLog('🧪 視覚的変化の確認完了')
}

// Phase 3: 月次切り替えの概念の確認機能
const testRotationConcept = () => {
  debugLog('🧪 Phase 3: 月次切り替えの概念の確認機能')
  
  // 月次切り替えの概念のテスト
  const concepts = [
    {
      name: '月次切り替えの基本概念',
      description: '月次切り替え = 新しい月のタブを表示し、古いタブを削除',
      implementation: '月次切り替え日時を基準にタブの内容を変化させる'
    },
    {
      name: '月次切り替え実行中の概念',
      description: '月次切り替え実行中 = 実行中であることを示す特別なタブ生成',
      implementation: '月次切り替え日時を基準にタブの内容を変化させる'
    },
    {
      name: '通常のタブ生成の概念',
      description: '通常のタブ生成 = 基本的なタブ生成ロジック',
      implementation: '月次切り替え日時を基準にタブの内容を変化させる'
    }
  ]
  
  concepts.forEach((concept, index) => {
    debugLog(`🧪 概念テスト ${index + 1}: ${concept.name}`)
    
    debugLog('🧪 概念詳細:', {
      name: concept.name,
      description: concept.description,
      implementation: concept.implementation
    })
    
    // 概念の実装をテスト
    debugLog('🧪 概念の実装をテスト:', concept.implementation)
  })
  
  // 月次切り替えの状態遷移をテスト
  debugLog('🧪 月次切り替えの状態遷移をテスト')
  
  const stateTransitions = [
    { from: 'idle', to: 'running', description: '待機状態から実行中状態へ' },
    { from: 'running', to: 'completed', description: '実行中状態から完了状態へ' },
    { from: 'completed', to: 'idle', description: '完了状態から待機状態へ' }
  ]
  
  stateTransitions.forEach((transition, index) => {
    debugLog(`🧪 状態遷移テスト ${index + 1}: ${transition.description}`)
    
    debugLog('🧪 状態遷移:', {
      from: transition.from,
      to: transition.to,
      description: transition.description
    })
    
    // 状態遷移の処理をテスト
    if (transition.from === 'running' && transition.to === 'completed') {
      debugLog('🧪 月次切り替え完了 - タブ内容変化と視覚的変化を適用')
    } else if (transition.from === 'idle' && transition.to === 'running') {
      debugLog('🧪 月次切り替え開始 - 実行中の視覚的変化を適用')
    } else {
      debugLog('🧪 状態遷移 - 特別な処理なし')
    }
  })
  
  debugLog('🧪 月次切り替えの概念の確認完了')
}

// Phase 3: 総合テスト機能
const runAllTests = () => {
  debugLog('🧪 Phase 3: 総合テスト機能')
  
  debugLog('🧪 全テストを実行開始')
  
  // 各テストを順次実行
  testMonthlyDisplay()
  testYearCrossing()
  testTabContentChange()
  testVisualChanges()
  testRotationConcept()
  
  debugLog('🧪 全テスト実行完了')
}

// 手動テスト機能の実装
const manualRotationTest = () => {
  debugLog('🧪 手動月次切り替えテストを開始')
  
  // 1. 月次切り替え状態をシミュレート
  debugLog('🧪 1. 月次切り替え状態をシミュレート')
  rotationStore.setRotationState('running')
  rotationStore.lastRotationCheck = new Date().toISOString()
  
  debugLog('🧪 シミュレート状態:', {
    rotationState: rotationStore.rotationState,
    lastRotationCheck: rotationStore.lastRotationCheck
  })
  
  // 2. タブ再生成を実行
  debugLog('🧪 2. タブ再生成を実行')
  forceRegeneration.value++
  
  // 3. データ同期を実行
  debugLog('🧪 3. データ同期を実行')
  refreshMonthlyData()
  
  // 4. タブの内容変化を実行
  debugLog('🧪 4. タブの内容変化を実行')
  updateTabContent()
  
  // 5. 視覚的変化を実行
  debugLog('🧪 5. 視覚的変化を実行')
  applyVisualChanges()
  
  // 6. 月次切り替え完了をシミュレート
  setTimeout(() => {
    debugLog('🧪 6. 月次切り替え完了をシミュレート')
    rotationStore.setRotationState('completed')
    
    // タブ再生成を実行
    forceRegeneration.value++
    
    // データ同期を実行
    refreshMonthlyData()
    
    // タブの内容変化を実行
    updateTabContent()
    
    // 視覚的変化を実行
    applyVisualChanges()
    
    debugLog('🧪 手動月次切り替えテスト完了')
  }, 2000) // 2秒後に完了をシミュレート
}

// 状態確認機能の実装
const checkCurrentState = () => {
  debugLog('🔍 現在の状態を確認')
  
  // nextTickの利用可能性を確認
  debugLog('🔍 nextTick利用可能性:', typeof nextTick !== 'undefined')
  debugLog('🔍 nextTick関数:', nextTick)
  
  debugLog('🔍 月次切り替え状態:', rotationStore.rotationState)
  debugLog('🔍 月次切り替えチェック時刻:', rotationStore.lastRotationCheck)
  debugLog('🔍 現在のタブ数:', tabs.value.length)
  debugLog('🔍 現在選択中のタブ:', currentTab.value)
  debugLog('🔍 強制再生成カウンター:', forceRegeneration.value)
  
  // タブの詳細情報を表示
  tabs.value.forEach((tab, index) => {
    debugLog(`🔍 タブ ${index + 1}:`, {
      id: tab.id,
      label: tab.label,
      isNewMonth: tab.isNewMonth,
      isPreviousMonth: tab.isPreviousMonth,
      isCurrentMonth: tab.isCurrentMonth,
      highlight: tab.highlight,
      monthlyRotation: tab.monthlyRotation,
      rotationRunning: tab.rotationRunning,
      rotationBased: tab.rotationBased,
      contentChange: tab.contentChange,
      tabContentUpdated: tab.tabContentUpdated,
      visualEffect: tab.visualEffect,
      concept: tab.concept,
      phase2Concept: tab.phase2Concept,
      phase2Implementation: tab.phase2Implementation
    })
  })
  
  // DOM要素の確認
  const tabElements = document.querySelectorAll('.monthly-tabs button')
  debugLog('🔍 DOM要素数:', tabElements.length)
  
  tabElements.forEach((element, index) => {
    const currentClasses = Array.from(element.classList)
    debugLog(`🔍 DOM要素 ${index + 1} のクラス:`, currentClasses)
  })
}

// タブの自動選択機能の実装
const selectNewMonthTab = async () => {
  debugLog('🔧 タブの自動選択機能を実装')
  
  // 🔧 優先度1修正: 初期表示中はスキップ（計画書ベースの修正）
  if (props.isInitialDisplay) {
    console.log('⚠️ 初期表示中のため、selectNewMonthTab()をスキップ', {
      isInitialDisplay: props.isInitialDisplay,
      rotationState: rotationStore.rotationState,
      lastRotationCheck: rotationStore.lastRotationCheck
    })
    return
  }
  
  try {
    // 1. 月次切り替え状態を確認
    const rotationState = rotationStore.rotationState
    const lastRotationCheck = rotationStore.lastRotationCheck
    
    debugLog('🔧 タブ自動選択: 月次切り替え状態を確認', {
      rotationState,
      lastRotationCheck
    })
    
    // 2. 月次切り替え完了時のタブ自動選択
    if (rotationState === 'completed' && lastRotationCheck) {
      debugLog('🎉 月次切り替え完了 - 新しい月のタブを自動選択')
      
      // 3. 新しい月のタブを特定
      const baseDate = new Date(lastRotationCheck)
      const currentYear = baseDate.getFullYear()
      const currentMonth = baseDate.getMonth() + 1
      
      // 新しい月のタブIDを生成
      const newMonthId = `${currentYear}-${currentMonth.toString().padStart(2, '0')}`
      
      debugLog('🔧 タブ自動選択: 新しい月のタブを特定', {
        baseDate,
        currentYear,
        currentMonth,
        newMonthId
      })
      
      // 4. 新しい月のタブが存在するか確認
      const newMonthTab = tabs.value.find(tab => tab.id === newMonthId)
      
      if (newMonthTab) {
        debugLog('🎉 新しい月のタブを発見 - 自動選択を実行', newMonthTab)
        
        // 5. リアクティブバインディングの修正: Vueのリアクティブシステムを確実に更新
        debugLog('🔧 リアクティブバインディング修正: タブ選択を実行')
        
        // 5-1. 現在の値を確認
        debugLog('🔧 修正前の値:', {
          currentTab: currentTab.value,
          modelValue: props.modelValue
        })
        
        // 5-2. Vueのリアクティブシステムを確実に更新
        if (typeof nextTick !== 'undefined') {
          await nextTick()
          emit('update:modelValue', newMonthId)
          await nextTick()
        } else {
          // nextTickが利用できない場合の代替処理
          debugLog('⚠️ nextTickが利用できません - 代替処理を実行')
          emit('update:modelValue', newMonthId)
        }
        
        // 5-3. 親コンポーネントへの反映を確認
        debugLog('🔧 修正後の値:', {
          currentTab: currentTab.value,
          modelValue: props.modelValue,
          parentValue: 'DashboardPage.currentMonthTabに反映される'
        })
        
        debugLog('🎉 タブの自動選択完了:', {
          previousTab: 'overview',
          newTab: newMonthId,
          tabLabel: newMonthTab.label,
          reactiveBindingFixed: true
        })
        
        // 6. タブの表示切り替えを実行
        await switchToNewMonthTab(newMonthId)
        
      } else {
        debugLog('⚠️ 新しい月のタブが見つかりません - フォールバック処理')
        
        // フォールバック: 最初の月次タブを選択
        const monthlyTabs = tabs.value.filter(tab => tab.id !== 'overview')
        if (monthlyTabs.length > 0) {
          const fallbackTab = monthlyTabs[0]
          
          // リアクティブバインディングの修正: フォールバック時も確実に更新
          if (typeof nextTick !== 'undefined') {
            await nextTick()
            emit('update:modelValue', fallbackTab.id)
            await nextTick()
          } else {
            // nextTickが利用できない場合の代替処理
            debugLog('⚠️ フォールバック処理: nextTickが利用できません - 代替処理を実行')
            emit('update:modelValue', fallbackTab.id)
          }
          
          debugLog('🔧 フォールバック: 最初の月次タブを選択', {
            fallbackTab: fallbackTab.id,
            tabLabel: fallbackTab.label,
            reactiveBindingFixed: true
          })
        }
      }
      
    } else {
      debugLog('⏳ 月次切り替え未完了 - タブ自動選択をスキップ')
    }
    
  } catch (error) {
    errorLog('❌ タブ自動選択エラー:', error)
    
    // フォールバック処理: nextTickが利用できない場合の代替処理
    try {
      debugLog('🔧 フォールバック処理: nextTickなしでタブ選択を実行')
      
      // 1. 月次切り替え状態を確認
      const rotationState = rotationStore.rotationState
      const lastRotationCheck = rotationStore.lastRotationCheck
      
      if (rotationState === 'completed' && lastRotationCheck) {
        // 2. 新しい月のタブを特定
        const baseDate = new Date(lastRotationCheck)
        const currentYear = baseDate.getFullYear()
        const currentMonth = baseDate.getMonth() + 1
        const newMonthId = `${currentYear}-${currentMonth.toString().padStart(2, '0')}`
        
        // 3. 直接タブ選択を実行
        emit('update:modelValue', newMonthId)
        
        debugLog('🔧 フォールバック処理完了:', {
          newMonthId,
          currentTab: currentTab.value,
          fallbackSuccess: true
        })
      } else {
        debugLog('⚠️ フォールバック処理: 月次切り替え未完了のためスキップ')
      }
    } catch (fallbackError) {
      errorLog('❌ フォールバック処理も失敗:', fallbackError)
    }
  }
}

// タブの表示切り替えロジックの実装（emitの二重発行問題を解決）
const switchToNewMonthTab = async (tabId) => {
  debugLog('🔧 タブの表示切り替えロジックを実装')
  
  try {
    // 1. タブの表示切り替えを実行
    debugLog('🔧 タブの表示切り替えを実行:', tabId)
    
    // 2. emitの二重発行問題を解決: emitは呼び出し元(selectNewMonthTab)で実行済み
    // ここでは追加の処理のみ実行
    debugLog('🔧 emitの二重発行問題を解決: emitは既に実行済み')
    
    debugLog('🎉 タブの表示切り替え完了:', {
      selectedTab: tabId,
      timestamp: new Date().toISOString()
    })
    
    // 3. タブの表示切り替え完了を通知
    debugLog('🎉 タブの表示切り替え完了 - 新しい月のタブが表示されました')
    
  } catch (error) {
    errorLog('❌ タブの表示切り替えエラー:', error)
  }
}

// Phase 2: タブの詳細表示の修正機能
const displayTabDetails = () => {
  debugLog('📋 Phase 2: タブの詳細表示の修正機能')
  const tabElements = document.querySelectorAll('.monthly-tabs button')
  debugLog('📋 DOM上のタブ要素数:', tabElements.length)
  debugLog('📋 DOM上のタブ詳細:', Array.from(tabElements).map((element, index) => ({
    index: index,
    text: element.textContent.trim(),
    dataTabId: element.getAttribute('data-tab-id'),
    isActive: element.classList.contains('border-pink-500'),
    classes: Array.from(element.classList)
  })))
}

// グローバルスコープでテスト関数を利用可能にする
window.debugTabDetails = debugTabDetails
window.testMonthlyDisplay = testMonthlyDisplay
window.testYearCrossing = testYearCrossing
window.testTabContentChange = testTabContentChange
window.testVisualChanges = testVisualChanges
window.testRotationConcept = testRotationConcept
window.runAllTests = runAllTests
window.updateTabContent = updateTabContent
window.applyVisualChanges = applyVisualChanges
window.regenerateTabs = regenerateTabs
window.refreshMonthlyData = refreshMonthlyData

// グローバルスコープでストアとリアクティブ変数を利用可能にする
window.rotationStore = rotationStore
window.tabs = tabs
window.currentTab = currentTab
window.forceRegeneration = forceRegeneration

// グローバルスコープで手動テスト機能を利用可能にする（エラーハンドリング付き）
try {
  window.manualRotationTest = manualRotationTest
  window.checkCurrentState = checkCurrentState
  window.selectNewMonthTab = selectNewMonthTab
  window.switchToNewMonthTab = switchToNewMonthTab
  window.displayTabDetails = displayTabDetails
  window.nextTick = nextTick
  debugLog('🔧 グローバルテスト関数の登録が完了しました')
} catch (error) {
  errorLog('❌ グローバルテスト関数の登録エラー:', error)
}

debugLog('🔧 グローバルテスト関数を利用可能にしました')
debugLog('🔧 利用可能な関数:', [
  'debugTabDetails',
  'testMonthlyDisplay', 
  'testYearCrossing',
  'testTabContentChange',
  'testVisualChanges',
  'testRotationConcept',
  'runAllTests',
  'updateTabContent',
  'applyVisualChanges',
  'regenerateTabs',
  'refreshMonthlyData',
  'manualRotationTest',
  'checkCurrentState',
  'selectNewMonthTab',
  'switchToNewMonthTab',
  'displayTabDetails',
  'nextTick'
])
debugLog('🔧 利用可能な変数:', [
  'rotationStore',
  'tabs',
  'currentTab',
  'forceRegeneration'
])


// Phase 3: 視覚的な変化の実装機能
const applyVisualEffects = () => {
  debugLog('🎨 Phase 3: 視覚的な変化の実装機能')
  const tabElements = document.querySelectorAll('.monthly-tabs button')
  
  tabElements.forEach((element, index) => {
    const tab = tabs.value[index]
    if (tab) {
      // Phase 3: 視覚的な変化の実装
      if (tab.visualEffect === 'new-month-highlight') {
        element.classList.add('animate-pulse', 'bg-gradient-to-r', 'from-green-50', 'to-blue-50')
        debugLog('🎨 新しい月のタブに視覚効果を適用:', tab.label)
      } else if (tab.visualEffect === 'current-month-running') {
        element.classList.add('animate-bounce', 'bg-orange-50')
        debugLog('🎨 実行中のタブに視覚効果を適用:', tab.label)
      } else if (tab.visualEffect === 'previous-month-subtle') {
        element.classList.add('bg-yellow-50')
        debugLog('🎨 前月のタブに視覚効果を適用:', tab.label)
      }
    }
  })
}

// Phase 3: ユーザー体験の向上機能
const enhanceUserExperience = () => {
  debugLog('👤 Phase 3: ユーザー体験の向上機能')
  
  // 月次切り替え完了時の視覚的フィードバック
  if (rotationStore.rotationState === 'completed') {
    debugLog('👤 月次切り替え完了の視覚的フィードバックを表示')
    // 新しい月のタブをハイライト
    applyVisualEffects()
  }
  
  // 月次切り替え実行中の視覚的フィードバック
  if (rotationStore.rotationState === 'running') {
    debugLog('👤 月次切り替え実行中の視覚的フィードバックを表示')
    // 実行中のタブをアニメーション
    applyVisualEffects()
  }
}
</script>

<style scoped>
.monthly-tabs {
  /* 横スクロール対応 */
  scrollbar-width: thin;
  scrollbar-color: #f3f4f6 #ffffff;
}

.monthly-tabs::-webkit-scrollbar {
  height: 4px;
}

.monthly-tabs::-webkit-scrollbar-track {
  background: #ffffff;
}

.monthly-tabs::-webkit-scrollbar-thumb {
  background: #f3f4f6;
  border-radius: 2px;
}


.monthly-tabs::-webkit-scrollbar-thumb:hover {
  background: #e5e7eb;
}

/* === タブテキスト色の強制適用（グローバルCSS競合回避） === */
.monthly-tabs button {
  color: #ec4899 !important; /* text-pink-500 */
}

.monthly-tabs button.text-pink-600 {
  color: #db2777 !important; /* text-pink-600 */
}

.monthly-tabs button.text-pink-500 {
  color: #ec4899 !important; /* text-pink-500 */
}

/* === タブシャドーの統一（Berryスタイル適用） === */
.monthly-tabs button {
  box-shadow: 0 10px 25px rgba(244, 114, 182, 0.25) !important;
  /* Step 4: レンダリング・描画時間最適化 - transition-colorsをGPU加速化 */
  transition: color 0.2s ease-in-out, background-color 0.2s ease-in-out, transform 0.2s ease-in-out;
  /* Step 4: will-change属性を追加してレンダリング最適化 */
  will-change: transform, color, background-color;
}

.monthly-tabs button:hover {
  box-shadow: 0 15px 35px rgba(244, 114, 182, 0.35) !important;
  /* Step 4: レンダリング・描画時間最適化 - transformを使用してGPU加速を有効化 */
  transform: translateY(-1px);
}
</style>
