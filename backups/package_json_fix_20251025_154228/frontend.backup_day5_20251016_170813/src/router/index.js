import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

// ページコンポーネントのインポート
import AuthPage from '../views/AuthPage.vue'
import DashboardPage from '../views/DashboardPage.vue'
import ProjectApp from '../views/ProjectApp.vue'
import InvoiceApp from '../views/InvoiceApp.vue'
import TodoApp from '../views/TodoApp.vue'
// 法的ページコンポーネント
import AboutPage from '../views/legal/AboutPage.vue'
import PrivacyPage from '../views/legal/PrivacyPage.vue'
import TermsPage from '../views/legal/TermsPage.vue'
import CompanyPage from '../views/legal/CompanyPage.vue'
import TokushoPage from '../views/legal/TokushoPage.vue'
import BlogPage from '../views/legal/BlogPage.vue'
import FAQPage from '../views/legal/FAQPage.vue'

// ルート定義（3層分離アーキテクチャ）
const routes = [
  // 1層目: 認証ページ（未認証専用）
  {
    path: '/',
    name: 'Auth',
    component: AuthPage,
    meta: { 
      requiresGuest: true,  // 未認証ユーザーのみアクセス可能
      title: 'InfluBerry - ログイン',
      description: 'InfluBerryにログインして、インフルエンサー・クリエイター向けの案件管理・請求書自動生成SaaSツールを利用開始。効率化・省力化でDXを推進。',
      keywords: 'InfluBerry,ログイン,インフルエンサー,クリエイター,SaaS,DX,効率化,省力化'
    }
  },
  
  // 2層目: メインダッシュボード（認証後・プラグイン選択）
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardPage,
    meta: { 
      requiresAuth: true,   // 認証必須
      title: 'InfluBerry - ダッシュボード',
      description: 'InfluBerryダッシュボードで案件管理・請求書管理・タスク管理を一元化。インフルエンサー・クリエイターの効率化・省力化をサポートするSaaSツール。',
      keywords: 'ダッシュボード,案件管理,請求書管理,タスク管理,インフルエンサー,クリエイター,SaaS,DX,効率化,省力化'
    }
  },
  
  // 3層目: 個別アプリページ（プラグイン専用UI）
  {
    path: '/apps/projects',
    name: 'ProjectApp',
    component: ProjectApp,
    meta: { 
      requiresAuth: true,   // 認証必須
      title: 'InfluBerry - スポンサー案件管理',
      description: 'スポンサー案件の進捗管理・納期管理を効率化。インフルエンサー・クリエイター向け案件管理SaaSツールで省力化・DXを実現。',
      keywords: 'スポンサー案件,案件管理,進捗管理,納期管理,インフルエンサー,クリエイター,SaaS,DX,効率化,省力化,バックヤード'
    }
  },
  {
    path: '/apps/invoices',
    name: 'InvoiceApp',
    component: InvoiceApp,
    meta: { 
      requiresAuth: true,   // 認証必須
      title: 'InfluBerry - 請求書管理',
      description: '請求書自動生成・管理で事務作業を効率化。インフルエンサー・クリエイター向け請求書管理SaaSツールで省力化・DXを推進。',
      keywords: '請求書管理,請求書自動生成,事務作業効率化,インフルエンサー,クリエイター,SaaS,DX,省力化,バックオフィス'
    }
  },
  
  // BerryDo｜タスク管理アプリ
  {
    path: '/berry-do',
    name: 'TodoApp',
    component: TodoApp,
    meta: { 
      requiresAuth: true,
      title: 'BerryDo｜タスク管理 - InfluBerry',
      description: 'タスク管理・todoリストで作業効率を最大化。インフルエンサー・クリエイター向けタスク管理SaaSツールで省力化・DXを実現。',
      keywords: 'タスク管理,todoリスト,作業効率化,インフルエンサー,クリエイター,SaaS,DX,省力化,バックヤード,効率化'
    }
  },
  
  // 法的ページ（認証不要・独立ページ）
  {
    path: '/about',
    name: 'About',
    component: AboutPage,
    meta: { 
      requiresAuth: false,  // 認証不要（法的要件）
      title: 'InfluBerry - アプリ説明',
      description: 'InfluBerryはインフルエンサー・クリエイター向けの案件管理・請求書自動生成SaaSツール。効率化・省力化でDXを推進し、Z世代女子のバックヤード業務をサポート。',
      keywords: 'InfluBerry,アプリ説明,インフルエンサー,クリエイター,SaaS,DX,効率化,省力化,Z世代女子,バックヤード,案件管理,請求書自動生成'
    }
  },
  {
    path: '/privacy',
    name: 'Privacy',
    component: PrivacyPage,
    meta: { 
      requiresAuth: false,  // 認証不要（法的要件）
      title: 'InfluBerry - プライバシーポリシー',
      description: 'InfluBerryのプライバシーポリシー。インフルエンサー・クリエイターの個人情報保護とセキュリティについて。SaaSツールとしての信頼性を確保。',
      keywords: 'プライバシーポリシー,個人情報保護,セキュリティ,インフルエンサー,クリエイター,SaaS,信頼性'
    }
  },
  {
    path: '/terms',
    name: 'Terms',
    component: TermsPage,
    meta: { 
      requiresAuth: false,  // 認証不要（法的要件）
      title: 'InfluBerry - ご利用規約',
      description: 'InfluBerryのご利用規約。インフルエンサー・クリエイター向けSaaSツールの利用条件とサービス内容について。',
      keywords: 'ご利用規約,利用条件,サービス内容,インフルエンサー,クリエイター,SaaS,利用規約'
    }
  },
  {
    path: '/company',
    name: 'Company',
    component: CompanyPage,
    meta: { 
      requiresAuth: false,  // 認証不要（法的要件）
      title: 'InfluBerry - 運営会社情報',
      description: 'InfluBerryの運営会社Air Edison（エアエジソン）の情報。インフルエンサー・クリエイター向けSaaSツールの開発・運営会社。',
      keywords: '運営会社,Air Edison,エアエジソン,会社情報,インフルエンサー,クリエイター,SaaS,開発会社'
    }
  },
  {
    path: '/tokusho',
    name: 'Tokusho',
    component: TokushoPage,
    meta: { 
      requiresAuth: false,  // 認証不要（法的要件）
      title: 'InfluBerry - 特定商取引法に基づく表記',
      description: 'InfluBerryの特定商取引法に基づく表記。インフルエンサー・クリエイター向けSaaSツールの法的情報と取引条件。',
      keywords: '特定商取引法,法的表記,取引条件,インフルエンサー,クリエイター,SaaS,法的情報'
    }
  },
  
  // ブログページ
  {
    path: '/blog',
    name: 'Blog',
    component: BlogPage,
    meta: { 
      requiresAuth: false,  // 認証不要（SEO用）
      title: 'InfluBerry Blog - インフルエンサー・クリエイター向け効率化・省力化ブログ',
      description: 'インフルエンサー・クリエイター向けの効率化・省力化ブログ。SaaSツール活用、DX推進、バックヤード業務最適化のノウハウを発信。Z世代女子クリエイターの成功をサポート。',
      keywords: 'インフルエンサー,クリエイター,効率化,省力化,SaaS,DX,バックヤード,案件管理,請求書自動生成,タスク管理,todoリスト,Z世代女子,ブログ'
    }
  },
  
  // FAQページ
  {
    path: '/faq',
    name: 'FAQ',
    component: FAQPage,
    meta: { 
      requiresAuth: false,  // 認証不要（SEO用）
      title: 'InfluBerry FAQ - よくある質問・効率化・省力化SaaS',
      description: 'InfluBerryのよくある質問と回答。インフルエンサー・クリエイター向け案件管理・請求書自動生成SaaSツールの使い方、料金、セキュリティについて。効率化・省力化でDXを推進。',
      keywords: 'FAQ,よくある質問,インフルエンサー,クリエイター,効率化,省力化,SaaS,DX,案件管理,請求書自動生成,タスク管理,todoリスト,Z世代女子'
    }
  },

  // 将来プラグイン用のルート（予約）
  {
    path: '/apps/calendar',
    name: 'CalendarApp',
    // component: () => import('../views/CalendarApp.vue'), // 遅延読み込み（一時無効化）
    meta: { 
      requiresAuth: true,
      title: 'InfluBerry - 投稿アイデアカレンダー',
      comingSoon: true  // 準備中フラグ
    }
  },
  {
    path: '/apps/proposal',
    name: 'ProposalApp',
    // component: () => import('../views/ProposalApp.vue'), // 遅延読み込み（一時無効化）
    meta: { 
      requiresAuth: true,
      title: 'InfluBerry - ブランド提案文ジェネレーター',
      comingSoon: true  // 準備中フラグ
    }
  },
  {
    path: '/apps/calculator',
    name: 'CalculatorApp',
    // component: () => import('../views/CalculatorApp.vue'), // 遅延読み込み（一時無効化）
    meta: { 
      requiresAuth: true,
      title: 'InfluBerry - 案件単価計算ツール',
      comingSoon: true  // 準備中フラグ
    }
  },
  
  // 404 Not Found
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    redirect: '/'
  }
]

