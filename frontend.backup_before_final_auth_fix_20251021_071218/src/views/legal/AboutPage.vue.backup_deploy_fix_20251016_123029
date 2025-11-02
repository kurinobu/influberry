<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// トップページに戻る
const goHome = () => {
  router.push('/')
}

// アプリ機能一覧
const features = [
  {
    icon: 'building',
    title: 'スポンサー案件管理',
    description: '案件の進捗管理から納期管理まで、お仕事を整理して効率アップ！'
  },
  {
    icon: 'document',
    title: '請求書自動生成',
    description: '案件情報から請求書を自動作成PDF印刷。近い将来、メール送信、会計ソフト連携予定！'
  },
  {
    icon: 'chart',
    title: 'ダッシュボード',
    description: '収益や案件状況が一目でわかる。あなたの成長が見える化されます。'
  }
]

// 将来追加予定機能
const comingSoonFeatures = [
  {
    icon: 'lightbulb',
    title: 'ブランド提案文ジェネレーター',
    description: 'AIがあなたにぴったりのブランド提案文を自動生成。'
  },
  {
    icon: 'calendar',
    title: '投稿アイデアカレンダー',
    description: 'コンテンツアイデアをカレンダーで管理。投稿スケジュールもバッチリ。'
  },
  {
    icon: 'money',
    title: '案件単価計算ツール',
    description: '適正な単価設定をサポート。あなたの価値を正しく評価します。'
  }
]
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50">
    <!-- ヘッダー -->
    <header class="berry-header">
      <div class="max-w-4xl mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
          <h1 class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-600 font-noto">
            🍓 InfluBerry
          </h1>
          <button
            @click="goHome"
            class="text-gray-600 hover:text-pink-500 transition-colors"
            aria-label="InfluBerryログインページに戻る"
          >
            ← ログインに戻る
          </button>
        </div>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="max-w-4xl mx-auto px-4 py-8">
      <!-- ヒーローセクション -->
      <section class="text-center mb-16">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          インフルエンサー・クリエイター向け
          <br>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-600">
            案件管理・請求書自動生成SaaS
          </span>
        </h1>
        <p class="text-xl text-gray-600 mb-8">
          案件管理から請求書作成まで、面倒な事務作業はInfluBerryにお任せ！<br>
          あなたはコンテンツ作りに集中できます。
        </p>
        
        <!-- 画像配置予定エリア（将来実装） -->
        <div class="berry-card-placeholder">
          <p class="text-gray-500">📱 アプリスクリーンショット（近日公開）</p>
        </div>
      </section>

      <!-- 現在の機能セクション -->
      <section class="mb-16">
        <h2 class="text-2xl font-bold text-gray-900 mb-8 text-center">
          今すぐ使える機能 - 効率化・省力化でDXを推進
        </h2>
        <div class="grid md:grid-cols-3 gap-8">
          <div
            v-for="feature in features"
            :key="feature.title"
            class="berry-card"
          >
            <div class="mb-4">
              <svg v-if="feature.icon === 'building'" class="w-12 h-12 text-pink-500 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
              <svg v-else-if="feature.icon === 'document'" class="w-12 h-12 text-pink-500 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              <svg v-else-if="feature.icon === 'chart'" class="w-12 h-12 text-pink-500 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ feature.title }}</h3>
            <p class="text-gray-600">{{ feature.description }}</p>
          </div>
        </div>
      </section>

      <!-- 将来追加予定機能セクション -->
      <section class="mb-16">
        <h2 class="text-2xl font-bold text-gray-900 mb-8 text-center">
          これから追加される機能 - さらなる効率化・省力化
        </h2>
        <div class="grid md:grid-cols-3 gap-8">
          <div
            v-for="feature in comingSoonFeatures"
            :key="feature.title"
            class="bg-white rounded-lg shadow-md p-6 relative"
          >
            <div class="absolute top-4 right-4">
              <span class="bg-purple-100 text-purple-600 text-xs px-2 py-1 rounded">
                準備中
              </span>
            </div>
            <div class="mb-4 opacity-60">
              <svg v-if="feature.icon === 'lightbulb'" class="w-12 h-12 text-purple-500 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
              </svg>
              <svg v-else-if="feature.icon === 'calendar'" class="w-12 h-12 text-purple-500 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
              <svg v-else-if="feature.icon === 'money'" class="w-12 h-12 text-purple-500 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-700 mb-2">{{ feature.title }}</h3>
            <p class="text-gray-500">{{ feature.description }}</p>
          </div>
        </div>
      </section>

      <!-- ターゲット説明セクション -->
      <section class="bg-white rounded-lg shadow-md p-8" style="margin-bottom: 3rem;">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 text-center">
          こんな方におすすめ - Z世代女子・クリエイター向け
        </h2>
        <div class="grid md:grid-cols-2 gap-6">
          <div class="flex items-start space-x-4">
            <div class="w-8 h-8 flex items-center justify-center">
              <svg class="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path>
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900 mb-2">インフルエンサー初心者</h3>
              <p class="text-gray-600">案件管理や請求書作成などの事務作業に慣れていない方</p>
            </div>
          </div>
          <div class="flex items-start space-x-4">
            <div class="w-8 h-8 flex items-center justify-center">
              <svg class="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900 mb-2">Z世代クリエイター</h3>
              <p class="text-gray-600">TikTok、Instagram、YouTubeなどで活動中の方</p>
            </div>
          </div>
          <div class="flex items-start space-x-4">
            <div class="w-8 h-8 flex items-center justify-center">
              <svg class="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900 mb-2">効率化したい方</h3>
              <p class="text-gray-600">事務作業の時間を減らして、コンテンツ作りに集中したい方</p>
            </div>
          </div>
          <div class="flex items-start space-x-4">
            <div class="w-8 h-8 flex items-center justify-center">
              <svg class="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900 mb-2">収益アップを目指す方</h3>
              <p class="text-gray-600">案件の見える化で収益管理を徹底したい方</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 使い方セクション -->
      <section class="rounded-lg text-white p-8 text-center" style="background-color: rgb(249, 168, 212);">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">
          使い方はとってもシンプル！<br>3ステップで始められるSaaS
        </h2>
        <div class="grid md:grid-cols-3 gap-6" style="margin-bottom: 2rem;">
          <div class="text-center">
            <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center mx-auto" style="margin-bottom: 2rem;">
              <span class="text-2xl font-bold text-pink-500">1</span>
            </div>
            <p class="text-gray-800 text-lg font-bold bg-white px-4 py-2 rounded-lg shadow-lg">無料でアカウント作成</p>
          </div>
          <div class="text-center">
            <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center mx-auto" style="margin-bottom: 2rem;">
              <span class="text-2xl font-bold text-pink-500">2</span>
            </div>
            <p class="text-gray-800 text-lg font-bold bg-white px-4 py-2 rounded-lg shadow-lg">案件情報を登録</p>
          </div>
          <div class="text-center">
            <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center mx-auto" style="margin-bottom: 2rem;">
              <span class="text-2xl font-bold text-pink-500">3</span>
            </div>
            <p class="text-gray-800 text-lg font-bold bg-white px-4 py-2 rounded-lg shadow-lg">請求書ボタンで<br>一発自動生成</p>
          </div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 1.5rem;">
          <button
            @click="goHome"
            class="px-8 py-3 bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-full hover:from-pink-600 hover:to-purple-700 transition-all duration-300 text-lg font-semibold shadow-lg hover:shadow-xl"
            aria-label="InfluBerryにログインして案件管理・請求書自動生成SaaSを開始"
          >
            今すぐInfluBerryを始める
          </button>
          
          <!-- ソーシャルシェア -->
          <div class="flex justify-center gap-6" style="margin-top: 1.5rem;">
            <a
              href="https://x.com/intent/tweet?text=InfluBerryでインフルエンサー・クリエイターの効率化・省力化を実現！案件管理・請求書自動生成SaaS&url=https://influberry.com"
              target="_blank"
              rel="noopener noreferrer"
              class="bg-black text-white px-6 py-3 rounded-lg hover:bg-gray-800 transition-colors text-sm flex items-center space-x-2"
              style="background-color: #000000 !important; color: #ffffff !important;"
              aria-label="Xでシェア"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
              </svg>
              <span>X</span>
            </a>
            <a
              href="https://www.threads.net/intent/post?text=InfluBerryでインフルエンサー・クリエイターの効率化・省力化を実現！案件管理・請求書自動生成SaaS&url=https://influberry.com"
              target="_blank"
              rel="noopener noreferrer"
              class="bg-black text-white px-6 py-3 rounded-lg hover:bg-gray-800 transition-colors text-sm flex items-center space-x-2"
              style="background-color: #000000 !important; color: #ffffff !important;"
              aria-label="Threadsでシェア"
            >
              <img src="/static/images/sns/threads-logo.svg" alt="Threads" class="h-4 w-auto" style="filter: invert(1);" />
              <span></span>
            </a>
            <a
              href="https://line.me/R/msg/text/?InfluBerryでインフルエンサー・クリエイターの効率化・省力化を実現！案件管理・請求書自動生成SaaS https://influberry.com"
              target="_blank"
              rel="noopener noreferrer"
              class="bg-white text-green-500 px-6 py-3 rounded-lg hover:bg-gray-100 transition-colors text-sm flex items-center space-x-2 border border-green-500"
              aria-label="LINEでシェア"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19.365 9.863c.349 0 .63.285.63.631 0 .345-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0 .344-.281.629-.63.629h-2.386c-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63h2.386c.349 0 .63.285.63.63 0 .349-.281.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443-3.317v2.94c0 .345-.279.629-.631.629-.346 0-.626-.284-.626-.629V8.108c0-.27.173-.51.43-.595.06-.023.136-.033.194-.033.195 0 .375.104.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0 .63.285.63.63v4.771zm-5.741 0c0 .345-.279.629-.631.629-.345 0-.627-.284-.627-.629V8.108c0-.345.282-.63.63-.63.346 0 .628.285.628.63v4.771zm-2.466.629H4.917c-.345 0-.63-.284-.63-.629V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756c.348 0 .629.283.629.63 0 .344-.281.629-.629.629M24 10.314C24 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078 9.436-6.975C23.176 14.393 24 12.458 24 10.314"/>
              </svg>
              <span>LINE</span>
            </a>
          </div>
        </div>
      </section>
    </main>

    <!-- フッター -->
    <footer class="berry-footer">
      <div class="berry-footer-inner">
        <p class="text-white">© 2025 InfluBerry by Air Edison. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* AboutPage専用スタイル */
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

