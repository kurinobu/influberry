# Phase 3 残存問題の完全調査分析レポート

## 📋 目次
1. [パフォーマンス目標の確認](#1-パフォーマンス目標の確認)
2. [問題1: TypeError の原因分析](#2-問題1-typeerror-の原因分析)
3. [問題2: stats: null問題の原因分析](#3-問題2-stats-null問題の原因分析)
4. [データ構造の不一致分析](#4-データ構造の不一致分析)
5. [根本原因の特定](#5-根本原因の特定)
6. [結論](#6-結論)

---

## 1. パフォーマンス目標の確認

### 1.1 計画書v2.0の要求事項

| 要求事項 | 記載内容 | 評価 |
|---------|---------|------|
| **パフォーマンス** | 本番環境で月次セクション表示が**1秒以内**（ページ読み込み開始から表示完了まで） | ✅ **正しい目標** |

### 1.2 計画書v2.1 Phase 3の要求事項

| 要求事項 | 記載内容 | 評価 |
|---------|---------|------|
| **APIレスポンスタイム** | **< 200ms** | ✅ **正しい目標** |
| **Load完了時間** | **< 800ms** | ✅ **正しい目標** |

### 1.3 評価レポートの誤り

| 誤った記述 | 正しい目標 | 評価 |
|-----------|----------|------|
| **Finish Time < 2.0s** | ❌ **誤り** - 目標は**1秒以内** | **誤り** |
| **Load Time < 2.0s** | ❌ **誤り** - Phase 3の目標は**< 800ms** | **誤り** |

**結論**: 「< 2.0s」という記述は完全に間違っていました。正しくは:
- **表示速度**: **1秒以内**（ページ読み込み開始から表示完了まで）
- **APIレスポンスタイム**: **< 200ms**
- **Load完了時間**: **< 800ms**（Phase 3の目標）

---

## 2. 問題1: TypeError の原因分析

### 2.1 エラーの詳細

```
MonthlyStatsSection.vue:63 Uncaught (in promise) TypeError: Cannot read properties of undefined (reading 'projects')
    at Proxy._sfc_render (MonthlyStatsSection.vue:63:33)
```

### 2.2 エラー発生箇所の確認

#### テンプレート内の記述
```vue
:target="stats?.target.projects || 0"
```

#### 問題の分析

**Optional chainingの使用**:
- `stats?.target.projects`という記述は、`stats`が`null`または`undefined`の場合は`undefined`を返すはず
- しかし、エラーメッセージは「Cannot read properties of undefined (reading 'projects')」
- これは、`stats?.target`が`undefined`の場合、`stats?.target.projects`が`undefined`を返すはずだが、エラーが発生している

**重要**: Optional chainingは最初のプロパティ（`stats`）のみに適用されている
- `stats?.target.projects`は`stats`が`null`または`undefined`の場合は`undefined`を返す
- しかし、`stats`が存在し、`stats.target`が`undefined`の場合、`stats?.target.projects`は`undefined.projects`となり、エラーが発生する

**正しい記述**:
- `stats?.target?.projects`とすべき（`target`にもOptional chainingを適用）

### 2.3 データ構造の確認

#### `fetchCurrentMonthlyData()`で設定される`stats`オブジェクト
```javascript
this.stats[monthKey] = {
  month: monthKey,
  actual: {
    acquired_projects: s.acquired_projects ?? 0,
    completed_projects: s.completed_projects ?? 0,
    sent_invoices_count: s.sent_invoices_count ?? 0,
    sent_invoices_amount: s.sent_invoices_amount ?? 0,
    paid_invoices_count: s.paid_invoices_count ?? 0,
    paid_invoices_amount: s.paid_invoices_amount ?? 0
  }
}
```

**問題**: `target`プロパティが含まれていない！

#### `/api/monthly/current`のレスポンス構造
```python
result['data'][month_key] = {
    'target': {
        'projects': target.target_projects if target else None,
        'income': target.target_income if target else None
    },
    'stats': stats,
    'achievement': { ... }
}
```

#### `fetchCurrentMonthlyData()`でのデータ設定
```javascript
Object.entries(data).forEach(([monthKey, payload]) => {
  const t = payload.target || {}
  const s = payload.stats || {}
  // 目標: 既存のフィールド名に合わせて保持
  this.targets[monthKey] = {
    target_month: monthKey,
    target_projects: t.projects ?? null,
    target_income: t.income ?? null
  }
  // 統計: そのまま保持（既存取得と併存可能）
  this.stats[monthKey] = {
    month: monthKey,
    actual: { ... }
  }
})
```

**問題**: `stats`オブジェクトに`target`プロパティが設定されていない！

#### 既存の`fetchStats()`で設定される`stats`オブジェクト（旧API）
`/api/monthly-stats/{year}/{month}`のレスポンス構造を確認する必要がある。

### 2.4 根本原因の特定

#### 原因1: `stats`オブジェクトの構造の不一致

**`fetchCurrentMonthlyData()`で設定される`stats`オブジェクト**:
```javascript
{
  month: '2025-10-01',
  actual: { ... }
  // targetプロパティがない！
}
```

**テンプレートでのアクセス**:
```vue
:target="stats?.target.projects || 0"
```

**問題**:
- `stats`が存在するが、`stats.target`が`undefined`の場合、`stats?.target.projects`は`undefined.projects`となり、エラーが発生する
- Optional chainingは`stats`のみに適用されているため、`stats.target`が`undefined`の場合、エラーが発生する

#### 原因2: Optional chainingの不完全な使用

**現在の記述**:
```vue
:target="stats?.target.projects || 0"
```

**正しい記述**:
```vue
:target="stats?.target?.projects || 0"
```

---

## 3. 問題2: stats: null問題の原因分析

### 3.1 問題の詳細

```
MonthlyStatsSection.vue:294 🔧 fetchCurrentMonthlyData()後のgetStatsByMonth呼び出し結果: 
{monthKey: '2025-10-01', stats: null, allStatsKeys: Array(2), hasStats: false}

MonthlyStatsSection.vue:303 月次統計データ（新API）: 
{tab: '2025-10', monthKey: '2025-10-01', stats: null, targets: Proxy(Object), allStatsKeys: Array(2)}
```

### 3.2 発生タイミング

1. `fetchCurrentMonthlyData()`が完了
2. `nextTick()`を実行
3. `getStatsByMonth('2025-10-01')`を呼び出し
4. 結果が`null`になる

### 3.3 ログからの分析

#### `fetchCurrentMonthlyData()`での設定
```
monthly.js:144 🔧 fetchCurrentMonthlyData: stats設定完了 {monthKey: '2025-10-01', hasStats: true, statsKeys: Array(3), statsData: Proxy(Object)}
```
→ `fetchCurrentMonthlyData()`では`statsKeys: Array(3)`で、`'2025-10-01'`が含まれている

#### `getStatsByMonth()`での取得
```
MonthlyStatsSection.vue:294 🔧 fetchCurrentMonthlyData()後のgetStatsByMonth呼び出し結果: 
{monthKey: '2025-10-01', stats: null, allStatsKeys: Array(2), hasStats: false}
```
→ `getStatsByMonth()`時点では`allStatsKeys: Array(2)`で、`'2025-10-01'`が含まれていない

**重要**: `fetchCurrentMonthlyData()`では`statsKeys: Array(3)`だが、`getStatsByMonth()`時点では`allStatsKeys: Array(2)`となっている。

### 3.4 原因分析

#### 仮説1: データ上書きの問題

**`watch`による`fetchStats()`再実行**:
- `fetchCurrentMonthlyData()`完了後に、`watch`がトリガーされて`fetchStats()`が再実行される可能性
- `fetchStats()`が`fetchCurrentMonthlyData()`で設定したstatsを上書きする可能性

**ログからの確認**:
```
MonthlyStatsSection.vue:377 ⚠️ watch: fetchCurrentMonthlyData実行中のため、統計再取得をスキップ
monthly.js:270 ⚠️ fetchStats: fetchCurrentMonthlyData実行中のため、実行をスキップ
```
→ `watch`と`fetchStats()`の実行抑制は動作している

しかし、その後:
```
MonthlyStatsSection.vue:387 目標データ（当該月）変更検知 - 統計を強制再取得
monthly.js:302 🔧 月次統計取得: 強制再取得のためキャッシュをクリア {monthKey: '2025-10-01'}
monthly.js:310 🔧 月次統計取得開始: {year: 2025, month: 10}
monthly.js:166 ✅ fetchCurrentMonthlyData: フラグ解除完了（遅延解除により競合状態を防止）
monthly.js:338 🔧 月次統計取得完了: {monthKey: '2025-10-01', stats: Proxy(Object), cached: true, fetchingCurrentMonthlyData: false}
```
→ `fetchCurrentMonthlyData()`完了後、`watch`がトリガーされて`fetchStats()`が再実行されている
→ `fetchStats()`が`fetchCurrentMonthlyData()`で設定したstatsを上書きする可能性

#### 仮説2: キーの不一致

**`fetchCurrentMonthlyData()`での設定**:
```javascript
const monthKey = `${year}-${String(month).padStart(2, '0')}-01`
this.stats[monthKey] = { ... }
```

**`getStatsByMonth()`での取得**:
```javascript
const monthKey = props.currentTab + '-01'
stats.value = monthlyStore.getStatsByMonth(monthKey)
```

**問題**: `monthKey`の形式が一致していない可能性
- `fetchCurrentMonthlyData()`: `'2025-10-01'`
- `getStatsByMonth()`: `props.currentTab + '-01'` → `'2025-10' + '-01'` → `'2025-10-01'`

これは一致しているはずだが、実際には`null`が返されている。

#### 仮説3: データ削除の問題

**`fetchStats()`でのキャッシュクリア**:
```javascript
if (forceRefresh) {
  delete this.stats[monthKey]
  this.lastFetchTime.stats = null
  console.log('🔧 月次統計取得: 強制再取得のためキャッシュをクリア', { monthKey })
}
```

**問題**: `fetchStats()`が`forceRefresh = true`で呼び出された場合、`this.stats[monthKey]`を削除する
- その後、`fetchStats()`が完了するまで、`stats[monthKey]`は存在しない
- この間に`getStatsByMonth()`が呼び出されると、`null`が返される

---

## 4. データ構造の不一致分析

### 4.1 `fetchCurrentMonthlyData()`で設定される`stats`オブジェクト

```javascript
this.stats[monthKey] = {
  month: monthKey,
  actual: {
    acquired_projects: s.acquired_projects ?? 0,
    completed_projects: s.completed_projects ?? 0,
    sent_invoices_count: s.sent_invoices_count ?? 0,
    sent_invoices_amount: s.sent_invoices_amount ?? 0,
    paid_invoices_count: s.paid_invoices_count ?? 0,
    paid_invoices_amount: s.paid_invoices_amount ?? 0
  }
  // targetプロパティがない！
}
```

### 4.2 `fetchStats()`で設定される`stats`オブジェクト（旧API）

`/api/monthly-stats/{year}/{month}`のレスポンス構造を確認する必要があるが、おそらく:
```javascript
{
  month: '2025-10-01',
  actual: { ... },
  target: {
    projects: ...,
    income: ...
  }
}
```

### 4.3 データ構造の不一致

| データソース | `target`プロパティ | 評価 |
|------------|------------------|------|
| `fetchCurrentMonthlyData()` | ❌ **含まれていない** | **問題** |
| `fetchStats()`（旧API） | ✅ **含まれている** | **正常** |

**結論**: `fetchCurrentMonthlyData()`で設定される`stats`オブジェクトに`target`プロパティが含まれていないため、テンプレート内で`stats?.target.projects`にアクセスしようとするとエラーが発生する。

---

## 5. 根本原因の特定

### 5.1 問題1: TypeError の根本原因

#### 原因1: Optional chainingの不完全な使用
- **現在**: `stats?.target.projects`
- **問題**: `stats.target`が`undefined`の場合、`stats?.target.projects`は`undefined.projects`となり、エラーが発生する
- **修正**: `stats?.target?.projects`とすべき

#### 原因2: データ構造の不一致
- **原因**: `fetchCurrentMonthlyData()`で設定される`stats`オブジェクトに`target`プロパティが含まれていない
- **影響**: テンプレート内で`stats?.target.projects`にアクセスしようとするとエラーが発生する
- **修正**: `fetchCurrentMonthlyData()`で`stats`オブジェクトに`target`プロパティを追加する

### 5.2 問題2: stats: null問題の根本原因

#### 原因1: データ上書きの問題
- **原因**: `fetchCurrentMonthlyData()`完了後、`watch`がトリガーされて`fetchStats()`が再実行され、statsを上書きする可能性
- **現在の対策**: `watch`と`fetchStats()`の実行抑制は動作しているが、`fetchCurrentMonthlyData()`完了後の`watch`トリガーは防止できていない
- **修正**: `fetchCurrentMonthlyData()`完了後、より長い待機時間を設定するか、`watch`の実行を完全に抑制する

#### 原因2: データ削除の問題
- **原因**: `fetchStats()`が`forceRefresh = true`で呼び出された場合、`this.stats[monthKey]`を削除する
- **影響**: `fetchStats()`が完了するまで、`stats[monthKey]`は存在しないため、`getStatsByMonth()`が`null`を返す
- **修正**: `fetchStats()`でのキャッシュクリアタイミングを調整する

#### 原因3: キーの不一致
- **原因**: `monthKey`の形式が一致していない可能性（ただし、現在の実装では一致しているはず）
- **修正**: `monthKey`の形式を確認し、統一する

---

## 6. 結論

### 6.1 パフォーマンス目標の誤り

**誤った記述**: 「目標（本番/ステージング）：< 2.0s」
**正しい目標**:
- **表示速度**: **1秒以内**（ページ読み込み開始から表示完了まで）
- **APIレスポンスタイム**: **< 200ms**
- **Load完了時間**: **< 800ms**（Phase 3の目標）

### 6.2 問題1: TypeError の根本原因

1. **Optional chainingの不完全な使用**: `stats?.target.projects` → `stats?.target?.projects`とすべき
2. **データ構造の不一致**: `fetchCurrentMonthlyData()`で設定される`stats`オブジェクトに`target`プロパティが含まれていない

### 6.3 問題2: stats: null問題の根本原因

1. **データ上書きの問題**: `fetchCurrentMonthlyData()`完了後、`watch`がトリガーされて`fetchStats()`が再実行され、statsを上書きする可能性
2. **データ削除の問題**: `fetchStats()`が`forceRefresh = true`で呼び出された場合、`this.stats[monthKey]`を削除するため、`getStatsByMonth()`が`null`を返す
3. **キーの不一致**: 可能性は低いが、`monthKey`の形式が一致していない可能性

### 6.4 修正方針

#### 優先度: 最高
1. **テンプレート内のOptional chainingの修正**: `stats?.target.projects` → `stats?.target?.projects`
2. **データ構造の統一**: `fetchCurrentMonthlyData()`で`stats`オブジェクトに`target`プロパティを追加する

#### 優先度: 高
3. **データ上書きの防止**: `fetchCurrentMonthlyData()`完了後の`watch`トリガーを完全に抑制する
4. **データ削除タイミングの調整**: `fetchStats()`でのキャッシュクリアタイミングを調整する

---

**作成日時**: 2025年10月31日
**調査者**: AI Assistant
**調査対象**: Phase 3 残存問題の完全調査分析

**結論**: 
1. **パフォーマンス目標の誤り**: 「< 2.0s」という記述は完全に間違っていました。正しくは「1秒以内」「< 200ms」「< 800ms」です。
2. **TypeError の根本原因**: Optional chainingの不完全な使用と、データ構造の不一致（`target`プロパティが含まれていない）。
3. **stats: null問題の根本原因**: データ上書きの問題と、データ削除の問題。


