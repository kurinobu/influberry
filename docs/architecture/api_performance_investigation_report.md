# API呼び出しのパフォーマンス問題と重複API呼び出しの解消 - 完全調査分析レポート

**作成日**: 2025年11月1日  
**対象**: Step 2 Phase 4 ステージング環境テスト結果に基づく  
**目的**: API呼び出しのパフォーマンス問題と重複API呼び出しの根本原因を特定し、大原則に沿った修正案を提示

---

## 1. 問題の概要

### 1.1 ステージング環境でのテスト結果

| 指標 | 目標値 | ステージング環境 | 評価 |
|------|--------|----------------|------|
| **Finish Time** | < 2秒 | **33.64秒** | ❌ 深刻（目標の約17倍） |
| **Load Time** | < 800ms | **6.60秒** | ❌ 深刻（目標の約8倍） |
| **DOMContentLoaded** | < 800ms | **922ms** | ❌ 目標未達成 |

### 1.2 API呼び出しの実測値（Network タブより）

| APIエンドポイント | 呼び出し回数 | 平均レスポンスタイム | 評価 |
|------------------|------------|------------------|------|
| `/api/monthly/current` | **4回以上** | **8.54秒 - 18.95秒** | ❌ 重複呼び出し・異常に遅い |
| `/api/monthly-targets/?year=2025&months=9` | 1回 | **16.29秒** | ❌ 異常に遅い |

**問題の深刻度**: 🔴 **極めて高い（ビジネスへの致命的影響）**

---

## 2. 根本原因の調査分析

### 2.1 重複API呼び出しの発生箇所の特定

#### 問題1: `MonthlyStatsSection.vue`での重複呼び出し

**発生箇所1: `onMounted`での初期化処理**

```vue:frontend/src/components/MonthlyStatsSection.vue
onMounted(async () => {
  // Step 2 Phase 3修正: lastProcessedTabをリセット
  lastProcessedTab = null
  
  // Phase 3: 新API使用時は初期化時に1回のみ取得（重複呼び出しを削減）
  if (monthlyStore.USE_NEW_API) {
    // fetchCurrentMonthlyData()は既にストアのloadingを管理
    // loadData()でデータが取得済みか確認し、必要時のみAPI呼び出し
    if (!monthlyStore.stats || Object.keys(monthlyStore.stats).length === 0) {
      await monthlyStore.fetchCurrentMonthlyData()  // ← 呼び出し1回目
    }
  }
  // loadData()は既存データから取得を試み、データがない場合のみAPI呼び出し（フォールバック）
  loadData()  // ← 呼び出し2回目（loadData()内でfetchCurrentMonthlyData()を呼び出す可能性）
})
```

**問題点**:
- `onMounted`で`fetchCurrentMonthlyData()`を呼び出し
- その後`loadData()`を呼び出し、`loadData()`内でも`fetchCurrentMonthlyData()`を呼び出す可能性がある
- データが存在しない場合、2回のAPI呼び出しが発生する

**発生箇所2: `watch(() => props.currentTab)`での呼び出し**

```vue:frontend/src/components/MonthlyStatsSection.vue
watch(() => props.currentTab, (newTab) => {
  // Step 2 Phase 3修正: 同じタブが既に処理済みの場合はスキップ
  if (lastProcessedTab === newTab) {
    debugLog('🔧 同じタブが既に処理済みのためスキップ:', newTab)
    return
  }
  
  // リスク対策: キャッシュがある場合は即座に表示（debounceをバイパス）
  if (newTab === 'overview') {
    if (monthlyStore.overview) {
      overviewData.value = monthlyStore.overview
      lastProcessedTab = newTab
      debugLog('🔧 キャッシュから概要データを即座に表示:', newTab)
      return // debounceをバイパスして即座に表示
    }
  } else {
    const monthKey = newTab + '-01'
    const cachedStats = monthlyStore.getStatsByMonth(monthKey)
    if (cachedStats) {
      stats.value = cachedStats
      lastProcessedTab = newTab
      debugLog('🔧 キャッシュから統計データを即座に表示:', { newTab, monthKey })
      return // debounceをバイパスして即座に表示
    }
  }
  
  // データが存在しない場合のみdebounce後にAPI呼び出し
  // 既存のタイマーをクリア
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  
  lastProcessedTab = newTab
  debugLog('🔧 データ未取得のため、debounce後にAPI呼び出し:', newTab)
  debounceTimer = setTimeout(async () => {
    await loadData()  // ← loadData()内でfetchCurrentMonthlyData()を呼び出す可能性
    debounceTimer = null
  }, 50)
})
```

