# InfluBerry BerryCard 要件定義書

**作成日**: 2025年10月16日

**バージョン**: 1.0 - 初版ドラフト

**対象**: Month 3実装・QRコード名刺アプリ

---

## 1. プロジェクト概要

### 1.1 目的・目標

**アプリ名**: BerryCard（ベリーカード）

**日本語表示名**: デジタル名刺・QRコード

**目的**: Z世代女子インフルエンサーのデジタル名刺作成・QRコード共有

**ターゲット**: 既存InfluBerryユーザー

**開発期間**: Month 3（2025年11月）実装予定

### 1.2 ビジネス目標

**主目標**:

- ユーザー数増加（デジタル名刺の需要取り込み）
- ユーザー定着化（日常的に使用される機能追加）
- 有料化促進（プレミアム機能の差別化）

**KPI**:

- BerryCard利用率: 70%以上（既存ユーザーのうち）
- プレミアム転換率: 20%（BerryCard利用者のうち）
- 月間QRコード生成数: 1,000回以上

### 1.3 利用シーン

- 紙の名刺にQRコード貼り付け
- オフ会・イベントで名刺代わりにQRコード表示
- SNS投稿でプロフィール共有
- 企業案件での自己紹介資料

---

## 2. 機能要件

### 2.1 プロフィール編集機能（Phase 1）

### 2.1.1 基本情報

**必須項目**:

- インフルエンサー名（`users.influencer_name` 使用）
- アイコン画像（ファイルアップロード）

**任意項目**:

- 自己紹介文（bio）
- 会社名（company_name）
- メールアドレス（email）※Usersテーブルから自動取得
- 電話番号（phone_number）
- ウェブサイトURL（website_url）

### 2.1.2 SNSリンク

**対応SNS**:

- TikTok
- Instagram
- Twitter (X)
- YouTube
- Threads

**入力形式**:

- URLフルパス入力
- バリデーション: URLフォーマットチェック

**表示順序**:

- Phase 1: 固定順序（TikTok → Instagram → X → YouTube → Threads）
- Phase 2: ドラッグ並び替え機能追加

### 2.1.3 LINE QRコード埋め込み（Phase 1）

**機能**:

- ユーザーがLINE QRコード画像をアップロード
- プロフィールページに「LINEで友だち追加」セクション表示
- QRコード画像を表示

**実装詳細**:

- データベース: `line_qr_filename VARCHAR(100)`
- ファイル保存先: `app/static/uploads/line_qrcodes/user_<id>_line_qr.png`
- 最大ファイルサイズ: 5MB
- 対応形式: JPEG, PNG

---

### 2.2 デザインカスタマイズ機能

### 2.2.1 カラー設定（24色）

**パステル・くすみ系カラーパレット**:

| カテゴリ | カラー名 | HEXコード |
| --- | --- | --- |
| ピンク系 | ピーチ | #FFD4C4 |
| ピンク系 | ローズ | #F4C2C2 |
| ピンク系 | サクラ | #FFB7C5 |
| ピンク系 | コーラル | #FF9999 |
| パープル系 | ラベンダー | #E6E6FA |
| パープル系 | モーブ | #E0B0FF |
| パープル系 | ライラック | #C8A2C8 |
| パープル系 | ダスティパープル | #B4A7D6 |
| ブルー系 | スカイブルー | #B0E0E6 |
| ブルー系 | パウダーブルー | #B0C4DE |
| ブルー系 | ミントブルー | #9FE2BF |
| ブルー系 | ベビーブルー | #A7C7E7 |
| グリーン系 | モスグリーン | #B2C9AB |
| グリーン系 | セージ | #BCB88A |
| グリーン系 | ミント | #C1E1C1 |
| グリーン系 | パステルグリーン | #B4E7CE |
| ブラウン系 | サンドベージュ | #F5E6D3 |
| ブラウン系 | モカブラウン | #D4A574 |
| ブラウン系 | カフェラテ | #C8B5A2 |
| ブラウン系 | グレージュ | #D3C5BA |
| ニュートラル | アイボリー | #FFFFF0 |
| ニュートラル | ベージュ | #F5F5DC |
| ニュートラル | ダスティグレー | #C9C9C9 |
| ニュートラル | ソフトホワイト | #FAFAFA |

**デフォルト**: ピーチ（#FFD4C4）

**プラン別制限**:

- フリー: デフォルト（ピーチ）のみ
- プレミアム: 全24色選択可能

### 2.2.2 フォント設定（10体）

**Google Fonts採用**:

| カテゴリ | フォント名 | 特徴 |
| --- | --- | --- |
| 丸文字系 | Nunito | 親しみやすい・読みやすい |
| 丸文字系 | Quicksand | 柔らかい・モダン |
| 丸文字系 | Poppins | シンプル・クリーン |
| 手書き系 | Pacifico | カジュアル・おしゃれ |
| 手書き系 | Caveat | 手書き風・親近感 |
| 手書き系 | Dancing Script | エレガント・華やか |
| 大人可愛い系 | Playfair Display | 高級感・洗練 |
| 大人可愛い系 | Raleway | シンプル・スタイリッシュ |
| シンプル系 | Lato | ビジネス・読みやすい |
| シンプル系 | Open Sans | クリーン・万能 |

**デフォルト**: Nunito

**プラン別制限**:

- フリー: デフォルト（Nunito）のみ
- プレミアム: 全10体選択可能

### 2.2.3 レイアウト設定（3種）

**1. シンプル名刺型**（デフォルト）:

- 横長カード
- 中央にQRコードと名前
- SNSアイコンを下部に配置
- ビジネス・フォーマル向け

**2. SNSプロフィール型**:

- 円形アイコンを上部中央
- 名前・自己紹介文を中央
- SNSアイコンをグリッド配置
- カジュアル・SNS風

**3. ストーリーカード型**:

- 背景に淡いグラデーション
- テキストを中央配置
- ビジュアル重視・おしゃれ

**プラン別制限**:

- フリー: シンプル名刺型のみ
- プレミアム: 全3種選択可能

---

### 2.3 リアルタイムプレビュー機能（Phase 1・高優先度）

### 2.3.1 機能概要

**目的**: ユーザーが編集結果を即座に確認できる

**実装方式**:

- 左側: 編集フォーム
- 右側: リアルタイムプレビュー
- 入力変更時に即座にプレビュー更新

### 2.3.2 プレビュー対象

- インフルエンサー名
- 自己紹介文
- アイコン画像
- SNSリンク（アイコン表示）
- カラー設定
- フォント設定
- レイアウト設定

### 2.3.3 技術実装

**Vue.js Reactivity**:

```jsx
// CardApp.vueで実装
watch([profile.displayName, profile.bio, ...], () => {
  updatePreview()
})

```

**CSS動的クラス**:

```
<div
  :class="`card-${profile.cardLayout}`"
  :style="{
    backgroundColor: profile.cardColor,
    fontFamily: profile.cardFont
  }"
>

```

---

### 2.4 QRコード生成機能

### 2.4.1 生成タイミング

**自動生成**: プロフィール情報保存時

**生成内容**:

- プロフィールページURL: `https://influberry.jp/@username`
- プレミアム: カスタムスラッグURL `https://influberry.jp/c/custom-slug`

### 2.4.2 ダウンロード形式（3形式）

**1. PNG形式**:

- 用途: スマホ保存・SNS共有・紙の名刺印刷
- サイズ: 500x500px
- ファイル名: `username_qr.png`

**2. SVG形式**:

- 用途: 高品質印刷・Webサイト埋め込み
- 拡大しても劣化なし
- ファイル名: `username_qr.svg`

**3. vCard形式**:

- 用途: 電話帳登録・オフライン対応
- 含まれる情報: 名前・電話・メール・ウェブサイト・SNSリンク
- ファイル名: `username.vcf`

### 2.4.3 QRコード中央アイコン挿入（Phase 2・プレミアム）

**機能**:

- アイコン画像をQRコード中央に配置
- エラー訂正レベル「H」（30%欠損修復可能）
- アイコンサイズ: QRコード全体の20%

**実装**:

```python
import qrcode
from PIL import Image

def generate_qr_with_icon(url, icon_path):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data(url)
    qr_img = qr.make_image()

    # アイコン合成
    icon = Image.open(icon_path).resize((icon_size, icon_size))
    qr_img.paste(icon, center_pos)

    return qr_img

```

**プラン別制限**:

- フリー: 基本QRコードのみ
- プレミアム: アイコン挿入可能

---

### 2.5 プロフィールページ

### 2.5.1 URL形式

**フリープラン**:

```
https://influberry.jp/@username

```

**プレミアムプラン**:

```
https://influberry.jp/@username        # 継続利用可
https://influberry.jp/c/custom-slug    # 追加設定可

```

### 2.5.2 表示内容

**基本情報**:

- アイコン画像
- インフルエンサー名
- 自己紹介文

**連絡先情報**:

- メールアドレス
- 電話番号
- 会社名
- ウェブサイトURL

**SNSリンク**:

- TikTok, Instagram, X, YouTube, Threads
- アイコンボタン表示

**LINE QRコード**:

- 「LINEで友だち追加」セクション
- QRコード画像表示

### 2.5.3 デザイン反映

- ユーザーが選択したカラー・フォント・レイアウトを反映
- レスポンシブデザイン（PC・スマホ対応）

### 2.5.4 クローラー対策

**実装方法**: User-Agent判定

```python
# app/blueprints/profiles.py

@profiles_bp.route('/@<username>')
def public_profile_username(username):
    # クローラー判定
    user_agent = request.headers.get('User-Agent', '').lower()
    crawler_patterns = ['bot', 'crawler', 'spider', 'scraper']

    if any(pattern in user_agent for pattern in crawler_patterns):
        abort(403)  # Forbiddenエラー

    # 通常アクセス
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profiles/public_profile.html', user=user)

```

**robots.txt**:

```
User-agent: *
Disallow: /@*
Disallow: /c/*

```

**meta tag**:

```html
<meta name="robots" content="noindex, nofollow">

```

---

### 2.6 AppIndexPage統合（新規作成）

### 2.6.1 画面構成

**2カードレイアウト**:

```
┌─────────────────────────────────┐
│   BerryManagement               │
│   案件・請求書・タスク管理       │
│   [案件管理ダッシュボードへ]     │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│   BerryCard                     │
│   デジタル名刺・QRコード         │
│   [名刺アプリへ]                 │
└─────────────────────────────────┘

```

### 2.6.2 ルーティング

**新規ルート**:

```
/auth          → AuthPage.vue（ログイン・新規登録）
/app-index     → AppIndexPage.vue（アプリ一覧）← ログイン後最初の画面
/dashboard     → DashboardPage.vue（案件系ダッシュボード）
/projects      → ProjectApp.vue（BerryWork）
/invoices      → InvoiceApp.vue（BerryPay）
/todos         → TodoApp.vue（BerryDo）
/card          → CardApp.vue（BerryCard）← 新規作成

```

**ナビゲーション**:

- ログイン成功 → `/app-index` へリダイレクト
- 各カードクリック → 対応するアプリへ遷移

---

## 3. データベース設計

### 3.1 Usersテーブル拡張

**追加カラム一覧**:

```sql
-- 既存カラム（BerryCardで使用）
influencer_name      VARCHAR(100)    -- ✅既存・プロフィール表示名

-- 新規追加カラム（Phase 1）
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

-- 新規追加カラム（Phase 2）
ALTER TABLE users ADD COLUMN sns_order TEXT;  -- JSON '["tiktok","instagram",...]'
ALTER TABLE users ADD COLUMN qr_with_icon BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE users ADD COLUMN background_image_filename VARCHAR(100);
ALTER TABLE users ADD COLUMN background_blur_level INTEGER DEFAULT 5;

```

---

### 3.2 マイグレーション計画

**Phase 1マイグレーション**:

**実行場所**: ローカル環境

```bash
# バックアップ作成
cp -r migrations migrations_backup_berrycard_phase1_$(date +%Y%m%d_%H%M%S)

# マイグレーションファイル作成
flask db migrate -m "Add BerryCard profile fields Phase 1"

# マイグレーション実行（ローカル確認）
flask db upgrade

# 構文チェック
python -m py_compile migrations/versions/*.py

```

**本番環境デプロイ**:

```bash
# Render.com Shellで実行
cd ~/project/src
flask db upgrade

```

---

## 4. 画面設計

### 4.1 AppIndexPage.vue（新規作成）

**コンポーネント構造**:

