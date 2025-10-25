# InfluBerry Git・ブランチ戦略（ローカル開発環境復旧・サブドメイン統合版）

**作成日**: 2025年9月12日  
**バージョン**: 3.0 - ローカル開発環境復旧・サブドメイン統合対応版  
**最終更新**: 2025年9月18日 16:00

## 1. 戦略概要

### 1.1 基本方針
- **統合型リポジトリ**: Flask + Vue.js統合プロジェクト管理
- **個人開発特化**: 1人開発に最適化されたシンプルな戦略
- **Claude Pro制約対応**: 1日2.5時間制限を考慮した効率的なワークフロー
- **開発環境統合**: ローカル開発環境復旧 + サブドメイン戦略
- **リスク管理重視**: 本番環境への影響最小化

### 1.2 実際のプロジェクト構成（2025年9月18日時点）
```
influberry_v2/ (統合型リポジトリ)
├── app/                    # Flask Backend
│   ├── __init__.py        # Flask アプリ初期化
│   ├── blueprints/        # Flask Blueprint（認証・API・プラグイン）
│   ├── models/            # SQLAlchemy データモデル
│   ├── plugins/           # プラグインシステム
│   ├── templates/         # Jinja2 テンプレート（最小限）
│   └── utils/             # ユーティリティ
├── frontend/              # Vue.js Frontend
│   ├── src/              # Vue.js ソースコード
│   ├── dist/             # ビルド成果物
│   ├── package.json      # Node.js 依存関係
│   └── vite.config.js    # Vite設定
├── instance/             # SQLite データベース（開発用）
├── migrations/           # Flask-Migrate
├── config.py             # Flask設定
├── wsgi.py              # WSGI エントリーポイント
├── requirements.txt      # Python依存関係
└── .env                 # 環境変数
```

### 1.3 新開発環境戦略（2025年9月18日決定）
**ローカル開発環境復旧 + サブドメイン戦略**を採用

**採用理由**:
- 個人開発の効率性最大化
- デザイン調整の即座確認
- リスクなしでの実験的開発
- 本番環境への影響完全排除

## 2. 開発環境戦略（2025年9月18日改定）

### 2.1 3層開発環境構成
```
1. ローカル開発環境（復旧予定）
   URL: http://127.0.0.1:5000（Flask） + http://127.0.0.1:3000（Vue.js）
   用途: リアルタイム開発・デザイン調整・即座確認
   データベース: SQLite
   
2. ステージング環境（新規構築）
   URL: https://staging.influberry.jp
   用途: feature ブランチテスト・本番前最終確認
   データベース: PostgreSQL（専用またはコピー）
   
3. 本番環境（運用中）
   URL: https://influberry.jp
   用途: ライブサービス・エンドユーザー向け
   データベース: PostgreSQL（本番）
```

### 2.2 環境別使い分け戦略

#### ローカル環境使用パターン
- 日常的なコード修正
- UI/UXデザイン調整
- 新機能の基本実装
- デバッグ・動作確認
- 即座フィードバックが必要な作業

#### ステージング環境使用パターン  
- feature ブランチの動作確認
- 大規模変更の事前テスト
- 本番環境との整合性確認
- 設計構造改善等のリスク高変更

#### 本番環境使用パターン
- 最終リリース
- ライブサービス運用
- 実ユーザーデータでの動作

## 3. ブランチ戦略（環境統合版）

### 3.1 ブランチ構成
```
main                           # 本番環境（https://influberry.jp）
├── staging                    # ステージング環境（https://staging.influberry.jp）
├── feature/menu-refactor      # 設計構造改善
├── feature/sns-auth          # SNS認証統合
├── feature/pdf-generation    # 請求書PDF生成
├── feature/qr-card-app       # QRコード名刺アプリ
└── hotfix/critical-xxx       # 緊急修正ブランチ
```

### 3.2 開発フロー別ブランチ戦略

#### パターンA: 小規模変更（main直接）
```bash
# ローカル環境で開発・確認
git checkout main
# コード修正・ローカルテスト
git add .
git commit -m "fix: 軽微なUI調整"
git push origin main  # 本番環境に直接反映
```

