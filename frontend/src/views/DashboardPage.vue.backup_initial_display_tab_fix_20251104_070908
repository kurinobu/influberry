<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useProjectsStore } from '../stores/projects.js'
import { useInvoicesStore } from '../stores/invoices.js'
import { useTodosStore } from '../stores/todos.js'
import { useUIStore } from '../stores/ui.js'
import { useMonthlyRotationStore } from '../stores/monthlyRotation.js'
import { useMonthlyStore } from '../stores/monthly.js'
import HamburgerMenu from '../components/HamburgerMenu.vue'
import BasicDataModal from '../components/BasicDataModal.vue'
import UserSettings from '../components/UserSettings.vue'
import AddToHomePrompt from '@/components/AddToHomePrompt.vue'
import DashboardIcon from '../components/icons/DashboardIcon.vue'
import InvoiceIcon from '../components/icons/InvoiceIcon.vue'
import ChecklistIcon from '../components/icons/ChecklistIcon.vue'
import BriefcaseIcon from '../components/icons/BriefcaseIcon.vue'
import MonthlyTabs from '../components/MonthlyTabs.vue'
import MonthlyStatsSection from '../components/MonthlyStatsSection.vue'

const router = useRouter()
const authStore = useAuthStore()
const projectsStore = useProjectsStore()
const invoicesStore = useInvoicesStore()
const todosStore = useTodosStore()
const uiStore = useUIStore()
const rotationStore = useMonthlyRotationStore()
const monthlyStore = useMonthlyStore()

// 月次管理タブ状態（初期化ロジック修正）
const currentMonthTab = ref('overview')

// ステップ3修正: 初期表示制御フラグ（環境に依存しない初期表示判定）
const isInitialDisplay = ref(true)

// Phase 3: 強制的な再レンダリングのためのカウンターとフラグ
const forceRerenderCounter = ref(0)
const forceRerenderFlag = ref(false)
const visualUpdateCounter = ref(0)

// タブ切り替え問題修正: 初期化時の優先順位の明確化
// 修正: 初期化時は常に現在月を優先し、lastRotationCheckが古い場合は現在月を選択
const initializeCurrentMonthTab = () => {
  console.log('🔧 月次管理タブの初期化を実行')
  
  try {
    // 1. 現在日時を取得（最優先）
    const now = new Date()
    const currentYear = now.getFullYear()
    const currentMonth = now.getMonth() + 1
    const currentMonthId = `${currentYear}-${currentMonth.toString().padStart(2, '0')}`
    
    // 2. 月次切り替え状態を確認
    const rotationState = rotationStore.rotationState
    const lastRotationCheck = rotationStore.lastRotationCheck
    
    console.log('🔧 初期化: 月次切り替え状態を確認', {
      rotationState,
      lastRotationCheck,
      currentYear,
      currentMonth,
      currentMonthId
    })
    
    // 3. 修正: 初期化時は常に現在月を優先するロジックを強化
    // lastRotationCheckが存在し、かつ現在月より新しいまたは同じ場合のみ、lastRotationCheckを基準にする
    if (rotationState === 'completed' && lastRotationCheck) {
      const baseDate = new Date(lastRotationCheck)
      const lastYear = baseDate.getFullYear()
      const lastMonth = baseDate.getMonth() + 1
      const lastMonthId = `${lastYear}-${lastMonth.toString().padStart(2, '0')}`
      
      // 修正: 現在日時とlastRotationCheckの比較を厳密化
      // lastRotationCheckが現在月より古い場合（不一致）、現在月を優先
      const isLastRotationOlder = (lastYear < currentYear) || 
                                  (lastYear === currentYear && lastMonth < currentMonth)
      
      if (isLastRotationOlder) {
        console.log('⚠️ lastRotationCheckが現在月より古い - 現在月を優先（初期化時の優先順位明確化）', {
          currentMonthId,
          lastMonthId,
          lastRotationCheck,
          reason: 'lastRotationCheckが現在月より古いため、現在月を優先'
        })
        currentMonthTab.value = currentMonthId
        return
      }
      
      // lastRotationCheckが現在月と同じか新しい場合のみ、lastRotationCheckを基準にタブ選択
      console.log('🎉 月次切り替え完了 - lastRotationCheckを基準にタブ選択', {
        lastMonthId,
        currentMonthTab: currentMonthTab.value,
        reason: 'lastRotationCheckが現在月と同じか新しいため、lastRotationCheckを基準に選択'
      })
      currentMonthTab.value = lastMonthId
      return
    }
    
    // 4. フォールバック - 初期化時は常に現在月を初期値に設定
    console.log('📅 現在月を初期値に設定（初期化時の優先順位明確化）:', currentMonthId)
    currentMonthTab.value = currentMonthId
    
  } catch (error) {
    console.error('❌ 初期化エラー:', error)
    // エラー時も現在月を初期値に設定
    const now = new Date()
    const currentYear = now.getFullYear()
    const currentMonth = now.getMonth() + 1
    const currentMonthId = `${currentYear}-${currentMonth.toString().padStart(2, '0')}`
    currentMonthTab.value = currentMonthId
  }
}

