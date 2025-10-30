<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth.js'
import { useMonthlyStore } from '../stores/monthly.js'
import { useUIStore } from '../stores/ui.js'

// 認証ストア
const authStore = useAuthStore()
const monthlyStore = useMonthlyStore()
const uiStore = useUIStore()

// フォーム状態
const profileForm = ref({
  username: '',
  influencer_name: '',
  profile: '',
  issuer_name: '',
  office_address: '',
  contact_info: ''
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
const paymentForm = ref({
  payment_method: '',
  bank_name: '',
  branch_name: '',
  account_type: '',
  account_number: '',
  account_holder: ''
})

// 支払い情報UI状態
const isPaymentLoading = ref(false)
const paymentMessage = ref('')
const paymentError = ref('')

// 月次目標設定フォーム状態
const targetForm = ref({
  projects: 0,
  income: 0
})

// 月次目標設定UI状態
const isTargetLoading = ref(false)
const targetMessage = ref('')
const targetError = ref('')

onMounted(async () => {
  if (authStore.user) {
    profileForm.value.username = authStore.user.username || ''
    profileForm.value.influencer_name = authStore.user.influencer_name || ''
    profileForm.value.profile = authStore.user.profile || ''
    profileForm.value.issuer_name = authStore.user.issuer_name || ''
    profileForm.value.office_address = authStore.user.office_address || ''
    profileForm.value.contact_info = authStore.user.contact_info || ''
  }
  
  // 支払い情報取得
  await fetchPaymentInfo()
  
  // 月次目標データ取得（現在月のみ）
  const now = new Date()
  const currentYear = now.getFullYear()
  const currentMonth = now.getMonth() + 1
  await monthlyStore.fetchTargets(currentYear, [currentMonth])
  loadCurrentMonthTarget()
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

  if (!profileForm.value.issuer_name.trim()) {
    profileError.value = '請求者名は必須です'
    return
  }

  isProfileLoading.value = true
  
  try {
    const result = await authStore.updateUserProfile({
      username: profileForm.value.username.trim(),
      influencer_name: profileForm.value.influencer_name.trim(),
      profile: profileForm.value.profile.trim(),
      issuer_name: profileForm.value.issuer_name.trim(),
      office_address: profileForm.value.office_address.trim(),
      contact_info: profileForm.value.contact_info.trim()
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

// 支払い情報取得処理
const fetchPaymentInfo = async () => {
  try {
    const result = await authStore.getPaymentInfo()
    
    if (result.success && result.data) {
      paymentForm.value = {
        payment_method: result.data.payment_method || '銀行振込',
        bank_name: result.data.bank_name || '',
        branch_name: result.data.branch_name || '',
        account_type: result.data.account_type || '普通',
        account_number: result.data.account_number || '',
        account_holder: result.data.account_holder || ''
      }
    }
  } catch (error) {
    console.error('支払い情報取得エラー:', error)
  }
}

// 支払い情報更新処理
const handlePaymentUpdate = async () => {
  if (isPaymentLoading.value) return
  
  paymentError.value = ''
  paymentMessage.value = ''
  
  isPaymentLoading.value = true
  
  try {
    const result = await authStore.updatePaymentInfo(paymentForm.value)
    
    if (result.success) {
      paymentMessage.value = result.message || '支払い情報を更新しました'
      setTimeout(() => {
        paymentMessage.value = ''
      }, 3000)
    } else {
      paymentError.value = result.error || '支払い情報更新に失敗しました'
    }
  } catch (error) {
    paymentError.value = '支払い情報更新中にエラーが発生しました'
  } finally {
    isPaymentLoading.value = false
  }
}

// 現在月のラベルを取得
const getCurrentMonthLabel = () => {
  const now = new Date()
  const currentYear = now.getFullYear()
  const currentMonth = now.getMonth() + 1
  return `${currentYear}年${currentMonth}月`
}

// 月次目標読み込み処理（現在月のみ）
const loadCurrentMonthTarget = async () => {
  const now = new Date()
  const currentYear = now.getFullYear()
  const currentMonth = now.getMonth() + 1
  const currentMonthStr = `${currentYear}-${currentMonth.toString().padStart(2, '0')}-01`
  
  const target = monthlyStore.getTargetByMonth(currentMonthStr)
  if (target) {
    targetForm.value.projects = target.target_projects || 0
    targetForm.value.income = target.target_income || 0
  } else {
    targetForm.value.projects = 0
    targetForm.value.income = 0
  }
}

// 月次目標保存処理（現在月のみ）
const handleTargetSave = async () => {
  if (isTargetLoading.value) return
  
  targetError.value = ''
  targetMessage.value = ''
  
  isTargetLoading.value = true
  
  try {
    const now = new Date()
    const currentYear = now.getFullYear()
    const currentMonth = now.getMonth() + 1
    const currentMonthStr = `${currentYear}-${currentMonth.toString().padStart(2, '0')}-01`
    
    const result = await monthlyStore.saveTarget(currentMonthStr, {
      target_projects: targetForm.value.projects,
      target_income: targetForm.value.income
    })
    
    if (result.success) {
      targetMessage.value = `${getCurrentMonthLabel()}の目標を保存しました！`
      setTimeout(() => {
        targetMessage.value = ''
      }, 3000)
    } else {
      targetError.value = result.error || '目標保存に失敗しました'
    }
  } catch (error) {
    targetError.value = '目標保存中にエラーが発生しました'
  } finally {
    isTargetLoading.value = false
  }
}

</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50 flex items-center justify-center p-4">
    <div class="w-full max-w-2xl space-y-6">
      <!-- ヘッダー -->
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-900 font-poppins mb-2 flex items-center">
          <svg class="w-8 h-8 text-pink-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          ユーザー設定
        </h1>
        <p class="text-gray-600 font-noto">
          プロフィール情報とパスワードの変更ができます
        </p>
      </div>


      <!-- プロフィール編集セクション -->
      <div class="bg-white rounded-2xl shadow-xl p-8 border border-pink-100">
        <h2 class="text-xl font-semibold text-gray-900 font-poppins mb-6 flex items-center">
          <svg class="w-6 h-6 text-pink-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          プロフィール編集
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
          
          <!-- 請求者名 -->
          <div>
            <label for="issuer_name" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              請求者名 *
            </label>
            <input
              id="issuer_name"
              v-model="profileForm.issuer_name"
              type="text"
              required
              :disabled="isProfileLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-pink-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors"
              placeholder="請求者名を入力（必須）"
            >
          </div>

          <!-- オフィス所在地 -->
          <div>
            <label for="office_address" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              オフィス所在地
            </label>
            <input
              id="office_address"
              v-model="profileForm.office_address"
              type="text"
              :disabled="isProfileLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-pink-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors"
              placeholder="オフィス所在地を入力（任意）"
            >
          </div>

          <!-- 連絡先 -->
          <div>
            <label for="contact_info" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              連絡先
            </label>
            <input
              id="contact_info"
              v-model="profileForm.contact_info"
              type="text"
              :disabled="isProfileLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-pink-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors"
              placeholder="電話番号またはメールアドレスを入力（任意）"
            >
          </div>

          <!-- 月次目標設定（簡素化版） -->
          <div class="border-t border-gray-200 pt-6 mt-6">
      <h3 class="text-lg font-semibold text-gray-900 font-poppins mb-4 flex items-center">
        <svg class="w-5 h-5 text-pink-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        今月の目標設定
      </h3>
            
            <!-- 現在月の表示 -->
            <div class="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <p class="text-blue-800 font-noto text-sm flex items-center">
                <svg class="w-4 h-4 text-blue-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {{ getCurrentMonthLabel() }}の目標を設定します
              </p>
            </div>
            
            <!-- 目標案件数 -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 font-noto mb-2 flex items-center">
                <svg class="w-4 h-4 text-blue-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                目標案件数
              </label>
              <div class="relative">
                <input 
                  v-model.number="targetForm.projects"
                  type="number"
                  min="0"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-pink-500 font-noto transition-colors"
                  placeholder="例: 5"
                />
                <span class="absolute right-4 top-3 text-gray-500 font-noto">件</span>
              </div>
            </div>
            
            <!-- 目標報酬額 -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 font-noto mb-2 flex items-center">
                <svg class="w-4 h-4 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
                目標報酬額
              </label>
              <div class="relative">
                <input 
                  v-model.number="targetForm.income"
                  type="number"
                  min="0"
                  step="10000"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-pink-500 font-noto transition-colors"
                  placeholder="例: 200000"
                />
                <span class="absolute right-4 top-3 text-gray-500 font-noto">円</span>
              </div>
            </div>
            
            <!-- 月次目標保存メッセージ -->
            <div v-if="targetMessage" class="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
              <p class="text-green-800 font-noto">{{ targetMessage }}</p>
            </div>

            <div v-if="targetError" class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p class="text-red-800 font-noto">{{ targetError }}</p>
            </div>
            
            <!-- 目標保存ボタン（簡素化版） -->
            <button
              type="button"
              @click="handleTargetSave"
              :disabled="isTargetLoading"
              class="w-full flex justify-center items-center px-6 py-3 font-semibold rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed font-poppins bg-gradient-to-r from-pink-500 to-purple-600 text-white hover:from-pink-600 hover:to-purple-700"
              style="box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3)"
            >
              <svg v-if="isTargetLoading" class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              {{ isTargetLoading ? '保存中...' : '今月の目標を保存' }}
            </button>
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
            <svg v-if="isProfileLoading" class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ isProfileLoading ? '更新中...' : 'プロフィールを更新' }}
          </button>
        </form>
      </div>

      <!-- パスワード変更セクション -->
      <div class="bg-white rounded-2xl shadow-xl p-8 border border-purple-100">
        <h2 class="text-xl font-semibold text-gray-900 font-poppins mb-6 flex items-center">
          <svg class="w-6 h-6 text-purple-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          パスワード変更
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
            <svg v-if="isPasswordLoading" class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ isPasswordLoading ? '変更中...' : 'パスワードを変更' }}
          </button>
        </form>
      </div>
      <!-- 支払い情報セクション -->
      <div class="bg-white rounded-2xl shadow-xl p-8 border border-blue-100">
        <h2 class="text-xl font-semibold text-gray-900 font-poppins mb-6 flex items-center">
          <svg class="w-6 h-6 text-blue-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
          </svg>
          支払い情報
        </h2>
        
        <form @submit.prevent="handlePaymentUpdate" class="space-y-6">
          <!-- 支払い方法 -->
          <div>
            <label for="payment_method" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              支払い方法
            </label>
            <select
              id="payment_method"
              v-model="paymentForm.payment_method"
              :disabled="isPaymentLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors"
            >
              <option value="">選択してください</option>
              <option value="銀行振込">銀行振込</option>
              <option value="PayPay">PayPay</option>
              <option value="その他">その他</option>
            </select>
          </div>

          <!-- 銀行名 -->
          <div>
            <label for="bank_name" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              銀行名
            </label>
            <input
              id="bank_name"
              v-model="paymentForm.bank_name"
              type="text"
              :disabled="isPaymentLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors"
              placeholder="銀行名を入力"
            >
          </div>

          <!-- 支店名 -->
          <div>
            <label for="branch_name" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              支店名
            </label>
            <input
              id="branch_name"
              v-model="paymentForm.branch_name"
              type="text"
              :disabled="isPaymentLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors"
              placeholder="支店名を入力"
            >
          </div>

          <!-- 口座種別 -->
          <div>
            <label for="account_type" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              口座種別
            </label>
            <select
              id="account_type"
              v-model="paymentForm.account_type"
              :disabled="isPaymentLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors"
            >
              <option value="">選択してください</option>
              <option value="普通">普通</option>
              <option value="当座">当座</option>
            </select>
          </div>

          <!-- 口座番号 -->
          <div>
            <label for="account_number" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              口座番号
            </label>
            <input
              id="account_number"
              v-model="paymentForm.account_number"
              type="text"
              :disabled="isPaymentLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors"
              placeholder="口座番号を入力"
            >
          </div>

          <!-- 口座名義 -->
          <div>
            <label for="account_holder" class="block text-sm font-medium text-gray-700 font-noto mb-2">
              口座名義
            </label>
            <input
              id="account_holder"
              v-model="paymentForm.account_holder"
              type="text"
              :disabled="isPaymentLoading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:text-gray-500 font-noto transition-colors"
              placeholder="カタカナで入力してください"
            >
          </div>

          <!-- 支払い情報更新メッセージ -->
          <div v-if="paymentMessage" class="p-4 bg-green-50 border border-green-200 rounded-lg">
            <p class="text-green-800 font-noto">{{ paymentMessage }}</p>
          </div>

          <div v-if="paymentError" class="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-red-800 font-noto">{{ paymentError }}</p>
          </div>

          <!-- 支払い情報更新ボタン -->
          <button
            type="submit"
            :disabled="isPaymentLoading"
            class="w-full flex justify-center items-center px-6 py-3 font-semibold rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed font-poppins bg-gradient-to-r from-blue-500 to-indigo-600 text-white hover:from-blue-600 hover:to-indigo-700"
            style="box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3)"
          >
            <svg v-if="isPaymentLoading" class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ isPaymentLoading ? '更新中...' : '支払い情報を更新' }}
          </button>
        </form>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* フォント統合 - @import文最優先 */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;500;700&display=swap');

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
  font-family: 'M PLUS Rounded 1c', sans-serif !important;
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