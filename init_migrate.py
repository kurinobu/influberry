#!/usr/bin/env python3
"""
マイグレーション初期化スクリプト
"""

from app import create_app, db
from flask_migrate import Migrate, init

def main():
    app = create_app()
    migrate = Migrate(app, db)
    
    with app.app_context():
        print("マイグレーション初期化中...")
        init()
        print("マイグレーション初期化完了")

if __name__ == '__main__':
    main()