**適用ケース**:
- Google Analytics動作確認
- 軽微なUI調整
- バグ修正
- 既存機能の小改善

#### パターンB: 大規模変更（feature ブランチ）
```bash
# ローカル環境で基本開発
git checkout -b feature/menu-refactor

# ローカルで基本実装・テスト
# コミット

# ステージング環境でテスト
git push origin feature/menu-refactor
# staging.influberry.jp で動作確認

# 問題なければ本番反映
git checkout main
git merge feature/menu-refactor --no-ff
git push origin main
```

**適用ケース**:
- 設計構造改善
- 新アプリ追加
- 認証システム変更
- アーキテクチャ変更

### 3.3 残存課題・Month 2計画のブランチ振り分け

#### main直接作業
- **Google Analytics動作確認**（48時間後・最優先）
- **InvoiceApp統計表示副作用修正**（軽微なCSS）
- **AuthPage.vueロゴ余白調整**（軽微なUI）
- **マイクロインタラクション追加**（アニメーション）

#### feature ブランチ必須
- **設計構造改善**（`feature/menu-system-refactor`）
- **SNS認証統合**（`feature/sns-auth`）
- **請求書PDF生成**（`feature/pdf-generation`）
- **プラグインシステム拡張**（`feature/plugin-architecture`）
- **Stripe決済統合**（`feature/stripe-payment`）
- **Todoリストプラグイン**（`feature/todo-plugin`）
- **QRコード名刺アプリ**（`feature/qr-card-app`）
- **ブランド提案文ジェネレーター**（`feature/ai-generator`）

## 4. 開発環境セットアップ（復旧・構築計画）

### 4.1 ローカル開発環境復旧（最優先）

#### Phase 1: 現状確認・問題特定
```bash
# 現在のローカル環境状況確認
cd influberry_v2

# Flask設定確認
cat config.py | grep -E "(CORS|DEBUG|ENV)"

# Vite設定確認  
cat frontend/vite.config.js

# 依存関係確認
pip list | grep -E "(flask|cors)"
cd frontend && npm list | grep -E "(vite|proxy)"
```

#### Phase 2: Flask + Vue.js ローカル連携設定
```bash
# Flask CORS設定（app/__init__.py修正）
# Vue.js proxy設定（frontend/vite.config.js修正）
# 環境変数設定（.env.local作成）

# ローカル起動確認
# Terminal 1: Flask Backend
python wsgi.py

# Terminal 2: Vue.js Frontend  
cd frontend && npm run dev

# 動作確認: http://127.0.0.1:3000
```

#### 予想される修正箇所
- `app/__init__.py`: Flask-CORS設定追加
- `frontend/vite.config.js`: proxy設定でFlaskに接続
- `.env.local`: ローカル環境専用変数
- `config.py`: 環境別設定分離

### 4.2 ステージング環境構築（Render.com）

#### Render.com追加サービス作成
```yaml
# staging用render.yaml設定
services:
  - type: web
    name: influberry-staging
    runtime: python
    plan: free
    branch: staging
    repo: https://github.com/kurinobu/influberry
    
    buildCommand: |
      pip install -r requirements.txt
      cd frontend && npm install && npm run build
      mkdir -p app/static && cp -r frontend/dist/* app/static/
    
    startCommand: gunicorn wsgi:app
    
    envVars:
      - key: FLASK_ENV
        value: staging
      - key: DATABASE_URL
        fromDatabase:
          name: influberry-staging-db
          property: connectionString
      - key: DOMAIN_NAME
        value: staging.influberry.jp
        
  - type: pgsql
    name: influberry-staging-db
    plan: free
    databaseName: influberry_staging
```

#### ドメイン設定
- メインドメイン: `influberry.jp` → 本番環境
- サブドメイン: `staging.influberry.jp` → ステージング環境

### 4.3 環境構築タイムライン
```
Day 1: ローカル環境復旧
- Flask CORS設定修正
- Vue.js proxy設定修正
- 動作確認・デバッグ

Day 2: ステージング環境構築
- Render.com追加サービス作成
- staging ブランチ作成・初期デプロイ
- ドメイン設定・動作確認

Day 3: 開発フロー確立
- 各環境でのテスト実行
- 設計構造改善着手（feature ブランチ）
```