```
<template>
  <div class="app-index-page">
    <header>
      <h1>InfluBerry アプリ一覧</h1>
      <UserSettings />
    </header>

    <main>
      <div class="app-cards-grid">
        <!-- BerryManagement -->
        <AppCard
          title="BerryManagement"
          subtitle="案件・請求書・タスク管理"
          icon="briefcase"
          @click="navigateTo('/dashboard')"
        />

        <!-- BerryCard -->
        <AppCard
          title="BerryCard"
          subtitle="デジタル名刺・QRコード"
          icon="qrcode"
          @click="navigateTo('/card')"
        />
      </div>
    </main>
  </div>
</template>

```

---

### 4.2 CardApp.vue（新規作成）

**コンポーネント構造**:

```
<template>
  <div class="card-app">
    <header>
      <h1>BerryCard - デジタル名刺</h1>
      <button @click="navigateTo('/app-index')">← アプリ一覧へ</button>
    </header>

    <div class="edit-preview-layout">
      <!-- 左: 編集フォーム -->
      <div class="edit-panel">
        <ProfileEditForm />
        <DesignCustomizer />
        <QRCodeDownload />
      </div>

      <!-- 右: リアルタイムプレビュー -->
      <div class="preview-panel">
        <ProfilePreview />
      </div>
    </div>
  </div>
</template>

```

---

### 4.3 PublicProfilePage（新規作成・Flask Template）

**実装方式**: Jinja2テンプレート（SEO不要・シンプル実装）

```html
<!-- app/templates/profiles/public_profile.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="robots" content="noindex, nofollow">
    <title>{{ user.influencer_name }} - InfluBerry</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/profile.css') }}">
    <link href="https://fonts.googleapis.com/css2?family={{ user.card_font }}" rel="stylesheet">
</head>
<body style="background-color: {{ user.card_color }}; font-family: {{ user.card_font }};">
    <div class="profile-card layout-{{ user.card_layout }}">
        <!-- アイコン -->
        <img src="{{ url_for('static', filename='uploads/icons/' + user.icon_filename) }}" alt="アイコン">

        <!-- 基本情報 -->
        <h1>{{ user.influencer_name }}</h1>
        <p>{{ user.bio }}</p>

        <!-- SNSリンク -->
        <div class="sns-links">
            {% if user.tiktok_url %}
            <a href="{{ user.tiktok_url }}"><img src="/icons/tiktok.svg"></a>
            {% endif %}
            <!-- ... -->
        </div>

        <!-- LINE QRコード -->
        {% if user.line_qr_filename %}
        <div class="line-qr-section">
            <p>LINEで友だち追加</p>
            <img src="{{ url_for('static', filename='uploads/line_qrcodes/' + user.line_qr_filename) }}">
        </div>
        {% endif %}
    </div>
</body>
</html>

```

---

## 5. 技術スタック

### 5.1 Backend（Flask）

**新規Blueprint**:

- `app/blueprints/profiles.py`
    - プロフィール編集API
    - 公開プロフィールページ
    - QRコード生成API

**ライブラリ追加**:

```
qrcode==7.4.2          # QRコード生成
Pillow==10.1.0         # 画像処理
vobject==0.9.7         # vCard生成

```

### 5.2 Frontend（Vue.js）

**新規コンポーネント**:

- `AppIndexPage.vue`（アプリ一覧）
- `CardApp.vue`（BerryCard メイン）
- `ProfileEditForm.vue`（プロフィール編集フォーム）
- `DesignCustomizer.vue`（デザインカスタマイズUI）
- `ProfilePreview.vue`（リアルタイムプレビュー）
- `QRCodeDownload.vue`（QRコードダウンロード）

**新規Store**:

```jsx
// src/stores/profiles.js
import { defineStore } from 'pinia'

export const useProfileStore = defineStore('profiles', {
  state: () => ({
    profile: {},
    qrCodes: {}
  }),
  actions: {
    async fetchProfile() { ... },
    async updateProfile(data) { ... },
    async generateQRCode() { ... }
  }
})

```

---

## 6. 非機能要件

### 6.1 パフォーマンス

- QRコード生成: 1秒以内
- プロフィールページ表示: 2秒以内
- 画像アップロード: 5MB以内・5秒以内
- リアルタイムプレビュー更新: 100ms以内

### 6.2 セキュリティ

- クローラーブロック（User-Agent判定）
- レート制限（同一IPから100リクエスト/時間）
- ファイルアップロード検証（MIME type・拡張子）
- XSS対策（入力サニタイズ）

### 6.3 スケーラビリティ

- 画像ストレージ: `app/static/uploads/`
    - `icons/`: アイコン画像
    - `qrcodes/`: QRコード画像
    - `line_qrcodes/`: LINE QRコード
    - `backgrounds/`: 背景画像（Phase 2）
- 将来的にCDN導入検討（Cloudflare等）

---

## 7. 開発スケジュール

### Phase 1実装（Month 3・Week 1-3）

**Week 1**:

- AppIndexPage.vue作成
- Usersテーブル拡張マイグレーション
- profiles.py Blueprint基本実装

**Week 2**:

- CardApp.vue メインUI実装
- ProfileEditForm.vue実装
- リアルタイムプレビュー実装
- LINE QRコード埋め込み実装

**Week 3**:

- QRコード生成機能実装（3形式）
- 公開プロフィールページ実装
- デザインカスタマイズ実装
- 統合テスト・デプロイ

### Phase 2実装（Month 4・Week 1-2）

**拡張機能**:

- SNSアイコン並び替え
- QRコード中央アイコン挿入（プレミアム）
- 背景ぼかし写真（プレミアム）
- アクセス解析・統計

---

## 8. テスト計画

### 8.1 単体テスト

- QRコード生成関数テスト
- vCard生成テスト
- 画像リサイズテスト
- URL生成テスト

### 8.2 統合テスト

- プロフィール編集→保存→QRコード生成フロー
- 公開プロフィールページ表示確認
- クローラーブロック動作確認

### 8.3 ブラウザテスト

- Chrome・Safari・Firefox動作確認
- スマホ実機テスト（Android・iOS）
- レスポンシブデザイン確認

---

## 9. リスク管理

### 9.1 技術リスク

| リスク | 発生確率 | 影響度 | 対策 |
| --- | --- | --- | --- |
| QRコード生成遅延 | 低 | 中 | 非同期処理・キャッシュ |
| 画像ストレージ容量不足 | 中 | 高 | 定期削除・CDN移行検討 |
| クローラー回避策 | 中 | 中 | レート制限強化 |

### 9.2 運用リスク

| リスク | 発生確率 | 影響度 | 対策 |
| --- | --- | --- | --- |
| スパム登録 | 中 | 中 | reCAPTCHA導入 |
| 不適切コンテンツ投稿 | 低 | 高 | 報告機能・モデレーション |

---

## 10. 成功指標（KPI）

### Month 3終了時（Phase 1完了）

- BerryCard利用率: 50%以上
- 月間QRコード生成数: 500回以上
- プロフィールページ閲覧数: 2,000回以上

### Month 4終了時（Phase 2完了）

- BerryCard利用率: 70%以上
- プレミアム転換率: 20%以上
- 月間QRコード生成数: 1,000回以上

---

## 11. 拡張機能ロードマップ

### Phase 2（Month 4）

- SNSアイコンドラッグ並び替え
- QRコード中央アイコン挿入
- 背景ぼかし写真

### Phase 3（Month 5以降）

- アクセス解析ダッシュボード
- 統計データ表示（プロフィール閲覧数・QRコードスキャン数）
- 複数プロフィール作成機能（プレミアム）
- NFCカード連携（NFC対応スマホでタップ共有）
- プロフィールページ独自ドメイン設定（プレミアム）

### Phase 4（Month 6以降）

- AIプロフィール文章生成
- プロフィールページアクセス制限（パスワード保護）
- チーム・組織向けプロフィール管理
- プロフィールページテンプレートマーケットプレイス

---

## 12. プレミアム機能一覧

### 12.1 フリープラン

**BerryCard機能**:

- ✅ プロフィール編集（基本情報・SNSリンク）
- ✅ LINE QRコード埋め込み
- ✅ QRコード生成（PNG, SVG, vCard）
- ✅ デフォルトデザイン（ピーチ・Nunito・シンプル名刺型）
- ✅ リアルタイムプレビュー
- ✅ プロフィールページURL: `@username`

**その他アプリ制限**:

- 請求書PDF: 月間1枚まで
- 案件管理: 無制限
- Todo管理: 無制限

### 12.2 プレミアムプラン（¥1,280/月）

**BerryCard拡張機能**:

- ✅ 全カラー選択可能（24色）
- ✅ 全フォント選択可能（10体）
- ✅ 全レイアウト選択可能（3種）
- ✅ QRコード中央アイコン挿入
- ✅ 背景ぼかし写真
- ✅ カスタムスラッグURL: `c/custom-slug`
- ✅ SNSアイコン並び替え
- ✅ アクセス解析・統計データ（Phase 3）
- ✅ 複数プロフィール作成（Phase 3）

**その他アプリ拡張**:

- 請求書PDF: 無制限
- 高度なUI/UXカスタマイズ

---

## 13. UI/UXデザイン詳細

### 13.1 カラーパレット実装

**CSS変数定義**:

```css
/* app/static/css/berrycard-colors.css */

:root {
  /* ピンク系 */
  --berry-peach: #FFD4C4;
  --berry-rose: #F4C2C2;
  --berry-sakura: #FFB7C5;
  --berry-coral: #FF9999;

  /* パープル系 */
  --berry-lavender: #E6E6FA;
  --berry-mauve: #E0B0FF;
  --berry-lilac: #C8A2C8;
  --berry-dusty-purple: #B4A7D6;

  /* ブルー系 */
  --berry-sky-blue: #B0E0E6;
  --berry-powder-blue: #B0C4DE;
  --berry-mint-blue: #9FE2BF;
  --berry-baby-blue: #A7C7E7;

  /* グリーン系 */
  --berry-moss-green: #B2C9AB;
  --berry-sage: #BCB88A;
  --berry-mint: #C1E1C1;
  --berry-pastel-green: #B4E7CE;

  /* ブラウン系 */
  --berry-sand-beige: #F5E6D3;
  --berry-mocha-brown: #D4A574;
  --berry-cafe-latte: #C8B5A2;
  --berry-greige: #D3C5BA;

  /* ニュートラル */
  --berry-ivory: #FFFFF0;
  --berry-beige: #F5F5DC;
  --berry-dusty-gray: #C9C9C9;
  --berry-soft-white: #FAFAFA;
}

```

**Vue.js動的適用**:

```
<template>
  <div
    class="profile-card"
    :style="{ backgroundColor: getColorCode(profile.cardColor) }"
  >
  </div>
</template>

<script setup>
const colorMap = {
  'peach': '#FFD4C4',
  'rose': '#F4C2C2',
  // ...
}

const getColorCode = (colorName) => colorMap[colorName]
</script>

```

### 13.2 フォント実装

**Google Fonts読み込み**:

```html
<!-- index.html -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&family=Quicksand:wght@400;600;700&family=Poppins:wght@400;600;700&family=Pacifico&family=Caveat:wght@400;700&family=Dancing+Script:wght@400;700&family=Playfair+Display:wght@400;700&family=Raleway:wght@400;600;700&family=Lato:wght@400;700&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">

```

**フォント選択UI**:

```
<template>
  <div class="font-selector">
    <label>フォント</label>
    <select v-model="profile.cardFont" :disabled="!isPremium">
      <option value="Nunito">Nunito（丸文字・親しみ）</option>
      <option value="Quicksand">Quicksand（丸文字・柔らか）</option>
      <option value="Poppins">Poppins（丸文字・モダン）</option>
      <option value="Pacifico">Pacifico（手書き・おしゃれ）</option>
      <option value="Caveat">Caveat（手書き・親近感）</option>
      <option value="Dancing Script">Dancing Script（手書き・華やか）</option>
      <option value="Playfair Display">Playfair Display（大人・高級感）</option>
      <option value="Raleway">Raleway（大人・スタイリッシュ）</option>
      <option value="Lato">Lato（シンプル・ビジネス）</option>
      <option value="Open Sans">Open Sans（シンプル・万能）</option>
    </select>
    <p v-if="!isPremium" class="premium-hint">
      ✨ プレミアムプランで全フォント利用可能
    </p>
  </div>
</template>

```

### 13.3 レイアウト実装

**1. シンプル名刺型（simple）**:

```html
<div class="layout-simple">
  <div class="card-header">
    <img class="icon-circular" :src="iconUrl">
    <h1 class="name">{{ profile.influencerName }}</h1>
  </div>
  <div class="card-body">
    <p class="bio">{{ profile.bio }}</p>
  </div>
  <div class="card-footer">
    <div class="qr-code">
      <img :src="qrCodeUrl">
    </div>
    <div class="sns-icons-horizontal">
      <a v-for="sns in snsLinks" :key="sns.name">
        <img :src="sns.icon">
      </a>
    </div>
  </div>
</div>

```

