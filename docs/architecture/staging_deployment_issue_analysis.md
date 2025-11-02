# ステージング環境デプロイ問題 - 根本原因分析と解決策

**作成日**: 2025年10月25日  
**問題**: ステージング環境に月次管理機能が反映されない  
**状態**: 🔴 重大な問題（ブランチ戦略違反）

---

## 🎯 **根本原因の特定**

### ❌ **問題1: ブランチ戦略の根本的な違反**

#### **現在の状況（誤った運用）**
```
ローカル環境（main）
  ↓ 開発・マイグレーション作成
  ↓ 264c518cdcf3 (2025-10-23) ← 最新マイグレーション
  ↓
本番環境（main）← 直接デプロイ済み ✅
  ↓
ステージング環境（staging）← 古いまま ❌
  └── 97f40bb745e2 (2025-10-10) ← 古いマイグレーション
```

#### **正しいブランチ戦略（ドキュメント規定）**
```
ローカル環境
  ↓ 開発
  ↓
feature ブランチ作成
  ↓ テスト
  ↓
ステージング環境（staging）← 先にテスト ✅
  ↓ 動作確認
  ↓
本番環境（main）← 最後にデプロイ ✅
```

---

## 📋 **ブランチ戦略の定義（ドキュメントより）**

### **3.1 ブランチ構成**
```
main                           # 本番環境（https://influberry.jp）
├── staging                    # ステージング環境（https://staging.influberry.jp）
├── feature/menu-refactor      # 設計構造改善
├── feature/sns-auth          # SNS認証統合
└── hotfix/critical-xxx       # 緊急修正ブランチ
```

### **3.2 大規模変更フロー（feature ブランチ）**

**ドキュメント規定（119-135行目）:**
```bash
# ローカル環境で基本開発
git checkout -b feature/menu-refactor

# ローカルで基本実装・テスト
# コミット

# ステージング環境でテスト ← 重要!
git push origin feature/menu-refactor
# staging.influberry.jp で動作確認 ← 必須!

# 問題なければ本番反映
git checkout main
git merge feature/menu-refactor --no-ff
git push origin main
```

**適用ケース（137-141行目）:**
- 設計構造改善 ✅
- 新アプリ追加 ✅
- 認証システム変更 ✅
- アーキテクチャ変更 ✅

**月次管理機能は「新アプリ追加」に該当 → feature ブランチ必須**

---

## 🔴 **現状の問題点**

### **1. ブランチ戦略違反**
- ❌ **feature ブランチ未使用**: 大規模変更なのに直接 main にコミット
- ❌ **ステージング環境未経由**: テストなしで本番デプロイ
- ❌ **staging ブランチ未更新**: ステージング環境が古いまま放置

### **2. デプロイフローの不整合**
```
【誤った現在のフロー】
ローカル(main) → 本番(main) → ❌ ステージング(staging)放置

【正しいフロー】
ローカル → feature ブランチ → staging ブランチ → main ブランチ
```

### **3. マイグレーション管理の問題**
```
本番環境: 264c518cdcf3 (2025-10-23) ✅ 最新
ステージング: 97f40bb745e2 (2025-10-10) ❌ 古い（2週間の差）
```

---

## ✅ **解決策**

### **Phase 1: 現状の整理**

#### **Step 1-1: 現在のブランチ状況確認**
```bash
# ローカルで確認
git branch -a
git log --oneline --graph --all -20

# staging ブランチの状態確認
git checkout staging
git log --oneline -10
```

#### **Step 1-2: main と staging の差分確認**
```bash
# main と staging の差分を確認
git diff staging..main

# マイグレーションファイルの差分確認
git diff staging..main -- migrations/
```

---

### **Phase 2: ブランチ戦略の修正**

#### **Option A: staging ブランチを main に同期（推奨）**
```bash
# staging ブランチを main と同期
git checkout staging
git merge main --no-ff -m "sync: staging を main に同期（月次管理機能含む）

- 本番環境の変更を staging に反映
- マイグレーション 264c518cdcf3 を staging に追加
- ブランチ戦略の正常化"

# ステージング環境に反映
git push origin staging

# Render.com でステージング環境が自動デプロイされる
# staging.influberry.jp でマイグレーション実行確認
```