// タブ切り替え問題修正: タブ更新トリガー（不一致チェックの厳密化）
// 修正: 現在日時とlastRotationCheckの不一致を厳密にチェックし、現在月より古い場合は現在月を優先
const triggerTabUpdate = async () => {
  console.log('🔧 タブ更新をトリガーします。')
  
  try {
    // 1. 現在日時を取得（最優先）
    const now = new Date()
    const currentYear = now.getFullYear()
    const currentMonth = now.getMonth() + 1
    const currentMonthId = `${currentYear}-${currentMonth.toString().padStart(2, '0')}`
    
    // 2. 月次切り替え状態を確認
    const rotationState = rotationStore.rotationState
    const lastRotationCheck = rotationStore.lastRotationCheck
    
    console.log('🔧 タブ更新: 月次切り替え状態を確認', {
      rotationState,
      lastRotationCheck,
      currentYear,
      currentMonth,
      currentMonthId
    })
    
    // 3. 修正: 月次切り替え完了時の処理（不一致チェックの厳密化）
    if (rotationState === 'completed' && lastRotationCheck) {
      const baseDate = new Date(lastRotationCheck)
      const lastYear = baseDate.getFullYear()
      const lastMonth = baseDate.getMonth() + 1
      const lastMonthId = `${lastYear}-${lastMonth.toString().padStart(2, '0')}`
      
      // 修正: 現在日時とlastRotationCheckの不一致を厳密にチェック
      // lastRotationCheckが現在月より古い場合のみ不一致と判断し、現在月を優先
      const isLastRotationOlder = (lastYear < currentYear) || 
                                  (lastYear === currentYear && lastMonth < currentMonth)
      
      if (isLastRotationOlder) {
        console.log('⚠️ lastRotationCheckが現在月より古い - 現在月を優先（不一致チェックの厳密化）', {
          currentMonthId,
          lastMonthId,
          lastRotationCheck,
          reason: 'lastRotationCheckが現在月より古いため、現在月を優先'
        })
        currentMonthTab.value = currentMonthId
        await rotationStore.refreshFrontendData()
        return
      }
      
      // lastRotationCheckが現在月と同じか新しい場合のみ、lastRotationCheckを基準にタブ切り替え
      console.log('🎉 月次切り替え完了 - lastRotationCheckを基準にタブ切り替え', {
        previousTab: currentMonthTab.value,
        newTab: lastMonthId,
        currentMonthTab: currentMonthTab.value,
        reason: 'lastRotationCheckが現在月と同じか新しいため、lastRotationCheckを基準に選択'
      })
      currentMonthTab.value = lastMonthId
      await rotationStore.refreshFrontendData()
      return
    }
    
    // 4. フォールバック - 現在月を設定
    console.log('📅 現在月を設定:', currentMonthId)
    currentMonthTab.value = currentMonthId
    
  } catch (error) {
    console.error('❌ タブ更新エラー:', error)
  }
}

// Phase 2: リアクティブな更新の同期化機能を追加
const syncReactiveUpdates = async (newTab, oldTab) => {
  console.log('🔧 Phase 2: リアクティブな更新の同期化を実行', {
    newTab,
    oldTab,
    timestamp: new Date().toISOString()
  })
  
  try {
    // 1. 複数回のnextTickを使用した確実な同期化
    await nextTick()
    console.log('🔧 Phase 2: 第1回nextTick完了')
    
    await nextTick()
    console.log('🔧 Phase 2: 第2回nextTick完了')
    
    // 2. 改善案4: forceRerender削除（重複実行防止）
    console.log('🔧 Phase 2: nextTickによる同期化完了（forceRerender削除）')
    
    // 3. 最終的なnextTickで確実に同期化
    await nextTick()
    console.log('🔧 Phase 2: 最終nextTick完了')
    
    // 5. 同期化後の状態確認
    console.log('🔧 Phase 2: 同期化後の状態確認', {
      currentMonthTab: currentMonthTab.value,
      rotationState: rotationStore.rotationState,
      lastRotationCheck: rotationStore.lastRotationCheck,
      forceRerenderCounter: forceRerenderCounter.value
    })
    
    console.log('🎉 Phase 2: リアクティブな更新の同期化完了')
    
  } catch (error) {
    console.error('❌ Phase 2: リアクティブな更新の同期化エラー:', error)
  }
}

// Phase 3: 強制的な再レンダリング機能を強化
const forceRerender = async () => {
  console.log('🔧 Phase 3: 強制的な再レンダリングを実行')
  
  try {
    // 1. 再レンダリングフラグを設定
    forceRerenderFlag.value = true
    forceRerenderCounter.value++
    visualUpdateCounter.value++
    
    console.log('🔧 Phase 3: 再レンダリングフラグを設定', {
      forceRerenderFlag: forceRerenderFlag.value,
      forceRerenderCounter: forceRerenderCounter.value,
      visualUpdateCounter: visualUpdateCounter.value
    })
    
    // 2. Phase 3: DOM操作による強制的な更新
    await forceDOMUpdate()
    
    // 3. nextTickを使用してDOM更新を確実に実行
    await nextTick()
    console.log('🔧 Phase 3: DOM更新を確実に実行')
    
    // 4. 月次切り替え状態を再確認
    const rotationState = rotationStore.rotationState
    const lastRotationCheck = rotationStore.lastRotationCheck
    
    console.log('🔧 Phase 3: 再レンダリング後の状態確認', {
      rotationState,
      lastRotationCheck,
      currentMonthTab: currentMonthTab.value,
      forceRerenderCounter: forceRerenderCounter.value,
      forceRerenderFlag: forceRerenderFlag.value,
      visualUpdateCounter: visualUpdateCounter.value
    })
    
    // 5. 改善案4: refreshFrontendData削除（重複実行防止）
    console.log('🔧 Phase 3: データ同期は他の箇所で実行（重複削除）')
    
    // 6. Phase 3: 視覚的な更新の確実化
    await ensureVisualUpdate()
    
    // 7. 再レンダリングフラグをリセット
    forceRerenderFlag.value = false
    
    console.log('🎉 Phase 3: 強制的な再レンダリング完了')
    
  } catch (error) {
    console.error('❌ Phase 3: 強制的な再レンダリングエラー:', error)
    forceRerenderFlag.value = false
  }
}

