#!/usr/bin/env python3
"""
マイグレーション状態修正スクリプト
"""

from app import create_app, db
from flask_migrate import Migrate, current, stamp

def main():
    app = create_app()
    migrate = Migrate(app, db)
    
    with app.app_context():
        print("現在のマイグレーション状態を確認中...")
        try:
            current_rev = current()
            print(f"Current revision: {current_rev}")
        except Exception as e:
            print(f"Error getting current revision: {e}")
        
        print("マイグレーション状態を最新に設定中...")
        stamp('head')
        print("マイグレーション状態修正完了")

if __name__ == '__main__':
    main()
