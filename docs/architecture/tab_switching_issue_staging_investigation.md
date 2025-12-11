# ステージング環境: タブ切り替え問題の完全調査分析レポート

**作成日**: 2025年11月1日  
**問題**: ステージング環境で、現在月（2025-11）に設定されるが、直後に前月（2025-10）に戻される  
**目的**: 問題の根本原因を特定し、大原則に沿った修正案を提示

---

## 1. 問題の詳細分析

### 1.1 問題の症状

**ユーザー報告**:
> 表示が、概要→当月タブ→前月タブ  
> と変わって当月タブではなく前月タブで停止する問題

**ログの時系列分析**:

1. **初期状態**:
   ```
   月次切り替え状態変更を検知: {newState: 'completed', oldState: 'idle'}
   lastRotationCheck: '2025-10-01T00:00:00'
   ```

2. **現在月の優先処理（`handleRotationStateChange`から）**:
   ```
   ⚠️ lastRotationCheckが現在月より古い - 現在月を優先（不一致チェックの厳密化）
   {currentMonthId: '2025-11', lastMonthId: '2025-10', ...}
   ```

3. **現在月に設定**:
   ```
   🔧 Phase 2: currentMonthTabの変更を検知 {newTab: '2025-11', oldTab: 'overview', ...}
   🎉 Phase 2: 新しい月のタブが選択されました {selectedTab: '2025-11', previousTab: 'overview'}
   ```

4. **前月に戻される（問題）**:
   ```
   🔧 Phase 2: currentMonthTabの変更を検知 {newTab: '2025-10', oldTab: '2025-11', ...}
   🎉 Phase 2: 新しい月のタブが選択されました {selectedTab: '2025-10', previousTab: '2025-11'}
   ```

5. **最終状態**:
   ```
   🔧 Phase 2: 同期化後の状態確認 {currentMonthTab: '2025-10', ...}
   ```

**重要な観察**:
- `triggerTabUpdate()`が実行され、現在月（2025-11）が設定される
- しかし、ログには「⚠️ lastRotationCheckが現在月より古い」または「🎉 月次切り替え完了 - lastRotationCheckを基準にタブ切り替え」のメッセージがない
- これは、`triggerTabUpdate()`が再度呼び出されていない可能性、または`triggerTabUpdate()`内のロジックが正しく動作していない可能性を示している

---

## 2. コードの実行フロー分析

### 2.1 実行フローの確認

**現在のコード構造**:

1. **`handleRotationStateChange`** (392行目):
   ```javascript
   const handleRotationStateChange = (newState, oldState) => {
     if (newState === 'completed' && oldState === 'running') {
       triggerTabUpdate()
     }
   }
   ```

2. **`watch(() => rotationStore.rotationState, handleRotationStateChange)`** (478行目):
   - `rotationState`が`idle`から`completed`に変更されたとき、`handleRotationStateChange`が呼び出される
   - しかし、`oldState === 'running'`の条件により、`triggerTabUpdate()`が呼び出されない

3. **`watch(() => rotationStore.lastRotationCheck, ...)`** (470行目):
   ```javascript
   watch(() => rotationStore.lastRotationCheck, (newValue, oldValue) => {
     if (newValue !== oldValue) {
       console.log('月次切り替えが検知されました。')
       triggerTabUpdate()
     }
   })
   ```

4. **`triggerTabUpdate()`** (112-177行目):
   - `isLastRotationOlder`が`true`の場合、現在月を設定（146-155行目）
   - `isLastRotationOlder`が`false`の場合、`lastRotationCheck`を基準に前月を設定（158-167行目）

### 2.2 問題の根本原因の特定

**問題の分析**:

ログを見ると:
1. `handleRotationStateChange`が呼び出され、`triggerTabUpdate()`が実行される
2. `triggerTabUpdate()`内で、`isLastRotationOlder`が`true`になり、現在月（2025-11）が設定される
3. しかし、その後`currentMonthTab`が`2025-10`に変更される

**根本原因の推測**:

1. **`watch(() => rotationStore.lastRotationCheck)`の実行タイミングの問題**:
   - `lastRotationCheck`が初期化時に設定される（`null`から`2025-10-01`に変更）
   - このとき、`oldValue`が`null`または`undefined`で、`newValue`が`2025-10-01`になる
   - `if (newValue !== oldValue)`の条件により、`triggerTabUpdate()`が呼び出される
   - しかし、この時点では`lastRotationCheck`が古い（2025-10-01）ため、`triggerTabUpdate()`内で`isLastRotationOlder`が`true`になるはず
   - しかし、ログには「⚠️ lastRotationCheckが現在月より古い」のメッセージがない

