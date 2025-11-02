# BerryCard アーキテクチャ設計書 v1.1 - セッション1完了版

---

**作成日**: 2025年10月18日  
**更新日**: 2025年10月18日  
**バージョン**: 1.1 - セッション1完了版  
**対象**: InfluBerry BerryCard実装（セッション1完了）

---

## 1. セッション1完了状況

### 1.1 実装完了項目 ✅

**基盤構築:**
- ✅ 依存関係追加（qrcode==7.4.2, vobject==0.9.7）
- ✅ ディレクトリ構造作成（uploads/icons, qrcodes, line_qrcodes, templates/profiles）
- ✅ データベースマイグレーション実行（Usersテーブル拡張）
- ✅ Flask Blueprint基本実装（profiles.py）
- ✅ アプリケーション統合完了

**APIエンドポイント実装:**
- ✅ `GET /api/profiles/me` - プロフィール情報取得
- ✅ `PUT /api/profiles/me` - プロフィール情報更新
- ✅ `POST /api/profiles/me/icon` - アイコン画像アップロード
- ✅ `POST /api/profiles/me/line-qr` - LINE QRコードアップロード
- ✅ `POST /api/profiles/me/generate-qr` - QRコード生成
- ✅ `GET /api/profiles/me/download-qr/<format>` - QRコードダウンロード
- ✅ `GET /@<username>` - 公開プロフィール（ユーザー名）
- ✅ `GET /@<custom_slug>` - 公開プロフィール（カスタムスラッグ）

**データベース拡張:**
- ✅ プロフィール情報（bio, icon_filename, phone_number, company_name, website_url）
- ✅ SNSリンク（tiktok_url, instagram_url, twitter_url, youtube_url, threads_url）
- ✅ デザイン設定（card_color, card_font, card_layout）
- ✅ プレミアム機能（custom_slug）
- ✅ 公開設定（profile_public）
- ✅ QRコード画像（qr_code_filename）
- ✅ LINE QRコード（line_qr_filename）

**セキュリティ機能:**
- ✅ クローラーブロック（User-Agent判定）
- ✅ ファイルアップロード検証
- ✅ ファイルサイズ制限（5MB）
- ✅ 拡張子制限（PNG, JPG, JPEG）

---

## 2. システム構成図（セッション1完了版）

### 2.1 全体アーキテクチャ

```
┌─────────────────────────────────────────────────────────┐
│                   ユーザー（ブラウザ）                    │
└─────────────────────────────────────────────────────────┘
                            │ HTTPS
┌─────────────────────────────────────────────────────────┐
│              Vue.js 3 Frontend (Vite)                   │
├─────────────────────────────────────────────────────────┤
│  - AppIndexPage.vue (未実装)                           │
│  - CardApp.vue (未実装)                                │
│  - ProfileEditForm.vue (未実装)                         │
│  - DesignCustomizer.vue (未実装)                        │
│  - ProfilePreview.vue (未実装)                          │
│  - QRCodeDownload.vue (未実装)                          │
│  - Pinia Store: profiles.js (未実装)                   │
└─────────────────────────────────────────────────────────┘
                            │ REST API (JSON)
┌─────────────────────────────────────────────────────────┐
│               Flask Backend (Python)                    │
├─────────────────────────────────────────────────────────┤
│  - profiles.py (✅ 実装完了)                            │
│  - ファイルアップロード処理 (✅ 実装完了)                │
│  - QRコード生成 (✅ 実装完了)                            │
│  - 公開プロフィール (✅ 実装完了)                        │
│  - クローラーブロック (✅ 実装完了)                      │
└─────────────────────────────────────────────────────────┘
                            │ SQL
┌─────────────────────────────────────────────────────────┐
│              PostgreSQL Database                         │
├─────────────────────────────────────────────────────────┤
│  - users テーブル (✅ 拡張完了)                         │
│  - BerryCard用カラム (✅ 追加完了)                      │
│  - マイグレーション (✅ 実行完了)                       │
└─────────────────────────────────────────────────────────┘
                            │ File System
┌─────────────────────────────────────────────────────────┐
│              File Storage                                │
├─────────────────────────────────────────────────────────┤
│  - app/static/uploads/icons/ (✅ 作成完了)              │
│  - app/static/uploads/qrcodes/ (✅ 作成完了)            │
│  - app/static/uploads/line_qrcodes/ (✅ 作成完了)       │
│  - app/templates/profiles/ (✅ 作成完了)                │
└─────────────────────────────────────────────────────────┘
```

---

## 3. 実装済みファイル構造

### 3.1 新規作成ファイル

```
app/
├── blueprints/
│   └── profiles.py (✅ 新規作成・実装完了)
├── static/
│   └── uploads/
│       ├── icons/ (✅ ディレクトリ作成)
│       ├── qrcodes/ (✅ ディレクトリ作成)
│       └── line_qrcodes/ (✅ ディレクトリ作成)
└── templates/
    └── profiles/ (✅ ディレクトリ作成)

migrations/
└── versions/
    └── 17c0a24e93a2_add_berrycard_profile_fields_phase_1.py (✅ 作成・実行完了)
```

### 3.2 更新済みファイル

```
app/
├── __init__.py (✅ profiles Blueprint登録完了)
└── models/
    └── user.py (✅ BerryCard用カラム追加完了)

requirements.txt (✅ 依存関係追加完了)
```

---

## 4. データベーススキーマ（セッション1完了版）

### 4.1 Usersテーブル拡張