// ルーター作成
const router = createRouter({
  history: createWebHistory(),
  routes,
  // スクロール動作の設定
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// グローバルナビゲーションガード（認証チェック）
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 認証状態を確認（初回アクセス時）
  if (authStore.isLoggedIn === null) {
    await authStore.checkAuthStatus()
  }
  
  // ページタイトル設定
  if (to.meta.title) {
    document.title = to.meta.title
  }
  
  // 認証が必要なページへのアクセス制御
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    console.log('未認証ユーザーのアクセス拒否:', to.path)
    next('/')  // 認証ページへリダイレクト
    return
  }
  
  // 未認証ユーザー専用ページ（認証済みユーザーはダッシュボードへ）
  if (to.meta.requiresGuest && authStore.isLoggedIn) {
    console.log('認証済みユーザーをダッシュボードへリダイレクト')
    next('/dashboard')  // ダッシュボードへリダイレクト
    return
  }
  
  // 準備中のプラグインページアクセス制御
  if (to.meta.comingSoon) {
    console.log('準備中プラグインへのアクセス:', to.path)
    // 開発環境では通す、本番環境ではダッシュボードへリダイレクト
    if (process.env.NODE_ENV === 'production') {
      next('/dashboard')
      return
    }
  }
  
  next()  // 通常の遷移
})

// ナビゲーション後の処理
router.afterEach((to, from) => {
  console.log(`ルート遷移完了: ${from.path} → ${to.path}`)
  
  // Google Analytics (GA4) ページビュー追跡
  if (typeof gtag !== 'undefined') {
    gtag('event', 'page_view', {
      page_title: to.name || document.title,
      page_location: window.location.href,
      page_path: to.path
    })
  }
})

export default router