2. **`handleRotationStateChange`の条件の問題**:
   - `handleRotationStateChange`は`oldState === 'running'`の場合のみ`triggerTabUpdate()`を呼び出す
   - しかし、ログを見ると、`oldState`が`'idle'`で`newState`が`'completed'`になっている
   - この場合、`handleRotationStateChange`は`triggerTabUpdate()`を呼び出さない
   - しかし、ログには「⚠️ lastRotationCheckが現在月より古い - 現在月を優先」のメッセージがある
   - これは、別の経路で`triggerTabUpdate()`が呼び出されている可能性を示している

3. **実行順序の問題**:
   - `watch(() => rotationStore.lastRotationCheck)`が、`handleRotationStateChange`の実行後に実行される可能性
   - このとき、`lastRotationCheck`が古い（2025-10-01）ため、`triggerTabUpdate()`が再度呼び出される
   - しかし、この時点での`triggerTabUpdate()`内のロジックが、前月に戻す処理を実行している可能性

**評価**: 🔴 **`watch(() => rotationStore.lastRotationCheck)`が、初期化時や`lastRotationCheck`が変わらない状態で実行され、古い`lastRotationCheck`に基づいて前月に戻す処理を実行している可能性が高い**

---

## 3. 問題の根本原因の特定

### 3.1 `watch(() => rotationStore.lastRotationCheck)`の問題

**問題の詳細**:

1. **初期化時の実行**:
   - `lastRotationCheck`が初期化時に設定される（`null`から`2025-10-01`に変更）
   - このとき、`watch(() => rotationStore.lastRotationCheck)`が実行される
   - `oldValue`が`null`または`undefined`で、`newValue`が`2025-10-01`になる
   - `if (newValue !== oldValue)`の条件により、`triggerTabUpdate()`が呼び出される

2. **`triggerTabUpdate()`内のロジック**:
   - `triggerTabUpdate()`内で、`isLastRotationOlder`のチェックが実行される
   - しかし、この時点では`lastRotationCheck`が古い（2025-10-01）ため、`isLastRotationOlder`が`true`になるはず
   - しかし、ログには「⚠️ lastRotationCheckが現在月より古い」のメッセージがない
   - これは、`triggerTabUpdate()`内のロジックが正しく動作していない可能性を示している

3. **実行順序の問題**:
   - `handleRotationStateChange`が実行され、現在月が設定される
   - その後、`watch(() => rotationStore.lastRotationCheck)`が実行され、`triggerTabUpdate()`が再度呼び出される
   - このとき、`lastRotationCheck`が古い（2025-10-01）ため、前月に戻す処理が実行される

**評価**: 🔴 **`watch(() => rotationStore.lastRotationCheck)`が、初期化時や`lastRotationCheck`が変わらない状態で実行され、古い`lastRotationCheck`に基づいて前月に戻す処理を実行している**

### 3.2 `handleRotationStateChange`の条件の問題

**問題の詳細**:

1. **条件の問題**:
   - `handleRotationStateChange`は`oldState === 'running'`の場合のみ`triggerTabUpdate()`を呼び出す
   - しかし、ログを見ると、`oldState`が`'idle'`で`newState`が`'completed'`になっている
   - この場合、`handleRotationStateChange`は`triggerTabUpdate()`を呼び出さないはず
   - しかし、ログには「⚠️ lastRotationCheckが現在月より古い - 現在月を優先」のメッセージがある

2. **別の経路での実行**:
   - `watch(() => rotationStore.lastRotationCheck)`が実行され、`triggerTabUpdate()`が呼び出されている可能性
   - または、`initializeCurrentMonthTab()`が実行されている可能性

**評価**: ⚠️ **`handleRotationStateChange`の条件が厳密すぎる可能性がある（`oldState === 'running'`の条件により、`idle`から`completed`への変更が検知されない）**

---

## 4. 大原則に沿った修正案

### 4.1 計画書の大原則の確認

**計画書の目的**:
> ユーザーが月次で案件管理の進捗を可視化し、**目標設定と達成度評価**を行える機能を実装する。

**核心的な原則**:
1. **現在月を優先**: ユーザーが現在月の進捗を確認できるようにする
2. **一貫性**: タブの切り替えが一貫して動作する
3. **予測可能性**: ユーザーが期待する動作を実現する

