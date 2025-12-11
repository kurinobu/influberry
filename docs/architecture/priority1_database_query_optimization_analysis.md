# 優先度1: データベースクエリの最適化 完全調査分析レポート

**作成日**: 2025年11月1日  
**優先度**: 🔴 緊急  
**対象**: InfluBerry 月次管理機能  
**目的**: データベースクエリの最適化によるAPIレスポンスタイムの改善（目標: < 500ms → 現在: 6-17秒）

---

## 1. 現状把握と問題定義

### 1.1 パフォーマンス指標（ステージング環境・2025年11月1日計測）

| 指標 | 目標値 | 現状値 | 差分 | 評価 |
|------|--------|--------|------|------|
| **APIレスポンスタイム** | < 500ms | **6-17秒** | **12-34倍遅い** | ❌ **深刻** |
| **Finish Time** | < 2秒 | **59.26秒** | **約30倍遅い** | ❌ **深刻** |
| **Load Time** | < 800ms | **1.20秒** | **1.5倍遅い** | ⚠️ **改善余地あり** |
| **DOMContentLoaded** | < 800ms | **589ms** | **目標達成** | ✅ |

### 1.2 影響を受けているAPIエンドポイント

| APIエンドポイント | レスポンスタイム | 呼び出し頻度 | 影響度 |
|------------------|----------------|------------|--------|
| `/api/monthly/current` | **15.55秒** | 1回/ページロード | 🔴 **極めて高い** |
| `/api/monthly-stats/overview` | **6.22秒** | 1回/ページロード | 🔴 **高い** |
| `/api/monthly-targets/?year=2025&months=9` | **17.07秒** | 1回/ページロード | 🔴 **極めて高い** |

### 1.3 問題の影響範囲

- **ユーザー体験**: ページ表示に約1分かかるため、実用性が著しく低下
- **ビジネス影響**: ユーザー離脱リスク、サービス評価の低下
- **システム負荷**: データベースへの過剰な負荷、リソース消費

---

## 2. 根本原因の詳細分析

### 2.1 問題点1: `extract()`関数によるインデックス無効化

#### 現状の問題コード

```46:59:app/blueprints/monthly_current.py
def calculate_monthly_stats(user_id, year, month):
    """
    月次統計を計算（正負集計ロジック対応）
    """
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
```

#### 問題の詳細

1. **インデックスが効かない**
   - `extract('year', changed_at)`と`extract('month', changed_at)`の使用により、`changed_at`にインデックスがあっても使用されない
   - PostgreSQLでは関数を使った条件ではインデックスが効かない（関数インデックスを作成していない限り）
   - **全テーブルスキャンまたはシーケンシャルスキャンが発生**

2. **発生箇所**
   - `calculate_monthly_stats()`関数内で8回使用
   - `monthly_summary_updater.py`の各計算関数で使用
   - `monthly_stats.py`の各エンドポイントで使用

3. **影響度**
   - **極めて高い**: データ量に比例してクエリ時間が線形に増加
   - 1万件の履歴データがある場合、各クエリが数秒かかる可能性

#### 確認済みインデックス状況

| テーブル | カラム | インデックス有無 | 状況 |
|---------|--------|----------------|------|
| `project_status_history` | `changed_at` | ✅ **あり** | しかし`extract()`により無効化 |
| `project_status_history` | `project_id` | ✅ **あり** | 有効 |
| `invoice_status_history` | `changed_at` | ✅ **あり** | しかし`extract()`により無効化 |
| `invoice_status_history` | `invoice_id` | ✅ **あり** | 有効 |
| `invoice` | `payment_date` | ❌ **なし** | インデックス追加が必要 |

### 2.2 問題点2: 複数回の個別クエリ実行

#### 現状のクエリ実行パターン

`calculate_monthly_stats()`関数内で以下のクエリが**個別に実行**されている:

1. 獲得案件数（正）: 1クエリ
2. 獲得案件数（負）: 1クエリ
3. 完了案件数（正）: 1クエリ
4. 完了案件数（負）: 1クエリ
5. 送信済み請求書（正）: 1クエリ
6. 送信済み請求書（負）: 1クエリ
7. 支払済み請求書: 1クエリ

**合計: 7クエリが個別に実行される**

#### 問題の詳細

