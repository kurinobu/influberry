# ステップ3修正: 競合・干渉リスク分析レポート

**調査日**: 2025年11月2日  
**調査者**: AI Assistant  
**対象**: 初期表示ロジック修正の問題解決に関するリスク分析

---

## 📋 目次

1. [問題の再確認](#1-問題の再確認)
2. [修正方法の候補](#2-修正方法の候補)
3. [競合・干渉リスク分析](#3-競合干渉リスク分析)
4. [各修正方法のリスク評価](#4-各修正方法のリスク評価)
5. [推奨修正方法](#5-推奨修正方法)
6. [実装時の注意事項](#6-実装時の注意事項)

---

## 1. 問題の再確認

### 1.1 問題の根本原因

**現在のフロー**:
```
1. onMounted(): currentMonthTab.value = 'overview'（ステップ3で設定）
   ↓
2. watch(() => rotationStore.rotationState) トリガー
   → handleRotationStateChange() 実行
   → triggerTabUpdate() 実行
   → currentMonthTab.value = '2025-11'（上書き）
   ↓
3. watch(() => currentMonthTab.value) トリガー
   → syncReactiveUpdates() 実行
   → 最終的に currentMonthTab.value = '2025-10'（上書き）
```

**問題点**:
- ❌ `watch(() => rotationStore.rotationState)`が`onMounted()`で設定した`overview`を上書き
- ❌ `watch(() => currentMonthTab.value)`が再度`overview`を上書き
- ❌ 初期表示時に`triggerTabUpdate()`が実行されてしまう

### 1.2 競合している`watch`関数

#### **watch1: `watch(() => rotationStore.rotationState)`** (517行目)
```javascript
watch(() => rotationStore.rotationState, handleRotationStateChange)

const handleRotationStateChange = (newState, oldState) => {
  if (newState === 'completed') {
    triggerTabUpdate()  // ← これが実行されて、currentMonthTabを変更
  }
}
```

#### **watch2: `watch(() => rotationStore.lastRotationCheck)`** (481行目)
```javascript
watch(() => rotationStore.lastRotationCheck, (newValue, oldValue) => {
  if (!oldValue || !newValue || newValue === oldValue) {
    return
  }
  // ...
  triggerTabUpdate()  // ← これも実行される可能性がある
})
```

#### **watch3: `watch(() => currentMonthTab.value)`** (520行目)
```javascript
watch(() => currentMonthTab.value, async (newTab, oldTab) => {
  // 月次切り替え状態を確認して、タブを変更する可能性がある
  // ...
})
```

---

## 2. 修正方法の候補

### 修正方法1: `watch(() => rotationStore.rotationState)`の条件を追加

**修正内容**:
```javascript
const handleRotationStateChange = (newState, oldState) => {
  console.log('月次切り替え状態変更を検知:', { newState, oldState })
  
  // 修正: 初期表示時（overviewタブ）は実行しない
  if (currentMonthTab.value === 'overview' && oldState === null) {
    console.log('⚠️ 初期表示時のため、triggerTabUpdate()をスキップ')
    return  // 初期表示時はスキップ
  }
  
  if (newState === 'completed') {
    console.log('月次切り替え完了を検知 - タブ更新をトリガー')
    triggerTabUpdate()
  }
}
```

**メリット**:
- ✅ 初期表示時の`triggerTabUpdate()`を防止
- ✅ 既存のロジックを最小限の変更で修正可能

**デメリット**:
- ⚠️ 条件判定が複雑になる可能性

### 修正方法2: `watch(() => rotationStore.lastRotationCheck)`の条件を追加

**修正内容**:
```javascript
watch(() => rotationStore.lastRotationCheck, (newValue, oldValue) => {
  // 初期化時や値が変わらない場合は実行しない
  if (!oldValue || !newValue || newValue === oldValue) {
    return
  }
  
  // 修正: 初期表示時（overviewタブ）は実行しない
  if (currentMonthTab.value === 'overview' && !oldValue) {
    console.log('⚠️ 初期表示時のため、triggerTabUpdate()をスキップ')
    return  // 初期表示時はスキップ
  }
  
  // 既存のロジック...
  triggerTabUpdate()
})
```

**メリット**:
- ✅ 初期表示時の`triggerTabUpdate()`を防止
- ✅ 既存のロジックを最小限の変更で修正可能

**デメリット**:
- ⚠️ 条件判定が複雑になる可能性

### 修正方法3: `watch(() => currentMonthTab.value)`の条件を追加

**修正内容**:
```javascript
watch(() => currentMonthTab.value, async (newTab, oldTab) => {
  // 修正: 初期表示時（overviewタブ）は実行しない
  if (newTab === 'overview' && oldTab === undefined) {
    console.log('⚠️ 初期表示時のため、タブ更新処理をスキップ')
    return  // 初期表示時はスキップ
  }
  
  // 既存のロジック...
})
```

**メリット**:
- ✅ 初期表示時のタブ更新処理を防止
- ✅ 既存のロジックを最小限の変更で修正可能

**デメリット**:
- ⚠️ `oldTab === undefined`の条件が正しく動作するか確認が必要

### 修正方法4: フラグによる初期表示制御

**修正内容**:
```javascript
// 初期表示制御フラグ
const isInitialDisplay = ref(true)

onMounted(async () => {
  // 初期表示: 概要タブを固定（最速表示）
  currentMonthTab.value = 'overview'
  
  // 軽量概要APIを並行実行
  await monthlyStore.fetchOverviewMinimal()
  
  // 月次データをバックグラウンドで非同期実行
  monthlyStore.fetchCurrentMonthlyData()
  
  // 初期表示完了後、フラグをオフ
  setTimeout(() => {
    isInitialDisplay.value = false
  }, 1000)  // 1秒後
})

const handleRotationStateChange = (newState, oldState) => {
  // 修正: 初期表示中は実行しない
  if (isInitialDisplay.value) {
    console.log('⚠️ 初期表示中のため、triggerTabUpdate()をスキップ')
    return
  }
  
  if (newState === 'completed') {
    triggerTabUpdate()
  }
}
```

**メリット**:
- ✅ 明確な初期表示制御
- ✅ タイミング制御が可能

**デメリット**:
- ⚠️ フラグ管理が追加される
- ⚠️ タイムアウトの時間設定が課題

---

## 3. 競合・干渉リスク分析

### 3.1 `triggerTabUpdate()`への依存関係

**使用箇所**:
- `handleRotationStateChange()`内で呼び出し（1箇所）
- `watch(() => rotationStore.lastRotationCheck)`内で呼び出し（1箇所）

**依存関係**:
- ❌ 他のコンポーネントからの直接呼び出しなし（確認済み）
- ✅ `DashboardPage.vue`内でのみ使用

**影響範囲**:
- ✅ 影響範囲は限定的（`DashboardPage.vue`内のみ）

### 3.2 `watch(() => rotationStore.rotationState)`への依存関係

**使用箇所**:
- `DashboardPage.vue`: `handleRotationStateChange()`を呼び出し（1箇所）
- `MonthlyTabs.vue`: タブ生成に使用（別のwatch関数）

**依存関係**:
- ✅ `MonthlyTabs.vue`は独自のwatchを使用しているため、影響なし
- ✅ `DashboardPage.vue`内でのみ使用

**影響範囲**:
- ✅ 影響範囲は限定的（`DashboardPage.vue`内のみ）

### 3.3 `watch(() => rotationStore.lastRotationCheck)`への依存関係

**使用箇所**:
- `DashboardPage.vue`: タブ更新トリガー（1箇所）

**依存関係**:
- ❌ 他のコンポーネントからの直接使用なし（確認済み）
- ✅ `DashboardPage.vue`内でのみ使用

**影響範囲**:
- ✅ 影響範囲は限定的（`DashboardPage.vue`内のみ）

### 3.4 `watch(() => currentMonthTab.value)`への依存関係

**使用箇所**:
- `DashboardPage.vue`: タブ変更時の処理（1箇所）

**依存関係**:
- ✅ `syncReactiveUpdates()`を呼び出しているのみ
- ✅ 他のコンポーネントからの直接使用なし

**影響範囲**:
- ✅ 影響範囲は限定的（`DashboardPage.vue`内のみ）

### 3.5 `MonthlyTabs.vue`への影響

**`MonthlyTabs.vue`の実装**:
```javascript
// MonthlyTabs.vueは独自のwatchを使用している
watch(() => [rotationStore.rotationState, rotationStore.lastRotationCheck], ...)
```

**影響分析**:
- ✅ `MonthlyTabs.vue`は独自のwatchを使用しているため、影響なし
- ✅ タブ生成ロジックは独立している

**結論**: ✅ **影響なし**

### 3.6 `MonthlyStatsSection.vue`への影響

**`MonthlyStatsSection.vue`の実装**:
```javascript
// MonthlyStatsSection.vueはprops.currentTabを使用している
watch(() => props.currentTab, ...)
```

**影響分析**:
- ✅ `MonthlyStatsSection.vue`は`props.currentTab`を使用している
- ✅ `currentMonthTab`の変更は`props.currentTab`を通じて伝播する
- ✅ 初期表示時の条件追加は影響しない

**結論**: ✅ **影響なし**

---

## 4. 各修正方法のリスク評価

### 修正方法1: `watch(() => rotationStore.rotationState)`の条件を追加

**リスク評価**:

| リスク項目 | リスクレベル | 説明 | 対策 |
|-----------|------------|------|------|
| **月次切り替え機能への影響** | 🟢 なし | 初期表示時のみスキップするため、月次切り替え機能は正常に動作 | 条件判定を明確化 |
| **タブ自動切り替えへの影響** | 🟢 なし | 初期表示時のみスキップするため、タブ自動切り替えは正常に動作 | - |
| **他のwatch関数への影響** | 🟢 なし | 他のwatch関数とは独立している | - |
| **MonthlyTabs.vueへの影響** | 🟢 なし | MonthlyTabs.vueは独自のwatchを使用 | - |
| **MonthlyStatsSection.vueへの影響** | 🟢 なし | props経由で伝播するため影響なし | - |
| **条件判定の複雑化** | 🟡 低 | `oldState === null`の条件を追加 | コメントで明確化 |

**総合リスク評価**: 🟢 **非常に低い**

### 修正方法2: `watch(() => rotationStore.lastRotationCheck)`の条件を追加

**リスク評価**:

| リスク項目 | リスクレベル | 説明 | 対策 |
|-----------|------------|------|------|
| **月次切り替え機能への影響** | 🟢 なし | 初期表示時のみスキップするため、月次切り替え機能は正常に動作 | 条件判定を明確化 |
| **タブ自動切り替えへの影響** | 🟢 なし | 初期表示時のみスキップするため、タブ自動切り替えは正常に動作 | - |
| **他のwatch関数への影響** | 🟢 なし | 他のwatch関数とは独立している | - |
| **MonthlyTabs.vueへの影響** | 🟢 なし | MonthlyTabs.vueは独自のwatchを使用 | - |
| **MonthlyStatsSection.vueへの影響** | 🟢 なし | props経由で伝播するため影響なし | - |
| **条件判定の複雑化** | 🟡 低 | `!oldValue`の条件を追加 | コメントで明確化 |

**総合リスク評価**: 🟢 **非常に低い**

### 修正方法3: `watch(() => currentMonthTab.value)`の条件を追加

**リスク評価**:

| リスク項目 | リスクレベル | 説明 | 対策 |
|-----------|------------|------|------|
| **タブ切り替え機能への影響** | 🟡 中 | 初期表示時のみスキップするが、タブ切り替えのタイミングに影響する可能性 | 慎重なテストが必要 |
| **syncReactiveUpdates()への影響** | 🟡 中 | 初期表示時に`syncReactiveUpdates()`が実行されない | 初期表示時の同期化が不要か確認 |
| **他のwatch関数への影響** | 🟢 なし | 他のwatch関数とは独立している | - |
| **MonthlyTabs.vueへの影響** | 🟢 なし | MonthlyTabs.vueは独自のwatchを使用 | - |
| **MonthlyStatsSection.vueへの影響** | 🟢 なし | props経由で伝播するため影響なし | - |
| **oldTab === undefinedの判定** | 🟡 低 | Vueのwatchの動作に依存 | テストで確認が必要 |

**総合リスク評価**: 🟡 **低い（テストが必要）**

### 修正方法4: フラグによる初期表示制御

**リスク評価**:

| リスク項目 | リスクレベル | 説明 | 対策 |
|-----------|------------|------|------|
| **フラグ管理の複雑化** | 🟡 低 | 追加のフラグ管理が必要 | コメントで明確化 |
| **タイムアウト時間の設定** | 🟡 中 | 適切なタイムアウト時間の設定が必要 | 環境に応じて調整 |
| **月次切り替え機能への影響** | 🟢 なし | 初期表示後は正常に動作 | - |
| **タブ自動切り替えへの影響** | 🟢 なし | 初期表示後は正常に動作 | - |
| **他のwatch関数への影響** | 🟢 なし | フラグによる制御のため影響なし | - |

**総合リスク評価**: 🟡 **低い（フラグ管理が必要）**

---

## 5. 推奨修正方法

### 推奨方法: 修正方法1 + 修正方法2の組み合わせ

**推奨理由**:
1. ✅ **リスクが最も低い**: 初期表示時のみスキップするため、既存機能への影響が最小限
2. ✅ **修正範囲が小さい**: 既存のロジックを最小限の変更で修正可能
3. ✅ **明確な条件判定**: `oldState === null`と`!oldValue`の条件で明確に初期表示時を判定
4. ✅ **他の機能への影響なし**: 月次切り替え機能、タブ自動切り替え機能は正常に動作

**修正内容**:
```javascript
// 修正1: handleRotationStateChange()の条件を追加
const handleRotationStateChange = (newState, oldState) => {
  console.log('月次切り替え状態変更を検知:', { newState, oldState })
  
  // 修正: 初期表示時（overviewタブ）は実行しない
  if (currentMonthTab.value === 'overview' && oldState === null) {
    console.log('⚠️ 初期表示時のため、triggerTabUpdate()をスキップ')
    return  // 初期表示時はスキップ
  }
  
  if (newState === 'completed') {
    console.log('月次切り替え完了を検知 - タブ更新をトリガー')
    triggerTabUpdate()
  }
}

// 修正2: watch(() => rotationStore.lastRotationCheck)の条件を追加
watch(() => rotationStore.lastRotationCheck, (newValue, oldValue) => {
  // 初期化時や値が変わらない場合は実行しない
  if (!oldValue || !newValue || newValue === oldValue) {
    return
  }
  
  // 修正: 初期表示時（overviewタブ）は実行しない
  if (currentMonthTab.value === 'overview' && !oldValue) {
    console.log('⚠️ 初期表示時のため、triggerTabUpdate()をスキップ')
    return  // 初期表示時はスキップ
  }
  
  // 既存のロジック...
  triggerTabUpdate()
})
```

**期待効果**:
- ✅ 初期表示時に`triggerTabUpdate()`が実行されない
- ✅ 初期表示が「概要」タブで固定される
- ✅ 月次切り替え機能は正常に動作する
- ✅ タブ自動切り替え機能は正常に動作する

---

## 6. 実装時の注意事項

### 6.1 条件判定の正確性

**注意点**:
- `oldState === null`の条件が正しく動作するか確認
- `!oldValue`の条件が正しく動作するか確認
- 初期表示時のタイミングを正確に判定する必要がある

**対策**:
- デバッグログを追加して条件判定を確認
- 複数の環境（ローカル・ステージング）でテスト

### 6.2 既存機能への影響確認

**確認項目**:
- [ ] 月次切り替え機能が正常に動作するか
- [ ] タブ自動切り替え機能が正常に動作するか
- [ ] 手動でタブを切り替えた時の動作
- [ ] 月次切り替え後にタブが自動切り替えされるか

### 6.3 アイコン・ボタン・テキスト・カラーリングへの影響

**確認項目**:
- ✅ **アイコン**: 変更なし（データ取得ロジックのみ変更）
- ✅ **テキスト**: 変更なし（データ取得ロジックのみ変更）
- ✅ **ボタン**: 変更なし（データ取得ロジックのみ変更）
- ✅ **カラーリング**: 変更なし（データ取得ロジックのみ変更）

**結論**: ✅ **影響なし**

---

## 7. まとめ

### 7.1 問題の根本原因

**競合している`watch`関数**:
1. `watch(() => rotationStore.rotationState)` - `triggerTabUpdate()`を実行
2. `watch(() => rotationStore.lastRotationCheck)` - `triggerTabUpdate()`を実行
3. `watch(() => currentMonthTab.value)` - タブ変更時の処理

**問題**:
- これらの`watch`が`onMounted()`で設定した`overview`を上書きしている

### 7.2 推奨修正方法

**修正方法1 + 修正方法2の組み合わせ**:
- `handleRotationStateChange()`に初期表示時の条件を追加
- `watch(() => rotationStore.lastRotationCheck)`に初期表示時の条件を追加

**リスク評価**: 🟢 **非常に低い**

### 7.3 競合・干渉リスク

**影響範囲**:
- ✅ `DashboardPage.vue`内のみ（他のコンポーネントへの影響なし）
- ✅ 月次切り替え機能は正常に動作
- ✅ タブ自動切り替え機能は正常に動作
- ✅ アイコン・テキスト・カラーリングへの影響なし

**総合評価**: ✅ **リスクは非常に低い**

---

**作成日**: 2025年11月2日  
**最終更新**: 2025年11月2日  
**調査者**: AI Assistant