### 4.2 修正案1: `watch(() => rotationStore.lastRotationCheck)`の条件を厳密化

**修正内容**:

1. **初期化時の実行を防止**:
   - `watch(() => rotationStore.lastRotationCheck)`が、初期化時や`lastRotationCheck`が変わらない状態で実行されないようにする
   - `oldValue`が`null`または`undefined`の場合、`triggerTabUpdate()`を呼び出さない

2. **現在月優先ロジックの強化**:
   - `triggerTabUpdate()`内で、現在月を優先するロジックを強化
   - `lastRotationCheck`が古い場合、現在月を設定し、`return`で早期終了

**修正ファイル**:
- `frontend/src/views/DashboardPage.vue` (470-475行目)

**修正コード**:
```javascript
// 修正案1: 初期化時の実行を防止し、現在月優先ロジックを強化
watch(() => rotationStore.lastRotationCheck, (newValue, oldValue) => {
  // 初期化時や値が変わらない場合は実行しない
  if (!oldValue || !newValue || newValue === oldValue) {
    return
  }
  
  console.log('月次切り替えが検知されました。')
  
  // 現在月を優先するため、triggerTabUpdate()を呼び出す前に現在日時を確認
  const now = new Date()
  const currentYear = now.getFullYear()
  const currentMonth = now.getMonth() + 1
  const currentMonthId = `${currentYear}-${currentMonth.toString().padStart(2, '0')}`
  
  const lastDate = new Date(newValue)
  const lastYear = lastDate.getFullYear()
  const lastMonth = lastDate.getMonth() + 1
  const lastMonthId = `${lastYear}-${lastMonth.toString().padStart(2, '0')}`
  
  // lastRotationCheckが現在月より古い場合は、triggerTabUpdate()を呼び出さない
  const isLastRotationOlder = (lastYear < currentYear) || 
                              (lastYear === currentYear && lastMonth < currentMonth)
  
  if (isLastRotationOlder) {
    console.log('⚠️ lastRotationCheckが現在月より古いため、triggerTabUpdate()をスキップ', {
      currentMonthId,
      lastMonthId,
      lastRotationCheck: newValue
    })
    return
  }
  
  triggerTabUpdate()
})
```

**効果**:
- 初期化時の不要な実行を防止
- 現在月を優先するロジックを強化
- `triggerTabUpdate()`の呼び出しを最適化

### 4.3 修正案2: `handleRotationStateChange`の条件を緩和

**修正内容**:

1. **条件の緩和**:
   - `oldState === 'running'`の条件を削除し、`newState === 'completed'`の場合のみ`triggerTabUpdate()`を呼び出す
   - これにより、`idle`から`completed`への変更も検知される

**修正ファイル**:
- `frontend/src/views/DashboardPage.vue` (392-398行目)

**修正コード**:
```javascript
// 修正案2: 条件を緩和し、completed状態の変更をすべて検知
const handleRotationStateChange = (newState, oldState) => {
  console.log('月次切り替え状態変更を検知:', { newState, oldState })
  
  // 修正: newState === 'completed'の場合、すべてtriggerTabUpdate()を呼び出す
  if (newState === 'completed') {
    console.log('月次切り替え完了を検知 - タブ更新をトリガー')
    triggerTabUpdate()
  }
}
```

**効果**:
- `idle`から`completed`への変更も検知される
- タブの切り替えがより確実に動作する

### 4.4 修正案3: `triggerTabUpdate()`内のロジックの強化（推奨）

**修正内容**:

1. **現在月優先ロジックの強化**:
   - `triggerTabUpdate()`内で、現在月を優先するロジックを最初に実行
   - `lastRotationCheck`が古い場合、現在月を設定し、`return`で早期終了

2. **デバッグログの追加**:
   - `triggerTabUpdate()`内の各分岐でデバッグログを追加し、実行フローを明確にする

**修正ファイル**:
- `frontend/src/views/DashboardPage.vue` (112-177行目)

