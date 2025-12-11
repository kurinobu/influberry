# Step 2 Phase 2: パフォーマンス最適化 - 評価レポート

**作成日**: 2025年10月31日  
**評価者**: AI Assistant  
**対象**: ステージング環境でのブラウザテスト結果

## 1. テスト環境

- **環境**: ステージング環境（https://staging.influberry.jp）
- **ブラウザ**: Chrome（開発者ツール）
- **テスト日時**: 2025年10月31日 11:28-11:29頃
- **テスト内容**: ページ読み込み、タブ切り替え、データ表示

## 2. 報告された問題

### 2.1 問題の詳細

**現象**:
> 「スケルトンの後に当月が一度表示され再度スケルトンになってから最後表示されます。これはイライラします。」

**問題の流れ**:
1. スケルトン表示（初回）
2. 当月データが一度表示される
3. 再度スケルトン表示になる
4. 最終的にデータが表示される

**ユーザー体験への影響**:
- データがちらつく（フリッカー）
- ローディング状態が不安定
- ユーザーがイライラする

## 3. ログ分析結果

### 3.1 ログ出力の時系列分析

**タイムライン**:

```
11:28:54.931 - タブ更新完了: {previousTab: 'overview', newTab: '2025-10', currentMonthTab: '2025-10'}
11:28:54.932 - Phase 2: リアクティブな更新の同期化を実行
11:28:54.932 - Phase 2: 第1回nextTick完了
11:28:54.932 - Phase 2: 第2回nextTick完了
11:28:54.932 - Phase 2: 同期化後の状態確認
11:28:54.932 - Phase 2: リアクティブな更新の同期化完了
11:29:07.128 - Phase 2: リアクティブな更新の同期化を実行（約12秒後）
11:29:07.128 - Phase 2: 第1回nextTick完了
11:29:07.128 - Phase 2: 第2回nextTick完了
11:29:07.128 - Phase 2: 同期化後の状態確認
11:29:07.128 - Phase 2: リアクティブな更新の同期化完了
```

### 3.2 パフォーマンス測定結果

| 指標 | 測定値 | 以前の値（Phase 1後） | 変化 |
|------|--------|---------------------|------|
| **Finish Time** | **22.81秒** | 59.63秒（Phase 1後） | ✅ **大幅改善（-36.82秒）** |
| **DOMContentLoaded** | **1.37秒** | 842ms（Phase 1後） | ❌ **悪化（+528ms）** |
| **Load Time** | **2.86秒** | 6.22秒（Phase 1後） | ✅ **改善（-3.36秒）** |
| **Scripting** | 544ms | 539ms（Phase 1後） | ⚠️ **ほぼ同等（+5ms）** |
| **System** | 211ms | 355ms（Phase 1後） | ✅ **改善（-144ms）** |
| **Rendering** | 54ms | 58ms（Phase 1後） | ✅ **改善（-4ms）** |
| **Loading** | 8ms | 10ms（Phase 1後） | ✅ **改善（-2ms）** |
| **Painting** | 6ms | 5ms（Phase 1後） | ⚠️ **ほぼ同等（+1ms）** |

### 3.3 問題の根本原因分析

#### 原因1: watch(() => props.currentTab)のdebounceとキャッシュ優先の競合

**問題の流れ**:
1. タブ切り替え（'overview' → '2025-10'）
2. `watch(() => props.currentTab)`がトリガー
3. キャッシュがある場合、即座に`stats.value = cachedStats`を設定（表示される）
4. しかし、その直後に`debouncedLoadData()`が実行される
5. 50ms後に`loadData()`が呼ばれる
6. `loadData()`内で、キャッシュがあっても再度API呼び出しが実行される可能性がある
7. `monthlyStore.loading`が`true`になり、再度スケルトン表示になる
8. データ取得完了後、`loading`が`false`になり、最終的に表示される

**コード分析**:
```javascript
// MonthlyStatsSection.vue (Phase 2修正後)
watch(() => props.currentTab, (newTab) => {
  // リスク対策: キャッシュがある場合は即座に表示
  if (newTab === 'overview') {
    if (monthlyStore.overview) {
      overviewData.value = monthlyStore.overview
      return // debounceをバイパス
    }
  } else {
    const monthKey = newTab + '-01'
    const cachedStats = monthlyStore.getStatsByMonth(monthKey)
    if (cachedStats) {
      stats.value = cachedStats
      return // debounceをバイパス ← ここでreturnしているが...
    }
  }
  
  // 問題: キャッシュがある場合でも、このコードは実行されないはず...
  // しかし、何らかの理由で実行されている可能性がある
  const debouncedLoadData = debounce(async () => {
    await loadData() // ← これが実行されると、再度データ取得が行われる
  }, 50)
  
  debouncedLoadData()
})
```

