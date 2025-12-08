# ステージング環境ブラウザテスト結果 - 詳細分析レポート

**テスト日時**: 2025年11月1日  
**環境**: ステージング環境  
**テストユーザー**: test3@air-edison.com  
**ブラウザ**: Chrome DevTools Network タブ

---

## 1. テスト結果サマリー

### 1.1 パフォーマンス指標

| 指標 | 実測値 | 目標値 | 達成状況 | 超過率 |
|------|--------|--------|---------|--------|
| **Finish Time** | **22.50秒** | < 2秒 | ❌ | **1,025%超過** (11.25倍) |
| **Load Time** | **1.53秒** | < 800ms | ❌ | **91%超過** (1.91倍) |
| **DOMContentLoaded** | **795ms** | < 800ms | ✅ | 目標達成 |
| **Total Requests** | 52件 | - | - | - |
| **Transferred Data** | 5,454 kB | - | - | - |
| **Resources** | 6,766 kB | - | - | - |

**総合評価**: 🔴 **深刻な問題あり**

---

## 2. API呼び出しの詳細分析

### 2.1 月次API呼び出しパターン

#### 呼び出されたAPIエンドポイント

| エンドポイント | レスポンスタイム | サイズ | ステータス | 評価 |
|-------------|---------------|--------|----------|------|
| `/api/monthly/overview` | **4.55秒** | 0.4 kB | 200 | ❌ 異常に遅い |
| `/api/monthly-stats/10` | **7.53秒** | 0.4 kB | 200 | ❌ 異常に遅い |
| `/api/monthly/current` | **14.83秒** | 0.5 kB | 200 | ❌ 極めて遅い |
| `/api/monthly-targets/?year=2025&months=10` | **11.42秒** | 0.4 kB | 200 | ❌ 極めて遅い |

**合計APIレスポンスタイム**: **38.33秒**（4つのAPIの合計）

### 2.2 API呼び出しの問題点

#### 問題1: API分離戦略が未実装

**現状**:
```
❌ /api/monthly/overview        (4.55秒)
❌ /api/monthly-stats/10        (7.53秒)
❌ /api/monthly/current         (14.83秒)  ← 実装されているが遅すぎる
❌ /api/monthly-targets/...     (11.42秒)
```

**計画書v2.0/v2.1の設計**:
```
✅ /api/monthly/current  (< 500ms) → 3ヶ月分を一度に返却
```

**判定**: 
- `/api/monthly/current` は実装されているが、**レスポンスタイムが目標の29.66倍**
- 依然として個別APIも呼び出されており、API分離が不完全

#### 問題2: 複数APIの並行呼び出し

4つの異なるAPIエンドポイントが呼び出されており、それぞれが5-15秒かかっている。これは以下を示唆：

1. **フロントエンドの問題**: 
   - `/api/monthly/current` が実装されているにも関わらず、旧来の個別API（overview, stats/10, targets）も呼び出されている
   - API移行が不完全

2. **バックエンドの問題**:
   - `/api/monthly/current` のレスポンスタイムが14.83秒と異常に遅い
   - 事前集計テーブル（monthly_summary）が活用されていない可能性

#### 問題3: レスポンスタイムの異常値

| API | レスポンスタイム | データサイズ | 問題 |
|-----|---------------|------------|------|
| `/api/monthly/current` | 14.83秒 | 0.5 kB | データサイズが小さいのに異常に遅い |
| `/api/monthly-targets/...` | 11.42秒 | 0.4 kB | データサイズが小さいのに異常に遅い |

**分析**:
- データサイズが0.4-0.5 kBと非常に小さい
- ネットワーク転送時間ではなく、**サーバー側の処理時間が問題**
- リアルタイム計算による遅延の可能性が高い

---

## 3. フロントエンドの動作分析

### 3.1 コンソールログから見る動作パターン

#### Phase 2のタブ切り替え処理

