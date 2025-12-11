# Step 2 Phase 2: 修正案の競合・干渉リスク分析と解決策

**作成日**: 2025年10月31日  
**調査者**: AI Assistant  
**対象**: 重複API呼び出し防止、watch最適化、キャッシュ戦略最適化

## 1. 事前調査サマリー

### 1.1 影響範囲の特定

**修正対象ファイル**:
- `frontend/src/components/MonthlyStatsSection.vue`
- `frontend/src/stores/monthly.js`

**依存コンポーネント**:
- `frontend/src/components/UserSettings.vue` (目標設定機能)
- `frontend/src/views/DashboardPage.vue` (親コンポーネント)

**相互作用の確認**:
1. `UserSettings.vue` → `monthlyStore.saveTarget()` → `targets[monthKey]`更新
2. `MonthlyStatsSection.vue` → `watch(() => monthlyStore.targets[monthKey])` → 統計再取得
3. `MonthlyStatsSection.vue` → `watch(() => props.currentTab)` → `loadData()`

### 1.2 データフローの確認

**目標設定時のデータフロー**:
```
UserSettings.vue
  ↓ saveTarget()
monthlyStore.saveTarget()
  ↓ targets[targetMonth] = newData (Piniaストア更新)
  ↓ fetchTargets(forceRefresh=true)
  ↓ fetchStats(forceRefresh=true)
  ↓ MonthlyStatsSection.watch(() => monthlyStore.targets[monthKey]) トリガー
  ↓ fetchStats() 再実行（重複の可能性）
```

**タブ切り替え時のデータフロー**:
```
MonthlyTabs.vue
  ↓ selectTab(tabId)
  ↓ emit('update:modelValue', tabId)
DashboardPage.vue
  ↓ currentMonthTab.value = tabId
  ↓ MonthlyStatsSection.vue
  ↓ watch(() => props.currentTab) トリガー
  ↓ loadData()
  ↓ (新API使用時) getStatsByMonth() または fetchCurrentMonthlyData()
  ↓ watch(() => monthlyStore.targets[monthKey]) もトリガーされる可能性
  ↓ fetchStats() 再実行（重複の可能性）
```

## 2. リスク分析

### 2.1 リスク1: watchの条件厳密化による目標設定後の統計更新の失敗（🔴 最高リスク）

**リスク内容**:
- `watch(() => monthlyStore.targets[monthKey])`の条件を厳密化すると、目標設定後の統計更新が実行されない可能性
- `saveTarget()`で`targets[monthKey]`を更新しても、watchが反応しない可能性

**発生シナリオ**:
1. `UserSettings.vue`で目標を保存
2. `monthlyStore.saveTarget()`が実行される
3. `this.targets[targetMonth]`が更新される
4. `fetchTargets()`と`fetchStats()`が強制的に再取得される
5. その後、`watch(() => monthlyStore.targets[monthKey])`がトリガーされる
6. しかし、条件が厳密すぎると、統計更新が実行されない可能性

**影響範囲**:
- 目標設定後の統計表示更新
- リアクティブなデータ同期

**リスクレベル**: 🔴 **最高**

**対策**:
- `saveTarget()`で強制的にキャッシュをクリアし、`fetchStats(forceRefresh=true)`を実行済み
- watchの条件は、`saveTarget()`後の更新を確実に検知するように設定
- 初期化時（`oldVal === undefined`）は除外するが、`saveTarget()`後の更新は検知する

### 2.2 リスク2: debounceによるタブ切り替えの遅延（🟠 高リスク）

**リスク内容**:
- `watch(() => props.currentTab)`にdebounceを追加すると、タブ切り替え時のデータ取得が50ms遅延する
- ユーザーが素早くタブを切り替えた場合、データ取得が複数回キャンセルされる可能性

