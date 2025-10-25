<template>
  <div class="min-h-fit flex items-start justify-center bg-gradient-to-br from-pink-50 to-purple-50 px-4 pt-8 pb-4">
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
            <label for="email" class="berry-label">
              メールアドレス
            </label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              required
              class="berry-input"
              placeholder="your@email.com"
              :disabled="authStore.isLoading"
            />
          </div>

          <!-- パスワード入力 -->
          <div>
            <label for="password" class="berry-label">
              パスワード
            </label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              required
              class="berry-input"
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
              class="berry-checkbox"
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
            class="group relative w-full flex justify-center py-2 px-4 border-2 border-white text-sm font-medium rounded-md text-white bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
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

/* === Phase 4 berry化CSS（TodoApp.vue成功パターン移植） === */
.berry-label {
  display: block;
  font-size: 1rem;
  font-weight: 700;
  color: #4b5563;  /* text-gray-600に統一（RegisterFormと統一） */
  margin-bottom: 0.5rem;
  text-shadow: none;
}

.berry-input {
  width: 100%;
  padding: 1rem 1.25rem;
  border-radius: 0.75rem;
  border: 2px solid #f9a8d4;
  background: #ffffff;
  font-size: 1rem;
  font-weight: 500;
  color: #111827;
  line-height: 1.5;
  transition: all 0.2s ease;
  margin-top: 0.25rem;
}

.berry-input:focus {
  outline: none;
  border-color: #ec4899;
  box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.1);
  background: #ffffff;
}

.berry-input::placeholder {
  color: #9ca3af;
  font-weight: 400;
}

.berry-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* === チェックボックス専用CSS（RegisterFormと統一） === */
input[type="checkbox"].berry-checkbox {
  width: 1.5rem !important;             /* 24px - 入力フィールドと統一感 */
  height: 1.5rem !important;            /* 24px */
  min-width: 1.5rem !important;         /* 最小幅を強制 */
  min-height: 1.5rem !important;         /* 最小高さを強制 */
  max-width: 1.5rem !important;         /* 最大幅を強制 */
  max-height: 1.5rem !important;        /* 最大高さを強制 */
  border: 2px solid #f9a8d4 !important;
  border-radius: 0.5rem !important;     /* 8px - 入力フィールドと統一 */
  background: #ffffff !important;
  accent-color: #ec4899 !important;     /* チェック時の色 */
  cursor: pointer !important;
  transition: all 0.2s ease !important;
  margin-top: 0.25rem !important;
  appearance: none !important;           /* ブラウザデフォルトスタイルを無効化 */
  -webkit-appearance: none !important;   /* WebKitブラウザのデフォルトスタイルを無効化 */
  -moz-appearance: none !important;      /* Firefoxのデフォルトスタイルを無効化 */
  box-sizing: border-box !important;    /* ボックスモデルを統一 */
  flex-shrink: 0 !important;            /* フレックスアイテムの縮小を防止 */
}

/* スマホ対応：タッチしやすいサイズ */
@media (max-width: 640px) {
  input[type="checkbox"].berry-checkbox {
    width: 1.75rem !important;          /* 28px - スマホでタッチしやすい */
    height: 1.75rem !important;         /* 28px */
    min-width: 1.75rem !important;      /* 最小幅を強制 */
    min-height: 1.75rem !important;     /* 最小高さを強制 */
    max-width: 1.75rem !important;      /* 最大幅を強制 */
    max-height: 1.75rem !important;     /* 最大高さを強制 */
  }
}

input[type="checkbox"].berry-checkbox:focus {
  outline: none !important;
  border-color: #ec4899 !important;
  box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.1) !important;
}

input[type="checkbox"].berry-checkbox:checked {
  background-color: #ec4899 !important;
  border-color: #ec4899 !important;
  background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='m13.854 3.646-7.5 7.5a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6 10.293l7.146-7.147a.5.5 0 0 1 .708.708z'/%3e%3c/svg%3e") !important;
  background-size: 100% 100% !important;
  background-position: center !important;
  background-repeat: no-repeat !important;
}

input[type="checkbox"].berry-checkbox:disabled {
  opacity: 0.6 !important;
  cursor: not-allowed !important;
}
</style>