1. **ネットワーク往復時間の増加**
   - 各クエリごとにデータベースへの往復が発生
   - レイテンシの累積により、全体の実行時間が増加

2. **データベース接続の負荷**
   - 複数のクエリが順次実行されるため、接続リソースを長時間占有
   - ステージング環境（Render.comフリープラン）では接続数制限があるため、他のリクエストに影響

3. **トランザクション管理の非効率性**
   - 各クエリが独立して実行されるため、一貫性チェックが都度行われる

### 2.3 問題点3: JOIN処理の非効率性

#### 現状のJOIN処理

```51:59:app/blueprints/monthly_current.py
    acquired_positive = db.session.query(
        func.count(func.distinct(ProjectStatusHistory.project_id))
    ).join(Project).filter(
        Project.user_id == user_id,
        ProjectStatusHistory.old_status == 'proposed',
        ProjectStatusHistory.new_status == 'contracted',
        extract('year', ProjectStatusHistory.changed_at) == year,
        extract('month', ProjectStatusHistory.changed_at) == month
    ).scalar() or 0
```

#### 問題の詳細

1. **JOINの順序**
   - `ProjectStatusHistory` → `Project` のJOINが実行される
   - `Project.user_id`でフィルタリングしているが、JOIN後にフィルタリングしているため非効率

2. **インデックスの活用不足**
   - `Project.user_id`にはインデックスがあるが、JOIN条件ではなくフィルタ条件として使用
   - JOINの最適化がデータベースエンジンに委ねられている

### 2.4 問題点4: 事前集計テーブルの未活用

#### 現状の実装

```191:211:app/blueprints/monthly_current.py
            # 統計取得（事前集計テーブル優先）
            summary = MonthlySummary.get_by_user_and_month(user_id, month_date.date())
            if summary:
                # 事前集計テーブルから高速取得
                stats = {
                    'acquired_projects': summary.acquired_projects,
                    'completed_projects': summary.completed_projects,
                    'sent_invoices_count': summary.sent_invoices_count,
                    'sent_invoices_amount': float(summary.sent_invoices_amount),
                    'paid_invoices_count': summary.paid_invoices_count,
                    'paid_invoices_amount': float(summary.paid_invoices_amount),
                    'overdue_invoices_count': summary.overdue_invoices_count,
                    'overdue_invoices_amount': float(summary.overdue_invoices_amount)
                }
            else:
                # フォールバック: リアルタイム計算
                stats = calculate_monthly_stats(
                    user_id,
                    month_date.year,
                    month_date.month
                )
```

#### 問題の詳細

1. **データが存在しない場合のパフォーマンス低下**
   - `MonthlySummary`テーブルにデータが存在しない場合、`calculate_monthly_stats()`が実行される
   - ステージング環境ではデータが古い、または存在しない可能性が高い

2. **更新タイミングの問題**
   - ステータス変更時に自動更新されるが、初期データがない場合にフォールバックが実行される
   - 月次切り替え時にスナップショットが作成されるが、ステージング環境では実行されていない可能性

---

## 3. 修正案の詳細設計

### 3.1 修正案1: 日付範囲クエリへの変更（最優先・即効性あり）

#### 目的
`extract()`関数の使用をやめ、日付範囲でのフィルタリングに変更することでインデックスを有効活用

#### 実装内容

**変更前**:
```python
extract('year', ProjectStatusHistory.changed_at) == year,
extract('month', ProjectStatusHistory.changed_at) == month
```

**変更後**:
```python
from datetime import date
month_start = date(year, month, 1)
if month == 12:
    month_end = date(year + 1, 1, 1)
else:
    month_end = date(year, month + 1, 1)

ProjectStatusHistory.changed_at >= month_start,
ProjectStatusHistory.changed_at < month_end
```

#### 期待効果

- **インデックス活用**: `changed_at`のインデックスが有効に使用される
- **クエリ速度**: O(n) → O(log n)に改善（n: データ総数）
- **改善率**: **50-90%の速度改善が期待できる**

#### リスク

- **低リスク**: 既存のロジックを変更しないため、結果の整合性は保たれる
- **互換性**: PostgreSQLとSQLiteの両方で動作する

### 3.2 修正案2: 複数クエリの統合（高優先）

#### 目的
個別に実行されている7つのクエリを、可能な限り統合して実行回数を削減

