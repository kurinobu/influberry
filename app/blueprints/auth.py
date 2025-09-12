"""
Authentication Blueprint - Flask-Login認証
InfluBerry v2
"""

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """ユーザーログイン（Flask-Login）"""
    try:
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'メールアドレスとパスワードが必要です'}), 400
        
        # User モデルをインポート
        from app.models.user import User
        
        # ユーザー認証処理
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.is_active and user.check_password(data['password']):
            login_user(user, remember=data.get('remember', False))
            return jsonify({
                'message': 'ログイン成功',
                'user': user.to_dict()
            }), 200
        
        return jsonify({'error': 'メールアドレスまたはパスワードが正しくありません'}), 401
        
    except Exception as e:
        return jsonify({'error': 'ログイン処理エラー'}), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """ユーザーログアウト"""
    try:
        logout_user()
        return jsonify({'message': 'ログアウトしました'}), 200
    except Exception as e:
        return jsonify({'error': 'ログアウト処理エラー'}), 500

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """現在のユーザー情報取得"""
    if current_user.is_authenticated:
        return jsonify({'user': current_user.to_dict()}), 200
    return jsonify({'error': 'ユーザーが認証されていません'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    """新規ユーザー登録"""
    try:
        data = request.get_json()
        
        # 必須フィールドバリデーション
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data or not data.get(field):
                return jsonify({'error': f'{field}は必須項目です'}), 400
        
        # User モデルをインポート
        from app.models.user import User
        
        # 重複チェック（email）
        existing_user_email = User.query.filter_by(email=data['email']).first()
        if existing_user_email:
            return jsonify({'error': 'このメールアドレスは既に登録されています'}), 409
        
        # 重複チェック（username）
        existing_user_username = User.query.filter_by(username=data['username']).first()
        if existing_user_username:
            return jsonify({'error': 'このユーザー名は既に使用されています'}), 409
        
        # 新規ユーザー作成（User.create()クラスメソッド活用）
        user = User.create(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            influencer_name=None
        )
        
        # 自動ログイン
        login_user(user, remember=False)
        
        return jsonify({
            'message': '新規登録が完了しました',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': '新規登録処理エラー'}), 500

@auth_bp.route('/test', methods=['GET'])
def auth_test():
    """認証システムテスト"""
    return jsonify({
        'message': 'Flask-Login認証システムテスト',
        'authenticated': current_user.is_authenticated,
        'user_id': current_user.get_id() if current_user.is_authenticated else None
    }), 200