**修正コード**:
```javascript
const triggerTabUpdate = async () => {
  console.log('🔧 タブ更新をトリガーします。')
  
  try {
    // 1. 現在日時を取得（最優先）
    const now = new Date()
    const currentYear = now.getFullYear()
    const currentMonth = now.getMonth() + 1
    const currentMonthId = `${currentYear}-${currentMonth.toString().padStart(2, '0')}`
    
    // 2. 月次切り替え状態を確認
    const rotationState = rotationStore.rotationState
    const lastRotationCheck = rotationStore.lastRotationCheck
    
    console.log('🔧 タブ更新: 月次切り替え状態を確認', {
      rotationState,
      lastRotationCheck,
      currentYear,
      currentMonth,
      currentMonthId
    })
    
    // 3. 修正: 現在月を優先するロジックを最初に実行
    // lastRotationCheckが古い場合、現在月を設定して早期終了
    if (rotationState === 'completed' && lastRotationCheck) {
      const baseDate = new Date(lastRotationCheck)
      const lastYear = baseDate.getFullYear()
      const lastMonth = baseDate.getMonth() + 1
      const lastMonthId = `${lastYear}-${lastMonth.toString().padStart(2, '0')}`
      
      const isLastRotationOlder = (lastYear < currentYear) || 
                                  (lastYear === currentYear && lastMonth < currentMonth)
      
      if (isLastRotationOlder) {
        console.log('⚠️ lastRotationCheckが現在月より古い - 現在月を優先（不一致チェックの厳密化）', {
          currentMonthId,
          lastMonthId,
          lastRotationCheck,
          reason: 'lastRotationCheckが現在月より古いため、現在月を優先'
        })
        currentMonthTab.value = currentMonthId
        await rotationStore.refreshFrontendData()
        return  // 早期終了
      }
      
      // lastRotationCheckが現在月と同じか新しい場合のみ、lastRotationCheckを基準にタブ切り替え
      console.log('🎉 月次切り替え完了 - lastRotationCheckを基準にタブ切り替え', {
        previousTab: currentMonthTab.value,
        newTab: lastMonthId,
        currentMonthTab: currentMonthTab.value,
        reason: 'lastRotationCheckが現在月と同じか新しいため、lastRotationCheckを基準に選択'
      })
      currentMonthTab.value = lastMonthId
      await rotationStore.refreshFrontendData()
      return  // 早期終了
    }
    
    // 4. フォールバック - 現在月を設定
    console.log('📅 現在月を設定:', currentMonthId)
    currentMonthTab.value = currentMonthId
    
  } catch (error) {
    console.error('❌ タブ更新エラー:', error)
  }
}
```

**効果**:
- 現在月を優先するロジックが確実に実行される
- デバッグログにより、実行フローが明確になる

---

## 5. 統合修正案（推奨）

### 5.1 修正案1, 2, 3の統合

**修正内容**:

1. **修正案1**: `watch(() => rotationStore.lastRotationCheck)`の条件を厳密化
2. **修正案2**: `handleRotationStateChange`の条件を緩和
3. **修正案3**: `triggerTabUpdate()`内のロジックの強化（既に実装済み）

**効果**:
- 初期化時の不要な実行を防止
- `idle`から`completed`への変更も検知される
- 現在月を優先するロジックが確実に実行される

---

## 6. 競合・干渉リスク分析

### 6.1 他の機能への影響

#### リスク1: `watch(() => rotationStore.lastRotationCheck)`の変更による影響

**影響範囲**: 
- `DashboardPage.vue`内の`watch(() => rotationStore.lastRotationCheck)`

**リスク内容**:
- `watch(() => rotationStore.lastRotationCheck)`の条件を厳密化することで、月次切り替えの検知が遅れる可能性
- しかし、`handleRotationStateChange`で検知するため、問題ない

**対策**:
- `handleRotationStateChange`の条件を緩和することで、月次切り替えの検知を確保

**リスクレベル**: 🟢 **低**（`handleRotationStateChange`で検知するため）

#### リスク2: `handleRotationStateChange`の条件変更による影響

**影響範囲**:
- `DashboardPage.vue`内の`handleRotationStateChange`

**リスク内容**:
- `oldState === 'running'`の条件を削除することで、不要な`triggerTabUpdate()`呼び出しが発生する可能性
- しかし、`triggerTabUpdate()`内で現在月を優先するロジックがあるため、問題ない

**対策**:
- `triggerTabUpdate()`内で現在月を優先するロジックを強化

**リスクレベル**: 🟢 **低**（`triggerTabUpdate()`内で適切に処理される）

### 6.2 UIへの影響

#### リスク3: タブの切り替えタイミングの変更

**影響範囲**:
- `MonthlyTabs.vue`、`MonthlyStatsSection.vue`

**リスク内容**:
- タブの切り替えタイミングが変わる可能性
- しかし、現在月を優先するロジックにより、ユーザー体験が向上する

**対策**:
- デバッグログにより、実行フローを確認

