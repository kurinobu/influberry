# Phase 2 ステージングデプロイ コマンドガイド

## 📋 目次
1. [現在の状態](#1-現在の状態)
2. [バックアップの作成](#2-バックアップの作成)
3. [ステージングデプロイ手順](#3-ステージングデプロイ手順)
4. [デプロイ後確認](#4-デプロイ後確認)

---

## 1. 現在の状態

### 1.1 確認済み項目

✅ **現在のブランチ**: `staging`  
✅ **変更ファイル**: 
- `app/blueprints/monthly_current.py`（認証方式統一）
- `frontend/src/stores/monthly.js`（USE_NEW_API = true）
- `frontend/src/components/MonthlyStatsSection.vue`（最適化）

✅ **ブランチ戦略**: 準拠（stagingブランチで作業中）

---

## 2. バックアップの作成

### 2.1 バックアップコマンド

```bash
# バックアップディレクトリの作成
mkdir -p backups/phase2_staging_deployment_$(date +%Y%m%d_%H%M%S)

# Phase 2で変更したファイルをバックアップ
cp app/blueprints/monthly_current.py backups/phase2_staging_deployment_$(date +%Y%m%d_%H%M%S)/
cp frontend/src/stores/monthly.js backups/phase2_staging_deployment_$(date +%Y%m%d_%H%M%S)/
cp frontend/src/components/MonthlyStatsSection.vue backups/phase2_staging_deployment_$(date +%Y%m%d_%H%M%S)/

# 既存のバックアップファイルもバックアップディレクトリにコピー
cp app/blueprints/monthly_current.py.backup_before_auth_fix_* backups/phase2_staging_deployment_$(date +%Y%m%d_%H%M%S)/ 2>/dev/null || true
cp frontend/src/stores/monthly.js.backup_before_phase2_* backups/phase2_staging_deployment_$(date +%Y%m%d_%H%M%S)/ 2>/dev/null || true
cp frontend/src/components/MonthlyStatsSection.vue.backup_before_phase2_* backups/phase2_staging_deployment_$(date +%Y%m%d_%H%M%S)/ 2>/dev/null || true

# バックアップファイルの確認
ls -la backups/phase2_staging_deployment_*/
```

---

## 3. ステージングデプロイ手順

### 3.1 デプロイ前チェック

```bash
# 現在のブランチ確認（stagingであることを確認）
git branch

# 現在の状態確認
git status

# 構文チェック（Pythonファイル）
python3 -m py_compile app/blueprints/monthly_current.py && echo "✅ Python構文チェック: OK"

# 変更ファイルの確認
git diff app/blueprints/monthly_current.py | head -30
git diff frontend/src/stores/monthly.js | head -30
git diff frontend/src/components/MonthlyStatsSection.vue | head -30
```

### 3.2 変更のコミット

```bash
# 変更ファイルをステージング
git add app/blueprints/monthly_current.py
git add frontend/src/stores/monthly.js
git add frontend/src/components/MonthlyStatsSection.vue

# コミット
git commit -m "Phase 2: 認証方式統一と新API有効化完了

- app/blueprints/monthly_current.py: @jwt_required() → @login_required に変更（既存APIと統一）
- frontend/src/stores/monthly.js: USE_NEW_API = true に変更
- frontend/src/components/MonthlyStatsSection.vue: 新API使用時の最適化実装

計画書v2.0準拠: 認証方式の統一、新API有効化、フォールバック機能維持"
```

### 3.3 ステージングブランチにプッシュ

```bash
# ステージングブランチにプッシュ
git push origin staging

# プッシュ後の確認
git log --oneline -5
git status
```

---

## 4. デプロイ後確認

### 4.1 Render.comでの確認

1. **Render.com Dashboard**: 
   - `influberry-staging`サービスのデプロイ状況を確認
   - デプロイが完了するまで待つ（通常5-10分）

2. **ステージング環境URL**: 
   - `https://staging.influberry.jp` または `https://influberry-staging.onrender.com`
   - ページが正常に表示されることを確認

### 4.2 パフォーマンス測定

#### Step 1: ブラウザでステージング環境にアクセス
- Chrome開発者ツールを開く（F12）
- PerformanceタブまたはNetworkタブで計測

#### Step 2: 測定項目
- **APIレスポンスタイム**: Networkタブで`/api/monthly/current`の「Total Time」を確認（目標: < 500ms）
- **ページ読み込み時間**: Performanceタブの「Navigation Timing」で「Load」時間を確認（目標: < 1秒）

---

## 5. ロールバック手順（必要に応じて）

### 5.1 ロールバックコマンド

```bash
# バックアップファイルから復元
cp backups/phase2_staging_deployment_YYYYMMDD_HHMMSS/app/blueprints/monthly_current.py app/blueprints/monthly_current.py
cp backups/phase2_staging_deployment_YYYYMMDD_HHMMSS/frontend/src/stores/monthly.js frontend/src/stores/monthly.js
cp backups/phase2_staging_deployment_YYYYMMDD_HHMMSS/frontend/src/components/MonthlyStatsSection.vue frontend/src/components/MonthlyStatsSection.vue

# 復元後のコミット
git add .
git commit -m "rollback: Phase 2変更をロールバック"
git push origin staging
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

- [ ] 現在のブランチが`staging`であることを確認
- [ ] バックアップファイルの作成完了
- [ ] 構文チェック完了（エラーなし）
- [ ] 変更ファイルの確認完了

---

## 7. まとめ

### 7.1 実行順序

1. **バックアップの作成**: 変更ファイルをバックアップ
2. **デプロイ前チェック**: 構文チェック、変更ファイルの確認
3. **変更のコミット**: Phase 2の変更をコミット
4. **ステージングブランチにプッシュ**: `git push origin staging`
5. **デプロイ後確認**: Render.comとステージング環境での確認

### 7.2 次のアクション

- [ ] ターミナルコマンドを実行
- [ ] ステージング環境でパフォーマンス測定
- [ ] 結果の評価とPhase 3の判断

---

**作成日時**: 2025-10-31
**準備者**: AI Assistant


