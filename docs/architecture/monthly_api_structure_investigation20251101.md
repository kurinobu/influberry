# 月次タブAPI構造調査レポート

**調査日時**: 2025年11月1日  
**調査対象**: InfluBerry 月次管理機能のAPI設計  
**調査依頼**: `/api/monthly/current` と `/api/monthly/history` の分離状況

---

## 1. 調査結果サマリー

### 1.1 API分離の設計意図（計画書v2.0）

計画書v2.0では、以下のAPI分離戦略が明確に定義されています：

| エンドポイント | 用途 | 返却データ | 目標レスポンスタイム |
|-------------|------|-----------|-------------------|
| **`GET /api/monthly/current`** | 今月+先月+次月の3ヶ月分のみ | 軽量・高速 | **< 500ms** |
| **`GET /api/monthly/history`** | 過去の履歴データ（必要時のみロード） | 重い | - |

### 1.2 設計の根拠

**従来の問題点**:
```
GET /api/monthly → 全履歴を一度に返す（重い・遅い）
```

**改善後の構造**:
```
GET /api/monthly/current  → 今月+先月+次月のみ（軽量・高速）
GET /api/monthly/history  → 過去履歴（必要時のみロード）
```

---

## 2. 実装状況の詳細分析

### 2.1 `/api/monthly/current` の設計（計画書v2.1より）

#### 実装仕様

**ファイル**: `app/blueprints/monthly_current.py`（新規作成予定）

**エンドポイント**:
```python
@monthly_current_bp.route('/api/monthly/current', methods=['GET'])
@jwt_required()
def get_current_monthly_data():
    """
    計画書v2.0準拠: 今月+先月+次月の3ヶ月分を1回で返す
    目標: レスポンスタイム < 500ms
    """
```

#### 返却データ構造

```json
{
  "success": true,
  "current_month": "2025-10-01",
  "data": {
    "2025-09-01": {
      "target": {
        "projects": 5,
        "income": 200000
      },
      "stats": {
        "acquired_projects": 3,
        "completed_projects": 2,
        "sent_invoices_count": 4,
        "sent_invoices_amount": 180000,
        "paid_invoices_count": 2,
        "paid_invoices_amount": 150000
      }
    },
    "2025-10-01": { /* 今月のデータ */ },
    "2025-11-01": { /* 次月のデータ */ }
  }
}
```

#### 処理フロー

1. **3ヶ月分の計算**:
   ```python
   now = datetime.utcnow()
   current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
   last_month = (current_month - timedelta(days=1)).replace(day=1)
   next_month = (current_month + timedelta(days=32)).replace(day=1)
   
   months = [last_month, current_month, next_month]
   ```

2. **事前集計テーブルの活用**:
   ```python
   # 優先: MonthlySummaryテーブルから高速取得（50-200ms）
   summary = MonthlySummary.query.filter_by(
       user_id=user_id,
       summary_month=month
   ).first()
   
   if summary:
       # 事前集計データを使用（高速）
       stats = {
           'acquired_projects': summary.acquired_projects,
           ...
       }
   else:
       # フォールバック: リアルタイム計算（遅い）
       stats = calculate_monthly_stats_realtime(user_id, month)
   ```

3. **1回のAPIコールで完結**:
   - 目標データ（MonthlyTarget）
   - 統計データ（MonthlySummary または リアルタイム計算）
   - 3ヶ月分を一度に返却

### 2.2 `/api/monthly/history` の設計

#### 実装仕様（計画書v2.0より）

**エンドポイント**:
```
GET /api/monthly/history?limit=12
```

**用途**:
- ユーザーが「過去を見る」ボタンを押した時のみ呼び出される
- 過去12ヶ月分などの履歴データを返す

**レスポンス例**:
```json
{
  "success": true,
  "data": [
    {
      "month": "2025-01-01",
      "target": { "projects": 4, "income": 150000 },
      "actual": { ... },
      "achievement": { ... }
    },
    // ... 過去のデータ
  ]
}
```

---

## 3. API分離の戦略的メリット

### 3.1 パフォーマンス最適化