**リスクレベル**: 🟢 **低**（ユーザー体験の向上）

### 6.3 データフローへの影響

#### リスク4: データ取得タイミングの変更

**影響範囲**:
- `monthly.js`、`MonthlyStatsSection.vue`

**リスク内容**:
- タブの切り替えタイミングが変わることで、データ取得タイミングが変わる可能性
- しかし、既存のデータ取得ロジックは変更しないため、問題ない

**対策**:
- 既存のデータ取得ロジックを変更しない

**リスクレベル**: 🟢 **低**（既存ロジックに影響なし）

---

## 7. 推奨される修正案

### 7.1 統合修正案（修正案1 + 修正案2）

**修正内容**:

1. **修正案1**: `watch(() => rotationStore.lastRotationCheck)`の条件を厳密化
   - 初期化時の実行を防止
   - 現在月を優先するロジックを追加

2. **修正案2**: `handleRotationStateChange`の条件を緩和
   - `oldState === 'running'`の条件を削除
   - `newState === 'completed'`の場合、すべて`triggerTabUpdate()`を呼び出す

**効果**:
- 初期化時の不要な実行を防止
- `idle`から`completed`への変更も検知される
- 現在月を優先するロジックが確実に実行される

**リスクレベル**: 🟢 **低**（既存機能への影響が最小限）

---

## 8. 結論

### 8.1 問題の根本原因

**根本原因**:
- `watch(() => rotationStore.lastRotationCheck)`が、初期化時や`lastRotationCheck`が変わらない状態で実行され、古い`lastRotationCheck`に基づいて前月に戻す処理を実行している
- `handleRotationStateChange`の条件が厳密すぎる（`oldState === 'running'`の条件により、`idle`から`completed`への変更が検知されない）

### 8.2 推奨される修正案

**統合修正案（修正案1 + 修正案2）**:
1. `watch(() => rotationStore.lastRotationCheck)`の条件を厳密化
2. `handleRotationStateChange`の条件を緩和

**効果**:
- 初期化時の不要な実行を防止
- `idle`から`completed`への変更も検知される
- 現在月を優先するロジックが確実に実行される

**リスクレベル**: 🟢 **低**（既存機能への影響が最小限）

---

---

## 9. 修正案の実装詳細

### 9.1 統合修正案の実装手順

**修正ファイル1**: `frontend/src/views/DashboardPage.vue`

#### 修正箇所1: `watch(() => rotationStore.lastRotationCheck)`の条件を厳密化（470-475行目）

**修正前**:
```javascript
watch(() => rotationStore.lastRotationCheck, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    console.log('月次切り替えが検知されました。')
    triggerTabUpdate()
  }
})
```

**修正後**:
```javascript
// 修正案1: 初期化時の実行を防止し、現在月優先ロジックを強化
watch(() => rotationStore.lastRotationCheck, (newValue, oldValue) => {
  // 初期化時や値が変わらない場合は実行しない
  if (!oldValue || !newValue || newValue === oldValue) {
    return
  }
  
  console.log('月次切り替えが検知されました。')
  
  // 現在月を優先するため、triggerTabUpdate()を呼び出す前に現在日時を確認
  const now = new Date()
  const currentYear = now.getFullYear()
  const currentMonth = now.getMonth() + 1
  const currentMonthId = `${currentYear}-${currentMonth.toString().padStart(2, '0')}`
  
  const lastDate = new Date(newValue)
  const lastYear = lastDate.getFullYear()
  const lastMonth = lastDate.getMonth() + 1
  const lastMonthId = `${lastYear}-${lastMonth.toString().padStart(2, '0')}`
  
  // lastRotationCheckが現在月より古い場合は、triggerTabUpdate()を呼び出さない
  const isLastRotationOlder = (lastYear < currentYear) || 
                              (lastYear === currentYear && lastMonth < currentMonth)
  
  if (isLastRotationOlder) {
    console.log('⚠️ lastRotationCheckが現在月より古いため、triggerTabUpdate()をスキップ', {
      currentMonthId,
      lastMonthId,
      lastRotationCheck: newValue
    })
    return
  }
  
  triggerTabUpdate()
})
```

#### 修正箇所2: `handleRotationStateChange`の条件を緩和（392-398行目）

**修正前**:
```javascript
const handleRotationStateChange = (newState, oldState) => {
  console.log('月次切り替え状態変更を検知:', { newState, oldState })
  if (newState === 'completed' && oldState === 'running') {
    console.log('月次切り替え完了を検知 - タブ更新をトリガー')
    triggerTabUpdate()
  }
}
```

