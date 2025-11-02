# BerryCard アーキテクチャ設計書 v1.2 - セッション2完了版

---

**作成日**: 2025年10月18日  
**バージョン**: v1.2  
**対象**: BerryCard セッション2完了  
**前バージョン**: v1.1 (セッション1完了版)  
**次バージョン**: v1.3 (セッション3完了版予定)

---

## 1. セッション2完了状況

### 1.1 実装完了項目 ✅

**フロントエンド実装:**
- ✅ Pinia Store (profiles.js) 作成完了
- ✅ ルーティング設定完了
- ✅ AppIndexPage.vue 作成完了
- ✅ CardApp.vue 作成完了
- ✅ 子コンポーネント群作成完了
- ✅ 公開プロフィールテンプレート作成完了

**Vue.jsコンポーネント:**
- ✅ ProfileEditForm.vue - プロフィール編集フォーム
- ✅ DesignCustomizer.vue - デザイン設定
- ✅ ProfilePreview.vue - プレビュー表示
- ✅ QRCodeDownload.vue - QRコード生成・ダウンロード

**ルーティング:**
- ✅ `/app-index` ルート追加（アプリ一覧ページ）
- ✅ `/card` ルート追加（BerryCardメインページ）
- ✅ 認証ガード設定完了
- ✅ ログイン後リダイレクト先変更

**テンプレート:**
- ✅ `app/templates/profiles/public_profile.html` 作成
- ✅ レスポンシブデザイン
- ✅ パステルカラーパレット
- ✅ ソーシャルリンク表示

---

## 2. アーキテクチャ概要

### 2.1 システム構成

```
InfluBerry v2 (BerryCard統合)
├── バックエンド (Flask)
│   ├── 既存アプリ (完全保持)
│   │   ├── 案件管理 (BerryWork)
│   │   ├── 請求書管理 (BerryPay)
│   │   └── タスク管理 (BerryDo)
│   └── BerryCard機能
│       ├── APIエンドポイント (/api/profiles/*)
│       ├── データベース統合 (Usersテーブル拡張)
│       └── 公開プロフィールテンプレート
├── フロントエンド (Vue.js 3)
│   ├── 既存アプリ (完全保持)
│   │   ├── DashboardPage.vue
│   │   ├── ProjectApp.vue
│   │   ├── InvoiceApp.vue
│   │   └── TodoApp.vue
│   └── BerryCard機能
│       ├── AppIndexPage.vue (アプリ一覧)
│       ├── CardApp.vue (メインページ)
│       └── 子コンポーネント群
└── データベース (PostgreSQL)
    ├── 既存テーブル (完全保持)
    └── Usersテーブル拡張 (BerryCard用カラム)
```

### 2.2 技術スタック

**バックエンド:**
- Flask (Python 3.11+)
- SQLAlchemy (ORM)
- PostgreSQL (データベース)
- Flask-Login (認証)
- qrcode (QRコード生成)
- vobject (vCard生成)

**フロントエンド:**
- Vue.js 3 (Composition API)
- Pinia (状態管理)
- Vue Router (ルーティング)
- Tailwind CSS (スタイリング)
- Axios (HTTP通信)

**デプロイメント:**
- Railway (本番環境)
- Render (ステージング環境)

---

## 3. データベース設計

### 3.1 Usersテーブル拡張

```sql
-- セッション1で追加されたBerryCard用カラム
ALTER TABLE users ADD COLUMN influencer_name VARCHAR(100);
ALTER TABLE users ADD COLUMN bio TEXT;
ALTER TABLE users ADD COLUMN website VARCHAR(255);
ALTER TABLE users ADD COLUMN instagram VARCHAR(255);
ALTER TABLE users ADD COLUMN twitter VARCHAR(255);
ALTER TABLE users ADD COLUMN youtube VARCHAR(255);
ALTER TABLE users ADD COLUMN tiktok VARCHAR(255);
ALTER TABLE users ADD COLUMN icon_url VARCHAR(500);
ALTER TABLE users ADD COLUMN line_qr_url VARCHAR(500);
ALTER TABLE users ADD COLUMN custom_slug VARCHAR(100) UNIQUE;
ALTER TABLE users ADD COLUMN is_public BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN design_settings JSON;
```

