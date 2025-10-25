// frontend/src/stores/ui.js
import { ref } from 'vue'
import { defineStore } from 'pinia'

/**
 * UIストア - メニューシステム中央集権化
 * 目的: 5コンポーネント連携・6ステップ処理を2ステップに簡素化
 * 効果: 重複コード削除・保守性向上・将来拡張容易性
 */
export const useUIStore = defineStore('ui', () => {
  // ===== 状態管理 =====
  
  // 設定モーダル表示状態
  const showSettings = ref(false)
  
  // 基本データモーダル表示状態  
  const showBasicData = ref(false)

  // ===== アクション（旧6ステップ処理を2ステップに簡素化） =====
  
  /**
   * 設定モーダル開閉切り替え
   * 旧フロー: HamburgerMenu → emit → 親コンポーネント → toggle関数 → 状態変更 → プロパティ受渡し → モーダル表示
   * 新フロー: HamburgerMenu → Store直接操作 → モーダル自動表示
   */
  const toggleSettings = () => {
    showSettings.value = !showSettings.value
  }
  
  /**
   * 設定モーダル表示
   */
  const openSettings = () => {
    showSettings.value = true
  }
  
  /**
   * 設定モーダル非表示
   */
  const closeSettings = () => {
    showSettings.value = false
  }
  
  /**
   * 基本データモーダル開閉切り替え
   * 旧フロー: HamburgerMenu → emit → 親コンポーネント → toggle関数 → 状態変更 → プロパティ受渡し → モーダル表示
   * 新フロー: HamburgerMenu → Store直接操作 → モーダル自動表示
   */
  const toggleBasicData = () => {
    showBasicData.value = !showBasicData.value
  }
  
  /**
   * 基本データモーダル表示
   */
  const openBasicData = () => {
    showBasicData.value = true
  }
  
  /**
   * 基本データモーダル非表示
   */
  const closeBasicData = () => {
    showBasicData.value = false
  }

  // ===== 全モーダル一括制御 =====
  
  /**
   * すべてのモーダルを閉じる
   * 用途: ページ遷移時・緊急時の状態リセット
   */
  const closeAllModals = () => {
    showSettings.value = false
    showBasicData.value = false
  }

  // ===== 返り値（公開API） =====
  return {
    // 状態（読み取り専用として使用推奨）
    showSettings,
    showBasicData,
    
    // 設定モーダル制御
    toggleSettings,
    openSettings,
    closeSettings,
    
    // 基本データモーダル制御
    toggleBasicData,
    openBasicData,
    closeBasicData,
    
    // 全体制御
    closeAllModals
  }
})