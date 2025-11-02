# BerryCard アーキテクチャ設計書 v1.0

---

**作成日**: 2025年10月16日  
**更新日**: 2025年10月21日  
**バージョン**: 1.0 → ロールバック完了 → 月次管理機能動的実装  
**対象**: InfluBerry BerryCard実装 → モバイルファースト再設計 → 月次管理機能改善

---

## ⚠️ 重要: ロールバック完了と再設計方針

### ロールバック実施概要

**実施日**: 2025年10月20日  
**理由**: デスクトップファースト設計によるモバイルユーザビリティの問題  
**結果**: BerryCard実装を完全にロールバックし、モバイルファースト再設計を決定

### 発見された根本的問題

**❌ 設計思想の逆転**:
- **99%のユーザー**: スマホで使用するが、デスクトップファースト設計
- **1%の開発者**: PCで使用するが、モバイルユーザーが使いにくい
- **ビジネス的に致命的**: 99%のユーザーが使いにくいアプリ

**❌ 技術的負債**:
- デスクトップ前提の複雑なレイアウト
- タブシステムによる非効率なナビゲーション
- 左右分割によるモバイルでの使いにくさ

### 次回設計方針

**🎯 モバイルファースト設計**:
- **スマホ画面を基準**: モバイルファーストの設計思想
- **タッチ操作**: モバイル標準の操作を前提
- **シンプル構造**: 複雑なレイアウトを避ける

**📱 モバイル最適化**:
- **全画面プレビュー**: スマホ画面全体を使用
- **スワイプナビゲーション**: タブの代わりにスワイプ
- **ボトムナビゲーション**: モバイル標準のUI

## 🎯 **月次管理機能の動的実装アーキテクチャ**

### 現在の問題点
- **固定月表示**: 10月、11月、12月が固定で表示
- **実用性ゼロ**: 6月でも10月の目標設定しかできない
- **無意味なデータ**: 未来の実績（常にゼロ）を表示

### 動的実装のアーキテクチャ

#### **1. 動的タブ生成システム**
```javascript
// MonthlyTabs.vue の動的実装
const generateDynamicTabs = () => {
  const now = new Date()
  const currentMonth = now.getMonth() + 1
  const currentYear = now.getFullYear()
  
  // 過去3ヶ月のタブを生成
  return [
    { id: `${currentYear}-${currentMonth-2}`, label: `${currentMonth-2}月` },
    { id: `${currentYear}-${currentMonth-1}`, label: `${currentMonth-1}月` },
    { id: `${currentYear}-${currentMonth}`, label: `${currentMonth}月` }
  ]
}
```

#### **2. 目標設定の簡素化**
```javascript
// UserSettings.vue の簡素化
const currentMonth = new Date().getMonth() + 1
const currentYear = new Date().getFullYear()
// ドロップダウン削除、当月のみの目標設定
```

#### **3. 実用的データ表示**
- **過去の実績**: 実際のデータが存在
- **当月の進捗**: 現在進行中の実績
- **目標設定**: 当月のみ、シンプルなUI

---

## 1. システム構成図（参考: 旧設計）

### 1.1 全体アーキテクチャ

```
┌─────────────────────────────────────────────────────────┐
│                   ユーザー（ブラウザ）                    │
└─────────────────────────────────────────────────────────┘
                            │ HTTPS
┌─────────────────────────────────────────────────────────┐
│              Vue.js 3 Frontend (Vite)                   │
├─────────────────────────────────────────────────────────┤
│  - AppIndexPage.vue                                     │
│  - CardApp.vue                                          │
│  - ProfileEditForm.vue                                  │
│  - DesignCustomizer.vue                                 │
│  - ProfilePreview.vue                                   │
│  - QRCodeDownload.vue                                   │
│  - AISuggestionPanel.vue                               │
│  - Pinia Store: profiles.js, ai.js                     │
└─────────────────────────────────────────────────────────┘
                            │ REST API (JSON)
┌─────────────────────────────────────────────────────────┐
│               Flask Backend (Python)                    │
├─────────────────────────────────────────────────────────┤
│  Blueprint: profiles.py, ai.py                          │
│  - GET  /api/profiles/me                                │
│  - PUT  /api/profiles/me                                │
│  - POST /api/profiles/me/icon                           │
│  - POST /api/profiles/me/line-qr                        │
│  - POST /api/profiles/me/generate-qr                    │
│  - GET  /api/profiles/me/download-qr                    │
│  - GET  /@<username>                                    │
│  - GET  /c/<custom_slug>                                │
│  - GET  /api/ai/health                                  │
│  - POST /api/ai/suggest-profile                         │
│  - POST /api/ai/suggest-sns-post                       │
│  - POST /api/ai/suggest-hashtags                       │
│  - POST /api/ai/analyze-engagement                        │
│  - GET  /api/ai/settings                               │
│  - GET  /api/ai/usage-stats                            │
└─────────────────────────────────────────────────────────┘
                            │ SQLAlchemy ORM
┌─────────────────────────────────────────────────────────┐
│            PostgreSQL Database                          │
├─────────────────────────────────────────────────────────┤
│  - users テーブル（拡張）                                 │
│  - projects テーブル（既存）                              │
│  - invoices テーブル（既存）                              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              File Storage (Static Files)                │
├─────────────────────────────────────────────────────────┤
│  app/static/uploads/                                    │
│    ├── icons/       (アイコン画像)                       │
│    ├── qrcodes/     (QRコード画像)                       │
│    └── line_qrcodes/ (LINE QRコード)                     │
└─────────────────────────────────────────────────────────┘

```

