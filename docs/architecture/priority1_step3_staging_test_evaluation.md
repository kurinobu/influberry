# ステップ3: 初期表示ロジック修正 ステージングテスト評価レポート

**テスト日**: 2025年11月2日  
**テスト環境**: ステージング環境（https://staging.influberry.jp）  
**テスト結果**: ⚠️ **問題発見 - 初期表示が「概要」タブにならない**

---

## 📊 テスト結果の要約

### ⚠️ 問題項目

1. **初期表示が「概要」タブになっていない**: ⚠️ 問題あり
   - 表示順序: 「スケルトン」→「概要」→「先月」
   - 最終表示: 「先月」（`2025-10`）タブ
   - **期待**: 「概要」タブが表示される

2. **タブが複数回切り替わっている**: ⚠️ 問題あり
   - `overview` → `2025-11` → `2025-10` → `overview` → `2025-10`
   - 最終的に`2025-10`になっている

### ✅ 成功項目

1. **軽量概要APIが呼び出されている**: ✅ 成功
   - `/api/monthly-stats/overview-minimal`が呼び出されている
   - レスポンスタイム: 3.00秒（ローカルより遅いが、ステージング環境の制約）

2. **月次データがバックグラウンドで取得されている**: ✅ 成功
   - `/api/monthly/current`がバックグラウンドで呼び出されている

---

## 🔍 詳細分析

### 1. タブ切り替えの流れ（問題の原因）

**ログからの確認**:
```
1. 初期状態: currentMonthTab = 'overview'（ステップ3で設定）
   ↓
2. 月次切り替え状態変更を検知: {newState: 'completed', oldState: 'idle'}
   ↓
3. triggerTabUpdate() 実行
   → ⚠️ lastRotationCheckが現在月より古い - 現在月を優先
   → currentMonthTab.value = '2025-11'
   ↓
4. watch(() => currentMonthTab.value) トリガー
   → 🎉 新しい月のタブが選択されました {selectedTab: '2025-11'}
   ↓
5. 再度 watch(() => currentMonthTab.value) トリガー
   → currentMonthTab.value = '2025-10'（月次切り替え状態に基づく）
   ↓
6. onMounted() 完了後
   → currentMonthTab.value = 'overview'（一時的に）
   ↓
7. 再度 watch(() => currentMonthTab.value) トリガー
   → currentMonthTab.value = '2025-10'（最終的に）
```

**問題の根本原因**:
- ✅ `onMounted()`で`currentMonthTab.value = 'overview'`を設定している
- ❌ しかし、その後に`watch(() => rotationStore.rotationState)`がトリガーされる
- ❌ `triggerTabUpdate()`が実行され、`currentMonthTab.value = '2025-11'`に変更される
- ❌ さらに`watch(() => currentMonthTab.value)`がトリガーされ、`2025-10`に変更される
- ❌ 最終的に`2025-10`になっている

### 2. 問題箇所の特定

**問題箇所1: `watch(() => rotationStore.rotationState)`**

**現在の実装**:
```javascript
watch(() => rotationStore.rotationState, (newState, oldState) => {
  if (newState === 'completed' && newState !== oldState) {
    triggerTabUpdate()  // ← これが実行されて、currentMonthTabが変更される
  }
})
```

**問題**:
- 月次切り替え状態が`completed`になると、`triggerTabUpdate()`が実行される
- `triggerTabUpdate()`が`currentMonthTab.value = '2025-11'`に変更する
- これにより、`onMounted()`で設定した`overview`が上書きされる

**問題箇所2: `watch(() => currentMonthTab.value)`**

**現在の実装**:
```javascript
watch(() => currentMonthTab.value, async (newTab, oldTab) => {
  // 月次切り替え状態を確認
  if (rotationState === 'completed' && lastRotationCheck) {
    // lastRotationCheckを基準にタブを選択
    currentMonthTab.value = lastMonthId  // ← '2025-10'に変更される
  }
})
```

**問題**:
- `currentMonthTab`が変更されると、`watch`がトリガーされる
- `watch`内で再度`currentMonthTab.value`を変更している
- これにより、`overview`が最終的に`2025-10`に上書きされる

### 3. パフォーマンス分析

**ステージング環境のパフォーマンス**:

| 指標 | ローカル | ステージング | 評価 |
|------|---------|------------|------|
| **Finish Time** | 1.13秒 | **21.67秒** | ⚠️ **非常に遅い** |
| **DOMContentLoaded** | 410ms | **559ms** | ✅ 許容範囲 |
| **Load Time** | 1.02秒 | **1.85秒** | ⚠️ 遅い |
| **初期表示API** | 26ms | **3.00秒** | ⚠️ **非常に遅い** |

**評価**:
- ⚠️ Finish Timeと初期表示APIが非常に遅い（ステージング環境の制約）
- ✅ DOMContentLoadedは許容範囲内
- ⚠️ しかし、タブ切り替えの問題がより深刻

### 4. 問題の影響

**ユーザー体験への影響**:
- ❌ 初期表示が「概要」タブにならない
- ❌ タブが複数回切り替わって見える（フリッカー）
- ❌ ユーザーが混乱する可能性

**機能への影響**:
- ✅ 軽量概要APIは正常に呼び出されている
- ✅ 月次データも正常に取得されている
- ❌ しかし、初期表示が「概要」タブにならない

---

## 📋 問題の説明

