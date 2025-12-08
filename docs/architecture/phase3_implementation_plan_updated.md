# フェーズ3 実装計画書（更新版）

## 📋 目次
1. [現在地点の完全把握](#1-現在地点の完全把握)
2. [フェーズ3の目標と目的（更新）](#2-フェーズ3の目標と目的更新)
3. [完全な問題分析](#3-完全な問題分析)
4. [実装計画（更新）](#4-実装計画更新)
5. [完全な競合・干渉リスク分析](#5-完全な競合干渉リスク分析)
6. [実装手順（詳細版）](#6-実装手順詳細版)

---

## 1. 現在地点の完全把握

### 1.1 実装済み項目（確認済み）

#### ✅ **Phase 1-6: 完了済み**
- データベース基盤構築（`monthly_targets`, `project_status_history`, `invoice_status_history`）
- バックエンドAPI実装（`/api/monthly-targets`, `/api/monthly-stats/{year}/{month}`, `/api/monthly-stats/overview`）
- フロントエンド実装（`MonthlyTabs.vue`, `MonthlyStatsSection.vue`, `ProgressBar.vue`）
- ステータス変更履歴記録機能
- 月次統計集計ロジック（正負集計）
- 動的タブ表示機能

#### ✅ **Phase 2: 修繕計画の実施状況（確認済み）**
- **monthly_summaryテーブル**: ✅ 実装済み（マイグレーション完了）
- **新API (`/api/monthly/current`)**: ✅ 実装済み（`app/blueprints/monthly_current.py`）
- **フロントエンド統合**: ✅ 実装済み（`USE_NEW_API = true`）
- **事前集計更新ロジック**: ✅ 実装済み（`app/services/monthly_summary_updater.py`）
- **ステータス変更時の自動更新**: ✅ 実装済み（`projects.py`, `invoices.py`）

#### ✅ **Phase 2の改善状況（最新確認）**
- **CORSエラー**: ✅ 解消済み（エラーなし）
- **500 Internal Server Error**: ✅ 解消済み（エラーなし）
- **認証方式の統一**: ✅ 統一済み（`@login_required`使用）
- **新APIの正常動作**: ✅ 正常動作（エラーなし、データ取得完了）

### 1.2 新たに発見された課題（最新コンソールログ分析）

#### ⚠️ **最重要課題**
1. **スケルトン表示時間の遅延**: 体感15秒（目標 < 1秒）
2. **複数回のAPI呼び出し**: 初期化時に複数回発生
3. **ローディング状態管理の問題**: 適切に管理されていない

#### ⚠️ **パフォーマンス課題**
- **Load完了時間**: 2.02秒（目標 < 1秒）
- **スケルトン表示時間**: 体感15秒（目標 < 1秒）
- **APIレスポンスタイム**: 未測定（目標 < 200ms）

---

## 2. フェーズ3の目標と目的（更新）

### 2.1 計画の目標と目的（最新認識）

#### **根本的な目標**
計画書v2.0, v2.1に記載されている目標を100%達成する。

#### **具体的な目的（優先順位順）**

**最優先（Phase 2で発見）**:
1. **スケルトン表示時間の最適化**
   - 目標: < 1秒（計画書v2.0）
   - 現状: 体感15秒
   - 原因: 複数回のAPI呼び出しとローディング状態管理の問題

2. **複数回のAPI呼び出しの削減**
   - 目標: 1回（計画書v2.0）
   - 現状: 複数回呼び出し
   - 原因: 複数のトリガー（初期化、タブ変更、watch）が同時に発生

3. **ローディング状態管理の改善**
   - 目標: 適切な管理
   - 現状: 複数のAPI呼び出しが完了するまで`loading`が`true`のまま
   - 原因: ローカル`loading`とストア`loading`が独立して管理されている

**高優先（計画書v2.1 Phase 3）**:
4. **パフォーマンス目標達成**
   - APIレスポンスタイム: < 200ms（計画書v2.1 Phase 3）
   - Load完了時間: < 800ms（計画書v2.1 Phase 3）

5. **事前集計テーブルの最適化**
   - ステータス変更時の自動更新の確実化
   - エラーハンドリングの強化
   - パフォーマンス監視の実装

6. **既存機能との完全な統合**
   - 他の機能やUIとの競合・干渉の排除
   - 安定性の向上

### 2.2 大原則の適用（確認）

| 原則 | 適用方針 | フェーズ3での適用 |
|------|----------|------------------|
| **引き継ぎ書準拠** | ✅ 計画書v2.0, v2.1の設計を100%実装 | 計画書の目標を完全達成 |
| **根本解決 > 暫定解決** | ✅ 複数回API呼び出しの根本原因を特定・修正 | 重複防止ロジックの改善 |
| **シンプル構造 > 複雑構造** | ✅ ローディング状態管理の簡素化・統一化 | ローカル`loading`とストア`loading`の統一 |
| **統一・同一化 > 特殊独自** | ✅ データ取得ロジックの統一化 | 新API (`/api/monthly/current`) の使用を徹底 |
| **具体的 > 一般** | ✅ 具体的なパフォーマンス数値目標を設定 | < 1秒（スケルトン）、< 200ms（API） |
| **拙速 < 安全確実** | ✅ 段階的実装・テスト・検証を徹底 | 各ステップでの動作確認 |

---

## 3. 完全な問題分析

### 3.1 複数回のAPI呼び出しの原因（完全特定）

#### **原因1: 初期化時の複数トリガー**

**発生箇所**:
1. `MonthlyStatsSection.vue`の`onMounted`: `fetchCurrentMonthlyData()` → `loadData()`
2. `monthlyRotation.js`の`startRotationMonitoring()`: 初回チェックで`checkRotationStatus()` → `refreshFrontendData()`
3. `DashboardPage.vue`の`onMounted`: 複数のデータ取得（`projects`, `invoices`, `todos`）

**発生タイミング**:
```
DashboardPage.onMounted
  → rotationStore.startRotationMonitoring()
    → checkRotationStatus() [初回実行]
      → refreshFrontendData()
        → fetchStats(), fetchTargets()
  
  → MonthlyStatsSection.onMounted
    → fetchCurrentMonthlyData()
      → loadData()
```

**問題点**:
- 複数の初期化処理が同時に実行される
- それぞれが独立してAPI呼び出しを行う
- 重複防止ロジックが機能していない

#### **原因2: watchによる自動再取得**

**発生箇所**:
1. `watch(() => props.currentTab)`: タブ変更時に`loadData()`
2. `watch(() => projectsStore.projects, { deep: true })`: プロジェクト変更時に`loadData()`
3. `watch(() => invoicesStore.invoices, { deep: true })`: 請求書変更時に`loadData()`
4. `watch(() => monthlyStore.targets[monthKey])`: 目標変更時に`fetchStats()`

**問題点**:
- `deep: true`により、プロジェクト・請求書の細かな変更でも`loadData()`が呼び出される
- 月次統計は履歴ベースで計算されるため、プロジェクト・請求書の変更時に再取得する必要はない（バックエンドで自動更新される）
- 初期化時にも`projectsStore.projects`や`invoicesStore.invoices`が変更されるため、`watch`が発火する

**不要なAPI呼び出し**:
- プロジェクト・請求書の変更時に`loadData()`を呼び出す必要はない
- 月次統計は`monthly_summary`テーブルで事前集計されている
- ステータス変更時にバックエンドで自動更新される

#### **原因3: 月次切り替え状態チェックとの競合**

**発生箇所**:
- `monthlyRotation.js`の`checkRotationStatus()`: `refreshFrontendData()` → `fetchStats()`, `fetchTargets()`
- `MonthlyStatsSection.vue`の`onMounted`: `fetchCurrentMonthlyData()`

**問題点**:
- 月次切り替え状態チェック時に`refreshFrontendData()`が呼び出される
- 同時に`MonthlyStatsSection`の`onMounted`でも`fetchCurrentMonthlyData()`が呼び出される
- 両方が独立してAPI呼び出しを行う

### 3.2 ローディング状態管理の問題（完全特定）

#### **原因1: ローカル`loading`とストア`loading`の独立管理**

**現状**:
- `MonthlyStatsSection.vue`: `const loading = ref(false)`（ローカル管理）
- `monthlyStore`: `this.loading = true`（ストア管理）

**問題点**:
- ローカル`loading`とストア`loading`が独立して管理されている
- 複数のAPI呼び出しが完了するまで、どちらの`loading`も`false`にならない
- スケルトンは`v-if="!loading"`で制御されているため、最後のAPI呼び出しが完了するまで表示され続ける

**影響**:
- 最初のAPI呼び出しが完了してもスケルトンが非表示にならない
- 複数のAPI呼び出しが完了するまで`loading.value`が`false`にならない
- 体感15秒スケルトンが表示される

#### **原因2: 複数の非同期処理の並行実行**

**現状**:
```
loadData() {
  loading.value = true  // 1回目
  // API呼び出し1
  // API呼び出し2
  // API呼び出し3
  loading.value = false  // 全て完了後
}
```

**問題点**:
- 複数のAPI呼び出しが並行実行される
- 全てのAPI呼び出しが完了するまで`loading.value = false`にならない
- 最初のAPI呼び出しが完了してもスケルトンが非表示にならない

### 3.3 スケルトン表示時間の遅延の原因（完全特定）

#### **根本原因**
1. **複数回のAPI呼び出し**: 初期化時に複数のAPI呼び出しが発生
2. **ローディング状態管理の問題**: 複数のAPI呼び出しが完了するまで`loading`が`true`のまま
3. **不要なwatchによる再取得**: プロジェクト・請求書の変更時に不要な再取得が発生

#### **タイムライン分析**
```
0ms:   DashboardPage.onMounted開始
       → rotationStore.startRotationMonitoring()
       → checkRotationStatus() [初回実行]
       → refreshFrontendData()
       → fetchStats(), fetchTargets() [API呼び出し1, 2]

100ms: MonthlyStatsSection.onMounted開始
       → fetchCurrentMonthlyData() [API呼び出し3]
       → loadData()

200ms: watch(() => projectsStore.projects)発火 [初期化完了]
       → loadData() [API呼び出し4]

300ms: watch(() => invoicesStore.invoices)発火 [初期化完了]
       → loadData() [API呼び出し5]

... (複数回のAPI呼び出しが継続)

15000ms: 最後のAPI呼び出し完了
         → loading.value = false
         → スケルトン非表示
```

### 3.4 データ取得ロジックの問題（完全特定）

#### **問題1: 新APIの使用が不十分**

**現状**:
- `MonthlyStatsSection.vue`の`loadData()`で新APIを使用
- しかし、`watch`による再取得では旧API（`fetchStats()`, `fetchTargets()`）を使用

**問題点**:
- 新API (`/api/monthly/current`) の使用が不徹底
- `watch`による再取得時に旧APIを使用している

#### **問題2: データ取得タイミングの不適切**

**現状**:
- 初期化時に`fetchCurrentMonthlyData()`を呼び出し
- タブ変更時に`loadData()`を呼び出し
- プロジェクト・請求書の変更時に`loadData()`を呼び出し
- 月次切り替え状態チェック時に`refreshFrontendData()`を呼び出し

**問題点**:
- 複数のタイミングでデータ取得が発生
- 同じデータを複数回取得している
- キャッシュが適切に機能していない

---

## 4. 実装計画（更新）

### 4.1 フェーズ3の実装範囲（優先順位順）

#### **Step 3-1: スケルトン表示時間の最適化（最優先）**

**目的**: スケルトン表示時間を体感15秒から< 1秒に短縮

**実装内容**:
1. 複数回のAPI呼び出しの削減
   - 初期化時の重複呼び出しを統合
   - `watch`による不要な再取得を削減
   - 月次切り替え状態チェックとの統合

2. ローディング状態管理の改善
   - ローカル`loading`とストア`loading`の統一
   - 複数のAPI呼び出しの完了状態を適切に追跡
   - 最初のAPI呼び出しが完了したらスケルトンを非表示

3. データ取得タイミングの最適化
   - 初期化時のデータ取得を1回に統合
   - `watch`による不要な再取得を削減
   - 新API (`/api/monthly/current`) の使用を徹底

**期待効果**:
- スケルトン表示時間: 体感15秒 → < 1秒
- API呼び出し回数: 複数回 → 1回
- Load完了時間: 2.02秒 → < 1秒

#### **Step 3-2: パフォーマンス最適化**

**目的**: APIレスポンスタイム < 200ms、Load完了時間 < 800msを達成

**実装内容**:
1. 事前集計テーブルの活用確認
   - `monthly_summary`テーブルのデータ確認
   - クエリ実行計画の確認
   - インデックスの確認

2. クエリ最適化
   - N+1問題の解消
   - 不要なJOINの削除
   - インデックスの最適化

3. フロントエンドの最適化
   - 不要な`watch`の削減
   - キャッシュ管理の最適化
   - 不要な再レンダリングの削減

4. パフォーマンス測定・監視
   - APIレスポンスタイムの測定
   - Load完了時間の測定
   - パフォーマンス監視の実装

**期待効果**:
- APIレスポンスタイム: < 200ms
- Load完了時間: < 800ms

#### **Step 3-3: 事前集計テーブルの最適化**

**目的**: ステータス変更時の自動更新の確実化

**実装内容**:
1. エラーハンドリングの強化
   - `monthly_summary_updater.py`のエラーハンドリング強化
   - ログ出力の強化
   - リトライ機能の実装（必要に応じて）

2. データ整合性チェック機能
   - データ整合性チェック機能の実装
   - 整合性チェック用のエンドポイント追加（既に`monthly_summary_admin.py`に実装済み）

3. 監視・アラート機能
   - 監視・アラート機能の実装（将来拡張）

#### **Step 3-4: 既存機能との統合確認**

**目的**: 他の機能やUIとの競合・干渉を排除

**実装内容**:
1. DashboardPageとの統合確認
2. MonthlyTabs、MonthlyStatsSectionとの統合確認
3. 他のストア（projects, invoices, todos）との相互作用確認
4. エンドツーエンドテストの実施

### 4.2 実装優先順位（更新）

```
優先度: 最高（体感15秒の問題を最優先解決）
└─ Step 3-1: スケルトン表示時間の最適化
   ├─ 3-1-1: 複数回のAPI呼び出しの削減（最優先）
   ├─ 3-1-2: ローディング状態管理の改善
   └─ 3-1-3: データ取得タイミングの最適化
   ↓
優先度: 高（計画書v2.1 Phase 3の目標達成）
└─ Step 3-2: パフォーマンス最適化
   ├─ 3-2-1: 事前集計テーブルの活用確認
   ├─ 3-2-2: クエリ最適化
   ├─ 3-2-3: フロントエンドの最適化
   └─ 3-2-4: パフォーマンス測定・監視
   ↓
優先度: 中
└─ Step 3-3: 事前集計テーブルの最適化
   ↓
優先度: 低
└─ Step 3-4: 既存機能との統合確認
```

---

## 5. 完全な競合・干渉リスク分析

### 5.1 既存機能との競合リスク（詳細調査）

#### **リスク1: DashboardPageとの統合（調査済み）**

**影響範囲**: `frontend/src/views/DashboardPage.vue`

**リスク内容**: 
- 月次管理セクションの追加により、レイアウトが崩れる可能性
- 既存のコンポーネント（ProjectsCard, InvoicesCard, TodoCard）との配置競合

**現状確認**:
- 月次管理セクションは独立したセクションとして配置済み
- レスポンシブデザインは実装済み

**対策**:
- 既存のレイアウトを維持
- 月次管理セクションは独立したセクションとして配置（現状維持）
- レスポンシブデザインの確認（現状維持）

**リスクレベル**: 🟢 **低**（既に統合済み、影響なし）

#### **リスク2: MonthlyTabsコンポーネントとの統合（調査済み）**

**影響範囲**: `frontend/src/components/MonthlyTabs.vue`

**リスク内容**:
- タブ自動切替ロジックとの競合
- 状態管理（`monthlyStore`, `monthlyRotationStore`）との相互作用

**現状確認**:
- タブ自動切替ロジックは実装済み
- ストア間の状態同期は実装済み

**対策**:
- 既存のタブ自動切替ロジックを維持（現状維持）
- ストア間の状態同期を確認（現状維持）
- 重複呼び出しの防止（改善必要）

**リスクレベル**: 🟡 **中**（重複呼び出しの改善が必要）

#### **リスク3: MonthlyStatsSectionコンポーネントとの統合（調査済み・改善必要）**

**影響範囲**: `frontend/src/components/MonthlyStatsSection.vue`

**リスク内容**:
- データ取得ロジックの重複
- ローディング状態管理の問題
- 複数回のAPI呼び出し

**現状確認**:
- `onMounted`で`fetchCurrentMonthlyData()`を呼び出し
- `watch(() => props.currentTab)`で`loadData()`を呼び出し
- `watch(() => projectsStore.projects, { deep: true })`で`loadData()`を呼び出し
- `watch(() => invoicesStore.invoices, { deep: true })`で`loadData()`を呼び出し
- `watch(() => monthlyStore.targets[monthKey])`で`fetchStats()`を呼び出し

**問題点**:
- 複数のトリガーが同時に発生し、重複呼び出しが発生
- `deep: true`により、不要な再取得が発生
- 月次統計は履歴ベースで計算されるため、プロジェクト・請求書の変更時に再取得する必要はない

**対策**:
- 新API (`/api/monthly/current`) の使用を徹底（改善必要）
- データ取得ロジックの統一化（改善必要）
- キャッシュ管理の統一化（改善必要）
- **不要な`watch`の削減**（新規対応）
  - `watch(() => projectsStore.projects, { deep: true })`の削減または条件付き実行
  - `watch(() => invoicesStore.invoices, { deep: true })`の削減または条件付き実行
  - 月次統計は履歴ベースで計算されるため、プロジェクト・請求書の変更時に再取得する必要はない

**リスクレベル**: 🔴 **高**（改善が必要）

#### **リスク4: 他のストアとの相互作用（調査済み・改善必要）**

**影響範囲**: `frontend/src/stores/projects.js`, `invoices.js`, `todos.js`

**リスク内容**:
- `watch(() => projectsStore.projects, { deep: true })`による不要な再取得
- `watch(() => invoicesStore.invoices, { deep: true })`による不要な再取得
- ステータス変更時の月次統計更新が重複実行される可能性

**現状確認**:
- `MonthlyStatsSection.vue`で`watch(() => projectsStore.projects, { deep: true })`を監視
- `MonthlyStatsSection.vue`で`watch(() => invoicesStore.invoices, { deep: true })`を監視
- 初期化時に`projectsStore.fetchProjects()`, `invoicesStore.fetchInvoices()`が実行される
- これらにより、初期化時に`watch`が発火し、不要な再取得が発生

**問題点**:
- 月次統計は履歴ベースで計算されるため、プロジェクト・請求書の変更時に再取得する必要はない
- ステータス変更時にバックエンドで自動更新される
- `deep: true`により、細かな変更でも`watch`が発火する

**対策**:
- **`watch(() => projectsStore.projects, { deep: true })`の削減または条件付き実行**（新規対応）
  - 月次統計は履歴ベースで計算されるため、プロジェクトの変更時に再取得する必要はない
  - ステータス変更時にバックエンドで自動更新される
- **`watch(() => invoicesStore.invoices, { deep: true })`の削減または条件付き実行**（新規対応）
  - 月次統計は履歴ベースで計算されるため、請求書の変更時に再取得する必要はない
  - ステータス変更時にバックエンドで自動更新される
- ステータス変更時の月次統計更新は1回のみ実行（既に実装済み）
- エラーハンドリングの強化（既存機能を破壊しない）
- トランザクション管理の確認（既に実装済み）

**リスクレベル**: 🔴 **高**（改善が必要）

### 5.2 データベースとの競合リスク（調査済み）

#### **リスク5: monthly_summaryテーブルの整合性（調査済み）**

**影響範囲**: `app/models/monthly_summary.py`, `app/services/monthly_summary_updater.py`

**リスク内容**:
- ステータス変更時の自動更新が失敗した場合のデータ不整合
- 複数のステータス変更が同時に発生した場合の競合状態

**現状確認**:
- ステータス変更時に自動更新が実装済み
- エラーハンドリングが実装済み（ログ出力、処理継続）

**対策**:
- トランザクション管理の強化（現状維持）
- エラーハンドリングの改善（ログ出力、リトライ機能）（改善可能）
- データ整合性チェック機能の実装（既に`monthly_summary_admin.py`に実装済み）

**リスクレベル**: 🟢 **低**（既に実装済み）

#### **リスク6: 既存テーブルへの影響（調査済み）**

**影響範囲**: `monthly_targets`, `project_status_history`, `invoice_status_history`

**リスク内容**:
- 既存テーブルのスキーマ変更による影響
- データ移行時の不整合

**対策**:
- 既存テーブルのスキーマ変更は行わない（計画）
- データ移行は不要（新規データのみ対象）
- 既存データへの影響を最小限に抑える（計画）

**リスクレベル**: 🟢 **低**（影響なし）

### 5.3 APIとの競合リスク（調査済み）

#### **リスク7: 既存APIとの競合（調査済み）**

**影響範囲**: `/api/monthly-targets`, `/api/monthly-stats/{year}/{month}`

**リスク内容**:
- 新API (`/api/monthly/current`) と既存APIの並存による混乱
- APIレスポンス形式の不整合

**対策**:
- 既存APIは維持（後方互換性）（現状維持）
- 新APIのレスポンス形式を統一（現状維持）
- フラグ (`USE_NEW_API`) による段階的移行（現状維持）

**リスクレベル**: 🟢 **低**（影響なし）

#### **リスク8: CORS設定の競合（調査済み）**

**影響範囲**: `app/__init__.py`, `config.py`

**リスク内容**:
- CORS設定の不一致によるエラー
- 既存APIへの影響

**現状確認**:
- `app/__init__.py`でCORS設定が実装済み
- `config.py`でCORS_ORIGINSが設定済み
- 現在エラーは出ていない

**対策**:
- CORS設定の統一化（現状維持）
- エラーハンドリングでのCORSヘッダー追加（改善可能）
- 既存APIへの影響を確認（現状維持）

**リスクレベル**: 🟢 **低**（現在エラーなし）

### 5.4 フロントエンドコンポーネント間の競合リスク（新規発見）

#### **リスク9: watchによる不要な再取得（新規発見・改善必要）**

**影響範囲**: `frontend/src/components/MonthlyStatsSection.vue`

**リスク内容**:
- `watch(() => projectsStore.projects, { deep: true })`による不要な再取得
- `watch(() => invoicesStore.invoices, { deep: true })`による不要な再取得
- 月次統計は履歴ベースで計算されるため、プロジェクト・請求書の変更時に再取得する必要はない

**現状確認**:
- `MonthlyStatsSection.vue`で`watch(() => projectsStore.projects, { deep: true })`を監視
- `MonthlyStatsSection.vue`で`watch(() => invoicesStore.invoices, { deep: true })`を監視
- 初期化時に`projectsStore.fetchProjects()`, `invoicesStore.fetchInvoices()`が実行される
- これらにより、初期化時に`watch`が発火し、不要な再取得が発生

**問題点**:
- 月次統計は履歴ベースで計算されるため、プロジェクト・請求書の変更時に再取得する必要はない
- ステータス変更時にバックエンドで自動更新される
- `deep: true`により、細かな変更でも`watch`が発火する
- 初期化時にも`projectsStore.projects`や`invoicesStore.invoices`が変更されるため、`watch`が発火する

**対策**:
- **`watch(() => projectsStore.projects, { deep: true })`の削減または条件付き実行**（新規対応）
  - 月次統計は履歴ベースで計算されるため、プロジェクトの変更時に再取得する必要はない
  - ステータス変更時にバックエンドで自動更新される
  - または、初期化完了後のみ`watch`を有効化
- **`watch(() => invoicesStore.invoices, { deep: true })`の削減または条件付き実行**（新規対応）
  - 月次統計は履歴ベースで計算されるため、請求書の変更時に再取得する必要はない
  - ステータス変更時にバックエンドで自動更新される
  - または、初期化完了後のみ`watch`を有効化

**リスクレベル**: 🔴 **高**（改善が必要）

#### **リスク10: ローディング状態管理の競合（新規発見・改善必要）**

**影響範囲**: `frontend/src/components/MonthlyStatsSection.vue`, `frontend/src/stores/monthly.js`

**リスク内容**:
- ローカル`loading`とストア`loading`が独立して管理されている
- 複数のAPI呼び出しが完了するまで、どちらの`loading`も`false`にならない
- スケルトンは`v-if="!loading"`で制御されているため、最後のAPI呼び出しが完了するまで表示され続ける

**現状確認**:
- `MonthlyStatsSection.vue`: `const loading = ref(false)`（ローカル管理）
- `monthlyStore`: `this.loading = true`（ストア管理）
- スケルトンは`v-if="!loading"`で制御

**問題点**:
- ローカル`loading`とストア`loading`が独立して管理されている
- 複数のAPI呼び出しが完了するまで、どちらの`loading`も`false`にならない
- 最初のAPI呼び出しが完了してもスケルトンが非表示にならない

**対策**:
- **ローカル`loading`とストア`loading`の統一**（新規対応）
  - ストア`loading`のみを使用し、ローカル`loading`を削除
  - または、ローカル`loading`のみを使用し、ストア`loading`は使用しない
- **複数のAPI呼び出しの完了状態を適切に追跡**（新規対応）
  - 最初のAPI呼び出しが完了したらスケルトンを非表示
  - または、全てのAPI呼び出しが完了するまで待つ（現状維持、ただし最適化が必要）

**リスクレベル**: 🔴 **高**（改善が必要）

---

## 6. 実装手順（詳細版）

### 6.1 Step 3-1: スケルトン表示時間の最適化（最優先）

#### **3-1-1: 複数回のAPI呼び出しの削減（最優先）**

**調査結果**:
- 初期化時に複数のAPI呼び出しが発生
  - `MonthlyStatsSection.vue`の`onMounted`: `fetchCurrentMonthlyData()`
  - `monthlyRotation.js`の`startRotationMonitoring()`: 初回チェックで`checkRotationStatus()` → `refreshFrontendData()`
- `watch`による不要な再取得
  - `watch(() => projectsStore.projects, { deep: true })`: 初期化時にも発火
  - `watch(() => invoicesStore.invoices, { deep: true })`: 初期化時にも発火

**実装内容**:

**1. 初期化時の重複呼び出しを統合**

**修正対象**: `frontend/src/components/MonthlyStatsSection.vue`

**修正内容**:
- `onMounted`で`fetchCurrentMonthlyData()`を呼び出す前に、既にデータが取得済みか確認
- `monthlyRotation.js`の`checkRotationStatus()`との統合
- 重複防止ロジックの強化

**2. `watch`による不要な再取得を削減**

**修正対象**: `frontend/src/components/MonthlyStatsSection.vue`

**修正内容**:
- `watch(() => projectsStore.projects, { deep: true })`の削減または条件付き実行
  - 月次統計は履歴ベースで計算されるため、プロジェクトの変更時に再取得する必要はない
  - ステータス変更時にバックエンドで自動更新される
  - または、初期化完了後のみ`watch`を有効化
- `watch(() => invoicesStore.invoices, { deep: true })`の削減または条件付き実行
  - 月次統計は履歴ベースで計算されるため、請求書の変更時に再取得する必要はない
  - ステータス変更時にバックエンドで自動更新される
  - または、初期化完了後のみ`watch`を有効化

**3. 月次切り替え状態チェックとの統合**

**修正対象**: `frontend/src/stores/monthlyRotation.js`

**修正内容**:
- `checkRotationStatus()`でのデータ取得と`MonthlyStatsSection`の初期化時のデータ取得を統合
- 重複防止ロジックの強化

**期待効果**:
- API呼び出し回数: 複数回 → 1回
- スケルトン表示時間: 体感15秒 → < 1秒

#### **3-1-2: ローディング状態管理の改善**

**調査結果**:
- ローカル`loading`とストア`loading`が独立して管理されている
- 複数のAPI呼び出しが完了するまで、どちらの`loading`も`false`にならない
- 最初のAPI呼び出しが完了してもスケルトンが非表示にならない

**実装内容**:

**1. ローカル`loading`とストア`loading`の統一**

**修正対象**: `frontend/src/components/MonthlyStatsSection.vue`, `frontend/src/stores/monthly.js`

**修正内容**:
- ストア`loading`のみを使用し、ローカル`loading`を削除
- または、ローカル`loading`のみを使用し、ストア`loading`は使用しない（スケルトン表示用のみ）

**2. 複数のAPI呼び出しの完了状態を適切に追跡**

**修正対象**: `frontend/src/components/MonthlyStatsSection.vue`

**修正内容**:
- 最初のAPI呼び出しが完了したらスケルトンを非表示
- または、全てのAPI呼び出しが完了するまで待つ（ただし、最適化が必要）

**期待効果**:
- スケルトン表示時間: 体感15秒 → < 1秒
- 最初のAPI呼び出しが完了したらスケルトンを非表示

#### **3-1-3: データ取得タイミングの最適化**

**調査結果**:
- 初期化時に複数のデータ取得が発生
- `watch`による不要な再取得が発生
- 新API (`/api/monthly/current`) の使用が不徹底

**実装内容**:

**1. 初期化時のデータ取得を1回に統合**

**修正対象**: `frontend/src/components/MonthlyStatsSection.vue`, `frontend/src/views/DashboardPage.vue`

**修正内容**:
- 初期化時のデータ取得を1回に統合
- `monthlyRotation.js`の`checkRotationStatus()`との統合

**2. 新API (`/api/monthly/current`) の使用を徹底**

**修正対象**: `frontend/src/components/MonthlyStatsSection.vue`

**修正内容**:
- `watch`による再取得時も新APIを使用
- 旧API（`fetchStats()`, `fetchTargets()`）の使用を削減

**期待効果**:
- API呼び出し回数: 複数回 → 1回
- データ取得タイミングの最適化

### 6.2 Step 3-2: パフォーマンス最適化

#### **3-2-1: 事前集計テーブルの活用確認**

**調査項目**:
1. `monthly_summary`テーブルのデータ確認
2. クエリ実行計画の確認
3. インデックスの確認

**実装内容**:
- 事前集計テーブルの活用を確認
- クエリ最適化（必要に応じて）

#### **3-2-2: クエリ最適化**

**調査項目**:
1. N+1問題の確認
2. 不要なJOINの削除
3. インデックスの最適化

**実装内容**:
- クエリの最適化
- インデックスの追加（必要に応じて）

#### **3-2-3: フロントエンドの最適化**

**調査項目**:
1. 不要な`watch`の削減
2. キャッシュ活用の確認
3. 不要な再レンダリングの削減

**実装内容**:
- 不要な`watch`の削減（`watch(() => projectsStore.projects)`, `watch(() => invoicesStore.invoices)`）
- キャッシュ管理の最適化（既に実装済み）
- 不要な再レンダリングの削減

#### **3-2-4: パフォーマンス測定・監視**

**実装内容**:
- APIレスポンスタイムの測定
- Load完了時間の測定
- スケルトン表示時間の測定
- パフォーマンス監視の実装

### 6.3 Step 3-3: 事前集計テーブルの最適化

#### **3-3-1: エラーハンドリングの強化**

**実装内容**:
- `monthly_summary_updater.py`のエラーハンドリング強化
- ログ出力の強化
- リトライ機能の実装（必要に応じて）

#### **3-3-2: データ整合性チェック機能**

**実装内容**:
- データ整合性チェック機能の実装（既に`monthly_summary_admin.py`に実装済み）
- 整合性チェック用のエンドポイント追加（既に実装済み）

#### **3-3-3: 監視・アラート機能**

**実装内容**:
- 監視・アラート機能の実装（将来拡張）

### 6.4 Step 3-4: 既存機能との統合確認

#### **3-4-1: DashboardPageとの統合確認**

**確認項目**:
1. レイアウトの確認
2. コンポーネント間の相互作用確認
3. レスポンシブデザインの確認

#### **3-4-2: 他のストアとの相互作用確認**

**確認項目**:
1. `projectsStore`との相互作用
2. `invoicesStore`との相互作用
3. `todosStore`との相互作用

#### **3-4-3: エンドツーエンドテスト**

**テスト項目**:
1. ステータス変更時の月次統計更新
2. 目標設定・保存機能
3. タブ自動切替機能
4. データ表示の整合性

---

## 7. 完全なリスク管理

### 7.1 想定リスクと対策（更新）

| リスク | 影響度 | 対策 | 優先度 |
|--------|--------|------|--------|
| スケルトン表示時間が改善しない | 高 | 複数回API呼び出しの削減、ローディング状態管理の改善 | **最優先** |
| 複数回のAPI呼び出しが削減できない | 高 | 初期化時の重複呼び出しを統合、`watch`による不要な再取得を削減 | **最優先** |
| ローディング状態管理が改善しない | 高 | ローカル`loading`とストア`loading`の統一 | **最優先** |
| `watch`の削減によるデータ不整合 | 中 | 月次統計は履歴ベースで計算されるため、プロジェクト・請求書の変更時に再取得する必要はない（バックエンドで自動更新） | **高** |
| パフォーマンス目標を達成できない | 中 | 段階的な最適化、代替案の検討 | **高** |
| 既存機能への影響 | 中 | 段階的実装、テスト、検証 | **中** |

### 7.2 ロールバック計画（更新）

#### **緊急ロールバック手順**
1. `USE_NEW_API = false`に変更（フロントエンド）
2. 新APIのBlueprint登録をコメントアウト（バックエンド）
3. 既存APIへのフォールバック確認
4. 問題解決後に再実装

#### **部分的ロールバック手順**
1. `watch`による不要な再取得を元に戻す（`watch(() => projectsStore.projects)`, `watch(() => invoicesStore.invoices`)）
2. ローディング状態管理の変更を元に戻す（ローカル`loading`とストア`loading`の分離）

---

## 8. 実装スケジュール（更新）

### 8.1 全体タイムライン（更新）

```
Step 3-1: スケルトン表示時間の最適化（3-4時間）
  ├─ 3-1-1: 複数回のAPI呼び出しの削減（2時間）
  ├─ 3-1-2: ローディング状態管理の改善（1時間）
  └─ 3-1-3: データ取得タイミングの最適化（1時間）
  ↓
Step 3-2: パフォーマンス最適化（2-3時間）
  ├─ 3-2-1: 事前集計テーブルの活用確認（30分）
  ├─ 3-2-2: クエリ最適化（1時間）
  ├─ 3-2-3: フロントエンドの最適化（1時間）
  └─ 3-2-4: パフォーマンス測定・監視（30分）
  ↓
Step 3-3: 事前集計テーブルの最適化（1-2時間）
  ↓
Step 3-4: 既存機能との統合確認（1-2時間）

合計所要時間: 7-11時間
```

### 8.2 マイルストーン（更新）

| マイルストーン | 完了判定 | 次ステップ開始条件 |
|--------------|---------|-------------------|
| **Step 3-1** | スケルトン表示時間 < 1秒 | 即座にStep 3-2開始 |
| **Step 3-2** | パフォーマンス目標達成（API < 200ms, Load < 800ms） | 即座にStep 3-3開始 |
| **Step 3-3** | エラーハンドリング強化 | 即座にStep 3-4開始 |
| **Step 3-4** | 統合確認完了 | 完了 |

---

## 9. 完了判定基準（更新）

### 9.1 Step 3-1完了条件（最優先）

- [ ] 複数回のAPI呼び出しが1回に削減
- [ ] スケルトン表示時間 < 1秒（体感15秒 → < 1秒）
- [ ] ローディング状態管理が改善
- [ ] データ取得タイミングが最適化

### 9.2 Step 3-2完了条件

- [ ] APIレスポンスタイム < 200ms（本番環境）
- [ ] Load完了時間 < 800ms（本番環境）
- [ ] 事前集計テーブルの活用確認
- [ ] クエリ最適化の確認

### 9.3 Step 3-3完了条件

- [ ] エラーハンドリングの強化確認
- [ ] データ整合性チェック機能の実装確認
- [ ] ステータス変更時の自動更新の確実化確認

### 9.4 Step 3-4完了条件

- [ ] DashboardPageとの統合確認
- [ ] 他のストアとの相互作用確認
- [ ] エンドツーエンドテストの合格

---

## 10. 重要な発見事項

### 10.1 新規発見された問題（最新コンソールログ分析）

#### **問題1: 不要な`watch`による再取得（新規発見）**

**現状**:
- `watch(() => projectsStore.projects, { deep: true })`: 初期化時にも発火
- `watch(() => invoicesStore.invoices, { deep: true })`: 初期化時にも発火

**問題点**:
- 月次統計は履歴ベースで計算されるため、プロジェクト・請求書の変更時に再取得する必要はない
- ステータス変更時にバックエンドで自動更新される
- `deep: true`により、細かな変更でも`watch`が発火する
- 初期化時にも`projectsStore.projects`や`invoicesStore.invoices`が変更されるため、`watch`が発火する

**対策**:
- `watch(() => projectsStore.projects, { deep: true })`の削減または条件付き実行
- `watch(() => invoicesStore.invoices, { deep: true })`の削減または条件付き実行

#### **問題2: ローディング状態管理の不統一（新規発見）**

**現状**:
- `MonthlyStatsSection.vue`: `const loading = ref(false)`（ローカル管理）
- `monthlyStore`: `this.loading = true`（ストア管理）

**問題点**:
- ローカル`loading`とストア`loading`が独立して管理されている
- 複数のAPI呼び出しが完了するまで、どちらの`loading`も`false`にならない
- 最初のAPI呼び出しが完了してもスケルトンが非表示にならない

**対策**:
- ローカル`loading`とストア`loading`の統一
- 複数のAPI呼び出しの完了状態を適切に追跡

### 10.2 Phase 2の改善状況（最新確認）

**✅ 改善された項目**:
- CORSエラーの解消（エラーなし）
- 500エラーの解消（エラーなし）
- 認証方式の統一（`@login_required`使用）
- 新APIの正常動作（エラーなし、データ取得完了）

**⚠️ 新たに発見された問題**:
- スケルトン表示時間の遅延（体感15秒）
- 複数回のAPI呼び出し
- ローディング状態管理の問題
- 不要な`watch`による再取得

---

## 11. 実装戦略（更新）

### 11.1 段階的実装アプローチ

#### **Phase 1: 緊急対応（Step 3-1）**
- 複数回のAPI呼び出しの削減
- ローディング状態管理の改善
- データ取得タイミングの最適化

**期待効果**: スケルトン表示時間 体感15秒 → < 1秒

#### **Phase 2: パフォーマンス最適化（Step 3-2）**
- 事前集計テーブルの活用確認
- クエリ最適化
- フロントエンドの最適化

**期待効果**: APIレスポンスタイム < 200ms, Load完了時間 < 800ms

#### **Phase 3: 最適化の確実化（Step 3-3, 3-4）**
- 事前集計テーブルの最適化
- 既存機能との統合確認

### 11.2 実装方針（大原則準拠）

#### **根本解決 > 暫定解決**
- 複数回API呼び出しの根本原因（初期化時の重複、不要な`watch`）を特定・修正
- ローディング状態管理の根本原因（ローカル`loading`とストア`loading`の分離）を特定・修正

#### **シンプル構造 > 複雑構造**
- ローディング状態管理の簡素化・統一化
- データ取得ロジックの統一化

#### **統一・同一化 > 特殊独自**
- 新API (`/api/monthly/current`) の使用を徹底
- ローディング状態管理の統一

#### **具体的 > 一般**
- 具体的なパフォーマンス数値目標を設定（< 1秒、< 200ms）

#### **拙速 < 安全確実**
- 段階的実装・テスト・検証を徹底
- 各ステップでの動作確認

---

**作成日**: 2025年11月1日（更新）
**作成者**: AI Assistant
**計画書バージョン**: v2.0（更新版）
**対象システム**: InfluBerry 月次管理機能
**最新認識**: コンソールログ分析に基づく完全な調査結果を反映