```javascript
// 1. ページロード時
🔧 月次切り替え完了を検知 - タブ更新をトリガー
🔧 タブ更新をトリガーします。
⚠️ lastRotationCheckが現在月より古い - 現在月を優先

// 2. タブが複数回切り替わる
🔧 Phase 2: currentMonthTabの変更を検知 {newTab: '2025-11', oldTab: 'overview'}
🔧 Phase 2: currentMonthTabの変更を検知 {newTab: '2025-10', oldTab: '2025-11'}
🔧 Phase 2: currentMonthTabの変更を検知 {newTab: '2025-11', oldTab: '2025-10'}
```

**問題点**:
1. **タブの頻繁な切り替え**: `overview` → `2025-11` → `2025-10` → `2025-11`
2. **各切り替えでAPI呼び出しが発生**している可能性
3. **不安定な初期化処理**: 最終的なタブが決まるまでに複数回の切り替えが発生

### 3.2 lastRotationCheckの不整合

```javascript
⚠️ lastRotationCheckが現在月より古い - 現在月を優先
{
  currentMonthId: '2025-11',
  lastMonthId: '2025-10',
  lastRotationCheck: '2025-10-01T00:00:00',
  reason: 'lastRotationCheckが現在月より古いため、現在月を優先'
}
```

**問題点**:
- `lastRotationCheck` が `2025-10-01` のまま更新されていない
- テスト日時は2025年11月1日なのに、10月のデータが残っている
- 月次切り替えロジックが正しく動作していない可能性

### 3.3 リアクティブ更新の過剰な実行

```javascript
🔧 Phase 2: リアクティブな更新の同期化を実行
🔧 Phase 2: 第1回nextTick完了
🔧 Phase 2: 第2回nextTick完了
🔧 Phase 2: nextTickによる同期化完了（forceRerender削除）
🔧 Phase 2: 最終nextTick完了
🔧 Phase 2: 同期化後の状態確認
🎉 Phase 2: リアクティブな更新の同期化完了
```

このパターンが**複数回繰り返される**ことで、不必要なレンダリングとAPI呼び出しが発生している。

---

## 4. 根本原因の分析

### 4.1 バックエンド側の問題

#### 原因1: 事前集計テーブルの未活用

**推定される実装状況**:
```python
# ❌ 現在の実装（推定）
@monthly_current_bp.route('/api/monthly/current')
def get_current_monthly_data():
    # リアルタイム計算を実行（遅い）
    stats = calculate_monthly_stats_realtime(user_id, month)
    # → 14.83秒かかる
```

**計画書v2.0/v2.1の設計**:
```python
# ✅ 計画された実装
@monthly_current_bp.route('/api/monthly/current')
def get_current_monthly_data():
    # 事前集計テーブルから取得（高速）
    summary = MonthlySummary.query.filter_by(
        user_id=user_id,
        summary_month=month
    ).first()
    
    if summary:
        # 50-200msで取得可能
        return summary.to_dict()
    else:
        # フォールバック
        return calculate_realtime()
```

**判定**: 事前集計テーブル（MonthlySummary）が存在しないか、活用されていない

#### 原因2: N+1クエリ問題

レスポンスサイズが0.4-0.5 kBと小さいにも関わらず、レスポンスタイムが5-15秒かかることから、以下が推定される：

```python
# ❌ 複数のクエリが個別に実行される
acquired_positive = db.session.query(...).scalar()  # 1回目
acquired_negative = db.session.query(...).scalar()  # 2回目
completed_positive = db.session.query(...).scalar()  # 3回目
completed_negative = db.session.query(...).scalar()  # 4回目
# ... さらに複数のクエリ
```

各クエリが1-3秒かかると、合計で15秒以上になる。

#### 原因3: インデックスの不足

```sql
-- ProjectStatusHistory, InvoiceStatusHistory テーブルに
-- 適切なインデックスが存在しない可能性
CREATE INDEX idx_project_status_history_user_changed_at 
ON project_status_history(project_id, changed_at);

CREATE INDEX idx_invoice_status_history_user_changed_at 
ON invoice_status_history(invoice_id, changed_at);
```

