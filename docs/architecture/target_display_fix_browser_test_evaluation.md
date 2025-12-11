# 目標設定表示修正: ブラウザテスト評価レポート

**作成日**: 2025年11月1日  
**テスト環境**: ローカル環境（修正案3実装後）  
**テスト内容**: 目標設定表示修正後のブラウザテスト  
**目的**: 修正の効果を評価し、残存問題を特定

---

## 1. 問題の継続状況

### 1.1 問題の詳細

**ユーザー報告**:
> 目標設定表示がゼロのままで、表示が変わらない問題が継続

**コンソールログの分析**:
```
MonthlyStatsSection.vue:296 [Vue warn]: Component provided template option but runtime compilation is not supported in this build of Vue.
  at <ProgressBar label="獲得案件" current=0 target=0  ... >
  at <ProgressBar label="完了案件" current=0 target=0  ... >
  at <ProgressBar label="請求額" current=0 target=0  ... >
```

**問題の特徴**:
- `ProgressBar`コンポーネントで`target=0`が表示されている
- 修正案3を実装したが、問題が継続している

---

## 2. コンソールログの詳細分析

### 2.1 データ取得のフロー

**ログの時系列**:

1. **初期化**:
   ```
   MonthlyStatsSection.vue:178 🔧 データ未取得のため、fetchCurrentMonthlyData()を呼び出し
   monthly.js:24 🔧 新API使用: GET /api/monthly/current
   ```

2. **目標取得の開始**:
   ```
   monthly.js:24 🔧 月次目標取得開始: {year: 2025, months: Array(1)}
   ```

3. **目標取得のスキップ**:
   ```
   monthly.js:24 🔧 月次目標取得: 既に実行中のためスキップ
   ```

4. **データ取得完了**:
   ```
   monthly.js:24 ✅ 月次データ取得完了（新API）
   MonthlyStatsSection.vue:178 月次統計データ（新API）: {tab: '2025-11', monthKey: '2025-11-01', stats: Proxy(Object), targets: Proxy(Object)}
   ```

5. **目標取得完了（後で完了）**:
   ```
   monthly.js:24 🔧 月次目標取得完了: {targets: Proxy(Object), cached: true}
   ```

### 2.2 問題の根本原因の推測

#### 問題1: 目標取得のタイミングの問題

**分析**:
- `fetchCurrentMonthlyData()`で目標が`null`の場合、非同期で`/api/monthly-targets/`から取得する
- しかし、目標取得が完了する前に`getStatsByMonth()`が呼び出される
- `getStatsByMonth()`で`targets`ストアから取得を試みるが、まだ目標が設定されていない
- 結果として、`target.projects = 0`、`target.income = 0`が設定される

**証拠**:
```
monthly.js:24 🔧 月次目標取得: 既に実行中のためスキップ
```
- 目標取得がスキップされている可能性

**問題の詳細**:
- `fetchCurrentMonthlyData()`内で非同期で`fetchTargets()`を呼び出すが、`await`していない
- そのため、目標取得が完了する前に`getStatsByMonth()`が呼び出される
- `getStatsByMonth()`で`targets[monthKey]`が存在しない場合、`target.projects = 0`、`target.income = 0`が設定される

#### 問題2: `getStatsByMonth()`のロジックの問題

**分析**:
- `getStatsByMonth()`で目標が`null`の場合、`targets`ストアから取得して補完する
- しかし、`targets`ストアに目標が存在しない場合、`target.projects = 0`、`target.income = 0`が設定される
- 目標が後で取得された場合でも、`stats`オブジェクトが既に作成されているため、更新されない

**証拠**:
- `getStatsByMonth()`はgetterであるため、呼び出されるたびに計算される
- しかし、`stats.value`に既に`stats`オブジェクトが設定されている場合、`getStatsByMonth()`の結果が反映されない可能性

#### 問題3: リアクティビティの問題

**分析**:
- `stats.value`に`stats`オブジェクトを設定している
- 後で`targets`ストアが更新されても、`stats.value`は更新されない
- `getStatsByMonth()`はgetterであるため、呼び出されるたびに計算されるが、`stats.value`に設定されたオブジェクトは更新されない

**証拠**:
- ログを見ると、目標取得が完了している（`monthly.js:24 🔧 月次目標取得完了`）
- しかし、`ProgressBar`で`target=0`が表示されている

---

## 3. API呼び出しの分析

### 3.1 API呼び出しのレスポンスタイム

