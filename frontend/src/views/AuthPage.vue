<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import LoginForm from '../components/LoginForm.vue'
import RegisterForm from '../components/RegisterForm.vue'
import AddToHomePrompt from '@/components/AddToHomePrompt.vue'

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
  authStore.error = null // タブ切り替え時にエラークリア
}

const switchToRegister = () => {
  authMode.value = 'register'
  authStore.error = null // タブ切り替え時にエラークリア
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
        <div class="flex items-center justify-center">
          <img src="/favicon512.png" alt="InfluBerry" class="w-8 h-8 mr-3">
          <h1 class="text-2xl font-bold bg-gradient-to-r from-pink-500 to-purple-600 bg-clip-text text-transparent">
            InfluBerry
          </h1>
        </div>
        <p class="mt-2 text-gray-600 font-noto">
          インフルエンサー向け案件管理システム
        </p>
      </div>

      <!-- 認証フォーム表示 -->
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

      <!-- フッター -->
      <div class="text-center text-sm text-gray-500">
        <p>&copy; 2025 InfluBerry. All rights reserved.</p>
      </div>
    </div>
  </div>
  <!-- ホーム画面追加促進モーダル -->
  <AddToHomePrompt page-name="auth" />
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

/* ヘッダータイトル強制カラフル表示 */
h1.text-2xl.font-bold {
  background: linear-gradient(to right, #ec4899, #8b5cf6) !important;
  -webkit-background-clip: text !important;
  background-clip: text !important;
  color: transparent !important;
  font-weight: 700 !important;
}
</style>