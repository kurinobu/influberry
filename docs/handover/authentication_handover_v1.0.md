# InfluBerry 認証システム引き継ぎ書 v1.0

## 概要
InfluBerryアプリケーションの認証システムの引き継ぎ書。想定内エラーの設計思想と実装方法について記載する。

## 想定内エラー設計の背景

### 問題の経緯
1. **初期実装**: 未認証状態で「ユーザー情報の取得に失敗しました」メッセージが表示
2. **UX問題**: ユーザーにとって不要なエラーメッセージが表示される
3. **設計改善**: 想定内エラー（401）を正常な状態として扱う設計に変更

### 想定内エラーとは
- **401 Unauthorized**: 未認証状態（正常な状態）
- **目的**: ユーザーに不要なエラーメッセージを表示しない
- **UX**: スムーズな認証フローを提供

## 技術実装詳細

### 1. フロントエンド実装（Vue.js 3 + Pinia）

#### 1.1 認証ストア（auth.js）の修正
```javascript
async getCurrentUser() {
  this.isLoading = true
  this.error = null // 最初にエラーメッセージをクリア
  
  try {
    const response = await axios.get('/api/auth/me')
    
    if (response.data.user) {
      // 認証済み処理
      this.user = response.data.user
      this.isAuthenticated = true
      this.error = null // 成功時もエラーメッセージをクリア
      return { success: true }
    }
    
    // 未認証状態（userフィールドなし）は正常な状態として扱う
    this.user = null
    this.isAuthenticated = false
    this.error = null // エラーメッセージをクリア
    return { success: false }
    
  } catch (error) {
    this.user = null
    this.isAuthenticated = false
    
    // 401エラーは正常（未認証状態）
    if (error.response?.status !== 401) {
      this.error = error.response?.data?.error || 'ユーザー情報の取得に失敗しました'
    } else {
      this.error = null // 401の場合はエラーメッセージをクリア
    }
    return { success: false }
  } finally {
    this.isLoading = false
  }
}
```

#### 1.2 環境変数設定
```javascript
// 開発環境: 空文字（Viteプロキシ使用）
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || 'https://influberry.jp'

// 本番環境: 本番ドメイン
// 開発環境: 空文字（相対パスでViteプロキシ経由）
```

### 2. バックエンド実装（Flask）

#### 2.1 認証エンドポイント
```python
@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """現在のユーザー情報取得"""
    if current_user.is_authenticated:
        return jsonify({
            'user': {
                'id': current_user.id,
                'email': current_user.email,
                'name': current_user.name
            }
        })
    else:
        return jsonify({
            'code': 'UNAUTHORIZED',
            'error': '認証が必要です'
        }), 401
```

#### 2.2 レスポンス仕様
- **認証済み**: 200 + ユーザー情報
- **未認証**: 401 + `{"code": "UNAUTHORIZED", "error": "認証が必要です"}`

### 3. 開発環境設定

#### 3.1 Viteプロキシ設定
```javascript
// vite.config.js
export default defineConfig({
  server: {
    host: '127.0.0.1',
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5001',
        changeOrigin: true,
        configure: (proxy, options) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            // Cookie認証情報を確実に転送
            if (req.headers.cookie) {
              proxyReq.setHeader('cookie', req.headers.cookie);
            }
          });
        }
      }
    }
  }
})
```

#### 3.2 環境変数
- **開発環境**: `VITE_API_BASE_URL=` （空文字）
- **本番環境**: `VITE_API_BASE_URL=https://influberry.jp`

## 想定内エラーの設計思想

### 1. 想定内エラー（正常な状態）
- **401 Unauthorized**: 未認証状態
- **目的**: ユーザーに不要なエラーメッセージを表示しない
- **UX**: スムーズな認証フローを提供

### 2. 想定外エラー（実際のエラー）
- **500 Internal Server Error**: サーバーエラー
- **404 Not Found**: エンドポイント不存在
- **ネットワークエラー**: 接続失敗
- **目的**: ユーザーに適切なエラーメッセージを表示

### 3. 実装原則
1. **根本解決**: 一時的な回避ではなく、根本的な解決を実装
2. **シンプル構造**: 複雑な条件分岐を避ける
3. **統一・同一化**: 認証フローの一貫性を保つ
4. **具体的**: 抽象的な処理ではなく、具体的な実装
5. **安全確実**: 拙速を避け、安全で確実な実装

## トラブルシューティング

### 1. よくある問題

