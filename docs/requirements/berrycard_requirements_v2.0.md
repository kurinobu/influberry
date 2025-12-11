\# BerryCard 要件定義書 v2.0

\#\# 📋 ドキュメント情報

\*\*プロジェクト名\*\*: BerryCard \- デジタル名刺システム    
\*\*バージョン\*\*: v2.0    
\*\*最終更新\*\*: 2025年11月13日    
\*\*ステータス\*\*: アプリ独立化・デザインシステム刷新

\#\# 🎯 v2.0 主要変更点

\#\#\# 1\. アプリケーション独立化  
\- \*\*InfluBerryからBerryCardへの完全独立\*\*  
\- 独自のカラーアイデンティティ確立  
\- 専用ブランディング・ロゴ採用

\#\#\# 2\. デザインシステム刷新  
\- \*\*メインカラー\*\*: ラベンダー・パープル系 (\#a855f7)  
\- \*\*アクセントカラー\*\*: 明るいラベンダー (\#c084fc)  
\- BerryManagement（ピンク系）との明確な差別化

\#\#\# 3\. インデックスページ構成  
\- \*\*固定フッター\*\*: SVGアイコン \+ アプリ名のみ（BerryManagement同等）  
\- \*\*Bodyエリア\*\*: 正方形カードのグリッドレイアウト  
\- \*\*2カラムグリッド\*\*: BerryCard（左）、BerryManagement（右）

\#\# 🏗️ システム構成

\#\#\# インデックスページ構造

\`\`\`  
┌─────────────────────────────────────┐  
│  Header (InfluBerryロゴ \+ メニュー)  │  
├─────────────────────────────────────┤  
│                                     │  
│  Body \- アプリケーションカードエリア   │  
│                                     │  
│  ┌──────────────┐  ┌──────────────┐ │  
│  │              │  │              │ │  
│  │  📇 名刺SVG   │  │ 💼 ブリーフ   │ │  
│  │              │  │   ケースSVG  │ │  
│  │  BerryCard   │  │  Berry       │ │  
│  │              │  │  Management  │ │  
│  │ デジタル名刺  │  │ 案件管理      │ │  
│  │              │  │              │ │  
│  └──────────────┘  └──────────────┘ │  
│  (ラベンダー)        (ピンク)        │  
│                                     │  
│  ┌──────────────┐  ┌──────────────┐ │  
│  │  新規アプリ1  │  │  新規アプリ2  │ │  
│  └──────────────┘  └──────────────┘ │  
│                                     │  
├─────────────────────────────────────┤  
│  Fixed Footer                       │  
│  📇 BerryCard  💼 BerryManagement   │  
└─────────────────────────────────────┘  
\`\`\`

\#\# 🎨 デザインシステム v2.0

\#\#\# BerryCard カラーパレット

\`\`\`css  
/\* BerryCard 専用カラーパレット v2.0 \*/  
:root {  
  /\* メインカラー \*/  
  \--berrycard-primary: \#a855f7;           /\* ラベンダー \*/  
  \--berrycard-primary-light: \#c084fc;     /\* 明るいラベンダー \*/  
  \--berrycard-primary-dark: \#9333ea;      /\* 濃いラベンダー \*/  
    
  /\* アクセントカラー \*/  
  \--berrycard-accent: \#c084fc;  
  \--berrycard-accent-light: \#d8b4fe;  
    
  /\* グラデーション \*/  
  \--berrycard-gradient: linear-gradient(135deg, \#a855f7 0%, \#c084fc 100%);  
  \--berrycard-gradient-hover: linear-gradient(135deg, \#9333ea 0%, \#a855f7 100%);  
    
  /\* 背景カラー \*/  
  \--berrycard-bg-light: \#faf5ff;          /\* 薄いラベンダー背景 \*/  
  \--berrycard-bg-card: \#ffffff;  
    
  /\* テキストカラー \*/  
  \--berrycard-text-primary: \#1f2937;  
  \--berrycard-text-secondary: \#6b7280;  
  \--berrycard-text-on-primary: \#ffffff;  
}

/\* BerryManagement 既存カラー（参考） \*/  
:root {  
  \--berrymanagement-primary: \#ec4899;     /\* ピンク \*/  
  \--berrymanagement-primary-light: \#f472b6;  
}  
\`\`\`

\#\#\# インデックスページ カードデザイン仕様

\`\`\`css  
/\* アプリケーションカード \*/  
.app-card {  
  /\* レイアウト \*/  
  aspect-ratio: 1 / 1;                    /\* 正方形 \*/  
  display: flex;  
  flex-direction: column;  
  align-items: center;  
  justify-content: center;  
  padding: 2rem;  
    
  /\* 背景 \*/  
  background: var(--card-gradient);        /\* アプリごとのグラデーション \*/  
  border-radius: 1.5rem;  
    
  /\* シャドウ \*/  
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  
    
  /\* トランジション \*/  
  transition: transform 0.3s ease, box-shadow 0.3s ease;  
    
  /\* ホバー効果なし（要件により削除） \*/  
}

/\* BerryCard カード \*/  
.app-card.berrycard {  
  background: var(--berrycard-gradient);  
}

/\* BerryManagement カード \*/  
.app-card.berrymanagement {  
  background: linear-gradient(135deg, \#ec4899 0%, \#f472b6 100%);  
}  
\`\`\`

\#\#\# カード要素構成

\`\`\`html  
\<\!-- BerryCard カード \--\>  
\<div class="app-card berrycard"\>  
  \<\!-- アイコン（大） \--\>  
  \<svg class="app-icon" width="120" height="120"\>  
    \<\!-- 名刺SVGアイコン \--\>  
  \</svg\>  
    
  \<\!-- アプリ名 \--\>  
  \<h2 class="app-name"\>BerryCard\</h2\>  
    
  \<\!-- 説明文（1行） \--\>  
  \<p class="app-description"\>デジタル名刺システム\</p\>  
\</div\>

\<\!-- BerryManagement カード \--\>  
\<div class="app-card berrymanagement"\>  
  \<\!-- アイコン（大） \--\>  
  \<svg class="app-icon" width="120" height="120"\>  
    \<\!-- ブリーフケースまたはノートSVGアイコン \--\>  
  \</svg\>  
    
  \<\!-- アプリ名 \--\>  
  \<h2 class="app-name"\>BerryManagement\</h2\>  
    
  \<\!-- 説明文（1行） \--\>  
  \<p class="app-description"\>案件・タスク管理\</p\>  
\</div\>  
\`\`\`

\#\#\# 固定フッター仕様

\`\`\`html  
\<\!-- 固定フッター（BerryManagement同等UI） \--\>  
\<footer class="fixed-footer"\>  
  \<\!-- BerryCard \--\>  
  \<a href="/berrycard" class="footer-item"\>  
    \<svg class="footer-icon" width="24" height="24"\>  
      \<\!-- 名刺SVGアイコン \--\>  
    \</svg\>  
    \<span class="footer-label"\>BerryCard\</span\>  
  \</a\>  
    
  \<\!-- BerryManagement \--\>  
  \<a href="/berrymanagement" class="footer-item"\>  
    \<svg class="footer-icon" width="24" height="24"\>  
      \<\!-- ブリーフケースSVGアイコン \--\>  
    \</svg\>  
    \<span class="footer-label"\>BerryManagement\</span\>  
  \</a\>  
\</footer\>  
\`\`\`

\#\# 📱 レスポンシブデザイン

\#\#\# グリッドレイアウト

\`\`\`css  
/\* デスクトップ・タブレット: 2カラム \*/  
@media (min-width: 640px) {  
  .app-grid {  
    display: grid;  
    grid-template-columns: repeat(2, 1fr);  
    gap: 1.5rem;  
    padding: 1.5rem;  
  }  
}

/\* モバイル: 1カラム \*/  
@media (max-width: 639px) {  
  .app-grid {  
    display: grid;  
    grid-template-columns: 1fr;  
    gap: 1rem;  
    padding: 1rem;  
  }  
}  
\`\`\`

\#\# 🎯 BerryCard 機能要件（変更なし）

\#\#\# 基本機能  
1\. \*\*プロフィール管理\*\*  
   \- 名前、役職、会社名  
   \- 自己紹介文  
   \- プロフィール画像  
   \- 連絡先情報

2\. \*\*SNSリンク統合\*\*  
   \- TikTok, Instagram, X (Twitter)  
   \- YouTube, Threads  
   \- LINE QRコード

3\. \*\*デザインカスタマイズ\*\*  
   \- カラーテーマ選択（パステル12色）  
   \- フォント選択  
   \- レイアウト選択

4\. \*\*QRコード生成\*\*  
   \- プロフィールURL QRコード  
   \- ダウンロード機能

5\. \*\*プレビュー機能\*\*  
   \- リアルタイムプレビュー  
   \- デバイスビュー切替

\#\# 🔧 技術スタック（変更なし）

\#\#\# フロントエンド  
\- Vue.js 3 (Composition API)  
\- Vite  
\- Tailwind CSS  
\- Pinia  
\- Vue Router

\#\#\# バックエンド  
\- Flask  
\- SQLAlchemy  
\- PostgreSQL  
\- qrcode

\#\# 🗄️ データベース設計（変更なし）

\#\#\# Users Table \- BerryCard関連カラム

\`\`\`sql  
\-- プロフィール情報  
bio TEXT,  
icon\_filename VARCHAR(100),  
phone\_number VARCHAR(20),  
company\_name VARCHAR(100),  
website\_url VARCHAR(255),

\-- SNSリンク  
tiktok\_url VARCHAR(255),  
instagram\_url VARCHAR(255),  
twitter\_url VARCHAR(255),  
youtube\_url VARCHAR(255),  
threads\_url VARCHAR(255),

\-- LINE QRコード  
line\_qr\_filename VARCHAR(100),

\-- デザイン設定  
card\_color VARCHAR(20) DEFAULT 'lavender',  
card\_font VARCHAR(50) DEFAULT 'poppins',  
card\_layout VARCHAR(20) DEFAULT 'modern',

\-- カスタムスラッグ  
custom\_slug VARCHAR(50) UNIQUE,

\-- QRコード  
qr\_code\_filename VARCHAR(100),

\-- 公開設定  
profile\_public BOOLEAN DEFAULT TRUE,  
\`\`\`

\#\# 🚀 実装フェーズ

\#\#\# Phase 1: インデックスページ刷新 ✅  
\- \[x\] インデックスページデザイン設計  
\- \[x\] BerryCardカラーシステム確立  
\- \[x\] カードグリッドレイアウト実装  
\- \[x\] 固定フッターUI統一

\#\#\# Phase 2: BerryCard内部ページ更新  
\- \[ \] ヘッダー「BerryCard」ブランディング適用  
\- \[ \] ラベンダー系カラーテーマ適用  
\- \[ \] タブナビゲーション更新  
\- \[ \] 全コンポーネントのカラー更新

\#\#\# Phase 3: SVGアイコン作成  
\- \[ \] 名刺SVGアイコン作成（BerryCard用）  
\- \[ \] ブリーフケース/ノートSVGアイコン作成（BerryManagement用）  
\- \[ \] アイコンサイズバリエーション作成

\#\#\# Phase 4: 統合テスト  
\- \[ \] カラー視認性テスト  
\- \[ \] アクセシビリティテスト  
\- \[ \] レスポンシブテスト  
\- \[ \] クロスブラウザテスト

\#\# 📊 成功指標

\#\#\# UI/UX指標  
\- アプリ識別率: 95%以上  
\- カラー視認性: WCAG AA準拠  
\- タップ成功率: 98%以上

\#\#\# パフォーマンス指標  
\- インデックスページ読み込み: 1秒以内  
\- カード表示遅延: 100ms以内

\#\# 🎨 ブランディングガイドライン

\#\#\# BerryCard アイデンティティ

\*\*カラー\*\*  
\- プライマリ: ラベンダー (\#a855f7)  
\- 洗練された、プロフェッショナルな印象  
\- デジタル名刺としての信頼感

\*\*ターゲット\*\*  
\- Generation Z 女性インフルエンサー  
\- クリエイター、フリーランサー  
\- SNSアクティブユーザー

\*\*コンセプト\*\*  
\- 「自分をブランディングする」  
\- 「つながりを創る」  
\- 「プロフェッショナルで可愛い」

\#\#\# BerryManagement アイデンティティ（参考）

\*\*カラー\*\*  
\- プライマリ: ピンク (\#ec4899)  
\- エネルギッシュ、活発な印象  
\- 案件管理・生産性

\#\# 📝 v2.0 更新サマリー

\#\#\# 主要変更  
1\. \*\*アプリ独立化\*\*: BerryCardの独自アイデンティティ確立  
2\. \*\*カラーシステム\*\*: ラベンダー・パープル系採用  
3\. \*\*インデックスUI\*\*: 正方形カードグリッドレイアウト  
4\. \*\*固定フッター\*\*: SVGアイコン \+ アプリ名のみのシンプル設計

\#\#\# 次のアクション  
\- インデックスページHTML/CSS実装  
\- SVGアイコン作成・統合  
\- BerryCard内部ページのカラー更新

\---

\*\*作成者\*\*: Claude & Air    
\*\*最終更新\*\*: 2025年11月13日    
\*\*バージョン\*\*: v2.0  
\</document\_content\>

\<document\_content\>  
\# BerryCard アーキテクチャ設計書 v2.0

\#\# 📋 ドキュメント情報

\*\*プロジェクト名\*\*: BerryCard \- デジタル名刺システム    
\*\*バージョン\*\*: v2.0    
\*\*最終更新\*\*: 2025年11月13日    
\*\*ステータス\*\*: アプリ独立化・デザインシステム刷新完了

\#\# 🎯 v2.0 アーキテクチャ変更点

\#\#\# 1\. アプリケーション独立化  
\- InfluBerryからBerryCardへの完全分離  
\- 独自のブランドアイデンティティ確立  
\- 専用カラーシステム（ラベンダー・パープル系）

\#\#\# 2\. インデックスページ再設計  
\- 正方形カードグリッドレイアウト  
\- 2カラム responsive グリッド  
\- SVGアイコン統合

\#\#\# 3\. デザインシステム刷新  
\- BerryCard専用カラーパレット  
\- BerryManagementとの視覚的差別化  
\- 統一されたブランディング

\#\# 🏗️ システム全体アーキテクチャ

\`\`\`  
InfluBerry Platform v2.0  
│  
├── Index Page (ログイン後ランディング)  
│   ├── Header  
│   │   ├── InfluBerryロゴ  
│   │   └── ハンバーガーメニュー  
│   │  
│   ├── Body \- App Card Grid  
│   │   ├── BerryCard (ラベンダー)  
│   │   │   ├── 名刺SVGアイコン  
│   │   │   ├── アプリ名  
│   │   │   └── 説明文  
│   │   │  
│   │   ├── BerryManagement (ピンク)  
│   │   │   ├── ブリーフケースSVGアイコン  
│   │   │   ├── アプリ名  
│   │   │   └── 説明文  
│   │   │  
│   │   └── Future Apps...  
│   │  
│   └── Fixed Footer  
│       ├── BerryCard (SVG \+ 名前)  
│       └── BerryManagement (SVG \+ 名前)  
│  
├── BerryCard Application  
│   ├── Header (BerryCardブランド)  
│   ├── Tab Navigation  
│   ├── Profile Edit  
│   ├── Design Customizer  
│   ├── Preview  
│   └── QR Code  
│  
└── BerryManagement Application  
    └── (既存システム)  
\`\`\`

\#\# 🎨 デザインシステムアーキテクチャ

\#\#\# カラーシステム v2.0

\`\`\`css  
/\* \==========================================  
   BerryCard Color System v2.0  
   \========================================== \*/

:root {  
  /\* \=== BerryCard Primary Colors \=== \*/  
  \--berrycard-primary: \#a855f7;              /\* ラベンダー \*/  
  \--berrycard-primary-light: \#c084fc;        /\* 明るいラベンダー \*/  
  \--berrycard-primary-dark: \#9333ea;         /\* 濃いラベンダー \*/  
  \--berrycard-primary-ultra-light: \#e9d5ff;  /\* 極薄ラベンダー \*/  
    
  /\* \=== BerryCard Accent Colors \=== \*/  
  \--berrycard-accent: \#c084fc;  
  \--berrycard-accent-light: \#d8b4fe;  
  \--berrycard-accent-dark: \#a855f7;  
    
  /\* \=== BerryCard Gradients \=== \*/  
  \--berrycard-gradient-primary: linear-gradient(135deg, \#a855f7 0%, \#c084fc 100%);  
  \--berrycard-gradient-hover: linear-gradient(135deg, \#9333ea 0%, \#a855f7 100%);  
  \--berrycard-gradient-soft: linear-gradient(135deg, \#faf5ff 0%, \#f3e8ff 100%);  
    
  /\* \=== BerryCard Background Colors \=== \*/  
  \--berrycard-bg-light: \#faf5ff;             /\* 薄いラベンダー背景 \*/  
  \--berrycard-bg-card: \#ffffff;              /\* カード背景 \*/  
  \--berrycard-bg-hover: \#f3e8ff;             /\* ホバー背景 \*/  
    
  /\* \=== BerryCard Text Colors \=== \*/  
  \--berrycard-text-primary: \#1f2937;         /\* メインテキスト \*/  
  \--berrycard-text-secondary: \#6b7280;       /\* セカンダリテキスト \*/  
  \--berrycard-text-on-primary: \#ffffff;      /\* プライマリ上のテキスト \*/  
  \--berrycard-text-muted: \#9ca3af;           /\* 薄いテキスト \*/  
    
  /\* \=== BerryCard Border Colors \=== \*/  
  \--berrycard-border: \#e9d5ff;               /\* ボーダー \*/  
  \--berrycard-border-light: \#f3e8ff;         /\* 薄いボーダー \*/  
    
  /\* \=== BerryCard Shadow \=== \*/  
  \--berrycard-shadow: 0 4px 6px rgba(168, 85, 247, 0.1);  
  \--berrycard-shadow-lg: 0 10px 25px rgba(168, 85, 247, 0.15);  
}

/\* \==========================================  
   BerryManagement Color System (参考)  
   \========================================== \*/

:root {  
  /\* \=== BerryManagement Primary Colors \=== \*/  
  \--berrymanagement-primary: \#ec4899;        /\* ピンク \*/  
  \--berrymanagement-primary-light: \#f472b6;  
  \--berrymanagement-primary-dark: \#db2777;  
    
  /\* \=== BerryManagement Gradients \=== \*/  
  \--berrymanagement-gradient-primary: linear-gradient(135deg, \#ec4899 0%, \#f472b6 100%);  
}

/\* \==========================================  
   Extended Pastel Palette (共通)  
   \========================================== \*/

:root {  
  /\* 既存のパステルカラー（BerryCard内で選択可能） \*/  
  \--berry-blue: \#3b82f6;  
  \--berry-blue-light: \#60a5fa;  
  \--berry-green: \#10b981;  
  \--berry-green-light: \#34d399;  
  \--berry-orange: \#f97316;  
  \--berry-orange-light: \#fb923c;  
  \--berry-mint: \#6ee7b7;  
  \--berry-mint-light: \#a7f3d0;  
  \--berry-coral: \#fb7185;  
  \--berry-coral-light: \#fda4af;  
  \--berry-sky: \#38bdf8;  
  \--berry-sky-light: \#7dd3fc;  
  \--berry-yellow: \#fbbf24;  
  \--berry-yellow-light: \#fcd34d;  
}  
\`\`\`

\#\# 📱 インデックスページアーキテクチャ

\#\#\# HTML構造

\`\`\`html  
\<\!DOCTYPE html\>  
\<html lang="ja"\>  
\<head\>  
  \<meta charset="UTF-8"\>  
  \<meta name="viewport" content="width=device-width, initial-scale=1.0"\>  
  \<title\>InfluBerry \- アプリ一覧\</title\>  
  \<link rel="stylesheet" href="/static/css/index.css"\>  
\</head\>  
\<body\>  
  \<\!-- Header \--\>  
  \<header class="main-header"\>  
    \<div class="header-container"\>  
      \<div class="logo"\>  
        \<img src="/static/images/influberry-logo.svg" alt="InfluBerry"\>  
      \</div\>  
      \<button class="hamburger-menu" aria-label="メニュー"\>  
        \<span\>\</span\>  
        \<span\>\</span\>  
        \<span\>\</span\>  
      \</button\>  
    \</div\>  
  \</header\>

  \<\!-- Main Content \--\>  
  \<main class="main-content"\>  
    \<div class="container"\>  
      \<\!-- App Grid \--\>  
      \<div class="app-grid"\>  
          
        \<\!-- BerryCard \--\>  
        \<a href="/berrycard" class="app-card berrycard"\>  
          \<div class="app-card-content"\>  
            \<svg class="app-icon" width="120" height="120" viewBox="0 0 120 120"\>  
              \<\!-- 名刺SVGアイコン \--\>  
              \<use href="\#icon-business-card"\>\</use\>  
            \</svg\>  
            \<h2 class="app-name"\>BerryCard\</h2\>  
            \<p class="app-description"\>デジタル名刺システム\</p\>  
          \</div\>  
        \</a\>

        \<\!-- BerryManagement \--\>  
        \<a href="/berrymanagement" class="app-card berrymanagement"\>  
          \<div class="app-card-content"\>  
            \<svg class="app-icon" width="120" height="120" viewBox="0 0 120 120"\>  
              \<\!-- ブリーフケースSVGアイコン \--\>  
              \<use href="\#icon-briefcase"\>\</use\>  
            \</svg\>  
            \<h2 class="app-name"\>BerryManagement\</h2\>  
            \<p class="app-description"\>案件・タスク管理\</p\>  
          \</div\>  
        \</a\>

        \<\!-- Future Apps (プレースホルダー) \--\>  
        \<\!--   
        \<a href="/berry-app-3" class="app-card berry-app-3"\>  
          \<div class="app-card-content"\>  
            \<svg class="app-icon" width="120" height="120"\>  
              \<use href="\#icon-app-3"\>\</use\>  
            \</svg\>  
            \<h2 class="app-name"\>BerryApp 3\</h2\>  
            \<p class="app-description"\>新機能\</p\>  
          \</div\>  
        \</a\>  
        \--\>

      \</div\>  
    \</div\>  
  \</main\>

  \<\!-- Fixed Footer \--\>  
  \<footer class="fixed-footer"\>  
    \<nav class="footer-nav"\>  
      \<a href="/berrycard" class="footer-item"\>  
        \<svg class="footer-icon" width="24" height="24" viewBox="0 0 24 24"\>  
          \<use href="\#icon-business-card-small"\>\</use\>  
        \</svg\>  
        \<span class="footer-label"\>BerryCard\</span\>  
      \</a\>  
        
      \<a href="/berrymanagement" class="footer-item"\>  
        \<svg class="footer-icon" width="24" height="24" viewBox="0 0 24 24"\>  
          \<use href="\#icon-briefcase-small"\>\</use\>  
        \</svg\>  
        \<span class="footer-label"\>BerryManagement\</span\>  
      \</a\>  
    \</nav\>  
  \</footer\>

  \<\!-- SVG Symbol Definitions \--\>  
  \<svg style="display: none;"\>  
    \<defs\>  
      \<\!-- 名刺アイコン (大) \--\>  
      \<symbol id="icon-business-card" viewBox="0 0 120 120"\>  
        \<\!-- SVG path here \--\>  
      \</symbol\>  
        
      \<\!-- ブリーフケースアイコン (大) \--\>  
      \<symbol id="icon-briefcase" viewBox="0 0 120 120"\>  
        \<\!-- SVG path here \--\>  
      \</symbol\>  
        
      \<\!-- 名刺アイコン (小 \- フッター用) \--\>  
      \<symbol id="icon-business-card-small" viewBox="0 0 24 24"\>  
        \<\!-- SVG path here \--\>  
      \</symbol\>  
        
      \<\!-- ブリーフケースアイコン (小 \- フッター用) \--\>  
      \<symbol id="icon-briefcase-small" viewBox="0 0 24 24"\>  
        \<\!-- SVG path here \--\>  
      \</symbol\>  
    \</defs\>  
  \</svg\>

  \<script src="/static/js/index.js"\>\</script\>  
\</body\>  
\</html\>  
\`\`\`

\#\#\# CSS構造

\`\`\`css  
/\* \==========================================  
   Index Page Styles v2.0  
   \========================================== \*/

/\* \=== Layout \=== \*/  
.main-content {  
  min-height: calc(100vh \- 64px \- 64px); /\* header \+ footer \*/  
  padding: 2rem 1rem 5rem; /\* bottom padding for fixed footer \*/  
}

.container {  
  max-width: 1200px;  
  margin: 0 auto;  
}

/\* \=== App Grid \=== \*/  
.app-grid {  
  display: grid;  
  gap: 1.5rem;  
}

/\* Desktop & Tablet: 2 columns \*/  
@media (min-width: 640px) {  
  .app-grid {  
    grid-template-columns: repeat(2, 1fr);  
  }  
}

/\* Mobile: 1 column \*/  
@media (max-width: 639px) {  
  .app-grid {  
    grid-template-columns: 1fr;  
    gap: 1rem;  
  }  
}

/\* \=== App Card \=== \*/  
.app-card {  
  aspect-ratio: 1 / 1;  
  display: flex;  
  border-radius: 1.5rem;  
  overflow: hidden;  
  text-decoration: none;  
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  
  transition: transform 0.3s ease, box-shadow 0.3s ease;  
}

/\* ホバー効果削除（要件により） \*/  
.app-card:hover {  
  /\* No hover effect \*/  
}

.app-card-content {  
  width: 100%;  
  display: flex;  
  flex-direction: column;  
  align-items: center;  
  justify-content: center;  
  padding: 2rem;  
  gap: 1rem;  
}

/\* \=== BerryCard Styling \=== \*/  
.app-card.berrycard {  
  background: var(--berrycard-gradient-primary);  
}

.app-card.berrycard .app-icon {  
  fill: white;  
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));  
}

.app-card.berrycard .app-name,  
.app-card.berrycard .app-description {  
  color: white;  
}

/\* \=== BerryManagement Styling \=== \*/  
.app-card.berrymanagement {  
  background: var(--berrymanagement-gradient-primary);  
}

.app-card.berrymanagement .app-icon {  
  fill: white;  
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));  
}

.app-card.berrymanagement .app-name,  
.app-card.berrymanagement .app-description {  
  color: white;  
}

/\* \=== App Card Typography \=== \*/  
.app-name {  
  font-size: 1.5rem;  
  font-weight: 700;  
  margin: 0;  
  text-align: center;  
}

.app-description {  
  font-size: 0.875rem;  
  margin: 0;  
  text-align: center;  
  opacity: 0.9;  
}

/\* \=== Fixed Footer \=== \*/  
.fixed-footer {  
  position: fixed;  
  bottom: 0;  
  left: 0;  
  right: 0;  
  background: white;  
  border-top: 1px solid \#e5e7eb;  
  box-shadow: 0 \-2px 10px rgba(0, 0, 0, 0.05);  
  z-index: 1000;  
}

.footer-nav {  
  display: flex;  
  justify-content: space-around;  
  align-items: center;  
  max-width: 600px;  
  margin: 0 auto;  
  padding: 0.75rem 1rem;  
}

.footer-item {  
  display: flex;  
  flex-direction: column;  
  align-items: center;  
  gap: 0.25rem;  
  text-decoration: none;  
  color: \#6b7280;  
  transition: color 0.2s ease;  
  padding: 0.5rem 1rem;  
}

.footer-item:hover {  
  color: var(--berrycard-primary);  
}

.footer-item.active {  
  color: var(--berrycard-primary);  
}

.footer-icon {  
  width: 24px;  
  height: 24px;  
}

.footer-label {  
  font-size: 0.75rem;  
  font-weight: 500;  
}

/\* \=== Responsive Adjustments \=== \*/  
@media (max-width: 480px) {  
  .app-card-content {  
    padding: 1.5rem;  
  }  
    
  .app-icon {  
    width: 80px \!important;  
    height: 80px \!important;  
  }  
    
  .app-name {  
    font-size: 1.25rem;  
  }  
    
  .app-description {  
    font-size: 0.75rem;  
  }  
}  
\`\`\`

\#\# 🔧 BerryCardアプリケーション内部アーキテクチャ

\#\#\# コンポーネント構造

\`\`\`  
BerryCard Application  
├── CardApp.vue (Root Component)  
│   ├── BerryCardHeader.vue (独自ヘッダー)  
│   │   ├── BerryCardロゴ  
│   │   └── ラベンダーブランディング  
│   │  
│   ├── TabNavigation.vue  
│   │   ├── プロフィール編集タブ  
│   │   ├── デザイン設定タブ  
│   │   ├── プレビュータブ  
│   │   └── QRコードタブ  
│   │  
│   ├── ProfileEditForm.vue  
│   │   ├── 基本情報フォーム  
│   │   ├── SNSリンクフォーム  
│   │   └── LINE QRコードアップロード  
│   │  
│   ├── DesignCustomizer.vue  
│   │   ├── カラーパレット選択  
│   │   ├── フォント選択  
│   │   └── レイアウト選択  
│   │  
│   ├── ProfilePreview.vue  
│   │   ├── デスクトップビュー  
│   │   ├── モバイルビュー  
│   │   └── リアルタイムプレビュー  
│   │  
│   └── QRCodeDownload.vue  
│       ├── QRコード生成  
│       ├── QRコードプレビュー  
│       └── ダウンロード機能  
│  
└── BerryCardFooter.vue (固定フッター)  
\`\`\`

\#\#\# Vue.js ファイル構造

\`\`\`  
src/  
├── components/  
│   ├── berrycard/  
│   │   ├── CardApp.vue  
│   │   ├── BerryCardHeader.vue  
│   │   ├── TabNavigation.vue  
│   │   ├── ProfileEditForm.vue  
│   │   ├── DesignCustomizer.vue  
│   │   ├── ProfilePreview.vue  
│   │   ├── QRCodeDownload.vue  
│   │   └── BerryCardFooter.vue  
│   │  
│   └── shared/  
│       ├── Header.vue (共通ヘッダー)  
│       └── Footer.vue (共通フッター)  
│  
├── assets/  
│   ├── css/  
│   │   ├── berrycard.css (BerryCard専用スタイル)  
│   │   ├── index.css (インデックスページスタイル)  
│   │   └── common.css (共通スタイル)  
│   │  
│   ├── icons/  
│   │   ├── business-card.svg  
│   │   ├── briefcase.svg  
│   │   └── ...  
│   │  
│   └── fonts/  
│       └── (Google Fonts)  
│  
├── stores/  
│   ├── berrycard.js (Pinia Store)  
│   └── user.js  
│  
└── router/  
    └── index.js  
\`\`\`

\#\# 🗄️ データベースアーキテクチャ

\#\#\# Users Table Schema (BerryCard統合)

\`\`\`sql  
\-- BerryCard プロフィール情報  
CREATE TABLE users (  
  id SERIAL PRIMARY KEY,  
    
  \-- 認証情報 (既存)  
  email VARCHAR(255) UNIQUE NOT NULL,  
  password\_hash VARCHAR(255) NOT NULL,  
  username VARCHAR(50) UNIQUE NOT NULL,  
    
  \-- 基本プロフィール (既存)  
  first\_name VARCHAR(50),  
  last\_name VARCHAR(50),  
    
  \-- BerryCard プロフィール情報  
  bio TEXT,  
  icon\_filename VARCHAR(100),  
  phone\_number VARCHAR(20),  
  company\_name VARCHAR(100),  
  website\_url VARCHAR(255),  
    
  \-- SNSリンク  
  tiktok\_url VARCHAR(255),  
  instagram\_url VARCHAR(255),  
  twitter\_url VARCHAR(255),  
  youtube\_url VARCHAR(255),  
  threads\_url VARCHAR(255),  
    
  \-- LINE QRコード  
  line\_qr\_filename VARCHAR(100),  
    
  \-- BerryCard デザイン設定  
  card\_color VARCHAR(20) DEFAULT 'lavender',  
  card\_font VARCHAR(50) DEFAULT 'poppins',  
  card\_layout VARCHAR(20) DEFAULT 'modern',  
    
  \-- カスタムスラッグ (プレミアム機能)  
  custom\_slug VARCHAR(50) UNIQUE,  
    
  \-- QRコード画像  
  qr\_code\_filename VARCHAR(100),  
    
  \-- 公開設定  
  profile\_public BOOLEAN DEFAULT TRUE,  
    
  \-- タイムスタンプ  
  created\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP,  
  updated\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP,  
    
  \-- インデックス  
  CONSTRAINT check\_email\_format CHECK (email \~\* '^\[A-Za-z0-9.\_%+-\]+@\[A-Za-z0-9.-\]+\\.\[A-Za-z\]{2,}$')  
);

\-- インデックス  
CREATE INDEX idx\_users\_username ON users(username);  
CREATE INDEX idx\_users\_custom\_slug ON users(custom\_slug);  
CREATE INDEX idx\_users\_email ON users(email);  
\`\`\`

\#\# 🔌 API エンドポイント設計

\#\#\# BerryCard API Endpoints

\`\`\`python  
\# Flask Routes

@app.route('/api/berrycard/profile', methods=\['GET', 'PUT'\])  
@login\_required  
def berrycard\_profile():  
    """BerryCardプロフィール取得・更新"""  
    pass

@app.route('/api/berrycard/profile/icon', methods=\['POST'\])  
@login\_required  
def upload\_profile\_icon():  
    """プロフィールアイコンアップロード"""  
    pass

@app.route('/api/berrycard/profile/line-qr', methods=\['POST'\])  
@login\_required  
def upload\_line\_qr():  
    """LINE QRコードアップロード"""  
    pass

@app.route('/api/berrycard/design', methods=\['GET', 'PUT'\])  
@login\_required  
def berrycard\_design():  
    """デザイン設定取得・更新"""  
    pass

@app.route('/api/berrycard/qrcode', methods=\['GET'\])  
@login\_required  
def generate\_qrcode():  
    """QRコード生成"""  
    pass

@app.route('/api/berrycard/preview', methods=\['GET'\])  
@login\_required  
def preview\_profile():  
    """プレビューデータ取得"""  
    pass

\# 公開プロフィールページ  
@app.route('/\<username\>', methods=\['GET'\])  
@app.route('/c/\<custom\_slug\>', methods=\['GET'\])  
def public\_profile(username=None, custom\_slug=None):  
    """公開プロフィールページ表示"""  
    pass  
\`\`\`

\#\# 🎯 パフォーマンス最適化

\#\#\# フロントエンド最適化

\`\`\`javascript  
// Vite設定 (vite.config.js)  
export default {  
  build: {  
    rollupOptions: {  
      output: {  
        manualChunks: {  
          'berrycard': \[  
            './src/components/berrycard/CardApp.vue',  
            './src/components/berrycard/ProfileEditForm.vue',  
            './src/components/berrycard/DesignCustomizer.vue',  
            './src/components/berrycard/ProfilePreview.vue',  
            './src/components/berrycard/QRCodeDownload.vue',  
          \],  
          'vendor': \['vue', 'pinia', 'vue-router'\]  
        }  
      }  
    },  
    cssCodeSplit: true,  
    minify: 'terser'  
  }  
}  
\`\`\`

\#\#\# 画像最適化

\- \*\*アイコン\*\*: SVG形式（スケーラブル）  
\- \*\*プロフィール画像\*\*: WebP対応、遅延読み込み  
\- \*\*QRコード\*\*: PNG、最適化圧縮

\#\# 🔒 セキュリティアーキテクチャ

\#\#\# 認証・認可

\`\`\`python  
\# Flask-Login統合  
from flask\_login import LoginManager, login\_required

login\_manager \= LoginManager()  
login\_manager.init\_app(app)

@login\_manager.user\_loader  
def load\_user(user\_id):  
    return User.query.get(int(user\_id))

\# CSRFトークン  
from flask\_wtf.csrf import CSRFProtect  
csrf \= CSRFProtect(app)  
\`\`\`

\#\#\# 入力検証

\`\`\`python  
\# SQLAlchemy検証  
from sqlalchemy import CheckConstraint

class User(db.Model):  
    \_\_table\_args\_\_ \= (  
        CheckConstraint(  
            "email \~\* '^\[A-Za-z0-9.\_%+-\]+@\[A-Za-z0-9.-\]+\\.\[A-Za-z\]{2,}$'",  
            name='check\_email\_format'  
        ),  
        CheckConstraint(  
            "LENGTH(custom\_slug) \>= 3 AND LENGTH(custom\_slug) \<= 50",  
            name='check\_custom\_slug\_length'  
        ),  
    )  
\`\`\`

\#\# 📊 テスト戦略

\#\#\# ユニットテスト

\`\`\`python  
\# tests/test\_berrycard\_v2.py

def test\_berrycard\_color\_system():  
    """BerryCardカラーシステムテスト"""  
    assert user.card\_color \== 'lavender'  
      
def test\_berrycard\_independence():  
    """BerryCard独立性テスト"""  
    \# BerryManagementと異なるカラーが設定されていることを確認  
    pass  
\`\`\`

\#\#\# 統合テスト

\`\`\`python  
def test\_index\_page\_rendering():  
    """インデックスページレンダリングテスト"""  
    response \= client.get('/')  
    assert b'BerryCard' in response.data  
    assert b'BerryManagement' in response.data  
\`\`\`

\#\# 🚀 デプロイメント戦略

\#\#\# ステージング環境

\`\`\`bash  
\# Render.com / Railway  
FLASK\_ENV=staging  
DATABASE\_URL=postgresql://...  
BERRYCARD\_ENABLED=true  
\`\`\`

\#\#\# 本番環境

\`\`\`bash  
\# Render.com / Railway  
FLASK\_ENV=production  
DATABASE\_URL=postgresql://...  
BERRYCARD\_ENABLED=true  
\`\`\`

\#\# 📝 実装チェックリスト

\#\#\# Phase 1: インデックスページ実装  
\- \[ \] HTML構造実装  
\- \[ \] CSS実装（グリッドレイアウト）  
\- \[ \] BerryCardカラーシステム適用  
\- \[ \] BerryManagementカラーシステム分離  
\- \[ \] レスポンシブ対応

\#\#\# Phase 2: SVGアイコン作成  
\- \[ \] 名刺SVGアイコン作成（大・小）  
\- \[ \] ブリーフケースSVGアイコン作成（大・小）  
\- \[ \] SVG symbol統合

\#\#\# Phase 3: BerryCard内部更新  
\- \[ \] ヘッダー「BerryCard」ブランディング  
\- \[ \] ラベンダーカラーテーマ適用  
\- \[ \] タブナビゲーション更新  
\- \[ \] 全コンポーネントカラー更新

\#\#\# Phase 4: テスト  
\- \[ \] カラー視認性テスト  
\- \[ \] レスポンシブテスト  
\- \[ \] アクセシビリティテスト  
\- \[ \] クロスブラウザテスト

\#\# 📈 成功指標

\#\#\# UI/UX指標  
\- \*\*アプリ識別率\*\*: 95%以上（ユーザーがBerryCardとBerryManagementを正しく識別）  
\- \*\*カラーコントラスト\*\*: WCAG AA準拠  
\- \*\*タップ成功率\*\*: 98%以上

\#\#\# パフォーマンス指標  
\- \*\*インデックスページ読み込み\*\*: \< 1秒  
\- \*\*カード表示遅延\*\*: \< 100ms  
\- \*\*Lighthouse Score\*\*: 90+

\#\# 📚 技術ドキュメント参照

\- \[Vue.js 3 公式ドキュメント\](https://vuejs.org/)  
\- \[Tailwind CSS\](https://tailwindcss.com/)  
\- \[Flask公式ドキュメント\](https://flask.palletsprojects.com/)  
\- \[PostgreSQL\](https://www.postgresql.org/docs/)

\---

\*\*作成者\*\*: Claude & Air    
\*\*最終更新\*\*: 2025年11月13日    
\*\*バージョン\*\*: v2.0    
\*\*ステータス\*\*: 設計完了・実装準備完了  
\</document\_content\>

v2.0の要件定義書とアーキテクチャ設計書を作成しました。

主な更新点：  
1\. \*\*BerryCard独立化\*\*: ラベンダー・パープル系カラーシステム確立  
2\. \*\*インデックスページ\*\*: 正方形カードの2カラムグリッドレイアウト  
3\. \*\*固定フッター\*\*: SVGアイコン \+ アプリ名のシンプル設計（ホバー効果削除）  
4\. \*\*SVGアイコン定義\*\*: 名刺・ブリーフケースの大小サイズ  
5\. \*\*完全なコード例\*\*: HTML/CSS/Vue.js構造

次のステップとして、SVGアイコンの作成や実装コードの作成が可能です。確認・修正点があればお知らせください。