// Phase 3: DOM操作による強制的な更新を実装
const forceDOMUpdate = async () => {
  console.log('🔧 Phase 3: DOM操作による強制的な更新を実行')
  
  try {
    // 1. MonthlyTabsコンポーネントのDOM要素を取得
    const monthlyTabsElement = document.querySelector('.monthly-tabs')
    if (monthlyTabsElement) {
      console.log('🔧 Phase 3: MonthlyTabsコンポーネントのDOM要素を取得')
      
      // 2. 一時的にクラスを変更して強制的な再レンダリングをトリガー
      monthlyTabsElement.classList.add('force-rerender')
      console.log('🔧 Phase 3: 強制再レンダリングクラスを追加')
      
      // 3. nextTickを使用してDOM更新を確実に実行
      await nextTick()
      console.log('🔧 Phase 3: DOM更新を確実に実行')
      
      // 4. クラスを削除
      monthlyTabsElement.classList.remove('force-rerender')
      console.log('🔧 Phase 3: 強制再レンダリングクラスを削除')
      
      // 5. タブ要素の強制的な更新
      const tabButtons = monthlyTabsElement.querySelectorAll('button')
      tabButtons.forEach((button, index) => {
        // 一時的にクラスを変更
        button.classList.add('force-update')
        console.log(`🔧 Phase 3: タブ要素 ${index + 1} に強制更新クラスを追加`)
      })
      
      // 6. nextTickを使用してDOM更新を確実に実行
      await nextTick()
      console.log('🔧 Phase 3: タブ要素のDOM更新を確実に実行')
      
      // 7. クラスを削除
      tabButtons.forEach((button, index) => {
        button.classList.remove('force-update')
        console.log(`🔧 Phase 3: タブ要素 ${index + 1} から強制更新クラスを削除`)
      })
      
    } else {
      console.log('⚠️ Phase 3: MonthlyTabsコンポーネントのDOM要素が見つかりません')
    }
    
    console.log('🎉 Phase 3: DOM操作による強制的な更新完了')
    
  } catch (error) {
    console.error('❌ Phase 3: DOM操作による強制的な更新エラー:', error)
  }
}

// Phase 3: 視覚的な更新の確実化を実装
const ensureVisualUpdate = async () => {
  console.log('🔧 Phase 3: 視覚的な更新の確実化を実行')
  
  try {
    // 1. 現在のタブ状態を確認
    const currentTab = currentMonthTab.value
    console.log('🔧 Phase 3: 現在のタブ状態を確認:', currentTab)
    
    // 2. タブ要素の視覚的な更新を強制実行
    const tabButtons = document.querySelectorAll('.monthly-tabs button')
    console.log('🔧 Phase 3: タブ要素数:', tabButtons.length)
    
    tabButtons.forEach((button, index) => {
      const tabId = button.getAttribute('data-tab-id')
      const isActive = tabId === currentTab
      
      console.log(`🔧 Phase 3: タブ ${index + 1} の状態確認:`, {
        tabId,
        currentTab,
        isActive,
        hasActiveClass: button.classList.contains('border-pink-500')
      })
      
      // 3. アクティブなタブの視覚的更新
      if (isActive) {
        console.log(`🎉 Phase 3: アクティブなタブ ${index + 1} の視覚的更新を実行`)
        
        // 既存のアクティブクラスを削除
        button.classList.remove('border-pink-500', 'text-pink-600', 'bg-pink-50')
        
        // 新しいアクティブクラスを追加
        button.classList.add('border-pink-500', 'text-pink-600', 'bg-pink-50')
        
        // 強制的な再レンダリングをトリガー
        button.style.transform = 'scale(1.01)'
        setTimeout(async () => {
          await nextTick()
          button.style.transform = 'scale(1)'
          console.log(`🔧 Phase 3: アクティブなタブ ${index + 1} の視覚的更新完了`)
        }, 50)
        
      } else {
        console.log(`🔧 Phase 3: 非アクティブなタブ ${index + 1} の視覚的更新を実行`)
        
        // 非アクティブなタブのクラスを設定
        button.classList.remove('border-pink-500', 'text-pink-600', 'bg-pink-50')
        button.classList.add('text-gray-500', 'hover:text-gray-700', 'hover:bg-gray-50')
        
        // 非アクティブなタブの視覚的更新
        button.classList.add('visual-update-inactive')
        setTimeout(async () => {
          await nextTick()
          button.classList.remove('visual-update-inactive')
          console.log(`🔧 Phase 3: 非アクティブなタブ ${index + 1} の視覚的更新完了`)
        }, 30)
      }
    })
    
    // 4. 視覚的更新カウンターを増加
    visualUpdateCounter.value++
    console.log('🔧 Phase 3: 視覚的更新カウンターを増加:', visualUpdateCounter.value)
    
    console.log('🎉 Phase 3: 視覚的な更新の確実化完了')
    
  } catch (error) {
    console.error('❌ Phase 3: 視覚的な更新の確実化エラー:', error)
  }
}

// 月次切り替え状態の監視（新規追加）
// 修正案2: 条件を緩和し、completed状態の変更をすべて検知
// ステップ3修正: 初期表示時のtriggerTabUpdate()を防止（環境に依存しない判定）
const handleRotationStateChange = (newState, oldState) => {
  console.log('月次切り替え状態変更を検知:', { newState, oldState })
  
  // ステップ3修正: 初期表示時（overviewタブ）は実行しない
  // 方法1: 初期表示フラグによる判定（環境に依存しない）
  if (isInitialDisplay.value && currentMonthTab.value === 'overview') {
    console.log('⚠️ 初期表示中のため、triggerTabUpdate()をスキップ（フラグ判定）')
    return  // 初期表示時はスキップ
  }
  
  // 方法2: oldStateによる判定（二重の防御）
  if (currentMonthTab.value === 'overview' && (oldState === null || oldState === 'idle')) {
    console.log('⚠️ 初期表示時のため、triggerTabUpdate()をスキップ（oldState判定）')
    return  // 初期表示時はスキップ
  }
  
  // 修正: newState === 'completed'の場合、すべてtriggerTabUpdate()を呼び出す
  if (newState === 'completed') {
    console.log('月次切り替え完了を検知 - タブ更新をトリガー')
    triggerTabUpdate()
  }
}

// 設定モーダル表示状態（UIStoreに統合）
// const showSettings = ref(false)
// const showBasicData = ref(false)

// 統計データ計算
const stats = computed(() => {
  const invoices = invoicesStore.invoices || []
  
  return {
    totalProjects: projectsStore.totalProjectsCount,
    completedProjects: projectsStore.completedCount,
    pendingProjects: projectsStore.pendingProjectsCount,
    totalInvoices: invoices.length,
    totalTodos: todosStore.todos?.length || 0,
    totalInvoiceAmount: invoicesStore.invoiceStats.total_invoice_amount,
    pendingTodos: todosStore.stats.pending_todos || 0
  }
})

