#!/usr/bin/env python3
"""
マイグレーション実行スクリプト
"""

from app import create_app, db
from flask_migrate import Migrate, upgrade

def main():
    app = create_app()
    migrate = Migrate(app, db)
    
    with app.app_context():
        print("マイグレーション実行中...")
        upgrade()
        print("マイグレーション実行完了")

if __name__ == '__main__':
    main()