**2. SNSプロフィール型（sns）**:

```html
<div class="layout-sns">
  <div class="card-center">
    <img class="icon-large-circular" :src="iconUrl">
    <h1 class="name-large">{{ profile.influencerName }}</h1>
    <p class="bio-center">{{ profile.bio }}</p>

    <div class="sns-icons-grid">
      <a v-for="sns in snsLinks" :key="sns.name" class="sns-button">
        <img :src="sns.icon">
        <span>{{ sns.name }}</span>
      </a>
    </div>

    <div class="qr-code-small">
      <img :src="qrCodeUrl">
    </div>
  </div>
</div>

```

**3. ストーリーカード型（story）**:

```html
<div class="layout-story">
  <div class="gradient-background">
    <div class="card-vertical-center">
      <img class="icon-medium-circular" :src="iconUrl">
      <h1 class="name-artistic">{{ profile.influencerName }}</h1>
      <p class="bio-artistic">{{ profile.bio }}</p>

      <div class="sns-qr-combined">
        <div class="qr-code-large">
          <img :src="qrCodeUrl">
        </div>
        <div class="sns-icons-vertical">
          <a v-for="sns in snsLinks" :key="sns.name">
            <img :src="sns.icon">
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

```

---

## 14. API設計

### 14.1 プロフィール管理API

**エンドポイント一覧**:

### GET `/api/profiles/me`

**説明**: 現在のユーザーのプロフィール取得

**レスポンス**:

```json
{
  "id": 10,
  "username": "testuser001",
  "influencer_name": "テストインフルエンサー",
  "bio": "Z世代インフルエンサーです！",
  "icon_url": "/static/uploads/icons/user_10_icon.jpg",
  "phone_number": "090-1234-5678",
  "company_name": "テスト株式会社",
  "website_url": "https://example.com",
  "tiktok_url": "https://tiktok.com/@testuser",
  "instagram_url": "https://instagram.com/testuser",
  "twitter_url": "https://twitter.com/testuser",
  "youtube_url": "https://youtube.com/@testuser",
  "threads_url": "https://threads.net/@testuser",
  "line_qr_url": "/static/uploads/line_qrcodes/user_10_line_qr.png",
  "card_color": "peach",
  "card_font": "Nunito",
  "card_layout": "simple",
  "custom_slug": null,
  "qr_code_url": "/static/uploads/qrcodes/user_10_qr.png",
  "profile_public": true,
  "plan_type": "free"
}

```

---

### PUT `/api/profiles/me`

**説明**: プロフィール更新

**リクエスト**:

```json
{
  "influencer_name": "更新後の名前",
  "bio": "更新後の自己紹介文",
  "phone_number": "090-9876-5432",
  "company_name": "新会社名",
  "website_url": "https://newsite.com",
  "tiktok_url": "https://tiktok.com/@newuser",
  "instagram_url": "https://instagram.com/newuser",
  "twitter_url": "https://twitter.com/newuser",
  "youtube_url": "https://youtube.com/@newuser",
  "threads_url": "https://threads.net/@newuser",
  "card_color": "lavender",
  "card_font": "Quicksand",
  "card_layout": "sns"
}

```

**レスポンス**:

```json
{
  "success": true,
  "message": "プロフィールを更新しました",
  "profile": { /* 更新後のプロフィール全体 */ }
}

```

---

### POST `/api/profiles/me/icon`

**説明**: アイコン画像アップロード

**リクエスト**: `multipart/form-data`

```
icon: (file) image.jpg

```

**レスポンス**:

```json
{
  "success": true,
  "message": "アイコン画像をアップロードしました",
  "icon_url": "/static/uploads/icons/user_10_icon.jpg"
}

```

---

### POST `/api/profiles/me/line-qr`

**説明**: LINE QRコード画像アップロード

**リクエスト**: `multipart/form-data`

```
line_qr: (file) line_qr_code.png

```

**レスポンス**:

```json
{
  "success": true,
  "message": "LINE QRコードをアップロードしました",
  "line_qr_url": "/static/uploads/line_qrcodes/user_10_line_qr.png"
}

```

---

### POST `/api/profiles/me/generate-qr`

**説明**: QRコード生成

**リクエスト**:

```json
{
  "format": "png"  // "png", "svg", "vcard"のいずれか
}

```

**レスポンス**:

```json
{
  "success": true,
  "message": "QRコードを生成しました",
  "qr_code_url": "/static/uploads/qrcodes/user_10_qr.png",
  "download_url": "/api/profiles/me/download-qr?format=png"
}

```

---

### GET `/api/profiles/me/download-qr`

**説明**: QRコードダウンロード

**クエリパラメータ**:

- `format`: `png` / `svg` / `vcard`

**レスポンス**: ファイルダウンロード

```
Content-Type: image/png (or image/svg+xml, text/vcard)
Content-Disposition: attachment; filename="testuser001_qr.png"

```

---

### GET `/@<username>`

**説明**: 公開プロフィールページ（HTML）

**レスポンス**: HTMLページ（Jinja2テンプレート）

---

### GET `/c/<custom_slug>`

**説明**: カスタムスラッグ公開プロフィールページ（プレミアム）

**レスポンス**: HTMLページ（Jinja2テンプレート）

---

### 14.2 Flask Blueprint実装

**ファイル**: `app/blueprints/profiles.py`

```python
# app/blueprints/profiles.py

from flask import Blueprint, request, jsonify, render_template, send_file, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import qrcode
import vobject
from PIL import Image
import os

profiles_bp = Blueprint('profiles', __name__)

# ===== API Endpoints =====

@profiles_bp.route('/api/profiles/me', methods=['GET'])
@login_required
def get_profile():
    """現在のユーザーのプロフィール取得"""
    user = current_user
    return jsonify({
        'id': user.id,
        'username': user.username,
        'influencer_name': user.influencer_name,
        'bio': user.bio,
        'icon_url': f'/static/uploads/icons/{user.icon_filename}' if user.icon_filename else None,
        'phone_number': user.phone_number,
        'company_name': user.company_name,
        'website_url': user.website_url,
        'tiktok_url': user.tiktok_url,
        'instagram_url': user.instagram_url,
        'twitter_url': user.twitter_url,
        'youtube_url': user.youtube_url,
        'threads_url': user.threads_url,
        'line_qr_url': f'/static/uploads/line_qrcodes/{user.line_qr_filename}' if user.line_qr_filename else None,
        'card_color': user.card_color,
        'card_font': user.card_font,
        'card_layout': user.card_layout,
        'custom_slug': user.custom_slug,
        'qr_code_url': f'/static/uploads/qrcodes/{user.qr_code_filename}' if user.qr_code_filename else None,
        'profile_public': user.profile_public,
        'plan_type': user.plan_type
    })

@profiles_bp.route('/api/profiles/me', methods=['PUT'])
@login_required
def update_profile():
    """プロフィール更新"""
    data = request.get_json()
    user = current_user

    # 基本情報更新
    if 'influencer_name' in data:
        user.influencer_name = data['influencer_name']
    if 'bio' in data:
        user.bio = data['bio']
    if 'phone_number' in data:
        user.phone_number = data['phone_number']
    if 'company_name' in data:
        user.company_name = data['company_name']
    if 'website_url' in data:
        user.website_url = data['website_url']

    # SNSリンク更新
    if 'tiktok_url' in data:
        user.tiktok_url = data['tiktok_url']
    if 'instagram_url' in data:
        user.instagram_url = data['instagram_url']
    if 'twitter_url' in data:
        user.twitter_url = data['twitter_url']
    if 'youtube_url' in data:
        user.youtube_url = data['youtube_url']
    if 'threads_url' in data:
        user.threads_url = data['threads_url']

    # デザイン設定更新
    if 'card_color' in data:
        # プレミアムチェック
        if user.plan_type != 'premium' and data['card_color'] != 'peach':
            return jsonify({'success': False, 'message': 'カラー変更はプレミアムプラン限定です'}), 403
        user.card_color = data['card_color']

    if 'card_font' in data:
        if user.plan_type != 'premium' and data['card_font'] != 'Nunito':
            return jsonify({'success': False, 'message': 'フォント変更はプレミアムプラン限定です'}), 403
        user.card_font = data['card_font']

    if 'card_layout' in data:
        if user.plan_type != 'premium' and data['card_layout'] != 'simple':
            return jsonify({'success': False, 'message': 'レイアウト変更はプレミアムプラン限定です'}), 403
        user.card_layout = data['card_layout']

    db.session.commit()

    # QRコード再生成（プロフィール更新時）
    generate_qr_code_file(user)

    return jsonify({
        'success': True,
        'message': 'プロフィールを更新しました',
        'profile': get_profile().json
    })

@profiles_bp.route('/api/profiles/me/icon', methods=['POST'])
@login_required
def upload_icon():
    """アイコン画像アップロード"""
    if 'icon' not in request.files:
        return jsonify({'success': False, 'message': 'ファイルがありません'}), 400

    file = request.files['icon']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'ファイルが選択されていません'}), 400

    # ファイル検証
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return jsonify({'success': False, 'message': '対応していないファイル形式です'}), 400

    # ファイル保存
    filename = secure_filename(f'user_{current_user.id}_icon.{file.filename.rsplit(".", 1)[1].lower()}')
    filepath = os.path.join('app/static/uploads/icons', filename)

    # 画像リサイズ（500x500px）
    img = Image.open(file)
    img = img.resize((500, 500), Image.LANCZOS)
    img.save(filepath)

    # データベース更新
    current_user.icon_filename = filename
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'アイコン画像をアップロードしました',
        'icon_url': f'/static/uploads/icons/{filename}'
    })

@profiles_bp.route('/api/profiles/me/generate-qr', methods=['POST'])
@login_required
def generate_qr():
    """QRコード生成"""
    data = request.get_json()
    format_type = data.get('format', 'png')

    if format_type not in ['png', 'svg', 'vcard']:
        return jsonify({'success': False, 'message': '無効なフォーマットです'}), 400

    # QRコード生成
    profile_url = f'https://influberry.jp/@{current_user.username}'

    if format_type == 'png':
        qr_filename = generate_qr_code_file(current_user)
        return jsonify({
            'success': True,
            'message': 'QRコードを生成しました',
            'qr_code_url': f'/static/uploads/qrcodes/{qr_filename}',
            'download_url': f'/api/profiles/me/download-qr?format=png'
        })

    elif format_type == 'svg':
        # SVG生成実装
        pass

    elif format_type == 'vcard':
        # vCard生成実装
        vcard_content = generate_vcard(current_user)
        vcard_filename = f'{current_user.username}.vcf'
        vcard_path = os.path.join('app/static/uploads/qrcodes', vcard_filename)

        with open(vcard_path, 'w') as f:
            f.write(vcard_content)

        return jsonify({
            'success': True,
            'message': 'vCardを生成しました',
            'download_url': f'/api/profiles/me/download-qr?format=vcard'
        })

# ===== Public Profile Pages =====

@profiles_bp.route('/@<username>')
def public_profile_username(username):
    """ユーザー名ベースの公開プロフィールページ"""
    # クローラーブロック
    user_agent = request.headers.get('User-Agent', '').lower()
    crawler_patterns = ['bot', 'crawler', 'spider', 'scraper', 'google', 'bing']

    if any(pattern in user_agent for pattern in crawler_patterns):
        abort(403)

    user = User.query.filter_by(username=username).first_or_404()

    if not user.profile_public:
        abort(404)

    return render_template('profiles/public_profile.html', user=user)

@profiles_bp.route('/c/<custom_slug>')
def public_profile_custom(custom_slug):
    """カスタムスラッグベースの公開プロフィールページ（プレミアム）"""
    # クローラーブロック
    user_agent = request.headers.get('User-Agent', '').lower()
    crawler_patterns = ['bot', 'crawler', 'spider', 'scraper', 'google', 'bing']

    if any(pattern in user_agent for pattern in crawler_patterns):
        abort(403)

    user = User.query.filter_by(custom_slug=custom_slug).first_or_404()

    if not user.profile_public:
        abort(404)

    return render_template('profiles/public_profile.html', user=user)

# ===== Helper Functions =====

def generate_qr_code_file(user):
    """QRコード画像ファイル生成"""
    profile_url = f'https://influberry.jp/@{user.username}'

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(profile_url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    qr_filename = f'user_{user.id}_qr.png'
    qr_path = os.path.join('app/static/uploads/qrcodes', qr_filename)
    qr_img.save(qr_path)

    user.qr_code_filename = qr_filename
    db.session.commit()

    return qr_filename

def generate_vcard(user):
    """vCard形式データ生成"""
    vcard = vobject.vCard()

    vcard.add('fn').value = user.influencer_name or user.username

    if user.phone_number:
        vcard.add('tel').value = user.phone_number

    vcard.add('email').value = user.email

    if user.website_url:
        vcard.add('url').value = user.website_url

    if user.company_name:
        vcard.add('org').value = [user.company_name]

    # SNSリンク（NOTE形式で追加）
    sns_links = []
    if user.tiktok_url:
        sns_links.append(f'TikTok: {user.tiktok_url}')
    if user.instagram_url:
        sns_links.append(f'Instagram: {user.instagram_url}')
    if user.twitter_url:
        sns_links.append(f'X: {user.twitter_url}')
    if user.youtube_url:
        sns_links.append(f'YouTube: {user.youtube_url}')
    if user.threads_url:
        sns_links.append(f'Threads: {user.threads_url}')

    if sns_links:
        vcard.add('note').value = '\n'.join(sns_links)

    return vcard.serialize()

```