| 最適化レイヤー | 目標 | 実装方法 |
|-------------|------|---------|
| **Layer 1: データベース最適化** | 300ms以内 | ・事前集計テーブル（monthly_summary）<br>・適切なインデックス<br>・クエリ最適化 |
| **Layer 2: API最適化** | 200ms以内 | ・API分離（/current と /history）<br>・JSONレスポンス最小化<br>・不要なJOIN削減 |
| **Layer 3: フロントエンド最適化** | 500ms以内 | ・並列データ取得<br>・レンダリング最適化<br>・スケルトンスクリーン |

**合計目標**: **1000ms（1秒）以内**

### 3.2 従来のフローとの比較

#### 従来の処理フロー（遅い）
```
リクエスト → 履歴テーブル全検索 → 正負集計計算 → レスポンス
           [500-2000ms]
```

#### 改善後の処理フロー（高速）
```
リクエスト → 事前集計テーブル読み取り → レスポンス
           [50-200ms]
```

**削減効果**: **75-90%の高速化**

---

## 4. 現在の実装状況（調査レポートより）

### 4.1 実装状況の問題点

調査レポート（`api_performance_investigation_report.md`）によると：

| 項目 | 現状 | 問題点 |
|------|------|--------|
| **API分離** | 🔴 未実装 | `/api/monthly/current` が存在しない |
| **API呼び出し回数** | 🔴 4回以上 | 重複呼び出しが発生 |
| **レスポンスタイム** | 🔴 8.54秒 - 18.95秒 | 目標の500msを大幅に超過 |
| **Finish Time** | 🔴 33.64秒 | 目標の2秒を大幅に超過 |

### 4.2 重複API呼び出しの発生箇所

#### 問題1: 同じAPIの複数回呼び出し

**現在の動作**:
```
/api/monthly/current が 4回以上呼び出される
```

**発生原因**:
1. `MonthlyStatsSection.vue`の`onMounted`で呼び出し
2. `watch(() => props.currentTab)`で呼び出し
3. `loadData()`内で呼び出し
4. 重複実行防止フラグの不足

#### 問題2: APIエンドポイントの未分離

現在は以下のようなエンドポイントが使用されている可能性：
- `/api/monthly-targets/?year=2025&months=9`
- `/api/monthly-stats/{year}/{month}`

これらは個別に呼び出される必要があるため、API呼び出し回数が増加。

---

## 5. 結論と推奨事項

### 5.1 API分離の実装状況

**判定**: 🔴 **未実装**

計画書v2.0/v2.1で明確に定義されている `/api/monthly/current` と `/api/monthly/history` の分離は、現時点では実装されていません。

### 5.2 現在の問題点

1. **API分離が未実装**
   - `/api/monthly/current` エンドポイントが存在しない
   - 個別のAPIエンドポイント（targets, stats）を複数回呼び出している

2. **重複API呼び出し**
   - 同じエンドポイントが4回以上呼び出される
   - 重複実行防止フラグが不足

3. **パフォーマンス問題**
   - APIレスポンスタイムが8.54秒 - 18.95秒（目標: 500ms以内）
   - ページロード完了時間が33.64秒（目標: 2秒以内）

### 5.3 推奨される実装優先順位

#### 🔴 最優先（Phase 2）: API分離戦略の実装

**実装内容**:
1. `app/blueprints/monthly_current.py` の新規作成
2. `/api/monthly/current` エンドポイントの実装
3. 3ヶ月分のデータ（先月・今月・来月）を1回で返却
4. 事前集計テーブル（MonthlySummary）の活用

**期待効果**:
- API呼び出し回数: 4回以上 → **1回**（75%削減）
- APIレスポンスタイム: 8.54秒 → **< 500ms**（95%改善）

#### 🔴 最優先（Phase 1）: 重複実行防止フラグの追加

**実装内容**:
1. `monthlyStore`に`fetchingCurrentMonthlyData`フラグを追加
2. `fetchCurrentMonthlyData()`メソッドに重複実行防止機能を実装
3. `MonthlyStatsSection.vue`の初期化処理を最適化

**期待効果**:
- 重複API呼び出しの完全防止

---

## 6. 技術的補足

### 6.1 事前集計テーブルの役割

