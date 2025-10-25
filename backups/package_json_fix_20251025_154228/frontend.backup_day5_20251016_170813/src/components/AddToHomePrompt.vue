<script setup>
import { ref, onMounted } from 'vue'
import IconX from './icons/IconX.vue'
import IconSmartphone from './icons/IconSmartphone.vue'

// Props
const props = defineProps({
  pageName: {
    type: String,
    required: true // 'auth' or 'dashboard'
  }
})

// State
const isVisible = ref(false)
const isIOS = ref(false)
const isAndroid = ref(false)

// LocalStorage Key
const STORAGE_KEY = 'influberry_add_to_home_prompt_count'

// モバイルデバイス判定（iOS・Android両対応）
const checkMobileDevice = () => {
  const userAgent = window.navigator.userAgent.toLowerCase()
  const isIOSDevice = /iphone|ipad|ipod/.test(userAgent) && !window.navigator.standalone
  const isAndroidDevice = /android/.test(userAgent)
  return isIOSDevice || isAndroidDevice
}

// 表示回数チェック
const checkDisplayCount = () => {
  const count = parseInt(localStorage.getItem(STORAGE_KEY) || '0', 10)
  return count < 2
}

// 表示回数インクリメント
const incrementDisplayCount = () => {
  const count = parseInt(localStorage.getItem(STORAGE_KEY) || '0', 10)
  localStorage.setItem(STORAGE_KEY, String(count + 1))
}

// モーダル閉じる
const closePrompt = () => {
  isVisible.value = false
  incrementDisplayCount()
}

// 初期化
onMounted(() => {
  const userAgent = window.navigator.userAgent.toLowerCase()
  isIOS.value = /iphone|ipad|ipod/.test(userAgent) && !window.navigator.standalone
  isAndroid.value = /android/.test(userAgent)
  
  // iOS または Android で表示
  if ((isIOS.value || isAndroid.value) && checkDisplayCount()) {
    setTimeout(() => {
      isVisible.value = true
    }, 500)
  }
})
</script>

<template>
  <!-- モーダルオーバーレイ -->
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="isVisible"
        class="fixed inset-0 z-[9999] flex items-center justify-center p-4"
        style="background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(4px);"
        @click.self="closePrompt"
      >
        <!-- モーダルコンテンツ -->
        <div
          class="relative w-full max-w-sm rounded-3xl shadow-2xl overflow-hidden"
          style="background: linear-gradient(135deg, #FF6B9D 0%, #B794F6 100%);"
        >
          <!-- 閉じるボタン -->
          <button
            @click="closePrompt"
            class="absolute top-4 right-4 p-2 rounded-full bg-white/20 hover:bg-white/30 transition-all duration-200 z-10"
            aria-label="閉じる"
          >
            <IconX class="w-5 h-5 text-white" />
          </button>

          <!-- コンテンツエリア -->
          <div class="p-8 text-center">
            <!-- アイコン -->
            <div class="mb-6 flex justify-center">
              <div class="p-4 rounded-full bg-white/20 backdrop-blur-sm">
                <IconSmartphone class="w-12 h-12 text-white" />
              </div>
            </div>

            <!-- タイトル -->
            <h3 class="text-2xl font-bold text-white mb-3 font-poppins">
              ホーム画面に追加
            </h3>

            <!-- メッセージ -->
            <p class="text-white/90 text-lg mb-6 font-noto leading-relaxed">
              ワンタップでInfluBerryに<br>アクセス！
            </p>

            <!-- iOS手順 -->
            <div class="bg-white/10 backdrop-blur-sm rounded-2xl p-6 text-left">
              <p class="text-white/80 text-sm mb-4 font-noto">
                📱 <strong>追加方法</strong>
              </p>
              <!-- iOS手順 -->
              <ol v-if="isIOS" class="text-white/70 text-sm space-y-2 font-noto">
                <li>1. 画面下部の <strong>共有ボタン</strong>（□に↑）をタップ</li>
                <li>2. <strong>「ホーム画面に追加」</strong> を選択</li>
                <li>3. <strong>「追加」</strong> をタップして完了！</li>
              </ol>

              <!-- Android手順 -->
              <ol v-else-if="isAndroid" class="text-white/70 text-sm space-y-2 font-noto">
                <li>1. 画面右上の <strong>メニュー</strong>（⋮）をタップ</li>
                <li>2. <strong>「ホーム画面に追加」</strong> を選択</li>
                <li>3. <strong>「追加」</strong> をタップして完了！</li>
              </ol>
            </div>

            <!-- 後でボタン -->
            <button
              @click="closePrompt"
              class="mt-6 w-full py-3 rounded-full bg-white text-pink-500 font-bold text-lg hover:bg-pink-50 transition-all duration-200 font-poppins shadow-lg"
            >
              OK
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
/* フェードアニメーション */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ホバーエフェクト強化 */
button:hover {
  transform: translateY(-1px);
}

button:active {
  transform: translateY(0);
}
</style>