#### 実装内容

**変更前**（7クエリ個別実行）:
```python
# 獲得案件数（正）
acquired_positive = db.session.query(...).scalar() or 0
# 獲得案件数（負）
acquired_negative = db.session.query(...).scalar() or 0
# 完了案件数（正）
completed_positive = db.session.query(...).scalar() or 0
# ... (合計7クエリ)
```

**変更後**（1クエリで集計）:
```python
from sqlalchemy import case

result = db.session.query(
    func.count(func.distinct(
        case(
            (and_(
                ProjectStatusHistory.old_status == 'proposed',
                ProjectStatusHistory.new_status == 'contracted'
            ), ProjectStatusHistory.project_id),
            else_=None
        )
    )).label('acquired_positive'),
    func.count(func.distinct(
        case(
            (and_(
                ProjectStatusHistory.old_status == 'contracted',
                ProjectStatusHistory.new_status == 'proposed'
            ), ProjectStatusHistory.project_id),
            else_=None
        )
    )).label('acquired_negative'),
    # ... 他の集計も同様に
).join(Project).filter(
    Project.user_id == user_id,
    ProjectStatusHistory.changed_at >= month_start,
    ProjectStatusHistory.changed_at < month_end
).first()
```

#### 期待効果

- **クエリ実行回数**: 7回 → 1回（**85.7%削減**）
- **ネットワーク往復**: 7回 → 1回（**85.7%削減**）
- **改善率**: **30-50%の速度改善が期待できる**

#### リスク

- **中リスク**: クエリが複雑になるため、可読性が低下する可能性
- **テスト**: 既存のロジックとの整合性確認が必要

### 3.3 修正案3: Invoice.payment_dateへのインデックス追加（中優先）

#### 目的
支払済み請求書の集計時に`Invoice.payment_date`でフィルタリングしているが、インデックスがないため追加

#### 実装内容

**マイグレーションファイル作成**:
```python
def upgrade():
    op.create_index('ix_invoice_payment_date', 'invoices', ['payment_date'], unique=False)

def downgrade():
    op.drop_index('ix_invoice_payment_date', 'invoices')
```

#### 期待効果

- **クエリ速度**: `payment_date`でのフィルタリングが高速化
- **改善率**: **20-40%の速度改善が期待できる**

#### リスク

- **低リスク**: インデックス追加のみで、既存ロジックに影響なし
- **ストレージ**: インデックスの追加により若干のストレージ消費増加（軽微）

### 3.4 修正案4: 事前集計テーブルのデータ確認と更新（中優先）

#### 目的
`MonthlySummary`テーブルのデータが最新であることを確認し、古い場合は更新処理を実行

#### 実装内容

**データ確認スクリプト**:
```python
def check_and_update_monthly_summary(user_id):
    """MonthlySummaryテーブルのデータを確認し、必要に応じて更新"""
    from datetime import datetime
    now = datetime.now()
    current_month = datetime(now.year, now.month, 1)
    
    # 直近3ヶ月のデータ確認
    for i in range(3):
        month_date = current_month - relativedelta(months=i)
        summary = MonthlySummary.get_by_user_and_month(user_id, month_date.date())
        
        if not summary:
            # データがない場合は更新
            update_monthly_summary(user_id, month_date)
        elif summary.last_updated_at < month_date:
            # データが古い場合は更新
            update_monthly_summary(user_id, month_date)
```

#### 期待効果

- **フォールバック回避**: リアルタイム計算が実行される頻度を削減
- **改善率**: データが存在する場合、**90%以上の速度改善**

#### リスク

- **低リスク**: 既存のロジックを使用するため、安全性が高い
- **実行タイミング**: バックグラウンドジョブまたは手動実行が必要

---

## 4. 競合・干渉リスク分析

### 4.1 既存機能への影響

#### 影響を受ける可能性のある機能

1. **案件管理機能** (`app/blueprints/projects.py`)
   - **影響**: なし（読み取り専用のクエリ変更のみ）
   - **リスク**: 低

2. **請求書管理機能** (`app/blueprints/invoices.py`)
   - **影響**: なし（読み取り専用のクエリ変更のみ）
   - **リスク**: 低

3. **月次統計API** (`app/blueprints/monthly_stats.py`)
   - **影響**: あり（同じクエリパターンを使用）
   - **リスク**: 中（修正案1-3を適用する必要がある）

