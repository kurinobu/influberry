## **環境構成の理解と対応方針**

---

## **1\. 現在の環境構成**

| 環境 | アプリサーバー | データベース | プラン |
| ----- | ----- | ----- | ----- |
| **ステージング** | Render Pro | Railway Hobby | 🟡 DB制約あり |
| **本番（main）** | Render Pro | Render Standard | 🟢 高性能 |

---

## **2\. スクリプト実行の必要性**

### **2.1 本番環境での実行判断**

**結論**: ✅ **本番環境でもスクリプト実行が必要です**

#### **理由**

1. **データの一貫性**

   * ステージングと本番は別のデータベース  
   * 本番環境のmonthly\_summaryテーブルも空の状態  
   * スクリプトを実行しないと、本番でも同じ問題が発生  
2. **ユーザー影響**

   * 本番ユーザーが月次ダッシュボードにアクセス  
   * APIが12秒かかる（事前集計テーブルが空）  
   * **ユーザー体験が著しく悪化**  
3. **データ投入のタイミング**

   * 本番環境には実際のユーザーデータが存在  
   * 履歴データから正確な月次サマリーを生成可能  
   * **今実行すれば、過去の全データを一括投入できる**

---

## **3\. 本番環境での実行計画**

### **3.1 実行前の確認事項**

\# 本番環境のRenderシェルに接続  
\# （Renderダッシュボードから接続）

\# 1\. 現在のデータ状況を確認  
psql $DATABASE\_URL \-c "SELECT COUNT(\*) FROM monthly\_summary;"

\# 2\. ユーザー数を確認  
psql $DATABASE\_URL \-c "SELECT COUNT(\*) FROM users;"

\# 3\. 履歴データの存在確認  
psql $DATABASE\_URL \-c "SELECT COUNT(\*) FROM project\_status\_history;"  
psql $DATABASE\_URL \-c "SELECT COUNT(\*) FROM invoice\_status\_history;"

### **3.2 スクリプトの修正版（全ユーザー対応）**

本番環境では**全ユーザー**のデータを投入する必要があります：

\#\!/usr/bin/env python3  
"""  
月次サマリー初期データ投入スクリプト（本番環境用）  
全ユーザーのデータを投入  
"""  
from app import create\_app, db  
from app.models import User, Project, Invoice, MonthlySummary  
from app.models import ProjectStatusHistory, InvoiceStatusHistory  
from app.services.monthly\_summary\_updater import update\_monthly\_summary  
from sqlalchemy import func  
from datetime import datetime  
from dateutil.relativedelta import relativedelta

app \= create\_app()

def get\_all\_months\_with\_history(user\_id):  
    """ユーザーの履歴データから全ての月を取得"""  
    months \= set()  
    with app.app\_context():  
        project\_months \= db.session.query(  
            func.distinct(func.date\_trunc('month', ProjectStatusHistory.changed\_at)).label('month')  
        ).join(Project, ProjectStatusHistory.project\_id \== Project.id).filter(Project.user\_id \== user\_id).all()  
        for (month,) in project\_months:  
            if month:  
                months.add(month.replace(day=1))  
        invoice\_months \= db.session.query(  
            func.distinct(func.date\_trunc('month', InvoiceStatusHistory.changed\_at)).label('month')  
        ).join(Invoice, InvoiceStatusHistory.invoice\_id \== Invoice.id).filter(Invoice.user\_id \== user\_id).all()  
        for (month,) in invoice\_months:  
            if month:  
                months.add(month.replace(day=1))  
        current\_date \= datetime.utcnow()  
        for i in range(24):  
            month\_date \= (current\_date \- relativedelta(months=i)).replace(day=1)  
            months.add(month\_date)  
    return sorted(months)