```sql
-- セッション1で追加されたカラム
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
ALTER TABLE users ADD COLUMN card_color VARCHAR(20) DEFAULT 'peach' NOT NULL;
ALTER TABLE users ADD COLUMN card_font VARCHAR(50) DEFAULT 'Nunito' NOT NULL;
ALTER TABLE users ADD COLUMN card_layout VARCHAR(20) DEFAULT 'simple' NOT NULL;

-- プレミアム機能
ALTER TABLE users ADD COLUMN custom_slug VARCHAR(50);
ALTER TABLE users ADD CONSTRAINT uq_users_custom_slug UNIQUE (custom_slug);

-- QRコード・公開設定
ALTER TABLE users ADD COLUMN qr_code_filename VARCHAR(100);
ALTER TABLE users ADD COLUMN profile_public BOOLEAN DEFAULT 1 NOT NULL;
```

---

## 5. API仕様（セッション1完了版）

### 5.1 実装済みエンドポイント

#### プロフィール管理
```http
GET /api/profiles/me
PUT /api/profiles/me
```

#### ファイルアップロード
```http
POST /api/profiles/me/icon
POST /api/profiles/me/line-qr
```

#### QRコード生成・ダウンロード
```http
POST /api/profiles/me/generate-qr
GET /api/profiles/me/download-qr/<format>
```

#### 公開プロフィール
```http
GET /@<username>
GET /@<custom_slug>
```

### 5.2 リクエスト・レスポンス例

#### プロフィール情報取得
```json
GET /api/profiles/me
Response:
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "influencer_name": "テストユーザー",
  "bio": "自己紹介文",
  "icon_filename": "uuid.png",
  "phone_number": "090-1234-5678",
  "company_name": "テスト会社",
  "website_url": "https://example.com",
  "tiktok_url": "https://tiktok.com/@testuser",
  "instagram_url": "https://instagram.com/testuser",
  "twitter_url": "https://twitter.com/testuser",
  "youtube_url": "https://youtube.com/@testuser",
  "threads_url": "https://threads.net/@testuser",
  "line_qr_filename": "line_qr_uuid.png",
  "card_color": "peach",
  "card_font": "Nunito",
  "card_layout": "simple",
  "custom_slug": "my-custom-slug",
  "qr_code_filename": "qr_uuid.png",
  "profile_public": true,
  "plan_type": "premium"
}
```

---

## 6. セキュリティ実装（セッション1完了版）

### 6.1 クローラーブロック
```python
# User-Agent判定によるクローラーブロック
user_agent = request.headers.get('User-Agent', '').lower()
crawler_patterns = ['bot', 'crawler', 'spider', 'scraper', 'googlebot', 'bingbot']

if any(pattern in user_agent for pattern in crawler_patterns):
    abort(403)  # Forbidden
```

### 6.2 ファイルアップロード検証
```python
# ファイル拡張子制限
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# ファイルサイズ制限
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# ファイル検証
def validate_image_file(file):
    if not file or not allowed_file(file.filename):
        return False, "Invalid file type. Only PNG, JPG, JPEG allowed."
    
    if file.content_length and file.content_length > MAX_FILE_SIZE:
        return False, "File too large. Maximum 5MB allowed."
    
    return True, "Valid file"
```

---

## 7. 次のセッション（セッション2）で実装予定

### 7.1 フロントエンド実装
- AppIndexPage.vue 作成
- CardApp.vue 作成
- ProfileEditForm.vue 作成
- DesignCustomizer.vue 作成
- ProfilePreview.vue 作成
- QRCodeDownload.vue 作成
- Pinia Store (profiles.js) 作成
- ルーティング設定

### 7.2 テンプレート・スタイリング
- 公開プロフィールテンプレート
- レスポンシブデザイン
- パステルカラーパレット
- Google Fonts統合

---

## 8. 技術的成果

### 8.1 既存アプリ完全保持
- InfluBerryの既存機能に一切影響なし
- 既存のAPIエンドポイントは全て保持
- 既存のデータベース構造は保持

### 8.2 段階的統合
- 新機能が既存アーキテクチャに自然に統合
- 既存の認証システムを活用
- 既存のエラーハンドリングを活用

### 8.3 拡張性確保
- プレミアム機能対応準備完了
- Phase 2対応準備完了
- セキュリティ機能実装完了

---

## 9. バックアップ情報

### 9.1 作成済みバックアップ
- `docs/requirements/berrycard_requirements_v1.0_backup_session1_20251018_052304.md`
- `docs/architecture/berrycard_architecture_v1.0_backup_session1_20251018_052304.md`
- `app_backup_berrycard_session1_20251018_052304/`
- `frontend_backup_berrycard_session1_20251018_052304/`
- `migrations_backup_berrycard_session1_20251018_052304/`

### 9.2 復旧手順
```bash
# 緊急時の復旧手順
cd /Users/kurinobu/projects/influberry_v2

# アプリケーション復旧
rm -rf app
mv app_backup_berrycard_session1_20251018_052304 app

# フロントエンド復旧
rm -rf frontend
mv frontend_backup_berrycard_session1_20251018_052304 frontend

# マイグレーション復旧
rm -rf migrations
mv migrations_backup_berrycard_session1_20251018_052304 migrations
```

---

## 10. まとめ

セッション1では、BerryCardの基盤構築が完了しました。既存のInfluBerryアプリケーションは完全に保持されており、新機能が安全に統合されています。次のセッション2では、フロントエンドの実装に進むことができます。