## 5. 日常開発ワークフロー（環境統合版）

### 5.1 小規模変更フロー（main直接）
```bash
# ローカル環境で開発
cd influberry_v2
git checkout main
git pull origin main

# Flask + Vue.js 同時起動
# Terminal 1
python wsgi.py

# Terminal 2  
cd frontend && npm run dev

# ブラウザで http://127.0.0.1:3000 確認
# 修正・テスト・確認のサイクル

# 完了後コミット
git add .
git commit -m "fix: AuthPage.vueロゴ余白調整

- 上部余白15px→10pxに調整
- レスポンシブ対応確認済み
- ローカル環境テスト完了"

git push origin main  # 本番環境に直接反映
```

### 5.2 大規模変更フロー（feature ブランチ）
```bash
# ローカル環境で基本実装
git checkout main
git pull origin main
git checkout -b feature/menu-system-refactor

# ローカルで段階的開発
# Phase 1: Pinia Store導入
git add .
git commit -m "feat: Pinia Store基本構造実装"

# Phase 2: HamburgerMenu簡素化
git add .
git commit -m "refactor: HamburgerMenu 6ステップ→2ステップ簡素化"

# ローカルテスト完了後、ステージング環境でテスト
git push origin feature/menu-system-refactor

# ステージング環境確認
# https://staging.influberry.jp で動作確認
# - メニュー表示確認
# - 基本データモーダル確認
# - 各ページ遷移確認

# 問題なければ本番反映
git checkout main
git merge feature/menu-system-refactor --no-ff
git push origin main

# ブランチクリーンアップ
git branch -d feature/menu-system-refactor
git push origin --delete feature/menu-system-refactor
```

### 5.3 緊急修正フロー（hotfix）
```bash
# 本番で問題発見時
git checkout main
git checkout -b hotfix/critical-auth-bug

# ローカルで緊急修正
# 最小限の修正・テスト

git add .
git commit -m "hotfix: 認証システム緊急修正

問題: ログイン時のセッション固定化
解決: セッションID再生成追加
影響: セキュリティ脆弱性解消"

# 即座に本番反映
git checkout main
git merge hotfix/critical-auth-bug --no-ff
git push origin main

# 必要に応じてステージング環境にも反映
git checkout staging
git merge main
git push origin staging
```

## 6. デプロイ戦略（3環境統合）

### 6.1 環境別デプロイ設定

#### 本番環境（Production）
```yaml
# render.yaml（既存）
services:
  - type: web
    name: influberry
    runtime: python
    plan: free → Professional予定
    branch: main
    repo: https://github.com/kurinobu/influberry
    
    buildCommand: |
      pip install -r requirements.txt
      cd frontend && npm install && npm run build
      mkdir -p app/static && cp -r frontend/dist/* app/static/
    
    startCommand: gunicorn wsgi:app
    
    envVars:
      - key: FLASK_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: influberry-db
          property: connectionString
      - key: DOMAIN_NAME
        value: influberry.jp
```

#### ステージング環境（新規作成）
```yaml
# staging用設定追加
services:
  - type: web
    name: influberry-staging
    runtime: python
    plan: free
    branch: staging
    repo: https://github.com/kurinobu/influberry
    
    buildCommand: |
      pip install -r requirements.txt
      cd frontend && npm install && npm run build
      mkdir -p app/static && cp -r frontend/dist/* app/static/
    
    startCommand: gunicorn wsgi:app
    
    envVars:
      - key: FLASK_ENV
        value: staging
      - key: DATABASE_URL
        fromDatabase:
          name: influberry-staging-db
          property: connectionString
      - key: DOMAIN_NAME
        value: staging.influberry.jp

  - type: pgsql
    name: influberry-staging-db
    plan: free
    databaseName: influberry_staging
```