/* Phase 4 berry化CSS - TodoApp.vue成功パターン移植 */
.berry-header {
  background: linear-gradient(135deg, #ffffff 0%, #fdf2f8 100%);
  border-bottom: 2px solid #f9a8d4;
  box-shadow: 0 4px 12px rgba(244, 114, 182, 0.15);
}

.berry-card {
  background: linear-gradient(135deg, #ffffff 0%, #fdf2f8 100%);
  border-radius: 1rem;
  box-shadow: 0 8px 20px rgba(244, 114, 182, 0.12);
  border: 2px solid #f9a8d4;
  padding: 1.5rem;
  transition: all 0.3s ease;
  margin-bottom: 1rem;
}

.berry-card:hover {
  box-shadow: 0 12px 30px rgba(244, 114, 182, 0.2);
  transform: scale(1.02) translateY(-2px);
}

.berry-card-placeholder {
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  border-radius: 1rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border: 2px solid #d1d5db;
  padding: 2rem;
  margin-bottom: 2rem;
}

.berry-footer {
  background: linear-gradient(to right, #ec4899 0%, #9333ea 100%) !important;
  border-top: 2px solid #f9a8d4 !important;
  color: #ffffff !important;
  padding: 2rem 0 !important;
  box-shadow: 0 -4px 12px rgba(244, 114, 182, 0.15) !important;
  min-height: 120px !important;
}

.berry-footer-inner {
  max-width: 64rem;
  margin: 0 auto;
  padding: 0 1rem;
  text-align: center;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>