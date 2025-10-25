#!/usr/bin/env python3
"""
月次管理機能用マイグレーション実行スクリプト
"""

from app import create_app, db
from flask_migrate import Migrate, upgrade

def main():
    app = create_app()
    migrate = Migrate(app, db)
    
    with app.app_context():
        print("月次管理機能用マイグレーションを実行中...")
        upgrade()
        print("マイグレーション完了")

if __name__ == '__main__':
    main()