**MonthlySummaryテーブル**:
```sql
CREATE TABLE monthly_summary (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    summary_month DATE NOT NULL,
    acquired_projects INTEGER DEFAULT 0,
    completed_projects INTEGER DEFAULT 0,
    sent_invoices_count INTEGER DEFAULT 0,
    sent_invoices_amount NUMERIC(15,2) DEFAULT 0,
    paid_invoices_count INTEGER DEFAULT 0,
    paid_invoices_amount NUMERIC(15,2) DEFAULT 0,
    overdue_invoices_count INTEGER DEFAULT 0,
    overdue_invoices_amount NUMERIC(15,2) DEFAULT 0,
    last_updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, summary_month)
);
```

**更新タイミング**:
- ステータス変更時（Project/Invoice）に自動更新
- リアルタイムで集計データを保持

### 6.2 正負集計ロジックの厳守

計画書v2.0で定義された正負集計ロジックを厳守：

```python
# 獲得案件数 = (proposed→contracted) - (contracted→proposed)
acquired_projects = positive_changes - negative_changes

# 完了案件数 = (contracted→completed) - (completed→contracted)
completed_projects = positive_changes - negative_changes
```

### 6.3 会計ロジックの厳守

**含める**: `sent`, `paid`, `overdue` ステータスの請求書  
**含めない**: `draft`, `canceled` ステータスの請求書

---

## 7. まとめ

### 現況

**API分離の状況**: 🔴 **未分離**

現時点では、計画書v2.0/v2.1で定義されている `/api/monthly/current` と `/api/monthly/history` のAPI分離は実装されていません。

### 実装の必要性

計画書v2.0/v2.1に従い、以下の実装が急務です：

1. **`/api/monthly/current` エンドポイントの実装**
   - 3ヶ月分のデータを1回で返却
   - 事前集計テーブルの活用
   - レスポンスタイム < 500ms

2. **`/api/monthly/history` エンドポイントの実装**
   - 過去履歴データの返却
   - 必要時のみロード

3. **重複実行防止機能の実装**
   - `fetchingCurrentMonthlyData` フラグの追加
   - 重複API呼び出しの完全防止

### 期待される効果

- **パフォーマンス**: 33.64秒 → < 2秒（94%改善）
- **API呼び出し回数**: 4回以上 → 1回（75%削減）
- **レスポンスタイム**: 8.54秒 → < 500ms（95%改善）

---

**調査者**: Claude (AI Assistant)  
**参照文書**: 
- `api_performance_investigation_report.md`
- `__月次管理機能実装_完全計画書_v2_20251030.md`
- `__月次管理機能実装_完全計画書_v2_1_20251030.md`

---

## 付録A: API構造の視覚的比較

### A.1 計画されているAPI構造（理想）

```
┌─────────────────────────────────────────────┐
│          Frontend (Vue.js)                  │
│                                             │
│  DashboardPage.vue                          │
│         ↓                                   │
│  MonthlyStatsSection.vue                    │
│         ↓                                   │
│  monthlyStore (Pinia)                       │
└─────────────────────────────────────────────┘
                    │
                    │ 1回のAPI呼び出し
                    ↓
┌─────────────────────────────────────────────┐
│     GET /api/monthly/current                │
│                                             │
│  返却データ:                                  │
│  {                                          │
│    "2025-09-01": { target, stats },         │
│    "2025-10-01": { target, stats },         │
│    "2025-11-01": { target, stats }          │
│  }                                          │
│                                             │
│  レスポンスタイム: < 500ms                    │
└─────────────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────┐
│         Backend (Flask)                     │
│                                             │
│  monthly_current_bp                         │
│         ↓                                   │
│  MonthlySummary テーブル（事前集計）          │
│  MonthlyTarget テーブル                      │
└─────────────────────────────────────────────┘
```

### A.2 現在のAPI構造（問題）