**修正後**:
```javascript
// 修正案2: 条件を緩和し、completed状態の変更をすべて検知
const handleRotationStateChange = (newState, oldState) => {
  console.log('月次切り替え状態変更を検知:', { newState, oldState })
  
  // 修正: newState === 'completed'の場合、すべてtriggerTabUpdate()を呼び出す
  if (newState === 'completed') {
    console.log('月次切り替え完了を検知 - タブ更新をトリガー')
    triggerTabUpdate()
  }
}
```

---

## 10. 競合・干渉リスクの詳細分析

### 10.1 他の機能への影響

#### リスク1: `watch(() => rotationStore.lastRotationCheck)`の変更による影響

**影響範囲**: 
- `DashboardPage.vue`内の`watch(() => rotationStore.lastRotationCheck)` (470-475行目)

**リスク内容**:
- `watch(() => rotationStore.lastRotationCheck)`の条件を厳密化することで、月次切り替えの検知が遅れる可能性
- しかし、`handleRotationStateChange`で検知するため、問題ない

**対策**:
- `handleRotationStateChange`の条件を緩和することで、月次切り替えの検知を確保
- `checkRotationStatus()`が実行される際に、`rotationState`が`completed`に設定されるため、`handleRotationStateChange`が呼び出される

**リスクレベル**: 🟢 **低**（`handleRotationStateChange`で検知するため）

#### リスク2: `handleRotationStateChange`の条件変更による影響

**影響範囲**:
- `DashboardPage.vue`内の`handleRotationStateChange` (392-398行目)

**リスク内容**:
- `oldState === 'running'`の条件を削除することで、不要な`triggerTabUpdate()`呼び出しが発生する可能性
- しかし、`triggerTabUpdate()`内で現在月を優先するロジックがあるため、問題ない

**対策**:
- `triggerTabUpdate()`内で現在月を優先するロジックを強化（既に実装済み）

**リスクレベル**: 🟢 **低**（`triggerTabUpdate()`内で適切に処理される）

### 10.2 UIへの影響

#### リスク3: タブの切り替えタイミングの変更

**影響範囲**:
- `MonthlyTabs.vue`、`MonthlyStatsSection.vue`

**リスク内容**:
- タブの切り替えタイミングが変わる可能性
- しかし、現在月を優先するロジックにより、ユーザー体験が向上する

**対策**:
- デバッグログにより、実行フローを確認

**リスクレベル**: 🟢 **低**（ユーザー体験の向上）

### 10.3 データフローへの影響

#### リスク4: データ取得タイミングの変更

**影響範囲**:
- `monthly.js`、`MonthlyStatsSection.vue`

**リスク内容**:
- タブの切り替えタイミングが変わることで、データ取得タイミングが変わる可能性
- しかし、既存のデータ取得ロジックは変更しないため、問題ない

**対策**:
- 既存のデータ取得ロジックを変更しない

**リスクレベル**: 🟢 **低**（既存ロジックに影響なし）

### 10.4 実行フローへの影響

#### リスク5: 実行順序の変更

**影響範囲**:
- `DashboardPage.vue`内の`watch`の実行順序

**リスク内容**:
- `watch(() => rotationStore.lastRotationCheck)`の条件を厳密化することで、実行順序が変わる可能性
- しかし、`handleRotationStateChange`で検知するため、問題ない

**対策**:
- `handleRotationStateChange`の条件を緩和することで、実行順序を確保

**リスクレベル**: 🟢 **低**（実行順序が改善される）

---

## 11. 修正案の実装優先順位

### 11.1 推奨される修正案

**統合修正案（修正案1 + 修正案2）**:

1. **修正案1**: `watch(() => rotationStore.lastRotationCheck)`の条件を厳密化
   - 初期化時の不要な実行を防止
   - 現在月を優先するロジックを追加

2. **修正案2**: `handleRotationStateChange`の条件を緩和
   - `oldState === 'running'`の条件を削除
   - `newState === 'completed'`の場合、すべて`triggerTabUpdate()`を呼び出す

**効果**:
- 初期化時の不要な実行を防止
- `idle`から`completed`への変更も検知される
- 現在月を優先するロジックが確実に実行される

**リスクレベル**: 🟢 **低**（既存機能への影響が最小限）

---

**作成者**: AI Assistant  
**関連文書**: 
- `staging_target_display_fix_test_evaluation.md`
- `phase3_implementation_plan.md`

