# Step 1: 安全なマージ手順書

**作成日**: 2025年11月2日  
**目的**: staging → main マージを安全に実行するための手順書

---

## 🛡️ 安全対策チェックリスト

### Phase 0: 事前準備（必須）✅

- [x] バックアップブランチ作成
- [x] 現在の変更をstash（作業中の変更を保存）
- [x] mainブランチの最新状態取得
- [x] コンフリクト確認（dry-runマージ）

---

## 📋 実行手順（段階的実行）

### Phase 1: mainブランチの準備（実施中）

```bash
# Step 1-1: mainブランチに切り替え
git checkout main

# Step 1-2: 最新状態を取得
git fetch origin main
git pull origin main

# Step 1-3: 現在の状態確認
git log --oneline -5
git status
```

### Phase 2: コンフリクト確認（必須）

```bash
# Step 2-1: dry-runマージ（実際にはマージしない）
git merge --no-commit --no-ff staging

# Step 2-2: 結果確認
# - コンフリクトが表示された場合 → 解決が必要
# - "Already up to date" または正常終了 → コンフリクトなし

# Step 2-3: dry-runを中止（確認後）
git merge --abort
```

### Phase 3: マージ実行（コンフリクト確認後）

```bash
# Step 3-1: マージ実行
git merge --no-ff staging -m "feat: 月次管理機能Phase 3完了とmain環境デプロイ準備

- 優先度1（概要タブ優先表示）実装完了
- ステージング環境テスト完了
- 全ユーザー対応スクリプト作成完了
- マイグレーション実行準備完了

Environment: staging → main
Test: ステージング環境で動作確認済み"

# Step 3-2: マージ結果確認
git log --oneline --graph -5
git status

# Step 3-3: リモートにプッシュ（確認後）
# ⚠️ 注意: プッシュ前に最終確認
git push origin main
```

### Phase 4: ロールバック準備（緊急時用）

```bash
# ロールバック手順（問題発生時）

# 方法1: マージを取り消す（プッシュ前の場合）
git reset --hard HEAD~1

# 方法2: マージを取り消す（プッシュ後の場合）
git revert -m 1 <merge-commit-hash>
git push origin main

# 方法3: バックアップブランチから復元
git checkout backup_before_main_merge_20251102_152212
git checkout -b main_recovered
# 必要に応じてmainブランチに反映
```

---

## ⚠️ 注意事項

### 1. プッシュ前の最終確認

- [ ] マージコミットの内容確認
- [ ] 変更ファイルの確認
- [ ] 重要なファイルの内容確認

### 2. プッシュ後の監視

- [ ] Render.comでの自動デプロイ開始確認
- [ ] デプロイログの監視
- [ ] エラーログの確認

### 3. 緊急時の対応

- [ ] ロールバック手順の確認
- [ ] 連絡先の確認
- [ ] バックアップの確認

---

**作成日**: 2025年11月2日  
**状態**: 実行準備完了