// アプリ初期化
onMounted(async () => {
  // 未認証の場合は認証ページへリダイレクト
  await authStore.checkAuthStatus()
  if (!authStore.isLoggedIn) {
    router.push('/')
    return
  }
  
  // 月次切り替え監視を自動開始
  try {
    rotationStore.startRotationMonitoring()
    console.log('月次切り替え監視を自動開始しました。')
  } catch (error) {
    console.error('月次切り替え監視の開始に失敗しました:', error)
  }
  
  // ステップ3: 初期表示ロジックの修正 - 概要タブを固定（最速表示）
  currentMonthTab.value = 'overview'
  
  // 軽量概要APIを並行実行
  await monthlyStore.fetchOverviewMinimal()
  
  // 月次データをバックグラウンドで非同期実行（awaitしない）
  monthlyStore.fetchCurrentMonthlyData()
  
  // Phase 2: 親子コンポーネント間の状態同期を確実化
  console.log('🔧 Phase 2: 親子コンポーネント間の状態同期を確実化')
  
  // データ取得
  await Promise.all([
    projectsStore.fetchProjects(),
    invoicesStore.fetchInvoices(),
    todosStore.fetchTodos()
  ])
  
  // Phase 2: nextTickを使用した非同期処理の最適化
  await nextTick()
  console.log('🔧 Phase 2: 初期化後の第1回nextTick完了')
  
  await nextTick()
  console.log('🔧 Phase 2: 初期化後の第2回nextTick完了')
  
  // ステップ3修正: 初期表示完了フラグをオフ（初期化処理の完了を待つ）
  await nextTick()
  isInitialDisplay.value = false
  console.log('🔧 初期表示完了フラグをオフ')
  
  // Phase 2: 初期化後の状態確認
  console.log('🔧 Phase 2: 初期化後の状態確認', {
    currentMonthTab: currentMonthTab.value,
    rotationState: rotationStore.rotationState,
    lastRotationCheck: rotationStore.lastRotationCheck,
    forceRerenderCounter: forceRerenderCounter.value,
    isInitialDisplay: isInitialDisplay.value
  })
  
  // Phase 3: 初期化後の強制的な同期化
  await syncReactiveUpdates(currentMonthTab.value, 'overview')
  console.log('🔧 Phase 3: 初期化後の同期化完了（改善案4: forceRerender削除）')
})

// 修正案1: 初期化時の実行を防止し、現在月優先ロジックを強化
// ステップ3修正: 初期表示時のtriggerTabUpdate()を防止（環境に依存しない判定）
watch(() => rotationStore.lastRotationCheck, (newValue, oldValue) => {
  // 初期化時や値が変わらない場合は実行しない
  if (!oldValue || !newValue || newValue === oldValue) {
    return
  }
  
  // ステップ3修正: 初期表示時（overviewタブ）は実行しない
  // 方法1: 初期表示フラグによる判定（環境に依存しない）
  if (isInitialDisplay.value && currentMonthTab.value === 'overview') {
    console.log('⚠️ 初期表示中のため、triggerTabUpdate()をスキップ（フラグ判定）')
    return  // 初期表示時はスキップ
  }
  
  // 方法2: oldValueによる判定（二重の防御）
  if (currentMonthTab.value === 'overview' && !oldValue) {
    console.log('⚠️ 初期表示時のため、triggerTabUpdate()をスキップ（oldValue判定）')
    return  // 初期表示時はスキップ
  }
  
  console.log('月次切り替えが検知されました。')
  
  // 現在月を優先するため、triggerTabUpdate()を呼び出す前に現在日時を確認
  const now = new Date()
  const currentYear = now.getFullYear()
  const currentMonth = now.getMonth() + 1
  const currentMonthId = `${currentYear}-${currentMonth.toString().padStart(2, '0')}`
  
  const lastDate = new Date(newValue)
  const lastYear = lastDate.getFullYear()
  const lastMonth = lastDate.getMonth() + 1
  const lastMonthId = `${lastYear}-${lastMonth.toString().padStart(2, '0')}`
  
  // lastRotationCheckが現在月より古い場合は、triggerTabUpdate()を呼び出さない
  const isLastRotationOlder = (lastYear < currentYear) || 
                              (lastYear === currentYear && lastMonth < currentMonth)
  
  if (isLastRotationOlder) {
    console.log('⚠️ lastRotationCheckが現在月より古いため、triggerTabUpdate()をスキップ', {
      currentMonthId,
      lastMonthId,
      lastRotationCheck: newValue
    })
    return
  }
  
  triggerTabUpdate()
})

// 月次切り替え状態の監視（新規追加）
watch(() => rotationStore.rotationState, handleRotationStateChange)

// Phase 2: currentMonthTabの変更を監視するwatchを強化
watch(() => currentMonthTab.value, async (newTab, oldTab) => {
  console.log('🔧 Phase 2: currentMonthTabの変更を検知', {
    newTab,
    oldTab,
    timestamp: new Date().toISOString()
  })
  
  try {
    // 1. 月次切り替え状態を確認
    const rotationState = rotationStore.rotationState
    const lastRotationCheck = rotationStore.lastRotationCheck
    
    console.log('🔧 Phase 2: 月次切り替え状態を確認', {
      rotationState,
      lastRotationCheck,
      newTab
    })
    
    // 2. 新しい月のタブが選択された場合の処理
    if (newTab && newTab !== 'overview' && newTab !== oldTab) {
      console.log('🎉 Phase 2: 新しい月のタブが選択されました', {
        selectedTab: newTab,
        previousTab: oldTab
      })
      
      // 3. Phase 2: リアクティブな更新の同期化を強化
      await syncReactiveUpdates(newTab, oldTab)
      
      // 4. 視覚的更新（syncReactiveUpdates内で実行済み - 重複削除）
      console.log('🔧 Phase 2: 視覚的更新はsyncReactiveUpdates内で実行済み')
      // await ensureVisualUpdate()
      
    } else if (newTab === 'overview') {
      console.log('📋 Phase 2: 概要タブが選択されました')
      
      // Phase 2: 概要タブ選択時の同期化
      await syncReactiveUpdates(newTab, oldTab)
      
      // 4. 視覚的更新（syncReactiveUpdates内で実行済み - 重複削除）
      console.log('🔧 Phase 2: 視覚的更新はsyncReactiveUpdates内で実行済み')
      // await ensureVisualUpdate()
    }
    
  } catch (error) {
    console.error('❌ Phase 2: currentMonthTab変更時の処理エラー:', error)
  }
}, { deep: false })



