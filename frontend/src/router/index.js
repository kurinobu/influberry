import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

// ページコンポーネントのインポート
import AuthPage from '../views/AuthPage.vue'
import DashboardPage from '../views/DashboardPage.vue'
import ProjectApp from '../views/ProjectApp.vue'
import InvoiceApp from '../views/InvoiceApp.vue'
// 法的ページコンポーネント
import AboutPage from '../views/legal/AboutPage.vue'
import PrivacyPage from '../views/legal/PrivacyPage.vue'
import TermsPage from '../views/legal/TermsPage.vue'
import CompanyPage from '../views/legal/CompanyPage.vue'
import TokushoPage from '../views/legal/TokushoPage.vue'

// ルート定義（3層分離アーキテクチャ）
const routes = [
  // 1層目: 認証ページ（未認証専用）
  {
    path: '/',
    name: 'Auth',
    component: AuthPage,
    meta: { 
      requiresGuest: true,  // 未認証ユーザーのみアクセス可能
      title: 'InfluBerry - ログイン'
    }
  },
  
  // 2層目: メインダッシュボード（認証後・プラグイン選択）
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardPage,
    meta: { 
      requiresAuth: true,   // 認証必須
      title: 'InfluBerry - ダッシュボード'
    }
  },
  
  // 3層目: 個別アプリページ（プラグイン専用UI）
  {
    path: '/apps/projects',
    name: 'ProjectApp',
    component: ProjectApp,
    meta: { 
      requiresAuth: true,   // 認証必須
      title: 'InfluBerry - スポンサー案件管理'
    }
  },
  {
    path: '/apps/invoices',
    name: 'InvoiceApp',
    component: InvoiceApp,
    meta: { 
      requiresAuth: true,   // 認証必須
      title: 'InfluBerry - 請求書管理'
    }
  },
  
  // 法的ページ（認証不要・独立ページ）
  {
    path: '/about',
    name: 'About',
    component: AboutPage,
    meta: { 
      requiresAuth: false,  // 認証不要（法的要件）
      title: 'InfluBerry - アプリ説明'
    }
  },
  {
    path: '/privacy',
    name: 'Privacy',
    component: PrivacyPage,
    meta: { 
      requiresAuth: false,  // 認証不要（法的要件）
      title: 'InfluBerry - プライバシーポリシー'
    }
  },
  {
    path: '/terms',
    name: 'Terms',
    component: TermsPage,
    meta: { 
      requiresAuth: false,  // 認証不要（法的要件）
      title: 'InfluBerry - ご利用規約'
    }
  },
  {
    path: '/company',
    name: 'Company',
    component: CompanyPage,
    meta: { 
      requiresAuth: false,  // 認証不要（法的要件）
      title: 'InfluBerry - 運営会社情報'
    }
  },
  {
    path: '/tokusho',
    name: 'Tokusho',
    component: TokushoPage,
    meta: { 
      requiresAuth: false,  // 認証不要（法的要件）
      title: 'InfluBerry - 特定商取引法に基づく表記'
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