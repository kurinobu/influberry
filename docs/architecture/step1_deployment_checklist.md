# Step 1: main環境へのデプロイ準備 - 最終チェックリスト

**作成日**: 2025年11月2日  
**対象**: main環境へのデプロイ準備（月次管理機能Phase 3完了後）

---

## ✅ **完了確認項目**

### 1. 実装完了確認 ✅

- [x] 優先度1（概要タブ優先表示の確立）実装完了（2025年11月2日）
- [x] ステージング環境でのテスト完了
- [x] Finish Time目標達成（18.63秒、目標20-25秒以下）
- [x] 全ユーザー対応スクリプト作成完了

### 2. ブランチ準備 ✅

- [x] stagingブランチの最新状態確認完了
- [x] mainブランチとの差分確認完了（約60コミット）
- [x] コンフリクト予測完了（コンフリクトなし）
- [x] 重要な変更ファイルの確認完了

### 3. スクリプト準備 ✅

- [x] `scripts/populate_monthly_summary.py`作成完了
- [x] 実行権限付与完了
- [x] 構文エラーチェック完了
- [ ] ステージング環境でのテスト（推奨）

---

## ⏳ **実行前チェックリスト**

### Phase 1: マージ準備（実施可能）

#### Step 1-1: mainブランチの最新状態確認
- [ ] mainブランチを最新化
  ```bash
  git fetch origin main
  git checkout main
  git pull origin main
  ```

#### Step 1-2: コンフリクト確認（dry-runマージ）
- [ ] stagingブランチとのdry-runマージ
  ```bash
  git merge --no-commit --no-ff staging
  ```
- [ ] コンフリクトの有無確認
- [ ] コンフリクトがある場合は解決

#### Step 1-3: マージコミット作成
- [ ] マージコミットメッセージ準備
- [ ] マージ実行
  ```bash
  git commit -m "feat: 月次管理機能Phase 3完了とmain環境デプロイ準備

- 優先度1（概要タブ優先表示）実装完了
- ステージング環境テスト完了
- 全ユーザー対応スクリプト作成完了
- マイグレーション実行準備完了

Environment: staging → main
Test: ステージング環境で動作確認済み"
  ```

#### Step 1-4: mainブランチへのプッシュ
- [ ] プッシュ実行
  ```bash
  git push origin main
  ```
- [ ] Render.comでの自動デプロイ開始確認

---

### Phase 2: マイグレーション実行（デプロイ後）

#### Step 2-1: 本番環境への接続
- [ ] Render.com Dashboard → Shell
- [ ] 本番環境のシェルに接続

#### Step 2-2: マイグレーション状態確認
- [ ] 現在のマイグレーションバージョン確認
  ```bash
  flask db current
  ```
- [ ] 実行予定のマイグレーション確認
  ```bash
  flask db heads
  ```

#### Step 2-3: マイグレーション実行
- [ ] マイグレーション実行
  ```bash
  flask db upgrade
  ```
- [ ] 実行結果確認（エラーログの確認）

#### Step 2-4: マイグレーション確認
- [ ] テーブル作成確認
  ```bash
  psql $DATABASE_URL -c "\dt monthly*"
  ```
- [ ] 期待されるテーブル:
  - `monthly_targets`
  - `project_status_history`
  - `invoice_status_history`
  - `monthly_snapshots`
  - `monthly_summary`

---

### Phase 3: スクリプト実行（マイグレーション後）

#### Step 3-1: 実行前確認
- [ ] データ状況確認
  ```bash
  # 月次サマリーテーブルの状態確認
  psql $DATABASE_URL -c "SELECT COUNT(*) FROM monthly_summary;"
  # 期待: 0件
  
  # ユーザー数確認
  psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"
  
  # 履歴データ確認
  psql $DATABASE_URL -c "SELECT COUNT(*) FROM project_status_history;"
  psql $DATABASE_URL -c "SELECT COUNT(*) FROM invoice_status_history;"
  ```

