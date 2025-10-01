<template>
  <div 
    v-if="showFooter"
    class="fixed bottom-0 left-0 right-0 bg-gradient-to-r from-pink-50 via-white to-purple-50 backdrop-blur-sm border-t border-gray-200 shadow-lg z-40"
  >
    <div class="flex justify-around items-center h-16 px-4 max-w-md mx-auto">
      <!-- Work (BerryWork - 案件管理) -->
      <router-link 
        to="/apps/projects"
        class="flex flex-col items-center justify-center p-2 rounded-xl transition-all duration-200"
        :class="isActive('/projects') ? activeClasses : inactiveClasses"
      >
        <svg class="w-6 h-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V8a2 2 0 012-2V6z"></path>
        </svg>
        <span class="text-xs font-medium">Work</span>
      </router-link>

      <!-- Pay (BerryPay - 請求書管理) -->
      <router-link 
        to="/apps/invoices" 
        class="flex flex-col items-center justify-center p-2 rounded-xl transition-all duration-200"
        :class="isActive('/invoices') ? activeClasses : inactiveClasses"
      >
        <svg class="w-6 h-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"></path>
        </svg>
        <span class="text-xs font-medium">Pay</span>
      </router-link>

      <!-- Do (BerryDo - Todo管理) -->
      <router-link 
        to="/berry-do" 
        class="flex flex-col items-center justify-center p-2 rounded-xl transition-all duration-200"
        :class="isActive('/berry-do') ? activeClasses : inactiveClasses"
      >
        <svg class="w-6 h-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
        </svg>
        <span class="text-xs font-medium">Do</span>
      </router-link>

      <!-- DB (Dashboard - メインダッシュボード) -->
      <router-link 
        to="/dashboard" 
        class="flex flex-col items-center justify-center p-2 rounded-xl transition-all duration-200"
        :class="isActive('/dashboard') ? activeClasses : inactiveClasses"
      >
        <svg class="w-6 h-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path>
        </svg>
        <span class="text-xs font-medium">DB</span>
      </router-link>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'FixedFooter',
  setup() {
    const route = useRoute()
    const authStore = useAuthStore()
    
    // 認証済みかつ認証ページ以外で表示
    const showFooter = computed(() => {
      return authStore.isAuthenticated && route.path !== '/'
    })
    
    // 現在のページがアクティブかどうか判定
    const isActive = (path) => {
      return route.path === path
    }
    
    // アクティブ状態のスタイル（Z世代向けグラデーション）
    const activeClasses = 'bg-gradient-to-br from-pink-400 to-purple-500 text-white shadow-md transform scale-105'
    
    // 非アクティブ状態のスタイル
    const inactiveClasses = 'text-gray-600 hover:text-pink-500 hover:bg-pink-50'
    
    return {
      showFooter,
      isActive,
      activeClasses,
      inactiveClasses
    }
  }
}
</script>

<style scoped>
/* タップ時のフィードバック効果 */
.router-link-active {
  transform: translateY(-1px);
}

/* スムーズな遷移アニメーション */
.transition-all {
  transition: all 0.2s ease-in-out;
}

/* ホバー時の軽微な浮き上がり効果 */
a:hover {
  transform: translateY(-1px);
}

/* アクティブ状態でのより強い効果 */
.scale-105 {
  transform: scale(1.05) translateY(-1px);
}
</style>