# Phase 2 実装計画書

## 📋 目次
1. [実装方針](#1-実装方針)
2. [大原則の準拠](#2-大原則の準拠)
3. [実装内容](#3-実装内容)
4. [影響範囲とリスク](#4-影響範囲とリスク)
5. [実装手順](#5-実装手順)
6. [ロールバック手順](#6-ロールバック手順)

---

## 1. 実装方針

### 1.1 Phase 2の目標

| 指標 | Phase 1後 | Phase 2後 | 改善率 |
|------|-----------|-----------|--------|
| **API呼び出し回数** | 2回 | **1回** | **50%削減** |
| **APIレスポンスタイム** | 5-13秒 | **< 500ms** | **95-97%削減** |
| **Load完了時間** | 0.5秒 | **< 1秒** | **目標達成** |

### 1.2 実装方針の概要

**根本解決**: `USE_NEW_API = true`で新API (`/api/monthly/current`) を有効化し、API呼び出し回数を2回→1回に削減

**シンプル構造**: 既存の`fetchCurrentMonthlyData()`を使用し、フラグ切り替えのみで動作変更

**統一・同一化**: 新APIに統一し、旧APIの特殊処理（個別呼び出し、順次実行）を排除

**安全確実**: フォールバック機能により、問題発生時は旧APIに自動切り替え

---

## 2. 大原則の準拠

### 2.1 大原則の適用

| 原則 | Phase 2での適用 | 判定 |
|------|-----------------|------|
| **引き継ぎ書準拠** | 計画書v2.0と引き継ぎ書を100%準拠 | ✅ |
| **根本解決 > 暫定解決** | `USE_NEW_API`フラグで新APIを有効化（根本解決） | ✅ |
| **シンプル構造 > 複雑構造** | 既存の`fetchCurrentMonthlyData()`を使用（シンプル） | ✅ |
| **統一・同一化 > 特殊独自** | 新API統一により旧APIの特殊処理を排除 | ✅ |
| **具体的 > 一般** | 計画書v2.0の具体的な実装方針に従う | ✅ |
| **拙速 < 安全確実** | フラグ切り替えによる段階的移行（安全確実） | ✅ |

### 2.2 引き継ぎ書準拠の詳細

- **引き継ぎ書の要求**: 「実装や修正の基本は引き継ぎ書などを準拠し、方向性は、根本解決>暫定解決、シンプル構造>複雑構造、統一・同一化>特殊独自、具体的>一般、拙速<安全確実」
- **Phase 2での対応**: ✅ すべての原則を100%準拠

### 2.3 計画書v2.0準拠の詳細

- **計画書v2.0の要求**: `/api/monthly/current`エンドポイントを使用し、API呼び出し回数を1回に削減
- **Phase 2での対応**: ✅ `USE_NEW_API = true`で新APIを有効化

---

## 3. 実装内容

### 3.1 Step 2-1: `USE_NEW_API`フラグを`true`に変更

#### 3.1.1 変更内容

**ファイル**: `frontend/src/stores/monthly.js`

**変更箇所**: 19行目

**変更前**:
```javascript
USE_NEW_API: false,
```

**変更後**:
```javascript
USE_NEW_API: true,
```

#### 3.1.2 影響範囲

- **直接影響**: `fetchCurrentMonthlyData()`関数の動作のみ
- **間接影響**: `MonthlyStatsSection.vue`のデータ取得方法（後述）

#### 3.1.3 リスク評価

- **リスク**: **低**
- **理由**: 
  - 既存のフォールバック機能により、新APIが失敗した場合、自動的に旧APIに切り替え
  - フラグ切り替えのみのため、即座にロールバック可能

### 3.2 Step 2-2: `MonthlyStatsSection.vue`の最適化

#### 3.2.1 変更内容

**ファイル**: `frontend/src/components/MonthlyStatsSection.vue`

**変更箇所**: `onMounted`フックと`loadData()`関数

#### 3.2.2 実装方針

**根本解決**: 初期化時に3ヶ月分を一括取得し、タブ切り替え時は既存データから取得

**シンプル構造**: 既存の`getStatsByMonth()`を使用し、変更を最小化

**統一・同一化**: 新API使用時は統一的なデータ取得方法を採用

#### 3.2.3 変更詳細

**変更前（現在の実装）**:
```javascript
onMounted(() => {
  loadData()
})

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
      
      await nextTick()
      stats.value = monthlyStore.getStatsByMonth(props.currentTab + '-01')
    }
  } catch (error) {
    console.error('データ読み込みエラー:', error)
  } finally {
    loading.value = false
    isLoadingTargets.value = false
    isLoadingStats.value = false
  }
}
```

**変更後（新API使用時）**:
```javascript
onMounted(async () => {
  // 新API使用時: 初期化時に3ヶ月分を一括取得
  if (monthlyStore.USE_NEW_API) {
    await monthlyStore.fetchCurrentMonthlyData()
  }
  loadData()
})

const loadData = async () => {
  if (isLoadingTargets.value || isLoadingStats.value) return
  loading.value = true
  
  try {
    if (props.currentTab === 'overview') {
      // overviewタブ: 既存の方法を維持
      const response = await monthlyStore.fetchOverview()
      overviewData.value = response
    } else if (monthlyStore.USE_NEW_API) {
      // 新API使用時: 既存データから取得（3ヶ月分は初期化時に取得済み）
      const monthKey = props.currentTab + '-01'
      stats.value = monthlyStore.getStatsByMonth(monthKey)
      
      // データがない場合のみAPI呼び出し（フォールバック）
      if (!stats.value) {
        await monthlyStore.fetchCurrentMonthlyData()
        stats.value = monthlyStore.getStatsByMonth(monthKey)
      }
    } else {
      // 旧API使用時: 既存の方法を維持
      const [year, month] = props.currentTab.split('-')
      
      isLoadingTargets.value = true
      await monthlyStore.fetchTargets(parseInt(year), [parseInt(month)])
      isLoadingTargets.value = false
      
      isLoadingStats.value = true
      await monthlyStore.fetchStats(parseInt(year), parseInt(month))
      isLoadingStats.value = false
      
      await nextTick()
      stats.value = monthlyStore.getStatsByMonth(props.currentTab + '-01')
    }
  } catch (error) {
    console.error('データ読み込みエラー:', error)
  } finally {
    loading.value = false
    isLoadingTargets.value = false
    isLoadingStats.value = false
  }
}
```

#### 3.2.4 影響範囲

- **直接影響**: `MonthlyStatsSection`コンポーネントのみ
- **間接影響**: `DashboardPage.vue`の初期化タイミング（透過的）

#### 3.2.5 リスク評価

- **リスク**: **低**
- **理由**: 
  - `overview`タブは既存の方法を維持（影響なし）
  - 旧API使用時（`USE_NEW_API = false`）は既存の方法を維持（後方互換性）
  - 新API使用時のみ最適化を適用（段階的移行）

---

## 4. 影響範囲とリスク

### 4.1 他の機能への影響

| 機能 | 影響内容 | 影響度 | 対策 |
|------|----------|--------|------|
| **プロジェクト管理** | ステータス変更時の統計更新 | **なし** | 既存の`update_monthly_summary()`を維持 |
| **請求書管理** | ステータス変更時の統計更新 | **なし** | 既存の`update_monthly_summary()`を維持 |
| **月次自動切り替え** | 月次切り替え時のデータ取得 | **低** | 既存のデータ取得ロジックを維持 |
| **目標設定** | 目標保存時の統計更新 | **なし** | 既存の`saveTarget()`を維持 |
| **UserSettings** | 目標設定UI | **なし** | 既存の`getTargetByMonth()`を維持 |

### 4.2 UIへの影響

| UIコンポーネント | 影響内容 | 影響度 | 対策 |
|----------------|----------|--------|------|
| **MonthlyTabs** | タブ表示ロジック | **なし** | データ取得方法の変更のみ |
| **MonthlyStatsSection** | 統計表示ロジック | **低** | データ取得方法の変更のみ |
| **ProgressBar** | プログレスバー表示 | **なし** | データ形式の変更なし |
| **DashboardPage** | ダッシュボード表示 | **なし** | データ取得方法の変更のみ |

### 4.3 APIへの影響

| APIエンドポイント | 影響内容 | 影響度 | 対策 |
|------------------|----------|--------|------|
| `/api/monthly/current` | 新API使用による負荷増加 | **低** | 事前集計テーブルにより高速化 |
| `/api/monthly-targets/` | 旧API使用頻度の減少 | **低** | フォールバック用に保持 |
| `/api/monthly-stats/{year}/{month}` | 旧API使用頻度の減少 | **低** | フォールバック用に保持 |

### 4.4 データベースへの影響

| テーブル | 影響内容 | 影響度 | 対策 |
|---------|----------|--------|------|
| `monthly_summary` | 新API使用によるアクセス増加 | **低** | インデックスにより高速化 |
| `monthly_targets` | 新API使用によるアクセス増加 | **低** | インデックスにより高速化 |
| `project_status_history` | フォールバック時のアクセス | **低** | 既存のインデックス維持 |
| `invoice_status_history` | フォールバック時のアクセス | **低** | 既存のインデックス維持 |

### 4.5 リスク対策

#### 4.5.1 フォールバック機能
- **実装状況**: ✅ 実装済み
- **動作**: 新APIが失敗した場合、自動的に旧APIに切り替え
- **コード**:
  ```javascript
  try {
    // 新API呼び出し
    const res = await axios.get('/api/monthly/current')
  } catch (err) {
    // フォールバック: 旧APIを使用
    await this._fetchCurrentMonthlyDataLegacy()
  }
  ```

#### 4.5.2 段階的移行
- **実装状況**: ✅ 実装済み
- **動作**: `USE_NEW_API`フラグで新API/旧APIを切り替え可能
- **利点**: 問題発生時、即座にロールバック可能

#### 4.5.3 後方互換性
- **実装状況**: ✅ 実装済み
- **動作**: `USE_NEW_API = false`の場合、既存の方法を維持
- **利点**: 旧API使用時の動作を保証

---

## 5. 実装手順

### 5.1 実装前の準備

#### Step 1: バックアップ作成
- **目的**: 問題発生時のロールバック準備
- **対象ファイル**:
  - `frontend/src/stores/monthly.js`
  - `frontend/src/components/MonthlyStatsSection.vue`
- **バックアップ名**:
  - `frontend/src/stores/monthly.js.backup_before_phase2_YYYYMMDD_HHMMSS`
  - `frontend/src/components/MonthlyStatsSection.vue.backup_before_phase2_YYYYMMDD_HHMMSS`

#### Step 2: 現状確認
- **目的**: Phase 2実装前の状態確認
- **確認項目**:
  - API呼び出し回数（2回）
  - APIレスポンスタイム（5-13秒）
  - ページ読み込み時間（0.5秒）

### 5.2 実装手順

#### Step 2-1: `USE_NEW_API`フラグを`true`に変更
- **ファイル**: `frontend/src/stores/monthly.js`
- **変更内容**:
  ```javascript
  // 変更前
  USE_NEW_API: false,
  
  // 変更後
  USE_NEW_API: true,
  ```
- **確認項目**:
  - [ ] バックアップファイル作成済み
  - [ ] `USE_NEW_API`フラグが`true`に変更されている
  - [ ] 構文エラーがない

#### Step 2-2: `MonthlyStatsSection.vue`の最適化
- **ファイル**: `frontend/src/components/MonthlyStatsSection.vue`
- **変更内容**: 
  - `onMounted`フック: 初期化時に`fetchCurrentMonthlyData()`を呼び出し（新API使用時）
  - `loadData()`関数: 新API使用時は既存データから取得、旧API使用時は既存の方法を維持
- **確認項目**:
  - [ ] バックアップファイル作成済み
  - [ ] `onMounted`で`fetchCurrentMonthlyData()`が呼び出されている（新API使用時）
  - [ ] `loadData()`で新API使用時は既存データから取得している
  - [ ] `overview`タブは既存の`fetchOverview()`を維持している
  - [ ] 旧API使用時（`USE_NEW_API = false`）は既存の方法を維持している
  - [ ] 構文エラーがない

#### Step 2-3: 動作確認
- **目的**: Phase 2実装後の動作確認
- **確認項目**:
  - [ ] API呼び出し回数が1回になっている
  - [ ] APIレスポンスタイムが500ms以内
  - [ ] ページ読み込み時間が1秒以内
  - [ ] データが正しく表示されている
  - [ ] エラーが発生していない

### 5.3 実装後の検証

#### Step 3-1: パフォーマンス測定
- **目的**: Phase 2後のパフォーマンス改善を確認
- **測定項目**:
  - API呼び出し回数
  - APIレスポンスタイム
  - ページ読み込み時間
- **測定方法**: ブラウザのDevToolsを使用

#### Step 3-2: 機能確認
- **目的**: Phase 2後の機能動作を確認
- **確認項目**:
  - [ ] 月次データが正しく表示される
  - [ ] タブ切り替えが正常に動作する
  - [ ] プログレスバーが正しく表示される
  - [ ] 目標設定が正常に動作する
  - [ ] `overview`タブが正常に動作する

#### Step 3-3: エラーハンドリング確認
- **目的**: Phase 2後のエラーハンドリングを確認
- **確認項目**:
  - [ ] 新APIがエラーを返した場合、旧APIにフォールバックする
  - [ ] エラーメッセージが正しく表示される

---

## 6. ロールバック手順

### 6.1 ロールバック条件

以下の場合、即座にロールバックを実行:
- 新APIがエラーを返す（フォールバック機能が動作しない場合）
- パフォーマンスが悪化した場合
- データが正しく表示されない場合
- ユーザー体験が悪化した場合

### 6.2 ロールバック手順

#### Step 1: `USE_NEW_API`フラグを`false`に戻す
- **ファイル**: `frontend/src/stores/monthly.js`
- **変更内容**:
  ```javascript
  // ロールバック後
  USE_NEW_API: false,
  ```

#### Step 2: `MonthlyStatsSection.vue`の変更を元に戻す（必要に応じて）
- **ファイル**: `frontend/src/components/MonthlyStatsSection.vue`
- **変更内容**: バックアップファイルから復元

#### Step 3: 動作確認
- **目的**: ロールバック後の動作確認
- **確認項目**:
  - [ ] 旧APIが正常に動作している
  - [ ] データが正しく表示されている

---

## 7. まとめ

### 7.1 Phase 2実行準備の完了状況

| 項目 | 状況 |
|------|------|
| **大原則の準拠確認** | ✅ 完了 |
| **引き継ぎ書・計画書の準拠確認** | ✅ 完了 |
| **Phase 2実装計画** | ✅ 完了 |
| **影響範囲分析** | ✅ 完了 |
| **リスク分析** | ✅ 完了 |
| **競合・干渉リスク分析** | ✅ 完了 |
| **実装手順** | ✅ 完了 |
| **ロールバック手順** | ✅ 完了 |

### 7.2 Phase 2実行の準備完了

- ✅ **大原則準拠**: 根本解決、シンプル構造、統一・同一化、具体的、安全確実
- ✅ **引き継ぎ書準拠**: 計画書v2.0と引き継ぎ書を100%準拠
- ✅ **影響範囲明確化**: 直接影響範囲と間接影響範囲を特定
- ✅ **リスク対策**: フォールバック機能と段階的移行によるリスク軽減
- ✅ **競合・干渉リスク**: 他の機能やUIへの影響を最小限に抑制

### 7.3 次のステップ

Phase 2実行準備が完了しました。実装指示を待機中です。

---

**重要**: 実装指示があるまで、**絶対に修正しないでください**。