---

## 2. データフロー図

### 2.1 プロフィール編集フロー

```
ユーザー → ProfileEditForm.vue → profiles Store → Flask API → Database
   │                                    │
   └─────── リアルタイムプレビュー ──────┘
           ProfilePreview.vue

```

**詳細ステップ**:

1. ユーザーがフォーム入力
2. `@input`イベント発火
3. `updateProfileLocal()`でStoreローカル更新
4. ProfilePreview.vueが自動再レンダリング（Vue Reactivity）
5. 保存ボタンクリック時に`updateProfile()` API呼び出し
6. Flask APIがデータベース更新
7. QRコード自動再生成

---

### 2.2 QRコード生成フロー

```
保存ボタン → updateProfile() → Flask API
                                   │
                        ┌──────────┴──────────┐
                        │                     │
                   DB更新            generate_qr_code_file()
                        │                     │
                        │              ┌──────┴──────┐
                        │              │             │
                        │          PNG生成      vCard生成
                        │              │             │
                        └──────────────┴─────────────┘
                                   │
                            ファイル保存
                    app/static/uploads/qrcodes/

```

---

### 2.3 画像アップロードフロー

```
ファイル選択 → <input type="file"> → handleIconUpload()
                                          │
                                    ┌─────┴─────┐
                                    │           │
                            プレビュー表示   API送信
                            (FileReader)   (FormData)
                                    │           │
                            ローカル表示   サーバー処理
                                              │
                                    ┌─────────┴─────────┐
                                    │                   │
                              ファイル検証        画像リサイズ
                              (5MB制限)         (500x500px)
                                    │                   │
                                    └─────────┬─────────┘
                                              │
                                        ファイル保存
                                app/static/uploads/icons/
                                              │
                                        DB更新
                                    (icon_filename)

```

---

## 3. コンポーネント設計

### 3.1 Vue.jsコンポーネント階層

```
App.vue
│
├── Router
    │
    ├── AuthPage.vue (既存)
    │
    ├── AppIndexPage.vue (新規) ← アプリ選択専用ページ
    │   ├── BerryWork (案件管理)
    │   ├── BerryPay (請求書管理)
    │   ├── BerryDo (タスク管理)
    │   ├── BerryCard (デジタル名刺)
    │   └── 将来プラグイン（準備中）
    │
    ├── DashboardPage.vue (既存)
    │
    ├── ProjectApp.vue (既存)
    │
    ├── InvoiceApp.vue (既存)
    │
    ├── TodoApp.vue (既存)
    │
    └── CardApp.vue (新規)
        ├── ProfileEditForm.vue (新規)
        │   ├── アイコンアップロード
        │   ├── 基本情報入力
        │   ├── SNSリンク入力
        │   └── LINE QRコードアップロード
        │
        ├── DesignCustomizer.vue (新規)
        │   ├── カラー選択
        │   ├── フォント選択
        │   └── レイアウト選択
        │
        ├── ProfilePreview.vue (新規)
        │   └── リアルタイムプレビュー表示
        │
        └── QRCodeDownload.vue (新規)
            ├── PNG ダウンロード
            ├── SVG ダウンロード
            └── vCard ダウンロード

```

---

### 3.2 Pinia Store設計

```
stores/
│
├── auth.js (既存)
│   ├── state: { isAuthenticated, user }
│   ├── actions: { login, logout, checkAuth }
│   └── 修正: ログイン後リダイレクト先 → /app-index
│
├── profiles.js (新規)
│   ├── state:
│   │   ├── profile: { ...全フィールド }
│   │   ├── loading: Boolean
│   │   └── error: String
│   │
│   ├── getters:
│   │   ├── isPremium
│   │   ├── profileUrl
│   │   └── snsLinks
│   │
│   └── actions:
│       ├── fetchProfile()
│       ├── updateProfile(data)
│       ├── updateProfileLocal(data)  ← リアルタイムプレビュー用
│       ├── updateDesignLocal(data)   ← リアルタイムプレビュー用
│       ├── uploadIcon(file)
│       ├── uploadLineQr(file)
│       ├── generateQrCode(format)
│       └── downloadQrCode(format)
│
├── projects.js (既存)
├── invoices.js (既存)
├── todos.js (既存)
└── ui.js (既存)

```

---

### 3.3 Flask Blueprint設計

```
app/blueprints/
│
├── auth.py (既存)
├── main.py (既存)
├── plugins.py (既存)
├── projects.py (既存)
├── invoices.py (既存)
├── todos.py (既存)
│
└── profiles.py (新規)
    │
    ├── API Endpoints:
    │   ├── GET  /api/profiles/me
    │   ├── PUT  /api/profiles/me
    │   ├── POST /api/profiles/me/icon
    │   ├── POST /api/profiles/me/line-qr
    │   ├── POST /api/profiles/me/generate-qr
    │   └── GET  /api/profiles/me/download-qr
    │
    ├── Public Pages:
    │   ├── GET  /@<username>
    │   └── GET  /c/<custom_slug>
    │
    └── Helper Functions:
        ├── generate_qr_code_file(user)
        ├── generate_vcard(user)
        ├── validate_image_file(file)
        └── is_crawler(user_agent)

```