これらのインデックスがない場合、フルテーブルスキャンが発生し、クエリが遅くなる。

#### 原因4: ステージング環境のリソース制限

Render.comのフリープランの場合：
- CPU: 共有CPU（制限あり）
- Memory: 512MB程度
- Database: 無料プラン（接続数制限あり）

これらの制限により、複雑なクエリの実行時間が本番環境よりも大幅に長くなる。

### 4.2 フロントエンド側の問題

#### 原因1: API移行の不完全

```javascript
// ❌ 現在の実装（推定）
// 新APIと旧APIの両方を呼び出している
await fetchOverview()              // /api/monthly/overview
await fetchStats(month)            // /api/monthly-stats/10
await fetchCurrentMonthlyData()    // /api/monthly/current
await fetchTargets(year, month)    // /api/monthly-targets/...
```

**計画された実装**:
```javascript
// ✅ 新APIのみを呼び出す
await fetchCurrentMonthlyData()  // /api/monthly/current
// → 3ヶ月分のデータ（targets + stats）を一度に取得
```

#### 原因2: タブ切り替えの不安定性

初期化時にタブが複数回切り替わることで：
1. 各切り替えでAPI呼び出しが発生
2. 前の呼び出しがキャンセルされず、複数の呼び出しが並行実行
3. 最終的なレスポンスタイムが合計される

#### 原因3: 重複実行防止フラグの不足

調査レポートで指摘した `fetchingCurrentMonthlyData` フラグが実装されていない可能性：

```javascript
// ❌ 重複実行防止なし
async fetchCurrentMonthlyData() {
    // 同時に複数回呼び出される可能性
    const res = await axios.get('/api/monthly/current')
}

// ✅ 重複実行防止あり
async fetchCurrentMonthlyData() {
    if (this.fetchingCurrentMonthlyData) return
    this.fetchingCurrentMonthlyData = true
    try {
        const res = await axios.get('/api/monthly/current')
    } finally {
        this.fetchingCurrentMonthlyData = false
    }
}
```

---

## 5. 問題の提起

### 5.1 致命的な問題（即座の対応が必要）

#### 問題1: ユーザー体験の崩壊

**現状**:
- ページロードに22.50秒かかる
- ユーザーは20秒以上待たされる
- 実用に耐えない状態

**影響**:
- ユーザーの離脱率が高くなる
- サービスの信頼性が著しく低下
- ビジネス目標が達成できない

#### 問題2: API分離戦略の実装不完全

**現状**:
- `/api/monthly/current` は実装されているが、レスポンスタイムが目標の30倍
- 旧来の個別API（overview, stats, targets）も依然として呼び出されている
- API移行が中途半端

**影響**:
- パフォーマンス改善の効果が得られない
- 計画書v2.0/v2.1の目標が未達成
- 開発リソースの無駄

#### 問題3: 事前集計テーブルの未実装または未活用

**現状**:
- `monthly_summary` テーブルが存在しないか、活用されていない
- リアルタイム計算により、APIレスポンスタイムが5-15秒

**影響**:
- パフォーマンス目標（< 500ms）の達成が不可能
- スケーラビリティの欠如
- ユーザー数増加時の破綻

### 5.2 深刻な問題（早期対応が必要）

#### 問題4: タブ切り替えの不安定性

**現状**:
- 初期化時にタブが `overview` → `2025-11` → `2025-10` → `2025-11` と複数回切り替わる
- 各切り替えでAPI呼び出しが発生する可能性

**影響**:
- 不必要なAPI呼び出しの増加
- レスポンスタイムのさらなる悪化
- UIの一貫性の欠如

#### 問題5: lastRotationCheckの不整合

**現状**:
- `lastRotationCheck` が `2025-10-01` のまま更新されない
- テスト日時（2025-11-01）との不整合

**影響**:
- 月次切り替えロジックの信頼性低下
- データの不整合
- バグの温床

#### 問題6: 重複実行防止の不足