#### Step 3-2: スクリプト実行
- [ ] スクリプトファイルの存在確認
  ```bash
  ls -la scripts/populate_monthly_summary.py
  ```
- [ ] 実行（全ユーザー）
  ```bash
  python scripts/populate_monthly_summary.py
  ```
- [ ] または、特定ユーザーのみ実行（テスト用）
  ```bash
  python scripts/populate_monthly_summary.py --user-id 2
  ```

#### Step 3-3: 実行後確認
- [ ] データ投入確認
  ```bash
  psql $DATABASE_URL -c "SELECT COUNT(*) FROM monthly_summary;"
  ```
- [ ] 実行ログの確認（エラーの有無）
- [ ] 最新3件の確認
  ```bash
  psql $DATABASE_URL -c "SELECT user_id, summary_month, acquired_projects, completed_projects, sent_invoices_amount FROM monthly_summary ORDER BY summary_month DESC LIMIT 3;"
  ```

---

### Phase 4: 動作確認（スクリプト実行後）

#### Step 4-1: 本番環境での動作確認
- [ ] ダッシュボードページの表示確認
  - URL: https://influberry.jp/dashboard
- [ ] 月次管理セクションの表示確認
  - 「概要」タブが優先表示されているか
  - 月次タブが正しく表示されているか
- [ ] データ表示確認
  - 累計活動案件数が表示されているか
  - 累計入金額が表示されているか
  - 月次統計が正しく表示されているか

#### Step 4-2: API動作確認
- [ ] `/api/monthly-stats/overview-minimal` - 軽量概要API
- [ ] `/api/monthly/current` - 統合API
- [ ] `/api/monthly-stats/{year}/{month}` - 月次統計API

#### Step 4-3: パフォーマンス確認
- [ ] Finish Timeの確認（目標: 20-25秒以下）
- [ ] APIレスポンスタイムの確認（本番環境は高性能DBのため、良好な可能性が高い）

---

## ⚠️ **注意事項**

### 1. ブランチ戦略の遵守

- ✅ **staging → main の順序でマージ**（正しいフロー）
- ⚠️ **過去の違反を繰り返さない**（`CRITICAL_BRANCH_STRATEGY_VIOLATION_20251025.md`参照）

### 2. マイグレーション実行のタイミング

- ⚠️ **デプロイ後、即座に実行**（テーブルがないとAPIエラーが発生）
- ⚠️ **実行前のバックアップ推奨**（本番データの保護）

### 3. スクリプト実行のタイミング

- ⚠️ **マイグレーション実行後、即座に実行**（空のテーブルへのデータ投入）
- ⚠️ **メンテナンス時間帯推奨**（サービスへの影響最小化）
- ⚠️ **実行時間の見積もり**（ユーザー数×月数に依存）

### 4. ロールバック計画

#### **緊急ロールバック手順**

```bash
# 1. マイグレーションのロールバック（必要に応じて）
flask db downgrade -1

# 2. コードのロールバック
git revert [commit-hash]
git push origin main --force-with-lease
```

---

## 📊 **期待される結果**

### デプロイ完了後

- ✅ 月次管理機能が本番環境で動作
- ✅ 「概要」タブが優先表示される
- ✅ 月次統計が正しく表示される
- ✅ APIレスポンスタイムが良好（本番環境の高性能DBのため）

### スクリプト実行後

- ✅ `monthly_summary`テーブルにデータが投入される
- ✅ 過去の履歴データから月次サマリーが生成される
- ✅ パフォーマンスが大幅に改善される（事前集計テーブルの活用）

---

## 🎯 **次のステップ（デプロイ後）**

### 推奨アクション

1. **本番環境でのパフォーマンス監視**
   - Finish Timeの監視
   - APIレスポンスタイムの監視
   - エラーログの監視

2. **ユーザーフィードバックの収集**
   - 月次管理機能の使用状況
   - 問題報告の有無

3. **継続的な改善**
   - パフォーマンスのさらなる最適化
   - 機能拡張（将来計画）

---

**作成日**: 2025年11月2日  
**状態**: デプロイ準備完了、実行待ち