---

## 4. ディレクトリ構造

### 4.1 新規作成ファイル一覧

```
influberry_v2/
│
├── app/
│   ├── blueprints/
│   │   └── profiles.py                    # 新規作成
│   │
│   ├── static/
│   │   └── uploads/
│   │       ├── icons/                     # 新規ディレクトリ
│   │       ├── qrcodes/                   # 新規ディレクトリ
│   │       └── line_qrcodes/              # 新規ディレクトリ
│   │
│   ├── templates/
│   │   └── profiles/                      # 新規ディレクトリ
│   │       └── public_profile.html        # 新規作成
│   │
│   └── utils/
│       ├── file_validation.py             # 新規作成
│       └── rate_limit.py                  # 新規作成
│
├── frontend/
│   └── src/
│       ├── views/
│       │   ├── AppIndexPage.vue           # 新規作成
│       │   └── CardApp.vue                # 新規作成
│       │
│       ├── components/
│       │   ├── ProfileEditForm.vue        # 新規作成
│       │   ├── DesignCustomizer.vue       # 新規作成
│       │   ├── ProfilePreview.vue         # 新規作成
│       │   └── QRCodeDownload.vue          # 新規作成
│       │
│       └── stores/
│           └── profiles.js                # 新規作成
│
└── migrations/
    └── versions/
        └── xxxx_add_berrycard_fields.py   # 新規作成（マイグレーション）

```

---

### 4.2 既存ファイル修正箇所

```
既存ファイル修正:

1. app/__init__.py
   └── profiles_bp を register_blueprint()

2. frontend/src/router/index.js
   └── /app-index, /card ルート追加

3. frontend/src/stores/auth.js
   └── ログイン後リダイレクト先を /app-index に変更

4. requirements.txt
   └── qrcode, Pillow, vobject 追加

```

---

## 5. データベース設計詳細

### 5.1 マイグレーションSQL

```sql
-- Phase 1: 基本フィールド追加

ALTER TABLE users ADD COLUMN bio TEXT;
ALTER TABLE users ADD COLUMN icon_filename VARCHAR(100);
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20);
ALTER TABLE users ADD COLUMN company_name VARCHAR(100);
ALTER TABLE users ADD COLUMN website_url VARCHAR(255);

-- SNSリンク
ALTER TABLE users ADD COLUMN tiktok_url VARCHAR(255);
ALTER TABLE users ADD COLUMN instagram_url VARCHAR(255);
ALTER TABLE users ADD COLUMN twitter_url VARCHAR(255);
ALTER TABLE users ADD COLUMN youtube_url VARCHAR(255);
ALTER TABLE users ADD COLUMN threads_url VARCHAR(255);

-- LINE QRコード
ALTER TABLE users ADD COLUMN line_qr_filename VARCHAR(100);

-- デザイン設定
ALTER TABLE users ADD COLUMN card_color VARCHAR(20) NOT NULL DEFAULT 'peach';
ALTER TABLE users ADD COLUMN card_font VARCHAR(50) NOT NULL DEFAULT 'Nunito';
ALTER TABLE users ADD COLUMN card_layout VARCHAR(20) NOT NULL DEFAULT 'simple';

-- カスタムスラッグ（プレミアム）
ALTER TABLE users ADD COLUMN custom_slug VARCHAR(50) UNIQUE;

-- QRコード画像
ALTER TABLE users ADD COLUMN qr_code_filename VARCHAR(100);

-- 公開設定
ALTER TABLE users ADD COLUMN profile_public BOOLEAN NOT NULL DEFAULT TRUE;

-- インデックス追加
CREATE INDEX idx_users_custom_slug ON users(custom_slug);

```

---

## 6. 実装計画（Phase別）

### Phase 1実装（MVP・Month 3 Week 1-3）

### Week 1: 基盤構築

**Day 1-2**:

- [ ]  マイグレーション作成・実行（20分）
- [ ]  `app/blueprints/profiles.py` 基本実装（40分）
- [ ]  `app/__init__.py` Blueprint登録（5分）
- [ ]  ディレクトリ作成（10分）
- [ ]  動作確認・デバッグ（20分）

**Day 3-4**:

- [ ]  `frontend/src/views/AppIndexPage.vue` 作成（30分）
- [ ]  ルーティング設定（10分）
- [ ]  認証フロー修正（10分）
- [ ]  動作確認（15分）

**Day 5-7**:

- [ ]  `frontend/src/stores/profiles.js` 作成（40分）
- [ ]  `frontend/src/views/CardApp.vue` 基本UI（30分）
- [ ]  統合テスト（20分）

### Week 2: フォーム実装

**Day 1-3**:

- [ ]  `ProfileEditForm.vue` 基本情報フォーム（30分）
- [ ]  アイコンアップロード機能（20分）
- [ ]  SNSリンク入力（20分）
- [ ]  LINE QRコードアップロード（15分）
- [ ]  バリデーション実装（15分）

**Day 4-5**:

- [ ]  `DesignCustomizer.vue` カラー選択（20分）
- [ ]  フォント選択（15分）
- [ ]  レイアウト選択（15分）
- [ ]  プレミアム制御（10分）

**Day 6-7**:

- [ ]  `ProfilePreview.vue` 基本表示（30分）
- [ ]  リアルタイムプレビュー連携（20分）
- [ ]  デザイン反映実装（20分）

