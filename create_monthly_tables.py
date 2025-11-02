#!/usr/bin/env python3
"""
月次管理機能用テーブル直接作成スクリプト
"""

from app import create_app, db
from app.models.monthly_target import MonthlyTarget
from app.models.project_status_history import ProjectStatusHistory
from app.models.invoice_status_history import InvoiceStatusHistory

def main():
    app = create_app()
    
    with app.app_context():
        print("月次管理機能用テーブル作成中...")
        
        # テーブル作成
        db.create_all()
        
        print("テーブル作成完了")
        
        # テーブル存在確認
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        monthly_tables = [t for t in tables if 'monthly' in t or 'history' in t]
        print(f"作成されたテーブル: {monthly_tables}")
        
        if 'monthly_targets' in tables:
            print("✅ monthly_targets テーブル作成成功")
        else:
            print("❌ monthly_targets テーブル作成失敗")
            
        if 'project_status_history' in tables:
            print("✅ project_status_history テーブル作成成功")
        else:
            print("❌ project_status_history テーブル作成失敗")
            
        if 'invoice_status_history' in tables:
            print("✅ invoice_status_history テーブル作成成功")
        else:
            print("❌ invoice_status_history テーブル作成失敗")

if __name__ == '__main__':
    main()
