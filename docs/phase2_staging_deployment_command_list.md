# Phase 2 ステージングデプロイ コマンド一覧

## 📋 実行手順

### Step 1: バックアップの作成（必須）

```bash
# バックアップディレクトリの作成
BACKUP_DIR="backups/phase2_staging_deployment_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Phase 2で変更したファイルをバックアップ
cp app/blueprints/monthly_current.py "$BACKUP_DIR/"
cp frontend/src/stores/monthly.js "$BACKUP_DIR/"
cp frontend/src/components/MonthlyStatsSection.vue "$BACKUP_DIR/"

# 既存のバックアップファイルもコピー
cp app/blueprints/monthly_current.py.backup_before_auth_fix_* "$BACKUP_DIR/" 2>/dev/null || true
cp frontend/src/stores/monthly.js.backup_before_phase2_* "$BACKUP_DIR/" 2>/dev/null || true
cp frontend/src/components/MonthlyStatsSection.vue.backup_before_phase2_* "$BACKUP_DIR/" 2>/dev/null || true

# バックアップファイルの確認
ls -la "$BACKUP_DIR/"
```

### Step 2: 現在の状態確認

```bash
# 現在のブランチ確認（stagingであることを確認）
git branch

# 現在の状態確認
git status

# 構文チェック（Pythonファイル）
python3 -m py_compile app/blueprints/monthly_current.py && echo "✅ Python構文チェック: OK"
```

### Step 3: 変更のコミット

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

### Step 4: ステージングブランチにプッシュ

```bash
# ステージングブランチにプッシュ
git push origin staging

# プッシュ後の確認
git log --oneline -5
git status
```

---

## 📋 一括実行コマンド（オプション）

### 方法1: スクリプトを使用（推奨）

```bash
# スクリプトを実行
./scripts/phase2_staging_deploy.sh
```

### 方法2: 手動で実行

上記のStep 1-4を順番に実行

---

## ⚠️ 注意事項

### 重要: mainブランチには絶対にデプロイしない

- Phase 2の変更はステージングブランチにのみデプロイ
- mainブランチは本番環境用のため、直接デプロイしない

### デプロイ前チェックリスト

- [ ] 現在のブランチが`staging`であることを確認
- [ ] バックアップファイルの作成完了
- [ ] 構文チェック完了（エラーなし）
- [ ] 変更ファイルの確認完了

---

## 📊 デプロイ後確認

### Render.comでの確認

1. **Render.com Dashboard**: 
   - `influberry-staging`サービスのデプロイ状況を確認
   - デプロイが完了するまで待つ（通常5-10分）

2. **ステージング環境URL**: 
   - `https://staging.influberry.jp` または `https://influberry-staging.onrender.com`
   - ページが正常に表示されることを確認

### パフォーマンス測定

#### Step 1: ブラウザでステージング環境にアクセス
- Chrome開発者ツールを開く（F12）
- PerformanceタブまたはNetworkタブで計測

#### Step 2: 測定項目
- **APIレスポンスタイム**: Networkタブで`/api/monthly/current`の「Total Time」を確認（目標: < 500ms）
- **ページ読み込み時間**: Performanceタブの「Navigation Timing」で「Load」時間を確認（目標: < 1秒）

---

## 🔄 ロールバック手順（必要に応じて）

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

**作成日時**: 2025-10-31
**準備者**: AI Assistant