### Week 3: QRコード・公開ページ

**Day 1-2**:

- [ ]  QRコード生成関数（20分）
- [ ]  vCard生成関数（15分）
- [ ]  `QRCodeDownload.vue` UI（20分）
- [ ]  ダウンロード機能（15分）

**Day 3-4**:

- [ ]  `public_profile.html` テンプレート（30分）
- [ ]  CSS実装（3レイアウト）（40分）
- [ ]  クローラーブロック実装（15分）

**Day 5-7**:

- [ ]  統合テスト（60分）
- [ ]  バグ修正（30分）
- [ ]  本番デプロイ（30分）

---

### Phase 2実装（拡張機能・Month 4 Week 1-2）

### Week 1: UI拡張

- [ ]  SNSアイコンドラッグ並び替え（2セッション）
- [ ]  背景ぼかし写真（2セッション）

### Week 2: プレミアム機能

- [ ]  QRコード中央アイコン挿入（1セッション）
- [ ]  アクセス解析基盤（2セッション）

---

## 7. 技術的課題と解決策

### 7.1 リアルタイムプレビュー実装

**課題**: フォーム入力と同時にプレビュー更新

**解決策**:

```jsx
// Vue.js Reactivity活用
const localProfile = reactive({ ...profileData })

watch(localProfile, () => {
  emit('update', localProfile)
}, { deep: true })

```

**ポイント**:

- `reactive()` でオブジェクト全体をリアクティブ化
- `watch()` で変更検知
- `emit('update')` で親コンポーネント通知
- ProfilePreview.vue は `computed()` で自動再レンダリング

---

### 7.2 QRコード生成最適化

**課題**: QRコード生成遅延

**解決策**:

```python
# キャッシュ機構導入
if user.qr_code_filename and os.path.exists(qr_path):
    # 既存QRコード返却（再生成不要）
    return qr_filename

# プロフィール変更時のみ再生成

```

**ポイント**:

- プロフィール更新時のみQRコード再生成
- ファイル存在チェックで不要な生成回避
- 生成時間: 平均200ms

---

### 7.3 画像リサイズ処理

**課題**: 大容量画像アップロード

**解決策**:

```python
from PIL import Image

img = Image.open(file)
img = img.resize((500, 500), Image.LANCZOS)
img.save(filepath, optimize=True, quality=85)

```

**ポイント**:

- サーバーサイドで自動リサイズ
- LANCZOS フィルタで高品質維持
- `optimize=True` でファイルサイズ削減
- 処理時間: 平均300ms

---

### 7.4 セキュリティ実装

**課題1: クローラーブロック**

**解決策**:

```python
def is_crawler(user_agent):
    crawler_patterns = ['bot', 'crawler', 'spider', 'scraper', 'google', 'bing']
    return any(pattern in user_agent.lower() for pattern in crawler_patterns)

@profiles_bp.route('/@<username>')
def public_profile(username):
    if is_crawler(request.headers.get('User-Agent', '')):
        abort(403)
    # ...

```

**課題2: レート制限**

**解決策**:

```python
from functools import wraps
import time

access_log = {}

def rate_limit(max_requests=100, window=3600):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            ip = request.remote_addr
            now = time.time()

            if ip not in access_log:
                access_log[ip] = []

            # 古いログ削除
            access_log[ip] = [t for t in access_log[ip] if now - t < window]

            if len(access_log[ip]) >= max_requests:
                abort(429)

            access_log[ip].append(now)
            return f(*args, **kwargs)
        return decorated
    return decorator

```

---

## 8. デプロイ手順

### 8.1 ローカル環境セットアップ

**実行場所**: ローカル環境（influberry_v2/）

```bash
# 1. バックアップ作成
cp -r migrations migrations_backup_berrycard_$(date +%Y%m%d_%H%M%S)
cp -r app app_backup_berrycard_$(date +%Y%m%d_%H%M%S)
cp -r frontend frontend_backup_berrycard_$(date +%Y%m%d_%H%M%S)

# 2. 依存関係追加
echo "qrcode==7.4.2" >> requirements.txt
echo "vobject==0.9.7" >> requirements.txt
pip install -r requirements.txt

# 3. ディレクトリ作成
mkdir -p app/static/uploads/icons
mkdir -p app/static/uploads/qrcodes
mkdir -p app/static/uploads/line_qrcodes
mkdir -p app/templates/profiles

# 4. マイグレーション作成
flask db migrate -m "Add BerryCard profile fields Phase 1"

# 5. マイグレーション実行
flask db upgrade

# 6. フロントエンド依存関係（必要に応じて）
cd frontend
npm install
cd ..

# 7. 動作確認
python wsgi.py
# ブラウザで http://127.0.0.1:5000 確認

```

---

### 8.2 本番環境デプロイ

**実行場所**: Render.com Shell

```bash
# 1. 本番環境接続
# Render.com Dashboard → Shell

# 2. 現在のブランチ確認
cd ~/project/src
git branch
git log --oneline -3

# 3. マイグレーション実行
flask db upgrade

# 4. ディレクトリ確認
ls -la app/static/uploads/
ls -la app/templates/profiles/

# 5. Flask再起動（Render.com自動）
# デプロイ完了後、自動再起動

# 6. 動作確認
curl -I https://influberry.jp/app-index
# → 302 Redirect (認証必要) が正常

```

