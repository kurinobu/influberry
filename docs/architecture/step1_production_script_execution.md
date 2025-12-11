# Step 1: 本番環境スクリプト実行手順書

**作成日**: 2025年11月2日  
**対象**: 本番環境（Render.com）でのスクリプト実行

---

## 📋 実行前確認事項

### 1. マイグレーション完了確認

- [ ] マイグレーション実行完了確認（`flask db current` で確認）
- [ ] テーブル作成確認（`\dt monthly*` で確認）

### 2. データ状況確認

- [ ] `monthly_summary`テーブルが空であることを確認
- [ ] ユーザー数と履歴データの存在確認

### 3. 実行タイミング

- [ ] **メンテナンス時間帯推奨**（サービスへの影響最小化）
- [ ] 実行時間の見積もり（ユーザー数×月数に依存）

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

### Step 2: スクリプトファイルの確認

```bash
# スクリプトファイルの存在確認
ls -la scripts/populate_monthly_summary.py

# 実行権限の確認
chmod +x scripts/populate_monthly_summary.py
```

### Step 3: データ状況確認（実行前）

```bash
# monthly_summaryテーブルの状態確認
psql $DATABASE_URL -c "SELECT COUNT(*) FROM monthly_summary;"
# 期待: 0件

# ユーザー数確認
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"

# 履歴データ確認
psql $DATABASE_URL -c "SELECT COUNT(*) FROM project_status_history;"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM invoice_status_history;"

# 履歴データの月範囲確認
psql $DATABASE_URL -c "SELECT MIN(DATE_TRUNC('month', changed_at)) as min_month, MAX(DATE_TRUNC('month', changed_at)) as max_month FROM project_status_history;"
psql $DATABASE_URL -c "SELECT MIN(DATE_TRUNC('month', changed_at)) as min_month, MAX(DATE_TRUNC('month', changed_at)) as max_month FROM invoice_status_history;"
```

### Step 4: テスト実行（推奨：特定ユーザーのみ）

```bash
# 特定ユーザーのみ実行（テスト用）
python scripts/populate_monthly_summary.py --user-id 2

# 実行結果確認
psql $DATABASE_URL -c "SELECT COUNT(*) FROM monthly_summary WHERE user_id = 2;"

# データ内容確認
psql $DATABASE_URL -c "SELECT user_id, summary_month, acquired_projects, completed_projects, sent_invoices_amount FROM monthly_summary WHERE user_id = 2 ORDER BY summary_month DESC LIMIT 5;"
```

### Step 5: 全ユーザー実行（テスト成功後）

```bash
# 全ユーザーのデータ投入
python scripts/populate_monthly_summary.py

# 実行中は進捗が表示されます:
# - ユーザーごとの処理進捗
# - 成功/エラー件数
# - 追加されたレコード数
```

### Step 6: 実行後確認

```bash
# データ投入確認
psql $DATABASE_URL -c "SELECT COUNT(*) FROM monthly_summary;"
# 期待: 0より大きい値（ユーザー数×月数に依存）

# ユーザーごとのレコード数確認
psql $DATABASE_URL -c "SELECT user_id, COUNT(*) as record_count FROM monthly_summary GROUP BY user_id ORDER BY user_id;"

# 最新3件の確認
psql $DATABASE_URL -c "SELECT user_id, summary_month, acquired_projects, completed_projects, sent_invoices_amount FROM monthly_summary ORDER BY summary_month DESC LIMIT 3;"

# 月ごとのレコード数確認
psql $DATABASE_URL -c "SELECT summary_month, COUNT(*) as record_count FROM monthly_summary GROUP BY summary_month ORDER BY summary_month DESC LIMIT 10;"
```

---

## 📊 期待される結果

### データ投入前

- `monthly_summary`テーブル: 0件

### データ投入後

- `monthly_summary`テーブル: ユーザー数×月数件（おおよそ）
- 各ユーザーごとに過去24ヶ月分のデータ（履歴がある場合）

### 実行時間見積もり

- **1ユーザーあたり**: 約1-3分（月数に依存）
- **全ユーザー**: ユーザー数×1-3分
- **例**: 10ユーザーの場合、約10-30分

---

## ✅ 実行後確認

### 確認項目

- [x] スクリプト実行完了（エラーなし）
- [x] データ投入確認（`monthly_summary`テーブルにレコードが存在）
- [x] データ内容確認（各月の統計データが正しく記録されている）
- [x] エラーログの確認（実行時のログ確認）

### データ検証（オプション）

```bash
# 特定ユーザーのデータ検証
psql $DATABASE_URL -c "
SELECT 
    user_id,
    summary_month,
    acquired_projects,
    completed_projects,
    sent_invoices_count,
    sent_invoices_amount,
    paid_invoices_count,
    paid_invoices_amount
FROM monthly_summary
WHERE user_id = 2
ORDER BY summary_month DESC
LIMIT 5;
"
```

---

## ⚠️ エラー時の対応

### エラー1: スクリプトが見つからない

**対応**:
```bash
# プロジェクトルートに移動
cd /opt/render/project/src  # Render.comのプロジェクトパスに調整

# スクリプトファイルの確認
ls -la scripts/populate_monthly_summary.py
```

### エラー2: モジュールインポートエラー

**対応**:
```bash
# Python環境の確認
python --version

# 必要なパッケージの確認
pip list | grep flask

# Flaskアプリのインポート確認
python -c "from app import create_app; app = create_app('production'); print('OK')"
```

### エラー3: データベース接続エラー

**対応**:
```bash
# 環境変数の確認
echo $DATABASE_URL

# データベース接続確認
psql $DATABASE_URL -c "SELECT version();"
```

### エラー4: 実行中のエラー

**対応**:
1. エラーメッセージを確認
2. エラーが発生したユーザーIDを記録
3. 該当ユーザーのみ再実行
   ```bash
   python scripts/populate_monthly_summary.py --user-id <user_id>
   ```

---

## 🔄 ロールバック（必要に応じて）

### データの削除（実行失敗時）

```bash
# ⚠️ 注意: この操作は全てのデータを削除します
psql $DATABASE_URL -c "TRUNCATE TABLE monthly_summary;"

# 特定ユーザーのみ削除する場合
psql $DATABASE_URL -c "DELETE FROM monthly_summary WHERE user_id = <user_id>;"
```

---

## 📝 実行ログ記録

実行時に以下の情報を記録してください：

- 実行日時
- 実行前のデータ件数
- 実行後のデータ件数
- 実行時間
- エラーログ（発生した場合）
- 処理したユーザー数とレコード数

---

**作成日**: 2025年11月2日  
**状態**: 実行準備完了