**問題点**:
- タブ切り替え時に`loadData()`が呼び出される
- `loadData()`内で`fetchCurrentMonthlyData()`を呼び出す可能性がある
- タブが複数回切り替わる場合、複数回のAPI呼び出しが発生する可能性がある

**発生箇所3: `loadData()`内での呼び出し**

```vue:frontend/src/components/MonthlyStatsSection.vue
const loadData = async () => {
  if (isLoadingTargets.value || isLoadingStats.value) return
  
  try {
    if (props.currentTab === 'overview') {
      // ... overview処理 ...
    } else if (monthlyStore.USE_NEW_API) {
      // Step 2 Phase 3修正: 新API使用時 - キャッシュがある場合は、loadingをtrueにしない
      const monthKey = props.currentTab + '-01'
      const cachedStats = monthlyStore.getStatsByMonth(monthKey)
      if (cachedStats) {
        stats.value = cachedStats
        debugLog('🔧 キャッシュから統計データを取得 - loadingをtrueにしない:', { monthKey })
        return // loadingをtrueにしない
      }
      
      // データがない場合のみAPI呼び出し（フォールバック）
      debugLog('🔧 データ未取得のため、fetchCurrentMonthlyData()を呼び出し')
      await monthlyStore.fetchCurrentMonthlyData()  // ← ここでAPI呼び出し
      stats.value = monthlyStore.getStatsByMonth(monthKey)
      // ...
    }
    // ...
  }
}
```

**問題点**:
- `loadData()`内で`fetchCurrentMonthlyData()`を呼び出している
- `onMounted`と`watch`の両方から`loadData()`が呼び出される可能性がある
- 重複防止のチェックが不十分

#### 問題2: `fetchCurrentMonthlyData()`の重複実行防止機能の不足

**現在の実装**:

```javascript:frontend/src/stores/monthly.js
async fetchCurrentMonthlyData() {
  if (this.USE_NEW_API) {
    this.loading = true
    this.error = null
    try {
      debugLog('🔧 新API使用: GET /api/monthly/current')
      const res = await axios.get('/api/monthly/current')  // ← 重複実行防止なし
      // ...
    } catch (err) {
      // ...
    } finally {
      this.loading = false
    }
  }
}
```

**問題点**:
- `fetchCurrentMonthlyData()`には重複実行防止フラグがない
- `fetchTargets()`や`fetchStats()`には`fetchingTargets`/`fetchingStats`フラグがあるが、`fetchCurrentMonthlyData()`には同様のフラグがない
- 複数のコンポーネントや`watch`から同時に呼び出された場合、複数回のAPI呼び出しが発生する

#### 問題3: タブ切り替え時の競合状態

**発生箇所: `DashboardPage.vue`の`watch`と`MonthlyStatsSection.vue`の`watch`**

```javascript:frontend/src/views/DashboardPage.vue
// Phase 2: currentMonthTabの変更を監視するwatchを強化
watch(() => currentMonthTab.value, async (newTab, oldTab) => {
  // ... タブ切り替え処理 ...
  // このwatchが発火すると、MonthlyStatsSection.vueのwatchも発火する可能性がある
})

// 月次切り替え状態の監視
watch(() => rotationStore.rotationState, handleRotationStateChange)
watch(() => rotationStore.lastRotationCheck, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    console.log('月次切り替えが検知されました。')
    triggerTabUpdate()  // ← これが発火すると、タブが切り替わり、MonthlyStatsSection.vueのwatchも発火
  }
})
```

