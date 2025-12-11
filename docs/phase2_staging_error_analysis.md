# Phase 2 ステージング環境エラー 根本原因分析レポート

## 📋 目次
1. [テスト結果のサマリー](#1-テスト結果のサマリー)
2. [根本原因の特定](#2-根本原因の特定)
3. [問題の詳細分析](#3-問題の詳細分析)
4. [対応方法の提案](#4-対応方法の提案)

---

## 1. テスト結果のサマリー

### 1.1 テスト結果の確認項目

| 調査項目 | 結果 | 判定 |
|---------|------|------|
| **MonthlySummaryインポート** | ✅ OK | **正常** |
| **データベース接続** | ✅ OK | **正常** |
| **Blueprint登録** | ✅ OK (`monthly_current`登録済み) | **正常** |
| **ルーティング** | ✅ OK (`/api/monthly/current`存在) | **正常** |
| **monthly_summaryテーブル** | ❌ **存在しない** | **問題** |
| **エンドポイント動作** | ❌ **500エラー** | **問題** |

### 1.2 エラーメッセージ

```
relation "monthly_summary" does not exist
LINE 2: FROM monthly_summary 
             ^
```

**エラーコード**: `psycopg2.errors.UndefinedTable`

---

## 2. 根本原因の特定

### 2.1 根本原因

✅ **特定完了**: `monthly_summary`テーブルがステージング環境のデータベースに**存在しない**

### 2.2 エラー発生の流れ

1. フロントエンドから `/api/monthly/current` にリクエスト
2. `app/blueprints/monthly_current.py` の `get_current_monthly_data()` 関数が実行
3. 192行目で `MonthlySummary.get_by_user_and_month(user_id, month_date.date())` を呼び出し
4. SQLAlchemyが `monthly_summary` テーブルに対してクエリを実行
5. **PostgreSQLが `relation "monthly_summary" does not exist` エラーを返す**
6. 例外が発生し、500エラーとして返される

### 2.3 コードの該当箇所

```python
# app/blueprints/monthly_current.py 192行目
summary = MonthlySummary.get_by_user_and_month(user_id, month_date.date())
```

この行で、存在しないテーブルにアクセスしようとしてエラーが発生しています。

---

## 3. 問題の詳細分析

### 3.1 テーブル存在確認の結果

**サーバーシェルコマンドの結果**:
```
✅ データベース接続: OK
テーブル一覧: ['invoice_status_history', 'projects', 'users', 'monthly_snapshots', 'alembic_version', 'invoices', 'monthly_targets', 'project_status_history']...
❌ monthly_summaryテーブル: 存在しない
⚠️ マイグレーションが必要かもしれません
```

**確認されたテーブル**:
- `invoice_status_history` ✅
- `projects` ✅
- `users` ✅
- `monthly_snapshots` ✅
- `alembic_version` ✅
- `invoices` ✅
- `monthly_targets` ✅
- `project_status_history` ✅
- **`monthly_summary`** ❌ **存在しない**

### 3.2 エンドポイントテストの結果

**エラーメッセージ全文**:
```
ステータスコード: 500
❌ エンドポイント: エラー (500)
レスポンス: {
  "error": "(psycopg2.errors.UndefinedTable) relation \"monthly_summary\" does not exist\nLINE 2: FROM monthly_summary \n             ^\n\n[SQL: SELECT monthly_summary.id AS monthly_summary_id, monthly_summary.user_id AS monthly_summary_user_id, monthly_summary.summary_month AS monthly_summary_summary_month, monthly_summary.acquired_projects AS monthly_summary_acquired_projects, monthly_summary.completed_projects AS monthly_summary_completed_projects, monthly_summary.sent_invoices_count AS mon
```

### 3.3 正常動作している項目

#### ✅ MonthlySummaryクラスのインポート
```
✅ MonthlySummaryインポート: OK
クラス: <class 'app.models.monthly_summary.MonthlySummary'>
get_by_user_and_monthメソッド存在: True
```

#### ✅ Blueprint登録
```
✅ Flaskアプリケーション作成: OK
Blueprint一覧: [..., 'monthly_current', ...]
✅ monthly_current Blueprint: 登録済み
登録済みルート:
  /api/monthly/current -> monthly_current.get_current_monthly_data
```

#### ✅ データベース接続
- PostgreSQLへの接続は正常
- 他のテーブルへのアクセスは正常

---

## 4. 対応方法の提案

### 4.1 対応方法の優先順位

#### 方法1: マイグレーションを実行してテーブルを作成（推奨）

**理由**:
- 計画書v2.0で定義された `monthly_summary` テーブルは、Phase 3で使用される重要な機能
- テーブルが存在することで、事前集計機能が正常に動作する
- 根本的な解決方法

**手順**:
1. マイグレーションファイルの確認
2. ステージング環境でマイグレーションを実行
3. テーブル作成の確認

#### 方法2: エラーハンドリングの改善（暫定対応）

**理由**:
- テーブルが存在しない場合でも、フォールバック処理（リアルタイム計算）が動作するようにする
- マイグレーション実行までの暫定対応として有効

**手順**:
1. `monthly_current.py` の192行目付近で、テーブル不存在エラーをキャッチ
2. エラー発生時は自動的にフォールバック処理（`calculate_monthly_stats`）を実行
3. エラーログを記録して、マイグレーションが必要であることを通知

### 4.2 推奨される対応手順

#### Step 1: マイグレーションファイルの確認

```bash
# マイグレーションファイルを確認
ls -la migrations/versions/ | grep monthly_summary
```

#### Step 2: マイグレーションの実行

```bash
# ステージング環境でマイグレーションを実行
flask db upgrade
```

#### Step 3: テーブル作成の確認

```bash
# テーブルが作成されたことを確認
python3 -c "
from app import create_app, db
from sqlalchemy import inspect
app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    if 'monthly_summary' in tables:
        print('✅ monthly_summaryテーブル: 作成完了')
    else:
        print('❌ monthly_summaryテーブル: まだ存在しない')
"
```

#### Step 4: エラーハンドリングの改善（オプション）

テーブルが存在しない場合のエラーハンドリングを改善して、フォールバック処理を確実に動作させる。

---

## 5. 結論

### 5.1 根本原因

✅ **特定完了**: `monthly_summary`テーブルがステージング環境のデータベースに存在しない

### 5.2 影響範囲

- **新API (`/api/monthly/current`)**: 500エラーが発生
- **フォールバック機能**: エラー発生により動作しない（テーブル不存在エラーで例外が発生）

### 5.3 対応の優先順位

1. **緊急**: マイグレーションを実行してテーブルを作成
2. **改善**: エラーハンドリングを改善して、テーブル不存在時でもフォールバック処理が動作するようにする

### 5.4 次のアクション

1. **マイグレーションファイルの確認**: `monthly_summary` テーブル作成用のマイグレーションが存在するか確認
2. **マイグレーションの実行**: ステージング環境でマイグレーションを実行
3. **再テスト**: マイグレーション実行後にエンドポイントの動作を確認

---

**作成日時**: 2025-10-31
**分析者**: AI Assistant


