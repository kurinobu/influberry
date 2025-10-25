# app/blueprints/scheduler.py
"""
Scheduler Management Blueprint
スケジューラー管理API
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime
import logging

scheduler_bp = Blueprint('scheduler', __name__, url_prefix='/api/scheduler')

@scheduler_bp.route('/status', methods=['GET'])
@login_required
def get_scheduler_status():
    """スケジューラーの状態取得"""
    try:
        from flask import current_app
        
        if not hasattr(current_app, 'monthly_scheduler'):
            return jsonify({
                'success': False,
                'error': 'Monthly scheduler not initialized'
            }), 500
        
        scheduler = current_app.monthly_scheduler
        status = scheduler.get_scheduler_status()
        
        return jsonify({
            'success': True,
            'data': status
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'スケジューラー状態取得エラー: {str(e)}'
        }), 500

@scheduler_bp.route('/trigger-rotation', methods=['POST'])
@login_required
def trigger_manual_rotation():
    """手動で月次切り替えを実行"""
    try:
        from flask import current_app
        
        if not hasattr(current_app, 'monthly_scheduler'):
            return jsonify({
                'success': False,
                'error': 'Monthly scheduler not initialized'
            }), 500
        
        scheduler = current_app.monthly_scheduler
        success = scheduler.trigger_manual_rotation()
        
        if success:
            return jsonify({
                'success': True,
                'message': '月次切り替えを手動実行しました'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': '月次切り替えの実行に失敗しました'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'手動月次切り替えエラー: {str(e)}'
        }), 500

@scheduler_bp.route('/test-snapshot', methods=['POST'])
@login_required
def test_snapshot_creation():
    """スナップショット作成のテスト"""
    try:
        from flask import current_app
        from app.models.monthly_snapshot import MonthlySnapshot
        from app.models.monthly_target import MonthlyTarget
        from app.blueprints.monthly_stats import get_monthly_stats
        from app import db
        from datetime import datetime
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'データが送信されていません'
            }), 400
        
        year = data.get('year')
        month = data.get('month')
        
        if not year or not month:
            return jsonify({
                'success': False,
                'error': '年月が指定されていません'
            }), 400
        
        user_id = current_user.id
        
        # 統計データを取得
        try:
            stats_response = get_monthly_stats(year, month)
            if stats_response[1] != 200:
                return jsonify({
                    'success': False,
                    'error': '統計データの取得に失敗しました'
                }), 500
            
            stats_data = stats_response[0].get_json()['data']
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'統計データ取得エラー: {str(e)}'
            }), 500
        
        # 目標データを取得
        target_date = datetime(year, month, 1).date()
        target = MonthlyTarget.query.filter_by(
            user_id=user_id,
            target_month=target_date
        ).first()
        
        targets_data = {
            'target_projects': target.target_projects if target else None,
            'target_income': target.target_income if target else None,
            'target_month': target_date.isoformat() if target else None
        }
        
        # スナップショット作成
        snapshot = MonthlySnapshot.create_snapshot(
            user_id=user_id,
            year=year,
            month=month,
            stats_data=stats_data,
            targets_data=targets_data
        )
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'テストスナップショットを作成しました',
            'data': snapshot.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'テストスナップショット作成エラー: {str(e)}'
        }), 500
