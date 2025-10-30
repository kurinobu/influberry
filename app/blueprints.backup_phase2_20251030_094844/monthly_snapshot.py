# app/blueprints/monthly_snapshot.py
"""
InfluBerry Monthly Snapshot Blueprint
月次スナップショット管理API
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime, date
from app import db
from app.models.monthly_snapshot import MonthlySnapshot
from app.models.monthly_target import MonthlyTarget
from app.blueprints.monthly_stats import get_monthly_stats

monthly_snapshot_bp = Blueprint('monthly_snapshot', __name__, url_prefix='/api/monthly-snapshots')

@monthly_snapshot_bp.route('', methods=['POST'])
@monthly_snapshot_bp.route('/', methods=['POST'])
@login_required
def create_snapshot():
    """月次スナップショット作成"""
    try:
        user_id = current_user.id
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
        
        # 対象月の統計データを取得
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
        
        # 対象月の目標データを取得
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
            'message': 'スナップショットを作成しました',
            'data': snapshot.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'スナップショット作成エラー: {str(e)}'
        }), 500

@monthly_snapshot_bp.route('/<int:year>/<int:month>', methods=['GET'])
@login_required
def get_snapshot(year, month):
    """指定月のスナップショット取得"""
    try:
        user_id = current_user.id
        
        snapshot = MonthlySnapshot.get_by_user_and_month(user_id, year, month)
        
        if not snapshot:
            return jsonify({
                'success': False,
                'error': 'スナップショットが見つかりません'
            }), 404
        
        return jsonify({
            'success': True,
            'data': snapshot.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'スナップショット取得エラー: {str(e)}'
        }), 500

@monthly_snapshot_bp.route('/latest', methods=['GET'])
@login_required
def get_latest_snapshots():
    """最新のスナップショット一覧取得"""
    try:
        user_id = current_user.id
        limit = request.args.get('limit', 3, type=int)
        
        snapshots = MonthlySnapshot.get_latest_snapshots(user_id, limit)
        
        return jsonify({
            'success': True,
            'data': [snapshot.to_dict() for snapshot in snapshots]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'スナップショット一覧取得エラー: {str(e)}'
        }), 500

@monthly_snapshot_bp.route('/<int:year>/<int:month>', methods=['DELETE'])
@login_required
def delete_snapshot(year, month):
    """指定月のスナップショット削除"""
    try:
        user_id = current_user.id
        
        snapshot = MonthlySnapshot.get_by_user_and_month(user_id, year, month)
        
        if not snapshot:
            return jsonify({
                'success': False,
                'error': 'スナップショットが見つかりません'
            }), 404
        
        db.session.delete(snapshot)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'スナップショットを削除しました'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'スナップショット削除エラー: {str(e)}'
        }), 500

@monthly_snapshot_bp.route('/bulk-create', methods=['POST'])
@login_required
def bulk_create_snapshots():
    """複数月のスナップショット一括作成"""
    try:
        user_id = current_user.id
        data = request.get_json()
        
        if not data or 'months' not in data:
            return jsonify({
                'success': False,
                'error': '月のリストが指定されていません'
            }), 400
        
        months = data['months']
        created_snapshots = []
        
        for month_data in months:
            year = month_data.get('year')
            month = month_data.get('month')
            
            if not year or not month:
                continue
            
            # 既存のスナップショットをチェック
            existing = MonthlySnapshot.get_by_user_and_month(user_id, year, month)
            if existing:
                continue
            
            # 統計データを取得
            try:
                stats_response = get_monthly_stats(year, month)
                if stats_response[1] != 200:
                    continue
                
                stats_data = stats_response[0].get_json()['data']
            except:
                continue
            
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
            
            created_snapshots.append(snapshot.to_dict())
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(created_snapshots)}件のスナップショットを作成しました',
            'data': created_snapshots
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'一括スナップショット作成エラー: {str(e)}'
        }), 500