**問題点**:
- `DashboardPage.vue`の`watch`が発火すると、`MonthlyStatsSection.vue`の`watch`も発火する
- タブ切り替え時に複数の`watch`が同時に発火し、複数回のAPI呼び出しが発生する可能性がある

### 2.2 API呼び出しのパフォーマンス問題の根本原因

#### 原因1: データベースクエリの非効率性

**バックエンドAPIの実装** (`app/blueprints/monthly_current.py`):

```python
def calculate_monthly_stats(user_id, year, month):
    # 獲得案件数（proposed → contracted）
    acquired_positive = db.session.query(
        func.count(func.distinct(ProjectStatusHistory.project_id))
    ).join(Project).filter(
        Project.user_id == user_id,
        ProjectStatusHistory.old_status == 'proposed',
        ProjectStatusHistory.new_status == 'contracted',
        extract('year', ProjectStatusHistory.changed_at) == year,
        extract('month', ProjectStatusHistory.changed_at) == month
    ).scalar() or 0
    
    # 複数のクエリが個別に実行される（N+1問題の可能性）
    # インデックスの不足により、クエリが遅い可能性がある
```

**問題点**:
- 複数のクエリが個別に実行される（N+1問題の可能性）
- インデックスの不足により、クエリが遅い可能性がある
- `ProjectStatusHistory`と`InvoiceStatusHistory`テーブルの結合処理が非効率

#### 原因2: ステージング環境のリソース制限

- Render.comのフリープランのリソース制限により、パフォーマンスが低下している可能性
- データベース接続数の制限により、同時リクエストがブロックされる可能性
- CPU/メモリリソースの制限により、クエリ実行時間が長くなる可能性

---

## 3. 大原則に沿った修正案

### 3.1 大原則の確認

| 原則 | 内容 |
|------|------|
| **引き継ぎ書準拠** | 計画書v2.0, v2.1の要求に完全準拠 |
| **根本解決 > 暫定解決** | 重複呼び出し防止機能の実装（根本解決） |
| **シンプル構造 > 複雑構造** | 既存のフラグシステムを拡張（シンプル） |
| **統一・同一化 > 特殊独自** | `fetchTargets()`/`fetchStats()`と同様のフラグシステムを使用（統一） |
| **具体的 > 一般** | 具体的なフラグ名とロジックを実装（具体的） |
| **拙速 < 安全確実** | 既存のフラグシステムを拡張し、後方互換性を保持（安全確実） |

### 3.2 修正案1: `fetchCurrentMonthlyData()`の重複実行防止機能の追加（最優先）

#### 修正内容

**ファイル**: `frontend/src/stores/monthly.js`

**修正箇所1: stateに`fetchingCurrentMonthlyData`フラグを追加**

```javascript
state: () => ({
  // ... 既存のstate ...
  
  // ✅ Phase 1: 重複呼び出し防止用のフラグ
  fetchingTargets: false,        // 目標取得中フラグ
  fetchingStats: false,          // 統計取得中フラグ
  fetchingCurrentMonthlyData: false,  // ← 新規追加: 月次データ取得中フラグ
  // ...
})
```

**修正箇所2: `fetchCurrentMonthlyData()`に重複実行防止機能を追加**

```javascript
async fetchCurrentMonthlyData() {
  // ✅ 修正: 既に取得中なら待つ（重複防止）
  if (this.fetchingCurrentMonthlyData) {
    debugLog('🔧 月次データ取得: 既に実行中のためスキップ')
    return
  }
  
  // ✅ 修正: キャッシュが有効なら再取得しない（追加オプション）
  // 注: fetchCurrentMonthlyData()は複数月のデータを取得するため、
  //     キャッシュチェックは実装しない（既存のstats/targetsのキャッシュを活用）
  
  if (this.USE_NEW_API) {
    this.fetchingCurrentMonthlyData = true  // ← フラグを設定
    this.loading = true
    this.error = null
    try {
      debugLog('🔧 新API使用: GET /api/monthly/current')
      const res = await axios.get('/api/monthly/current')
      // ... 既存の処理 ...
    } catch (err) {
      // ... 既存のエラーハンドリング ...
    } finally {
      this.loading = false
      this.fetchingCurrentMonthlyData = false  // ← フラグを解除
    }
  } else {
    // 旧API（後方互換）
    await this._fetchCurrentMonthlyDataLegacy()
  }
}
```