**現状**:
- API呼び出しの重複実行防止フラグが実装されていない可能性

**影響**:
- 同じAPIが複数回呼び出される
- サーバー負荷の増加
- レスポンスタイムの悪化

### 5.3 中程度の問題（改善が望ましい）

#### 問題7: リアクティブ更新の過剰実行

**現状**:
- `nextTick` が複数回実行される
- 同期化処理が頻繁に発生

**影響**:
- CPU使用率の増加
- バッテリー消費の増加
- パフォーマンスの微妙な低下

#### 問題8: デバッグログの過多

**現状**:
- 16個のグローバルデバッグ関数が登録されている
- Phase 2, Phase 3, Phase 4のログが大量に出力される

**影響**:
- 本番環境でのパフォーマンス低下の可能性
- コンソールの可読性低下
- デバッグの困難化

---

## 6. パフォーマンス改善の修正案

### 6.1 最優先（Phase 1）: バックエンドの緊急対応

#### 修正案1-1: 事前集計テーブルの実装確認と修正

**目的**: APIレスポンスタイムを14.83秒 → < 500ms に改善

**実施内容**:

1. **MonthlySummaryテーブルの存在確認**
   - データベースにテーブルが存在するか確認
   - 存在しない場合は作成

2. **データの事前集計**
   - 既存データに対してmigrationを実行し、MonthlySummaryテーブルにデータを投入
   - ステータス変更時の自動更新ロジックを実装

3. **APIの修正**
   - `/api/monthly/current` を修正し、MonthlySummaryテーブルから取得
   - リアルタイム計算はフォールバックのみ

**期待効果**:
- APIレスポンスタイム: 14.83秒 → **50-200ms**（97%改善）
- Finish Time: 22.50秒 → **5-8秒**（65-78%改善）

#### 修正案1-2: データベースインデックスの追加

**目的**: クエリのパフォーマンス改善

**実施内容**:

```sql
-- ProjectStatusHistory テーブル
CREATE INDEX IF NOT EXISTS idx_psh_user_changed_at 
ON project_status_history(project_id, changed_at);

CREATE INDEX IF NOT EXISTS idx_psh_old_new_status 
ON project_status_history(old_status, new_status, changed_at);

-- InvoiceStatusHistory テーブル
CREATE INDEX IF NOT EXISTS idx_ish_user_changed_at 
ON invoice_status_history(invoice_id, changed_at);

CREATE INDEX IF NOT EXISTS idx_ish_old_new_status 
ON invoice_status_history(old_status, new_status, changed_at);

-- MonthlySummary テーブル
CREATE INDEX IF NOT EXISTS idx_ms_user_month 
ON monthly_summary(user_id, summary_month);
```

**期待効果**:
- リアルタイム計算（フォールバック時）のパフォーマンス改善
- 5-15秒 → 1-3秒（60-80%改善）

#### 修正案1-3: クエリの最適化

**目的**: N+1クエリ問題の解決

**実施内容**:

1. **クエリの統合**
   - 複数の個別クエリを1つのクエリにまとめる
   - JOINを使用して一度に取得

2. **EXPLAIN ANALYZEによる分析**
   - 各クエリのボトルネックを特定
   - 実行計画を最適化

**期待効果**:
- クエリ実行時間: 5-15秒 → **500ms-2秒**（70-90%改善）

### 6.2 高優先（Phase 2）: フロントエンドの修正

#### 修正案2-1: 旧APIの完全削除

**目的**: API呼び出し回数を4回 → 1回に削減

**実施内容**:

1. **旧APIエンドポイントの呼び出しを削除**
   ```javascript
   // ❌ 削除対象
   fetchOverview()
   fetchStats(month)
   fetchTargets(year, month)
   
   // ✅ 残す
   fetchCurrentMonthlyData()  // これだけで全データを取得
   ```

2. **フロントエンドのデータ構造を新APIに合わせる**
   - レスポンスデータを適切に分解
   - 既存のコンポーネントに適切に配分