// プラグインアプリへの遷移
const navigateToApp = (appName) => {
  if (appName === 'berry-do') {
    router.push('/berry-do')  // BerryDo専用ルート
  } else {
    router.push(`/apps/${appName}`)  // 既存projects/invoices
  }
}

// 設定モーダル表示切り替え（UIStoreに統合）
// const toggleSettings = () => {
//   showSettings.value = !showSettings.value
// }

// 基本データモーダル表示切り替え（UIStoreに統合）
// const toggleBasicData = () => {
//   showBasicData.value = !showBasicData.value
// }

// Phase 2: デバッグ用のグローバル関数を強化
const debugParentChildCommunication = () => {
  console.log('🔧 Phase 2: 親子コンポーネント間の通信状況を確認')
  
  console.log('🔧 親コンポーネント(DashboardPage)の状態:', {
    currentMonthTab: currentMonthTab.value,
    forceRerenderCounter: forceRerenderCounter.value,
    rotationState: rotationStore.rotationState,
    lastRotationCheck: rotationStore.lastRotationCheck
  })
  
  // DOM要素の確認
  const monthlyTabsElement = document.querySelector('.monthly-tabs')
  if (monthlyTabsElement) {
    console.log('🔧 MonthlyTabsコンポーネントのDOM要素を確認:', {
      element: monthlyTabsElement,
      classes: monthlyTabsElement.classList.toString(),
      children: monthlyTabsElement.children.length
    })
  }
  
  // タブ要素の詳細確認
  const tabButtons = document.querySelectorAll('.monthly-tabs button')
  console.log('🔧 タブ要素の詳細:', Array.from(tabButtons).map((button, index) => ({
    index,
    text: button.textContent.trim(),
    dataTabId: button.getAttribute('data-tab-id'),
    isActive: button.classList.contains('border-pink-500'),
    classes: Array.from(button.classList)
  })))
}

// Phase 3: 詳細な状態確認機能を強化
const debugDetailedState = async () => {
  console.log('🔧 Phase 3: 詳細な状態確認を実行')
  
  try {
    // 1. 現在の状態を詳細に確認
    console.log('🔧 Phase 3: 現在の状態詳細:', {
      currentMonthTab: currentMonthTab.value,
      forceRerenderCounter: forceRerenderCounter.value,
      forceRerenderFlag: forceRerenderFlag.value,
      visualUpdateCounter: visualUpdateCounter.value,
      rotationState: rotationStore.rotationState,
      lastRotationCheck: rotationStore.lastRotationCheck,
      timestamp: new Date().toISOString()
    })
    
    // 2. nextTickを使用した状態確認
    await nextTick()
    console.log('🔧 Phase 3: nextTick後の状態確認')
    
    // 3. DOM要素の詳細確認
    const monthlyTabsElement = document.querySelector('.monthly-tabs')
    if (monthlyTabsElement) {
      console.log('🔧 Phase 3: MonthlyTabsコンポーネントの詳細:', {
        element: monthlyTabsElement,
        classes: monthlyTabsElement.classList.toString(),
        children: monthlyTabsElement.children.length,
        innerHTML: monthlyTabsElement.innerHTML.substring(0, 200) + '...',
        hasForceRerenderClass: monthlyTabsElement.classList.contains('force-rerender')
      })
    }
    
    // 4. タブ要素の詳細確認
    const tabButtons = document.querySelectorAll('.monthly-tabs button')
    console.log('🔧 Phase 3: タブ要素の詳細確認:', Array.from(tabButtons).map((button, index) => ({
      index,
      text: button.textContent.trim(),
      dataTabId: button.getAttribute('data-tab-id'),
      isActive: button.classList.contains('border-pink-500'),
      classes: Array.from(button.classList),
      dataset: button.dataset,
      hasForceUpdateClass: button.classList.contains('force-update'),
      hasVisualUpdateActiveClass: button.classList.contains('visual-update-active'),
      hasVisualUpdateInactiveClass: button.classList.contains('visual-update-inactive'),
      transform: button.style.transform
    })))
    
    // 5. リアクティブな更新の状況確認
    console.log('🔧 Phase 3: リアクティブな更新の状況確認:', {
      currentMonthTabValue: currentMonthTab.value,
      currentMonthTabType: typeof currentMonthTab.value,
      forceRerenderCounterValue: forceRerenderCounter.value,
      forceRerenderCounterType: typeof forceRerenderCounter.value,
      forceRerenderFlagValue: forceRerenderFlag.value,
      forceRerenderFlagType: typeof forceRerenderFlag.value,
      visualUpdateCounterValue: visualUpdateCounter.value,
      visualUpdateCounterType: typeof visualUpdateCounter.value
    })
    
    console.log('🎉 Phase 3: 詳細な状態確認完了')
    
  } catch (error) {
    console.error('❌ Phase 3: 詳細な状態確認エラー:', error)
  }
}

// Phase 2: 強制的な状態同期機能を強化
const forceParentChildSync = async () => {
  console.log('🔧 Phase 2: 強制的な親子コンポーネント間の状態同期を実行')
  
  try {
    // 1. 現在の状態を確認
    console.log('🔧 同期前の状態:', {
      currentMonthTab: currentMonthTab.value,
      rotationState: rotationStore.rotationState,
      lastRotationCheck: rotationStore.lastRotationCheck
    })
    
    // 2. Phase 2: 複数回のnextTickを使用した確実な同期化
    await nextTick()
    console.log('🔧 Phase 2: 第1回nextTick完了')
    
    // 3. 強制的な再レンダリングを実行
    await forceRerender()
    
    // 4. Phase 2: 追加のnextTickを使用してDOM更新を確実に実行
    await nextTick()
    console.log('🔧 Phase 2: 第2回nextTick完了')
    
    await nextTick()
    console.log('🔧 Phase 2: 第3回nextTick完了')
    
    // 5. 同期後の状態を確認
    console.log('🔧 同期後の状態:', {
      currentMonthTab: currentMonthTab.value,
      rotationState: rotationStore.rotationState,
      lastRotationCheck: rotationStore.lastRotationCheck,
      forceRerenderCounter: forceRerenderCounter.value
    })
    
    console.log('🎉 Phase 2: 強制的な親子コンポーネント間の状態同期完了')
    
  } catch (error) {
    console.error('❌ Phase 2: 強制的な親子コンポーネント間の状態同期エラー:', error)
  }
}