**問題点**:
- キャッシュがある場合は`return`しているが、`debouncedLoadData()`が既に設定されている可能性がある
- または、`watch`が複数回トリガーされている可能性がある

#### 原因2: loadData()内のキャッシュチェック不足

**コード分析**:
```javascript
// MonthlyStatsSection.vue
const loadData = async () => {
  if (isLoadingTargets.value || isLoadingStats.value) return
  
  try {
    if (props.currentTab === 'overview') {
      // Phase 2: キャッシュを確認
      if (monthlyStore.overview) {
        overviewData.value = monthlyStore.overview
        return // ← ここでreturnしているが、既に表示されている
      }
      // ...
    } else if (monthlyStore.USE_NEW_API) {
      // Phase 2: 新API使用時 - キャッシュを確認
      const monthKey = props.currentTab + '-01'
      const cachedStats = monthlyStore.getStatsByMonth(monthKey)
      if (cachedStats) {
        stats.value = cachedStats
        return // ← ここでreturnしているが、既に表示されている
      }
      
      // 問題: キャッシュがない場合のみAPI呼び出し
      // しかし、monthlyStore.loadingがtrueになると、スケルトン表示になる
      debugLog('🔧 データ未取得のため、fetchCurrentMonthlyData()を呼び出し')
      await monthlyStore.fetchCurrentMonthlyData() // ← この時点でloadingがtrueになる
      stats.value = monthlyStore.getStatsByMonth(monthKey)
    }
  }
}
```

**問題点**:
- キャッシュがある場合は`return`しているが、既に`stats.value`が設定されている
- しかし、`monthlyStore.loading`が`true`の状態が残っている可能性がある
- または、`loadData()`が複数回呼ばれている可能性がある

#### 原因3: monthlyStore.loadingの状態管理

**テンプレート分析**:
```vue
<!-- MonthlyStatsSection.vue -->
<div v-if="!monthlyStore.loading" class="monthly-stats-section">
  <!-- 通常表示 -->
</div>

<div v-else-if="monthlyStore.loading" class="monthly-stats-section">
  <!-- スケルトン表示 -->
</div>
```

**問題点**:
- `monthlyStore.loading`が`true`の時、スケルトン表示になる
- `monthlyStore.loading`が`false`の時、通常表示になる
- しかし、データ取得が複数回実行されると、`loading`が`true`→`false`→`true`→`false`と変化する可能性がある

## 4. 評価と結論

### 4.1 Phase 2修正の効果

#### ✅ 成功した点

1. **Finish Timeの大幅改善**
   - **22.81秒**（以前の59.63秒より**-36.82秒**改善）
   - Phase 1の修正と合わせて、大幅なパフォーマンス向上

2. **Load Timeの改善**
   - **2.86秒**（以前の6.22秒より**-3.36秒**改善）
   - リソース読み込みの最適化が効果的

3. **System Timeの改善**
   - **211ms**（以前の355msより**-144ms**改善）
   - システム負荷の軽減

#### ⚠️ 改善が必要な点

1. **DOMContentLoadedの悪化**
   - **1.37秒**（以前の842msより**+528ms**悪化）
   - キャッシュ優先表示の実装が、初期レンダリングに影響している可能性

2. **スケルトン表示のフリッカー問題**
   - キャッシュがある場合でも、スケルトンが表示される
   - データがちらつく（フリッカー）
   - ユーザー体験の低下

### 4.2 問題の根本原因

**主な原因**:
1. `watch(() => props.currentTab)`のdebounceとキャッシュ優先の競合
2. `loadData()`が複数回呼ばれる可能性
3. `monthlyStore.loading`の状態管理が不適切

**影響範囲**:
- タブ切り替え時のデータ表示
- ユーザー体験（フリッカー）
- ローディング状態の一貫性

### 4.3 総合評価

**Phase 2修正の評価**: ⚠️ **部分的成功（問題あり）**

**理由**:
1. ✅ パフォーマンス（Finish Time）は大幅改善
2. ✅ Load Timeも改善
3. ⚠️ DOMContentLoadedが悪化
4. ❌ スケルトン表示のフリッカー問題が発生

**結論**:
- Phase 2修正は、パフォーマンス向上という目的は達成
- しかし、スケルトン表示のフリッカー問題が新たに発生
- この問題は、ユーザー体験に大きな影響を与える

## 5. 推奨される修正案

