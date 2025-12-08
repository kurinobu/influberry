# 最終解決策 - monthly_summary データ投入

**調査完了日時**: 2025年11月1日  
**根本原因**: `recalculate_all_monthly_summaries`が既存レコードしか再計算しない

---

## 🔴 **重大な問題を発見**

### `recalculate_all_monthly_summaries`の実装

```python
def recalculate_all_monthly_summaries(user_id):
    """
    指定ユーザーの全月次サマリーを再計算
    データ整合性チェック用
    """
    # ユーザーの全月次サマリーを取得
    summaries = MonthlySummary.query.filter_by(user_id=user_id).all()  # ← 問題！
    
    for summary in summaries:
        changed_month = datetime.combine(summary.summary_month, datetime.min.time())
        update_monthly_summary(user_id, changed_month)
```

**問題点**: 
- `MonthlySummary.query.filter_by(user_id=user_id).all()` は**既存レコードのみ**を取得
- monthly_summaryテーブルが空（0件）なので、**何もループしない**
- 結果: データが1件も投入されない

**判定**: この関数は**既存データの再計算用**であり、**初期データ投入には使えない**

---

## 🎯 解決策: 履歴から全期間のデータを投入

### 方法1: Flaskシェルで直接実行（推奨）

```bash
flask shell
```

```python
from app import db
from app.models import User, ProjectStatusHistory, InvoiceStatusHistory
from app.services.monthly_summary_updater import update_monthly_summary
from datetime import datetime
from dateutil.relativedelta import relativedelta

# user_id=2のユーザーを対象
user_id = 2

# 履歴データから月次を抽出
def get_all_months_with_history(user_id):
    """ユーザーの履歴データから全ての月を取得"""
    months = set()
    
    # Projectステータス変更履歴から月を取得
    project_months = db.session.query(
        func.distinct(
            func.date_trunc('month', ProjectStatusHistory.changed_at)
        ).label('month')
    ).join(
        Project, ProjectStatusHistory.project_id == Project.id
    ).filter(
        Project.user_id == user_id
    ).all()
    
    for (month,) in project_months:
        if month:
            months.add(month.replace(day=1))
    
    # Invoiceステータス変更履歴から月を取得
    invoice_months = db.session.query(
        func.distinct(
            func.date_trunc('month', InvoiceStatusHistory.changed_at)
        ).label('month')
    ).join(
        Invoice, InvoiceStatusHistory.invoice_id == Invoice.id
    ).filter(
        Invoice.user_id == user_id
    ).all()
    
    for (month,) in invoice_months:
        if month:
            months.add(month.replace(day=1))
    
    # 過去24ヶ月を追加（データがない月も含める）
    current_date = datetime.utcnow()
    for i in range(24):
        month_date = (current_date - relativedelta(months=i)).replace(day=1)
        months.add(month_date)
    
    return sorted(months)

# 全ての月に対してデータを投入
months = get_all_months_with_history(user_id)
print(f"対象月数: {len(months)}")

for i, month in enumerate(months, 1):
    print(f"[{i}/{len(months)}] {month.strftime('%Y-%m')} を処理中...")
    try:
        update_monthly_summary(user_id, month)
    except Exception as e:
        print(f"  ⚠️ エラー: {e}")
        continue

print("✅ 完了！")

# データ確認
from app.models import MonthlySummary
count = MonthlySummary.query.filter_by(user_id=user_id).count()
print(f"\n投入されたレコード数: {count}")

# 最新3件を表示
latest = MonthlySummary.query.filter_by(
    user_id=user_id
).order_by(
    MonthlySummary.summary_month.desc()
).limit(3).all()

print("\n最新3件:")
for s in latest:
    print(f"  {s.summary_month}: "
          f"acquired={s.acquired_projects}, "
          f"completed={s.completed_projects}, "
          f"sent_amount={s.sent_invoices_amount}")
```

### 方法2: スクリプトファイルを作成して実行