---

## 15. セキュリティ実装詳細

### 15.1 ファイルアップロード検証

```python
# app/utils/file_validation.py

import os
import imghdr
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_image_file(file):
    """画像ファイル検証"""
    # ファイル名検証
    if not file or file.filename == '':
        return False, 'ファイルが選択されていません'

    # 拡張子検証
    if '.' not in file.filename:
        return False, '無効なファイル名です'

    ext = file.filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, '対応していないファイル形式です（PNG, JPG, JPEG のみ）'

    # ファイルサイズ検証
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_FILE_SIZE:
        return False, 'ファイルサイズが大きすぎます（最大5MB）'

    # MIME type検証
    header = file.read(512)
    file.seek(0)
    format_type = imghdr.what(None, header)

    if format_type not in ['png', 'jpeg']:
        return False, '無効な画像ファイルです'

    return True, None

```

### 15.2 レート制限

```python
# app/utils/rate_limit.py

from flask import request, abort
from functools import wraps
import time

# IPアドレスごとのアクセス記録
access_log = {}

def rate_limit(max_requests=100, window=3600):
    """レート制限デコレーター"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr
            now = time.time()

            # 古いログ削除
            if ip in access_log:
                access_log[ip] = [t for t in access_log[ip] if now - t < window]
            else:
                access_log[ip] = []

            # レート制限チェック
            if len(access_log[ip]) >= max_requests:
                abort(429)  # Too Many Requests

            # アクセス記録
            access_log[ip].append(now)

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 使用例
@profiles_bp.route('/@<username>')
@rate_limit(max_requests=100, window=3600)  # 1時間に100リクエスト
def public_profile_username(username):
    ...

```

---

---

## 15.3 XSS対策

```python
# app/utils/sanitizer.py

import bleach

ALLOWED_TAGS = []  # プレーンテキストのみ許可
ALLOWED_ATTRIBUTES = {}

def sanitize_input(text):
    """入力テキストのサニタイズ"""
    if not text:
        return text

    # HTMLタグを完全除去
    cleaned = bleach.clean(
        text,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )

    return cleaned.strip()

# 使用例
@profiles_bp.route('/api/profiles/me', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()

    if 'bio' in data:
        # サニタイズ適用
        user.bio = sanitize_input(data['bio'])

```

---

## 16. Vue.js コンポーネント詳細設計

### 16.1 AppIndexPage.vue（新規作成）

**ファイルパス**: `frontend/src/views/AppIndexPage.vue`

```
<template>
  <div class="app-index-page">
    <!-- ヘッダー -->
    <header class="page-header">
      <div class="header-content">
        <h1 class="page-title">InfluBerry アプリ一覧</h1>
        <button @click="openUserSettings" class="settings-button">
          <SettingsIcon />
        </button>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="app-cards-container">
      <div class="app-cards-grid">
        <!-- BerryManagement カード -->
        <div class="app-card" @click="navigateTo('/dashboard')">
          <div class="card-icon berry-management">
            <BriefcaseIcon />
          </div>
          <h2 class="card-title">BerryManagement</h2>
          <p class="card-subtitle">案件・請求書・タスク管理</p>
          <div class="card-arrow">
            <ArrowRightIcon />
          </div>
        </div>

        <!-- BerryCard カード -->
        <div class="app-card" @click="navigateTo('/card')">
          <div class="card-icon berry-card">
            <QrCodeIcon />
          </div>
          <h2 class="card-title">BerryCard</h2>
          <p class="card-subtitle">デジタル名刺・QRコード</p>
          <div class="card-arrow">
            <ArrowRightIcon />
          </div>
        </div>
      </div>
    </main>

    <!-- ユーザー設定モーダル -->
    <UserSettings v-if="showUserSettings" @close="showUserSettings = false" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { BriefcaseIcon, QrCodeIcon, SettingsIcon, ArrowRightIcon } from 'lucide-vue-next'
import UserSettings from '@/components/UserSettings.vue'

const router = useRouter()
const showUserSettings = ref(false)

const navigateTo = (path) => {
  router.push(path)
}

const openUserSettings = () => {
  showUserSettings.value = true
}
</script>

<style scoped>
.app-index-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #FFB7C5 0%, #E6E6FA 100%);
  padding: 2rem;
}

.page-header {
  max-width: 1200px;
  margin: 0 auto 3rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
}

.settings-button {
  padding: 0.75rem;
  background: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.settings-button:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.app-cards-container {
  max-width: 1200px;
  margin: 0 auto;
}

.app-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.app-card {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  position: relative;
  overflow: hidden;
}

.app-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.card-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  transition: all 0.3s;
}

.berry-management {
  background: linear-gradient(135deg, #FFD4C4 0%, #FF9999 100%);
}

.berry-card {
  background: linear-gradient(135deg, #B0E0E6 0%, #9FE2BF 100%);
}

.app-card:hover .card-icon {
  transform: scale(1.1) rotate(5deg);
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.5rem;
}

.card-subtitle {
  font-size: 1rem;
  color: #666;
  margin-bottom: 1rem;
}

.card-arrow {
  position: absolute;
  bottom: 1.5rem;
  right: 1.5rem;
  color: #999;
  transition: all 0.3s;
}

.app-card:hover .card-arrow {
  transform: translateX(5px);
  color: #333;
}

/* レスポンシブ対応 */
@media (max-width: 768px) {
  .app-index-page {
    padding: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .app-cards-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>

```

---

### 16.2 CardApp.vue（新規作成）

**ファイルパス**: `frontend/src/views/CardApp.vue`

```
<template>
  <div class="card-app">
    <!-- ヘッダー -->
    <header class="app-header">
      <button @click="navigateBack" class="back-button">
        <ArrowLeftIcon />
        <span>アプリ一覧へ</span>
      </button>
      <h1 class="app-title">BerryCard - デジタル名刺</h1>
      <div class="header-spacer"></div>
    </header>

    <!-- メインコンテンツ -->
    <main class="app-main">
      <div class="edit-preview-layout">
        <!-- 左: 編集パネル -->
        <div class="edit-panel">
          <ProfileEditForm @update="handleProfileUpdate" />
          <DesignCustomizer @change="handleDesignChange" />
          <QRCodeDownload />
        </div>

        <!-- 右: プレビューパネル -->
        <div class="preview-panel">
          <div class="preview-header">
            <h2>プレビュー</h2>
            <p class="preview-hint">編集内容がリアルタイムで反映されます</p>
          </div>
          <ProfilePreview :profile="previewProfile" />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeftIcon } from 'lucide-vue-next'
import { useProfileStore } from '@/stores/profiles'
import ProfileEditForm from '@/components/ProfileEditForm.vue'
import DesignCustomizer from '@/components/DesignCustomizer.vue'
import QRCodeDownload from '@/components/QRCodeDownload.vue'
import ProfilePreview from '@/components/ProfilePreview.vue'

const router = useRouter()
const profileStore = useProfileStore()

// プレビュー用リアクティブデータ
const previewProfile = computed(() => profileStore.profile)

const navigateBack = () => {
  router.push('/app-index')
}

const handleProfileUpdate = (updatedData) => {
  // リアルタイムプレビュー更新
  profileStore.updateProfileLocal(updatedData)
}

const handleDesignChange = (designData) => {
  // デザイン変更をリアルタイム反映
  profileStore.updateDesignLocal(designData)
}

// 初期データ読み込み
profileStore.fetchProfile()
</script>

<style scoped>
.card-app {
  min-height: 100vh;
  background: #f8f9fa;
}

.app-header {
  background: white;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: transparent;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
  color: #666;
}

.back-button:hover {
  background: #f5f5f5;
  border-color: #bbb;
}

.app-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
}

.header-spacer {
  width: 150px; /* back-buttonと同じ幅確保 */
}

.app-main {
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
}

.edit-preview-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.edit-panel {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.preview-panel {
  position: sticky;
  top: 2rem;
  height: fit-content;
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.preview-header {
  margin-bottom: 1.5rem;
}

.preview-header h2 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.5rem;
}

.preview-hint {
  font-size: 0.875rem;
  color: #999;
}

/* レスポンシブ対応 */
@media (max-width: 1200px) {
  .edit-preview-layout {
    grid-template-columns: 1fr;
  }

  .preview-panel {
    position: static;
  }
}

@media (max-width: 768px) {
  .app-header {
    padding: 1rem;
  }

  .app-title {
    font-size: 1.2rem;
  }

  .app-main {
    padding: 1rem;
  }

  .header-spacer {
    display: none;
  }
}
</style>

```

---

### 16.3 ProfileEditForm.vue（新規作成）

**ファイルパス**: `frontend/src/components/ProfileEditForm.vue`

