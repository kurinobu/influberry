<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-50 to-purple-50 px-4">
    <div class="max-w-md w-full space-y-8">
      <!-- InfluBerry ロゴ・タイトル -->
      <div class="text-center">
        <h2 class="mt-6 text-3xl font-bold text-gray-900">
          🍓 InfluBerry
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          新規アカウント登録
        </p>
      </div>

      <!-- 新規登録フォーム -->
      <form @submit.prevent="handleRegister" class="mt-8 space-y-6">
        <!-- エラーメッセージ -->
        <div v-if="authStore.error" class="bg-red-50 border border-red-200 rounded-md p-3">
          <div class="text-sm text-red-600">
            {{ authStore.error }}
          </div>
        </div>

        <div class="space-y-4">
          <!-- ユーザー名入力 -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              ユーザー名
            </label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-pink-500 focus:border-pink-500 focus:z-10 sm:text-sm"
              placeholder="ユーザー名（英数字）"
              :disabled="authStore.isLoading"
            />
          </div>

          <!-- メールアドレス入力 -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              メールアドレス
            </label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-pink-500 focus:border-pink-500 focus:z-10 sm:text-sm"
              placeholder="your@email.com"
              :disabled="authStore.isLoading"
            />
          </div>

          <!-- パスワード入力 -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              パスワード
            </label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-pink-500 focus:border-pink-500 focus:z-10 sm:text-sm"
              placeholder="パスワード（8文字以上）"
              :disabled="authStore.isLoading"
            />
          </div>

          
        </div>

        <!-- 新規登録ボタン -->
        <div>
          <button
            type="submit"
            :disabled="authStore.isLoading || !isFormValid"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            <span v-if="authStore.isLoading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <!-- ローディングスピナー -->
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ authStore.isLoading ? '登録中...' : '新規登録' }}
          </button>
        </div>

        <!-- ログインページへのリンク -->
        <div class="text-center">
          <p class="text-sm text-gray-600">
            既にアカウントをお持ちですか？
            <button
              type="button"
              @click="$emit('switch-to-login')"
              class="font-medium text-pink-600 hover:text-pink-500"
              :disabled="authStore.isLoading"
            >
              ログイン
            </button>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'
import { useAuthStore } from '../stores/auth.js'

// イベント定義
const emit = defineEmits(['switch-to-login'])

// 認証ストア
const authStore = useAuthStore()

// フォームデータ
const formData = reactive({
  username: '',
  email: '',
  password: ''
})

// フォームバリデーション
const isFormValid = computed(() => {
  return formData.username.trim() !== '' && 
         formData.email.trim() !== '' && 
         formData.password.trim() !== ''
})

// 新規登録処理
const handleRegister = async () => {
  // エラーメッセージクリア
  authStore.clearError()
  
  try {
    const result = await authStore.register(
      formData.username.trim(),
      formData.email.trim(),
      formData.password
    )
    
    if (result.success) {
      // 新規登録成功時の処理
      console.log('新規登録成功:', result.message)
      // ページリロードまたはルート変更
      window.location.reload()
    }
    // エラーは authStore.error に自動設定される
    
  } catch (error) {
    console.error('新規登録処理エラー:', error)
  }
}
</script>

<style scoped>
/* カスタムスタイル */
.bg-gradient-to-br {
  background-image: linear-gradient(to bottom right, var(--tw-gradient-stops));
}

.bg-gradient-to-r {
  background-image: linear-gradient(to right, var(--tw-gradient-stops));
}

/* フォーカス時のアニメーション */
input:focus {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

/* ボタンホバーエフェクト */
button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* ローディング時のアニメーション */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* ボタンカラー強制適用（LoginForm統一） */
.bg-gradient-to-r {
  background-image: linear-gradient(to right, var(--tw-gradient-stops)) !important;
}

/* グラデーション変数強制設定 */
.from-pink-500 {
  --tw-gradient-from: var(--color-pink-500) !important;
  --tw-gradient-stops: var(--tw-gradient-from) var(--tw-gradient-from-position), var(--tw-gradient-to) var(--tw-gradient-to-position) !important;
}

.to-purple-500 {
  --tw-gradient-to: var(--color-purple-500) !important;
}
</style>