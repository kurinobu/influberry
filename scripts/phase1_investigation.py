#!/usr/bin/env python3
"""
Phase 1: 現状調査・パフォーマンス測定スクリプト
月次管理機能の現状を調査し、計画書v2.0との差異を判定する
"""

import sys
import os
from datetime import datetime, date

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

from app import create_app, db
from app.models.monthly_summary import MonthlySummary
from app.models.monthly_target import MonthlyTarget
from app.models.project_status_history import ProjectStatusHistory
from app.models.invoice_status_history import InvoiceStatusHistory
from app.models.project import Project
from app.models.invoice import Invoice
from app.models.user import User
from sqlalchemy import func, extract
from datetime import datetime

app = create_app()

def check_monthly_summary_table():
    """monthly_summaryテーブルの状態を確認"""
    print("\n" + "="*80)
    print("📊 monthly_summary テーブル状態確認")
    print("="*80)
    
    with app.app_context():
        # テーブルの存在確認
        try:
            count = db.session.query(func.count(MonthlySummary.id)).scalar()
            print(f"✅ テーブル存在: {count} 件のレコードがあります")
            
            # 最新5件を表示
            summaries = MonthlySummary.query.order_by(
                MonthlySummary.last_updated_at.desc()
            ).limit(5).all()
            
            if summaries:
                print("\n📋 最新5件のレコード:")
                for s in summaries:
                    print(f"  - user_id={s.user_id}, month={s.summary_month}, "
                          f"acquired={s.acquired_projects}, completed={s.completed_projects}, "
                          f"sent={s.sent_invoices_count}, paid={s.paid_invoices_count}, "
                          f"updated={s.last_updated_at}")
            else:
                print("⚠️ レコードがありません（事前集計が実行されていない可能性）")
            
            # ユーザーごとの集計
            user_summary = db.session.query(
                MonthlySummary.user_id,
                func.count(MonthlySummary.id).label('count')
            ).group_by(MonthlySummary.user_id).all()
            
            if user_summary:
                print("\n👥 ユーザーごとの集計:")
                for user_id, count in user_summary:
                    print(f"  - user_id={user_id}: {count} 件の月次サマリー")
            
        except Exception as e:
            print(f"❌ テーブル確認エラー: {e}")
            return False
    
    return True

def check_monthly_targets_table():
    """monthly_targetsテーブルの状態を確認"""
    print("\n" + "="*80)
    print("🎯 monthly_targets テーブル状態確認")
    print("="*80)
    
    with app.app_context():
        try:
            count = db.session.query(func.count(MonthlyTarget.id)).scalar()
            print(f"✅ テーブル存在: {count} 件のレコードがあります")
            
            # 最新5件を表示
            targets = MonthlyTarget.query.order_by(
                MonthlyTarget.updated_at.desc()
            ).limit(5).all()
            
            if targets:
                print("\n📋 最新5件のレコード:")
                for t in targets:
                    print(f"  - user_id={t.user_id}, month={t.target_month}, "
                          f"projects={t.target_projects}, income={t.target_income}, "
                          f"updated={t.updated_at}")
            else:
                print("⚠️ レコードがありません")
                
        except Exception as e:
            print(f"❌ テーブル確認エラー: {e}")
            return False
    
    return True

def check_status_history_tables():
    """ステータス変更履歴テーブルの状態を確認"""
    print("\n" + "="*80)
    print("📝 ステータス変更履歴テーブル状態確認")
    print("="*80)
    
    with app.app_context():
        try:
            # project_status_history
            project_count = db.session.query(
                func.count(ProjectStatusHistory.id)
            ).scalar()
            print(f"✅ project_status_history: {project_count} 件のレコード")
            
            # invoice_status_history
            invoice_count = db.session.query(
                func.count(InvoiceStatusHistory.id)
            ).scalar()
            print(f"✅ invoice_status_history: {invoice_count} 件のレコード")
            
            # 最近の変更履歴
            recent_projects = ProjectStatusHistory.query.order_by(
                ProjectStatusHistory.changed_at.desc()
            ).limit(5).all()
            
            if recent_projects:
                print("\n📋 最近のプロジェクトステータス変更:")
                for p in recent_projects:
                    print(f"  - project_id={p.project_id}, "
                          f"{p.old_status} → {p.new_status}, "
                          f"changed_at={p.changed_at}")
            
            recent_invoices = InvoiceStatusHistory.query.order_by(
                InvoiceStatusHistory.changed_at.desc()
            ).limit(5).all()
            
            if recent_invoices:
                print("\n📋 最近の請求書ステータス変更:")
                for i in recent_invoices:
                    print(f"  - invoice_id={i.invoice_id}, "
                          f"{i.old_status} → {i.new_status}, "
                          f"changed_at={i.changed_at}")
                
        except Exception as e:
            print(f"❌ テーブル確認エラー: {e}")
            return False
    
    return True