def populate\_for\_user(user\_id):  
    """指定ユーザーの月次サマリーを投入"""  
    with app.app\_context():  
        print(f"\\nuser\_id={user\_id} のデータ投入開始")  
        before \= MonthlySummary.query.filter\_by(user\_id=user\_id).count()  
        print(f"投入前: {before} レコード")  
        months \= get\_all\_months\_with\_history(user\_id)  
        print(f"対象月数: {len(months)}")  
        success\_count \= 0  
        error\_count \= 0  
        for i, month in enumerate(months, 1):  
            print(f"\[{i}/{len(months)}\] {month.strftime('%Y-%m')} を処理中...")  
            try:  
                update\_monthly\_summary(user\_id, month)  
                success\_count \+= 1  
            except Exception as e:  
                print(f"エラー: {e}")  
                error\_count \+= 1  
        after \= MonthlySummary.query.filter\_by(user\_id=user\_id).count()  
        print(f"投入後: {after} レコード")  
        print(f"追加: {after \- before} レコード")

def populate\_all\_users():  
    """全ユーザーの月次サマリーを投入"""  
    with app.app\_context():  
        users \= User.query.all()  
        total\_users \= len(users)  
        print(f"\\n全ユーザーのデータ投入を開始します")  
        print(f"対象ユーザー数: {total\_users}")  
          
        for i, user in enumerate(users, 1):  
            print(f"\\n========== ユーザー {i}/{total\_users} \==========")  
            print(f"ユーザーID: {user.id}")  
            print(f"メール: {user.email}")  
            populate\_for\_user(user.id)  
          
        \# 最終結果  
        total\_records \= MonthlySummary.query.count()  
        print(f"\\n========== 完了 \==========")  
        print(f"全ユーザーのデータ投入完了")  
        print(f"投入されたレコード総数: {total\_records}")

if \_\_name\_\_ \== '\_\_main\_\_':  
    populate\_all\_users()

### **3.3 実行手順（本番環境）**

\# 1\. Renderダッシュボードで本番環境のシェルに接続

\# 2\. スクリプトを作成  
cat \> populate\_monthly\_summary\_production.py \<\< 'ENDOFFILE'  
\# 上記のスクリプト内容をコピー  
ENDOFFILE

\# 3\. 実行前に確認  
psql $DATABASE\_URL \-c "SELECT COUNT(\*) FROM monthly\_summary;"  
\# 期待: 0件

\# 4\. スクリプトを実行  
python populate\_monthly\_summary\_production.py

\# 5\. 実行後の確認  
psql $DATABASE\_URL \-c "SELECT COUNT(\*) FROM monthly\_summary;"  
psql $DATABASE\_URL \-c "SELECT user\_id, COUNT(\*) FROM monthly\_summary GROUP BY user\_id ORDER BY user\_id;"

---

## **4\. Railway Hobbyプランの制約**

### **4.1 ステージング環境が遅い理由**

**Railway Hobbyプランの制限**:

* 共有CPU（優先度低）  
* メモリ: 512MB-1GB  
* ネットワーク帯域幅: 制限あり  
* 同時接続数: 制限あり

**これが12秒のボトルネック**:

データベースクエリ実行: 0.055ms（高速）  
     ↓  
ネットワーク遅延: 11,000-12,000ms（遅い）← Railway Hobbyの制約  
     ↓  
API合計: 12,080ms

### **4.2 本番環境（Render Standard）の期待値**

**Render Standard DBの性能**:

* 専用リソース  
* 高速ネットワーク  
* 高い同時接続数

**期待されるレスポンス**:

データベースクエリ実行: 0.055ms  
ネットワーク遅延: 10-50ms（高速）  
API合計: 100-200ms（予想）

**判定**: 本番環境では、スクリプト実行後に**大幅な改善**が見込める

---

## **5\. 実行優先順位**

### **5.1 推奨実行順序**

#### **ステップ1: ステージング環境でフロントエンド修正を先に完了**

**理由**:

* ステージングは開発環境  
* フロントエンドの修正テストができる  
* 本番へのデプロイ前に動作確認

**実施内容**:

