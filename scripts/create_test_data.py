#!/usr/bin/env python3
"""
InfluBerry v2 - 包括的テストデータ投入スクリプト
作成日: 2025年9月5日
目的: データベース完全テスト・初期データ投入
"""

from datetime import datetime, date, timedelta
from decimal import Decimal
from app import create_app, db
from app.models import User, Project
from werkzeug.security import generate_password_hash

def create_test_data():
    """包括的テストデータを投入"""
    
    app = create_app()
    with app.app_context():
        
        print("=== InfluBerry v2 テストデータ投入開始 ===")
        
        # 既存データ確認
        existing_users = User.query.count()
        existing_projects = Project.query.count()
        print(f"投入前 - Users: {existing_users}, Projects: {existing_projects}")
        
        # テストユーザー作成（既存2名に追加で3名）
        test_users_data = [
            {
                'username': 'yui_kawaii',
                'email': 'yui@influberry.com',
                'password': 'testpass123',
                'influencer_name': 'ゆいちゃん',
                'plan_type': 'free',
                'is_active': True
            },
            {
                'username': 'miku_fashion',
                'email': 'miku@influberry.com', 
                'password': 'testpass123',
                'influencer_name': 'みくファッション',
                'plan_type': 'pro',
                'is_active': True
            },
            {
                'username': 'inactive_user',
                'email': 'inactive@influberry.com',
                'password': 'testpass123', 
                'influencer_name': '非アクティブユーザー',
                'plan_type': 'free',
                'is_active': False
            }
        ]
        
        # ユーザー投入
        created_users = []
        for user_data in test_users_data:
            # 既存確認
            if not User.query.filter_by(email=user_data['email']).first():
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    password_hash=generate_password_hash(user_data['password']),
                    influencer_name=user_data['influencer_name'],
                    plan_type=user_data['plan_type'],
                    is_active=user_data['is_active']
                )
                db.session.add(user)
                created_users.append(user_data['username'])
        
        db.session.commit()
        print(f"新規ユーザー作成: {len(created_users)}名 - {created_users}")
        
        # 全ユーザー取得（既存+新規）
        all_users = User.query.filter_by(is_active=True).all()
        user_ids = [user.id for user in all_users]
        
        print(f"テスト対象ユーザー: {len(all_users)}名 (IDs: {user_ids})")
        
        # テストプロジェクト作成
        test_projects_data = [
            # proposed ステータス（5件）
            {
                'company_name': 'コスメブランドA株式会社',
                'amount': Decimal('80000.00'),
                'deadline': date.today() + timedelta(days=30),
                'description': 'リップ新商品のInstagram投稿プロモーション',
                'status': 'proposed',
                'user_id': user_ids[0] if len(user_ids) > 0 else 1
            },
            {
                'company_name': 'ファッションブランドB',
                'amount': Decimal('120000.00'),
                'deadline': date.today() + timedelta(days=14),
                'description': '春夏コレクションのTikTok動画制作',
                'status': 'proposed',
                'user_id': user_ids[1] if len(user_ids) > 1 else 1
            },
            {
                'company_name': 'グルメ企業C',
                'amount': Decimal('45000.00'),
                'deadline': date.today() + timedelta(days=21),
                'description': 'カフェ新メニューのストーリー投稿',
                'status': 'proposed',
                'user_id': user_ids[0] if len(user_ids) > 0 else 1
            },
            {
                'company_name': 'アクセサリーショップD',
                'amount': Decimal('25000.00'),
                'deadline': date.today() + timedelta(days=45),
                'description': 'ピアス商品レビュー動画',
                'status': 'proposed',
                'user_id': user_ids[2] if len(user_ids) > 2 else 1
            },
            {
                'company_name': 'スキンケアブランドE',
                'amount': Decimal('200000.00'),
                'deadline': date.today() + timedelta(days=60),
                'description': '洗顔料1ヶ月使用レポート',
                'status': 'proposed',
                'user_id': user_ids[1] if len(user_ids) > 1 else 1
            },
            
            # contracted ステータス（5件）
            {
                'company_name': 'テクノロジー企業F',
                'amount': Decimal('350000.00'),
                'deadline': date.today() + timedelta(days=10),
                'description': 'スマホアプリのレビュー投稿',
                'status': 'contracted',
                'user_id': user_ids[0] if len(user_ids) > 0 else 1
            },
            {
                'company_name': 'ヘアケアブランドG',
                'amount': Decimal('90000.00'),
                'deadline': date.today() + timedelta(days=7),
                'description': 'シャンプー使用前後比較動画',
                'status': 'contracted',
                'user_id': user_ids[2] if len(user_ids) > 2 else 1
            },
            {
                'company_name': 'フィットネスジムH',
                'amount': Decimal('150000.00'),
                'deadline': date.today() + timedelta(days=20),
                'description': 'ワークアウト動画コラボ',
                'status': 'contracted',
                'user_id': user_ids[1] if len(user_ids) > 1 else 1
            },
            {
                'company_name': 'スイーツブランドI',
                'amount': Decimal('60000.00'),
                'deadline': date.today() + timedelta(days=5),
                'description': '新作ケーキの試食レビュー',
                'status': 'contracted',
                'user_id': user_ids[0] if len(user_ids) > 0 else 1
            },
            {
                'company_name': 'ファッション通販サイトJ',
                'amount': Decimal('180000.00'),
                'deadline': date.today() + timedelta(days=15),
                'description': '秋冬コーディネート提案',
                'status': 'contracted',
                'user_id': user_ids[2] if len(user_ids) > 2 else 1
            },
            
            # completed ステータス（5件）
            {
                'company_name': 'ネイルサロンK',
                'amount': Decimal('40000.00'),
                'deadline': date.today() - timedelta(days=5),
                'description': 'ネイルデザイン紹介動画',
                'status': 'completed',
                'user_id': user_ids[1] if len(user_ids) > 1 else 1
            },
            {
                'company_name': 'カフェチェーンL',
                'amount': Decimal('75000.00'),
                'deadline': date.today() - timedelta(days=10),
                'description': '期間限定ドリンクの紹介',
                'status': 'completed',
                'user_id': user_ids[0] if len(user_ids) > 0 else 1
            },
            {
                'company_name': 'ジュエリーブランドM',
                'amount': Decimal('250000.00'),
                'deadline': date.today() - timedelta(days=15),
                'description': 'ブライダルリング着用撮影',
                'status': 'completed',
                'user_id': user_ids[2] if len(user_ids) > 2 else 1
            },
            {
                'company_name': '書籍出版社N',
                'amount': Decimal('30000.00'),
                'deadline': date.today() - timedelta(days=20),
                'description': '話題の小説読書レビュー',
                'status': 'completed',
                'user_id': user_ids[1] if len(user_ids) > 1 else 1
            },
            {
                'company_name': 'ライフスタイルブランドO',
                'amount': Decimal('100000.00'),
                'deadline': date.today() - timedelta(days=30),
                'description': '雑貨商品のルームツアー',
                'status': 'completed',
                'user_id': user_ids[0] if len(user_ids) > 0 else 1
            }
        ]
        
        # プロジェクト投入
        created_projects = 0
        for project_data in test_projects_data:
            project = Project(
                user_id=project_data['user_id'],
                company_name=project_data['company_name'],
                amount=project_data['amount'],
                deadline=project_data['deadline'],
                description=project_data['description'],
                status=project_data['status']
            )
            db.session.add(project)
            created_projects += 1
        
        db.session.commit()
        print(f"新規プロジェクト作成: {created_projects}件")
        
        # 投入後の状況確認
        final_users = User.query.count()
        final_projects = Project.query.count()
        print(f"投入後 - Users: {final_users}, Projects: {final_projects}")
        
        # ステータス別統計
        print("\n=== プロジェクトステータス別統計 ===")
        for status in ['proposed', 'contracted', 'completed']:
            count = Project.query.filter_by(status=status).count()
            print(f"{status}: {count}件")
        
        # ユーザー別統計
        print("\n=== ユーザー別プロジェクト数 ===")
        for user in User.query.filter_by(is_active=True).all():
            project_count = Project.query.filter_by(user_id=user.id).count()
            print(f"{user.username} ({user.influencer_name}): {project_count}件")
        
        print("\n=== テストデータ投入完了 ===")
        return True

if __name__ == "__main__":
    create_test_data()