```
<template>
  <div class="profile-edit-form card">
    <h2 class="section-title">基本情報</h2>

    <!-- アイコン画像 -->
    <div class="form-group">
      <label>アイコン画像</label>
      <div class="icon-upload">
        <div class="icon-preview">
          <img v-if="localProfile.iconUrl" :src="localProfile.iconUrl" alt="アイコン">
          <UserIcon v-else />
        </div>
        <input
          type="file"
          ref="iconInput"
          @change="handleIconUpload"
          accept="image/png, image/jpeg"
          class="file-input"
        >
        <button @click="$refs.iconInput.click()" class="upload-button">
          <UploadIcon />
          <span>画像を選択</span>
        </button>
        <p class="hint">PNG, JPEG形式・最大5MB</p>
      </div>
    </div>

    <!-- インフルエンサー名 -->
    <div class="form-group">
      <label>インフルエンサー名 <span class="required">*</span></label>
      <input
        v-model="localProfile.influencerName"
        @input="emitUpdate"
        type="text"
        placeholder="例: さくら"
        maxlength="100"
      >
    </div>

    <!-- 自己紹介文 -->
    <div class="form-group">
      <label>自己紹介文</label>
      <textarea
        v-model="localProfile.bio"
        @input="emitUpdate"
        placeholder="例: Z世代インフルエンサーです！美容・ファッション・ライフスタイルを発信中✨"
        rows="4"
        maxlength="500"
      ></textarea>
      <p class="char-count">{{ localProfile.bio?.length || 0 }} / 500</p>
    </div>

    <!-- 連絡先情報 -->
    <h3 class="subsection-title">連絡先情報</h3>

    <div class="form-group">
      <label>メールアドレス</label>
      <input
        v-model="localProfile.email"
        type="email"
        placeholder="例: example@example.com"
        disabled
      >
      <p class="hint">※ 変更はユーザー設定から行えます</p>
    </div>

    <div class="form-group">
      <label>電話番号</label>
      <input
        v-model="localProfile.phoneNumber"
        @input="emitUpdate"
        type="tel"
        placeholder="例: 090-1234-5678"
      >
    </div>

    <div class="form-group">
      <label>会社名</label>
      <input
        v-model="localProfile.companyName"
        @input="emitUpdate"
        type="text"
        placeholder="例: 株式会社○○"
      >
    </div>

    <div class="form-group">
      <label>ウェブサイトURL</label>
      <input
        v-model="localProfile.websiteUrl"
        @input="emitUpdate"
        type="url"
        placeholder="例: https://example.com"
      >
    </div>

    <!-- SNSリンク -->
    <h3 class="subsection-title">SNSリンク</h3>

    <div class="form-group">
      <label>
        <TikTokIcon class="sns-icon" />
        TikTok
      </label>
      <input
        v-model="localProfile.tiktokUrl"
        @input="emitUpdate"
        type="url"
        placeholder="https://tiktok.com/@username"
      >
    </div>

    <div class="form-group">
      <label>
        <InstagramIcon class="sns-icon" />
        Instagram
      </label>
      <input
        v-model="localProfile.instagramUrl"
        @input="emitUpdate"
        type="url"
        placeholder="https://instagram.com/username"
      >
    </div>

    <div class="form-group">
      <label>
        <TwitterIcon class="sns-icon" />
        X (Twitter)
      </label>
      <input
        v-model="localProfile.twitterUrl"
        @input="emitUpdate"
        type="url"
        placeholder="https://twitter.com/username"
      >
    </div>

    <div class="form-group">
      <label>
        <YoutubeIcon class="sns-icon" />
        YouTube
      </label>
      <input
        v-model="localProfile.youtubeUrl"
        @input="emitUpdate"
        type="url"
        placeholder="https://youtube.com/@username"
      >
    </div>

    <div class="form-group">
      <label>
        <ThreadsIcon class="sns-icon" />
        Threads
      </label>
      <input
        v-model="localProfile.threadsUrl"
        @input="emitUpdate"
        type="url"
        placeholder="https://threads.net/@username"
      >
    </div>

    <!-- LINE QRコード -->
    <h3 class="subsection-title">LINE QRコード</h3>

    <div class="form-group">
      <label>LINE QRコード画像</label>
      <div class="line-qr-upload">
        <div v-if="localProfile.lineQrUrl" class="line-qr-preview">
          <img :src="localProfile.lineQrUrl" alt="LINE QRコード">
        </div>
        <input
          type="file"
          ref="lineQrInput"
          @change="handleLineQrUpload"
          accept="image/png, image/jpeg"
          class="file-input"
        >
        <button @click="$refs.lineQrInput.click()" class="upload-button">
          <UploadIcon />
          <span>{{ localProfile.lineQrUrl ? 'QRコードを変更' : 'QRコードを追加' }}</span>
        </button>
        <p class="hint">LINEアプリで保存したQRコードをアップロード</p>
      </div>
    </div>

    <!-- 保存ボタン -->
    <div class="form-actions">
      <button @click="saveProfile" class="save-button" :disabled="saving">
        <SaveIcon />
        <span>{{ saving ? '保存中...' : 'プロフィールを保存' }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { useProfileStore } from '@/stores/profiles'
import {
  UserIcon,
  UploadIcon,
  SaveIcon
} from 'lucide-vue-next'
import TikTokIcon from '@/components/icons/TikTokIcon.vue'
import InstagramIcon from '@/components/icons/InstagramIcon.vue'
import TwitterIcon from '@/components/icons/TwitterIcon.vue'
import YoutubeIcon from '@/components/icons/YoutubeIcon.vue'
import ThreadsIcon from '@/components/icons/ThreadsIcon.vue'

const emit = defineEmits(['update'])
const profileStore = useProfileStore()

const iconInput = ref(null)
const lineQrInput = ref(null)
const saving = ref(false)

const localProfile = reactive({
  iconUrl: profileStore.profile.icon_url,
  influencerName: profileStore.profile.influencer_name,
  bio: profileStore.profile.bio,
  email: profileStore.profile.email,
  phoneNumber: profileStore.profile.phone_number,
  companyName: profileStore.profile.company_name,
  websiteUrl: profileStore.profile.website_url,
  tiktokUrl: profileStore.profile.tiktok_url,
  instagramUrl: profileStore.profile.instagram_url,
  twitterUrl: profileStore.profile.twitter_url,
  youtubeUrl: profileStore.profile.youtube_url,
  threadsUrl: profileStore.profile.threads_url,
  lineQrUrl: profileStore.profile.line_qr_url
})

// リアルタイムプレビュー更新
const emitUpdate = () => {
  emit('update', localProfile)
}

// アイコン画像アップロード
const handleIconUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // ファイルサイズチェック
  if (file.size > 5 * 1024 * 1024) {
    alert('ファイルサイズが大きすぎます（最大5MB）')
    return
  }

  // プレビュー表示
  const reader = new FileReader()
  reader.onload = (e) => {
    localProfile.iconUrl = e.target.result
    emitUpdate()
  }
  reader.readAsDataURL(file)

  // サーバーアップロード
  await profileStore.uploadIcon(file)
}

// LINE QRコードアップロード
const handleLineQrUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    alert('ファイルサイズが大きすぎます（最大5MB）')
    return
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    localProfile.lineQrUrl = e.target.result
    emitUpdate()
  }
  reader.readAsDataURL(file)

  await profileStore.uploadLineQr(file)
}

// プロフィール保存
const saveProfile = async () => {
  saving.value = true
  try {
    await profileStore.updateProfile(localProfile)
    alert('プロフィールを保存しました')
  } catch (error) {
    alert('保存に失敗しました')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1.5rem;
}

.subsection-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #555;
  margin: 2rem 0 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #555;
  margin-bottom: 0.5rem;
}

.required {
  color: #ff4444;
}

.sns-icon {
  width: 20px;
  height: 20px;
}

input[type="text"],
input[type="email"],
input[type="tel"],
input[type="url"],
textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #FFB7C5;
  box-shadow: 0 0 0 3px rgba(255, 183, 197, 0.1);
}

input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.hint {
  font-size: 0.875rem;
  color: #999;
  margin-top: 0.5rem;
}

.char-count {
  text-align: right;
  font-size: 0.875rem;
  color: #999;
  margin-top: 0.5rem;
}

/* アイコンアップロード */
.icon-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.icon-preview {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.icon-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.file-input {
  display: none;
}

.upload-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #FFB7C5;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
}

.upload-button:hover {
  background: #FF9999;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 183, 197, 0.3);
}

/* LINE QRコードアップロード */
.line-qr-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.line-qr-preview {
  width: 200px;
  height: 200px;
  border: 2px dashed #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.line-qr-preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* 保存ボタン */
.form-actions {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}

.save-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #FFB7C5 0%, #FF9999 100%);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 700;
  font-size: 1.1rem;
  box-shadow: 0 4px 15px rgba(255, 183, 197, 0.3);
}

.save-button:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(255, 183, 197, 0.4);
}

.save-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>

```

---

## 17. Pinia Store実装

### 17.1 profiles.js（新規作成）

**ファイルパス**: `frontend/src/stores/profiles.js`