**発生シナリオ**:
1. ユーザーがタブ1 → タブ2 → タブ3と素早く切り替え
2. debounceにより、タブ1のデータ取得がキャンセルされる
3. タブ2のデータ取得もキャンセルされる
4. 最終的にタブ3のデータ取得のみが実行される
5. しかし、タブ3のデータがない場合、スケルトン表示が長時間表示される

**影響範囲**:
- タブ切り替え時のデータ表示
- ユーザー体験

**リスクレベル**: 🟠 **高**

**対策**:
- debounce時間を短く設定（50ms）- ユーザー体験への影響を最小化
- データが既に取得済みの場合、即座にキャッシュを使用（debounceをバイパス）
- キャッシュがある場合は即座に表示し、ない場合のみdebounce後にAPI呼び出し

### 2.3 リスク3: キャッシュ戦略の変更によるデータ整合性への影響（🟡 中リスク）

**リスク内容**:
- キャッシュを最大限に活用すると、目標設定後の統計更新が反映されない可能性
- `saveTarget()`で`fetchStats(forceRefresh=true)`を実行しても、watch内のキャッシュチェックにより更新がスキップされる可能性

**発生シナリオ**:
1. `saveTarget()`で`fetchStats(forceRefresh=true)`が実行される
2. 統計データが更新される
3. その後、`watch(() => monthlyStore.targets[monthKey])`がトリガーされる
4. watch内でキャッシュの有効性をチェック
5. キャッシュが5分以内であれば、更新をスキップ
6. しかし、`saveTarget()`で更新された最新データを反映する必要がある

**影響範囲**:
- 目標設定後の統計表示更新
- データ整合性

**リスクレベル**: 🟡 **中**

**対策**:
- `saveTarget()`で強制的にキャッシュをクリア済み（`clearMonthCache()`）
- `fetchStats(forceRefresh=true)`で強制的に再取得済み
- watch内のキャッシュチェックでは、`saveTarget()`直後の更新は検知しない（`fetchStats()`が既に実行済みのため）
- または、watch内で`saveTarget()`実行フラグを確認し、キャッシュチェックをスキップ

### 2.4 リスク4: nextTick削減によるリアクティブ更新の失敗（🟡 中リスク）

**リスク内容**:
- 不要な`nextTick()`を削除すると、リアクティブな更新が確実に実行されない可能性
- Vueのレンダリングサイクルとデータ更新のタイミングがずれる可能性

**発生シナリオ**:
1. `stats.value = monthlyStore.getStatsByMonth(monthKey)`
2. `nextTick()`を削除
3. テンプレートが`stats.value`を参照する
4. しかし、Vueのリアクティブシステムが更新を検知する前に、テンプレートがレンダリングされる
5. 古いデータが表示される可能性

**影響範囲**:
- データ表示の更新タイミング
- リアクティブな更新

**リスクレベル**: 🟡 **中**

**対策**:
- 必要な箇所のみ`nextTick()`を維持
- 削除する`nextTick()`を慎重に選定
- テストで動作確認を徹底

### 2.5 リスク5: lodash-esの依存関係追加（🟢 低リスク）

**リスク内容**:
- `lodash-es`が既にインストールされていない場合、追加の依存関係が必要

**影響範囲**:
- プロジェクトの依存関係
- バンドルサイズ

**リスクレベル**: 🟢 **低**

**対策**:
- 既存の依存関係を確認
- インストールされていない場合は、`npm install lodash-es`を実行
- または、簡易的なdebounce関数を自前実装

## 3. 修正案の詳細（リスク対策込み）

### 3.1 解決策2: 重複API呼び出しの防止（リスク対策強化版）

**実装内容**:
1. `watch(() => monthlyStore.targets[monthKey])`の条件を厳密化
2. `saveTarget()`直後の更新は検知しない（既に`fetchStats()`が実行済み）
3. キャッシュの有効性チェックを実装

