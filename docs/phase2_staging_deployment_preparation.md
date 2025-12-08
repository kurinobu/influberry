# Phase 2 ステージングデプロイ準備ガイド

## 📋 目次
1. [ブランチ戦略の確認](#1-ブランチ戦略の確認)
2. [ステージングデプロイ準備](#2-ステージングデプロイ準備)
3. [バックアップの作成](#3-バックアップの作成)
4. [デプロイ手順](#4-デプロイ手順)

---

## 1. ブランチ戦略の確認

### 1.1 現在のブランチ

確認が必要な項目:
- 現在のブランチ
- 変更ファイルの状態
- コミット履歴

### 1.2 ブランチ戦略（一般的な運用）

一般的なブランチ戦略:
- **main**: 本番環境用（絶対に直接デプロイしない）
- **staging**: ステージング環境用（Phase 2をデプロイ）
- **feature/xxx**: 機能開発用ブランチ

---

## 2. ステージングデプロイ準備

### 2.1 準備手順

#### Step 1: 現在の状態確認
- 現在のブランチを確認
- 変更ファイルの状態を確認
- コミット履歴を確認

#### Step 2: バックアップの作成
- 変更ファイルのバックアップを作成
- バックアップファイルの確認

#### Step 3: コミットとプッシュ
- 変更をコミット（まだコミットしていない場合）
- ステージングブランチにプッシュ

#### Step 4: デプロイ準備
- デプロイ前のチェックリスト確認
- ステージング環境へのデプロイ準備

---

## 3. バックアップの作成

### 3.1 バックアップ対象ファイル

Phase 2で変更したファイル:
- `app/blueprints/monthly_current.py`（認証方式統一）
- `frontend/src/stores/monthly.js`（USE_NEW_API = true）
- `frontend/src/components/MonthlyStatsSection.vue`（最適化）

### 3.2 バックアップ手順

バックアップファイルの作成:
- 変更前のファイルをバックアップ
- バックアップファイルの確認

---

## 4. デプロイ手順

### 4.1 デプロイ前チェックリスト

- [ ] バックアップファイルの作成完了
- [ ] 構文チェック完了（エラーなし）
- [ ] ローカル環境での動作確認完了
- [ ] コミット履歴の確認完了

### 4.2 デプロイ手順

1. **現在の状態確認**
2. **バックアップの作成**
3. **変更のコミット**（まだコミットしていない場合）
4. **ステージングブランチへの切り替え**
5. **マージまたはコミット**
6. **プッシュ**
7. **ステージング環境での確認**

---

## 5. ターミナルコマンド

### 5.1 現在の状態確認

```bash
# 現在のブランチを確認
git branch

# 現在の状態を確認
git status

# 最近のコミット履歴を確認
git log --oneline -10
```

### 5.2 バックアップの作成

```bash
# バックアップディレクトリの作成
mkdir -p backups/phase2_staging_deployment_$(date +%Y%m%d_%H%M%S)

# Phase 2で変更したファイルをバックアップ
cp app/blueprints/monthly_current.py backups/phase2_staging_deployment_$(date +%Y%m%d_%H%M%S)/
cp frontend/src/stores/monthly.js backups/phase2_staging_deployment_$(date +%Y%m%d_%H%M%S)/
cp frontend/src/components/MonthlyStatsSection.vue backups/phase2_staging_deployment_$(date +%Y%m%d_%H%M%S)/

# バックアップファイルの確認
ls -la backups/phase2_staging_deployment_*/
```

### 5.3 変更のコミット（まだコミットしていない場合）

```bash
# 変更ファイルをステージング
git add app/blueprints/monthly_current.py
git add frontend/src/stores/monthly.js
git add frontend/src/components/MonthlyStatsSection.vue

# コミット
git commit -m "Phase 2: 認証方式統一と新API有効化完了"
```

### 5.4 ステージングブランチへの切り替え

```bash
# ステージングブランチが存在する場合
git checkout staging

# ステージングブランチが存在しない場合（新規作成）
git checkout -b staging

# または、既存のステージングブランチを取得
git fetch origin staging
git checkout staging
```

### 5.5 マージまたはコミット

```bash
# 現在のブランチからステージングブランチにマージ
git merge $(git branch --show-current)

# または、変更を直接コミット
git add .
git commit -m "Phase 2: 認証方式統一と新API有効化完了"
```

### 5.6 プッシュ

```bash
# ステージングブランチにプッシュ
git push origin staging
```

### 5.7 デプロイ後の確認

```bash
# プッシュ後の状態確認
git log --oneline -5
git status
```

---

## 6. 注意事項

### 6.1 mainブランチへのデプロイ禁止

⚠️ **重要**: mainブランチには絶対にデプロイしない

- Phase 2の変更はステージングブランチにのみデプロイ
- mainブランチは本番環境用のため、直接デプロイしない

### 6.2 バックアップの重要性

- バックアップファイルは必ず作成する
- デプロイ前にバックアップファイルの確認を行う
- 問題発生時のロールバックに使用する

### 6.3 デプロイ前の確認

- 構文チェック完了（エラーなし）
- ローカル環境での動作確認完了
- コミット履歴の確認完了

---

## 7. まとめ

### 7.1 デプロイ準備手順

1. **現在の状態確認**: `git branch`, `git status`, `git log`
2. **バックアップの作成**: 変更ファイルをバックアップ
3. **変更のコミット**: まだコミットしていない場合
4. **ステージングブランチへの切り替え**: `git checkout staging`
5. **マージまたはコミット**: 変更をマージまたはコミット
6. **プッシュ**: `git push origin staging`

### 7.2 次のアクション

- [ ] ターミナルコマンドを実行
- [ ] ステージング環境でパフォーマンス測定
- [ ] 結果の評価とPhase 3の判断

---

**作成日時**: 2025-10-31
**準備者**: AI Assistant


