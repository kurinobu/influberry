/**
 * Google Analytics 4 トラッキングユーティリティ
 * 全コンポーネントで使用する統一的なイベント送信関数
 */

/**
 * GA4が利用可能かチェック
 */
export const isGtagAvailable = () => {
  return typeof window !== 'undefined' && typeof window.gtag !== 'undefined'
}

/**
 * カスタムイベントを送信
 * @param {string} eventName - イベント名
 * @param {object} params - イベントパラメータ
 */
export const trackEvent = (eventName, params = {}) => {
  if (!isGtagAvailable()) {
    console.warn('Google Analytics not available')
    return
  }
  
  window.gtag('event', eventName, params)
  console.log(`[GA4] Event tracked: ${eventName}`, params)
}

/**
 * ビジネス指標トラッキング
 */
export const trackProjectCreate = (method = 'manual') => {
  trackEvent('project_create', {
    method,
    page_path: window.location.pathname
  })
}

export const trackInvoiceCreate = (fromProject = false, amount = null) => {
  trackEvent('invoice_create', {
    from_project: fromProject,
    amount: amount ? parseFloat(amount) : null,
    page_path: window.location.pathname
  })
}

export const trackPdfDownload = (documentType = 'invoice') => {
  trackEvent('pdf_download', {
    document_type: documentType,
    page_path: window.location.pathname
  })
}

/**
 * UX改善トラッキング
 */
export const trackModalOpen = (modalName) => {
  trackEvent('modal_open', {
    modal_name: modalName,
    page_path: window.location.pathname
  })
}

export const trackModalClose = (modalName) => {
  trackEvent('modal_close', {
    modal_name: modalName,
    page_path: window.location.pathname
  })
}

export const trackSettingsUpdate = (settingType) => {
  trackEvent('settings_update', {
    setting_type: settingType,
    page_path: window.location.pathname
  })
}

export const trackError = (errorType, errorMessage = '', component = '') => {
  trackEvent('error_occurred', {
    error_type: errorType,
    error_message: errorMessage,
    component,
    page_path: window.location.pathname
  })
}

/**
 * 詳細分析トラッキング
 */
export const trackSearch = (searchTerm, resultCount = null) => {
  trackEvent('search', {
    search_term: searchTerm,
    result_count: resultCount,
    page_path: window.location.pathname
  })
}

export const trackFilter = (filterType, filterValue) => {
  trackEvent('filter_used', {
    filter_type: filterType,
    filter_value: filterValue,
    page_path: window.location.pathname
  })
}

export const trackTaskComplete = (taskType, duration = null) => {
  trackEvent('task_complete', {
    task_type: taskType,
    duration: duration ? Math.round(duration / 1000) : null, // 秒単位
    page_path: window.location.pathname
  })
}

export const trackFormStart = (formType) => {
  trackEvent('form_start', {
    form_type: formType,
    page_path: window.location.pathname
  })
}

export const trackFormAbandon = (formType, fieldsFilled = 0) => {
  trackEvent('form_abandon', {
    form_type: formType,
    fields_filled: fieldsFilled,
    page_path: window.location.pathname
  })
}