**実装方法**:
```javascript
// MonthlyStatsSection.vue
// 目標設定直後の更新を検知しないためのフラグ
const isTargetSaving = ref(false)

watch(
  () => {
    if (props.currentTab === 'overview') return null
    const monthKey = props.currentTab + '-01'
    const target = monthlyStore.targets[monthKey]
    // 値が存在し、かつ実際に変更された場合のみ再取得
    return target ? JSON.stringify(target) : null
  },
  async (newVal, oldVal) => {
    if (props.currentTab === 'overview') return
    
    // リスク対策1: 初期化時（oldVal === undefined）は実行しない
    if (!oldVal && newVal) {
      // 初期化時の処理は不要（データは既に取得済み）
      return
    }
    
    // リスク対策2: 目標設定直後の更新は検知しない（saveTarget()で既にfetchStats()が実行済み）
    if (isTargetSaving.value) {
      debugLog('目標設定直後の更新を検知 - saveTarget()で既に更新済みのためスキップ')
      isTargetSaving.value = false
      return
    }
    
    // リスク対策3: 値が変更された場合のみ実行
    if (newVal && oldVal && newVal !== oldVal) {
      const [year, month] = props.currentTab.split('-')
      const monthKey = props.currentTab + '-01'
      const cachedStats = monthlyStore.stats[monthKey]
      
      // リスク対策4: キャッシュの有効性を厳密にチェック
      // ただし、saveTarget()で強制的に更新された場合は無視
      if (cachedStats && monthlyStore.lastFetchTime.stats) {
        const cacheAge = Date.now() - monthlyStore.lastFetchTime.stats
        // キャッシュが5分以内であれば使用（ただし、目標設定後は除く）
        if (cacheAge < monthlyStore.cacheDuration) {
          debugLog('キャッシュを使用（目標変更時の統計更新）')
          stats.value = monthlyStore.getStatsByMonth(monthKey)
          return
        }
      }
      
      // キャッシュが無効な場合のみ再取得
      await monthlyStore.fetchStats(parseInt(year), parseInt(month), true)
      await nextTick()
      stats.value = monthlyStore.getStatsByMonth(monthKey)
    }
  },
  { deep: false }
)

// 目標設定時にフラグを設定する方法
// 注意: この方法は、UserSettings.vueとMonthlyStatsSection.vueの間で状態を共有する必要がある
// より安全な方法: watch内で、lastFetchTime.statsを確認し、直近（1秒以内）に更新された場合はスキップ
```

**リスク対策（改善版）**:
- ✅ 初期化時は実行しない（データは既に取得済み）
- ✅ `saveTarget()`で`fetchStats(forceRefresh=true)`が実行されているため、watch内でのキャッシュチェックは不要
- ✅ `saveTarget()`実行後1秒以内の更新は検知しない（`lastFetchTime.stats`を確認）
- ✅ 値が変更された場合のみ実行

**改善された実装方法**:
```javascript
watch(
  () => {
    if (props.currentTab === 'overview') return null
    const monthKey = props.currentTab + '-01'
    const target = monthlyStore.targets[monthKey]
    return target ? JSON.stringify(target) : null
  },
  async (newVal, oldVal) => {
    if (props.currentTab === 'overview') return
    
    // リスク対策1: 初期化時は実行しない
    if (!oldVal && newVal) {
      return
    }
    
    // リスク対策2: 値が変更された場合のみ実行
    if (newVal && oldVal && newVal !== oldVal) {
      const [year, month] = props.currentTab.split('-')
      const monthKey = props.currentTab + '-01'
      
      // リスク対策3: saveTarget()直後の更新は検知しない
      // saveTarget()でfetchStats(forceRefresh=true)が実行される
      // lastFetchTime.statsを確認し、1秒以内の更新はスキップ
      if (monthlyStore.lastFetchTime.stats) {
        const timeSinceLastFetch = Date.now() - monthlyStore.lastFetchTime.stats
        if (timeSinceLastFetch < 1000) {
          debugLog('目標設定直後の更新を検知 - saveTarget()で既に更新済みのためスキップ')
          // データは既に更新されているので、表示を更新
          stats.value = monthlyStore.getStatsByMonth(monthKey)
          return
        }
      }
      
      // キャッシュの有効性をチェック
      const cachedStats = monthlyStore.stats[monthKey]
      if (cachedStats && monthlyStore.lastFetchTime.stats) {
        const cacheAge = Date.now() - monthlyStore.lastFetchTime.stats
        // キャッシュが5分以内であれば使用
        if (cacheAge < monthlyStore.cacheDuration) {
          debugLog('キャッシュを使用（目標変更時の統計更新）')
          stats.value = monthlyStore.getStatsByMonth(monthKey)
          return
        }
      }
      
      // キャッシュが無効な場合のみ再取得
      await monthlyStore.fetchStats(parseInt(year), parseInt(month), true)
      await nextTick()
      stats.value = monthlyStore.getStatsByMonth(monthKey)
    }
  },
  { deep: false }
)
```