1. 旧API（overview, stats, targets）の削除  
2. `/api/monthly/current`のみを使用  
3. 重複実行防止フラグの実装  
4. タブ切り替えバグの修正

#### **ステップ2: 本番環境でスクリプト実行**

**タイミング**:

* フロントエンド修正が完了し、mainブランチにマージ後  
* 本番デプロイと同時、またはデプロイ直後

**理由**:

* フロントエンド修正 \+ データ投入で最大の効果  
* ユーザー影響を最小化  
* 一度の作業で完結

---

## **6\. 実行計画の提案**

### **Phase 1: ステージング環境（今すぐ）**

✅ **既に完了**:

* monthly\_summaryデータ投入済み（24件）

🔧 **次のアクション**:

* フロントエンド修正（旧API削除）  
* タブ切り替えバグ修正  
* 動作確認

### **Phase 2: 本番環境（フロントエンド修正完了後）**

#### **2-1: 準備**

\# 本番環境の現状確認  
psql $DATABASE\_URL \-c "SELECT COUNT(\*) FROM monthly\_summary;"  
psql $DATABASE\_URL \-c "SELECT COUNT(\*) FROM users;"

#### **2-2: スクリプト実行**

\# 全ユーザーのデータ投入  
python populate\_monthly\_summary\_production.py

**推定時間**:

* ユーザー数が10名の場合: 5-10分  
* ユーザー数が100名の場合: 30-60分

#### **2-3: 確認**

\# データ投入確認  
psql $DATABASE\_URL \-c "SELECT user\_id, COUNT(\*) FROM monthly\_summary GROUP BY user\_id ORDER BY user\_id;"

\# 本番ダッシュボードでテスト  
\# ブラウザで /dashboard にアクセス  
\# APIレスポンスタイムを確認

---

## **7\. リスク評価**

### **7.1 本番環境でのリスク**

| リスク | 影響度 | 対策 |
| ----- | ----- | ----- |
| **スクリプト実行中のエラー** | 🟡 中 | try-catchでエラーハンドリング実装済み |
| **実行時間が長い** | 🟡 中 | バックグラウンドで実行可能 |
| **既存データの上書き** | 🟢 低 | UPSERTロジックで安全 |
| **ユーザーへの影響** | 🟢 低 | データ投入中もサービス継続 |

### **7.2 実行しないリスク**

| リスク | 影響度 | 詳細 |
| ----- | ----- | ----- |
| **本番ユーザーの体験悪化** | 🔴 高 | APIが12秒かかり、使用不可 |
| **monthly\_summaryが空** | 🔴 高 | 事前集計の効果がゼロ |
| **リアルタイム計算に依存** | 🔴 高 | 毎回履歴テーブルを検索 |

**判定**: **実行しないリスクの方が高い**

---

## **8\. 結論と推奨アクション**

### **8.1 本番環境でのスクリプト実行**

**結論**: ✅ **必須**

### **8.2 実行タイミング**

**推奨**: フロントエンド修正完了後、本番デプロイと同時

### **8.3 実行順序**

1\. ステージング環境でフロントエンド修正  
   ↓  
2\. 動作確認・テスト  
   ↓  
3\. mainブランチにマージ  
   ↓  
4\. 本番デプロイ  
   ↓  
5\. 本番環境でスクリプト実行（全ユーザー）  
   ↓  
6\. 本番環境で動作確認

### **8.4 期待される改善効果**

#### **ステージング環境**

* 現状: 12.08秒  
* フロントエンド修正後: **3-5秒**（Railway Hobbyの制約あり）

#### **本番環境**

* 現状: 不明（おそらく10-15秒）  
* データ投入 \+ フロントエンド修正後: **100-500ms**（Render Standardの高性能）

---

## **9\. 次のアクション**

### **優先度1: フロントエンド修正（ステージング）**

指示があるまで実施しません。

### **優先度2: 本番環境スクリプト実行**

フロントエンド修正完了後に実施。

---

