"""
Users Blueprint - ユーザー管理API
InfluBerry v2 - 認証統合済み設計
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash

from app.models.user import User
from app.models.project import Project
from app import db
from app.utils.db_optimizations import UserQueryOptimizer

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """ユーザープロフィール取得"""
    try:
        return jsonify({'user': current_user.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': 'プロフィール取得エラー'}), 500

@users_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """ユーザープロフィール更新"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'データが送信されていません'}), 400
        
        # 更新可能フィールド
        updatable_fields = ['username', 'influencer_name']
        updated = False
        
        for field in updatable_fields:
            if field in data:
                # ユーザー名重複チェック
                if field == 'username':
                    existing_user = User.query.filter(
                        User.username == data[field],
                        User.id != current_user.id
                    ).first()
                    if existing_user:
                        return jsonify({'error': 'このユーザー名は既に使用されています'}), 400
                
                setattr(current_user, field, data[field])
                updated = True
        
        if updated:
            current_user.updated_at = datetime.utcnow()
            db.session.commit()
            return jsonify({
                'message': 'プロフィールを更新しました',
                'user': current_user.to_dict()
            }), 200
        else:
            return jsonify({'error': '更新するデータがありません'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'プロフィール更新エラー'}), 500

@users_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """パスワード変更"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'データが送信されていません'}), 400
        
        # 必須フィールドチェック
        required_fields = ['current_password', 'new_password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field}は必須です'}), 400
        
        # 現在のパスワード確認
        if not current_user.check_password(data['current_password']):
            return jsonify({'error': '現在のパスワードが正しくありません'}), 401
        
        # 新しいパスワード設定
        if len(data['new_password']) < 6:
            return jsonify({'error': 'パスワードは6文字以上である必要があります'}), 400
        
        current_user.set_password(data['new_password'])
        current_user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'パスワードを変更しました'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'パスワード変更エラー'}), 500

@users_bp.route('/stats', methods=['GET'])
@login_required
def get_user_stats():
    """ユーザー統計情報"""
    try:
        user_id = current_user.id
        
        # プロジェクト統計
        user_data = UserQueryOptimizer.get_user_with_stats_optimized(user_id)
        if not user_data:
            return jsonify({'error': 'ユーザーが見つかりません'}), 404

        return jsonify(user_data['stats'])
        
    except Exception as e:
        return jsonify({'error': '統計情報取得エラー'}), 500

@users_bp.route('/settings', methods=['GET'])
@login_required
def get_user_settings():
    """ユーザー設定情報取得"""
    try:
        return jsonify({
            'settings': {
                'plan_type': current_user.plan_type,
                'email_notifications': True,  # 将来の設定項目
                'privacy_settings': {
                    'profile_public': False,
                    'stats_public': False
                },
                'account_status': 'active' if current_user.is_active else 'inactive'
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': '設定取得エラー'}), 500

@users_bp.route('/deactivate', methods=['POST'])
@login_required
def deactivate_account():
    """アカウント無効化（論理削除）"""
    try:
        data = request.get_json()
        if not data or not data.get('confirm'):
            return jsonify({'error': 'アカウント無効化の確認が必要です'}), 400
        
        # パスワード確認
        if not data.get('password') or not current_user.check_password(data['password']):
            return jsonify({'error': 'パスワードが正しくありません'}), 401
        
        # アカウント無効化
        current_user.is_active = False
        current_user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'アカウントを無効化しました'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'アカウント無効化エラー'}), 500