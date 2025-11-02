# BerryCard セッション2引き継ぎ書

---

**作成日**: 2025年10月18日  
**対象**: BerryCard セッション2実装  
**前セッション**: セッション1完了（基盤構築）  
**次セッション**: セッション2（フロントエンド実装）

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

---

## 2. セッション2で実装すべき項目

### 2.1 フロントエンド実装（優先度：高）

#### Vue.jsコンポーネント作成
```
frontend/src/views/
├── AppIndexPage.vue (新規作成)
└── CardApp.vue (新規作成)

frontend/src/components/
├── ProfileEditForm.vue (新規作成)
├── DesignCustomizer.vue (新規作成)
├── ProfilePreview.vue (新規作成)
└── QRCodeDownload.vue (新規作成)
```

#### Pinia Store作成
```
frontend/src/stores/
└── profiles.js (新規作成)
```

#### ルーティング設定
```
frontend/src/router/index.js (更新)
- /app-index ルート追加
- /card ルート追加
```

### 2.2 テンプレート・スタイリング（優先度：中）

#### 公開プロフィールテンプレート
```
app/templates/profiles/
└── public_profile.html (新規作成)
```

#### スタイリング
- レスポンシブデザイン
- パステルカラーパレット
- Google Fonts統合

---

## 3. セッション2開始手順

### 3.1 環境確認
```bash
cd /Users/kurinobu/projects/influberry_v2

# 既存アプリケーション動作確認
python -c "from app import create_app; app = create_app(); print('Flask app OK')"

# 依存関係確認
python -c "import qrcode, vobject, PIL; print('Dependencies OK')"

# データベース確認
flask db current
```

### 3.2 バックアップ作成
```bash
# セッション2開始前のバックアップ
date +%Y%m%d_%H%M%S
# 例: 20251018_060000

# フロントエンドバックアップ
cp -r frontend frontend_backup_berrycard_session2_start_$(date +%Y%m%d_%H%M%S)
```

### 3.3 実装順序

#### Phase 2-1: Pinia Store作成
1. `frontend/src/stores/profiles.js` 作成
2. 既存の `auth.js` との統合確認

#### Phase 2-2: ルーティング設定
1. `frontend/src/router/index.js` 更新
2. 新規ルート追加（/app-index, /card）
3. 認証ガード設定

#### Phase 2-3: AppIndexPage.vue作成
1. アプリ一覧ページ作成
2. BerryCardアプリカード追加
3. 既存アプリ（BerryManagement）との統合

#### Phase 2-4: CardApp.vue作成
1. メインページ作成
2. 編集・プレビューレイアウト
3. コンポーネント統合

#### Phase 2-5: 子コンポーネント作成
1. ProfileEditForm.vue
2. DesignCustomizer.vue
3. ProfilePreview.vue
4. QRCodeDownload.vue

#### Phase 2-6: 公開プロフィールテンプレート
1. `app/templates/profiles/public_profile.html` 作成
2. レスポンシブデザイン
3. パステルカラーパレット

---

## 4. 技術的注意点

### 4.1 既存アプリとの統合
- **既存のInfluBerryアプリは絶対に保持**
- 既存のルーティング（/dashboard, /projects等）は変更禁止
- 既存のコンポーネント（UserSettings.vue等）は保持

### 4.2 認証システム
- 既存のFlask-Login認証システムを活用
- 既存のauth.js Pinia Storeを活用
- ログイン後リダイレクト先を `/app-index` に変更

### 4.3 API統合
- セッション1で実装した `/api/profiles/*` エンドポイントを活用
- 既存のAPIエンドポイント（/api/auth, /api/projects等）は保持

### 4.4 データベース
- セッション1で追加したUsersテーブルのカラムを活用
- 既存のデータベース構造は保持

---

## 5. 実装参考資料

### 5.1 要件定義書
- `docs/requirements/berrycard_requirements_v1.0.md`
- 特に以下のセクションを参照：
  - 4. 機能要件詳細
  - 11. Vue.jsコンポーネント設計
  - 12. Pinia Store実装
  - 13. ルーティング設計

### 5.2 アーキテクチャ設計書
- `docs/architecture/berrycard_architecture_v1.1_session1_completed.md`
- セッション1完了版を参照

### 5.3 既存コード参考
- `frontend/src/views/DashboardPage.vue` - 既存ページ構造参考
- `frontend/src/stores/auth.js` - 既存Store構造参考
- `frontend/src/router/index.js` - 既存ルーティング参考

---

## 6. セッション2完了目標

### 6.1 必須完了項目
- ✅ AppIndexPage.vue 作成・動作確認
- ✅ CardApp.vue 作成・動作確認
- ✅ ProfileEditForm.vue 作成・動作確認
- ✅ DesignCustomizer.vue 作成・動作確認
- ✅ ProfilePreview.vue 作成・動作確認
- ✅ QRCodeDownload.vue 作成・動作確認
- ✅ profiles.js Pinia Store 作成・動作確認
- ✅ ルーティング設定完了
- ✅ 公開プロフィールテンプレート作成

### 6.2 動作確認項目
- ログイン後 `/app-index` にリダイレクト
- BerryCardアプリカードクリックで `/card` に遷移
- プロフィール編集フォーム動作確認
- リアルタイムプレビュー動作確認
- QRコード生成・ダウンロード動作確認
- 公開プロフィールページ表示確認

---

## 7. トラブルシューティング

### 7.1 よくある問題
1. **Vue.jsコンポーネントのインポートエラー**
   - パス指定を確認
   - 既存のコンポーネント構造を参考

2. **Pinia Storeの統合エラー**
   - 既存のauth.jsとの競合確認
   - インポート文の確認

3. **ルーティングエラー**
   - 既存のルートとの競合確認
   - 認証ガードの設定確認

4. **API通信エラー**
   - セッション1で実装したエンドポイントの確認
   - CORS設定の確認

### 7.2 緊急時復旧手順
```bash
# セッション1完了状態に復旧
cd /Users/kurinobu/projects/influberry_v2

# フロントエンド復旧
rm -rf frontend
mv frontend_backup_berrycard_session1_20251018_052304 frontend

# 動作確認
python -c "from app import create_app; app = create_app(); print('Recovery OK')"
```

---

## 8. 次のセッション（セッション3）準備

### 8.1 セッション3で実装予定
- スタイリング完成
- レスポンシブデザイン
- パステルカラーパレット
- Google Fonts統合
- 最終テスト・デバッグ

### 8.2 セッション3開始時の確認事項
- セッション2で作成したコンポーネントの動作確認
- 既存アプリとの統合確認
- パフォーマンステスト
- セキュリティテスト

---

## 9. まとめ

セッション1では、BerryCardの基盤構築が完了しました。セッション2では、フロントエンドの実装に集中し、ユーザーインターフェースの完成を目指します。

**重要**: 既存のInfluBerryアプリケーションは完全に保持されており、新機能が安全に統合されています。セッション2でも、この原則を守りながら実装を進めてください。

**成功の鍵**: 
1. 既存アプリの保持を最優先
2. 段階的な実装とテスト
3. 既存コードの構造を参考にした実装
4. セッション1で実装したAPIエンドポイントの活用