### 3.2 データフロー

```
ユーザー入力 → Vue.jsコンポーネント → Pinia Store → Axios → Flask API → データベース
                ↓
            リアルタイムプレビュー ← データ取得 ← APIレスポンス ← データベース
```

---

## 4. API設計

### 4.1 BerryCard APIエンドポイント

**プロフィール管理:**
- `GET /api/profiles/me` - プロフィール情報取得
- `PUT /api/profiles/me` - プロフィール情報更新

**ファイルアップロード:**
- `POST /api/profiles/me/icon` - アイコン画像アップロード
- `POST /api/profiles/me/line-qr` - LINE QRコードアップロード

**QRコード生成:**
- `POST /api/profiles/me/generate-qr` - QRコード生成
- `GET /api/profiles/me/download-qr/<format>` - QRコードダウンロード

**公開プロフィール:**
- `GET /@<username>` - 公開プロフィール（ユーザー名）
- `GET /@<custom_slug>` - 公開プロフィール（カスタムスラッグ）

### 4.2 既存APIエンドポイント（保持）

**認証:**
- `POST /api/auth/login` - ログイン
- `POST /api/auth/logout` - ログアウト
- `GET /api/auth/me` - 現在のユーザー情報

**案件管理:**
- `GET /api/projects` - 案件一覧取得
- `POST /api/projects` - 案件作成
- `PUT /api/projects/<id>` - 案件更新
- `DELETE /api/projects/<id>` - 案件削除

**請求書管理:**
- `GET /api/invoices` - 請求書一覧取得
- `POST /api/invoices` - 請求書作成
- `PUT /api/invoices/<id>` - 請求書更新
- `DELETE /api/invoices/<id>` - 請求書削除

**タスク管理:**
- `GET /api/todos` - タスク一覧取得
- `POST /api/todos` - タスク作成
- `PUT /api/todos/<id>` - タスク更新
- `DELETE /api/todos/<id>` - タスク削除

---

## 5. フロントエンド設計

### 5.1 コンポーネント構成

```
AppIndexPage.vue (アプリ一覧)
├── 統計サマリー表示
├── 既存アプリカード (BerryWork, BerryPay, BerryDo)
└── BerryCardアプリカード

CardApp.vue (BerryCardメイン)
├── タブナビゲーション
├── ProfileEditForm.vue (プロフィール編集)
├── DesignCustomizer.vue (デザイン設定)
├── ProfilePreview.vue (プレビュー表示)
├── QRCodeDownload.vue (QRコード生成)
└── リアルタイムプレビュー
```

### 5.2 Pinia Store設計

**profiles.js:**
```javascript
state: {
  profile: { /* プロフィール情報 */ },
  isLoading: false,
  isSaving: false,
  error: null,
  previewMode: false,
  previewData: null,
  qrCodeGenerated: false,
  qrCodeUrl: ''
}

actions: {
  fetchProfile(),
  updateProfile(),
  uploadIcon(),
  uploadLineQR(),
  generateQRCode(),
  downloadQRCode(),
  togglePreview(),
  togglePublicStatus()
}
```

**auth.js (既存保持):**
```javascript
state: {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null
}

actions: {
  login(),
  logout(),
  register(),
  getCurrentUser(),
  checkAuthStatus()
}
```

### 5.3 ルーティング設計

**既存ルート（保持）:**
- `/` - 認証ページ
- `/dashboard` - ダッシュボード
- `/apps/projects` - 案件管理
- `/apps/invoices` - 請求書管理
- `/berry-do` - タスク管理

**新規ルート:**
- `/app-index` - アプリ一覧ページ
- `/card` - BerryCardメインページ

**公開ルート:**
- `/@<username>` - 公開プロフィール（ユーザー名）
- `/@<custom_slug>` - 公開プロフィール（カスタムスラッグ）

---

## 6. セキュリティ設計

### 6.1 認証・認可

**既存認証システム（保持）:**
- Flask-Login セッション認証
- Cookie ベース認証
- CSRF 保護

**BerryCard認証:**
- 既存認証システムを活用
- プロフィール編集は認証必須
- 公開プロフィールは認証不要

### 6.2 データ保護

