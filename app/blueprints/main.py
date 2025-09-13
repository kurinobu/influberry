"""
Main Blueprint - メインページ・基本API
InfluBerry v2
"""

from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)



@main_bp.route('/api')
@main_bp.route('/api/')
def api_info():
    """API情報エンドポイント"""
    return jsonify({
        'api_version': '2.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'projects': '/api/projects',
            'dashboard': '/api/dashboard',
            'user-status': '/api/user-status',
            'health': '/health'
        },
        'authentication': 'Flask-Login (Session-based)'
    })

from flask_login import login_required, current_user

@main_bp.route('/api/dashboard')
@login_required
def dashboard_info():
    """認証済みユーザー向けダッシュボード情報"""
    return jsonify({
        'message': f'Welcome back, {current_user.influencer_name}!',
        'user_id': current_user.id,
        'plan_type': current_user.plan_type,
        'dashboard_data': {
            'available_features': ['project_management', 'analytics'],
            'user_status': 'active'
        }
    })

@main_bp.route('/api/user-status')
@login_required
def user_status():
    """認証済みユーザーのステータス確認"""
    from app.models.project import Project
    
    project_count = Project.query.filter_by(user_id=current_user.id).count()
    
    return jsonify({
        'user': current_user.to_dict(),
        'project_count': project_count,
        'last_activity': current_user.updated_at.isoformat() if current_user.updated_at else None
    })
@main_bp.route('/api/docs')
def api_documentation():
    """REST API仕様書"""
    return jsonify({
        'api_version': '1.0',
        'authentication': 'Cookie-based (Flask-Login)',
        'base_url': 'http://127.0.0.1:5001',
        'endpoints': {
            'auth': '/api/auth/*',
            'projects': '/api/projects/*', 
            'users': '/api/users/*',
            'plugins': '/api/plugins/*',
            'invoices': '/api/invoices/*'
        },
        'cors_enabled': True,
        'credentials_required': True
    })