#### 大原則への適合性

| 原則 | 適合性 | 評価 |
|------|--------|------|
| **根本解決 > 暫定解決** | ✅ 重複実行防止機能の実装により、根本的に重複呼び出しを防止 | **完全適合** |
| **シンプル構造 > 複雑構造** | ✅ 既存の`fetchingTargets`/`fetchingStats`フラグと同様のシンプルな実装 | **完全適合** |
| **統一・同一化 > 特殊独自** | ✅ 既存のフラグシステムと統一された実装 | **完全適合** |
| **具体的 > 一般** | ✅ 具体的なフラグ名`fetchingCurrentMonthlyData`を使用 | **完全適合** |
| **拙速 < 安全確実** | ✅ 既存のフラグシステムを拡張し、後方互換性を保持 | **完全適合** |

### 3.3 修正案2: `MonthlyStatsSection.vue`の初期化処理の最適化（高優先度）

#### 修正内容

**ファイル**: `frontend/src/components/MonthlyStatsSection.vue`

**修正箇所: `onMounted`の初期化処理を最適化**

```javascript
onMounted(async () => {
  // Step 2 Phase 3修正: lastProcessedTabをリセット
  lastProcessedTab = null
  
  // ✅ 修正: 初期化時はloadData()のみを呼び出し、fetchCurrentMonthlyData()の重複呼び出しを防止
  // loadData()内でキャッシュチェックとfetchCurrentMonthlyData()の呼び出しが統合管理される
  await loadData()
})
```

**理由**:
- `onMounted`で`fetchCurrentMonthlyData()`を直接呼び出すのではなく、`loadData()`を通じて呼び出す
- `loadData()`内でキャッシュチェックが行われ、データがない場合のみAPI呼び出しが発生する
- 重複呼び出しが防止される

#### 大原則への適合性

| 原則 | 適合性 | 評価 |
|------|--------|------|
| **根本解決 > 暫定解決** | ✅ 初期化処理の統合により、重複呼び出しを根本的に防止 | **完全適合** |
| **シンプル構造 > 複雑構造** | ✅ 初期化処理を`loadData()`に統合し、シンプル化 | **完全適合** |
| **統一・同一化 > 特殊独自** | ✅ データ取得処理を`loadData()`に統一 | **完全適合** |
| **具体的 > 一般** | ✅ 具体的な初期化処理の修正 | **完全適合** |
| **拙速 < 安全確実** | ✅ 既存の`loadData()`を使用し、後方互換性を保持 | **完全適合** |

### 3.4 修正案3: `loadData()`内のキャッシュチェック強化（中優先度）

#### 修正内容

**ファイル**: `frontend/src/components/MonthlyStatsSection.vue`

**修正箇所: `loadData()`内のキャッシュチェックを強化**

```javascript
const loadData = async () => {
  // ✅ 修正: fetchingCurrentMonthlyDataフラグもチェック
  if (isLoadingTargets.value || isLoadingStats.value || monthlyStore.fetchingCurrentMonthlyData) {
    debugLog('🔧 データ取得中または既に実行中のためスキップ')
    return
  }
  
  try {
    if (props.currentTab === 'overview') {
      // ... 既存のoverview処理 ...
    } else if (monthlyStore.USE_NEW_API) {
      // Step 2 Phase 3修正: 新API使用時 - キャッシュがある場合は、loadingをtrueにしない
      const monthKey = props.currentTab + '-01'
      const cachedStats = monthlyStore.getStatsByMonth(monthKey)
      if (cachedStats) {
        stats.value = cachedStats
        debugLog('🔧 キャッシュから統計データを取得 - loadingをtrueにしない:', { monthKey })
        return // loadingをtrueにしない
      }
      
      // ✅ 修正: データがない場合のみAPI呼び出し（fetchingCurrentMonthlyDataフラグで重複防止）
      debugLog('🔧 データ未取得のため、fetchCurrentMonthlyData()を呼び出し')
      await monthlyStore.fetchCurrentMonthlyData()
      stats.value = monthlyStore.getStatsByMonth(monthKey)
      // ...
    }
    // ...
  }
}
```