### 問題1: 初期表示が「概要」タブにならない

**問題の詳細**:
- ステップ3で`onMounted()`で`currentMonthTab.value = 'overview'`を設定している
- しかし、その後に`watch(() => rotationStore.rotationState)`がトリガーされる
- `triggerTabUpdate()`が実行され、`currentMonthTab.value = '2025-11'`に変更される
- さらに`watch(() => currentMonthTab.value)`がトリガーされ、`2025-10`に変更される
- 最終的に`2025-10`になっている

**根本原因**:
- `watch(() => rotationStore.rotationState)`と`watch(() => currentMonthTab.value)`が競合している
- これらの`watch`が`onMounted()`で設定した`overview`を上書きしている

**ログからの確認**:
```
currentMonthTabの変更を検知 {newTab: '2025-11', oldTab: 'overview'}
  ↓
currentMonthTabの変更を検知 {newTab: '2025-10', oldTab: '2025-11'}
  ↓
currentMonthTabの変更を検知 {newTab: 'overview', oldTab: '2025-10'}
  ↓
currentMonthTabの変更を検知 {newTab: '2025-10', oldTab: 'overview'}
  ↓
最終的に: currentMonthTab = '2025-10'
```

### 問題2: タブが複数回切り替わっている

**問題の詳細**:
- タブが`overview` → `2025-11` → `2025-10` → `overview` → `2025-10`と切り替わっている
- ユーザーには「スケルトン」→「概要」→「先月」の順序で表示される

**根本原因**:
- 複数の`watch`が競合している
- `triggerTabUpdate()`と`watch(() => currentMonthTab.value)`が交互に実行されている

---

## 🎯 評価結果

### ステップ3の実装評価

**実装状況**: ⚠️ **部分的に成功（問題あり）**

**達成項目**:
- ✅ 軽量概要APIが正常に呼び出されている
- ✅ 月次データがバックグラウンドで取得されている
- ✅ コード実装は完了している

**問題項目**:
- ❌ 初期表示が「概要」タブにならない
- ❌ タブが複数回切り替わっている
- ❌ `watch`関数が競合している

**問題の根本原因**:
- `watch(() => rotationStore.rotationState)`と`watch(() => currentMonthTab.value)`が競合している
- これらの`watch`が`onMounted()`で設定した`overview`を上書きしている

---

## 📝 推奨される修正方法

### 修正方法1: `watch(() => rotationStore.rotationState)`の条件を追加

**修正内容**:
```javascript
watch(() => rotationStore.rotationState, (newState, oldState) => {
  // 初期表示時（overviewタブ）は実行しない
  if (currentMonthTab.value === 'overview' && oldState === null) {
    return  // 初期表示時はスキップ
  }
  
  if (newState === 'completed' && newState !== oldState) {
    triggerTabUpdate()
  }
})
```

### 修正方法2: `watch(() => currentMonthTab.value)`の条件を追加

**修正内容**:
```javascript
watch(() => currentMonthTab.value, async (newTab, oldTab) => {
  // 初期表示時（overviewタブ）は実行しない
  if (newTab === 'overview' && oldTab === undefined) {
    return  // 初期表示時はスキップ
  }
  
  // 既存のロジック...
})
```

### 修正方法3: `triggerTabUpdate()`の実行タイミングを調整

**修正内容**:
```javascript
// onMounted()で初期表示を設定した後、一定時間後にtriggerTabUpdate()を実行
onMounted(async () => {
  // 初期表示: 概要タブを固定
  currentMonthTab.value = 'overview'
  
  // 軽量概要APIを並行実行
  await monthlyStore.fetchOverviewMinimal()
  
  // 月次データをバックグラウンドで非同期実行
  monthlyStore.fetchCurrentMonthlyData()
  
  // 初期表示後、一定時間後にタブ更新を許可
  setTimeout(() => {
    // タブ更新を許可するフラグを設定
    allowTabUpdate.value = true
  }, 1000)  // 1秒後
})
```

---

## 🔍 問題の優先度

### 優先度評価

| 問題 | 優先度 | 理由 |
|------|--------|------|
| **初期表示が「概要」タブにならない** | 🔴 **最高** | ステップ3の主要な目標が達成されていない |
| **タブが複数回切り替わっている** | 🔴 **最高** | ユーザー体験に悪影響 |
| **パフォーマンス（ステージング）** | 🟡 **中** | ステージング環境の制約によるもの |

**総合評価**: ⚠️ **修正が必要**

---

## 📝 結論

### ステップ3の実装評価

**実装状況**: ⚠️ **部分的に成功（問題あり）**

**達成項目**:
- ✅ 軽量概要APIが正常に呼び出されている
- ✅ 月次データがバックグラウンドで取得されている
- ✅ コード実装は完了している

**問題項目**:
- ❌ 初期表示が「概要」タブにならない（主要な問題）
- ❌ タブが複数回切り替わっている（ユーザー体験への悪影響）
- ❌ `watch`関数が競合している（根本原因）

**問題の根本原因**:
- `watch(() => rotationStore.rotationState)`と`watch(() => currentMonthTab.value)`が競合している
- これらの`watch`が`onMounted()`で設定した`overview`を上書きしている

**修正の優先度**: 🔴 **最高（即座に対応が必要）**

---

**作成日**: 2025年11月2日  
**最終更新**: 2025年11月2日  
**評価者**: AI Assistant

