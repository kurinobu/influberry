#!/bin/bash
# Phase 2 ステージングデプロイ準備スクリプト
# ブランチ戦略準拠: stagingブランチにデプロイ（mainには絶対にデプロイしない）

set -e  # エラー発生時に停止

echo "=========================================="
echo "Phase 2 ステージングデプロイ準備"
echo "=========================================="
echo ""

# バックアップディレクトリの作成
BACKUP_DIR="backups/phase2_staging_deployment_$(date +%Y%m%d_%H%M%S)"
echo "📦 バックアップディレクトリを作成: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# Phase 2で変更したファイルをバックアップ
echo "📦 Phase 2で変更したファイルをバックアップ..."
cp app/blueprints/monthly_current.py "$BACKUP_DIR/" 2>/dev/null || true
cp frontend/src/stores/monthly.js "$BACKUP_DIR/" 2>/dev/null || true
cp frontend/src/components/MonthlyStatsSection.vue "$BACKUP_DIR/" 2>/dev/null || true

# 既存のバックアップファイルもコピー
echo "📦 既存のバックアップファイルをコピー..."
cp app/blueprints/monthly_current.py.backup_before_auth_fix_* "$BACKUP_DIR/" 2>/dev/null || true
cp frontend/src/stores/monthly.js.backup_before_phase2_* "$BACKUP_DIR/" 2>/dev/null || true
cp frontend/src/components/MonthlyStatsSection.vue.backup_before_phase2_* "$BACKUP_DIR/" 2>/dev/null || true

echo "✅ バックアップ完了: $BACKUP_DIR"
ls -la "$BACKUP_DIR/"
echo ""

# 現在のブランチ確認
CURRENT_BRANCH=$(git branch --show-current)
echo "📋 現在のブランチ: $CURRENT_BRANCH"

if [ "$CURRENT_BRANCH" != "staging" ]; then
    echo "⚠️  警告: 現在のブランチが 'staging' ではありません"
    echo "   ステージングブランチに切り替えますか？ (y/n)"
    read -r response
    if [ "$response" = "y" ]; then
        git checkout staging
        echo "✅ ステージングブランチに切り替えました"
    else
        echo "❌ キャンセルされました"
        exit 1
    fi
fi

echo ""

# 構文チェック
echo "🔍 構文チェックを実行..."
python3 -m py_compile app/blueprints/monthly_current.py && echo "✅ Python構文チェック: OK" || echo "❌ Python構文チェック: エラー"

echo ""

# 変更ファイルの確認
echo "📋 変更ファイルを確認..."
git status --short

echo ""
echo "=========================================="
echo "次のステップ"
echo "=========================================="
echo "1. 変更を確認: git diff"
echo "2. 変更をコミット: git add . && git commit -m 'Phase 2: 認証方式統一と新API有効化完了'"
echo "3. ステージングブランチにプッシュ: git push origin staging"
echo ""
echo "⚠️  重要: mainブランチには絶対にデプロイしない"
echo ""


