# Phase 1: ブラウザでのパフォーマンス測定コマンド

## 📋 測定項目

1. API呼び出し回数の測定
2. APIレスポンスタイムの測定
3. ページ読み込み時間の測定
4. 新API動作確認
5. 旧APIとの比較

---

## 🚀 実行手順

### Step 1: ブラウザでダッシュボードページを開く

1. ブラウザで `https://influberry.jp/dashboard` または `http://127.0.0.1:5173/dashboard` を開く
2. ログインしてダッシュボードページを表示

### Step 2: 開発者ツールを開く

- Chrome/Edge: `F12` または `Ctrl+Shift+I` (Mac: `Cmd+Option+I`)
- Network タブを開く
- Console タブを開く

### Step 3: コンソールで以下を実行

---

## 📊 測定コマンド（コンソールに貼り付け実行）

```javascript
// ============================================================================
// Phase 1: 現状調査・パフォーマンス測定
// ============================================================================

// 1. API呼び出し回数の測定
async function measureAPICalls() {
  console.log('\n📊 API呼び出し回数測定');
  console.log('='.repeat(80));
  
  // Network タブの記録をクリア
  console.log('🔧 Network タブを開いて記録をクリアしてください');
  
  // ページをリロードして測定
  const startTime = performance.now();
  
  // リロード前の処理
  console.log('⏱️ 測定開始: ページをリロードしてください');
  console.log('   → Network タブで /api/monthly-targets と /api/monthly-stats の呼び出し回数を確認');
  
  // リロード後に実行するコマンド（手動で実行）
  return {
    instruction: 'ページリロード後、以下のコマンドを実行してください',
    commands: [
      'analyzeNetworkRequests()',
      'measureAPIResponseTime()',
      'measurePageLoadTime()'
    ]
  };
}

// 2. Network リクエストの分析
function analyzeNetworkRequests() {
  console.log('\n📊 Network リクエスト分析');
  console.log('='.repeat(80));
  
  // Performance APIからリソース取得
  const resources = performance.getEntriesByType('resource');
  const monthlyAPIs = resources.filter(r => 
    r.name.includes('/api/monthly') || 
    r.name.includes('/api/monthly-targets') || 
    r.name.includes('/api/monthly-stats')
  );
  
  console.log(`\n✅ 月次管理関連API呼び出し数: ${monthlyAPIs.length} 回`);
  
  const apiGroups = {
    'monthly-targets': monthlyAPIs.filter(r => r.name.includes('/api/monthly-targets')),
    'monthly-stats': monthlyAPIs.filter(r => r.name.includes('/api/monthly-stats')),
    'monthly-current': monthlyAPIs.filter(r => r.name.includes('/api/monthly/current'))
  };
  
  console.log('\n📋 API別呼び出し数:');
  Object.entries(apiGroups).forEach(([name, calls]) => {
    console.log(`  - ${name}: ${calls.length} 回`);
    if (calls.length > 0) {
      const totalTime = calls.reduce((sum, r) => sum + r.duration, 0);
      const avgTime = totalTime / calls.length;
      console.log(`    合計時間: ${totalTime.toFixed(2)}ms, 平均: ${avgTime.toFixed(2)}ms`);
    }
  });
  
  // 計画書v2.0との比較
  console.log('\n📋 計画書v2.0との比較:');
  const expectedCalls = {
    old: monthlyAPIs.filter(r => r.name.includes('/api/monthly-targets') || 
                                 r.name.includes('/api/monthly-stats')).length,
    new: monthlyAPIs.filter(r => r.name.includes('/api/monthly/current')).length
  };
  
  if (expectedCalls.new > 0) {
    console.log(`  ✅ 新API使用: ${expectedCalls.new} 回`);
    if (expectedCalls.new === 1) {
      console.log('  ✅ 目標達成: API呼び出し回数 = 1回');
    } else {
      console.log(`  ⚠️ 目標未達成: API呼び出し回数 = ${expectedCalls.new}回（目標: 1回）`);
    }
  } else {
    console.log(`  ⚠️ 旧API使用: ${expectedCalls.old} 回`);
    console.log(`  ⚠️ 新API未使用: USE_NEW_API = false の可能性`);
    if (expectedCalls.old > 1) {
      console.log(`  ⚠️ 目標未達成: API呼び出し回数 = ${expectedCalls.old}回（目標: 1回）`);
    }
  }
  
  return {
    totalCalls: monthlyAPIs.length,
    apiGroups: Object.fromEntries(
      Object.entries(apiGroups).map(([name, calls]) => [name, calls.length])
    ),
    expectedCalls
  };
}

// 3. APIレスポンスタイムの測定
function measureAPIResponseTime() {
  console.log('\n⏱️ APIレスポンスタイム測定');
  console.log('='.repeat(80));
  
  const resources = performance.getEntriesByType('resource');
  const monthlyAPIs = resources.filter(r => 
    r.name.includes('/api/monthly') || 
    r.name.includes('/api/monthly-targets') || 
    r.name.includes('/api/monthly-stats')
  );
  
  if (monthlyAPIs.length === 0) {
    console.log('⚠️ 月次管理関連APIの呼び出しが見つかりません');
    console.log('   → ページをリロードしてから再度実行してください');
    return null;
  }
  
  console.log('\n📋 各APIのレスポンスタイム:');
  monthlyAPIs.forEach((r, index) => {
    const duration = r.duration;
    const status = duration < 500 ? '✅' : duration < 1000 ? '⚠️' : '❌';
    console.log(`  ${status} ${r.name.split('/').pop()}: ${duration.toFixed(2)}ms`);
  });
  
  const totalTime = monthlyAPIs.reduce((sum, r) => sum + r.duration, 0);
  const avgTime = totalTime / monthlyAPIs.length;
  const maxTime = Math.max(...monthlyAPIs.map(r => r.duration));
  
  console.log(`\n📊 統計:`);
  console.log(`  - 合計時間: ${totalTime.toFixed(2)}ms`);
  console.log(`  - 平均時間: ${avgTime.toFixed(2)}ms`);
  console.log(`  - 最大時間: ${maxTime.toFixed(2)}ms`);
  
  // 計画書v2.0との比較
  console.log('\n📋 計画書v2.0との比較:');
  if (maxTime < 500) {
    console.log('  ✅ 目標達成: 最大レスポンスタイム < 500ms');
  } else if (maxTime < 1000) {
    console.log('  ⚠️ 目標未達成: 最大レスポンスタイム < 1秒（目標: < 500ms）');
  } else {
    console.log('  ❌ 目標未達成: 最大レスポンスタイム >= 1秒');
  }
  
  return {
    totalTime,
    avgTime,
    maxTime,
    apis: monthlyAPIs.map(r => ({
      name: r.name,
      duration: r.duration
    }))
  };
}

// 4. ページ読み込み時間の測定
function measurePageLoadTime() {
  console.log('\n⏱️ ページ読み込み時間測定');
  console.log('='.repeat(80));
  
  const navigation = performance.getEntriesByType('navigation')[0];
  
  if (!navigation) {
    console.log('⚠️ ナビゲーション情報が見つかりません');
    console.log('   → ページをリロードしてから再度実行してください');
    return null;
  }
  
  const metrics = {
    'DOMContentLoaded': navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
    'Load完了': navigation.loadEventEnd - navigation.loadEventStart,
    'DNS解決': navigation.domainLookupEnd - navigation.domainLookupStart,
    'TCP接続': navigation.connectEnd - navigation.connectStart,
    'リクエスト': navigation.responseStart - navigation.requestStart,
    'レスポンス': navigation.responseEnd - navigation.responseStart,
    'DOM処理': navigation.domComplete - navigation.domInteractive,
    '総時間': navigation.loadEventEnd - navigation.fetchStart
  };
  
  console.log('\n📋 ページ読み込みメトリクス:');
  Object.entries(metrics).forEach(([name, value]) => {
    const status = value < 1000 ? '✅' : value < 2000 ? '⚠️' : '❌';
    console.log(`  ${status} ${name}: ${value.toFixed(2)}ms`);
  });
  
  // 計画書v2.0との比較
  const totalTime = metrics['総時間'];
  console.log('\n📋 計画書v2.0との比較:');
  if (totalTime < 1000) {
    console.log('  ✅ 目標達成: ページ読み込み時間 < 1秒');
  } else if (totalTime < 2000) {
    console.log('  ⚠️ 目標未達成: ページ読み込み時間 < 2秒（目標: < 1秒）');
  } else {
    console.log('  ❌ 目標未達成: ページ読み込み時間 >= 2秒');
  }
  
  return metrics;
}

// 5. 新API動作確認
async function testNewAPI() {
  console.log('\n🔌 新API動作確認');
  console.log('='.repeat(80));
  
  try {
    const token = localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token');
    
    if (!token) {
      console.log('⚠️ 認証トークンが見つかりません');
      console.log('   → ログインしてから再度実行してください');
      return null;
    }
    
    console.log('🔧 新API呼び出し: GET /api/monthly/current');
    const startTime = performance.now();
    
    const response = await fetch('/api/monthly/current', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    });
    
    const endTime = performance.now();
    const duration = endTime - startTime;
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ 新API呼び出し成功');
      console.log(`⏱️ レスポンスタイム: ${duration.toFixed(2)}ms`);
      console.log(`📊 レスポンスデータ:`, data);
      
      // 計画書v2.0との比較
      console.log('\n📋 計画書v2.0との比較:');
      if (duration < 500) {
        console.log('  ✅ 目標達成: レスポンスタイム < 500ms');
      } else {
        console.log(`  ⚠️ 目標未達成: レスポンスタイム = ${duration.toFixed(2)}ms（目標: < 500ms）`);
      }
      
      // レスポンス形式の確認
      if (data.success && data.data && data.current_month) {
        console.log('  ✅ レスポンス形式: 計画書v2.0準拠');
      } else {
        console.log('  ⚠️ レスポンス形式: 計画書v2.0と異なる可能性');
      }
      
      return { success: true, duration, data };
    } else {
      console.log(`❌ 新API呼び出し失敗: ${response.status} ${response.statusText}`);
      const error = await response.json().catch(() => ({ error: 'Unknown error' }));
      console.log('📋 エラー詳細:', error);
      return { success: false, status: response.status, error };
    }
  } catch (error) {
    console.log('❌ 新API呼び出しエラー:', error);
    return { success: false, error: error.message };
  }
}

// 6. 旧APIとの比較
async function compareOldAndNewAPI() {
  console.log('\n📊 旧APIと新APIの比較');
  console.log('='.repeat(80));
  
  const token = localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token');
  
  if (!token) {
    console.log('⚠️ 認証トークンが見つかりません');
    return null;
  }
  
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth() + 1;
  
  // 旧API呼び出し
  console.log('\n📊 旧API呼び出し:');
  const oldStart = performance.now();
  
  const [targetsRes, statsRes] = await Promise.all([
    fetch(`/api/monthly-targets/?year=${year}&months=${month}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    }),
    fetch(`/api/monthly-stats/${year}/${month}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })
  ]);
  
  const oldEnd = performance.now();
  const oldDuration = oldEnd - oldStart;
  
  console.log(`⏱️ 旧API合計時間: ${oldDuration.toFixed(2)}ms (2回のAPI呼び出し)`);
  
  // 新API呼び出し
  console.log('\n📊 新API呼び出し:');
  const newStart = performance.now();
  
  const newRes = await fetch('/api/monthly/current', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    credentials: 'include'
  });
  
  const newEnd = performance.now();
  const newDuration = newEnd - newStart;
  
  console.log(`⏱️ 新API合計時間: ${newDuration.toFixed(2)}ms (1回のAPI呼び出し)`);
  
  // 比較
  console.log('\n📋 比較結果:');
  const improvement = ((oldDuration - newDuration) / oldDuration * 100).toFixed(1);
  console.log(`  - 旧API: ${oldDuration.toFixed(2)}ms (2回の呼び出し)`);
  console.log(`  - 新API: ${newDuration.toFixed(2)}ms (1回の呼び出し)`);
  console.log(`  - 改善率: ${improvement}%`);
  
  if (newDuration < oldDuration) {
    console.log('  ✅ 新APIの方が高速');
  } else {
    console.log('  ⚠️ 新APIの方が遅い（キャッシュやネットワーク状態の影響の可能性）');
  }
  
  return {
    oldDuration,
    newDuration,
    improvement: parseFloat(improvement)
  };
}

// 7. 総合レポート生成
function generateReport() {
  console.log('\n📊 Phase 1 総合レポート');
  console.log('='.repeat(80));
  
  const networkAnalysis = analyzeNetworkRequests();
  const apiTiming = measureAPIResponseTime();
  const pageTiming = measurePageLoadTime();
  
  console.log('\n📋 総合評価:');
  
  // API呼び出し回数
  const apiCalls = networkAnalysis?.totalCalls || 0;
  if (apiCalls === 1) {
    console.log('  ✅ API呼び出し回数: 1回（目標達成）');
  } else {
    console.log(`  ⚠️ API呼び出し回数: ${apiCalls}回（目標: 1回）`);
  }
  
  // APIレスポンスタイム
  const maxApiTime = apiTiming?.maxTime || 0;
  if (maxApiTime < 500) {
    console.log('  ✅ APIレスポンスタイム: < 500ms（目標達成）');
  } else {
    console.log(`  ⚠️ APIレスポンスタイム: ${maxApiTime.toFixed(2)}ms（目標: < 500ms）`);
  }
  
  // ページ読み込み時間
  const totalLoadTime = pageTiming?.['総時間'] || 0;
  if (totalLoadTime < 1000) {
    console.log('  ✅ ページ読み込み時間: < 1秒（目標達成）');
  } else {
    console.log(`  ⚠️ ページ読み込み時間: ${totalLoadTime.toFixed(2)}ms（目標: < 1秒）`);
  }
  
  // 計画書v2.0との差異
  console.log('\n📋 計画書v2.0との差異:');
  const differences = [];
  
  if (apiCalls !== 1) {
    differences.push(`API呼び出し回数: ${apiCalls}回（目標: 1回）`);
  }
  if (maxApiTime >= 500) {
    differences.push(`APIレスポンスタイム: ${maxApiTime.toFixed(2)}ms（目標: < 500ms）`);
  }
  if (totalLoadTime >= 1000) {
    differences.push(`ページ読み込み時間: ${totalLoadTime.toFixed(2)}ms（目標: < 1秒）`);
  }
  
  if (differences.length === 0) {
    console.log('  ✅ 差異なし（目標達成）');
  } else {
    differences.forEach(diff => console.log(`  ⚠️ ${diff}`));
  }
  
  return {
    apiCalls,
    maxApiTime,
    totalLoadTime,
    differences
  };
}

// ============================================================================
// 一括実行用コマンド
// ============================================================================

// Phase 1 測定を一括実行
async function runPhase1Measurement() {
  console.log('\n🚀 Phase 1: 現状調査・パフォーマンス測定');
  console.log('='.repeat(80));
  console.log('実行日時:', new Date().toISOString());
  
  // 1. Network リクエスト分析
  console.log('\n📊 Step 1: Network リクエスト分析');
  const networkAnalysis = analyzeNetworkRequests();
  
  // 2. APIレスポンスタイム測定
  console.log('\n⏱️ Step 2: APIレスポンスタイム測定');
  const apiTiming = measureAPIResponseTime();
  
  // 3. ページ読み込み時間測定
  console.log('\n⏱️ Step 3: ページ読み込み時間測定');
  const pageTiming = measurePageLoadTime();
  
  // 4. 新API動作確認
  console.log('\n🔌 Step 4: 新API動作確認');
  const newAPITest = await testNewAPI();
  
  // 5. 旧APIと新APIの比較（オプション）
  console.log('\n📊 Step 5: 旧APIと新APIの比較');
  const comparison = await compareOldAndNewAPI();
  
  // 6. 総合レポート
  console.log('\n📊 Step 6: 総合レポート生成');
  const report = generateReport();
  
  console.log('\n✅ Phase 1 測定完了');
  console.log('='.repeat(80));
  
  return {
    networkAnalysis,
    apiTiming,
    pageTiming,
    newAPITest,
    comparison,
    report
  };
}

// ============================================================================
// グローバルに公開
// ============================================================================

// 個別関数
window.measureAPICalls = measureAPICalls;
window.analyzeNetworkRequests = analyzeNetworkRequests;
window.measureAPIResponseTime = measureAPIResponseTime;
window.measurePageLoadTime = measurePageLoadTime;
window.testNewAPI = testNewAPI;
window.compareOldAndNewAPI = compareOldAndNewAPI;
window.generateReport = generateReport;

// 一括実行
window.runPhase1Measurement = runPhase1Measurement;

console.log('\n✅ Phase 1 測定コマンドを読み込みました');
console.log('📋 利用可能なコマンド:');
console.log('  - runPhase1Measurement() : 一括実行');
console.log('  - analyzeNetworkRequests() : Network リクエスト分析');
console.log('  - measureAPIResponseTime() : APIレスポンスタイム測定');
console.log('  - measurePageLoadTime() : ページ読み込み時間測定');
console.log('  - testNewAPI() : 新API動作確認');
console.log('  - compareOldAndNewAPI() : 旧APIと新APIの比較');
console.log('  - generateReport() : 総合レポート生成');
```

---

## 📝 実行方法

### 方法1: 一括実行（推奨）

1. ブラウザのコンソールに上記のJavaScriptコード全体を貼り付けて実行
2. `runPhase1Measurement()` を実行

### 方法2: 個別実行

各関数を個別に実行:

```javascript
// Network リクエスト分析
analyzeNetworkRequests()

// APIレスポンスタイム測定
measureAPIResponseTime()

// ページ読み込み時間測定
measurePageLoadTime()

// 新API動作確認
testNewAPI()

// 旧APIと新APIの比較
compareOldAndNewAPI()

// 総合レポート生成
generateReport()
```

---

## 📊 結果の共有方法

測定結果を以下の形式で共有してください:

```json
{
  "apiCalls": 2,
  "maxApiTime": 1234.56,
  "totalLoadTime": 2345.67,
  "newAPITest": {
    "success": true,
    "duration": 456.78
  },
  "differences": [
    "API呼び出し回数: 2回（目標: 1回）",
    "ページ読み込み時間: 2345.67ms（目標: < 1秒）"
  ]
}
```


