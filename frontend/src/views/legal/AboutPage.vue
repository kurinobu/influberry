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
    icon: '🏢',
    title: 'スポンサー案件管理',
    description: '案件の進捗管理から納期管理まで、お仕事を整理して効率アップ！'
  },
  {
    icon: '📋',
    title: '請求書自動生成',
    description: '案件情報から請求書を自動作成。面倒な事務作業はInfluBerryにお任せ！'
  },
  {
    icon: '📊',
    title: 'ダッシュボード',
    description: '収益や案件状況が一目でわかる。あなたの成長が見える化されます。'
  }
]

// 将来追加予定機能
const comingSoonFeatures = [
  {
    icon: '💡',
    title: 'ブランド提案文ジェネレーター',
    description: 'AIがあなたにぴったりのブランド提案文を自動生成。'
  },
  {
    icon: '📅',
    title: '投稿アイデアカレンダー',
    description: 'コンテンツアイデアをカレンダーで管理。投稿スケジュールもバッチリ。'
  },
  {
    icon: '💰',
    title: '案件単価計算ツール',
    description: '適正な単価設定をサポート。あなたの価値を正しく評価します。'
  }
]
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50">
    <!-- ヘッダー -->
    <header class="bg-white shadow-sm">
      <div class="max-w-4xl mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
          <h1 class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-600 font-poppins">
            🍓 InfluBerry
          </h1>
          <button
            @click="goHome"
            class="text-gray-600 hover:text-pink-500 transition-colors"
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
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          Z世代インフルエンサーのための
          <br>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-600">
            オールインワンツール
          </span>
        </h2>
        <p class="text-xl text-gray-600 mb-8">
          案件管理から請求書作成まで、面倒な事務作業はInfluBerryにお任せ！<br>
          あなたはコンテンツ作りに集中できます。
        </p>
        
        <!-- 画像配置予定エリア（将来実装） -->
        <div class="bg-gray-100 rounded-lg p-8 mb-8">
          <p class="text-gray-500">📱 アプリスクリーンショット（近日公開）</p>
        </div>
      </section>

      <!-- 現在の機能セクション -->
      <section class="mb-16">
        <h3 class="text-2xl font-bold text-gray-900 mb-8 text-center">
          今すぐ使える機能
        </h3>
        <div class="grid md:grid-cols-3 gap-8">
          <div
            v-for="feature in features"
            :key="feature.title"
            class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
          >
            <div class="text-4xl mb-4">{{ feature.icon }}</div>
            <h4 class="text-lg font-semibold text-gray-900 mb-2">{{ feature.title }}</h4>
            <p class="text-gray-600">{{ feature.description }}</p>
          </div>
        </div>
      </section>

      <!-- 将来追加予定機能セクション -->
      <section class="mb-16">
        <h3 class="text-2xl font-bold text-gray-900 mb-8 text-center">
          これから追加される機能
        </h3>
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
            <div class="text-4xl mb-4 opacity-60">{{ feature.icon }}</div>
            <h4 class="text-lg font-semibold text-gray-700 mb-2">{{ feature.title }}</h4>
            <p class="text-gray-500">{{ feature.description }}</p>
          </div>
        </div>
      </section>

      <!-- ターゲット説明セクション -->
      <section class="bg-white rounded-lg shadow-md p-8 mb-8">
        <h3 class="text-2xl font-bold text-gray-900 mb-6 text-center">
          こんな方におすすめ
        </h3>
        <div class="grid md:grid-cols-2 gap-6">
          <div class="flex items-start space-x-4">
            <div class="text-2xl">🌟</div>
            <div>
              <h4 class="font-semibold text-gray-900 mb-2">インフルエンサー初心者</h4>
              <p class="text-gray-600">案件管理や請求書作成などの事務作業に慣れていない方</p>
            </div>
          </div>
          <div class="flex items-start space-x-4">
            <div class="text-2xl">📱</div>
            <div>
              <h4 class="font-semibold text-gray-900 mb-2">Z世代クリエイター</h4>
              <p class="text-gray-600">TikTok、Instagram、YouTubeなどで活動中の方</p>
            </div>
          </div>
          <div class="flex items-start space-x-4">
            <div class="text-2xl">⏰</div>
            <div>
              <h4 class="font-semibold text-gray-900 mb-2">効率化したい方</h4>
              <p class="text-gray-600">事務作業の時間を減らして、コンテンツ作りに集中したい方</p>
            </div>
          </div>
          <div class="flex items-start space-x-4">
            <div class="text-2xl">💎</div>
            <div>
              <h4 class="font-semibold text-gray-900 mb-2">収益アップを目指す方</h4>
              <p class="text-gray-600">案件の見える化で収益管理を徹底したい方</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 使い方セクション -->
      <section class="bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg text-white p-8 text-center">
        <h3 class="text-2xl font-bold mb-4">
          使い方はとってもシンプル！
        </h3>
        <div class="grid md:grid-cols-3 gap-6 mb-6">
          <div>
            <div class="text-3xl mb-2">1️⃣</div>
            <p>無料でアカウント作成</p>
          </div>
          <div>
            <div class="text-3xl mb-2">2️⃣</div>
            <p>案件情報を登録</p>
          </div>
          <div>
            <div class="text-3xl mb-2">3️⃣</div>
            <p>請求書を自動生成</p>
          </div>
        </div>
        <button
          @click="goHome"
          class="bg-white text-pink-500 font-semibold px-8 py-3 rounded-lg hover:bg-gray-100 transition-colors"
        >
          今すぐ始める
        </button>
      </section>
    </main>

    <!-- フッター -->
    <footer class="bg-gray-900 text-white py-8">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <p class="text-gray-400">© 2025 InfluBerry by Air Edison. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* Z世代向けモダンデザイン */
.font-poppins {
  font-family: 'Poppins', sans-serif;
}

/* スムーズなトランジション */
.transition-colors {
  transition-property: color, background-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

.transition-shadow {
  transition-property: box-shadow;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* グラデーション背景 */
.bg-gradient-to-br {
  background-image: linear-gradient(to bottom right, var(--tw-gradient-stops));
}

.bg-gradient-to-r {
  background-image: linear-gradient(to right, var(--tw-gradient-stops));
}

/* レスポンシブ調整 */
@media (max-width: 768px) {
  .text-4xl {
    font-size: 2rem;
  }
  
  .text-2xl {
    font-size: 1.5rem;
  }
}
</style>