#### **Option B: feature ブランチ経由で再構築（正式手順）**
```bash
# 1. feature ブランチ作成（月次管理機能用）
git checkout main
git checkout -b feature/monthly-management

# 2. staging にマージしてテスト
git checkout staging
git merge feature/monthly-management --no-ff

# 3. ステージング環境でテスト
git push origin staging
# staging.influberry.jp で動作確認

# 4. 問題なければ本番反映（すでに反映済みなのでスキップ可能）
# git checkout main
# git merge feature/monthly-management --no-ff
# git push origin main

# 5. feature ブランチ削除
git branch -d feature/monthly-management
```

---

### **Phase 3: ステージング環境でのマイグレーション実行**

#### **Step 3-1: Render.com でステージング環境のシェル接続**
```bash
# Render.com Dashboard
# → influberry-staging サービス選択
# → Shell タブ

# マイグレーション状況確認
flask db current
flask db history

# マイグレーション実行
flask db upgrade

# テーブル作成確認
psql $DATABASE_URL -c "\dt" | grep -E "(monthly|project_status|invoice_status)"
```

#### **Step 3-2: 動作確認**
```bash
# ステージング環境で月次セクション確認
# https://staging.influberry.jp にアクセス
# - 月次セクションの表示確認
# - 月次管理機能の動作確認
```

---

### **Phase 4: 今後のブランチ運用ルール確立**

#### **ルール1: 大規模変更は必ず feature ブランチ経由**
```bash
# 新機能開発時
git checkout main
git checkout -b feature/new-feature

# ローカルで実装・テスト

# staging でテスト
git checkout staging
git merge feature/new-feature --no-ff
git push origin staging

# staging.influberry.jp で動作確認

# 問題なければ本番反映
git checkout main
git merge feature/new-feature --no-ff
git push origin main
```

#### **ルール2: staging ブランチは常に最新に保つ**
```bash
# 定期的に staging を main に同期
git checkout staging
git merge main --no-ff
git push origin staging
```

#### **ルール3: マイグレーションは staging で先にテスト**
```bash
# マイグレーション作成後
# 1. feature ブランチにコミット
# 2. staging にマージ
# 3. staging 環境でマイグレーション実行
# 4. 動作確認後に main にマージ
```

---

## 📊 **期待される結果**

### **Phase 2 完了後**
```
staging ブランチ: 264c518cdcf3 (2025-10-23) ✅ 最新
main ブランチ: 264c518cdcf3 (2025-10-23) ✅ 最新
ブランチ戦略: 正常 ✅
```

### **Phase 3 完了後**
```
ステージング環境:
- マイグレーション: 264c518cdcf3 ✅
- テーブル: monthly_projects, project_status_history, invoice_status_history ✅
- 月次セクション: 表示 ✅
```

---

## 🎯 **推奨アクション（優先順位順）**

### **1. 即座実行（最優先）**
```bash
# staging ブランチを main に同期
git checkout staging
git merge main --no-ff
git push origin staging
```

### **2. ステージング環境確認（5分後）**
- Render.com で自動デプロイ確認
- staging.influberry.jp で動作確認

### **3. マイグレーション実行（デプロイ完了後）**
```bash
# Render.com Shell
flask db upgrade
```

### **4. 動作確認**
- 月次セクションの表示確認
- 月次管理機能のテスト

### **5. 今後のルール適用**
- 大規模変更は feature ブランチ必須
- staging で先にテスト
- main は最後にデプロイ

---

## 📝 **まとめ**

### **根本原因**
1. ✅ **ブランチ戦略違反**: 大規模変更を main に直接コミット
2. ✅ **staging ブランチ未更新**: ステージング環境が2週間古い
3. ✅ **テストフロー未実施**: staging 環境でのテスト未実行

### **解決策**
1. ✅ **staging を main に同期**: `git merge main`
2. ✅ **マイグレーション実行**: `flask db upgrade`
3. ✅ **ブランチ運用ルール確立**: feature → staging → main

### **今後の対策**
1. ✅ **feature ブランチ必須**: 新機能は必ず feature ブランチ経由
2. ✅ **staging 優先テスト**: 本番前に必ず staging でテスト
3. ✅ **定期的な同期**: staging を定期的に main に同期

---

**作成者**: Claude (Anthropic)  
**対象**: InfluBerry ステージング環境デプロイ問題  
**重要度**: 🔴 高（ブランチ戦略の根本的な改善が必要）