```bash
# スクリプトを作成
cat > populate_monthly_summary.py << 'SCRIPT'
#!/usr/bin/env python3
"""
月次サマリー初期データ投入スクリプト
"""
from app import create_app, db
from app.models import User, Project, Invoice, MonthlySummary
from app.models import ProjectStatusHistory, InvoiceStatusHistory
from app.services.monthly_summary_updater import update_monthly_summary
from sqlalchemy import func
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = create_app()

def get_all_months_with_history(user_id):
    """ユーザーの履歴データから全ての月を取得"""
    months = set()
    
    with app.app_context():
        # Projectステータス変更履歴から月を取得
        project_months = db.session.query(
            func.distinct(
                func.date_trunc('month', ProjectStatusHistory.changed_at)
            ).label('month')
        ).join(
            Project, ProjectStatusHistory.project_id == Project.id
        ).filter(
            Project.user_id == user_id
        ).all()
        
        for (month,) in project_months:
            if month:
                months.add(month.replace(day=1))
        
        # Invoiceステータス変更履歴から月を取得
        invoice_months = db.session.query(
            func.distinct(
                func.date_trunc('month', InvoiceStatusHistory.changed_at)
            ).label('month')
        ).join(
            Invoice, InvoiceStatusHistory.invoice_id == Invoice.id
        ).filter(
            Invoice.user_id == user_id
        ).all()
        
        for (month,) in invoice_months:
            if month:
                months.add(month.replace(day=1))
        
        # 過去24ヶ月を追加
        current_date = datetime.utcnow()
        for i in range(24):
            month_date = (current_date - relativedelta(months=i)).replace(day=1)
            months.add(month_date)
    
    return sorted(months)

def populate_for_user(user_id):
    """指定ユーザーの月次サマリーを投入"""
    with app.app_context():
        print(f"\n🔧 user_id={user_id} のデータ投入開始")
        
        # 投入前のレコード数
        before = MonthlySummary.query.filter_by(user_id=user_id).count()
        print(f"投入前: {before} レコード")
        
        # 全ての月を取得
        months = get_all_months_with_history(user_id)
        print(f"対象月数: {len(months)}")
        
        # 各月のデータを投入
        for i, month in enumerate(months, 1):
            print(f"[{i}/{len(months)}] {month.strftime('%Y-%m')} を処理中...")
            try:
                update_monthly_summary(user_id, month)
            except Exception as e:
                print(f"  ⚠️ エラー: {e}")
                continue
        
        # 投入後のレコード数
        after = MonthlySummary.query.filter_by(user_id=user_id).count()
        print(f"投入後: {after} レコード")
        print(f"追加: {after - before} レコード")
        
        # 最新3件を表示
        latest = MonthlySummary.query.filter_by(
            user_id=user_id
        ).order_by(
            MonthlySummary.summary_month.desc()
        ).limit(3).all()
        
        print("\n最新3件:")
        for s in latest:
            print(f"  {s.summary_month}: "
                  f"acquired={s.acquired_projects}, "
                  f"completed={s.completed_projects}, "
                  f"sent_amount={s.sent_invoices_amount}")

if __name__ == '__main__':
    # user_id=2のデータを投入
    populate_for_user(2)
    
    # 全ユーザーのデータを投入する場合
    # with app.app_context():
    #     users = User.query.all()
    #     for user in users:
    #         populate_for_user(user.id)
    
    print("\n✅ 完了！")
SCRIPT

# 実行権限を付与
chmod +x populate_monthly_summary.py

# 実行
python populate_monthly_summary.py
```

---

## 📊 期待される結果

### データ投入後

```sql
-- PostgreSQLで確認
SELECT COUNT(*) FROM monthly_summary WHERE user_id = 2;
-- 期待: 10-24件（履歴データの期間による）

SELECT 
    summary_month,
    acquired_projects,
    completed_projects,
    sent_invoices_count,
    sent_invoices_amount,
    paid_invoices_count,
    paid_invoices_amount
FROM monthly_summary
WHERE user_id = 2
ORDER BY summary_month DESC
LIMIT 5;
```

### APIパフォーマンス

ブラウザでダッシュボードにアクセス:
- `/api/monthly/current`: **< 1秒**（現在14.83秒）
- Finish Time: **3-5秒**（現在22.50秒）

---

## 🔍 追加の最適化（オプション）

### 履歴テーブルのインデックス追加

データ投入後、さらなる高速化のためにインデックスを追加:

```sql
-- PostgreSQLで実行
psql $DATABASE_URL
```