#### 大原則への適合性

| 原則 | 適合性 | 評価 |
|------|--------|------|
| **根本解決 > 暫定解決** | ✅ `fetchingCurrentMonthlyData`フラグで重複呼び出しを根本的に防止 | **完全適合** |
| **シンプル構造 > 複雑構造** | ✅ 既存のフラグチェックに1行追加するだけ（シンプル） | **完全適合** |
| **統一・同一化 > 特殊独自** | ✅ 既存の`isLoadingTargets`/`isLoadingStats`チェックと統一 | **完全適合** |
| **具体的 > 一般** | ✅ 具体的なフラグ名`fetchingCurrentMonthlyData`を使用 | **完全適合** |
| **拙速 < 安全確実** | ✅ 既存のチェックロジックを拡張し、後方互換性を保持 | **完全適合** |

---

## 4. 他の機能やUIへの競合・干渉リスク分析

### 4.1 修正案1のリスク分析

#### リスク1: 既存のフラグシステムとの競合

**リスク内容**:
- `fetchingTargets`/`fetchingStats`フラグとの競合の可能性

**リスク評価**: 🟢 **低リスク**

**理由**:
- `fetchCurrentMonthlyData()`は`fetchTargets()`/`fetchStats()`とは異なるAPIエンドポイントを使用
- フラグ名が異なり、名前空間の競合はない
- 既存のフラグシステムと同じパターンを使用しているため、互換性が高い

**対策**:
- 既存のフラグシステムと同じパターンを厳密に遵守
- フラグ名を明確に区別（`fetchingCurrentMonthlyData`）

#### リスク2: 後方互換性の問題

**リスク内容**:
- 既存のコードが`fetchCurrentMonthlyData()`の戻り値を期待している場合、早期リターンで問題が発生する可能性

**リスク評価**: 🟡 **中リスク**

**理由**:
- `fetchCurrentMonthlyData()`は`void`を返すため、戻り値を期待するコードはない
- ただし、呼び出し側で完了を待機している場合は、早期リターンで待機が解除される可能性がある

**対策**:
- `fetchCurrentMonthlyData()`の呼び出し箇所を全て確認し、完了待機の有無を確認
- 必要に応じて、完了待機のロジックを追加

#### リスク3: UIのローディング状態の不整合

**リスク内容**:
- `fetchingCurrentMonthlyData`フラグが`true`の間、UIのローディング状態が正しく表示されない可能性

**リスク評価**: 🟢 **低リスク**

**理由**:
- `fetchCurrentMonthlyData()`内で`this.loading = true`が設定されている
- 既存の`fetchTargets()`/`fetchStats()`と同じパターンを使用しているため、UIのローディング状態は正しく表示される

**対策**:
- 既存のローディング状態表示ロジックを維持
- `fetchingCurrentMonthlyData`フラグは内部的な重複防止用であり、UIには影響しない

### 4.2 修正案2のリスク分析

#### リスク1: `loadData()`の呼び出しタイミングの変更

**リスク内容**:
- `onMounted`で`fetchCurrentMonthlyData()`を直接呼び出していた箇所が、`loadData()`経由になるため、タイミングが変わる可能性

**リスク評価**: 🟡 **中リスク**

**理由**:
- `loadData()`内でキャッシュチェックが行われ、データがない場合のみAPI呼び出しが発生する
- 初期化時のデータ取得タイミングが変わる可能性がある

**対策**:
- `loadData()`内のキャッシュチェックロジックを確認し、初期化時に適切にデータが取得されることを確認
- 必要に応じて、初期化時のデータ取得ロジックを調整

#### リスク2: 既存のエラーハンドリングの変更

**リスク内容**:
- `fetchCurrentMonthlyData()`を直接呼び出していた箇所が、`loadData()`経由になるため、エラーハンドリングが変わる可能性