def check_new_api_endpoint():
    """新APIエンドポイント(/api/monthly/current)の実装状況を確認"""
    print("\n" + "="*80)
    print("🔌 新APIエンドポイント (/api/monthly/current) 実装状況確認")
    print("="*80)
    
    try:
        from app.blueprints.monthly_current import monthly_current_bp
        
        # Blueprintが登録されているか確認
        routes = []
        for rule in app.url_map.iter_rules():
            if 'monthly' in rule.rule and 'current' in rule.rule:
                routes.append(rule.rule)
        
        if routes:
            print(f"✅ エンドポイント実装済み:")
            for route in routes:
                print(f"  - {route}")
        else:
            print("⚠️ エンドポイントが見つかりません（未登録の可能性）")
            
        # Blueprintの登録確認
        if monthly_current_bp in app.blueprints.values():
            print("✅ Blueprint登録済み")
        else:
            print("⚠️ Blueprint未登録の可能性")
            
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        return False
    except Exception as e:
        print(f"❌ 確認エラー: {e}")
        return False
    
    return True

def check_frontend_api_flag():
    """フロントエンドのAPI使用フラグを確認"""
    print("\n" + "="*80)
    print("🎨 フロントエンド API使用フラグ確認")
    print("="*80)
    
    try:
        monthly_js_path = "frontend/src/stores/monthly.js"
        if os.path.exists(monthly_js_path):
            with open(monthly_js_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if 'USE_NEW_API' in content:
                if 'USE_NEW_API: false' in content or "USE_NEW_API = false" in content:
                    print("⚠️ USE_NEW_API = false（新APIが無効化されています）")
                elif 'USE_NEW_API: true' in content or "USE_NEW_API = true" in content:
                    print("✅ USE_NEW_API = true（新APIが有効化されています）")
                else:
                    print("⚠️ USE_NEW_API フラグの値を特定できません")
                
                if 'fetchCurrentMonthlyData' in content:
                    print("✅ fetchCurrentMonthlyData() 関数実装済み")
                else:
                    print("⚠️ fetchCurrentMonthlyData() 関数が見つかりません")
            else:
                print("⚠️ USE_NEW_API フラグが見つかりません")
        else:
            print(f"❌ ファイルが見つかりません: {monthly_js_path}")
            return False
            
    except Exception as e:
        print(f"❌ 確認エラー: {e}")
        return False
    
    return True

def compare_with_plan():
    """計画書v2.0との差異を判定"""
    print("\n" + "="*80)
    print("📋 計画書v2.0との差異判定")
    print("="*80)
    
    differences = []
    
    with app.app_context():
        # 1. monthly_summary テーブルの存在確認
        try:
            count = db.session.query(func.count(MonthlySummary.id)).scalar()
            if count == 0:
                differences.append("❌ monthly_summary テーブルにデータがありません（初期データ生成が必要）")
            else:
                print("✅ monthly_summary テーブル: データあり")
        except:
            differences.append("❌ monthly_summary テーブルが存在しません")
        
        # 2. 新APIエンドポイントの確認
        try:
            from app.blueprints.monthly_current import monthly_current_bp
            routes = [rule.rule for rule in app.url_map.iter_rules() 
                     if 'monthly' in rule.rule and 'current' in rule.rule]
            if not routes:
                differences.append("⚠️ /api/monthly/current エンドポイントが登録されていません")
            else:
                print("✅ /api/monthly/current エンドポイント: 実装済み")
        except:
            differences.append("❌ /api/monthly/current エンドポイントが実装されていません")
        
        # 3. フロントエンドのAPI使用フラグ確認
        try:
            monthly_js_path = "frontend/src/stores/monthly.js"
            if os.path.exists(monthly_js_path):
                with open(monthly_js_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'USE_NEW_API: false' in content or "USE_NEW_API = false" in content:
                    differences.append("⚠️ USE_NEW_API = false（新APIが有効化されていません）")
            else:
                differences.append("❌ monthly.js が見つかりません")
        except:
            differences.append("❌ フロントエンドのAPI使用フラグを確認できません")
    
    if differences:
        print("\n📊 差異一覧:")
        for diff in differences:
            print(f"  {diff}")
    else:
        print("\n✅ 計画書v2.0との差異なし")
    
    return differences

def main():
    """メイン処理"""
    print("\n" + "="*80)
    print("🔍 Phase 1: 現状調査・パフォーマンス測定")
    print("="*80)
    print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # 各調査項目を実行
    results.append(("monthly_summary", check_monthly_summary_table()))
    results.append(("monthly_targets", check_monthly_targets_table()))
    results.append(("status_history", check_status_history_tables()))
    results.append(("new_api", check_new_api_endpoint()))
    results.append(("frontend_flag", check_frontend_api_flag()))
    
    # 計画書との差異判定
    differences = compare_with_plan()
    
    # 結果サマリー
    print("\n" + "="*80)
    print("📊 Phase 1 調査結果サマリー")
    print("="*80)
    
    success_count = sum(1 for _, result in results if result)
    print(f"✅ 成功: {success_count}/{len(results)} 項目")
    
    if differences:
        print(f"⚠️ 差異: {len(differences)} 件")
        print("\n📋 推奨アクション:")
        print("  1. monthly_summary テーブルにデータがない場合は初期データ生成を実行")
        print("  2. USE_NEW_API フラグを true に変更して新APIを有効化")
        print("  3. ブラウザでのパフォーマンス測定を実行")
    else:
        print("✅ 計画書v2.0との差異なし")
    
    print("\n" + "="*80)
    print("Phase 1 調査完了")
    print("="*80)

if __name__ == '__main__':
    main()