**期待効果**:
- API呼び出し回数: 4回 → **1回**（75%削減）
- ネットワーク待機時間の削減
- Finish Time: 5-8秒 → **2-3秒**（50-70%改善）

#### 修正案2-2: 重複実行防止フラグの実装

**目的**: 同じAPIの重複呼び出しを防止

**実施内容**:

1. **monthlyStoreにフラグを追加**
   ```javascript
   state: () => ({
       fetchingCurrentMonthlyData: false,
   })
   ```

2. **fetchCurrentMonthlyData()に重複防止を実装**
   ```javascript
   async fetchCurrentMonthlyData() {
       if (this.fetchingCurrentMonthlyData) {
           console.log('既に実行中のためスキップ')
           return
       }
       this.fetchingCurrentMonthlyData = true
       try {
           const res = await axios.get('/api/monthly/current')
           // データ処理
       } finally {
           this.fetchingCurrentMonthlyData = false
       }
   }
   ```

**期待効果**:
- 重複API呼び出しの完全防止
- サーバー負荷の軽減

#### 修正案2-3: タブ切り替えロジックの安定化

**目的**: 初期化時のタブ切り替えを1回に限定

**実施内容**:

1. **初期化時の処理順序を明確化**
   ```javascript
   // 1. rotationStoreの状態を確認
   // 2. 現在月を確定
   // 3. currentMonthTabを設定（1回のみ）
   // 4. データ取得
   ```

2. **不要な中間状態を削除**
   - `overview` を経由せず、直接 `2025-11` に設定

3. **lastRotationCheckの更新**
   - 月次切り替え完了時に必ず更新
   - 不整合を防止

**期待効果**:
- タブ切り替え回数: 4回 → **1回**（75%削減）
- 不必要なAPI呼び出しの削減
- UIの安定性向上

### 6.3 中優先（Phase 3）: 最適化

#### 修正案3-1: リアクティブ更新の最適化

**目的**: 不要なレンダリングの削減

**実施内容**:

1. **nextTickの回数を削減**
   - 現在: 第1回、第2回、最終回の3回
   - 改善後: 1回のみ

2. **同期化処理の簡素化**
   - forceRerenderの完全削除
   - シンプルなリアクティブ更新のみ

**期待効果**:
- CPU使用率の軽減
- バッテリー消費の削減

#### 修正案3-2: デバッグログの本番環境での無効化

**目的**: 本番環境でのパフォーマンス最適化

**実施内容**:

1. **環境変数による制御**
   ```javascript
   if (import.meta.env.DEV) {
       console.log('🔧 デバッグログ')
   }
   ```

2. **グローバルデバッグ関数の条件付き登録**
   - 開発環境のみ登録
   - 本番環境では登録しない

**期待効果**:
- 本番環境でのパフォーマンス向上
- コンソールのクリーン化

#### 修正案3-3: ステージング環境のアップグレード検討

**目的**: より正確なパフォーマンステスト

**実施内容**:

1. **Render.comの有料プランへのアップグレード**
   - CPU: 専用CPU
   - Memory: 2GB以上
   - Database: 有料プラン（接続数増加）

2. **本番環境に近い構成でテスト**

**期待効果**:
- ステージング環境でのレスポンスタイム改善
- 本番環境のパフォーマンス予測精度向上

---

## 7. 実装優先順位と期待効果

### 7.1 Phase 1（即座実施）: バックエンド緊急対応

| 修正案 | 所要時間 | 期待効果 | 優先度 |
|--------|---------|---------|--------|
| **修正案1-1**: 事前集計テーブルの実装確認と修正 | 3-5時間 | APIレスポンス **97%改善** | 🔴 最高 |
| **修正案1-2**: データベースインデックスの追加 | 1-2時間 | クエリ **70-80%改善** | 🔴 最高 |
| **修正案1-3**: クエリの最適化 | 2-3時間 | クエリ実行時間 **70-90%改善** | 🔴 高 |

