# BerryCard セッション2開始ガイド

---

**作成日**: 2025年10月18日  
**対象**: BerryCard セッション2実装開始  
**前提**: セッション1完了（基盤構築完了）

---

## 1. セッション2開始前の確認

### 1.1 環境確認
```bash
cd /Users/kurinobu/projects/influberry_v2

# 現在のディレクトリ確認
pwd
# 期待値: /Users/kurinobu/projects/influberry_v2

# 既存アプリケーション動作確認
python -c "from app import create_app; app = create_app(); print('Flask app OK')"

# 依存関係確認
python -c "import qrcode, vobject, PIL; print('Dependencies OK')"

# データベース確認
flask db current
# 期待値: 17c0a24e93a2 (BerryCard用マイグレーション)
```

### 1.2 セッション1完了確認
```bash
# 実装済みファイル確認
ls -la app/blueprints/profiles.py
ls -la app/static/uploads/
ls -la app/templates/profiles/

# マイグレーション確認
ls -la migrations/versions/ | grep berrycard

# バックアップ確認
ls -la | grep backup_berrycard_session1
```

---

## 2. セッション2開始手順

### 2.1 バックアップ作成
```bash
# 現在時刻取得
date +%Y%m%d_%H%M%S
# 例: 20251018_060000

# フロントエンドバックアップ
cp -r frontend frontend_backup_berrycard_session2_start_$(date +%Y%m%d_%H%M%S)

# アプリケーションバックアップ
cp -r app app_backup_berrycard_session2_start_$(date +%Y%m%d_%H%M%S)
```

### 2.2 実装順序

#### Step 1: Pinia Store作成
```bash
# ファイル作成
touch frontend/src/stores/profiles.js
```

#### Step 2: ルーティング設定
```bash
# 既存ルーティングファイル確認
cat frontend/src/router/index.js
```

#### Step 3: Vue.jsコンポーネント作成
```bash
# ディレクトリ確認
ls -la frontend/src/views/
ls -la frontend/src/components/

# 新規ファイル作成
touch frontend/src/views/AppIndexPage.vue
touch frontend/src/views/CardApp.vue
touch frontend/src/components/ProfileEditForm.vue
touch frontend/src/components/DesignCustomizer.vue
touch frontend/src/components/ProfilePreview.vue
touch frontend/src/components/QRCodeDownload.vue
```

#### Step 4: 公開プロフィールテンプレート
```bash
# テンプレートファイル作成
touch app/templates/profiles/public_profile.html
```

---

## 3. 実装開始コマンド

### 3.1 セッション2開始宣言
```bash
# セッション2開始
echo "=== BerryCard セッション2開始 ==="
echo "実装目標: フロントエンド実装"
echo "開始時刻: $(date)"
echo "================================"
```

### 3.2 実装順序確認
```bash
# 実装順序表示
echo "実装順序:"
echo "1. Pinia Store (profiles.js)"
echo "2. ルーティング設定"
echo "3. AppIndexPage.vue"
echo "4. CardApp.vue"
echo "5. 子コンポーネント群"
echo "6. 公開プロフィールテンプレート"
```

---

## 4. 実装時の注意点

### 4.1 既存アプリ保持
- **重要**: 既存のInfluBerryアプリは絶対に変更しない
- 既存のコンポーネント（DashboardPage.vue等）は保持
- 既存のルーティング（/dashboard, /projects等）は保持
- 既存のPinia Store（auth.js等）は保持

### 4.2 新規実装方針
- セッション1で実装したAPIエンドポイントを活用
- 既存のコード構造を参考にした実装
- 段階的な実装とテスト
- 既存アプリとの統合確認

### 4.3 テスト方針
- 各コンポーネント作成後に動作確認
- 既存アプリの動作確認
- API通信の動作確認
- レスポンシブデザインの確認

---

## 5. 実装参考資料

### 5.1 要件定義書
```bash
# 要件定義書確認
cat docs/requirements/berrycard_requirements_v1.0.md | head -50
```

### 5.2 アーキテクチャ設計書
```bash
# セッション1完了版確認
cat docs/architecture/berrycard_architecture_v1.1_session1_completed.md | head -50
```

### 5.3 引き継ぎ書
```bash
# 引き継ぎ書確認
cat docs/handover/berrycard_session2_handover.md | head -50
```

### 5.4 既存コード参考
```bash
# 既存コンポーネント確認
ls -la frontend/src/views/
ls -la frontend/src/components/
ls -la frontend/src/stores/

# 既存ルーティング確認
cat frontend/src/router/index.js
```

---

## 6. トラブルシューティング

### 6.1 よくある問題
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

### 6.2 緊急時復旧手順
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

## 7. セッション2完了目標

### 7.1 必須完了項目
- ✅ AppIndexPage.vue 作成・動作確認
- ✅ CardApp.vue 作成・動作確認
- ✅ ProfileEditForm.vue 作成・動作確認
- ✅ DesignCustomizer.vue 作成・動作確認
- ✅ ProfilePreview.vue 作成・動作確認
- ✅ QRCodeDownload.vue 作成・動作確認
- ✅ profiles.js Pinia Store 作成・動作確認
- ✅ ルーティング設定完了
- ✅ 公開プロフィールテンプレート作成

### 7.2 動作確認項目
- ログイン後 `/app-index` にリダイレクト
- BerryCardアプリカードクリックで `/card` に遷移
- プロフィール編集フォーム動作確認
- リアルタイムプレビュー動作確認
- QRコード生成・ダウンロード動作確認
- 公開プロフィールページ表示確認

---

## 8. 次のセッション準備

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

セッション2では、フロントエンドの実装に集中し、ユーザーインターフェースの完成を目指します。

**重要**: 既存のInfluBerryアプリケーションは完全に保持されており、新機能が安全に統合されています。セッション2でも、この原則を守りながら実装を進めてください。

**成功の鍵**: 
1. 既存アプリの保持を最優先
2. 段階的な実装とテスト
3. 既存コードの構造を参考にした実装
4. セッション1で実装したAPIエンドポイントの活用

---

## 10. セッション2開始宣言

```bash
# セッション2開始宣言
echo "=== BerryCard セッション2開始 ==="
echo "実装目標: フロントエンド実装"
echo "開始時刻: $(date)"
echo "================================"

# 実装開始
echo "実装開始: Pinia Store (profiles.js) 作成"
```