// Phase 4: コンポーネント内の状態にアクセスできる関数の提供
const getComponentState = () => {
  console.log('🔧 Phase 4: コンポーネント内の状態を取得')
  
  return {
    // 親コンポーネント(DashboardPage)の状態
    parentComponent: {
      currentMonthTab: currentMonthTab.value,
      forceRerenderCounter: forceRerenderCounter.value,
      forceRerenderFlag: forceRerenderFlag.value,
      visualUpdateCounter: visualUpdateCounter.value,
      rotationState: rotationStore.rotationState,
      lastRotationCheck: rotationStore.lastRotationCheck
    },
    // 子コンポーネント(MonthlyTabs)の状態
    childComponent: {
      // DOM要素から子コンポーネントの状態を推測
      monthlyTabsElement: document.querySelector('.monthly-tabs'),
      tabButtons: document.querySelectorAll('.monthly-tabs button'),
      activeTab: document.querySelector('.monthly-tabs button.border-pink-500')
    },
    // 親子コンポーネント間の通信状況
    communication: {
      vModelBinding: currentMonthTab.value,
      emitEvents: 'update:modelValue',
      watchTriggers: 'currentMonthTab.value changes'
    }
  }
}

// Phase 4: より詳細な状態確認機能を追加
const debugEnhancedState = async () => {
  console.log('🔧 Phase 4: 強化された状態確認を実行')
  
  try {
    // 1. コンポーネント内の状態を取得
    const componentState = getComponentState()
    console.log('🔧 Phase 4: コンポーネント内の状態:', componentState)
    
    // 2. 親子コンポーネント間の状態同期を確認
    const parentChildSync = await checkParentChildSync()
    console.log('🔧 Phase 4: 親子コンポーネント間の状態同期:', parentChildSync)
    
    // 3. リアクティブな更新の状況を確認
    const reactiveUpdateStatus = await checkReactiveUpdateStatus()
    console.log('🔧 Phase 4: リアクティブな更新の状況:', reactiveUpdateStatus)
    
    // 4. 強制的な再レンダリングの状況を確認
    const forceRerenderStatus = await checkForceRerenderStatus()
    console.log('🔧 Phase 4: 強制的な再レンダリングの状況:', forceRerenderStatus)
    
    // 5. 総合的な状態レポートを生成
    const comprehensiveReport = {
      timestamp: new Date().toISOString(),
      componentState,
      parentChildSync,
      reactiveUpdateStatus,
      forceRerenderStatus,
      summary: {
        totalIssues: 0,
        resolvedIssues: 0,
        pendingIssues: 0
      }
    }
    
    console.log('🔧 Phase 4: 総合的な状態レポート:', comprehensiveReport)
    console.log('🎉 Phase 4: 強化された状態確認完了')
    
    return comprehensiveReport
    
  } catch (error) {
    console.error('❌ Phase 4: 強化された状態確認エラー:', error)
    return null
  }
}

// Phase 4: 親子コンポーネント間の状態同期を確認
const checkParentChildSync = async () => {
  console.log('🔧 Phase 4: 親子コンポーネント間の状態同期を確認')
  
  try {
    // 1. 親コンポーネントの状態
    const parentState = {
      currentMonthTab: currentMonthTab.value,
      forceRerenderCounter: forceRerenderCounter.value,
      forceRerenderFlag: forceRerenderFlag.value,
      visualUpdateCounter: visualUpdateCounter.value
    }
    
    // 2. 子コンポーネントの状態（DOM要素から推測）
    const childState = {
      activeTab: document.querySelector('.monthly-tabs button.border-pink-500')?.getAttribute('data-tab-id'),
      totalTabs: document.querySelectorAll('.monthly-tabs button').length,
      monthlyTabsElement: document.querySelector('.monthly-tabs') !== null
    }
    
    // 3. 状態同期の確認
    const syncStatus = {
      parentState,
      childState,
      isSynced: childState.activeTab === parentState.currentMonthTab,
      lastSyncTime: new Date().toISOString()
    }
    
    console.log('🔧 Phase 4: 親子コンポーネント間の状態同期確認完了:', syncStatus)
    return syncStatus
    
  } catch (error) {
    console.error('❌ Phase 4: 親子コンポーネント間の状態同期確認エラー:', error)
    return null
  }
}

// Phase 4: リアクティブな更新の状況を確認
const checkReactiveUpdateStatus = async () => {
  console.log('🔧 Phase 4: リアクティブな更新の状況を確認')
  
  try {
    // 1. 現在の状態
    const currentState = {
      currentMonthTab: currentMonthTab.value,
      rotationState: rotationStore.rotationState,
      lastRotationCheck: rotationStore.lastRotationCheck,
      forceRerenderCounter: forceRerenderCounter.value
    }
    
    // 2. nextTickの利用可能性
    const nextTickAvailable = typeof nextTick !== 'undefined'
    
    // 3. リアクティブな更新の状況
    const reactiveStatus = {
      currentState,
      nextTickAvailable,
      lastUpdateTime: new Date().toISOString(),
      updateFrequency: forceRerenderCounter.value,
      isReactive: currentMonthTab.value !== 'overview' || forceRerenderCounter.value > 0
    }
    
    console.log('🔧 Phase 4: リアクティブな更新の状況確認完了:', reactiveStatus)
    return reactiveStatus
    
  } catch (error) {
    console.error('❌ Phase 4: リアクティブな更新の状況確認エラー:', error)
    return null
  }
}

