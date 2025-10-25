<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth.js'

// 認証ストア
const authStore = useAuthStore()

// フォーム状態
const profileForm = ref({
  username: '',
  influencer_name: '',
  profile: ''
})

const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

// UI状態
const isProfileLoading = ref(false)
const isPasswordLoading = ref(false)
const profileMessage = ref('')
const passwordMessage = ref('')
const profileError = ref('')
const passwordError = ref('')

// 初期化時にユーザー情報を設定
onMounted(() => {
  if (authStore.user) {
    profileForm.value.username = authStore.user.username || ''
    profileForm.value.influencer_name = authStore.user.influencer_name || ''
    profileForm.value.profile = authStore.user.profile || ''
  }
})

// プロフィール更新処理
const handleProfileUpdate = async () => {
  if (isProfileLoading.value) return
  
  profileError.value = ''
  profileMessage.value = ''
  
  // バリデーション
  if (!profileForm.value.username.trim()) {
    profileError.value = 'ユーザー名は必須です'
    return
  }
  
  if (!profileForm.value.influencer_name.trim()) {
    profileError.value = 'インフルエンサー名は必須です'
    return
  }
  
  isProfileLoading.value = true
  
  try {
    const result = await authStore.updateUserProfile({
      username: profileForm.value.username.trim(),
      influencer_name: profileForm.value.influencer_name.trim(),
      profile: profileForm.value.profile.trim()
    })
    
    if (result.success) {
      profileMessage.value = result.message || 'プロフィールを更新しました'
      // 成功時は3秒後にメッセージクリア
      setTimeout(() => {
        profileMessage.value = ''
      }, 3000)
    } else {
      profileError.value = result.error || 'プロフィール更新に失敗しました'
    }
  } catch (error) {
    profileError.value = 'プロフィール更新中にエラーが発生しました'
  } finally {
    isProfileLoading.value = false
  }
}