```jsx
import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000'

export const useProfileStore = defineStore('profiles', {
  state: () => ({
    profile: {
      id: null,
      username: '',
      influencer_name: '',
      bio: '',
      icon_url: null,
      phone_number: '',
      company_name: '',
      website_url: '',
      tiktok_url: '',
      instagram_url: '',
      twitter_url: '',
      youtube_url: '',
      threads_url: '',
      line_qr_url: null,
      card_color: 'peach',
      card_font: 'Nunito',
      card_layout: 'simple',
      custom_slug: null,
      qr_code_url: null,
      profile_public: true,
      plan_type: 'free'
    },
    loading: false,
    error: null
  }),

  getters: {
    isPremium: (state) => state.profile.plan_type === 'premium',

    profileUrl: (state) => {
      if (state.profile.custom_slug && state.profile.plan_type === 'premium') {
        return `https://influberry.jp/c/${state.profile.custom_slug}`
      }
      return `https://influberry.jp/@${state.profile.username}`
    },

    snsLinks: (state) => {
      const links = []
      if (state.profile.tiktok_url) links.push({ name: 'TikTok', url: state.profile.tiktok_url, icon: 'tiktok' })
      if (state.profile.instagram_url) links.push({ name: 'Instagram', url: state.profile.instagram_url, icon: 'instagram' })
      if (state.profile.twitter_url) links.push({ name: 'X', url: state.profile.twitter_url, icon: 'twitter' })
      if (state.profile.youtube_url) links.push({ name: 'YouTube', url: state.profile.youtube_url, icon: 'youtube' })
      if (state.profile.threads_url) links.push({ name: 'Threads', url: state.profile.threads_url, icon: 'threads' })
      return links
    }
  },

  actions: {
    // プロフィール取得
    async fetchProfile() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${API_BASE_URL}/api/profiles/me`, {
          withCredentials: true
        })
        this.profile = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'プロフィールの取得に失敗しました'
        throw error
      } finally {
        this.loading = false
      }
    },

    // プロフィール更新
    async updateProfile(profileData) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.put(
          `${API_BASE_URL}/api/profiles/me`,
          profileData,
          { withCredentials: true }
        )
        this.profile = response.data.profile
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'プロフィールの更新に失敗しました'
        throw error
      } finally {
        this.loading = false
      }
    },

    // ローカル更新（リアルタイムプレビュー用）
    updateProfileLocal(profileData) {
      Object.assign(this.profile, profileData)
    },

    // デザイン設定更新（リアルタイムプレビュー用）
    updateDesignLocal(designData) {
      if (designData.cardColor) this.profile.card_color = designData.cardColor
      if (designData.cardFont) this.profile.card_font = designData.cardFont
      if (designData.cardLayout) this.profile.card_layout = designData.cardLayout
    },

    // アイコン画像アップロード
    async uploadIcon(file) {
      this.loading = true
      this.error = null
      try {
        const formData = new FormData()
        formData.append('icon', file)

        const response = await axios.post(
          `${API_BASE_URL}/api/profiles/me/icon`,
          formData,
          {
            withCredentials: true,
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        )

        this.profile.icon_url = response.data.icon_url
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'アイコンのアップロードに失敗しました'
        throw error
      } finally {
        this.loading = false
      }
    },

    // LINE QRコードアップロード
    async uploadLineQr(file) {
      this.loading = true
      this.error = null
      try {
        const formData = new FormData()
        formData.append('line_qr', file)

        const response = await axios.post(
          `${API_BASE_URL}/api/profiles/me/line-qr`,
          formData,
          {
            withCredentials: true,
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        )

        this.profile.line_qr_url = response.data.line_qr_url
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'LINE QRコードのアップロードに失敗しました'
        throw error
      } finally {
        this.loading = false
      }
    },

    // QRコード生成
    async generateQrCode(format = 'png') {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(
          `${API_BASE_URL}/api/profiles/me/generate-qr`,
          { format },
          { withCredentials: true }
        )

        if (format === 'png') {
          this.profile.qr_code_url = response.data.qr_code_url
        }

        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'QRコードの生成に失敗しました'
        throw error
      } finally {
        this.loading = false
      }
    },

    // QRコードダウンロード
    async downloadQrCode(format = 'png') {
      try {
        const response = await axios.get(
          `${API_BASE_URL}/api/profiles/me/download-qr?format=${format}`,
          {
            withCredentials: true,
            responseType: 'blob'
          }
        )

        // ダウンロード処理
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url

        const extension = format === 'vcard' ? 'vcf' : format
        link.setAttribute('download', `${this.profile.username}_qr.${extension}`)

        document.body.appendChild(link)
        link.click()
        link.remove()

        window.URL.revokeObjectURL(url)
      } catch (error) {
        this.error = error.response?.data?.message || 'QRコードのダウンロードに失敗しました'
        throw error
      }
    }
  }
})

```

---

## 18. ルーティング設定

### 18.1 router/index.js 修正

**ファイルパス**: `frontend/src/router/index.js`

```jsx
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/auth'
    },
    {
      path: '/auth',
      name: 'auth',
      component: () => import('@/views/AuthPage.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/app-index',
      name: 'app-index',
      component: () => import('@/views/AppIndexPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/projects',
      name: 'projects',
      component: () => import('@/views/ProjectApp.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/invoices',
      name: 'invoices',
      component: () => import('@/views/InvoiceApp.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/todos',
      name: 'todos',
      component: () => import('@/views/TodoApp.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/card',
      name: 'card',
      component: () => import('@/views/CardApp.vue'),
      meta: { requiresAuth: true }
    },
    // 既存の法的ページ等
    {
      path: '/privacy',
      name: 'privacy',
      component: () => import('@/views/legal/PrivacyPolicy.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/terms',
      name: 'terms',
      component: () => import('@/views/legal/TermsOfService.vue'),
      meta: { requiresAuth: false }
    }
  ]
})

// 認証ガード
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      // 認証チェック
      try {
        await authStore.checkAuth()
        if (authStore.isAuthenticated) {
          next()
        } else {
          next('/auth')
        }
      } catch (error) {
        next('/auth')
      }
    } else {
      next()
    }
  } else {
    // 認証不要ページ
    if (to.path === '/auth' && authStore.isAuthenticated) {
      // 既にログイン済みの場合はapp-indexへリダイレクト
      next('/app-index')
    } else {
      next()
    }
  }
})

export default router

```

---

## 19. 認証フロー修正

### 19.1 auth.js Store修正

**ファイルパス**: `frontend/src/stores/auth.js`

**修正箇所**: ログイン成功後のリダイレクト先変更

```jsx
// 既存のauth.jsに以下を追加・修正

actions: {
  async login(credentials) {
    this.loading = true
    this.error = null
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/auth/login`,
        credentials,
        { withCredentials: true }
      )

      this.isAuthenticated = true
      this.user = response.data.user

      // ★ リダイレクト先を /app-index に変更
      this.router.push('/app-index')

      return response.data
    } catch (error) {
      this.error = error.response?.data?.message || 'ログインに失敗しました'
      throw error
    } finally {
      this.loading = false
    }
  },

  async register(userData) {
    this.loading = true
    this.error = null
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/auth/register`,
        userData,
        { withCredentials: true }
      )

      this.isAuthenticated = true
      this.user = response.data.user

      // ★ リダイレクト先を /app-index に変更
      this.router.push('/app-index')

      return response.data
    } catch (error) {
      this.error = error.response?.data?.message || '登録に失敗しました'
      throw error
    } finally {
      this.loading = false
    }
  }
}

```

---

## 20. 最終チェックリスト

### 20.1 要件定義書完成確認

✅ **1. プロジェクト概要**

- アプリ名・目的・ターゲット明確化
- ビジネス目標・KPI設定

✅ **2. 機能要件**

- プロフィール編集機能詳細
- デザインカスタマイズ（24色・10フォント・3レイアウト）
- リアルタイムプレビュー
- QRコード生成（3形式）
- LINE QRコード埋め込み
- プロフィールページ（公開・クローラーブロック）
- AppIndexPage統合

✅ **3. データベース設計**

- Usersテーブル拡張カラム一覧
- マイグレーション計画

✅ **4. API設計**

- 8つのエンドポイント詳細
- リクエスト・レスポンス仕様

✅ **5. UI/UXデザイン**

- AppIndexPage.vue
- CardApp.vue
- ProfileEditForm.vue
- カラーパレット・フォント実装

✅ **6. 技術スタック**

- Flask Blueprint（profiles.py）
- Vue.js コンポーネント
- Pinia Store（profiles.js）
- ルーティング設定

✅ **7. セキュリティ**

- ファイルアップロード検証
- レート制限
- XSS対策
- クローラーブロック

✅ **8. 拡張機能ロードマップ**

- Phase 1（MVP）
- Phase 2-4（拡張機能）

✅ **9. プレミアム機能**

- フリー・プレミアムプラン詳細

✅ **10. 開発スケジュール**

- Week単位の実装計画

---

## 21. 拡張機能ロードマップ

### 21.1 Phase 1（MVP・Month 3実装）

**必須実装機能**:

### プロフィール管理

- ✅ 基本情報編集（名前・自己紹介・アイコン）
- ✅ 連絡先情報（メール・電話・会社名・ウェブサイト）
- ✅ SNSリンク（TikTok, Instagram, X, YouTube, Threads）
- ✅ LINE QRコード埋め込み

### デザインカスタマイズ

- ✅ カラー選択（フリー: ピーチのみ / プレミアム: 24色）
- ✅ フォント選択（フリー: Nunitoのみ / プレミアム: 10体）
- ✅ レイアウト選択（フリー: シンプル名刺型のみ / プレミアム: 3種）

### QRコード機能

- ✅ 自動生成（プロフィール保存時）
- ✅ 3形式ダウンロード（PNG, SVG, vCard）
- ✅ プロフィールURL: `@username`

### プロフィールページ

- ✅ 公開プロフィールページ（Jinja2テンプレート）
- ✅ デザイン設定反映
- ✅ クローラーブロック（User-Agent判定）

### UI統合

- ✅ AppIndexPage（アプリ一覧）
- ✅ CardApp（メインアプリページ）
- ✅ リアルタイムプレビュー

**技術実装**:

- Flask Blueprint: profiles.py
- Vue.js: 6コンポーネント
- Pinia Store: profiles.js
- データベースマイグレーション: 21カラム追加

**完了目標**: Month 3終了時（Week 3完了）

---

### 21.2 Phase 2（拡張機能・Month 4実装）

**拡張機能**:

### SNSアイコン並び替え機能

**実装内容**:

- ドラッグ＆ドロップでSNSアイコンの表示順変更
- または優先順位番号指定

**技術実装**:

```jsx
// Vue Draggable使用
import draggable from 'vuedraggable'

// データベース: sns_order TEXT (JSON形式)
// '["tiktok","instagram","twitter","youtube","threads"]'

```

**工数**: 2セッション（約5時間）

---

### QRコード中央アイコン挿入（プレミアム限定）

**実装内容**:

- ユーザーのアイコン画像をQRコード中央に配置
- エラー訂正レベル「H」（30%欠損修復可能）
- アイコンサイズ: QRコード全体の20%

**技術実装**:

```python
import qrcode
from PIL import Image

def generate_qr_with_icon(url, icon_path):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data(url)
    qr_img = qr.make_image()

    # アイコン合成
    icon = Image.open(icon_path).resize((icon_size, icon_size))
    qr_img.paste(icon, center_pos)

    return qr_img

```

**データベース追加**:

```sql
ALTER TABLE users ADD COLUMN qr_with_icon BOOLEAN NOT NULL DEFAULT FALSE;

```

**工数**: 1セッション（約2-3時間）

---

### 背景ぼかし写真機能（プレミアム限定）

**実装内容**:

**Option A: ユーザーカスタム背景**

- 背景画像アップロード
- ぼかしレベル調整（0-10段階）

**Option B: プリセット背景**（推奨）

- プリセット背景パターン提供
- パステルグラデーション
- ぼかし写真風デザイン

**技術実装**:

```sql
ALTER TABLE users ADD COLUMN background_image_filename VARCHAR(100);
ALTER TABLE users ADD COLUMN background_blur_level INTEGER DEFAULT 5;

```

```css
.profile-card {
  background-image: url('background.jpg');
  background-size: cover;
  filter: blur(5px);
  /* または backdrop-filter: blur(5px); */
}

```

**工数**: 2セッション（約4-5時間）

---

### アクセス解析基盤

**実装内容**:

- プロフィールページ閲覧数記録
- QRコードスキャン数推定
- 日別・週別・月別統計

**技術実装**:

```python
# 新規テーブル: profile_analytics
CREATE TABLE profile_analytics (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    view_date DATE NOT NULL,
    view_count INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

# 閲覧時に記録
@profiles_bp.route('/@<username>')
def public_profile(username):
    # ... 既存処理
    record_profile_view(user.id)
    # ...

```

**工数**: 2セッション（約4-5時間）

**完了目標**: Month 4終了時（Week 2完了）

---

### 21.3 Phase 3（高度機能・Month 5以降）

**実装予定機能**:

### 複数プロフィール作成（プレミアム限定）

- ユーザーごとに最大3つのプロフィール作成
- 用途別に使い分け（ビジネス用・プライベート用等）
- 各プロフィールに個別URL

**工数**: 3セッション（約7-8時間）

---

### NFCカード連携

- NFC対応スマホでタップ共有
- プロフィールURLをNFCタグに書き込み
- スマホケース型NFCカード対応

**工数**: 2セッション（約5時間）

---

### プロフィールページ独自ドメイン設定（プレミアム限定）

- カスタムドメイン設定
- 例: `myname.com` → InfluBerryプロフィールページ
- DNS設定ガイド提供

**工数**: 4セッション（約10時間）

---

### 21.4 Phase 4（将来構想・Month 6以降）

**実装検討機能**:

### AIプロフィール文章生成

- OpenAI API統合
- 自己紹介文の自動生成
- SNS投稿文の提案

**工数**: 3セッション（約7-8時間）

---

### プロフィールページアクセス制限

- パスワード保護機能
- 特定の人のみ閲覧可能
- 一時的な公開リンク生成

**工数**: 2セッション（約5時間）

---

### チーム・組織向けプロフィール管理

- 複数メンバーのプロフィール一括管理
- 組織専用ページ
- メンバー一覧表示

**工数**: 5セッション（約12-15時間）

---

### プロフィールページテンプレートマーケットプレイス

- ユーザー作成テンプレート共有
- 有料・無料テンプレート販売
- レビュー・評価システム

**工数**: 10セッション（約25時間）

---

## 22. プレミアム機能詳細

### 22.1 フリープラン

**料金**: ¥0/月（無料）

**BerryCard機能**:

- ✅ プロフィール編集（全項目）
    - 基本情報（名前・自己紹介・アイコン）
    - 連絡先情報（メール・電話・会社名・ウェブサイト）
    - SNSリンク（TikTok, Instagram, X, YouTube, Threads）
- ✅ LINE QRコード埋め込み
- ✅ QRコード生成（PNG, SVG, vCard）
- ✅ デフォルトデザインのみ
    - カラー: ピーチ（#FFD4C4）固定
    - フォント: Nunito 固定
    - レイアウト: シンプル名刺型 固定
- ✅ リアルタイムプレビュー
- ✅ プロフィールページURL: `@username`

**その他アプリ制限**:

- ✅ 案件管理（BerryWork）: 無制限
- ✅ Todo管理（BerryDo）: 無制限
- ⚠️ 請求書PDF（BerryPay）: **月間1枚まで**

**制限事項**:

- ❌ カラー変更不可
- ❌ フォント変更不可
- ❌ レイアウト変更不可
- ❌ カスタムスラッグURL不可
- ❌ QRコード中央アイコン不可
- ❌ 背景ぼかし写真不可
- ❌ アクセス解析不可

---

### 22.2 プレミアムプラン

**料金**: ¥1,280/月（税込）

**BerryCard拡張機能**:

- ✅ 全カラー選択可能（24色）
    - パステル・くすみ系全色使用可能
    - 気分・シーズンで変更可能
- ✅ 全フォント選択可能（10体）
    - 丸文字系・手書き系・大人可愛い系
    - ブランドイメージに合わせて選択
- ✅ 全レイアウト選択可能（3種）
    - シンプル名刺型
    - SNSプロフィール型
    - ストーリーカード型
- ✅ カスタムスラッグURL
    - `@username` + `c/custom-slug`
    - 覚えやすいURL設定可能
- ✅ QRコード中央アイコン挿入（Phase 2）
    - 自分の顔写真・ロゴ入りQR
    - ブランディング強化
- ✅ 背景ぼかし写真（Phase 2）
    - プリセット背景パターン
    - カスタム背景画像アップロード（検討中）
- ✅ SNSアイコン並び替え（Phase 2）
    - ドラッグ操作で優先順位変更
    - メインSNSを目立たせる
- ✅ アクセス解析・統計データ（Phase 3）
    - プロフィール閲覧数
    - 日別・週別・月別グラフ
    - QRコードスキャン数推定
- ✅ 複数プロフィール作成（Phase 3）
    - 最大3つまで作成可能
    - 用途別に使い分け

**その他アプリ拡張**:

- ✅ 請求書PDF（BerryPay）: **無制限**
- ✅ 高度なUI/UXカスタマイズ
- ✅ 優先サポート

**価格設定の根拠**:

- 競合サービス（Eight Premium）: ¥480-980/月
- InfluBerry統合サービス価値: 案件管理 + 請求書 + 名刺
- ターゲット（Z世代女子）の支払い可能価格帯
- 月間コーヒー2-3杯分の価格設定

---

### 22.3 プラン比較表

| 機能 | フリープラン | プレミアムプラン |
| --- | --- | --- |
| **料金** | **¥0/月** | **¥1,280/月** |
| **BerryCard機能** |  |  |
| プロフィール編集 | ✅ | ✅ |
| LINE QRコード | ✅ | ✅ |
| QRコード生成（3形式） | ✅ | ✅ |
| カラー選択 | ❌ ピーチのみ | ✅ 24色 |
| フォント選択 | ❌ Nunitoのみ | ✅ 10体 |
| レイアウト選択 | ❌ シンプル名刺型のみ | ✅ 3種 |
| カスタムURL | ❌ | ✅ `c/custom-slug` |
| QRアイコン挿入 | ❌ | ✅ |
| 背景ぼかし写真 | ❌ | ✅ |
| SNSアイコン並び替え | ❌ | ✅ |
| アクセス解析 | ❌ | ✅ |
| 複数プロフィール | ❌ | ✅ 最大3つ |
| **その他アプリ** |  |  |
| 案件管理（BerryWork） | ✅ 無制限 | ✅ 無制限 |
| Todo管理（BerryDo） | ✅ 無制限 | ✅ 無制限 |
| 請求書PDF（BerryPay） | ⚠️ 月1枚 | ✅ 無制限 |
| **サポート** | 標準 | 優先 |

---

### 22.4 プレミアム転換戦略

**無料トライアル**:

- 初回登録後14日間プレミアム機能無料
- トライアル期間中に全機能体験
- 期間終了前にリマインド通知

**アップグレード導線**:

- フリープラン利用時、プレミアム機能に✨アイコン表示
- 「プレミアムプランで利用可能」と明示
- ワンクリックでアップグレード画面へ

**ターゲット別訴求**:

- **初心者インフルエンサー**: 「プロフェッショナルな名刺で差をつける」
- **中級インフルエンサー**: 「ブランディング強化・アクセス解析」
- **本格派インフルエンサー**: 「複数プロフィール・統計データ活用」

**年払い割引**（検討中）:

- 月払い: ¥1,280/月 × 12ヶ月 = ¥15,360/年
- 年払い: ¥12,800/年（2ヶ月分お得）
- 割引率: 約17%OFF

---

## 23. 開発スケジュール（詳細）

### 23.1 Month 3（Phase 1実装）

### Week 1: 基盤構築（Day 1-7）

**Day 1-2（実装時間: 約2.5時間）**:

```
タスク1: 環境準備・マイグレーション
□ バックアップ作成（5分）
□ requirements.txt更新（5分）
□ ディレクトリ作成（10分）
□ マイグレーション作成（15分）
□ マイグレーション実行・確認（20分）

タスク2: Flask Blueprint基本実装
□ profiles.py 作成（40分）
□ __init__.py修正（5分）
□ 基本エンドポイント実装（30分）
□ 動作確認（15分）

合計: 約2時間25分

```

**Day 3-4（実装時間: 約2.5時間）**:

```
タスク3: AppIndexPage実装
□ AppIndexPage.vue 作成（30分）
□ ルーティング設定（10分）
□ auth.js修正（10分）
□ スタイリング（20分）
□ 動作確認（15分）

タスク4: Pinia Store基本実装
□ profiles.js 作成（40分）
□ state・getters定義（20分）
□ actions基本実装（30分）
□ 動作確認（15分）

合計: 約2時間30分

```

**Day 5-7（実装時間: 約2.5時間）**:

```
タスク5: CardApp基本UI
□ CardApp.vue 作成（30分）
□ レイアウト実装（30分）
□ ナビゲーション実装（15分）
□ 動作確認（10分）

タスク6: 統合テスト・デバッグ
□ 全ルート遷移確認（20分）
□ 認証フロー確認（15分）
□ バグ修正（30分）

合計: 約2時間30分

```

**Week 1完了チェック**:

- [ ]  データベースマイグレーション完了
- [ ]  Flask Blueprint基本動作確認
- [ ]  AppIndexPage表示・遷移確認
- [ ]  CardApp基本UI表示確認

---

### Week 2: フォーム実装（Day 8-14）

**Day 8-10（実装時間: 約2.5時間）**:

```
タスク7: ProfileEditForm基本情報
□ ProfileEditForm.vue 作成（30分）
□ 基本情報フォーム（30分）
□ アイコンアップロードUI（20分）
□ SNSリンク入力（20分）
□ LINE QRコードアップロード（15分）
□ 動作確認（15分）

合計: 約2時間10分

```

**Day 11-12（実装時間: 約2.5時間）**:

```
タスク8: DesignCustomizer実装
□ DesignCustomizer.vue 作成（20分）
□ カラー選択UI（25分）
□ フォント選択UI（20分）
□ レイアウト選択UI（20分）
□ プレミアム制御実装（15分）
□ 動作確認（15分）

タスク9: バリデーション・エラーハンドリング
□ フォームバリデーション（20分）
□ エラーメッセージ表示（15分）
□ 動作確認（10分）

合計: 約2時間40分

```

**Day 13-14（実装時間: 約2.5時間）**:

```
タスク10: ProfilePreview実装
□ ProfilePreview.vue 作成（30分）
□ 基本表示実装（30分）
□ デザイン反映実装（20分）
□ リアルタイム更新連携（20分）
□ 3レイアウト対応（30分）
□ 動作確認（20分）

合計: 約2時間30分

```

**Week 2完了チェック**:

- [ ]  ProfileEditForm全項目入力可能
- [ ]  DesignCustomizer動作確認
- [ ]  ProfilePreviewリアルタイム更新確認
- [ ]  プレミアム制御動作確認

---

### Week 3: QRコード・公開ページ（Day 15-21）

**Day 15-17（実装時間: 約2.5時間）**:

```
タスク11: QRコード生成機能
□ Flask QRコード生成関数（20分）
□ vCard生成関数（15分）
□ QRCodeDownload.vue UI（20分）
□ ダウンロード機能実装（20分）
□ 3形式対応確認（15分）

タスク12: 画像アップロード処理
□ Flask画像アップロードAPI（25分）
□ 画像リサイズ実装（15分）
□ エラーハンドリング（15分）
□ 動作確認（15分）

合計: 約2時間40分

```

**Day 18-19（実装時間: 約2.5時間）**:

```
タスク13: 公開プロフィールページ
□ public_profile.html作成（30分）
□ Jinja2テンプレート実装（30分）
□ CSS実装（3レイアウト）（40分）
□ クローラーブロック実装（15分）
□ 動作確認（25分）

合計: 約2時間20分

```

**Day 20-21（実装時間: 約2.5時間）**:

```
タスク14: 統合テスト・最終調整
□ 全機能統合テスト（40分）
□ ブラウザテスト（30分）
□ バグ修正（40分）
□ パフォーマンステスト（20分）

タスク15: 本番デプロイ
□ 本番環境マイグレーション（15分）
□ デプロイ実行（15分）
□ 本番動作確認（30分）

合計: 約2時間30分

```

**Week 3完了チェック**:

- [ ]  QRコード生成・ダウンロード動作確認
- [ ]  公開プロフィールページ表示確認
- [ ]  全機能統合テスト完了
- [ ]  本番環境デプロイ完了

---

### 23.2 Month 4（Phase 2実装）

### Week 1: UI拡張（Day 22-28）

**Day 22-24（実装時間: 約2.5時間）**:

```
タスク16: SNSアイコン並び替え
□ Vue Draggableインストール（5分）
□ ドラッグUI実装（40分）
□ 順序保存API実装（30分）
□ データベース更新（15分）
□ 動作確認（20分）

合計: 約1時間50分

```

**Day 25-28（実装時間: 約2.5時間）**:

```
タスク17: 背景ぼかし写真
□ データベースカラム追加（10分）
□ プリセット背景準備（30分）
□ 背景選択UI実装（40分）
□ CSS実装（30分）
□ 動作確認（20分）

合計: 約2時間10分

```

---

### Week 2: プレミアム機能（Day 29-35）

**Day 29-31（実装時間: 約2.5時間）**:

```
タスク18: QRコード中央アイコン挿入
□ Python画像合成実装（30分）
□ API実装（20分）
□ UI実装（25分）
□ プレミアム制御（15分）
□ 動作確認（20分）

合計: 約1時間50分

```

**Day 32-35（実装時間: 約2.5時間）**:

```
タスク19: アクセス解析基盤
□ profile_analyticsテーブル作成（15分）
□ 閲覧記録API実装（30分）
□ 統計取得API実装（40分）
□ 簡易ダッシュボードUI（40分）
□ 動作確認（25分）

合計: 約2時間30分

```

**Month 4完了チェック**:

- [ ]  SNSアイコン並び替え動作確認
- [ ]  背景ぼかし写真動作確認
- [ ]  QRアイコン挿入動作確認
- [ ]  アクセス解析記録確認

---

### 23.3 累計工数見積もり

**Phase 1（Month 3）**:

- Week 1: 約7.5時間（3セッション）
- Week 2: 約7.5時間（3セッション）
- Week 3: 約7.5時間（3セッション）
- **合計**: 約22.5時間（9セッション）

**Phase 2（Month 4）**:

- Week 1: 約4時間（2セッション）
- Week 2: 約4.5時間（2セッション）
- **合計**: 約8.5時間（4セッション）

**総工数**: 約31時間（13セッション）

---

## 24. 成功指標（KPI）詳細

### 24.1 Month 3終了時（Phase 1完了）

**ユーザー指標**:

- BerryCard利用率: **50%以上**
    - 計測: 既存InfluBerryユーザーのうち、BerryCard機能を使用したユーザー割合
    - 目標根拠: 新機能のため、既存ユーザーの半数が試用すれば成功
- 月間QRコード生成数: **500回以上**
    - 計測: QRコード生成API呼び出し回数
    - 目標根拠: 利用率50% × 想定アクティブユーザー100人 × 月5回更新
- プロフィールページ閲覧数: **2,000回以上**
    - 計測: `/@username` エンドポイントアクセス数
    - 目標根拠: 1ユーザーあたり月平均20回閲覧（友人・ファン・クライアント）

**技術指標**:

- プロフィール編集完了率: **70%以上**
    - 計測: プロフィール編集開始 → 保存完了の割合
    - 目標根拠: UI直感性・入力項目の適切さ確認
- QRコードダウンロード率: **60%以上**
    - 計測: QRコード生成 → ダウンロード実行の割合
    - 目標根拠: 生成したQRコードを実際に活用している割合

---

### 24.2 Month 4終了時（Phase 2完了）

**ユーザー指標**:

- BerryCard利用率: **70%以上**
    - 目標根拠: 口コミ・SNS拡散で新規ユーザー増加
- プレミアム転換率: **20%以上**
    - 計測: BerryCard利用者のうち、プレミアムプラン加入者割合
- 月間QRコード生成数: **1,000回以上**
    - 目標根拠: 利用率70% × アクティブユーザー150人 × 月5回更新
- プロフィールページ閲覧数: **5,000回以上**
    - 目標根拠: 1ユーザーあたり月平均30回閲覧 + 外部流入増加

**プレミアム機能利用指標**:

- カラー変更利用率: **80%以上**（プレミアムユーザー内）
    - 計測: プレミアムユーザーのうち、デフォルト以外のカラー使用者
    - 目標根拠: カラー変更は視覚的効果が高く、最も使われる機能
- レイアウト変更利用率: **60%以上**（プレミアムユーザー内）
    - 計測: プレミアムユーザーのうち、シンプル名刺型以外を使用
    - 目標根拠: 個性表現のため多様なレイアウト選択
- QRアイコン挿入利用率: **50%以上**（プレミアムユーザー内）
    - 計測: プレミアムユーザーのうち、QRアイコン挿入機能を使用
    - 目標根拠: ブランディング意識の高いユーザーが使用

**収益指標**:

- 月間売上（BerryCard起因）: **¥30,000以上**
    - 計算: プレミアムユーザー25人 × ¥1,280/月 = ¥32,000
    - 目標根拠: プレミアム転換率20% × 利用者数150人 = 30人

---

### 24.3 Month 6終了時（半年後）

**ユーザー指標**:

- BerryCard利用率: **80%以上**
    - 目標根拠: 定着化・必須機能として認識
- プレミアム転換率: **30%以上**
    - 目標根拠: 無料トライアル・機能拡充による転換促進
- 月間新規ユーザー登録数（BerryCard目的）: **50人以上**
    - 計測: 登録理由アンケート「デジタル名刺機能」選択者
    - 目標根拠: SNS拡散・口コミによる新規ユーザー獲得

**技術指標**:

- プロフィールページ平均表示速度: **500ms以下**
    - 計測: `/@username` エンドポイントレスポンスタイム
    - 目標根拠: ユーザー体験向上・離脱率低減
- QRコード生成平均時間: **800ms以下**
    - 計測: QRコード生成API処理時間
    - 目標根拠: ストレスなく生成完了

**収益指標**:

- 月間売上（BerryCard起因）: **¥100,000以上**
    - 計算: プレミアムユーザー80人 × ¥1,280/月 = ¥102,400
    - 目標根拠: ユーザー数300人 × 転換率30% = 90人

---

### 24.4 Year 1終了時（1年後）

**ユーザー指標**:

- BerryCard利用率: **90%以上**
    - 目標根拠: InfluBerry必須機能として完全定着
- プレミアム転換率: **35%以上**
    - 目標根拠: Phase 3-4拡張機能による付加価値向上
- 累計プロフィール閲覧数: **100,000回以上**
    - 目標根拠: 1日平均270回閲覧 × 365日

**収益指標**:

- 月間売上（BerryCard起因）: **¥300,000以上**
    - 計算: プレミアムユーザー250人 × ¥1,280/月 = ¥320,000
    - 目標根拠: ユーザー数1,000人 × 転換率35% = 350人
    - **重要**: 要件定義書「1.1 目的・目標」の「各プラグインで1日1万円売上達成」に相当

**市場シェア**:

- Z世代女子インフルエンサーツール市場でトップ3入り
    - 計測: 競合サービス（Eight, Sansan等）との比較
    - 差別化: Z世代特化・インフルエンサー特化・統合型サービス

---

## 25. リスク管理・対策

### 25.1 技術リスク

### リスク1: QRコード生成遅延

**発生確率**: 低

**影響度**: 中

**詳細**: 大量の同時リクエストによるQRコード生成遅延

**対策**:

1. **非同期処理導入**（Phase 2以降）:

```python
from celery import Celery

@celery.task
def generate_qr_code_async(user_id):
    user = User.query.get(user_id)
    generate_qr_code_file(user)

```

1. **キャッシュ機構**:

```python
# プロフィール変更時のみ再生成
if not profile_changed:
    return cached_qr_code

```

1. **CDN配信**（Phase 3以降）:
- QRコード画像をCDN（Cloudflare）で配信
- 生成後の読み込み速度向上

---

### リスク2: 画像ストレージ容量不足

**発生確率**: 中

**影響度**: 高

**詳細**: アイコン・QRコード・LINE QRコード画像の累積による容量不足

**対策**:

1. **定期削除ポリシー**:

```python
# 90日間未ログインユーザーの画像削除（警告後）
# 削除前にメール通知

```

1. **画像最適化**:

```python
# アップロード時に自動圧縮
img.save(filepath, optimize=True, quality=85)

```

1. **外部ストレージ移行**（Phase 3以降）:
- AWS S3 / Cloudflare R2 導入検討
- Render.com Professional Plan: 10GB制限対策

**容量見積もり**:

- アイコン画像: 平均100KB × 1,000ユーザー = 100MB
- QRコード画像: 平均50KB × 1,000ユーザー = 50MB
- LINE QRコード: 平均150KB × 500ユーザー = 75MB
- **合計**: 約225MB（1,000ユーザー時）
- Render.com Professional Plan: 10GB → 余裕あり

---

### リスク3: クローラー回避策

**発生確率**: 中

**影響度**: 中

**詳細**: User-Agent偽装による大量スクレイピング

**対策**:

1. **レート制限強化**:

```python
@rate_limit(max_requests=50, window=3600)  # 1時間50リクエストに制限
def public_profile(username):
    # ...

```

1. **CAPTCHA導入**（Phase 3以降）:

```python
# 短時間に複数アクセス検知時、reCAPTCHA表示
if access_count > 10:
    verify_recaptcha()

```

1. **Cloudflare Bot Management**（Phase 4以降）:
- 高度なボット検知
- 自動ブロック

---

### 25.2 運用リスク

### リスク4: スパム登録

**発生確率**: 中

**影響度**: 中

**詳細**: 偽アカウント大量登録によるサービス品質低下

**対策**:

1. **メール認証必須化**:

```python
# 新規登録時にメール認証リンク送信
# 認証完了までBerryCard機能制限

```

1. **reCAPTCHA導入**:

```jsx
// RegisterForm.vueに追加
<vue-recaptcha @verify="onVerify"></vue-recaptcha>

```

1. **登録数制限**:
- 同一IPアドレスから1日3アカウントまで
- 異常検知時に管理者通知

---

### リスク5: 不適切コンテンツ投稿

**発生確率**: 低

**影響度**: 高

**詳細**: プロフィール画像・自己紹介文に不適切コンテンツ

**対策**:

1. **利用規約明記**:
- 禁止事項明示
- 違反時のアカウント停止ポリシー
1. **報告機能**（Phase 3以降）:

```html
<!-- 公開プロフィールページに追加 -->
<button @click="reportProfile">不適切なコンテンツを報告</button>

```

1. **AI画像審査**（Phase 4以降）:
- AWS Rekognition / Google Vision API
- アップロード時に自動審査

---

### 25.3 ビジネスリスク

### リスク6: プレミアム転換率低迷

**発生確率**: 中

**影響度**: 高

**詳細**: 想定20%に対し、実際10%以下

**対策**:

1. **無料トライアル延長**:
- 14日間 → 30日間に延長検討
- プレミアム機能の価値体験促進
1. **段階的価格プラン**（Phase 3以降）:

```
フリープラン: ¥0/月
ライトプラン: ¥680/月（カラー・フォント変更のみ）
プレミアムプラン: ¥1,280/月（全機能）

```

1. **限定キャンペーン**:
- 初回登録特典: 3ヶ月半額
- 友達紹介: 1ヶ月無料

---

### リスク7: 競合サービス参入

**発生確率**: 中

**影響度**: 中

**詳細**: 類似サービスのZ世代特化版登場

**対策**:

1. **統合型価値の強化**:
- 案件管理 + 請求書 + 名刺の一体型
- 他サービスにない統合体験
1. **コミュニティ形成**:
- InfluBerryユーザーコミュニティ
- Discord・オフ会開催
1. **継続的機能拡張**:
- Phase 3-4拡張機能の早期実装
- ユーザーフィードバック反映

---

## 26. 継続的改善計画

### 26.1 ユーザーフィードバック収集

**収集方法**:

1. **アプリ内フィードバック**:

```
<!-- CardApp.vueに追加 -->
<button @click="openFeedback" class="feedback-button">
  <MessageIcon />
  フィードバックを送る
</button>

```

1. **定期アンケート**:
- 月次アンケート: 満足度・改善要望
- 四半期アンケート: 新機能要望
1. **SNS監視**:
- Twitter・Instagram・TikTokでのメンション監視
- ユーザーの声を定期収集

---

### 26.2 A/Bテスト実施

**テスト項目**（Phase 3以降）:

1. **カラーパレット配置**:
- パターンA: 色相順
- パターンB: 人気順
- 計測: 選択率・変更頻度
1. **プレミアム訴求文言**:
- パターンA: 「プロフェッショナルな名刺」
- パターンB: 「ブランディング強化」
- 計測: 転換率
1. **レイアウトデフォルト**:
- パターンA: シンプル名刺型
- パターンB: SNSプロフィール型
- 計測: 変更率・満足度

---

### 26.3 パフォーマンス監視

**監視項目**:

1. **レスポンスタイム**:

```python
# app/utils/performance_monitor.py
import time
from functools import wraps

def monitor_performance(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        duration = time.time() - start

        # 閾値超過時に警告
        if duration > 1.0:
            logger.warning(f'{f.__name__} took {duration}s')

        return result
    return decorated

```

1. **エラー率**:
- API エラー率: 1%以下維持
- フロントエンドエラー: Google Analytics計測
1. **稼働率**:
- 目標: 99.9%稼働率
- Render.com Professional Plan: 自動スケーリング

---

## 27. ドキュメント管理

### 27.1 開発ドキュメント

**作成済み**:

- ✅ 要件定義書 v1.0（本書）
- ✅ アーキテクチャ設計書 v1.0

**作成予定**:

- [ ]  API仕様書（OpenAPI/Swagger形式）
- [ ]  データベーススキーマ図
- [ ]  コンポーネント設計書
- [ ]  テスト仕様書

---

### 27.2 運用ドキュメント

**作成予定**（Phase 1完了後）:

- [ ]  デプロイ手順書
- [ ]  トラブルシューティングガイド
- [ ]  バックアップ・復旧手順
- [ ]  セキュリティチェックリスト

---

### 27.3 ユーザー向けドキュメント

**作成予定**（Phase 1完了後）:

- [ ]  BerryCard使い方ガイド
- [ ]  よくある質問（FAQ）
- [ ]  プレミアムプラン説明ページ
- [ ]  チュートリアル動画（TikTok・Instagram）

---

## 28. 法的・コンプライアンス対応

### 28.1 個人情報保護

**収集する個人情報**:

- 基本情報: 名前・メールアドレス・電話番号
- プロフィール情報: 自己紹介・アイコン画像
- SNSリンク: TikTok, Instagram等のURL
- LINE QRコード画像

**プライバシーポリシー更新**:

```
追加項目:
- BerryCard機能での個人情報取り扱い
- 公開プロフィールページの情報範囲
- 画像データの保存期間・削除ポリシー
- 第三者提供の有無（なし）

```

---

### 28.2 利用規約更新

**追加条項**:

1. **プロフィール公開に関する規約**:
    - ユーザーは公開範囲を理解した上で利用
    - クローラーブロック対策の限界説明
2. **禁止事項**:
    - 不適切な画像・文章の投稿禁止
    - 他者のプライバシー侵害禁止
    - 商標権・著作権侵害禁止
3. **免責事項**:
    - QRコード読み取り不可の免責
    - 外部SNSリンク先の責任範囲

---

### 28.3 著作権・ライセンス

**使用ライブラリ**:

- qrcode: BSD License（商用利用可）
- Pillow: HPND License（商用利用可）
- vobject: Apache License 2.0（商用利用可）
- Google Fonts: Open Font License（商用利用可）

**自社コンテンツ**:

- カラーパレット: オリジナル作成
- レイアウトデザイン: オリジナル作成
- コンポーネント: MIT License検討

---

## 29. 緊急時対応計画

### 29.1 障害発生時の対応フロー

**Level 1: 軽微な障害**（一部機能の不具合）

```
検知 → 調査（30分以内） → 修正作業 → デプロイ → 確認
所要時間: 1-2時間
通知: 不要

```

**Level 2: 中度の障害**（主要機能の停止）

```
検知 → ユーザー通知 → 調査（15分以内） → 修正作業 → デプロイ → 確認 → 完了通知
所要時間: 1-3時間
通知: アプリ内通知・Twitter投稿

```

**Level 3: 重大な障害**（サービス全体停止）

```
検知 → 緊急通知 → 調査（即座） → ロールバック or 緊急修正 → デプロイ → 確認 → 詳細報告
所要時間: 30分-2時間
通知: アプリ内通知・Twitter投稿・メール通知

```

---

### 29.2 ロールバック手順

**Git ロールバック**:

```bash
# 最新コミットの取り消し
git revert HEAD
git push origin main

# Render.com自動デプロイ
# 約3-5分で反映

```

**データベースロールバック**:

```bash
# マイグレーションダウングレード
flask db downgrade

# バックアップから復元（最終手段）
psql $DATABASE_URL < backup_YYYYMMDD.sql

```

---

### 29.3 データバックアップ

**自動バックアップ**:

- Render.com PostgreSQL: 毎日自動バックアップ
- 保持期間: 7日間（Free Tier） / 30日間（Professional Plan）

**手動バックアップ**（重要実装前）:

```bash
# データベースダンプ
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# ファイルストレージバックアップ
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz app/static/uploads/

```

---

## 30. まとめ

### 30.1 要件定義書完成確認

**本要件定義書に含まれる内容**:

✅ **1-10**: 基本情報・機能要件・データベース設計

✅ **11-19**: API設計・UI設計・認証フロー

✅ **20-21**: 最終チェックリスト・拡張機能ロードマップ

✅ **22**: プレミアム機能詳細（フリー・プレミアム比較）

✅ **23**: 開発スケジュール（Month 3-4詳細）

✅ **24**: 成功指標（KPI）詳細

✅ **25**: リスク管理・対策

✅ **26**: 継続的改善計画

✅ **27**: ドキュメント管理

✅ **28**: 法的・コンプライアンス対応

✅ **29**: 緊急時対応計画

✅ **30**: まとめ（本セクション）

**総ページ数**: 約70ページ相当

**総セクション数**: 30セクション

**総サブセクション数**: 100以上

---

### 30.2 次のアクション

**即座に実施可能**:

1. ✅ 要件定義書確認・承認
2. ✅ アーキテクチャ設計書確認
3. ⏭️ 実装開始判断

**実装開始時の推奨順序**:

```
Phase 1-1: データベース基盤（Day 1-2）
  → マイグレーション・ディレクトリ作成

Phase 1-2: Flask Blueprint基本（Day 3-4）
  → profiles.py基本実装・動作確認

Phase 1-3: AppIndexPage（Day 5-7）
  → アプリ一覧ページ・ルーティング

Phase 1-4: CardApp基本UI（Week 2）
  → メインページ・フォーム実装

Phase 1-5: QRコード・公開ページ（Week 3）
  → QRコード生成・公開プロフィール

Phase 1-6: 統合テスト・デプロイ（Week 3終盤）
  → 本番環境デプロイ

```

---

### 30.3 成功への鍵

**技術面**:

- ✅ 既存アーキテクチャとの完全統合
- ✅ パフォーマンス最適化（N+1問題回避等）
- ✅ セキュリティ対策（クローラーブロック・レート制限）

**ビジネス面**:

- ✅ Z世代女子インフルエンサーへの訴求
- ✅ プレミアム転換率20%以上達成
- ✅ 統合型サービス価値の最大化

**運用面**:

- ✅ ユーザーフィードバック継続収集
- ✅ 定期的な機能拡張（Phase 2-4）
- ✅ コミュニティ形成・口コミ促進

---

### 30.4 想定される成果

**Month 3終了時**:

- BerryCard MVP完成
- 利用率50%達成
- 月間QRコード生成500回

**Month 4終了時**:

- Phase 2拡張機能完成
- プレミアム転換率20%達成
- 月間売上¥30,000達成

**Year 1終了時**:

- 利用率90%達成
- プレミアム転換率35%達成
- 月間売上¥300,000達成
- **目標達成**: 「各プラグインで1日1万円売上」

---

## 要件定義書 v1.0 完成

**作成日**: 2025年10月16日

**最終更新**: 2025年10月16日

**バージョン**: 1.0 - 完全版

**作成者**: Claude (Anthropic)

**対象**: InfluBerry BerryCard実装

**状況**: 要件定義完了・実装準備完了

---