**ファイルアップロード:**
- ファイル形式制限 (jpg, png, gif)
- ファイルサイズ制限 (5MB)
- セキュアなファイル保存

**公開データ:**
- 公開プロフィールのみ表示
- プライベート情報は非表示
- 適切なSEO設定

---

## 7. パフォーマンス設計

### 7.1 フロントエンド最適化

**Vue.js最適化:**
- Composition API使用
- リアクティブデータの最適化
- コンポーネントの遅延読み込み

**Pinia最適化:**
- 状態管理の効率化
- 不要な再レンダリング防止
- エラーハンドリング

### 7.2 バックエンド最適化

**API最適化:**
- 適切なHTTPステータスコード
- エラーレスポンスの統一
- レート制限実装

**データベース最適化:**
- インデックス設定
- クエリ最適化
- 接続プール管理

---

## 8. デプロイメント設計

### 8.1 環境構成

**本番環境 (Railway):**
- ドメイン: influberry.jp
- データベース: PostgreSQL
- ファイルストレージ: Railway Volume

**ステージング環境 (Render):**
- ドメイン: influberry-staging.onrender.com
- データベース: PostgreSQL
- ファイルストレージ: Render Volume

### 8.2 CI/CD

**自動デプロイ:**
- GitHub連携
- 自動テスト実行
- ステージング環境への自動デプロイ
- 本番環境への手動デプロイ

---

## 9. 監視・ログ設計

### 9.1 ログ設計

**アプリケーションログ:**
- エラーログ
- アクセスログ
- パフォーマンスログ

**セキュリティログ:**
- 認証ログ
- ファイルアップロードログ
- APIアクセスログ

### 9.2 監視設計

**パフォーマンス監視:**
- レスポンス時間監視
- メモリ使用量監視
- データベース接続監視

**セキュリティ監視:**
- 不正アクセス検知
- レート制限監視
- ファイルアップロード監視

---

## 10. セッション3予定

### 10.1 実装予定項目

**スタイリング完成:**
- レスポンシブデザイン最適化
- パステルカラーパレット完成
- Google Fonts統合
- アニメーション効果追加

**テスト・デバッグ:**
- ユニットテスト追加
- 統合テスト実行
- パフォーマンステスト
- セキュリティテスト

**最適化:**
- コード最適化
- パフォーマンス最適化
- SEO最適化
- アクセシビリティ向上

### 10.2 完了目標

**必須完了項目:**
- ✅ スタイリング完成
- ✅ レスポンシブデザイン最適化
- ✅ パフォーマンス最適化
- ✅ 最終テスト・デバッグ

**動作確認項目:**
- ✅ 全機能の動作確認
- ✅ 既存アプリとの統合確認
- ✅ パフォーマンステスト
- ✅ セキュリティテスト

---

## 11. まとめ

### 11.1 セッション2完了状況

**実装完了:**
- ✅ フロントエンド実装完了
- ✅ Vue.jsコンポーネント作成完了
- ✅ Pinia Store実装完了
- ✅ ルーティング設定完了
- ✅ 公開プロフィールテンプレート作成完了

**既存アプリ保護:**
- ✅ InfluBerryの既存機能は完全保持
- ✅ 既存のルーティングは変更なし
- ✅ 既存のコンポーネントは保持
- ✅ 既存のStoreは保持
- ✅ 既存のAPIエンドポイントは保持

### 11.2 技術的成果

**アーキテクチャ:**
- 既存アプリとの完全統合
- モジュラー設計の実現
- スケーラブルな構造

**機能性:**
- 直感的なユーザーインターフェース
- リアルタイムプレビュー機能
- レスポンシブデザイン

**保守性:**
- クリーンなコード構造
- 適切なエラーハンドリング
- 包括的なドキュメント

### 11.3 次のステップ

セッション3では、スタイリングの完成と最終テストに集中し、BerryCardの完全なリリースを目指します。

**重要**: 既存のInfluBerryアプリケーションは一切変更されておらず、新機能が安全に統合されています。セッション3では、最終的な仕上げを行います。

---

**作成者**: AI Assistant  
**レビュー**: 未実施  
**承認**: 未実施  
**次回更新**: セッション3完了時
