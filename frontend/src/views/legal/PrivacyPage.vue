<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// トップページに戻る
const goHome = () => {
  router.push('/')
}

// 最終更新日
const lastUpdated = '2025年9月17日'
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-pink-100">
    <!-- ヘッダー -->
    <div class="bg-white/80 backdrop-blur-sm border-b border-pink-200">
      <div class="max-w-4xl mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <span class="text-2xl">🍓</span>
            <h1 class="text-xl font-bold text-gray-800">InfluBerry</h1>
          </div>
          <button 
            @click="goHome"
            class="px-4 py-2 bg-pink-500 text-white rounded-full hover:bg-pink-600 transition-colors text-sm font-medium"
          >
            ログインに戻る
          </button>
        </div>
      </div>
    </div>

    <!-- メインコンテンツ -->
    <div class="max-w-4xl mx-auto px-4 py-8">
      <!-- タイトルセクション -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-800 mb-4">プライバシーポリシー</h1>
        <p class="text-gray-600 text-lg">あなたの個人情報を大切に守ります</p>
        <p class="text-sm text-gray-500 mt-2">最終更新日: {{ lastUpdated }}</p>
      </div>

      <!-- プライバシーポリシー内容 -->
      <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg p-8 space-y-8">
        
        <!-- 1. 基本方針 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">1. 基本方針</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <p>InfluBerry（以下「当サービス」）を運営するAir Edison（エアエジソン）（以下「当社」）は、ユーザーの皆様の個人情報の保護を重要な責務と考え、個人情報の保護に関する法律（個人情報保護法）、その他の関係法令等を遵守し、適切に取り扱います。</p>
            <p>特にZ世代の女性インフルエンサーの皆様が安心してご利用いただけるよう、最新のセキュリティ技術と透明性のある運営を心がけています。</p>
          </div>
        </section>

        <!-- 2. 取得する個人情報 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">2. 取得する個人情報</h2>
          <div class="text-gray-700 leading-relaxed">
            <p class="mb-3">当サービスでは、以下の個人情報を取得いたします：</p>
            <div class="bg-pink-50 p-4 rounded-lg">
              <h3 class="font-semibold text-gray-800 mb-2">基本情報</h3>
              <ul class="list-disc list-inside space-y-1 text-sm">
                <li>ユーザー名、メールアドレス</li>
                <li>インフルエンサー名（任意）</li>
                <li>パスワード（暗号化して保存）</li>
              </ul>
            </div>
            <div class="bg-purple-50 p-4 rounded-lg mt-3">
              <h3 class="font-semibold text-gray-800 mb-2">サービス利用情報</h3>
              <ul class="list-disc list-inside space-y-1 text-sm">
                <li>スポンサー案件情報（企業名、プロジェクト名、金額等）</li>
                <li>請求書作成データ</li>
                <li>サービス利用履歴、アクセスログ</li>
                <li>Cookie情報（認証・利便性向上のため）</li>
              </ul>
            </div>
          </div>
        </section>

        <!-- 3. 個人情報の利用目的 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">3. 個人情報の利用目的</h2>
          <div class="text-gray-700 leading-relaxed">
            <p class="mb-3">取得した個人情報は、以下の目的で利用いたします：</p>
            <ul class="list-disc list-inside space-y-2 ml-4">
              <li>サービスの提供・運営・改善</li>
              <li>ユーザー認証・本人確認</li>
              <li>カスタマーサポート・お問い合わせ対応</li>
              <li>利用状況の分析・統計情報の作成（個人を特定できない形式）</li>
              <li>重要なお知らせ・サービス更新情報の通知</li>
              <li>法令に基づく対応</li>
            </ul>
          </div>
        </section>

        <!-- 4. Cookie の使用について -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">4. Cookieの使用について</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <p>当サービスでは、ユーザーの利便性向上のためCookieを使用しています。</p>
            <div class="bg-yellow-50 p-4 rounded-lg">
              <h3 class="font-semibold text-gray-800 mb-2">Cookieの用途</h3>
              <ul class="list-disc list-inside space-y-1 text-sm">
                <li>ログイン状態の維持（Flask-Login認証システム）</li>
                <li>ユーザー設定の記憶</li>
                <li>サービス利用状況の分析</li>
              </ul>
            </div>
            <p>ブラウザの設定によりCookieを無効にすることも可能ですが、一部機能がご利用いただけなくなる場合があります。</p>
          </div>
        </section>

        <!-- 5. 個人情報の共有・第三者提供 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">5. 個人情報の共有・第三者提供</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <p>当社は、以下の場合を除き、ユーザーの個人情報を第三者に提供いたしません：</p>
            <ul class="list-disc list-inside space-y-2 ml-4">
              <li>ユーザーの同意がある場合</li>
              <li>法令に基づく場合</li>
              <li>人の生命、身体または財産の保護のために必要がある場合</li>
              <li>サービス運営に必要な業務委託先（適切な管理体制下）</li>
            </ul>
            <div class="bg-green-50 p-4 rounded-lg mt-4">
              <p class="text-sm font-medium">🔒 当サービスは、ユーザーの個人情報を外部サービスに不当に提供することはありません。</p>
            </div>
          </div>
        </section>

        <!-- 6. 個人情報の保管・セキュリティ -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">6. 個人情報の保管・セキュリティ</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <p>当社は、個人情報を適切に保護するため、以下の対策を講じています：</p>
            <ul class="list-disc list-inside space-y-2 ml-4">
              <li>SSL/TLS暗号化通信の使用</li>
              <li>パスワードの暗号化保存（Werkzeugハッシュ化）</li>
              <li>アクセス制限・権限管理</li>
              <li>定期的なセキュリティ監査</li>
              <li>PostgreSQLデータベースの適切な管理</li>
            </ul>
          </div>
        </section>

        <!-- 7. ユーザーの権利 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">7. ユーザーの権利</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <p>ユーザーは、ご自身の個人情報について以下の権利を有します：</p>
            <ul class="list-disc list-inside space-y-2 ml-4">
              <li>開示・訂正・削除の請求</li>
              <li>利用停止の請求</li>
              <li>アカウントの削除</li>
            </ul>
            <p>これらのご要望がある場合は、下記お問い合わせ先までご連絡ください。</p>
          </div>
        </section>

        <!-- 8. GDPR・国際対応 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">8. GDPR・国際対応</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <p>当サービスは、EU一般データ保護規則（GDPR）にも配慮した運営を行っています。EU圏内のユーザーには追加の権利が適用される場合があります。</p>
          </div>
        </section>

        <!-- 9. プライバシーポリシーの変更 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">9. プライバシーポリシーの変更</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <p>当社は、法令の変更やサービス内容の変更に伴い、本プライバシーポリシーを変更する場合があります。重要な変更については、サービス内での通知または当ページでの告知を行います。</p>
          </div>
        </section>

        <!-- 10. お問い合わせ -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">10. お問い合わせ</h2>
          <div class="text-gray-700 leading-relaxed">
            <p class="mb-4">個人情報の取り扱いに関するお問い合わせは、以下までご連絡ください：</p>
            <div class="bg-gray-50 p-4 rounded-lg">
              <div class="space-y-2 text-sm">
                <p><strong>運営者:</strong> Air Edison（エアエジソン）</p>
                <p><strong>運営責任者:</strong> 栗原伸行</p>
                <p><strong>所在地:</strong> 神戸市兵庫区西出町２−３−２３</p>
                <p><strong>お問い合わせ:</strong> <a href="https://air-edison.com/ask/" class="text-pink-600 hover:text-pink-800 underline" target="_blank" rel="noopener noreferrer">https://air-edison.com/ask/</a></p>
                <p><strong>ホームページ:</strong> <a href="https://air-edison.com" class="text-pink-600 hover:text-pink-800 underline" target="_blank" rel="noopener noreferrer">https://air-edison.com</a></p>
              </div>
            </div>
          </div>
        </section>

      </div>

      <!-- フッター -->
      <div class="text-center mt-12 py-8">
        <button 
          @click="goHome"
          class="px-8 py-3 bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-full hover:from-pink-600 hover:to-purple-700 transition-all duration-300 text-lg font-semibold shadow-lg hover:shadow-xl"
        >
          今すぐInfluBerryを始める
        </button>
        <p class="text-gray-500 text-sm mt-4">© 2025 InfluBerry - Air Edison. All rights reserved.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* プライバシーポリシー専用スタイル */
section h2 {
  scroll-margin-top: 100px;
}

/* スムーススクロール */
html {
  scroll-behavior: smooth;
}

/* レスポンシブ対応 */
@media (max-width: 768px) {
  .max-w-4xl {
    max-width: 100%;
    margin: 0 auto;
  }
  
  .px-4 {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>