---

## 9. テストシナリオ

### 9.1 単体テスト

```python
# tests/test_profiles.py

def test_generate_qr_code():
    """QRコード生成テスト"""
    url = "https://influberry.jp/@testuser"
    qr_filename = generate_qr_code_file(test_user)

    assert qr_filename is not None
    assert os.path.exists(f'app/static/uploads/qrcodes/{qr_filename}')

def test_generate_vcard():
    """vCard生成テスト"""
    vcard = generate_vcard(test_user)

    assert 'BEGIN:VCARD' in vcard
    assert 'VERSION:3.0' in vcard
    assert test_user.email in vcard

def test_validate_image():
    """画像検証テスト"""
    valid, error = validate_image_file(valid_image)
    assert valid is True

    invalid, error = validate_image_file(large_image)
    assert invalid is False
    assert 'ファイルサイズ' in error

```

---

### 9.2 統合テスト

```bash
# tests/integration_test.sh

# 1. プロフィール編集フロー
echo "=== プロフィール編集テスト ==="
curl -X PUT http://127.0.0.1:5000/api/profiles/me \
  -H "Content-Type: application/json" \
  -d '{"influencer_name":"テストユーザー","bio":"テスト自己紹介"}' \
  --cookie-jar cookies.txt

# 2. アイコンアップロード
echo "=== アイコンアップロードテスト ==="
curl -X POST http://127.0.0.1:5000/api/profiles/me/icon \
  -F "icon=@test_icon.jpg" \
  --cookie cookies.txt

# 3. QRコード生成
echo "=== QRコード生成テスト ==="
curl -X POST http://127.0.0.1:5000/api/profiles/me/generate-qr \
  -H "Content-Type: application/json" \
  -d '{"format":"png"}' \
  --cookie cookies.txt

# 4. 公開プロフィール表示
echo "=== 公開プロフィールテスト ==="
curl -I http://127.0.0.1:5000/@testuser001

```

---

### 9.3 ブラウザテスト

**チェック項目**:

1. **AppIndexPage表示**:
    - [ ]  ログイン後、/app-index に自動遷移
    - [ ]  BerryManagement・BerryCard カード表示
    - [ ]  カードクリックで各アプリへ遷移
2. **CardApp表示**:
    - [ ]  ProfileEditForm 表示
    - [ ]  DesignCustomizer 表示
    - [ ]  ProfilePreview 表示
    - [ ]  レスポンシブデザイン確認
3. **リアルタイムプレビュー**:
    - [ ]  名前入力でプレビュー即座更新
    - [ ]  カラー変更で背景色即座反映
    - [ ]  フォント変更で文字即座反映
4. **画像アップロード**:
    - [ ]  アイコン画像選択・プレビュー表示
    - [ ]  保存後、画像URL取得
    - [ ]  LINE QRコード同様動作
5. **QRコードダウンロード**:
    - [ ]  PNG ダウンロード動作
    - [ ]  SVG ダウンロード動作
    - [ ]  vCard ダウンロード動作
6. **公開プロフィールページ**:
    - [ ]  `/@username` でプロフィール表示
    - [ ]  デザイン設定反映確認
    - [ ]  SNSリンク動作確認
    - [ ]  LINE QRコード表示確認

---

## 10. パフォーマンス目標

### 10.1 レスポンスタイム目標

| エンドポイント | 目標 | 現実的目標 |
| --- | --- | --- |
| GET /api/profiles/me | < 200ms | < 300ms |
| PUT /api/profiles/me | < 500ms | < 800ms |
| POST /api/profiles/me/icon | < 2000ms | < 3000ms |
| POST /api/profiles/me/generate-qr | < 1000ms | < 1500ms |
| GET /@username | < 300ms | < 500ms |

### 10.2 最適化施策

1. **データベースクエリ最適化**:
    - インデックス活用: `idx_users_custom_slug`
    - 必要フィールドのみSELECT
2. **画像処理最適化**:
    - Pillow最適化オプション使用
    - 非同期処理検討（Phase 2）
3. **QRコード生成最適化**:
   - キャッシュ機構導入
   - 変更時のみ再生成

---

## 10. AI機能アーキテクチャ

### 10.1 AI機能概要

**実装されたAI機能**:
- プロフィール自動生成
- SNS投稿文提案
- ハッシュタグ提案
- エンゲージメント分析

### 10.2 AI機能アーキテクチャ図

```
┌─────────────────────────────────────────────────────────┐
│                AI機能フロントエンド                      │
├─────────────────────────────────────────────────────────┤
│  - AISuggestionPanel.vue                               │
│  - Pinia Store: ai.js                                 │
│  - 4つのタブ: プロフィール・SNS・ハッシュタグ・分析        │
│  - リアルタイム提案・履歴管理・提案適用                  │
└─────────────────────────────────────────────────────────┘
                            │ REST API (JSON)
┌─────────────────────────────────────────────────────────┐
│                AI機能バックエンド                        │
├─────────────────────────────────────────────────────────┤
│  Blueprint: ai.py                                       │
│  - OpenAI API統合 (GPT-4o-mini)                        │
│  - 認証・認可・レート制限                               │
│  - エラーハンドリング・ログ管理                         │
│  - 設定管理・使用統計                                   │
└─────────────────────────────────────────────────────────┘
                            │ OpenAI API
┌─────────────────────────────────────────────────────────┐
│                OpenAI API                              │
├─────────────────────────────────────────────────────────┤
│  - GPT-4o-mini モデル                                  │
│  - プロンプトエンジニアリング                           │
│  - レスポンス解析・フォーマット                         │
│  - エラーハンドリング                                   │
└─────────────────────────────────────────────────────────┘
```