4. **月次サマリー更新サービス** (`app/services/monthly_summary_updater.py`)
   - **影響**: あり（同じクエリパターンを使用）
   - **リスク**: 中（修正案1-3を適用する必要がある）

5. **月次切り替えスケジューラー** (`app/schedulers/monthly_rotation.py`)
   - **影響**: あり（同じクエリパターンを使用）
   - **リスク**: 中（修正案1-3を適用する必要がある）

#### 影響を受けない機能

- フロントエンド（APIレスポンス形式は変更しない）
- 他のAPIエンドポイント（月次管理機能以外）
- 認証・認可機能

### 4.2 データ整合性への影響

#### リスク分析

| 修正案 | データ整合性への影響 | リスク評価 |
|--------|-------------------|----------|
| 修正案1: 日付範囲クエリ | なし（同じ結果を返す） | ✅ **低リスク** |
| 修正案2: クエリ統合 | なし（同じ結果を返す） | ✅ **低リスク** |
| 修正案3: インデックス追加 | なし（読み取り専用） | ✅ **低リスク** |
| 修正案4: 事前集計更新 | あり（データ更新） | ⚠️ **中リスク**（既存ロジック使用） |

#### データ整合性チェック

修正後、以下の確認が必要:

1. **月次統計の計算結果の整合性**
   - 修正前後で同じ結果が返されることを確認
   - テストケース: 既存の月次統計データとの比較

2. **事前集計テーブルの整合性**
   - `MonthlySummary`テーブルのデータが正しく更新されることを確認
   - テストケース: ステータス変更後の自動更新確認

### 4.3 UIへの影響

#### 影響分析

- **レスポンス形式**: 変更なし（JSON形式は維持）
- **データ内容**: 変更なし（計算結果は同じ）
- **エラーハンドリング**: 変更なし（既存のエラーハンドリングを維持）

#### ユーザー体験への影響

- **改善**: ページ表示速度の大幅な改善（59秒 → 2秒以下を目標）
- **影響**: なし（既存のUI・UXは維持）

---

## 5. 実装計画と優先順位

### 5.1 実装順序（優先度順）

#### Phase 1: 即効性のある修正（優先度: 最高）

1. **修正案1: 日付範囲クエリへの変更**
   - **対象ファイル**:
     - `app/blueprints/monthly_current.py`
     - `app/services/monthly_summary_updater.py`
     - `app/blueprints/monthly_stats.py`
     - `app/schedulers/monthly_rotation.py`
   - **期待効果**: 50-90%の速度改善
   - **実装時間**: 2-3時間
   - **テスト時間**: 1-2時間

2. **修正案3: Invoice.payment_dateへのインデックス追加**
   - **対象ファイル**: 新規マイグレーションファイル作成
   - **期待効果**: 20-40%の速度改善（支払済み請求書集計時）
   - **実装時間**: 30分
   - **テスト時間**: 30分

#### Phase 2: さらなる最適化（優先度: 高）

3. **修正案2: 複数クエリの統合**
   - **対象ファイル**: 同Phase 1
   - **期待効果**: 30-50%の速度改善
   - **実装時間**: 3-4時間
   - **テスト時間**: 2-3時間

#### Phase 3: データ整合性の確保（優先度: 中）

4. **修正案4: 事前集計テーブルのデータ確認と更新**
   - **対象ファイル**: 新規スクリプト作成
   - **期待効果**: データが存在する場合、90%以上の速度改善
   - **実装時間**: 1-2時間
   - **テスト時間**: 1時間

### 5.2 実装スケジュール（想定）

| フェーズ | 実装時間 | テスト時間 | 合計 | 開始時期 |
|---------|---------|-----------|------|---------|
| **Phase 1** | 2.5-3.5時間 | 1.5-2.5時間 | **4-6時間** | 即座 |
| **Phase 2** | 3-4時間 | 2-3時間 | **5-7時間** | Phase 1完了後 |
| **Phase 3** | 1-2時間 | 1時間 | **2-3時間** | Phase 2完了後 |
| **合計** | **6.5-9.5時間** | **4.5-6.5時間** | **11-16時間** | - |

---

## 6. テスト計画

### 6.1 単体テスト

#### テスト項目