```sql
-- project_status_historyテーブル
CREATE INDEX IF NOT EXISTS idx_psh_changed_at 
ON project_status_history(changed_at);

CREATE INDEX IF NOT EXISTS idx_psh_project_user 
ON project_status_history(project_id);

-- invoice_status_historyテーブル
CREATE INDEX IF NOT EXISTS idx_ish_changed_at 
ON invoice_status_history(changed_at);

CREATE INDEX IF NOT EXISTS idx_ish_invoice_user 
ON invoice_status_history(invoice_id);

-- インデックス確認
SELECT tablename, indexname
FROM pg_indexes
WHERE tablename IN ('project_status_history', 'invoice_status_history')
ORDER BY tablename, indexname;
```

---

## ⚠️ トラブルシューティング

### エラー1: `func`が見つからない

```python
# インポートを追加
from sqlalchemy import func
```

### エラー2: `relativedelta`が見つからない

```bash
# パッケージをインストール
pip install python-dateutil --break-system-packages
```

```python
# インポートを追加
from dateutil.relativedelta import relativedelta
```

### エラー3: 履歴データが存在しない

```python
# 履歴データを確認
from app.models import ProjectStatusHistory, InvoiceStatusHistory, Project, Invoice

# Projectの履歴を確認
project_count = db.session.query(
    func.count(ProjectStatusHistory.id)
).join(
    Project
).filter(
    Project.user_id == 2
).scalar()

print(f"Project履歴: {project_count} 件")

# Invoiceの履歴を確認
invoice_count = db.session.query(
    func.count(InvoiceStatusHistory.id)
).join(
    Invoice
).filter(
    Invoice.user_id == 2
).scalar()

print(f"Invoice履歴: {invoice_count} 件")

# 履歴が0件の場合は、テストデータを作成するか、
# 手動でステータス変更を実施する必要がある
```

---

## 📈 最終的な改善効果

### Phase 1完了後（データ投入）

| 指標 | 現状 | Phase 1後 | 改善率 |
|------|------|----------|--------|
| **APIレスポンス** | 14.83秒 | **< 1秒** | **93%改善** |
| **Finish Time** | 22.50秒 | **3-5秒** | **78-86%改善** |
| **monthly_summary件数** | 0件 | **10-24件** | ✅ |

### Phase 2完了後（フロントエンド修正 + インデックス追加）

| 指標 | Phase 1後 | Phase 2後 | 改善率 |
|------|----------|----------|--------|
| **APIレスポンス** | < 1秒 | **< 500ms** | **50%改善** |
| **Finish Time** | 3-5秒 | **< 2秒** | **50-70%改善** |
| **API呼び出し回数** | 4回 | **1回** | **75%削減** |

### 最終結果

- ✅ Finish Time: **< 2秒**（目標達成）
- ✅ APIレスポンス: **< 500ms**（目標達成）
- ✅ API呼び出し: **1回**（目標達成）
- ✅ ユーザー体験: **実用レベルに改善**

---

## 🚀 実行手順まとめ

### ステップ1: データ投入（15分）

```bash
# 方法A: Flaskシェルで実行（推奨）
flask shell
# 上記のPythonコードを実行

# 方法B: スクリプトで実行
python populate_monthly_summary.py
```

### ステップ2: 動作確認（5分）

```bash
# データベースで確認
psql $DATABASE_URL
SELECT COUNT(*) FROM monthly_summary WHERE user_id = 2;

# ブラウザで確認
# ダッシュボードにアクセス
# Chrome DevTools → Network タブでレスポンスタイム確認
```

### ステップ3: インデックス追加（オプション、10分）

```sql
-- 上記のCREATE INDEX文を実行
```

---

## 📝 次のフェーズ

データ投入が完了したら、以下を実施:

1. **フロントエンド修正**
   - 旧API（overview, stats, targets）の呼び出しを削除
   - `/api/monthly/current`のみを使用

2. **重複実行防止**
   - `fetchingCurrentMonthlyData`フラグの実装

3. **タブ切り替えの安定化**
   - 初期化時のタブ切り替えを1回に限定

---

**重要**: このスクリプトを実行すれば、**15分で93%のパフォーマンス改善**が見込めます！

