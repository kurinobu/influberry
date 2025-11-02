<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// トップページに戻る
const goHome = () => {
  router.push('/')
}

// ブログ記事一覧
const blogPosts = [
  {
    id: 1,
    title: 'インフルエンサー・クリエイターの事務作業を効率化するSaaSツール活用法',
    excerpt: '案件管理から請求書作成まで、インフルエンサー・クリエイターの事務作業を効率化するSaaSツールの活用法を詳しく解説。省力化・DXでバックヤード業務を最適化。',
    date: '2025-01-15',
    category: '効率化',
    readTime: '5分',
    image: '/blog-images/efficiency-saas.jpg',
    slug: 'influencer-creator-efficiency-saas'
  },
  {
    id: 2,
    title: 'Z世代女子クリエイターの収益管理術 - 請求書自動生成で省力化',
    excerpt: 'Z世代女子クリエイターが収益管理を効率化する方法。請求書自動生成ツールを使った省力化テクニックとバックオフィス業務の最適化について。',
    date: '2025-01-14',
    category: '収益管理',
    readTime: '7分',
    image: '/blog-images/revenue-management.jpg',
    slug: 'z-generation-creator-revenue-management'
  },
  {
    id: 3,
    title: 'スポンサー案件管理で失敗しないためのタスク管理術',
    excerpt: 'スポンサー案件管理でよくある失敗を避けるためのタスク管理術。todoリスト活用とプロジェクト管理のベストプラクティスを紹介。',
    date: '2025-01-13',
    category: '案件管理',
    readTime: '6分',
    image: '/blog-images/project-management.jpg',
    slug: 'sponsor-project-task-management'
  },
  {
    id: 4,
    title: 'クリエイター向けDX推進 - デジタル化で業務効率を3倍向上',
    excerpt: 'クリエイター向けのDX推進方法。デジタル化で業務効率を3倍向上させる具体的なステップとツール選びのポイントを解説。',
    date: '2025-01-12',
    category: 'DX',
    readTime: '8分',
    image: '/blog-images/dx-transformation.jpg',
    slug: 'creator-dx-digital-transformation'
  },
  {
    id: 5,
    title: 'バックヤード業務の自動化でクリエイターの時間を有効活用',
    excerpt: 'バックヤード業務の自動化でクリエイターの時間を有効活用する方法。請求書管理、案件管理、タスク管理の自動化テクニック。',
    date: '2025-01-11',
    category: '自動化',
    readTime: '6分',
    image: '/blog-images/backyard-automation.jpg',
    slug: 'backyard-automation-creator-time'
  }
]

// カテゴリ一覧
const categories = [
  { name: '効率化', count: 1 },
  { name: '収益管理', count: 1 },
  { name: '案件管理', count: 1 },
  { name: 'DX', count: 1 },
  { name: '自動化', count: 1 }
]
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50">
    <!-- ヘッダー -->
    <header class="berry-header">
      <div class="max-w-6xl mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
          <h1 class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-600 font-noto">
            🍓 InfluBerry Blog
          </h1>
          <button
            @click="goHome"
            class="text-gray-600 hover:text-pink-500 transition-colors"
            aria-label="InfluBerryメインページに戻る"
          >
            ← メインに戻る
          </button>
        </div>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="max-w-6xl mx-auto px-4 py-8">
      <!-- ヒーローセクション -->
      <section class="text-center mb-16">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          インフルエンサー・クリエイター向け
          <br>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-600">
            効率化・省力化ブログ
          </span>
        </h1>
        <p class="text-xl text-gray-600 mb-8">
          SaaSツール活用、DX推進、バックヤード業務最適化のノウハウを発信<br>
          Z世代女子クリエイターの成功をサポート
        </p>
      </section>

      <!-- ブログ記事一覧 -->
      <section class="mb-16">
        <h2 class="text-3xl font-bold text-gray-900 mb-8 text-center">
          最新記事 - 効率化・省力化でDXを推進
        </h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <article
            v-for="post in blogPosts"
            :key="post.id"
            class="berry-card cursor-pointer hover:shadow-xl transition-all duration-300"
          >
            <div class="aspect-w-16 aspect-h-9 mb-4">
              <div class="bg-gradient-to-br from-pink-100 to-purple-100 rounded-lg flex items-center justify-center">
                <span class="text-4xl">📝</span>
              </div>
            </div>
            <div class="p-6">
              <div class="flex items-center justify-between mb-3">
                <span class="bg-pink-100 text-pink-800 text-xs px-2 py-1 rounded-full">
                  {{ post.category }}
                </span>
                <span class="text-sm text-gray-500">{{ post.readTime }}</span>
              </div>
              <h3 class="text-lg font-semibold text-gray-900 mb-3 line-clamp-2">
                {{ post.title }}
              </h3>
              <p class="text-gray-600 text-sm mb-4 line-clamp-3">
                {{ post.excerpt }}
              </p>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-500">{{ post.date }}</span>
                <button class="text-pink-600 hover:text-pink-800 text-sm font-medium">
                  続きを読む →
                </button>
              </div>
            </div>
          </article>
        </div>
      </section>

      <!-- カテゴリ一覧 -->
      <section class="bg-white rounded-lg shadow-md p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 text-center">
          カテゴリ別記事 - 効率化・省力化の専門知識
        </h2>
        <div class="grid md:grid-cols-5 gap-4">
          <div
            v-for="category in categories"
            :key="category.name"
            class="text-center p-4 bg-gradient-to-br from-pink-50 to-purple-50 rounded-lg hover:shadow-md transition-all duration-300 cursor-pointer"
          >
            <h3 class="font-semibold text-gray-900 mb-2">{{ category.name }}</h3>
            <p class="text-sm text-gray-600">{{ category.count }}記事</p>
          </div>
        </div>
      </section>

      <!-- CTA セクション -->
      <section class="bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg text-white p-8 text-center">
        <h2 class="text-2xl font-bold mb-4">
          InfluBerryで効率化・省力化を実現
        </h2>
        <p class="text-lg mb-6">
          案件管理・請求書自動生成・タスク管理でDXを推進<br>
          Z世代女子クリエイターの成功をサポート
        </p>
        <button
          @click="goHome"
          class="bg-white text-pink-500 font-semibold px-8 py-3 rounded-lg hover:bg-gray-100 transition-colors"
          aria-label="InfluBerryにログインして効率化・省力化SaaSを開始"
        >
          今すぐ始める
        </button>
      </section>
    </main>

    <!-- フッター -->
    <footer class="berry-footer">
      <div class="berry-footer-inner">
        <p class="text-gray-400">© 2025 InfluBerry Blog - Air Edison. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* ブログ専用スタイル */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Phase 4 berry化CSS */
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
  transition: all 0.3s ease;
}

.berry-card:hover {
  box-shadow: 0 12px 30px rgba(244, 114, 182, 0.2);
  transform: translateY(-2px);
}

.berry-footer {
  background: linear-gradient(135deg, #1f2937 0%, #374151 100%) !important;
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