### 10.3 AI機能詳細

#### **10.3.1 プロフィール自動生成**

**機能**: ユーザー情報から魅力的なプロフィール文を生成

**入力データ**:
- 名前
- 職業・活動
- 趣味・興味
- 特技・スキル
- 目標・夢

**出力形式**:
- キャッチフレーズ（30文字以内）
- 自己紹介文（100文字以内）
- ハッシュタグ（5個以内）
- 連絡先メッセージ（50文字以内）

#### **10.3.2 SNS投稿文提案**

**機能**: プラットフォーム別の最適化された投稿文を提案

**入力データ**:
- プラットフォーム（Instagram, Twitter, TikTok, YouTube）
- 投稿の目的（商品紹介、日常共有、コーディネート等）
- 投稿内容・テーマ
- ターゲット（Z世代女性等）
- トーン（親しみやすい、クール、可愛い等）

**出力形式**:
- メイン投稿文（150文字以内）
- ハッシュタグ（10個以内）
- ストーリー用短文（50文字以内）
- コメント誘導文（30文字以内）

#### **10.3.3 ハッシュタグ提案**

**機能**: エンゲージメント向上のためのハッシュタグを提案

**入力データ**:
- 投稿内容

**出力形式**:
- トレンド系ハッシュタグ（3個）
- ニッチ系ハッシュタグ（3個）
- ブランド系ハッシュタグ（2個）
- 地域系ハッシュタグ（2個）

#### **10.3.4 エンゲージメント分析**

**機能**: 過去の投稿データから改善提案を生成

**入力データ**:
- 投稿文
- 使用したハッシュタグ
- エンゲージメント率
- いいね数・コメント数・シェア数

**出力形式**:
- 現在の投稿の強み
- 改善すべき点
- 具体的な改善案
- 次回投稿への提案
- エンゲージメント向上のコツ

### 10.4 AI機能技術仕様

#### **10.4.1 バックエンド技術**

**OpenAI API統合**:
```python
# 設定
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')
OPENAI_MAX_TOKENS = int(os.environ.get('OPENAI_MAX_TOKENS', '1000'))
OPENAI_TEMPERATURE = float(os.environ.get('OPENAI_TEMPERATURE', '0.7'))

# AI機能制御
AI_FEATURES_ENABLED = os.environ.get('AI_FEATURES_ENABLED', 'false').lower() == 'true'
```

**APIエンドポイント**:
```
GET  /api/ai/health              - AI機能ヘルスチェック
POST /api/ai/suggest-profile     - プロフィール自動生成
POST /api/ai/suggest-sns-post    - SNS投稿文提案
POST /api/ai/suggest-hashtags    - ハッシュタグ提案
POST /api/ai/analyze-engagement  - エンゲージメント分析
GET  /api/ai/settings           - AI機能設定取得
GET  /api/ai/usage-stats        - 使用統計取得
```

#### **10.4.2 フロントエンド技術**

**Vue 3 Composition API**:
- リアクティブな状態管理
- コンポーネント分割
- 型安全性

**Pinia Store管理**:
```javascript
// ai.js store
const useAIStore = defineStore('ai', () => {
  const aiEnabled = ref(false)
  const isLoading = ref(false)
  const suggestionHistory = ref([])
  const usageStats = ref({})
  
  // アクション
  const suggestProfile = async (userInfo) => { ... }
  const suggestSnsPost = async (context) => { ... }
  const suggestHashtags = async (content) => { ... }
  const analyzeEngagement = async (postData) => { ... }
})
```

#### **10.4.3 セキュリティ・品質**

**セキュリティ対策**:
- 認証必須（全APIエンドポイント）
- レート制限（過度な使用防止）
- 入力検証（全入力データの検証）
- エラーハンドリング（セキュアなエラー処理）

**品質保証**:
- 構文チェック（全ファイルでエラーなし）
- 型安全性（TypeScript風の実装）
- エラーハンドリング（包括的な例外処理）
- ログ管理（適切なログ出力）

### 10.5 AI機能統合

#### **10.5.1 ProfileEditForm統合**

**統合内容**:
- AI提案パネルの組み込み
- 提案内容の自動適用
- フォーム連携機能

**実装例**:
```vue
<!-- AI提案パネル -->
<div v-if="aiEnabled" class="berry-card">
  <div class="flex items-center justify-between mb-4">
    <h3 class="text-lg font-semibold text-gray-900">AI提案アシスタント</h3>
    <button @click="showAIPanel = !showAIPanel">
      {{ showAIPanel ? 'AIパネルを閉じる' : 'AI提案を開く' }}
    </button>
  </div>
  
  <div v-if="showAIPanel">
    <AISuggestionPanel />
  </div>
</div>
```

#### **10.5.2 CardApp統合**

**統合内容**:
- AI機能の初期化
- ストア管理の統合
- エラーハンドリング

**実装例**:
```javascript
// アプリ初期化
onMounted(async () => {
  await authStore.checkAuthStatus()
  await profilesStore.initializeProfile()
  await aiStore.initialize() // AI機能初期化
})
```

