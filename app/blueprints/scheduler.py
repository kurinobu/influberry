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

@scheduler_bp.route('/rotation-status', methods=['GET'])
@login_required
def get_rotation_status():
    """月次切り替え状態の取得"""
    try:
        from flask import current_app
        from app.models.monthly_snapshot import MonthlySnapshot
        from datetime import datetime, date
        
        if not hasattr(current_app, 'monthly_scheduler'):
            return jsonify({
                'success': False,
                'error': 'Monthly scheduler not initialized'
            }), 500
        
        # 現在の年月を取得
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        
        # 前月のスナップショットが存在するかチェック
        previous_month = current_month - 1 if current_month > 1 else 12
        previous_year = current_year if current_month > 1 else current_year - 1
        
        # Cookie認証に変更
        user_id = current_user.id
        
        # 前月のスナップショットをチェック
        snapshot = MonthlySnapshot.query.filter_by(
            user_id=user_id,
            snapshot_month=date(previous_year, previous_month, 1),
            snapshot_type='monthly'
        ).first()
        
        # 月次切り替え状態の判定
        rotation_completed = snapshot is not None
        
        # Step 2 Phase 4修正: 実際の月次切り替え日時を計算
        # スナップショットが存在する場合は、そのスナップショットの月の月初日（実際の月次切り替え日時）を使用
        if snapshot:
            # スナップショットの月の月初日（実際の月次切り替え日時）を使用
            snapshot_date = snapshot.snapshot_month  # date型（年-月-1）
            last_rotation_date = datetime.combine(snapshot_date, datetime.min.time())
        else:
            # スナップショットが存在しない場合は、現在月の月初日を計算
            last_rotation_date = datetime(current_year, current_month, 1)
        
        # 修正: フロントエンドが期待する形式に合わせる
        return jsonify({
            'success': True,
            'data': {
                'rotation_completed': rotation_completed,
                'snapshot_exists': snapshot is not None,
                'last_rotation_date': last_rotation_date.isoformat() if last_rotation_date else None,
                'current_month': current_month,
                'current_year': current_year
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'月次切り替え状態取得エラー: {str(e)}'
        }), 500

@scheduler_bp.route('/rotation-completed', methods=['POST'])
@login_required
def notify_rotation_completed():
    """月次切り替え完了の通知"""
    try:
        from flask import current_app
        from datetime import datetime
        
        # 月次切り替え完了の通知をログに記録
        logger = logging.getLogger(__name__)
        user_id = current_user.id
        logger.info(f"Monthly rotation completed notification for user {user_id}")
        
        return jsonify({
            'success': True,
            'message': '月次切り替え完了通知を送信しました',
            'data': {
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'月次切り替え完了通知エラー: {str(e)}'
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