// Phase 4: 強制的な再レンダリングの状況を確認
const checkForceRerenderStatus = async () => {
  console.log('🔧 Phase 4: 強制的な再レンダリングの状況を確認')
  
  try {
    // 1. 再レンダリングの状況
    const rerenderStatus = {
      forceRerenderCounter: forceRerenderCounter.value,
      forceRerenderFlag: forceRerenderFlag.value,
      visualUpdateCounter: visualUpdateCounter.value,
      lastRerenderTime: new Date().toISOString()
    }
    
    // 2. DOM要素の状況
    const domStatus = {
      monthlyTabsElement: document.querySelector('.monthly-tabs') !== null,
      tabButtons: document.querySelectorAll('.monthly-tabs button').length,
      activeTab: document.querySelector('.monthly-tabs button.border-pink-500') !== null
    }
    
    // 3. 強制的な再レンダリングの状況
    const forceRerenderStatus = {
      rerenderStatus,
      domStatus,
      isForceRerenderActive: forceRerenderFlag.value,
      hasVisualUpdates: visualUpdateCounter.value > 0
    }
    
    console.log('🔧 Phase 4: 強制的な再レンダリングの状況確認完了:', forceRerenderStatus)
    return forceRerenderStatus
    
  } catch (error) {
    console.error('❌ Phase 4: 強制的な再レンダリングの状況確認エラー:', error)
    return null
  }
}

// Phase 4: グローバルスコープでデバッグ関数を利用可能にする
try {
  window.debugParentChildCommunication = debugParentChildCommunication
  window.debugDetailedState = debugDetailedState
  window.debugEnhancedState = debugEnhancedState
  window.getComponentState = getComponentState
  window.checkParentChildSync = checkParentChildSync
  window.checkReactiveUpdateStatus = checkReactiveUpdateStatus
  window.checkForceRerenderStatus = checkForceRerenderStatus
  window.forceParentChildSync = forceParentChildSync
  window.forceRerender = forceRerender
  window.forceDOMUpdate = forceDOMUpdate
  window.ensureVisualUpdate = ensureVisualUpdate
  window.syncReactiveUpdates = syncReactiveUpdates
  window.currentMonthTab = currentMonthTab
  window.forceRerenderCounter = forceRerenderCounter
  window.forceRerenderFlag = forceRerenderFlag
  window.visualUpdateCounter = visualUpdateCounter
  console.log('🔧 Phase 4: グローバルデバッグ関数の登録が完了しました')
} catch (error) {
  console.error('❌ Phase 4: グローバルデバッグ関数の登録エラー:', error)
}

console.log('🔧 Phase 4: 利用可能なデバッグ関数:', [
  'debugParentChildCommunication',
  'debugDetailedState',
  'debugEnhancedState',
  'getComponentState',
  'checkParentChildSync',
  'checkReactiveUpdateStatus',
  'checkForceRerenderStatus',
  'forceParentChildSync',
  'forceRerender',
  'forceDOMUpdate',
  'ensureVisualUpdate',
  'syncReactiveUpdates',
  'currentMonthTab',
  'forceRerenderCounter',
  'forceRerenderFlag',
  'visualUpdateCounter'
])

</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 統一ヘッダー -->
    <header class="shadow-lg border-b-2" style="background: linear-gradient(to right, var(--influberry-pink-light), var(--influberry-lavender-light)); border-color: var(--influberry-pink);">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- InfluBerry ロゴ -->
          <div class="flex items-center">
            <!-- Step 3: 画像の遅延読み込み - loading="lazy"属性を追加（初期読み込み時間の削減） -->
            <img src="/favicon512.png" alt="InfluBerry" class="w-8 h-8 mr-3" loading="lazy">
            <h1 class="text-2xl font-bold bg-gradient-to-r from-pink-500 to-purple-600 bg-clip-text text-transparent">
              InfluBerry
            </h1>
          </div>
          
          <!-- ハンバーガーメニュー -->
          <HamburgerMenu />
        </div>
      </div>
    </header>
    <!-- メインコンテンツ -->
    <main class="max-w-7xl mx-auto py-6">
      <div class="py-6">
        
        <!-- 月次管理セクション（NEW） -->
        <div class="monthly-management-section mb-12" style="margin-bottom: 3rem !important;">
          <MonthlyTabs v-model="currentMonthTab" />
          <MonthlyStatsSection :current-tab="currentMonthTab" />
          
        </div>

        <!-- 統計サマリー -->
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <DashboardIcon :size="28" color="#ec4899" class="mr-2" />
            その他の実績
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <div class="berry-card text-center">
              <div class="text-2xl font-bold text-green-600">{{ stats.completedProjects }}</div>
              <div class="text-sm text-gray-600">完了案件</div>
            </div>
            <div class="berry-card text-center">
              <div class="text-2xl font-bold text-yellow-600">{{ stats.pendingProjects }}</div>
              <div class="text-sm text-gray-600">進行中案件</div>
            </div>
            <div class="berry-card text-center">
              <div class="text-2xl font-bold text-purple-600">{{ stats.totalInvoices }}</div>
              <div class="text-sm text-gray-600">請求書数</div>
            </div>
            <div class="berry-card text-center">
              <div class="text-2xl font-bold text-pink-600">¥{{ stats.totalInvoiceAmount.toLocaleString() }}</div>
              <div class="text-sm text-gray-600">総請求額</div>
            </div>
            <div class="berry-card text-center">
              <div class="text-2xl font-bold text-blue-600">{{ stats.pendingTodos }}</div>
              <div class="text-sm text-gray-600">総タスク数</div>
            </div>
          </div>
        </div>

        <!-- プラグインアプリ選択 -->
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <DashboardIcon :size="28" color="#ec4899" class="mr-2" />
          アプリケーション
        </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            
            <!-- スポンサー案件管理アプリ -->
            <div class="berry-card cursor-pointer" @click="navigateToApp('projects')">
              <div class="p-6">
                <div class="flex items-center mb-4">
                  <div class="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center">
                    <BriefcaseIcon :size="32" color="#3b82f6" />
                  </div>
                  <div class="ml-4">
                    <h3 class="text-lg font-semibold text-gray-900">BerryWork｜案件管理</h3>
                    <p class="text-sm text-gray-600">案件の登録・管理・進捗追跡</p>
                  </div>
                </div>
                <div class="text-right">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-pink-100 text-pink-800">
                    {{ stats.totalProjects }} 件
                  </span>
                </div>
              </div>
            </div>

            <!-- 請求書管理アプリ -->
            <div class="berry-card cursor-pointer" @click="navigateToApp('invoices')">
              <div class="p-6">
                <div class="flex items-center mb-4">
                  <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                    <InvoiceIcon :size="32" color="#a855f7" />
                  </div>
                  <div class="ml-4">
                    <h3 class="text-lg font-semibold text-gray-900">BerryPay｜請求書管理</h3>
                    <p class="text-sm text-gray-600">自動請求書生成・管理</p>
                  </div>
                </div>
                <div class="text-right">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                    {{ stats.totalInvoices }} 件
                  </span>
                </div>
              </div>
            </div>

            <!-- BerryDo｜タスク管理アプリ -->
            <div class="berry-card cursor-pointer" @click="navigateToApp('berry-do')">
              <div class="p-6">
                <div class="flex items-center mb-4">
                  <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                    <ChecklistIcon :size="32" color="#10b981" />
                  </div>
                  <div class="ml-4">
                    <h3 class="text-lg font-semibold text-gray-900">BerryDo｜タスク管理</h3>
                    <p class="text-sm text-gray-600">タスク・Todo管理・優先度設定</p>
                  </div>
                </div>
                <div class="text-right">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    {{ stats.totalTodos }} 件
                  </span>
                </div>
              </div>
            </div>

            <!-- 将来プラグイン（予定） -->
            <div class="berry-card-disabled cursor-not-allowed opacity-75">
              <div class="p-6">
                <div class="flex items-center mb-4">
                  <div class="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center text-2xl">
                    💡
                  </div>
                  <div class="ml-4">
                    <h3 class="text-lg font-semibold text-gray-600">投稿アイデアカレンダー</h3>
                    <p class="text-sm text-gray-500">コンテンツ企画・スケジュール管理</p>
                  </div>
                </div>
                <div class="text-right">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-200 text-gray-600">
                    準備中
                  </span>
                </div>
              </div>
            </div>

          </div>
        </div>

      </div>
    </main>

    <!-- 設定モーダル -->
    <div v-if="uiStore.showSettings" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="uiStore.closeSettings()">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="inline-block align-bottom berry-card text-left overflow-hidden transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full" @click.stop>
          <div class="berry-modal-content px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
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
    <!-- 基本データモーダル -->
    <BasicDataModal :show="uiStore.showBasicData" @close="uiStore.closeBasicData()" />

  </div>
  <!-- ホーム画面追加促進モーダル -->
  <AddToHomePrompt page-name="dashboard" />

