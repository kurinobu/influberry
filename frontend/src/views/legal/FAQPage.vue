<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// トップページに戻る
const goHome = () => {
  router.push('/')
}

// FAQデータ
const faqCategories = [
  {
    name: '基本機能について',
    icon: 'tools',
    faqs: [
      {
        question: 'InfluBerryでできることは何ですか？',
        answer: 'InfluBerryはインフルエンサー・クリエイター向けの案件管理・請求書自動生成SaaSツールです。スポンサー案件管理、請求書自動生成、タスク管理・todoリスト機能で効率化・省力化を実現し、DXを推進します。'
      },
      {
        question: '請求書自動生成機能の使い方を教えてください',
        answer: '案件情報を登録し請求書ボタンをタップすると、自動的に請求書が生成されます。PDF出力もできます。メール送信、会計ソフト連携（予定）でバックオフィス業務を効率化できます。'
      },
      {
        question: 'タスク管理機能（BerryDo）の特徴は？',
        answer: 'BerryDoは優先度設定、期限管理、プロジェクト連携機能を持つタスク管理ツールです。todoリストで作業効率を最大化し、Z世代女子クリエイターの業務をサポートします。'
      }
    ]
  },
  {
    name: '料金・プランについて',
    icon: 'money',
    faqs: [
      {
        question: '料金プランはどのようになっていますか？',
        answer: '基本プランは無料、プレミアムプランは月額1,280円（予定）です。初回1ヶ月間は全ユーザー無料提供で、効率化・省力化の効果を実感いただけます。'
      },
      {
        question: '無料プランでも請求書自動生成は使えますか？',
        answer: 'はい、無料プランでも請求書自動生成機能をご利用いただけます。基本的な案件管理・請求書管理機能で効率化・省力化を実現できます。'
      }
    ]
  },
  {
    name: '技術・セキュリティについて',
    icon: 'security',
    faqs: [
      {
        question: 'データのセキュリティは大丈夫ですか？',
        answer: 'SSL/TLS暗号化通信、パスワード暗号化保存、アクセス制限・権限管理など、最新のセキュリティ技術でインフルエンサー・クリエイターの個人情報を保護します。'
      },
      {
        question: 'SaaSツールとしての信頼性は？',
        answer: 'Air Edison（エアエジソン）が開発・運営する信頼性の高いSaaSツールです。PostgreSQLデータベース、定期的なセキュリティ監査で安定したサービスを提供します。'
      }
    ]
  },
  {
    name: '効率化・省力化について',
    icon: 'lightning',
    faqs: [
      {
        question: 'どの程度の効率化・省力化が期待できますか？',
        answer: '事務作業時間を50-70%削減、案件管理の見える化で収益管理を徹底、バックヤード業務の自動化でクリエイターの時間を有効活用できます。'
      },
      {
        question: 'Z世代女子クリエイター向けの機能はありますか？',
        answer: '直感的なUI、モバイル対応、SNS連携機能（予定）など、Z世代女子クリエイターのニーズに特化した機能を提供します。'
      },
      {
        question: 'DX推進にどのように貢献しますか？',
        answer: 'デジタル化による業務効率向上、データ分析による意思決定支援、自動化による人的リソースの最適化でDXを推進します。'
      }
    ]
  }
]

// アコーディオン状態管理
const openItems = ref({})

const toggleItem = (categoryIndex, faqIndex) => {
  const key = `${categoryIndex}-${faqIndex}`
  openItems.value[key] = !openItems.value[key]
}

// アイコンマッピング
const getIcon = (iconName) => {
  const icons = {
    tools: 'tools',
    money: 'money',
    security: 'security',
    lightning: 'lightning'
  }
  return icons[iconName] || 'tools'
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50">
    <!-- ヘッダー -->
    <header class="berry-header">
      <div class="max-w-6xl mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
          <h1 class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-600 font-noto">
            🍓 InfluBerry FAQ
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
          よくある質問
          <br>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-600">
            InfluBerry効率化・省力化SaaS
          </span>
        </h1>
        <p class="text-xl text-gray-600 mb-8">
          インフルエンサー・クリエイター向け案件管理・請求書自動生成ツールの<br>
          よくある質問と回答をまとめました
        </p>
      </section>

      <!-- FAQ カテゴリ別 -->
      <section class="space-y-12">
        <div
          v-for="(category, categoryIndex) in faqCategories"
          :key="category.name"
          class="bg-white rounded-lg shadow-md p-8"
        >
          <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <svg v-if="category.icon === 'tools'" class="w-8 h-8 text-pink-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
            </svg>
            <svg v-else-if="category.icon === 'money'" class="w-8 h-8 text-pink-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
            </svg>
            <svg v-else-if="category.icon === 'security'" class="w-8 h-8 text-pink-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
            </svg>
            <svg v-else-if="category.icon === 'lightning'" class="w-8 h-8 text-pink-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
            {{ category.name }}
          </h2>
          
          <div class="space-y-4">
            <div
              v-for="(faq, faqIndex) in category.faqs"
              :key="faqIndex"
              class="border border-gray-200 rounded-lg"
            >
              <button
                @click="toggleItem(categoryIndex, faqIndex)"
                class="w-full text-left p-6 hover:bg-gray-50 transition-colors"
                :aria-expanded="openItems[`${categoryIndex}-${faqIndex}`]"
                :aria-controls="`faq-${categoryIndex}-${faqIndex}`"
              >
                <div class="flex items-center justify-between">
                  <h3 class="text-lg font-semibold text-gray-900 pr-4">
                    {{ faq.question }}
                  </h3>
                  <svg
                    class="w-5 h-5 text-gray-500 transform transition-transform"
                    :class="{ 'rotate-180': openItems[`${categoryIndex}-${faqIndex}`] }"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </div>
              </button>
              
              <div
                v-if="openItems[`${categoryIndex}-${faqIndex}`]"
                :id="`faq-${categoryIndex}-${faqIndex}`"
                class="px-6 pb-6 text-gray-600 leading-relaxed"
              >
                {{ faq.answer }}
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- お問い合わせセクション -->
      <section class="bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg text-white p-8 text-center mt-16">
        <h2 class="text-2xl font-bold mb-4">
          他にご質問はありませんか？
        </h2>
        <p class="text-lg mb-6">
          効率化・省力化、SaaSツール活用、DX推進について<br>
          お気軽にお問い合わせください
        </p>
        <a
          href="https://air-edison.com/ask/"
          target="_blank"
          rel="noopener noreferrer"
          class="bg-white text-pink-500 font-semibold px-8 py-3 rounded-lg hover:bg-gray-100 transition-colors inline-block"
          aria-label="InfluBerryお問い合わせページを開く"
        >
          お問い合わせ
        </a>
      </section>
    </main>

    <!-- フッター -->
    <footer class="berry-footer">
      <div class="berry-footer-inner">
        <p class="text-white">© 2025 InfluBerry FAQ - Air Edison. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* FAQ専用スタイル */
.berry-header {
  background: linear-gradient(135deg, #ffffff 0%, #fdf2f8 100%);
  border-bottom: 2px solid #f9a8d4;
  box-shadow: 0 4px 12px rgba(244, 114, 182, 0.15);
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