```
┌─────────────────────────────────────────────┐
│          Frontend (Vue.js)                  │
│                                             │
│  DashboardPage.vue                          │
│         ↓                                   │
│  MonthlyStatsSection.vue                    │
│    ├─ onMounted() → fetchCurrentMonthlyData()
│    ├─ watch(currentTab) → loadData()       │
│    └─ loadData() → fetchCurrentMonthlyData()│
│         ↓                                   │
│  monthlyStore (Pinia)                       │
└─────────────────────────────────────────────┘
         │           │           │         │
         │           │           │         │ 
         └───────────┴───────────┴─────────┘
                    │
              🔴 4回以上の重複呼び出し
                    │
                    ↓
┌─────────────────────────────────────────────┐
│  個別APIエンドポイント（推定）                 │
│                                             │
│  ❌ /api/monthly-targets/?year=2025&months=9│
│     レスポンスタイム: 16.29秒                 │
│                                             │
│  ❌ /api/monthly-stats/{year}/{month}       │
│     レスポンスタイム: 8.54秒 - 18.95秒       │
│                                             │
│  ⚠️ /api/monthly/current （未実装）          │
└─────────────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────┐
│         Backend (Flask)                     │
│                                             │
│  ❌ monthly_summary テーブル（未実装）        │
│  ✅ ProjectStatusHistory（履歴テーブル）      │
│  ✅ InvoiceStatusHistory（履歴テーブル）      │
│                                             │
│  🐌 リアルタイム計算（遅い）                  │
└─────────────────────────────────────────────┘
```

### A.3 パフォーマンス比較

```
理想のAPI構造（計画書v2.0/v2.1）:
┌──────────────────────────────────────┐
│ API呼び出し: 1回                      │
│ レスポンスタイム: < 500ms             │ ✅ 目標達成
│ 総ロード時間: < 1秒                   │
└──────────────────────────────────────┘

現在のAPI構造（実測値）:
┌──────────────────────────────────────┐
│ API呼び出し: 4回以上                  │
│ レスポンスタイム: 8.54秒 - 18.95秒    │ ❌ 目標の17-38倍
│ 総ロード時間: 33.64秒                 │ ❌ 目標の33倍
└──────────────────────────────────────┘

改善必要度: 🔴 緊急（94%の改善が必要）
```

---

## 付録B: 実装チェックリスト

### Phase 1: 重複防止（即効性あり）

- [ ] **Step 1-1**: `monthlyStore`に`fetchingCurrentMonthlyData`フラグを追加
- [ ] **Step 1-2**: `fetchCurrentMonthlyData()`に重複実行防止機能を実装
- [ ] **Step 1-3**: `MonthlyStatsSection.vue`の`onMounted`を最適化
- [ ] **Step 1-4**: `loadData()`内のキャッシュチェックを強化
- [ ] **テスト**: API呼び出しが1回のみになることを確認

**期待効果**: API呼び出し回数 4回以上 → 2回（50%削減）

### Phase 2: API分離（根本解決）

- [ ] **Step 2-1**: `app/blueprints/monthly_current.py`の新規作成
- [ ] **Step 2-2**: `/api/monthly/current`エンドポイントの実装
- [ ] **Step 2-3**: `monthly_summary`テーブルの作成（未実装の場合）
- [ ] **Step 2-4**: 事前集計ロジックの実装
- [ ] **Step 2-5**: フロントエンド側の`fetchCurrentMonthlyData()`を新APIに切り替え
- [ ] **テスト**: レスポンスタイムが500ms以内になることを確認

**期待効果**: 
- API呼び出し回数 2回 → **1回**（50%削減）
- レスポンスタイム 8.54秒 → **< 500ms**（95%改善）

### Phase 3: 履歴API実装（オプション）

- [ ] **Step 3-1**: `/api/monthly/history`エンドポイントの実装
- [ ] **Step 3-2**: 過去データ取得UIの実装
- [ ] **テスト**: 過去12ヶ月分のデータが取得できることを確認

---

## 付録C: 検証方法

### C.1 API呼び出し回数の確認

```bash
# Chrome DevTools → Network タブで確認
1. ページをリロード
2. "monthly" または "current" でフィルタ
3. 同じエンドポイントが何回呼ばれているか確認

目標: 各エンドポイント 1回のみ
```

### C.2 レスポンスタイムの測定

```bash
# curl コマンドでAPIのレスポンスタイムを測定
curl -w "\nTime: %{time_total}s\n" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.influberry.jp/api/monthly/current

目標: < 0.5秒（500ms）
```

### C.3 総ロード時間の測定

```bash
# Lighthouse または Chrome DevTools → Performance タブで確認
1. ページをリロード
2. "Finish" までの時間を確認

目標: < 2秒
```

---

**レポート作成日**: 2025年11月1日  
**最終更新**: 2025年11月1日  
**調査者**: Claude (AI Assistant)

