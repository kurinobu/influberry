import './assets/main.css'

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from './App.vue'
import { setupAxiosInterceptors } from './stores/auth.js'

// Vue Router設定（新しいルーター使用）
import router from './router/index.js'

// Pinia状態管理
const pinia = createPinia()

// アプリケーション初期化
const app = createApp(App)
app.use(router)
app.use(pinia)

// Axios認証インターセプター設定
setupAxiosInterceptors()

app.mount('#app')