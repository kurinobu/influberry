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
        <h1 class="text-4xl font-bold text-gray-800 mb-4">運営会社情報</h1>
        <p class="text-gray-600 text-lg">InfluBerryを運営しているチームについて</p>
        <p class="text-sm text-gray-500 mt-2">最終更新日: {{ lastUpdated }}</p>
      </div>

      <!-- 運営会社情報 -->
      <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg p-8 space-y-8">
        
        <!-- 1. 会社概要 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-6 border-b border-pink-200 pb-2">会社概要</h2>
          <div class="grid md:grid-cols-2 gap-6">
            <div class="space-y-4">
              <div class="bg-pink-50 p-6 rounded-lg">
                <h3 class="font-semibold text-gray-800 mb-3 flex items-center">
                  <span class="text-pink-500 mr-2">🏢</span>
                  基本情報
                </h3>
                <div class="space-y-2 text-sm text-gray-700">
                  <p><strong>会社名:</strong> Air Edison（エアエジソン）</p>
                  <p><strong>運営責任者:</strong> 栗原伸行</p>
                  <p><strong>設立:</strong> 2020年</p>
                  <p><strong>事業内容:</strong> Webアプリケーション開発・運営</p>
                </div>
              </div>
            </div>
            
            <div class="space-y-4">
              <div class="bg-purple-50 p-6 rounded-lg">
                <h3 class="font-semibold text-gray-800 mb-3 flex items-center">
                  <span class="text-purple-500 mr-2">📍</span>
                  所在地・連絡先
                </h3>
                <div class="space-y-2 text-sm text-gray-700">
                  <p><strong>本社所在地:</strong><br>〒652-0804<br>神戸市兵庫区西出町２−３−２３</p>
                  <p><strong>電話番号:</strong> お問い合わせフォームにて承ります</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 2. 代表メッセージ -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-6 border-b border-pink-200 pb-2">代表メッセージ</h2>
          <div class="bg-gradient-to-r from-pink-50 to-purple-50 p-6 rounded-lg">
            <div class="flex items-start space-x-4">
              <div class="w-16 h-16 bg-gradient-to-r from-pink-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-xl">
                K
              </div>
              <div class="flex-1">
                <h3 class="font-bold text-gray-800 mb-2">栗原伸行（代表）</h3>
                <div class="text-gray-700 leading-relaxed space-y-3">
                  <p>InfluBerryをご利用いただき、ありがとうございます。</p>
                  <p>私たちAir Edisonは、インフルエンサーやクリエイターが活動しやすい環境を作ることを使命として、InfluBerryを開発しました。初心者の方でも簡単に案件管理ができ、クリエイティブな活動に集中できるツールを目指しています。</p>
                  <p>ユーザーの皆様からのご意見を大切にしながら、継続的にサービスを改善してまいります。何かご不明な点やご要望がございましたら、お気軽にお問い合わせください。</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 3. 事業内容 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-6 border-b border-pink-200 pb-2">事業内容</h2>
          <div class="grid md:grid-cols-3 gap-4">
            <div class="bg-blue-50 p-4 rounded-lg text-center">
              <div class="text-3xl mb-3">💻</div>
              <h3 class="font-semibold text-gray-800 mb-2">Webアプリ開発</h3>
              <p class="text-sm text-gray-600">モダンな技術を使った使いやすいWebアプリケーションの開発</p>
            </div>
            <div class="bg-green-50 p-4 rounded-lg text-center">
              <div class="text-3xl mb-3">🎯</div>
              <h3 class="font-semibold text-gray-800 mb-2">クリエイター支援</h3>
              <p class="text-sm text-gray-600">インフルエンサーやクリエイターの活動を支援するツールの提供</p>
            </div>
            <div class="bg-yellow-50 p-4 rounded-lg text-center">
              <div class="text-3xl mb-3">🔧</div>
              <h3 class="font-semibold text-gray-800 mb-2">システム運営</h3>
              <p class="text-sm text-gray-600">安全で安定したサービス運営とユーザーサポート</p>
            </div>
          </div>
        </section>

        <!-- 4. よくある質問 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-6 border-b border-pink-200 pb-2">よくある質問</h2>
          <div class="space-y-4">
            <div class="bg-white p-4 rounded-lg border border-gray-200">
              <h3 class="font-semibold text-gray-800 mb-2">Q. InfluBerryは無料で使えますか？</h3>
              <p class="text-sm text-gray-600">A. 基本機能は無料でご利用いただけます。将来的にプレミアムプランも予定しています。</p>
            </div>
            <div class="bg-white p-4 rounded-lg border border-gray-200">
              <h3 class="font-semibold text-gray-800 mb-2">Q. データのセキュリティは大丈夫ですか？</h3>
              <p class="text-sm text-gray-600">A. SSL暗号化、パスワード暗号化など、最新のセキュリティ技術を導入して皆様のデータをお守りしています。</p>
            </div>
            <div class="bg-white p-4 rounded-lg border border-gray-200">
              <h3 class="font-semibold text-gray-800 mb-2">Q. スマートフォンでも使えますか？</h3>
              <p class="text-sm text-gray-600">A. はい、スマートフォンのご利用を前提に開発しました。逆にPCでもご利用できます。</p>
            </div>
          </div>
        </section>

        <!-- 5. お問い合わせ -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-6 border-b border-pink-200 pb-2">お問い合わせ</h2>
          <div class="bg-gray-50 p-6 rounded-lg">
            <div class="space-y-2 text-sm">
              <p><strong>運営者:</strong> Air Edison（エアエジソン）</p>
              <p><strong>運営責任者:</strong> 栗原伸行</p>
              <p><strong>所在地:</strong> 神戸市兵庫区西出町２−３−２３</p>
              <p><strong>お問い合わせ:</strong> <a href="https://air-edison.com/ask/" class="text-pink-600 hover:text-pink-800 underline" target="_blank" rel="noopener noreferrer">https://air-edison.com/ask/</a></p>
              <p><strong>ホームページ:</strong> <a href="https://air-edison.com" class="text-pink-600 hover:text-pink-800 underline" target="_blank" rel="noopener noreferrer">https://air-edison.com</a></p>
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
/* 運営会社情報専用スタイル */
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
  
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>