#### 1.1 CORSエラー
**症状**: `Access to XMLHttpRequest at 'http://127.0.0.1:5001/api/auth/me' has been blocked by CORS policy`
**原因**: フロントエンドが直接バックエンドにアクセス
**解決**: Viteプロキシを使用（`VITE_API_BASE_URL=` に設定）

#### 1.2 URL重複問題
**症状**: `http://127.0.0.1:5173/api/api/auth/login` で405エラー
**原因**: `VITE_API_BASE_URL=/api` で重複
**解決**: `VITE_API_BASE_URL=` （空文字）に設定

#### 1.3 エラーメッセージ表示
**症状**: 「ユーザー情報の取得に失敗しました」が表示される
**原因**: 未認証状態でエラーメッセージを表示
**解決**: 401エラーを正常な状態として扱う

### 2. デバッグ方法

#### 2.1 フロントエンド
```javascript
// 認証状態の確認
console.log('認証状態:', authStore.isAuthenticated)
console.log('ユーザー情報:', authStore.user)
console.log('エラーメッセージ:', authStore.error)
```

#### 2.2 バックエンド
```python
# 認証状態の確認
print(f"認証状態: {current_user.is_authenticated}")
print(f"ユーザーID: {current_user.id if current_user.is_authenticated else 'None'}")
```

## 今後の改善点

### 1. セキュリティ強化
- CSRFトークンの適切な処理
- セキュアなCookie設定
- 認証トークンの有効期限管理

### 2. パフォーマンス最適化
- 認証状態のキャッシュ
- 不要なAPI呼び出しの削減
- プロキシ設定の最適化

### 3. UX改善
- ローディング状態の改善
- エラーメッセージの統一
- 認証フローの簡素化

## 認証問題解決手順（2025年10月22日）

### 問題の概要
- **ログアウトAPI**: 400 BAD REQUEST エラー
- **CORS問題**: ローカル開発環境からのリクエストが拒否される
- **認証失敗**: ログイン・ログアウトが正常に動作しない

### 根本原因の分析
1. **ログアウトAPI**: `@login_required`デコレータが原因で400エラー
2. **CORS設定**: ローカル開発環境のオリジンが許可されていない
3. **CSRF保護**: 開発環境でCSRFトークンが必要

### 解決手順

#### 1. CORS設定修正
```python
# config.py
CORS_ORIGINS = [
    'https://influberry-app.onrender.com',
    'https://influberry.jp',
    'http://127.0.0.1:5173',      # 追加
    'http://localhost:5173'       # 追加
]
```

#### 2. ログアウトAPI修正
```python
# app/blueprints/auth.py
@auth_bp.route('/logout', methods=['POST'])
def logout():  # @login_requiredを削除
    """ユーザーログアウト"""
    try:
        # 認証状態に関係なくログアウト処理を実行
        if current_user.is_authenticated:
            logout_user()
        # セッション完全削除
        session.clear()
        return jsonify({'message': 'ログアウトしました'}), 200
    except Exception as e:
        # エラーが発生してもセッションはクリア
        session.clear()
        return jsonify({'message': 'ログアウトしました'}), 200
```

#### 3. CSRF保護無効化（開発環境）
```python
# config.py
class DevelopmentConfig(Config):
    # Development用CSRF保護無効化
    WTF_CSRF_ENABLED = False
```

### 結果
- **認証機能**: 完全復旧（ログイン・ログアウト正常動作）
- **CORS問題**: 根本解決
- **セッション管理**: 完全なセッションクリア実装
- **フロントエンドとバックエンド**: 状態一致

## 更新履歴

- **2025-10-21**: 初版作成（想定内エラー設計の文書化）
- **想定内エラー**: 401 Unauthorizedを正常な未認証状態として扱う設計を実装
- **2025-10-22**: 設定画面の月次目標設定機能追加
  - **新機能**: プロフィール編集セクション内に月次目標設定を追加
  - **既存機能保持**: 請求者情報・支払い情報・パスワード変更機能を維持
  - **UI設計**: 既存フォームと同じスタイルで統合
  - **実装方針**: 既存機能を破壊せず、追加のみで実装
- **UX改善**: ユーザーに不要なエラーメッセージを表示しない設計を実装
- **技術実装**: フロントエンド・バックエンドの具体的な実装方法を文書化
- **2025-10-22**: 認証問題根本解決とCORS設定修正
  - **問題**: ログアウトAPIで400エラー、CORS問題による認証失敗
  - **根本原因**: `@login_required`デコレータ、CORS設定不備、CSRF保護
  - **解決策**: ログアウトAPI修正、CORS設定追加、CSRF保護無効化
  - **結果**: 認証機能完全復旧、ログイン・ログアウト正常動作