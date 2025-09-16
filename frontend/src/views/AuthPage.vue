<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import LoginForm from '../components/LoginForm.vue'
import RegisterForm from '../components/RegisterForm.vue'

const router = useRouter()
const authStore = useAuthStore()

// 認証フォーム切り替え状態（login or register）
const authMode = ref('login')

// 認証済みの場合はダッシュボードへリダイレクト
onMounted(async () => {
  await authStore.checkAuthStatus()
  if (authStore.isLoggedIn) {
    router.push('/dashboard')
  }
})

// 認証フォーム切り替え
const switchToLogin = () => {
  authMode.value = 'login'
}

const switchToRegister = () => {
  authMode.value = 'register'
}

// 認証成功時のリダイレクト処理
const handleAuthSuccess = () => {
  router.push('/dashboard')
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50 flex items-center justify-center">
    <div class="max-w-md w-full space-y-4 p-4">
      <!-- InfluBerry ロゴ・ブランディング -->
      <div class="text-center">
        <h1 class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-600 font-poppins mt-0 mb-0 leading-none">
          🍓 InfluBerry
        </h1>
        <p class="mt-2 text-gray-600 font-noto">
          Z世代インフルエンサー向け案件管理システム
        </p>
      </div>

      <!-- 認証フォーム表示 -->
      <div class="bg-white rounded-xl shadow-lg p-6">
        <LoginForm 
          v-if="authMode === 'login'" 
          @switch-to-register="switchToRegister"
          @auth-success="handleAuthSuccess"
        />
        <RegisterForm 
          v-if="authMode === 'register'" 
          @switch-to-login="switchToLogin"
          @auth-success="handleAuthSuccess"
        />
      </div>

      <!-- フッター -->
      <div class="text-center text-sm text-gray-500">
        <p>&copy; 2025 InfluBerry. All rights reserved.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* InfluBerry カスタムスタイル */
.bg-gradient-to-br {
  background: linear-gradient(135deg, 
    var(--influberry-pink-light, #fdf2f8), 
    var(--influberry-lavender-light, #f3e8ff)
  );
}

/* モバイルファースト最適化 */
@media (max-width: 640px) {
  .max-w-md {
    margin: 1rem;
    max-width: calc(100% - 2rem);
  }
  
  .p-8 {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .text-4xl {
    font-size: 2rem;
    line-height: 2.5rem;
  }
  
  .p-6 {
    padding: 1rem;
  }
}
</style>