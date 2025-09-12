"""
Projects Blueprint - Project管理CRUD API
InfluBerry v2 - スポンサー案件管理システム
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date
from decimal import Decimal, InvalidOperation

from app.models.project import Project
from app import db
from app.utils.db_optimizations import ProjectQueryOptimizer
from app.utils.security_validators import SecurityDecorator, ProjectValidator

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('', methods=['POST'])
@projects_bp.route('/', methods=['POST'])
@SecurityDecorator.validate_json_request(
    required_fields=['company_name', 'amount', 'deadline', 'description'],
    optional_fields=['project_name', 'notes', 'status']
)
@SecurityDecorator.rate_limit_basic(max_requests=10, window_seconds=60)
@login_required
def create_project():
    """新規プロジェクト作成"""
    try:
        data = request.get_json()
        
        # セキュリティ強化されたバリデーション
        validated_data, validation_errors = ProjectValidator.validate_project_data(data)
        if validation_errors:
            return jsonify({'error': validation_errors[0]}), 400
        
        # 新規プロジェクト作成
        project = Project(
            user_id=current_user.id,
            company_name=validated_data['company_name'],
            amount=validated_data['amount'],
            deadline=validated_data['deadline'],
            description=validated_data['description'],
            project_name=validated_data.get('project_name', ''),
            notes=validated_data.get('notes', ''),
            status=data.get('status', 'proposed')
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'message': 'プロジェクトを作成しました',
            'project': project.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'プロジェクト作成エラー'}), 500

@projects_bp.route('', methods=['GET'])
@projects_bp.route('/', methods=['GET'])
@login_required
def get_projects():
    """プロジェクト一覧取得"""
    try:  # 一時的にコメントアウト - デバッグ用
        # クエリパラメータ処理
        status = request.args.get('status')
        if status == '':  # 空文字をNoneに変換
            status = None
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # sort_by, order パラメータは無視（ProjectQueryOptimizerで固定順序）
        
        # 最適化されたクエリを使用
        pagination = ProjectQueryOptimizer.get_user_projects_optimized(
            user_id=current_user.id,
            status=status,
            page=page,
            per_page=per_page
        )
        # pagination.itemsを直接使用（変数代入を削除）
        
        return jsonify({
            'projects': [project.to_dict() for project in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:  # 一時的にコメントアウト - デバッグ用
        return jsonify({'error': 'プロジェクト一覧取得エラー'}), 500

@projects_bp.route('/<int:project_id>', methods=['GET'])
@login_required
def get_project(project_id):
    """プロジェクト詳細取得"""
    try:
        project = Project.query.filter_by(
            id=project_id, 
            user_id=current_user.id
        ).first()
        
        if not project:
            return jsonify({'error': 'プロジェクトが見つかりません'}), 404
        
        return jsonify({'project': project.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'プロジェクト取得エラー'}), 500

@projects_bp.route('/<int:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
    """プロジェクト更新"""
    try:
        project = Project.query.filter_by(
            id=project_id, 
            user_id=current_user.id
        ).first()
        
        if not project:
            return jsonify({'error': 'プロジェクトが見つかりません'}), 404
        
        if not project.can_edit():
            return jsonify({'error': '完了済みプロジェクトは編集できません'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'データが送信されていません'}), 400
        
        # 更新可能フィールド
        if 'company_name' in data:
            project.company_name = data['company_name']
        
        if 'amount' in data:
            try:
                amount = Decimal(str(data['amount']))
                if amount <= 0:
                    return jsonify({'error': '金額は0より大きい値である必要があります'}), 400
                project.amount = amount
            except (InvalidOperation, ValueError):
                return jsonify({'error': '金額が無効な形式です'}), 400
        
        if 'deadline' in data:
            try:
                project.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': '納期の形式が正しくありません（YYYY-MM-DD）'}), 400
        
        if 'description' in data:
            project.description = data['description']

        if 'project_name' in data:
            project.project_name = data['project_name']
        
        if 'notes' in data:
            project.notes = data['notes']
        
        if 'status' in data:
            try:
                project.update_status(data['status'])
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
        
        project.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'プロジェクトを更新しました',
            'project': project.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'プロジェクト更新エラー'}), 500

@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    """プロジェクト削除"""
    try:
        project = Project.query.filter_by(
            id=project_id, 
            user_id=current_user.id
        ).first()
        
        if not project:
            return jsonify({'error': 'プロジェクトが見つかりません'}), 404
        
        if not project.can_delete():
            return jsonify({'error': '提案中のプロジェクトのみ削除可能です'}), 403
        
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({'message': 'プロジェクトを削除しました'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'プロジェクト削除エラー'}), 500

@projects_bp.route('/stats', methods=['GET'])
@login_required
def get_project_stats():
    """プロジェクト統計情報"""
    try:
        user_id = current_user.id
        
        # 基本統計
        # 最適化された単一クエリで統計取得
        stats = ProjectQueryOptimizer.get_user_stats_optimized(user_id)
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': '統計情報取得エラー'}), 500