# Step 1: 本番環境マイグレーション実行手順書

**作成日**: 2025年11月2日  
**対象**: 本番環境（Render.com）でのマイグレーション実行

---

## 📋 実行前確認事項

### 1. デプロイ完了確認

- [ ] Render.com Dashboardでデプロイ完了を確認
- [ ] 本番環境（https://influberry.jp）が正常に動作していることを確認

### 2. バックアップ確認

- [ ] データベースバックアップの確認（推奨）
- [ ] ロールバック手順の確認

---

## 🔧 実行手順

### Step 1: Render.com Shellに接続

1. **Render.com Dashboardにアクセス**
   - https://dashboard.render.com

2. **本番環境のサービスを選択**
   - InfluBerry 本番環境のサービスを選択

3. **Shellに接続**
   - 左メニューから「Shell」を選択
   - 「Connect」をクリック

### Step 2: 現在のマイグレーション状態確認

```bash
# 現在のマイグレーションバージョンを確認
flask db current

# 期待される結果（マイグレーション未実行の場合）:
# 97f40bb745e2 または それ以前のバージョン
```

### Step 3: 実行予定のマイグレーション確認

```bash
# 実行予定のマイグレーションを確認
flask db heads

# 期待される結果:
# 251101092000 (最新)
```

### Step 4: マイグレーション実行

```bash
# マイグレーション実行
flask db upgrade

# 実行結果を確認
# 以下のマイグレーションが順次実行される:
# 1. f59971728522_add_monthly_management_tables.py
# 2. 264c518cdcf3_add_monthly_snapshot_model.py
# 3. 251031101032_add_monthly_summary_table.py
# 4. 251101092000_add_index_to_invoice_payment_date.py
```

### Step 5: マイグレーション確認

```bash
# マイグレーション状態再確認
flask db current

# 期待される結果:
# 251101092000 (head)

# テーブル確認
psql $DATABASE_URL -c "\dt monthly*"

# 期待されるテーブル:
# - monthly_targets
# - project_status_history
# - invoice_status_history
# - monthly_snapshots
# - monthly_summary
```

### Step 6: テーブル構造確認（オプション）

```bash
# monthly_summaryテーブルの構造確認
psql $DATABASE_URL -c "\d monthly_summary"

# インデックスの確認
psql $DATABASE_URL -c "\di monthly_summary*"
```

---

## ✅ 実行後確認

### 確認項目

- [x] マイグレーション実行完了（`flask db current` で確認）
- [x] 全てのテーブルが作成されている（`\dt monthly*` で確認）
- [x] エラーログがない（マイグレーション実行時のログ確認）

### 期待される結果

- **マイグレーションバージョン**: `251101092000`
- **作成されたテーブル**: 5つ（monthly_targets, project_status_history, invoice_status_history, monthly_snapshots, monthly_summary）

---

## ⚠️ エラー時の対応

### エラー1: マイグレーションが実行できない

**原因**: データベース接続エラー

**対応**:
```bash
# 環境変数の確認
echo $DATABASE_URL

# データベース接続確認
psql $DATABASE_URL -c "SELECT version();"
```

### エラー2: テーブルが既に存在する

**原因**: 過去にマイグレーションが実行されている

**対応**:
```bash
# 現在のマイグレーション状態確認
flask db current

# 必要なマイグレーションのみ実行（通常は自動的に処理される）
flask db upgrade
```

### エラー3: マイグレーション実行中のエラー

**対応**:
1. エラーメッセージを確認
2. 必要に応じてロールバック
   ```bash
   flask db downgrade -1
   ```
3. 問題を解決してから再実行

---

## 📝 実行ログ記録

実行時に以下の情報を記録してください：

- 実行日時
- 実行前のマイグレーションバージョン
- 実行後のマイグレーションバージョン
- エラーログ（発生した場合）
- 作成されたテーブル一覧

---

**作成日**: 2025年11月2日  
**状態**: 実行準備完了

