# Step 1: 本番環境実行コマンド集

**作成日**: 2025年11月2日  
**用途**: 本番環境（Render.com Shell）での実行用コマンド集

---

## 📋 マイグレーション実行コマンド

### 実行前確認

```bash
# 現在のマイグレーションバージョン確認
flask db current

# 実行予定のマイグレーション確認
flask db heads

# データベース接続確認
psql $DATABASE_URL -c "SELECT version();"
```

### マイグレーション実行

```bash
# マイグレーション実行
flask db upgrade

# 実行後の確認
flask db current

# テーブル確認
psql $DATABASE_URL -c "\dt monthly*"
```

### テーブル構造確認

```bash
# monthly_summaryテーブルの構造確認
psql $DATABASE_URL -c "\d monthly_summary"

# インデックス確認
psql $DATABASE_URL -c "\di monthly_summary*"
```

---

## 📋 スクリプト実行コマンド

### 実行前確認

```bash
# スクリプトファイルの確認
ls -la scripts/populate_monthly_summary.py

# 実行権限の付与
chmod +x scripts/populate_monthly_summary.py

# データ状況確認
psql $DATABASE_URL -c "SELECT COUNT(*) FROM monthly_summary;"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM project_status_history;"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM invoice_status_history;"
```

### テスト実行（特定ユーザーのみ）

```bash
# 特定ユーザーのみ実行（テスト用）
python scripts/populate_monthly_summary.py --user-id 2

# 実行結果確認
psql $DATABASE_URL -c "SELECT COUNT(*) FROM monthly_summary WHERE user_id = 2;"
psql $DATABASE_URL -c "SELECT user_id, summary_month, acquired_projects, completed_projects, sent_invoices_amount FROM monthly_summary WHERE user_id = 2 ORDER BY summary_month DESC LIMIT 5;"
```

### 全ユーザー実行

```bash
# 全ユーザーのデータ投入
python scripts/populate_monthly_summary.py
```

### 実行後確認

```bash
# データ投入確認
psql $DATABASE_URL -c "SELECT COUNT(*) FROM monthly_summary;"

# ユーザーごとのレコード数確認
psql $DATABASE_URL -c "SELECT user_id, COUNT(*) as record_count FROM monthly_summary GROUP BY user_id ORDER BY user_id;"

# 最新3件の確認
psql $DATABASE_URL -c "SELECT user_id, summary_month, acquired_projects, completed_projects, sent_invoices_amount FROM monthly_summary ORDER BY summary_month DESC LIMIT 3;"

# 月ごとのレコード数確認
psql $DATABASE_URL -c "SELECT summary_month, COUNT(*) as record_count FROM monthly_summary GROUP BY summary_month ORDER BY summary_month DESC LIMIT 10;"
```

---

## 📋 動作確認コマンド

### API動作確認

```bash
# 軽量概要API確認（本番環境URLを使用）
curl -X GET "https://influberry.jp/api/monthly-stats/overview-minimal" \
  -H "Cookie: session=<session_cookie>"

# 統合API確認
curl -X GET "https://influberry.jp/api/monthly/current" \
  -H "Cookie: session=<session_cookie>"
```

### データ検証コマンド

```bash
# 特定ユーザーの詳細データ確認
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

# 月次サマリーの整合性チェック（オプション）
psql $DATABASE_URL -c "
SELECT 
    summary_month,
    COUNT(*) as user_count,
    SUM(acquired_projects) as total_acquired,
    SUM(completed_projects) as total_completed,
    SUM(sent_invoices_amount) as total_sent
FROM monthly_summary
GROUP BY summary_month
ORDER BY summary_month DESC
LIMIT 12;
"
```

---

## 🔄 ロールバックコマンド（緊急時）

### マイグレーションのロールバック

```bash
# 1つ前のマイグレーションに戻す
flask db downgrade -1

# 特定のマイグレーションに戻す
flask db downgrade <revision>
```

### スクリプトデータの削除

```bash
# ⚠️ 注意: 全てのデータを削除
psql $DATABASE_URL -c "TRUNCATE TABLE monthly_summary;"

# 特定ユーザーのみ削除
psql $DATABASE_URL -c "DELETE FROM monthly_summary WHERE user_id = <user_id>;"
```

---

## 📝 ログ確認コマンド

### アプリケーションログ

```bash
# Render.com Dashboard → Logs で確認
# または、Shellから（可能な場合）
tail -f /var/log/app.log  # パスは環境により異なる
```

### データベースログ

```bash
# データベースのクエリログ（PostgreSQL）
# Render.com Dashboard → Database → Logs で確認
```

---

## ⚠️ 注意事項

### 実行タイミング

- **マイグレーション**: デプロイ完了後、即座に実行
- **スクリプト**: マイグレーション実行後、即座に実行
- **推奨**: メンテナンス時間帯（サービスへの影響最小化）

### 実行前の確認

- [ ] デプロイ完了確認
- [ ] データベースバックアップ確認（推奨）
- [ ] 実行手順の確認

### 実行中の監視

- [ ] エラーログの監視
- [ ] 実行進捗の確認
- [ ] データベース負荷の監視

---

**作成日**: 2025年11月2日  
**状態**: 実行準備完了