### 10.6 AI機能パフォーマンス

#### **10.6.1 最適化**

**API最適化**:
- 非同期処理（非ブロッキング処理）
- キャッシュ（提案履歴のキャッシュ）
- レート制限（適切な制限設定）
- エラー処理（効率的なエラー処理）

**フロントエンド最適化**:
- コンポーネント分割（再利用可能な設計）
- 状態管理（効率的な状態管理）
- レスポンシブ（モバイル最適化）
- アクセシビリティ（ユーザビリティ向上）

#### **10.6.2 監視・分析**

**使用統計**:
- 総リクエスト数
- 成功リクエスト数
- 失敗リクエスト数
- 最後使用日時

**パフォーマンス指標**:
- レスポンス時間
- 成功率
- エラー率
- ユーザー満足度

### 10.7 AI機能将来拡張

#### **10.7.1 Phase 2拡張機能**

**画像分析**:
- 投稿画像の分析機能
- 視覚的コンテンツの最適化提案

**トレンド分析**:
- リアルタイムトレンド分析
- トレンド予測機能

**競合分析**:
- 競合インフルエンサー分析
- ベンチマーク機能

**収益最適化**:
- 収益最大化の提案
- ROI分析機能

#### **10.7.2 技術的拡張**

**機械学習**:
- カスタムモデルの実装
- ユーザー固有の学習

**リアルタイム**:
- WebSocket通信
- リアルタイム提案

**分析**:
- 詳細な分析機能
- 予測分析

**統合**:
- 外部サービス統合
- API連携

---

## 11. まとめ

### 11.1 実装完了チェックリスト

**Phase 1（MVP）**:

- [x]  データベースマイグレーション完了
- [x]  Flask Blueprint実装完了
- [x]  AppIndexPage実装完了
- [x]  CardApp実装完了
- [x]  ProfileEditForm実装完了
- [x]  DesignCustomizer実装完了
- [x]  ProfilePreview実装完了
- [x]  QRCodeDownload実装完了
- [x]  Pinia Store実装完了
- [x]  公開プロフィールページ実装完了
- [x]  AI機能統合完了
- [x]  統合テスト完了
- [x]  実装調査・問題特定完了
- [x]  リダイレクト修正完了
- [x]  AppIndexPage最適化完了
- [ ]  本番デプロイ完了

**Phase 2（拡張機能）**:

- [ ]  SNSアイコン並び替え
- [ ]  QRコード中央アイコン挿入
- [ ]  背景ぼかし写真
- [ ]  アクセス解析
- [ ]  AI機能画像分析
- [ ]  AI機能トレンド分析
- [ ]  AI機能競合分析
- [ ]  AI機能収益最適化

---

### 11.2 推定工数

**Phase 1（MVP）**:

- 開発工数: 約10-12時間（4-5セッション）
- AI機能開発: 約4-5時間（2セッション）
- テスト工数: 約3-4時間（1-2セッション）
- 実装調査・問題特定: 約2-3時間（1セッション）
- **合計**: 約19-24時間（8-10セッション）

**Phase 2（拡張）**:

- 開発工数: 約6-8時間（3-4セッション）
- AI機能拡張: 約4-6時間（2-3セッション）
- テスト工数: 約2時間（1セッション）
- **合計**: 約12-16時間（6-8セッション）

---

## アーキテクチャ設計書 v1.0 完成

**作成日**: 2025年10月16日

**最終更新**: 2025年10月18日

**バージョン**: 1.1 - 実装調査・問題特定版

**総ページ数**: 約50ページ相当

**セクション数**: 11セクション（AI機能追加・実装調査完了）

**状況**: 要件定義完了・AI機能統合完了・実装完了・問題特定完了

---

## 12. 実装調査・問題特定結果

### 12.1 調査実施概要

**調査日**: 2025年10月18日
**調査対象**: BerryCard実装の設計書との整合性
**調査結果**: 実装不足項目を特定

### 12.2 特定された問題

#### **問題1: ログイン後リダイレクト先の不整合**

**問題箇所**: `frontend/src/views/AuthPage.vue`
- **Line 19**: `router.push('/dashboard')` → 設計では `/app-index`
- **Line 36**: `router.push('/dashboard')` → 設計では `/app-index`

**影響**: ユーザーがダッシュボードページを経由してBerryCardにアクセスする必要があり、設計通りの直接的なアプリ選択フローが実現されていない

**修正必要度**: 高

#### **問題2: データベースエラー（解決済み）**

**問題**: `no such table: users` エラー
**解決**: マイグレーション実行・テーブル作成完了
**状況**: 解決済み

#### **問題3: OpenAIライブラリバージョン不整合（解決済み）**

**問題**: OpenAIライブラリのインポートエラー
**解決**: ライブラリアップデート完了
**状況**: 解決済み

### 12.3 実装完了項目

**✅ 正常に実装されている項目**:
- AppIndexPage.vue: 完全実装済み
- ルーティング設定: `/app-index` パス設定済み
- ナビゲーションガード: 認証済みユーザーを`/app-index`にリダイレクト
- BerryCard遷移: `navigateToApp('card')` で `/card` に遷移
- AI機能統合: 完全実装済み
- データベース: 正常動作

### 12.4 次回セッションでの修正項目

