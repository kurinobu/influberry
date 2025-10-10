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
        :class="isActive('/apps/projects') ? activeClasses : inactiveClasses"
      >
        <BriefcaseIcon 
          :size="24" 
          :color="isActive('/apps/projects') ? '#ffffff' : '#3b82f6'" 
          class="mb-1"
        />
        <span class="text-xs font-medium">Work</span>
      </router-link>

      <!-- Pay (BerryPay - 請求書管理) -->
      <router-link 
        to="/apps/invoices" 
        class="flex flex-col items-center justify-center p-2 rounded-xl transition-all duration-200"
        :class="isActive('/apps/invoices') ? activeClasses : inactiveClasses"
      >
        <InvoiceIcon 
          :size="24" 
          :color="isActive('/apps/invoices') ? '#ffffff' : '#a855f7'" 
          class="mb-1"
        />
        <span class="text-xs font-medium">Pay</span>
      </router-link>

      <!-- Do (BerryDo - Todo管理) -->
      <router-link 
        to="/berry-do" 
        class="flex flex-col items-center justify-center p-2 rounded-xl transition-all duration-200"
        :class="isActive('/berry-do') ? activeClasses : inactiveClasses"
      >
        <ChecklistIcon 
          :size="24" 
          :color="isActive('/berry-do') ? '#ffffff' : '#10b981'" 
          class="mb-1"
        />
        <span class="text-xs font-medium">Do</span>
      </router-link>

      <!-- DB (Dashboard - メインダッシュボード) -->
      <router-link 
        to="/dashboard" 
        class="flex flex-col items-center justify-center p-2 rounded-xl transition-all duration-200"
        :class="isActive('/dashboard') ? activeClasses : inactiveClasses"
      >
        <DashboardIcon 
          :size="24" 
          :color="isActive('/dashboard') ? '#ffffff' : '#ec4899'" 
          class="mb-1"
        />
        <span class="text-xs font-medium">DB</span>
      </router-link>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BriefcaseIcon from './icons/BriefcaseIcon.vue'
import InvoiceIcon from './icons/InvoiceIcon.vue'
import ChecklistIcon from './icons/ChecklistIcon.vue'
import DashboardIcon from './icons/DashboardIcon.vue'

export default {
  name: 'FixedFooter',
  components: {
    BriefcaseIcon,
    InvoiceIcon,
    ChecklistIcon,
    DashboardIcon
  },
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