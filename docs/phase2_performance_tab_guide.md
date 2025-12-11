# Phase 2 パフォーマンスタブの確認方法ガイド

## 📋 目次
1. [現在表示されている指標の説明](#1-現在表示されている指標の説明)
2. [ページ全体の読み込み時間の確認方法](#2-ページ全体の読み込み時間の確認方法)
3. [APIレスポンスタイムの確認方法](#3-apiレスポンスタイムの確認方法)
4. [計画書v2.0の目標との比較](#4-計画書v20の目標との比較)

---

## 1. 現在表示されている指標の説明

### 1.1 現在表示されている指標

パフォーマンスタブに表示されている指標は、**Core Web Vitals**というWebパフォーマンス指標です：

| 指標 | 値 | 評価 | 説明 |
|------|-----|------|------|
| **LCP** (Largest Contentful Paint) | 2.03秒 | ✅ Good | 最大コンテンツの表示時間 |
| **CLS** (Cumulative Layout Shift) | 0.03 | ✅ Good | レイアウトのずれ（視覚的安定性） |
| **INP** (Interaction to Next Paint) | 96ms | ✅ Good | インタラクションの応答時間 |

### 1.2 各指標の評価

#### ✅ LCP（Largest Contentful Paint）: 2.03秒
- **評価**: Good（< 2.5秒）
- **説明**: 最大のコンテンツが表示されるまでの時間
- **目標**: < 2.5秒（Good）、2.5秒-4.0秒（要改善）、> 4.0秒（悪い）

#### ✅ CLS（Cumulative Layout Shift）: 0.03
- **評価**: Good（< 0.1）
- **説明**: ページのレイアウトがどれだけずれるか（視覚的安定性）
- **目標**: < 0.1（Good）、0.1-0.25（要改善）、> 0.25（悪い）

#### ✅ INP（Interaction to Next Paint）: 96ms
- **評価**: Good（< 200ms）
- **説明**: ユーザーのインタラクション（クリック、タップなど）に対する応答時間
- **目標**: < 200ms（Good）、200ms-500ms（要改善）、> 500ms（悪い）

---

## 2. ページ全体の読み込み時間の確認方法

### 2.1 パフォーマンスタブでの確認方法

#### Step 1: Performanceタブを開く
- Chrome開発者ツールの「Performance」タブを選択

#### Step 2: 記録を開始
- 左上の「Record」ボタン（赤い丸）をクリック
- または、`Cmd+E`（Mac）/ `Ctrl+E`（Windows）

#### Step 3: ページをリロード
- `Cmd+R`（Mac）/ `Ctrl+R`（Windows）でページをリロード

#### Step 4: 記録を停止
- 「Stop」ボタンをクリック
- または、`Cmd+E`（Mac）/ `Ctrl+E`（Windows）を再度押す

#### Step 5: Navigation Timingを確認
記録結果の画面で、以下の手順で確認：

1. **下部のタイムラインを確認**
   - タイムラインの左側に「Navigation」という項目があります
   - これをクリックすると、詳細なタイミング情報が表示されます

2. **Navigation Timingの確認**
   - **DOMContentLoaded**: DOM構築完了までの時間
   - **Load**: ページ全体の読み込み完了までの時間（計画書v2.0の目標との比較に使用）
   - **Total Time**: 総時間

3. **表示方法**
   - タイムライン上の「Navigation」をクリック
   - または、左側の「Summary」タブで「Navigation」を選択

### 2.2 Networkタブでの確認方法

#### Step 1: Networkタブを開く
- Chrome開発者ツールの「Network」タブを選択

#### Step 2: ページをリロード
- `Cmd+R`（Mac）/ `Ctrl+R`（Windows）でページをリロード

#### Step 3: 結果を確認
- **Summary**: ページ全体の統計情報
  - **Finish Time**: 最後のリクエスト完了までの時間（ページ全体の読み込み時間）
  - **Total Time**: すべてのリクエストの総時間

### 2.3 Console APIでの確認方法

ブラウザのコンソールで実行するコード：

```javascript
// ページ読み込み時間を計測
window.addEventListener('load', () => {
  const navigation = performance.getEntriesByType('navigation')[0];
  const timing = {
    'DOMContentLoaded': `${((navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart) / 1000).toFixed(2)}秒`,
    'Load完了': `${((navigation.loadEventEnd - navigation.loadEventStart) / 1000).toFixed(2)}秒`,
    '総時間': `${((navigation.loadEventEnd - navigation.fetchStart) / 1000).toFixed(2)}秒`
  };
  console.table(timing);
});
```

---

## 3. APIレスポンスタイムの確認方法

### 3.1 Networkタブでの確認方法

#### Step 1: Networkタブを開く
- Chrome開発者ツールの「Network」タブを選択

#### Step 2: ページをリロード
- `Cmd+R`（Mac）/ `Ctrl+R`（Windows）でページをリロード

#### Step 3: API呼び出しを確認
- フィルターで「XHR」または「Fetch」を選択
- `/api/monthly/current`のリクエストを探す

#### Step 4: タイミングを確認
- `/api/monthly/current`のリクエストをクリック
- **Timing**タブを選択
  - **Waiting (TTFB)**: サーバー応答時間（Time To First Byte）
  - **Content Download**: コンテンツダウンロード時間
  - **Total Time**: 総時間（計画書v2.0の目標 < 500ms）

### 3.2 Performanceタブでの確認方法

#### Step 1: Performanceタブで記録
- 記録を開始 → ページをリロード → 記録を停止

#### Step 2: Network Timingを確認
- タイムライン上の「Network」セクションを確認
- `/api/monthly/current`のリクエストを探す
- リクエストの時間を確認

### 3.3 Console APIでの確認方法

ブラウザのコンソールで実行するコード：

```javascript
// API呼び出し時間を計測
const apiTimings = [];
const originalFetch = window.fetch;

window.fetch = function(...args) {
  const url = args[0];
  const startTime = performance.now();
  
  return originalFetch.apply(this, args).then(response => {
    const endTime = performance.now();
    const duration = endTime - startTime;
    
    apiTimings.push({ 
      url: url,
      duration: `${duration.toFixed(2)}ms`,
      status: response.status
    });
    
    console.log(`API呼び出し: ${url}, 時間: ${duration.toFixed(2)}ms`);
    
    return response;
  });
};

// 結果を表示（3秒後に実行）
setTimeout(() => {
  console.table(apiTimings);
}, 3000);
```

---

## 4. 計画書v2.0の目標との比較

### 4.1 計画書v2.0の目標

| 指標 | 計画書v2.0の目標 | 現在の指標 | 確認方法 |
|------|-----------------|-----------|----------|
| **APIレスポンスタイム** | < 500ms | ⏳ 要確認 | NetworkタブまたはConsole API |
| **ページ読み込み時間** | < 1秒 | ⏳ 要確認 | Performanceタブ（Navigation Timing）またはNetworkタブ（Finish Time） |

### 4.2 現在確認できている指標

| 指標 | 値 | 評価 | 計画書v2.0の目標との関係 |
|------|-----|------|----------------------|
| **LCP** | 2.03秒 | ✅ Good | 異なる指標（最大コンテンツの表示時間） |
| **CLS** | 0.03 | ✅ Good | レイアウトの安定性（読み込み速度とは異なる） |
| **INP** | 96ms | ✅ Good | インタラクションの応答時間（読み込み速度とは異なる） |

### 4.3 確認が必要な指標

#### 1. ページ全体の読み込み時間
- **確認方法**: 
  - Performanceタブの「Navigation Timing」で「Load」時間を確認
  - または、Networkタブの「Summary」で「Finish Time」を確認
- **目標**: < 1秒（計画書v2.0）

#### 2. APIレスポンスタイム
- **確認方法**: 
  - Networkタブで`/api/monthly/current`の「Total Time」を確認
  - または、Console APIで計測
- **目標**: < 500ms（計画書v2.0）

---

## 5. 次のステップ

### 5.1 確認手順

#### Step 1: ページ全体の読み込み時間を確認
1. Performanceタブで記録を開始
2. ページをリロード
3. 記録を停止
4. 「Navigation Timing」で「Load」時間を確認
   - または、Networkタブの「Summary」で「Finish Time」を確認

#### Step 2: APIレスポンスタイムを確認
1. Networkタブを開く
2. ページをリロード
3. `/api/monthly/current`のリクエストを探す
4. 「Timing」タブで「Total Time」を確認

#### Step 3: 結果の評価
- ページ全体の読み込み時間 < 1秒か？
- APIレスポンスタイム < 500msか？

### 5.2 確認後の対応

#### 目標達成している場合
- ✅ Phase 2完了として報告
- Phase 3（事前集計テーブルの活用）は任意

#### 目標未達成の場合
- ⚠️ Phase 3（事前集計テーブルの活用）の検討
- その他のパフォーマンス最適化の検討

---

## 6. まとめ

### 6.1 現在確認できている指標

- ✅ **LCP**: 2.03秒（Good）
- ✅ **CLS**: 0.03（Good）
- ✅ **INP**: 96ms（Good）

### 6.2 確認が必要な指標

- ⏳ **ページ全体の読み込み時間**: Performanceタブ（Navigation Timing）またはNetworkタブ（Finish Time）で確認
- ⏳ **APIレスポンスタイム**: Networkタブ（`/api/monthly/current`のTotal Time）で確認

### 6.3 計画書v2.0の目標

- **APIレスポンスタイム**: < 500ms
- **ページ読み込み時間**: < 1秒

---

**作成日時**: 2025-10-31
**評価者**: AI Assistant