### 5.1 問題の解決策

#### 解決策1: watch(() => props.currentTab)の修正

**問題**: キャッシュがある場合でも、`debouncedLoadData()`が実行される可能性がある

**修正案**:
```javascript
// MonthlyStatsSection.vue
let debounceTimer = null
let lastProcessedTab = null // 最後に処理したタブを記録

watch(() => props.currentTab, (newTab) => {
  // 同じタブが既に処理済みの場合はスキップ
  if (lastProcessedTab === newTab) {
    return
  }
  
  // リスク対策: キャッシュがある場合は即座に表示
  if (newTab === 'overview') {
    if (monthlyStore.overview) {
      overviewData.value = monthlyStore.overview
      lastProcessedTab = newTab
      return // debounceをバイパス
    }
  } else {
    const monthKey = newTab + '-01'
    const cachedStats = monthlyStore.getStatsByMonth(monthKey)
    if (cachedStats) {
      stats.value = cachedStats
      lastProcessedTab = newTab
      return // debounceをバイパス
    }
  }
  
  // データが存在しない場合のみdebounce後にAPI呼び出し
  // 既存のタイマーをクリア
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  
  lastProcessedTab = newTab
  debounceTimer = setTimeout(async () => {
    await loadData()
    debounceTimer = null
  }, 50)
})
```

#### 解決策2: loadData()内のローディング状態管理の改善

**問題**: `monthlyStore.loading`が不適切に`true`になる

**修正案**:
```javascript
// MonthlyStatsSection.vue
const loadData = async () => {
  if (isLoadingTargets.value || isLoadingStats.value) return
  
  // キャッシュがある場合は、loadingをtrueにしない
  if (props.currentTab === 'overview') {
    if (monthlyStore.overview) {
      overviewData.value = monthlyStore.overview
      return
    }
  } else if (monthlyStore.USE_NEW_API) {
    const monthKey = props.currentTab + '-01'
    const cachedStats = monthlyStore.getStatsByMonth(monthKey)
    if (cachedStats) {
      stats.value = cachedStats
      return // loadingをtrueにしない
    }
  }
  
  // キャッシュがない場合のみ、データ取得を実行
  // この時点でloadingがtrueになる
  try {
    // ... データ取得処理 ...
  } catch (error) {
    // ... エラー処理 ...
  }
}
```

#### 解決策3: テンプレート側のローディング状態チェック改善

**問題**: `monthlyStore.loading`だけでスケルトン表示を制御している

**修正案**:
```vue
<!-- MonthlyStatsSection.vue -->
<!-- データが存在する場合は、loadingがtrueでも表示 -->
<div v-if="stats || overviewData" class="monthly-stats-section">
  <!-- 通常表示 -->
</div>

<!-- データが存在しない場合のみ、スケルトン表示 -->
<div v-else-if="monthlyStore.loading" class="monthly-stats-section">
  <!-- スケルトン表示 -->
</div>

<!-- データが存在せず、loadingもfalseの場合 -->
<div v-else class="monthly-stats-section">
  <!-- 空の状態表示 -->
</div>
```

### 5.2 優先順位

1. **最優先**: 解決策3（テンプレート側の修正）
   - 即座に問題を解決できる
   - 影響範囲が小さい
   - ユーザー体験への影響が大きい

2. **高優先**: 解決策1（watchの修正）
   - 根本原因の解決
   - フリッカーの完全解消

3. **中優先**: 解決策2（loadDataの修正）
   - ローディング状態管理の改善
   - 長期的な保守性向上

## 6. 次のステップ

### 6.1 緊急対応（推奨）

**優先度**: 🔴 **最高**

**対応内容**:
- 解決策3（テンプレート側の修正）を実施
- データが存在する場合は、loadingがtrueでも表示する
- これにより、フリッカー問題を即座に解決できる

### 6.2 根本対応（推奨）

**優先度**: 🟠 **高**

**対応内容**:
- 解決策1（watchの修正）を実施
- 解決策2（loadDataの修正）を実施
- これにより、根本原因を解決し、長期的な保守性を向上

### 6.3 テスト項目

**修正後のテスト項目**:
- [ ] タブ切り替え時にスケルトンがフリッカーしないことを確認
- [ ] キャッシュがある場合、即座に表示されることを確認
- [ ] キャッシュがない場合、スケルトンが表示されることを確認
- [ ] データ取得中も、既存データが表示されることを確認

---

**注意**: このレポートは調査分析と評価であり、修正指示ではありません。修正を開始する前に、ユーザーからの明示的な指示を待ってください。

