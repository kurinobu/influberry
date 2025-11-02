# app/blueprints/monthly.py
"""
InfluBerry Monthly Management Blueprint
月次目標管理API
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date
from app import db
from app.models.monthly_target import MonthlyTarget

monthly_bp = Blueprint('monthly', __name__, url_prefix='/api/monthly-targets')

@monthly_bp.route('', methods=['GET'])
@monthly_bp.route('/', methods=['GET'])
@login_required
def get_targets():
    """月次目標一覧取得"""
    try:
        user_id = current_user.id
        year = request.args.get('year', type=int)
        months_str = request.args.get('months', '')
        
        query = MonthlyTarget.query.filter_by(user_id=user_id)
        
        if year and months_str:
            months = [int(m) for m in months_str.split(',')]
            # 年月でフィルタリング
            from sqlalchemy import extract
            query = query.filter(
                extract('year', MonthlyTarget.target_month) == year,
                extract('month', MonthlyTarget.target_month).in_(months)
            )
        
        targets = query.order_by(MonthlyTarget.target_month.asc()).all()
        
        return jsonify({
            'success': True,
            'data': [target.to_dict() for target in targets]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'目標取得エラー: {str(e)}'
        }), 500

@monthly_bp.route('', methods=['POST'])
@monthly_bp.route('/', methods=['POST'])
@login_required
def save_target():
    """月次目標設定・更新（UPSERT）"""
    try:
        user_id = current_user.id
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'データが送信されていません'
            }), 400
        
        target_month = data.get('target_month')
        if not target_month:
            return jsonify({
                'success': False,
                'error': '対象月が指定されていません'
            }), 400
        
        # 対象月を日付オブジェクトに変換
        try:
            target_month_date = datetime.strptime(target_month, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'error': '対象月の形式が正しくありません（YYYY-MM-DD）'
            }), 400
        
        # UPSERT処理
        target = MonthlyTarget.query.filter_by(
            user_id=user_id,
            target_month=target_month_date
        ).first()
        
        if target:
            # 既存目標の更新
            target.target_projects = data.get('target_projects')
            target.target_income = data.get('target_income')
            target.updated_at = datetime.utcnow()
        else:
            # 新規目標の作成
            target = MonthlyTarget(
                user_id=user_id,
                target_month=target_month_date,
                target_projects=data.get('target_projects'),
                target_income=data.get('target_income')
            )
            db.session.add(target)
        
        db.session.commit()
        
        # 統計データの即座更新（トランザクション統一）
        try:
            from app.blueprints.monthly_stats import get_monthly_stats
            # 統計データを即座に更新
            stats_response = get_monthly_stats(target_month_date.year, target_month_date.month)
            print(f"統計データ更新完了: {target_month_date}")
        except Exception as e:
            print(f"統計データ更新エラー: {e}")
        
        return jsonify({
            'success': True,
            'message': '目標を設定しました',
            'data': target.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'目標設定エラー: {str(e)}'
        }), 500

@monthly_bp.route('/<target_month>', methods=['DELETE'])
@login_required
def delete_target(target_month):
    """特定月の目標削除"""
    try:
        user_id = current_user.id
        
        # 対象月を日付オブジェクトに変換
        try:
            target_month_date = datetime.strptime(target_month, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'error': '対象月の形式が正しくありません（YYYY-MM-DD）'
            }), 400
        
        target = MonthlyTarget.query.filter_by(
            user_id=user_id,
            target_month=target_month_date
        ).first()
        
        if not target:
            return jsonify({
                'success': False,
                'error': '目標が見つかりません'
            }), 404
        
        db.session.delete(target)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '目標を削除しました'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'目標削除エラー: {str(e)}'
        }), 500