1. **修正案1: 日付範囲クエリ**
   - 同じ月のデータで、修正前後で同じ結果が返されることを確認
   - 境界値テスト（月初日・月末日・月を跨ぐデータ）

2. **修正案2: クエリ統合**
   - 修正前後で同じ集計結果が返されることを確認
   - 空データ、大量データでの動作確認

3. **修正案3: インデックス追加**
   - インデックスが正しく作成されることを確認
   - クエリ実行計画でインデックスが使用されることを確認

4. **修正案4: 事前集計更新**
   - データが正しく更新されることを確認
   - 更新後の整合性チェック

### 6.2 統合テスト

#### テスト項目

1. **APIエンドポイントの動作確認**
   - `/api/monthly/current`の正常動作
   - `/api/monthly-stats/{year}/{month}`の正常動作
   - `/api/monthly-stats/overview`の正常動作

2. **パフォーマンステスト**
   - レスポンスタイムの測定（目標: < 500ms）
   - ローカル環境・ステージング環境での比較

3. **データ整合性テスト**
   - 既存データとの整合性確認
   - ステータス変更後の自動更新確認

### 6.3 ロールバック計画

#### ロールバック手順

1. **マイグレーションのロールバック**（修正案3）
   ```bash
   flask db downgrade
   ```

2. **コードのロールバック**（修正案1, 2）
   - Gitでコミット前の状態に戻す
   - バックアップファイルから復元（必要に応じて）

3. **確認**
   - 既存機能が正常に動作することを確認
   - パフォーマンス指標の確認

---

## 7. 期待される改善効果

### 7.1 パフォーマンス改善予測

| 修正案 | 改善率 | 改善後のレスポンスタイム（予測） |
|--------|--------|----------------------------|
| **修正案1: 日付範囲クエリ** | **50-90%** | **1.6-7.8秒** |
| **修正案2: クエリ統合** | **30-50%** | **0.8-5.5秒** |
| **修正案3: インデックス追加** | **20-40%** | **0.6-4.4秒** |
| **修正案4: 事前集計更新** | **90%以上** | **< 1秒**（データ存在時） |
| **合計（Phase 1-3適用）** | **80-95%** | **0.3-3秒** |

### 7.2 目標達成可能性

- **目標**: APIレスポンスタイム < 500ms
- **現状**: 6-17秒
- **予測**: Phase 1-3適用後、**0.3-3秒**（データ存在時は< 1秒）

**評価**: ⚠️ **目標達成には追加の最適化が必要な可能性がある**

ただし、**大幅な改善（80-95%）が期待できるため、実用性は大幅に向上**

---

## 8. 結論と推奨事項

### 8.1 結論

1. **根本原因**: `extract()`関数によるインデックス無効化が主な原因
2. **即効性**: 修正案1（日付範囲クエリ）で50-90%の改善が期待できる
3. **追加最適化**: 修正案2-4の適用により、さらなる改善が可能

### 8.2 推奨事項

#### 最優先で実施すべき修正

1. ✅ **修正案1: 日付範囲クエリへの変更**（即効性あり・低リスク）
2. ✅ **修正案3: Invoice.payment_dateへのインデックス追加**（低リスク・簡単実装）

#### 次に実施すべき修正

3. ✅ **修正案2: 複数クエリの統合**（中リスク・可読性低下に注意）
4. ✅ **修正案4: 事前集計テーブルのデータ確認と更新**（中リスク・既存ロジック使用）

### 8.3 リスク評価

| 修正案 | リスク | 推奨度 |
|--------|--------|--------|
| 修正案1 | ✅ 低 | ✅ **強く推奨** |
| 修正案2 | ⚠️ 中 | ✅ **推奨** |
| 修正案3 | ✅ 低 | ✅ **強く推奨** |
| 修正案4 | ⚠️ 中 | ✅ **推奨** |

### 8.4 次のステップ

1. **即座に開始**: Phase 1（修正案1, 3）の実装
2. **効果測定**: Phase 1完了後のパフォーマンス測定
3. **追加最適化**: 必要に応じてPhase 2-3を実施

---

**作成者**: AI Assistant  
**関連文書**: 
- `phase3_implementation_plan.md`
- `step2_phase4-3_staging_test_evaluation.md`
- `monthly_management_phase3_handover.md`

