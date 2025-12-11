# Step 1: 本番環境実行手順（コピペ実行用）

**作成日**: 2025年11月2日  
**用途**: Render.com Shellでコピペ実行用

---

## 📋 実行前の確認

### 1. Render.com Shellに接続
1. Render.com Dashboard → 本番環境サービス → Shell → Connect

### 2. プロジェクトディレクトリに移動（必要に応じて）
```bash
cd /opt/render/project/src || pwd
```

---

## Phase 1: マイグレーション実行

### Step 1-1: 現在のマイグレーション状態確認

```bash
flask db current
```

**期待される結果**: `97f40bb745e2` またはそれ以前のバージョン

---

### Step 1-2: 実行予定のマイグレーション確認

```bash
flask db heads
```

**期待される結果**: `251101092000` (head)

---

### Step 1-3: データベース接続確認

```bash
psql $DATABASE_URL -c "SELECT version();"
```

**期待される結果**: PostgreSQLのバージョン情報が表示される

---

### Step 1-4: マイグレーション実行

```bash
flask db upgrade
```

**実行内容**: 以下のマイグレーションが順次実行されます
- `f59971728522_add_monthly_management_tables.py`
- `264c518cdcf3_add_monthly_snapshot_model.py`
- `251031101032_add_monthly_summary_table.py`
- `251101092000_add_index_to_invoice_payment_date.py`

**実行時間**: 約1-2分

---

### Step 1-5: マイグレーション実行後確認

```bash
flask db current
```

**期待される結果**: `251101092000` (head)

---

### Step 1-6: テーブル作成確認

```bash
psql $DATABASE_URL -c "\dt monthly*"
```

**期待される結果**: 以下のテーブルが表示される
- `monthly_targets`
- `project_status_history`
- `invoice_status_history`
- `monthly_snapshots`
- `monthly_summary`

---

### Step 1-7: monthly_summaryテーブル構造確認（オプション）

```bash
psql $DATABASE_URL -c "\d monthly_summary"
```

---

## Phase 2: スクリプト実行準備

### Step 2-1: スクリプトファイルの確認

```bash
ls -la scripts/populate_monthly_summary.py
```

**期待される結果**: ファイルが存在することを確認

---

### Step 2-2: 実行権限の付与

```bash
chmod +x scripts/populate_monthly_summary.py
```

---

### Step 2-3: データ状況確認（実行前）

```bash
psql $DATABASE_URL -c "SELECT COUNT(*) FROM monthly_summary;"
```

**期待される結果**: `0` (データ未投入)

---

### Step 2-4: ユーザー数確認

```bash
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"
```

**期待される結果**: ユーザー数が表示される

---

### Step 2-5: 履歴データ確認

```bash
psql $DATABASE_URL -c "SELECT COUNT(*) FROM project_status_history;"
```

```bash
psql $DATABASE_URL -c "SELECT COUNT(*) FROM invoice_status_history;"
```

---

## Phase 3: スクリプト実行（テスト実行）

### Step 3-1: テスト実行（特定ユーザーのみ）

⚠️ **推奨**: まず1ユーザーでテスト実行して問題がないか確認

```bash
python scripts/populate_monthly_summary.py --user-id 2
```

**実行時間**: 約1-3分（月数に依存）

**出力**: 進捗情報が表示されます

---

### Step 3-2: テスト実行結果確認

```bash
psql $DATABASE_URL -c "SELECT COUNT(*) FROM monthly_summary WHERE user_id = 2;"
```

**期待される結果**: 0より大きい値（月数に依存）

---

### Step 3-3: テスト実行データ内容確認

```bash
psql $DATABASE_URL -c "SELECT user_id, summary_month, acquired_projects, completed_projects, sent_invoices_amount FROM monthly_summary WHERE user_id = 2 ORDER BY summary_month DESC LIMIT 5;"
```

**期待される結果**: 月次サマリーデータが表示される

---

## Phase 4: スクリプト実行（全ユーザー）

### Step 4-1: 全ユーザー実行

⚠️ **注意**: テスト実行が成功したことを確認してから実行

```bash
python scripts/populate_monthly_summary.py
```

**実行時間**: ユーザー数×1-3分（月数に依存）
- 例: 10ユーザーの場合、約10-30分

**出力**: 
- ユーザーごとの進捗情報
- 成功/エラー件数
- 追加されたレコード数

---

### Step 4-2: 実行後データ確認

```bash
psql $DATABASE_URL -c "SELECT COUNT(*) FROM monthly_summary;"
```

**期待される結果**: 0より大きい値（ユーザー数×月数に依存）

---

### Step 4-3: ユーザーごとのレコード数確認

```bash
psql $DATABASE_URL -c "SELECT user_id, COUNT(*) as record_count FROM monthly_summary GROUP BY user_id ORDER BY user_id;"
```

**期待される結果**: 各ユーザーごとのレコード数が表示される

---

### Step 4-4: 最新データ確認

```bash
psql $DATABASE_URL -c "SELECT user_id, summary_month, acquired_projects, completed_projects, sent_invoices_amount FROM monthly_summary ORDER BY summary_month DESC LIMIT 3;"
```

---

### Step 4-5: 月ごとのレコード数確認

```bash
psql $DATABASE_URL -c "SELECT summary_month, COUNT(*) as record_count FROM monthly_summary GROUP BY summary_month ORDER BY summary_month DESC LIMIT 10;"
```

---

## Phase 5: 動作確認

### Step 5-1: 本番環境での表示確認

**ブラウザで確認**:
- URL: https://influberry.jp/dashboard
- 月次管理セクションが表示されることを確認
- 「概要」タブが優先表示されることを確認

---

### Step 5-2: データ検証（オプション）

```bash
psql $DATABASE_URL -c "SELECT user_id, summary_month, acquired_projects, completed_projects, sent_invoices_count, sent_invoices_amount, paid_invoices_count, paid_invoices_amount FROM monthly_summary WHERE user_id = 2 ORDER BY summary_month DESC LIMIT 5;"
```

---

## 🔄 エラー時の対応

### マイグレーションエラー時

```bash
# マイグレーション状態確認
flask db current

# エラーが発生した場合、1つ前のマイグレーションに戻す（必要に応じて）
flask db downgrade -1
```

---

### スクリプトエラー時

```bash
# エラーが発生したユーザーIDを確認
# エラーログから user_id を特定

# 特定ユーザーのみ再実行
python scripts/populate_monthly_summary.py --user-id <user_id>
```

---

### データの削除（実行失敗時）

⚠️ **注意**: この操作は全てのデータを削除します

```bash
# 全データ削除
psql $DATABASE_URL -c "TRUNCATE TABLE monthly_summary;"

# 特定ユーザーのみ削除（例: user_id = 2）
psql $DATABASE_URL -c "DELETE FROM monthly_summary WHERE user_id = 2;"
```

---

## 📝 実行ログ記録用テンプレート

実行時に以下の情報を記録してください：

```
【実行日時】: 
【実行者】: 
【Phase 1 - マイグレーション実行前】: flask db current = 
【Phase 1 - マイグレーション実行後】: flask db current = 
【Phase 1 - 作成されたテーブル】: 
【Phase 2 - 実行前データ件数】: 
【Phase 4 - 実行後データ件数】: 
【Phase 4 - 実行時間】: 
【エラー】: （発生した場合）
【備考】: 
```

---

**作成日**: 2025年11月2日  
**状態**: 実行準備完了