**リスク評価**: 🟢 **低リスク**

**理由**:
- `loadData()`内でエラーハンドリングが実装されている
- 既存のエラーハンドリングロジックを維持

**対策**:
- `loadData()`内のエラーハンドリングロジックを確認し、適切にエラーが処理されることを確認

### 4.3 修正案3のリスク分析

#### リスク1: `loadData()`の早期リターンの増加

**リスク内容**:
- `fetchingCurrentMonthlyData`フラグのチェックを追加することで、早期リターンが増える可能性

**リスク評価**: 🟢 **低リスク**

**理由**:
- 早期リターンは重複呼び出しを防止するためのものであり、機能に問題はない
- 既存の`isLoadingTargets`/`isLoadingStats`チェックと同じパターン

**対策**:
- デバッグログを追加し、早期リターンの発生を確認
- 必要に応じて、ログレベルを調整

#### リスク2: UIのローディング状態の表示タイミングの変更

**リスク内容**:
- `fetchingCurrentMonthlyData`フラグのチェックにより、ローディング状態の表示タイミングが変わる可能性

**リスク評価**: 🟢 **低リスク**

**理由**:
- `loadData()`内で`monthlyStore.loading`が管理されており、UIのローディング状態は正しく表示される
- `fetchingCurrentMonthlyData`フラグは内部的な重複防止用であり、UIには影響しない

**対策**:
- UIのローディング状態の表示を確認し、適切に表示されることを確認

---

## 5. 修正案の統合評価

### 5.1 修正案の優先度

| 修正案 | 優先度 | 理由 |
|--------|--------|------|
| **修正案1: `fetchCurrentMonthlyData()`の重複実行防止機能の追加** | **最高** | 重複API呼び出しの根本原因を解消 |
| **修正案2: `MonthlyStatsSection.vue`の初期化処理の最適化** | **高** | 初期化時の重複呼び出しを防止 |
| **修正案3: `loadData()`内のキャッシュチェック強化** | **中** | 追加的な重複呼び出し防止 |

### 5.2 修正案の実施順序

1. **修正案1を最優先で実施**（重複API呼び出しの根本原因を解消）
2. **修正案2を次に実施**（初期化時の重複呼び出しを防止）
3. **修正案3を最後に実施**（追加的な重複呼び出し防止）

### 5.3 総合リスク評価

**リスクレベル**: 🟢 **低リスク**

**理由**:
- 既存のフラグシステムと同じパターンを使用しているため、互換性が高い
- 後方互換性を保持している
- 既存のローディング状態表示ロジックを維持している

---

## 6. パフォーマンス問題への対応（別途対応が必要）

### 6.1 データベースクエリの最適化

**推奨事項**:
- `ProjectStatusHistory`と`InvoiceStatusHistory`テーブルにインデックスを追加
- クエリの結合処理を最適化
- `monthly_summary`テーブルの活用を強化

### 6.2 ステージング環境のリソース確認

**推奨事項**:
- Render.comのリソース制限の確認
- データベース接続数の確認
- CPU/メモリリソースの確認

---

## 7. 結論

### 7.1 修正案の採用推奨

**✅ 修正案1, 2, 3を全て採用することを推奨**

**理由**:
- 大原則に完全適合している
- 重複API呼び出しの根本原因を解消できる
- リスクが低く、後方互換性を保持している

### 7.2 実施後の期待効果

- **重複API呼び出しの削減**: 4回以上 → 1回（75%以上の削減）
- **Finish Timeの改善**: 33.64秒 → 10-15秒程度（50%以上の改善）
- **Load Timeの改善**: 6.60秒 → 2-3秒程度（50%以上の改善）

**注意**: パフォーマンス問題（API呼び出しの遅延）については、データベースクエリの最適化とステージング環境のリソース確認が別途必要です。

---

**作成者**: AI Assistant  
**対象システム**: InfluBerry 月次管理機能  
**関連文書**: `phase3_implementation_plan.md`, `phase2_preparation_analysis.md`

