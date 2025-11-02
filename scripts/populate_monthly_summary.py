#!/usr/bin/env python3
"""
月次サマリー初期データ投入スクリプト（本番環境用）
全ユーザーのデータを投入

作成日: 2025年11月2日
目的: monthly_summaryテーブルに既存履歴データから初期データを投入
"""

import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User
from app.models.monthly_summary import MonthlySummary
from app.models.project import Project
from app.models.invoice import Invoice
from app.models.project_status_history import ProjectStatusHistory
from app.models.invoice_status_history import InvoiceStatusHistory
from app.services.monthly_summary_updater import update_monthly_summary
from sqlalchemy import func
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = create_app()


def get_all_months_with_history(user_id):
    """
    ユーザーの履歴データから全ての月を取得
    
    Args:
        user_id (int): ユーザーID
        
    Returns:
        list: 日付オブジェクトのリスト（月初日）
    """
    months = set()
    
    with app.app_context():
        # プロジェクトステータス履歴から月を抽出
        project_months = db.session.query(
            func.distinct(func.date_trunc('month', ProjectStatusHistory.changed_at)).label('month')
        ).join(Project, ProjectStatusHistory.project_id == Project.id).filter(
            Project.user_id == user_id
        ).all()
        
        for (month,) in project_months:
            if month:
                months.add(month.replace(day=1))
        
        # 請求書ステータス履歴から月を抽出
        invoice_months = db.session.query(
            func.distinct(func.date_trunc('month', InvoiceStatusHistory.changed_at)).label('month')
        ).join(Invoice, InvoiceStatusHistory.invoice_id == Invoice.id).filter(
            Invoice.user_id == user_id
        ).all()
        
        for (month,) in invoice_months:
            if month:
                months.add(month.replace(day=1))
        
        # 過去24ヶ月も追加（履歴がない場合でも表示可能にする）
        current_date = datetime.utcnow()
        for i in range(24):
            month_date = (current_date - relativedelta(months=i)).replace(day=1)
            months.add(month_date)
    
    return sorted(months)


def populate_for_user(user_id):
    """
    指定ユーザーの月次サマリーを投入
    
    Args:
        user_id (int): ユーザーID
    """
    with app.app_context():
        print(f"\n🔧 user_id={user_id} のデータ投入開始")
        
        # 投入前のレコード数
        before = MonthlySummary.query.filter_by(user_id=user_id).count()
        print(f"投入前: {before} レコード")
        
        # 全ての月を取得
        months = get_all_months_with_history(user_id)
        print(f"対象月数: {len(months)}")
        
        success_count = 0
        error_count = 0
        
        # 各月のデータを投入
        for i, month in enumerate(months, 1):
            print(f"[{i}/{len(months)}] {month.strftime('%Y-%m')} を処理中...")
            try:
                update_monthly_summary(user_id, month)
                success_count += 1
            except Exception as e:
                print(f"  ⚠️ エラー: {e}")
                error_count += 1
                continue
        
        # 投入後のレコード数
        after = MonthlySummary.query.filter_by(user_id=user_id).count()
        print(f"投入後: {after} レコード")
        print(f"追加: {after - before} レコード")
        print(f"成功: {success_count}件, エラー: {error_count}件")
        
        # 最新3件を表示
        latest = MonthlySummary.query.filter_by(
            user_id=user_id
        ).order_by(
            MonthlySummary.summary_month.desc()
        ).limit(3).all()
        
        if latest:
            print("\n最新3件:")
            for s in latest:
                print(f"  {s.summary_month}: "
                      f"acquired={s.acquired_projects}, "
                      f"completed={s.completed_projects}, "
                      f"sent_amount={s.sent_invoices_amount}")


def populate_all_users():
    """
    全ユーザーの月次サマリーを投入
    """
    with app.app_context():
        users = User.query.all()
        total_users = len(users)
        
        print(f"\n{'='*60}")
        print(f"全ユーザーのデータ投入を開始します")
        print(f"対象ユーザー数: {total_users}")
        print(f"{'='*60}\n")
        
        total_success = 0
        total_errors = 0
        
        for i, user in enumerate(users, 1):
            print(f"\n{'='*60}")
            print(f"ユーザー {i}/{total_users}")
            print(f"ユーザーID: {user.id}")
            print(f"メール: {user.email}")
            print(f"{'='*60}")
            
            try:
                populate_for_user(user.id)
                total_success += 1
            except Exception as e:
                print(f"  ⚠️ ユーザー {user.id} の処理でエラー: {e}")
                total_errors += 1
                continue
        
        # 最終結果
        total_records = MonthlySummary.query.count()
        
        print(f"\n{'='*60}")
        print(f"========== 完了 ==========")
        print(f"全ユーザーのデータ投入完了")
        print(f"成功ユーザー: {total_success}/{total_users}")
        print(f"エラーユーザー: {total_errors}/{total_users}")
        print(f"投入されたレコード総数: {total_records}")
        print(f"{'='*60}\n")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='月次サマリー初期データ投入スクリプト')
    parser.add_argument('--user-id', type=int, help='特定ユーザーのみ投入（指定しない場合は全ユーザー）')
    args = parser.parse_args()
    
    if args.user_id:
        # 特定ユーザーのみ投入
        print(f"特定ユーザー（user_id={args.user_id}）のデータ投入を開始します")
        populate_for_user(args.user_id)
        print("\n✅ 完了！")
    else:
        # 全ユーザー投入
        populate_all_users()
        print("\n✅ 完了！")