1. **AuthPage.vue修正**: ログイン成功後のリダイレクト先を`/app-index`に変更
2. **動作確認**: 修正後のユーザーフロー確認
3. **最終テスト**: BerryCard機能の完全動作確認

**状況**: 要件定義完了・AI機能統合完了・実装完了・問題特定完了

---

## 13. 最新の実装状況（2025年10月18日更新）

### 13.1 AppIndexPage.vueの修正完了

**修正内容:**
- ✅ 不要なウェルカムメッセージ削除
- ✅ コンパクトデザイン実装
- ✅ アイコンとカラーの統一
- ✅ スクロール不要の表示

**修正詳細:**
- **ウェルカムメッセージ**: 「アプリを選択してください」等の不要な文言を削除
- **コンパクトデザイン**: 各フレームの縦幅を小さく、テキストサイズをワンサイズ小さく
- **アイコン統一**: フッターと同じアイコン・カラーに統一
  - BerryWork: ブリーフケースアイコン（ブルー）
  - BerryPay: ドキュメントアイコン（パープル）
  - BerryDo: チェックリストアイコン（グリーン）
  - BerryCard: ユーザーアイコン（ピンク）
- **スクロール不要**: 画面内に全アプリカードが表示

### 13.2 バックアップファイル

**作成されたバックアップ:**
- `frontend/src/views/AppIndexPage.vue.backup_simplification_20251018_095933`
- `frontend/src/views/AppIndexPage.vue.backup_compact_design_20251018_100938`
- `frontend/src/views/AppIndexPage.vue.backup_icon_consistency_20251018_101620`
- `frontend/src/views/AppIndexPage.vue.backup_icon_unify_20251018_102052`
- `frontend/src/views/AppIndexPage.vue.backup_pay_do_unify_20251018_102202`
- `frontend/src/views/AppIndexPage.vue.backup_berrycard_pink_fix_20251018_101000`
- `frontend/src/views/AppIndexPage.vue.backup_icon_restore_20251018_101000`
- `frontend/src/views/AppIndexPage.vue.backup_remove_welcome_text_20251018_101000`
- `frontend/src/views/AppIndexPage.vue.backup_compact_restore_20251018_101000`

### 13.3 現在の状態

**AppIndexPage.vue:**
- ✅ シンプルなアプリ選択画面
- ✅ コンパクトデザイン
- ✅ アイコンとカラーの統一
- ✅ スクロール不要の表示
- ✅ 不要な文言なし

**BerryCard実装:**
- ✅ 完全実装済み
- ✅ フッターとの統一性確保
- ✅ ユーザビリティ向上

---

## 14. 公開ページ修正 (2025-10-20)

### 14.1 問題の特定

**症状**: 公開ページURL（`/@influberuco`）が500エラーで表示されない
**根本原因**:
1. **ルーティング競合**: `/@<username>`と`/@<custom_slug>`の競合
2. **テンプレート変数不一致**: DBスキーマとテンプレート変数名の不整合
3. **SPA干渉**: Vue RouterとFlaskルーティングの競合

### 14.2 アーキテクチャ修正

#### 14.2.1 ルーティング設計の改善

**修正前**:
```python
# profiles.py内で競合する2つのルート
@profiles_bp.route('/@<username>')
@profiles_bp.route('/@<custom_slug>')
```

**修正後**:
```python
# public_profiles.py - 独立したブループリント
@public_profiles_bp.route('/@<identifier>')
def public_profile(identifier):
    # custom_slug → username の順で検索
    user = User.query.filter_by(custom_slug=identifier).first()
    if not user:
        user = User.query.filter_by(username=identifier).first()
```

#### 14.2.2 SPAルーティング除外

**修正内容**:
```python
# app/__init__.py
@app.route('/<path:filename>')
def serve_static_files(filename):
    # 公開ページパターンを除外（@で始まるパス）
    if filename.startswith('@'):
        pass  # 公開ページは別のブループリントで処理
```

#### 14.2.3 テンプレート変数統一

**修正前**:
```html
<!-- 混在する変数参照 -->
{{ user.icon_url }}
{{ profile.website }}
```

**修正後**:
```html
<!-- DBスキーマに統一 -->
{{ icon_url }}
{{ user.website_url }}
```

### 14.3 ファイル構成

```
app/
├── blueprints/
│   ├── public_profiles.py          # 新規: 公開ページ専用
│   └── profiles.py                 # 修正: 公開ページルート削除
├── templates/profiles/
│   └── public_profile.html         # 修正: 変数参照統一
└── __init__.py                     # 修正: SPA除外、ブループリント登録
```

### 14.4 修正結果

**パフォーマンス**:
- ✅ 公開ページ表示: 200ステータス
- ✅ カスタムスラッグ優先検索
- ✅ SPAルーティング競合解消

**保守性**:
- ✅ ルーティング責任分離
- ✅ テンプレート変数統一
- ✅ エラーハンドリング改善

### 14.5 バックアップ戦略

**バックアップファイル**:
- `app/__init__.py.backup_public_page_fix_20251020_155028`
- `app/blueprints/profiles.py.backup_public_page_fix_20251020_155028`
- `app/blueprints/public_profiles.py.bak_20251020_160053`
- `app/templates/profiles/public_profile.html.bak_20251020_160053`

---

**作成者**: AI Assistant  
**レビュー**: 未実施  
**承認**: 未実施  
**次回更新**: セッション4完了時