**影響範囲**:
- `MonthlyStatsSection.vue`の`watch(() => monthlyStore.targets[monthKey])`
- 目標設定後の統計更新タイミング

### 3.2 解決策3: watchの最適化とdebounce実装（リスク対策強化版）

**実装内容**:
1. `watch(() => props.currentTab)`にdebounceを適用
2. データが既に取得済みの場合、即座にキャッシュを使用（debounceをバイパス）

**実装方法（簡易debounce実装版 - lodash-es不要）**:
```javascript
// MonthlyStatsSection.vue

// 簡易debounce関数の実装（lodash-es不要）
let debounceTimer = null
const debounce = (fn, delay) => {
  return (...args) => {
    if (debounceTimer) {
      clearTimeout(debounceTimer)
    }
    debounceTimer = setTimeout(() => {
      fn(...args)
    }, delay)
  }
}

// watchの最適化（リスク対策: キャッシュがある場合は即座に表示）
watch(() => props.currentTab, (newTab) => {
  // リスク対策: データが既に取得済みの場合、即座にキャッシュを使用（debounceをバイパス）
  if (newTab === 'overview') {
    if (monthlyStore.overview) {
      overviewData.value = monthlyStore.overview
      return // debounceをバイパスして即座に表示
    }
  } else {
    const monthKey = newTab + '-01'
    const cachedStats = monthlyStore.getStatsByMonth(monthKey)
    if (cachedStats) {
      stats.value = cachedStats
      return // debounceをバイパスして即座に表示
    }
  }
  
  // データが存在しない場合のみdebounce後にAPI呼び出し
  const debouncedLoadData = debounce(async () => {
    await loadData()
  }, 50)
  
  debouncedLoadData()
})
```

**リスク対策**:
- ✅ キャッシュがある場合は即座に表示（debounceをバイパス）
- ✅ データが存在しない場合のみdebounce後にAPI呼び出し
- ✅ debounce時間を短く設定（50ms）- ユーザー体験への影響を最小化
- ✅ lodash-es不要（簡易debounce実装）

**影響範囲**:
- `MonthlyStatsSection.vue`の`watch(() => props.currentTab)`
- タブ切り替え時のデータ取得タイミング

### 3.3 解決策6: データ取得の最適化（リスク対策込み）

**実装内容**:
1. データ取得前にキャッシュの有効性を確認
2. 新API使用時のフォールバック処理を最適化

