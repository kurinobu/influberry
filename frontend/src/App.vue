<script setup>
// 3層分離アーキテクチャ実装完了
// App.vue は純粋なルーターアウトレットとして機能
// 各ページコンポーネントが責務を持つ
</script>

<template>
  <!-- ルーターアウトレット（ページコンポーネント表示） -->
  <router-view />
</template>

<style>
/* InfluBerry カスタムカラーパレット（CSS変数定義） */
:root {
  /* スポンサー案件管理 - ピンク系 */
  --influberry-pink: #FF6B9D;
  --influberry-pink-light: #FFB5C1;
  --influberry-pink-dark: #E91E63;
  
  /* 請求書管理 - ラベンダー系 */
  --influberry-lavender: #B794F6;
  --influberry-lavender-light: #E0C3FC;
  --influberry-lavender-dark: #9F7AEA;
  
  /* 投稿アイデアカレンダー - ミント系（将来用） */
  --influberry-mint: #81E6D9;
  --influberry-mint-light: #B2F5EA;
  --influberry-mint-dark: #4FD1C7;
  
  /* 単価計算ツール - ベージュ系（将来用） */
  --influberry-beige: #F7E6A3;
  --influberry-beige-light: #FFF3C4;
  --influberry-beige-dark: #EDD94C;
  
  /* その他設定用 - グリーン系 */
  --influberry-green: #68D391;
  --influberry-green-light: #9AE6B4;
  --influberry-green-dark: #48BB78;
}

/* グローバルフォント設定 */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700&display=swap');

.font-poppins {
  font-family: 'Poppins', sans-serif;
}

.font-noto {
  font-family: 'Noto Sans JP', sans-serif;
}

/* ベース設定 */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Noto Sans JP', sans-serif;
  background-color: #f9fafb;
}

/* スムーズなページ遷移 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* スクロールバーカスタマイズ */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: var(--influberry-pink-light);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--influberry-pink);
}
</style>