| APIエンドポイント | レスポンスタイム | 評価 |
|------------------|----------------|------|
| `/api/monthly-stats/overview` | **130ms** | ✅ **正常（目標500ms未満）** |
| `/api/monthly/current` | **26ms** | ✅ **正常（目標500ms未満）** |
| `/api/monthly-targets/?year=2025&months=10` | **5ms** | ✅ **正常（目標500ms未満）** |

### 3.2 改善状況の分析

#### ✅ API呼び出しは正常

- `/api/monthly/current`: 26ms（正常）
- `/api/monthly-targets/`: 5ms（正常）
- API呼び出し自体は成功している

---

## 4. パフォーマンス指標の分析

### 4.1 パフォーマンス指標

| 指標 | 目標値 | 現在の値 | 評価 |
|------|--------|---------|------|
| **Finish Time** | < 2秒 | **1.17秒** | ✅ **目標達成** |
| **DOMContentLoaded** | < 800ms | **325ms** | ✅ **目標達成** |
| **Load Time** | < 800ms | **1.06秒** | ⚠️ **目標未達成（+260ms超過）** |

**評価**: ✅ **Finish TimeとDOMContentLoadedは目標達成、Load Timeは目標未達成だが大幅改善**

---

## 5. 問題の根本原因の詳細分析

### 5.1 修正案3の実装の問題点

#### 問題1: 非同期処理のタイミング

**修正案3の実装**:
```javascript
// fetchCurrentMonthlyData()内で
if ((targetProjects === null || targetProjects === undefined) || (targetIncome === null || targetIncome === undefined)) {
  // 非同期で目標を取得（表示をブロックしない）
  this.fetchTargets(parseInt(year), [parseInt(month.replace('-01', ''))]).then(() => {
    // 目標取得後に、statsを更新
    if (this.stats[monthKey]) {
      const target = this.targets[monthKey]
      if (target) {
        this.stats[monthKey].target.projects = target.target_projects ?? 0
        this.stats[monthKey].target.income = target.target_income ?? 0
      }
    }
  })
}
```

**問題点**:
1. **非同期処理が完了する前に`getStatsByMonth()`が呼び出される**
   - `fetchCurrentMonthlyData()`が完了した後、`MonthlyStatsSection.vue`で`getStatsByMonth()`が呼び出される
   - この時点では、目標取得がまだ完了していない可能性がある
   - `getStatsByMonth()`で`targets[monthKey]`が存在しない場合、`target.projects = 0`、`target.income = 0`が設定される

2. **`stats`オブジェクトが更新されても、`stats.value`が更新されない**
   - `fetchTargets()`の`.then()`内で`this.stats[monthKey].target`を更新している
   - しかし、`MonthlyStatsSection.vue`の`stats.value`は既に設定されている
   - `stats.value`は`getStatsByMonth()`の結果を参照しているが、`stats.value`が更新されない

3. **リアクティビティの問題**
   - `stats.value`に`stats`オブジェクトを設定している
   - `this.stats[monthKey]`を直接更新しても、Vueのリアクティビティが検知しない可能性がある

#### 問題2: `getStatsByMonth()`のロジック

**修正案3の実装**:
```javascript
getStatsByMonth: (state) => (month) => {
  const stats = state.stats[month] || null
  if (!stats) return null
  
  // targetがnullまたはundefinedの場合、targetsストアから取得して補完
  if (!stats.target || 
      (stats.target.projects === null || stats.target.projects === undefined) ||
      (stats.target.income === null || stats.target.income === undefined)) {
    const target = state.targets[month]
    if (target) {
      stats.target = {
        projects: target.target_projects ?? 0,
        income: target.target_income ?? 0
      }
    } else if (!stats.target) {
      stats.target = {
        projects: 0,
        income: 0
      }
    } else {
      // stats.targetが存在するが、nullのプロパティがある場合は補完
      if (stats.target.projects === null || stats.target.projects === undefined) {
        stats.target.projects = 0
      }
      if (stats.target.income === null || stats.target.income === undefined) {
        stats.target.income = 0
      }
    }
  }
  
  return stats
}
```

**問題点**:
1. **`targets[monthKey]`が存在しない場合、`target.projects = 0`、`target.income = 0`が設定される**
   - 目標が後で取得された場合でも、`stats.target`が既に`{projects: 0, income: 0}`に設定されている
   - `getStatsByMonth()`はgetterであるため、呼び出されるたびに計算されるが、`stats.value`に設定されたオブジェクトは更新されない