</template>

/* === Phase 4 berry化CSS - リーガルページ成功パターン移植 === */
.berry-header {
  background: linear-gradient(135deg, #ffffff 0%, #fdf2f8 100%);
  border-bottom: 2px solid #f9a8d4;
  box-shadow: 0 4px 12px rgba(244, 114, 182, 0.15);
}

/* ヘッダータイトル強制カラフル表示 */
h1.text-2xl.font-bold {
  background: linear-gradient(to right, #ec4899, #8b5cf6) !important;
  -webkit-background-clip: text !important;
  background-clip: text !important;
  color: transparent !important;
  font-weight: 700 !important;
}

<style scoped>
/* === Phase 4 berry化CSS - リーガルページ成功パターン移植 === */
.berry-header {
  background: linear-gradient(135deg, #ffffff 0%, #fdf2f8 100%);
  border-bottom: 2px solid #f9a8d4;
  box-shadow: 0 4px 12px rgba(244, 114, 182, 0.15);
}

/* ヘッダータイトル強制カラフル表示 */
h1.text-2xl.font-bold {
  background: linear-gradient(to right, #ec4899, #8b5cf6) !important;
  -webkit-background-clip: text !important;
  background-clip: text !important;
  color: transparent !important;
  font-weight: 700 !important;
}
.berry-card {
  background: linear-gradient(135deg, #ffffff 0%, #fdf2f8 100%);
  border-radius: 1rem;
  box-shadow: 0 8px 20px rgba(244, 114, 182, 0.12);
  border: 2px solid #f9a8d4;
  padding: 1.5rem;
  transition: all 0.3s ease;
  margin-bottom: 1rem;
  z-index: 10; /* ハンバーガーメニュー競合解決 */
}

.berry-card:hover {
  box-shadow: 0 12px 30px rgba(244, 114, 182, 0.2);
  /* transform削除でスタッキングコンテキスト生成阻止 */
}

/* 無効化カード（将来プラグイン用） */
.berry-card-disabled {
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  border-radius: 1rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border: 2px solid #d1d5db;
  padding: 1.5rem;
  margin-bottom: 1rem;
  z-index: 10;
}

/* InfluBerry カスタムスタイル */
header {
  backdrop-filter: blur(10px);
}

/* ホバーエフェクト */
.hover\:shadow-xl:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* スムーズなトランジション */
.transition-shadow {
  transition: box-shadow 0.3s ease;
}

/* モバイルファースト最適化 */
@media (max-width: 640px) {
  .max-w-7xl {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .grid-cols-5 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  
  .flex.items-center.space-x-4 {
    flex-direction: column;
    align-items: flex-end;
    gap: 0.5rem;
  }
}

@media (max-width: 480px) {
  .grid-cols-5 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}

/* Phase 3: 強制的な再レンダリング用のCSSスタイル */
.force-rerender {
  animation: force-rerender-pulse 0.1s ease-in-out;
}

.force-update {
  animation: force-update-pulse 0.1s ease-in-out;
}

.visual-update-active {
  animation: visual-update-active-pulse 0.2s ease-in-out;
}

.visual-update-inactive {
  animation: visual-update-inactive-pulse 0.15s ease-in-out;
}

@keyframes force-rerender-pulse {
  0% { opacity: 1; }
  50% { opacity: 0.8; }
  100% { opacity: 1; }
}

@keyframes force-update-pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.02); }
  100% { transform: scale(1); }
}

@keyframes visual-update-active-pulse {
  0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(236, 72, 153, 0.4); }
  50% { transform: scale(1.05); box-shadow: 0 0 0 4px rgba(236, 72, 153, 0.2); }
  100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(236, 72, 153, 0); }
}

@keyframes visual-update-inactive-pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}
</style>