**実装方法**:
```javascript
// MonthlyStatsSection.vue
const loadData = async () => {
  if (isLoadingTargets.value || isLoadingStats.value) return
  
  try {
    if (props.currentTab === 'overview') {
      // リスク対策: キャッシュを確認
      if (monthlyStore.overview) {
        overviewData.value = monthlyStore.overview
        return
      }
      const response = await monthlyStore.fetchOverview()
      overviewData.value = response || {
        total_projects: 0,
        total_income: 0,
        recent_months: []
      }
    } else if (monthlyStore.USE_NEW_API) {
      const monthKey = props.currentTab + '-01'
      
      // リスク対策: キャッシュを確認
      const cachedStats = monthlyStore.getStatsByMonth(monthKey)
      if (cachedStats) {
        stats.value = cachedStats
        return
      }
      
      // リスク対策: キャッシュが存在しない場合のみAPI呼び出し
      // ただし、初期化時に既に取得済みの可能性がある
      if (!monthlyStore.stats || Object.keys(monthlyStore.stats).length === 0) {
        await monthlyStore.fetchCurrentMonthlyData()
      }
      stats.value = monthlyStore.getStatsByMonth(monthKey)
    } else {
      // 旧API使用時: 既存の方法を維持（後方互換性）
      const [year, month] = props.currentTab.split('-')
      
      isLoadingTargets.value = true
      await monthlyStore.fetchTargets(parseInt(year), [parseInt(month)])
      isLoadingTargets.value = false
      
      isLoadingStats.value = true
      await monthlyStore.fetchStats(parseInt(year), parseInt(month))
      isLoadingStats.value = false
      
      // リスク対策: 必要な箇所のみnextTick()を維持
      await nextTick()
      stats.value = monthlyStore.getStatsByMonth(props.currentTab + '-01')
    }
  } catch (error) {
    errorLog('データ読み込みエラー:', error)
  } finally {
    isLoadingTargets.value = false
    isLoadingStats.value = false
  }
}
```

**リスク対策**:
- ✅ キャッシュの有効性を厳密にチェック
- ✅ データが既に取得済みの場合、即座にキャッシュを使用
- ✅ データが存在しない場合のみAPI呼び出し

**影響範囲**:
- `MonthlyStatsSection.vue`の`loadData()`
- データ取得のタイミング

### 3.4 解決策4: nextTickの削減（リスク対策込み）

**実装内容**:
1. 不要な`nextTick()`を削除
2. 必要な箇所のみ`nextTick()`を維持

**削除可能なnextTick**:
```javascript
// 修正前
await nextTick()
stats.value = monthlyStore.getStatsByMonth(monthKey)
await nextTick()

// 修正後（不要なnextTickを削除）
stats.value = monthlyStore.getStatsByMonth(monthKey)
// nextTickは削除（Vueのリアクティブシステムで自動的に更新される）
```

**維持が必要なnextTick**:
```javascript
// watch(() => monthlyStore.targets[monthKey])内
await monthlyStore.fetchStats(parseInt(year), parseInt(month), true)
await nextTick() // ← このnextTickは維持（データ更新後の表示更新を確実にする）
stats.value = monthlyStore.getStatsByMonth(monthKey)
```

**リスク対策**:
- ✅ 必要な箇所のみ`nextTick()`を維持
- ✅ 削除する`nextTick()`を慎重に選定
- ✅ テストで動作確認を徹底

**影響範囲**:
- `MonthlyStatsSection.vue`の複数箇所
- リアクティブな更新のタイミング

## 4. 総合リスク評価

### 4.1 リスクマトリクス

| 解決策 | リスクレベル | 影響範囲 | 対策の妥当性 | 追加対策の必要性 |
|--------|------------|---------|------------|----------------|
| 解決策2: 重複API呼び出し防止 | 🔴 最高 | 目標設定後の統計更新 | ✅ 対策妥当 | ⚠️ 追加対策必要 |
| 解決策3: watch最適化とdebounce | 🟠 高 | タブ切り替え時のデータ取得 | ✅ 対策妥当 | ✅ 対策十分 |
| 解決策6: データ取得最適化 | 🟡 中 | データ整合性 | ✅ 対策妥当 | ✅ 対策十分 |
| 解決策4: nextTick削減 | 🟡 中 | レンダリングタイミング | ✅ 対策妥当 | ✅ 対策十分 |