**Phase 1完了後の予測**:
- Finish Time: 22.50秒 → **3-5秒**（78-86%改善）
- APIレスポンスタイム: 14.83秒 → **< 1秒**（93%改善）

### 7.2 Phase 2（早期実施）: フロントエンド修正

| 修正案 | 所要時間 | 期待効果 | 優先度 |
|--------|---------|---------|--------|
| **修正案2-1**: 旧APIの完全削除 | 2-3時間 | API呼び出し **75%削減** | 🔴 高 |
| **修正案2-2**: 重複実行防止フラグの実装 | 1-2時間 | 重複呼び出し **完全防止** | 🔴 高 |
| **修正案2-3**: タブ切り替えロジックの安定化 | 2-4時間 | タブ切り替え **75%削減** | 🟡 中 |

**Phase 2完了後の予測**:
- Finish Time: 3-5秒 → **< 2秒**（目標達成）
- API呼び出し回数: 4回 → **1回**
- UIの安定性: **大幅改善**

### 7.3 Phase 3（継続改善）: 最適化

| 修正案 | 所要時間 | 期待効果 | 優先度 |
|--------|---------|---------|--------|
| **修正案3-1**: リアクティブ更新の最適化 | 2-3時間 | CPU使用率軽減 | 🟢 低 |
| **修正案3-2**: デバッグログの本番環境での無効化 | 1時間 | 本番パフォーマンス向上 | 🟢 低 |
| **修正案3-3**: ステージング環境のアップグレード検討 | - | テスト精度向上 | 🟢 低 |

---

## 8. 総合的な改善ロードマップ

### 8.1 Week 1: 緊急対応（Phase 1）

**Day 1-2**:
- 事前集計テーブルの実装確認
- データベースインデックスの追加
- 初期データのマイグレーション

**Day 3-4**:
- APIの修正（MonthlySummaryテーブルの活用）
- クエリの最適化
- テスト

**Day 5**:
- ステージング環境でのテスト
- パフォーマンス測定
- 問題の洗い出し

**期待効果**: Finish Time 22.50秒 → **3-5秒**

### 8.2 Week 2: フロントエンド修正（Phase 2）

**Day 1-2**:
- 旧APIの完全削除
- 重複実行防止フラグの実装

**Day 3-4**:
- タブ切り替えロジックの安定化
- lastRotationCheckの修正

**Day 5**:
- ステージング環境でのテスト
- パフォーマンス測定
- 目標達成確認

**期待効果**: Finish Time 3-5秒 → **< 2秒**（目標達成）

### 8.3 Week 3: 最適化（Phase 3）

**Day 1-3**:
- リアクティブ更新の最適化
- デバッグログの本番無効化
- 細かい調整

**Day 4-5**:
- 総合テスト
- ドキュメント作成
- 本番デプロイ準備

---

## 9. 結論

### 9.1 現状の評価

**判定**: 🔴 **深刻な問題 - 即座の対応が必要**

- Finish Time: 22.50秒（目標の11.25倍）
- APIレスポンスタイム: 5-15秒（目標の10-30倍）
- API呼び出し回数: 4回（目標の4倍）

**ユーザー体験**: 実用に耐えないレベル

### 9.2 根本原因

1. **バックエンド**: 事前集計テーブルの未活用、インデックス不足
2. **フロントエンド**: API移行の不完全、重複実行防止の不足
3. **環境**: ステージング環境のリソース制限

### 9.3 推奨アクション

**即座実施**:
1. 事前集計テーブルの実装確認と修正
2. データベースインデックスの追加
3. 旧APIの完全削除

**期待される最終結果**:
- ✅ Finish Time: < 2秒（目標達成）
- ✅ APIレスポンスタイム: < 500ms（目標達成）
- ✅ API呼び出し回数: 1回（目標達成）
- ✅ ユーザー体験: 実用レベルに改善

---

**レポート作成日**: 2025年11月1日  
**分析者**: Claude (AI Assistant)  
**参照データ**: ステージング環境ブラウザテスト結果（2025-11-01）

