#!/usr/bin/env python3
"""
月次管理機能用マイグレーション作成・実行スクリプト
"""

from app import create_app, db
from flask_migrate import Migrate, revision, upgrade

def main():
    app = create_app()
    migrate = Migrate(app, db)
    
    with app.app_context():
        print("月次管理機能用マイグレーション作成中...")
        revision(message='Add monthly management tables')
        print("マイグレーション作成完了")
        
        print("マイグレーション実行中...")
        upgrade()
        print("マイグレーション実行完了")

if __name__ == '__main__':
    main()