// パスワード変更処理
const handlePasswordChange = async () => {
  if (isPasswordLoading.value) return
  
  passwordError.value = ''
  passwordMessage.value = ''
  
  // バリデーション
  if (!passwordForm.value.current_password) {
    passwordError.value = '現在のパスワードを入力してください'
    return
  }
  
  if (!passwordForm.value.new_password) {
    passwordError.value = '新しいパスワードを入力してください'
    return
  }
  
  if (passwordForm.value.new_password.length < 6) {
    passwordError.value = 'パスワードは6文字以上で入力してください'
    return
  }
  
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    passwordError.value = 'パスワードが一致しません'
    return
  }
  
  isPasswordLoading.value = true
  
  try {
    const result = await authStore.changePassword({
      current_password: passwordForm.value.current_password,
      new_password: passwordForm.value.new_password
    })
    
    if (result.success) {
      passwordMessage.value = result.message || 'パスワードを変更しました'
      // 成功時はフォームクリア
      passwordForm.value = {
        current_password: '',
        new_password: '',
        confirm_password: ''
      }
      // 3秒後にメッセージクリア
      setTimeout(() => {
        passwordMessage.value = ''
      }, 3000)
    } else {
      passwordError.value = result.error || 'パスワード変更に失敗しました'
    }
  } catch (error) {
    passwordError.value = 'パスワード変更中にエラーが発生しました'
  } finally {
    isPasswordLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50 flex items-center justify-center p-4">
    <div class="w-full max-w-2xl space-y-6">
      <!-- ヘッダー -->
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-900 font-poppins mb-2">
          ⚙️ ユーザー設定
        </h1>
        <p class="text-gray-600 font-noto">
          プロフィール情報とパスワードの変更ができます
        </p>
      </div>

      <!-- プロフィール編集セクション -->
      <div class="bg-white rounded-2xl shadow-xl p-8 border border-pink-100">
        <h2 class="text-xl font-semibold text-gray-900 font-poppins mb-6 flex items-center">
          👤 プロフィール編集
        </h2>
        
        <form @submit.prevent="handleProfileUpdate" class="space-y-6">
          <!-- ユーザー名 -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              ユーザー名 *
            </label>
            <input
              id="username"
              v-model="profileForm.username"
              type="text"
              required
              :disabled="isProfileLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-pink-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors"
              placeholder="ユーザー名を入力"
            >
          </div>

          <!-- インフルエンサー名 -->
          <div>
            <label for="influencer_name" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              インフルエンサー名 *
            </label>
            <input
              id="influencer_name"
              v-model="profileForm.influencer_name"
              type="text"
              required
              :disabled="isProfileLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-pink-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors"
              placeholder="インフルエンサー名を入力"
            >
          </div>

          <!-- プロフィール（自己紹介） -->
          <div>
            <label for="profile" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              プロフィール（自己紹介）
            </label>
            <textarea
              id="profile"
              v-model="profileForm.profile"
              rows="4"
              :disabled="isProfileLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-pink-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors resize-none"
              placeholder="自己紹介やプロフィールを入力（任意）"
            ></textarea>
          </div>

          <!-- プロフィール更新メッセージ -->
          <div v-if="profileMessage" class="p-4 bg-green-50 border border-green-200 rounded-lg">
            <p class="text-green-800 font-noto">{{ profileMessage }}</p>
          </div>

          <div v-if="profileError" class="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-red-800 font-noto">{{ profileError }}</p>
          </div>

          <!-- プロフィール更新ボタン -->
          <button
            type="submit"
            :disabled="isProfileLoading"
            class="w-full flex justify-center items-center px-6 py-3 font-semibold rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed font-poppins bg-gradient-to-r from-pink-500 to-purple-600 text-white hover:from-pink-600 hover:to-purple-700"
            style="box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3)"
          >
            <span v-if="isProfileLoading" class="mr-2">🔄</span>
            {{ isProfileLoading ? '更新中...' : 'プロフィールを更新' }}
          </button>
        </form>
      </div>

      <!-- パスワード変更セクション -->
      <div class="bg-white rounded-2xl shadow-xl p-8 border border-purple-100">
        <h2 class="text-xl font-semibold text-gray-900 font-poppins mb-6 flex items-center">
          🔐 パスワード変更
        </h2>
        
        <form @submit.prevent="handlePasswordChange" class="space-y-6">
          <!-- 現在のパスワード -->
          <div>
            <label for="current_password" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              現在のパスワード *
            </label>
            <input
              id="current_password"
              v-model="passwordForm.current_password"
              type="password"
              required
              :disabled="isPasswordLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors"
              placeholder="現在のパスワードを入力"
            >
          </div>

          <!-- 新しいパスワード -->
          <div>
            <label for="new_password" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              新しいパスワード *
            </label>
            <input
              id="new_password"
              v-model="passwordForm.new_password"
              type="password"
              required
              :disabled="isPasswordLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors"
              placeholder="新しいパスワードを入力（6文字以上）"
            >
          </div>

          <!-- パスワード確認 -->
          <div>
            <label for="confirm_password" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              パスワード確認 *
            </label>
            <input
              id="confirm_password"
              v-model="passwordForm.confirm_password"
              type="password"
              required
              :disabled="isPasswordLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors"
              placeholder="新しいパスワードを再度入力"
            >
          </div>

          <!-- パスワード変更メッセージ -->
          <div v-if="passwordMessage" class="p-4 bg-green-50 border border-green-200 rounded-lg">
            <p class="text-green-800 font-noto">{{ passwordMessage }}</p>
          </div>

          <div v-if="passwordError" class="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-red-800 font-noto">{{ passwordError }}</p>
          </div>

          <!-- パスワード変更ボタン -->
          <button
            type="submit"
            :disabled="isPasswordLoading"
            class="w-full flex justify-center items-center px-6 py-3 font-semibold rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed font-poppins bg-gradient-to-r from-pink-500 to-purple-600 text-white hover:from-pink-600 hover:to-purple-700"
            style="box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3)"
          >
            <span v-if="isPasswordLoading" class="mr-2">🔄</span>
            {{ isPasswordLoading ? '変更中...' : 'パスワードを変更' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* フォント統合 - @import文最優先 */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');

/* InfluBerry カラーパレット統合 */
:root {
  --influberry-pink: #FF6B9D;
  --influberry-pink-light: #FFB5C1;
  --influberry-pink-dark: #E91E63;
  --influberry-lavender: #B794F6;
  --influberry-lavender-light: #E0C3FC;
  --influberry-lavender-dark: #9F7AEA;
}

.font-poppins {
  font-family: 'Poppins', sans-serif;
}

.font-noto {
  font-family: 'Noto Sans JP', sans-serif;
}

/* スムーズなトランジション */
.transition-colors {
  transition: color 0.3s ease, background-color 0.3s ease, border-color 0.3s ease;
}

/* モバイルファースト最適化 */
@media (max-width: 640px) {
  .min-h-screen {
    padding: 1rem;
  }
  
  .rounded-2xl {
    border-radius: 1rem;
  }
  
  .p-8 {
    padding: 1.5rem;
  }
  
  .space-y-6 > * + * {
    margin-top: 1rem;
  }
}

@media (max-width: 480px) {
  .text-3xl {
    font-size: 1.75rem;
  }
  
  .text-xl {
    font-size: 1.125rem;
  }
  
  .p-8 {
    padding: 1rem;
  }
}
</style>