### 4.2 総合評価

**リスクレベル**: 🟠 **高**（追加対策により低リスク化可能）

**理由**:
1. **解決策2に追加対策が必要**:
   - `saveTarget()`直後の更新を検知しないためのロジック追加
   - `lastFetchTime.stats`を確認し、1秒以内の更新はスキップ

2. **その他の解決策は対策が妥当**:
   - debounceはキャッシュがある場合は即座に表示
   - キャッシュ戦略は`saveTarget()`で強制的にクリア済み
   - nextTick削減は必要な箇所のみ維持

### 4.3 推奨実装順序（リスクを考慮）

#### フェーズ2-1: 低リスク修正（最初に実施）
1. ✅ **解決策6: データ取得の最適化**
   - リスク: 🟡 中（データ整合性への影響）
   - キャッシュの有効性チェックを実装

2. ✅ **解決策4: nextTickの削減**
   - リスク: 🟡 中（レンダリングタイミングへの影響）
   - 必要な箇所のみ`nextTick()`を維持

#### フェーズ2-2: 高リスク修正（慎重に実施）
3. ✅ **解決策2: 重複API呼び出しの防止**
   - リスク: 🔴 最高（目標設定後の統計更新への影響）
   - 追加対策を実装（`lastFetchTime.stats`チェック）

4. ✅ **解決策3: watchの最適化とdebounce実装**
   - リスク: 🟠 高（タブ切り替え時のデータ取得への影響）
   - キャッシュがある場合は即座に表示

## 5. 追加対策の詳細

### 5.1 解決策2への追加対策

**問題**: `saveTarget()`直後の更新をwatchが検知し、重複して`fetchStats()`が実行される可能性

**追加対策**: `lastFetchTime.stats`を確認し、1秒以内の更新はスキップ

**実装**:
```javascript
// watch(() => monthlyStore.targets[monthKey])内
if (newVal && oldVal && newVal !== oldVal) {
  const [year, month] = props.currentTab.split('-')
  const monthKey = props.currentTab + '-01'
  
  // 追加対策: saveTarget()直後の更新は検知しない
  // saveTarget()でfetchStats(forceRefresh=true)が実行される
  // lastFetchTime.statsを確認し、1秒以内の更新はスキップ
  if (monthlyStore.lastFetchTime.stats) {
    const timeSinceLastFetch = Date.now() - monthlyStore.lastFetchTime.stats
    if (timeSinceLastFetch < 1000) {
      debugLog('目標設定直後の更新を検知 - saveTarget()で既に更新済みのためスキップ')
      // データは既に更新されているので、表示を更新
      stats.value = monthlyStore.getStatsByMonth(monthKey)
      return
    }
  }
  
  // 通常の処理（キャッシュチェック → API呼び出し）
  // ...
}
```

## 6. テスト項目

### 6.1 機能テスト
- [ ] タブ切り替えが正常に動作することを確認
- [ ] データ表示が正常に更新されることを確認
- [ ] **目標設定後の統計更新が正常に動作することを確認**（重要）
- [ ] キャッシュが正常に機能することを確認
- [ ] debounceが正常に機能することを確認

### 6.2 パフォーマンステスト
- [ ] タブ切り替え時の表示時間測定（目標: < 0.5秒）
- [ ] API呼び出し回数の測定（タブ切り替え時: 0-1回、目標設定後: 1回）
- [ ] キャッシュの有効性確認

### 6.3 エッジケーステスト
- [ ] 素早いタブ切り替え（連続3回以上）時の動作確認
- [ ] 目標設定直後のタブ切り替え時の動作確認
- [ ] 目標設定後にすぐタブを切り替えた場合の動作確認

---

**注意**: このドキュメントはリスク分析と対策を含む修正案であり、実装指示ではありません。実装を開始する前に、ユーザーからの明示的な指示を待ってください。