2. **Piniaのgetterは、毎回新しいオブジェクトを返す可能性がある**
   - `getStatsByMonth()`で`stats.target`を直接変更している
   - これはPiniaの状態を直接変更することになり、リアクティビティの問題が発生する可能性がある

#### 問題3: `loadData()`のキャッシュチェック

**修正案3の実装**:
```javascript
// キャッシュがあるが目標値がない場合も即座に表示（目標値は非同期で補完される）
if (cachedStats) {
  stats.value = cachedStats
  // 目標値がnullの場合は、非同期で取得を試みる（表示をブロックしない）
  const [year, month] = props.currentTab.split('-')
  monthlyStore.fetchTargets(parseInt(year), [parseInt(month)]).then(() => {
    // 目標取得後に、statsを更新
    const updatedStats = monthlyStore.getStatsByMonth(monthKey)
    if (updatedStats) {
      stats.value = updatedStats
    }
  })
  return // loadingをtrueにしない
}
```

**問題点**:
1. **`fetchTargets()`が完了する前に、`cachedStats`が表示される**
   - `cachedStats`には`target.projects = 0`、`target.income = 0`が設定されている
   - 目標取得が完了する前に表示されるため、`target=0`が表示される

2. **`fetchTargets()`の`.then()`で`stats.value`を更新しているが、タイミングの問題**
   - `fetchTargets()`が完了した時点で、`getStatsByMonth()`が正しい値を返すかどうかは不明
   - `getStatsByMonth()`のロジックに問題がある場合、正しい値が返されない可能性がある

---

## 6. 結論

### 6.1 修正案3の効果

#### ❌ 目標設定表示の問題は解決されていない

**理由**:
1. **非同期処理のタイミングの問題**
   - 目標取得が完了する前に`getStatsByMonth()`が呼び出される
   - `targets[monthKey]`が存在しない場合、`target.projects = 0`、`target.income = 0`が設定される

2. **リアクティビティの問題**
   - `stats.value`に`stats`オブジェクトを設定している
   - 後で`targets`ストアが更新されても、`stats.value`は更新されない

3. **`getStatsByMonth()`のロジックの問題**
   - `targets[monthKey]`が存在しない場合、`target.projects = 0`、`target.income = 0`が設定される
   - 目標が後で取得された場合でも、`stats.target`が既に`{projects: 0, income: 0}`に設定されている

### 6.2 パフォーマンスの改善

#### ✅ パフォーマンスは改善されている

- **Finish Time**: 1.17秒（目標達成）
- **DOMContentLoaded**: 325ms（目標達成）
- **Load Time**: 1.06秒（目標未達成だが大幅改善）

### 6.3 残存問題

#### 🔴 目標設定表示の問題（最高優先度）

**問題内容**:
- 目標設定表示がゼロのままで、表示が変わらない

**根本原因**:
1. 非同期処理のタイミングの問題
2. リアクティビティの問題
3. `getStatsByMonth()`のロジックの問題

**影響度**: 🔴 **極めて高い（計画書の核心機能が動作しない、ユーザー満足度への致命的影響）**
**優先度**: **最高（緊急対応が必要・計画書の核心目的を完全に阻害）**

---

## 7. 推奨される次のステップ

### 7.1 即座に実施すべき事項

#### 🔴 目標設定表示の問題の再修正（最高優先度）

1. **修正方針の再検討**
   - 非同期処理のタイミングを修正
   - リアクティビティの問題を解決
   - `getStatsByMonth()`のロジックを見直す

2. **修正案の検討**
   - 目標取得を同期処理にする（表示をブロックする）
   - または、目標取得が完了するまで待つ
   - `stats.value`の更新タイミングを修正

### 7.2 調査項目

1. **APIレスポンスのデータ構造確認**
   - `/api/monthly/current`のレスポンスで目標が`null`になっている理由を確認
   - `/api/monthly-targets/`のレスポンスで目標が正しく返されているか確認

2. **データフローの確認**
   - `fetchCurrentMonthlyData()` → `getStatsByMonth()` → `stats.value`のデータフローを確認
   - 目標取得のタイミングを確認

3. **リアクティビティの確認**
   - Piniaの状態更新がVueのリアクティビティに反映されるか確認
   - `stats.value`の更新タイミングを確認

---

**作成者**: AI Assistant  
**関連文書**: 
- `target_display_fix_consistency_check.md`
- `monthly_tab_and_target_display_improvement_plan.md`
- `phase3_implementation_plan.md`

