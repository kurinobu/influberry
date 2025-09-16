<template>
  <div class="min-h-screen flex items-start justify-center bg-gradient-to-br from-pink-50 to-purple-50 px-4 pt-8">
    <div class="max-w-md w-full space-y-8">
      <!-- InfluBerry ロゴ・タイトル -->
      

      <!-- ログインフォーム -->
      <form @submit.prevent="handleLogin" class="mt-4 space-y-6">
        <!-- エラーメッセージ -->
        <div v-if="authStore.error" class="bg-red-50 border border-red-200 rounded-md p-3">
          <div class="text-sm text-red-600">
            {{ authStore.error }}
          </div>
        </div>

        <div class="space-y-4">
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
              placeholder="パスワード"
              :disabled="authStore.isLoading"
            />
          </div>

          <!-- ログイン状態保持 -->
          <div class="flex items-center">
            <input
              id="remember"
              v-model="formData.remember"
              type="checkbox"
              class="h-4 w-4 text-pink-600 focus:ring-pink-500 border-gray-300 rounded"
              :disabled="authStore.isLoading"
            />
            <label for="remember" class="ml-2 block text-sm text-gray-700">
              ログイン状態を保持する
            </label>
          </div>
        </div>

        <!-- ログインボタン -->
        <div>
          <button
            type="submit"
            :disabled="authStore.isLoading || !isFormValid"
            class="group relative w-full flex justify-center py-2 px-4 border-2 border-white text-sm font-medium rounded-md text-white bg-gradient-to-r from-pink-600 to-purple-700 hover:from-pink-700 hover:to-purple-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            <span v-if="authStore.isLoading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <!-- ローディングスピナー -->
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ authStore.isLoading ? 'ログイン中...' : 'ログイン' }}
          </button>
        </div>

        <!-- テスト用ユーザー情報 - 本番環境では非表示 -->
        <!--
        <div class="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
          <h3 class="text-sm font-medium text-blue-800 mb-2">テスト用アカウント</h3>
          <div class="text-xs text-blue-600 space-y-1">
            <p>メール: test@example.com</p>
            <p>パスワード: password123</p>
          </div>
          <button
            type="button"
            @click="fillTestAccount"
            class="mt-2 text-xs text-blue-600 hover:text-blue-800 underline"
            :disabled="authStore.isLoading"
          >
            テストアカウントを入力
          </button>
        </div>
        -->
        <!-- 新規登録ページへのリンク -->
        <div class="text-center">
          <p class="text-sm text-gray-600">
            アカウントをお持ちではありませんか？
            <button
              type="button"
              @click="$emit('switch-to-register')"
              class="font-medium text-pink-600 hover:text-pink-500"
              :disabled="authStore.isLoading"
            >
              新規登録
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
const emit = defineEmits(['switch-to-register'])

// 認証ストア
const authStore = useAuthStore()

// フォームデータ
const formData = reactive({
  email: '',
  password: '',
  remember: false
})

// フォームバリデーション
const isFormValid = computed(() => {
  return formData.email.trim() !== '' && formData.password.trim() !== ''
})

// ログイン処理
const handleLogin = async () => {
  // エラーメッセージクリア
  authStore.clearError()
  
  try {
    const result = await authStore.login(
      formData.email.trim(),
      formData.password,
      formData.remember
    )
    
    if (result.success) {
      // ログイン成功時の処理
      console.log('ログイン成功:', result.message)
      // ページリロードまたはルート変更
      // この実装では単純にページリロードで認証状態を反映
      window.location.reload()
    }
    // エラーは authStore.error に自動設定される
    
  } catch (error) {
    console.error('ログイン処理エラー:', error)
  }
}

// テストアカウント入力
const fillTestAccount = () => {
  formData.email = 'test@example.com'
  formData.password = 'password123'
  formData.remember = true
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
</style>