### 6.2 自動デプロイフロー
```
Local Development → Staging → Production

git push origin feature/xxx
    ↓ (自動)
staging.influberry.jp でテスト
    ↓ (手動マージ)
git merge → git push origin main
    ↓ (自動)  
influberry.jp に本番反映
```

### 6.3 ドメイン構成
- **本番**: `https://influberry.jp`
- **ステージング**: `https://staging.influberry.jp`
- **ローカル**: `http://127.0.0.1:3000`

## 7. Claude Pro制約対応・効率的作業分割

### 7.1 制約を活かした作業計画
```bash
# セッション1（2.5時間）: ローカル環境復旧
- Flask CORS設定確認・修正
- Vue.js proxy設定確認・修正  
- 動作確認・デバッグ
- 作業記録・次回引き継ぎ準備

# セッション2（2.5時間）: ステージング環境構築
- Render.com staging サービス作成
- staging ブランチ作成・初期デプロイ
- ドメイン設定・動作確認

# セッション3（2.5時間）: 設計構造改善着手
- feature/menu-system-refactor ブランチ作成
- Pinia Store基本実装
- ローカル→ステージングテスト
```

### 7.2 作業継続性確保
```bash
# セッション終了時の必須作業
git add .
git commit -m "wip: [具体的作業内容]

完了:
- [完了した具体的作業]

進行中:  
- [現在の作業状況]

次回セッション予定:
- [次回実施予定作業]

Claude Pro制限による中断: 2.5時間経過"

git push origin current-branch

# 次回セッション開始時の確認
git log --oneline -5  # 前回作業確認
```

### 7.3 効率的な時間配分
- **環境構築**: 1セッション集中投入
- **開発作業**: 機能単位で完結する範囲
- **テスト・確認**: 各セッション終了前15分確保
- **記録・引き継ぎ**: 各セッション終了前10分確保

## 8. コミット規約（環境統合対応）

### 8.1 Conventional Commits + 環境識別
```
<type>(<scope>): <description>

<body>

Environment: [local/staging/production]
```

### 8.2 Type一覧（環境統合版）
- **feat**: 新機能実装
- **fix**: バグ修正
- **refactor**: 設計構造改善
- **ui**: UI/UX改善
- **env**: 環境設定・構築
- **deploy**: デプロイ関連
- **docs**: ドキュメント
- **test**: テスト関連
- **wip**: 作業中（Claude Pro制限対応）

### 8.3 環境統合対応コミットメッセージ例
```bash
feat(menu): Pinia Store統合によるメニュー簡素化

- HamburgerMenu 6ステップ→2ステップ削減
- Vue.js reactivity問題根本解決
- z-index競合問題解消

Environment: local→staging→production
Test: 全環境動作確認済み
```

## 9. 品質管理・監視体制

### 9.1 環境別品質チェック
```bash
# ローカル環境
- ESLint/Prettier実行
- Flask syntax check
- 基本動作確認

# ステージング環境  
- 本番同等の統合テスト
- パフォーマンステスト
- セキュリティチェック

# 本番環境
- デプロイ後監視（15分間）
- Google Analytics確認
- エラーログ監視
```

### 9.2 ロールバック体制
```bash
# 即座ロールバック手順
git revert [commit-hash]
git push origin main --force-with-lease

# または
git reset --hard [previous-commit]
git push origin main --force-with-lease
```

## 10. 次のステップ・実装計画

### 10.1 優先度1: 環境構築（Week 1）
1. **ローカル環境復旧**
2. **ステージング環境構築**
3. **開発フロー確立**

### 10.2 優先度2: 残存課題対応（Week 2-3）
1. **Google Analytics動作確認**（48時間後）
2. **設計構造改善**（feature ブランチ）
3. **軽微なUI調整**（main直接）

### 10.3 優先度3: 新機能開発（Month 2以降）
1. **SNS認証統合**
2. **PDF生成機能**
3. **新アプリ追加**

---

**作成者**: Claude (Anthropic)  
**対象**: InfluBerry統合型プロジェクト  
**特徴**: ローカル開発環境復旧 + サブドメイン戦略  
**制約対応**: Claude Pro 1日2.5時間制限最適化  
**最終更新**: 2025年9月18日 16:00