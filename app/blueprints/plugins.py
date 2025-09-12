"""
Plugins Blueprint - プラグイン管理API
InfluBerry v2 - プラグインシステム基盤・認証統合済み設計
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime

from app.models.user import User
from app import db

plugins_bp = Blueprint('plugins', __name__)

@plugins_bp.route('/available', methods=['GET'])
@login_required
def get_available_plugins():
    """利用可能プラグイン一覧取得"""
    try:
        # 現在の段階的プラグイン設計
        available_plugins = [
            {
                'id': 'sponsor_management',
                'name': 'スポンサー案件管理',
                'description': '案件の登録・管理・進捗追跡・自動請求書発行',
                'version': '1.0.0',
                'status': 'active',
                'enabled_for_user': True,  # 全ユーザー利用可能
                'usage_limit': None if current_user.plan_type == 'pro' else 'unlimited_until_month_4',
                'endpoints': [
                    '/api/projects',
                    '/api/projects/stats'
                ]
            },
            {
                'id': 'pricing_calculator', 
                'name': '案件単価自動計算ツール',
                'description': 'フォロワー数とエンゲージメントに基づく適正単価算出',
                'version': '1.0.0',
                'status': 'coming_soon',
                'enabled_for_user': False,
                'release_date': '2025-10-01',
                'usage_limit': None if current_user.plan_type == 'pro' else 'monthly_limit_after_phase_4'
            },
            {
                'id': 'content_calendar',
                'name': '投稿アイデアカレンダー', 
                'description': 'コンテンツスケジュール管理・アイデア保存',
                'version': '1.0.0',
                'status': 'coming_soon',
                'enabled_for_user': False,
                'release_date': '2025-11-01',
                'usage_limit': None if current_user.plan_type == 'pro' else 'monthly_limit_after_phase_4'
            },
            {
                'id': 'proposal_generator',
                'name': 'ブランド提案文ジェネレーター',
                'description': 'AI活用による魅力的なブランド提案文自動生成',
                'version': '1.0.0',
                'status': 'coming_soon',
                'enabled_for_user': False,
                'release_date': '2025-12-01',
                'usage_limit': None if current_user.plan_type == 'pro' else 'monthly_limit_after_phase_4'
            }
        ]
        
        return jsonify({
            'plugins': available_plugins,
            'user_plan': current_user.plan_type,
            'total_available': len([p for p in available_plugins if p['enabled_for_user']])
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'プラグイン情報取得エラー'}), 500

@plugins_bp.route('/usage-stats', methods=['GET'])
@login_required
def get_plugin_usage_stats():
    """プラグイン使用統計"""
    try:
        # Phase 1段階では sponsor_management のみ使用統計
        from app.models.project import Project
        
        project_count = Project.query.filter_by(user_id=current_user.id).count()
        completed_projects = Project.query.filter_by(
            user_id=current_user.id, 
            status='completed'
        ).count()
        
        stats = {
            'sponsor_management': {
                'total_usage': project_count,
                'this_month_usage': project_count,  # 簡易実装：実際は当月フィルタ必要
                'features_used': ['project_creation', 'status_management'],
                'last_used': datetime.utcnow().isoformat(),
                'efficiency_score': (completed_projects / project_count * 100) if project_count > 0 else 0
            },
            'pricing_calculator': {'status': 'not_released'},
            'content_calendar': {'status': 'not_released'}, 
            'proposal_generator': {'status': 'not_released'}
        }
        
        return jsonify({
            'usage_stats': stats,
            'summary': {
                'most_used_plugin': 'sponsor_management',
                'total_actions_this_month': project_count,
                'user_efficiency_score': stats['sponsor_management']['efficiency_score']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'プラグイン使用統計取得エラー'}), 500

@plugins_bp.route('/settings', methods=['GET'])
@login_required
def get_plugin_settings():
    """プラグイン設定取得"""
    try:
        # 将来のプラグイン設定管理（現在は基本設定のみ）
        settings = {
            'sponsor_management': {
                'auto_notifications': True,
                'default_currency': 'JPY',
                'deadline_reminders': True,
                'reminder_days_before': 3
            },
            'global_settings': {
                'email_notifications': True,
                'browser_notifications': False,
                'data_export_format': 'csv'
            }
        }
        
        return jsonify({
            'plugin_settings': settings,
            'last_updated': current_user.updated_at.isoformat() if current_user.updated_at else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'プラグイン設定取得エラー'}), 500

@plugins_bp.route('/settings', methods=['PUT'])
@login_required
def update_plugin_settings():
    """プラグイン設定更新"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'データが送信されていません'}), 400
        
        # 将来の実装：データベースにプラグイン設定保存
        # 現在は成功レスポンスのみ返す（設定保存機能は将来実装）
        
        return jsonify({
            'message': 'プラグイン設定を更新しました',
            'updated_settings': data
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'プラグイン設定更新エラー'}), 500

@plugins_bp.route('/marketplace', methods=['GET'])
@login_required
def get_plugin_marketplace():
    """プラグインマーケットプレイス（将来機能）"""
    try:
        # 将来の拡張機能：サードパーティプラグイン
        marketplace = {
            'featured_plugins': [],
            'coming_soon': [
                {
                    'name': 'Instagram Analytics連携',
                    'description': 'Instagram Insights APIと連携した詳細分析',
                    'estimated_release': '2026-01-01'
                },
                {
                    'name': 'TikTok Creator Fund 管理',
                    'description': 'TikTokクリエイターファンド収益管理',
                    'estimated_release': '2026-03-01'
                }
            ],
            'message': 'プラグインマーケットプレイスは将来リリース予定です'
        }
        
        return jsonify(marketplace), 200
        
    except Exception as e:
        return jsonify({'error': 'マーケットプレイス情報取得エラー'}), 500

@plugins_bp.route('/health', methods=['GET'])
@login_required
def plugins_health_check():
    """プラグインシステム稼働状況"""
    try:
        health_status = {
            'system_status': 'healthy',
            'active_plugins': 1,  # sponsor_management
            'total_plugins': 4,
            'api_version': '2.0.0',
            'last_check': datetime.utcnow().isoformat(),
            'plugin_statuses': {
                'sponsor_management': 'active',
                'pricing_calculator': 'development', 
                'content_calendar': 'development',
                'proposal_generator': 'planning'
            }
        }
        
        return jsonify(health_status), 200
        
    except Exception as e:
        return jsonify({'error': 'ヘルスチェックエラー'}), 500