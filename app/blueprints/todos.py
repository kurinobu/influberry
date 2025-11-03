# app/blueprints/todos.py
"""
BerryDo｜タスク管理アプリ API Blueprint
Projectsテーブル拡張方式による統合実装
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, date, timedelta
from sqlalchemy import case, and_
from app import db
from app.models.project import Project

# Blueprint作成
todos_bp = Blueprint('todos', __name__)
csrf = CSRFProtect()

@todos_bp.route('', methods=['GET'])
@todos_bp.route('/', methods=['GET'])
@login_required
def get_todos():
    """Todo一覧取得・フィルター・ソート対応"""
    
    # フィルタリングパラメータ
    status_filter = request.args.get('status', 'all')
    priority_filter = request.args.get('priority', 'all')
    importance_filter = request.args.get('importance', 'all')
    sort_by = request.args.get('sort', 'urgency_importance_matrix')
    
    # Todoのみをフィルター（is_todo=True）
    query = Project.query.filter_by(user_id=current_user.id, is_todo=True)
    
    # ステータスフィルター
    if status_filter != 'all':
        query = query.filter(Project.todo_status == status_filter)
    
    # 優先順位フィルター
    if priority_filter != 'all':
        query = query.filter(Project.todo_priority == priority_filter)
    
    # 重要度フィルター
    if importance_filter != 'all':
        query = query.filter(Project.todo_importance == int(importance_filter))
    
    # ソート処理
    if sort_by == 'urgency_importance_matrix':
        # 第4段階: DB側ソート（メモリソートを削減）
        # 緊急度×重要度マトリックス順
        # 1. 緊急度高×重要度高 2. 重要度高×緊急度低 3. 緊急度高×重要度低 4. 緊急度低×重要度低
        today = date.today()
        three_days_later = today + timedelta(days=3)
        
        # 緊急度判定をDB側で計算（3日以内なら0、それ以外は1）
        urgency_case = case(
            (
                and_(
                    Project.todo_due_date.isnot(None),
                    Project.todo_due_date <= three_days_later
                ),
                0  # 緊急（3日以内）
            ),
            else_=1  # 非緊急
        )
        
        # DB側でソート：重要度降順 → 緊急度昇順（0=緊急優先）
        todos = query.order_by(
            Project.todo_importance.desc().nulls_last(),  # 重要度降順（NULLは最後）
            urgency_case.asc(),  # 緊急度昇順（0=緊急優先）
            Project.created_at.desc()  # 作成日時降順（同順位の場合）
        ).all()
    elif sort_by == 'sponsor':
        todos = query.order_by(Project.company_name.asc()).all()
    elif sort_by == 'deadline':
        todos = query.order_by(Project.todo_due_date.asc().nulls_last()).all()
    else:
        todos = query.order_by(Project.created_at.desc()).all()
    
    # レスポンス形式変換
    result = []
    for todo in todos:
        todo_data = todo.to_dict()
        # Todo専用フィールド追加
        todo_data.update({
            'todo_priority': todo.todo_priority,
            'todo_importance': todo.todo_importance,
            'todo_status': todo.todo_status,
            'is_todo': todo.is_todo,
            'todo_title': todo.todo_title,
            'todo_description': todo.todo_description,
            'todo_due_date': todo.todo_due_date.isoformat() if todo.todo_due_date else None,
            'urgency_level': get_urgency_level(todo),
            'importance_label': get_importance_label(todo.todo_importance)
        })
        result.append(todo_data)
    
    # 第2段階: 統計データを同時に計算（API呼び出し1回分削減）
    # 全Todoを取得して統計計算（フィルター前の全データを使用）
    all_todos = Project.query.filter_by(user_id=current_user.id, is_todo=True).all()
    today = date.today()
    pending_todos = len([t for t in all_todos if t.todo_status == 'pending'])
    upcoming_todos = len([
        t for t in all_todos 
        if t.todo_due_date and t.todo_due_date <= today + timedelta(days=3) 
        and t.todo_due_date >= today and t.todo_status == 'pending'
    ])
    
    return jsonify({
        'todos': result,
        'total': len(result),
        'stats': {
            'pending_todos': pending_todos,
            'upcoming_todos': upcoming_todos
        },
        'filters': {
            'status': status_filter,
            'priority': priority_filter,
            'importance': importance_filter,
            'sort': sort_by
        }
    })

@todos_bp.route('', methods=['POST'])
@todos_bp.route('/', methods=['POST'])
@login_required
def create_todo():
    """Todo作成（BerryWork・BerryPay連動対応）"""
    
    data = request.get_json()
    
    # 必須フィールド検証
    required_fields = ['todo_title', 'todo_due_date', 'todo_priority', 'todo_importance']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field}は必須です'}), 400
    
    try:
        # 新規Todo作成
        todo = Project(
            user_id=current_user.id,
            company_name=data.get('company_name', 'その他'),  # デフォルト値
            amount=0,  # Todo用のため0
            deadline=datetime.strptime(data['todo_due_date'], '%Y-%m-%d').date(),
            description=data.get('todo_description', ''),
            # Todo専用フィールド
            is_todo=1,  # SQLite Boolean型対応
            linked_project_id=data.get('linked_project_id'), 
            linked_invoice_id=data.get('linked_invoice_id'),
            todo_title=data['todo_title'],
            todo_description=data.get('todo_description', ''),
            todo_due_date=datetime.strptime(data['todo_due_date'], '%Y-%m-%d').date(),
            todo_priority=data['todo_priority'],
            todo_importance=int(data['todo_importance']),
            todo_status='pending',
            # BerryWork連動（オプション）
            project_name=data.get('project_name', ''),
            notes=data.get('notes', ''),
        )
        
        db.session.add(todo)
        db.session.commit()
        
        todo_data = todo.to_dict()
        todo_data.update({
            'todo_priority': todo.todo_priority,
            'todo_importance': todo.todo_importance,
            'todo_status': todo.todo_status,
            'is_todo': todo.is_todo,
            'todo_title': todo.todo_title,
            'todo_description': todo.todo_description,
            'todo_due_date': todo.todo_due_date.isoformat() if todo.todo_due_date else None,
        })
        
        return jsonify({
            'message': 'Todo作成成功',
            'todo': todo_data
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Todo作成エラー: {str(e)}'}), 400

@todos_bp.route('/<int:todo_id>', methods=['GET'])
@login_required
def get_todo(todo_id):
    """Todo詳細取得"""
    
    todo = Project.query.filter_by(
        id=todo_id, 
        user_id=current_user.id, 
        is_todo=True
    ).first()
    
    if not todo:
        return jsonify({'error': 'Todoが見つかりません'}), 404
    
    todo_data = todo.to_dict()
    todo_data.update({
        'todo_priority': todo.todo_priority,
        'todo_importance': todo.todo_importance,
        'todo_status': todo.todo_status,
        'is_todo': todo.is_todo,
        'todo_title': todo.todo_title,
        'todo_description': todo.todo_description,
        'todo_due_date': todo.todo_due_date.isoformat() if todo.todo_due_date else None,
        'linked_project_id': todo.linked_project_id,
    })
    
    return jsonify({'todo': todo_data})

@todos_bp.route('/<int:todo_id>', methods=['PUT'])
@csrf.exempt
@login_required
def update_todo(todo_id):
    """Todo更新"""
    
    todo = Project.query.filter_by(
        id=todo_id, 
        user_id=current_user.id, 
        is_todo=True
    ).first()
    
    if not todo:
        return jsonify({'error': 'Todoが見つかりません'}), 404
    
    data = request.get_json()
    
    try:
        # Todo専用フィールド更新
        if 'todo_title' in data:
            todo.todo_title = data['todo_title']
        if 'todo_description' in data:
            todo.todo_description = data['todo_description']
        if 'todo_due_date' in data and data['todo_due_date']:
            todo.todo_due_date = datetime.strptime(data['todo_due_date'], '%Y-%m-%d').date()
        elif 'todo_due_date' in data and data['todo_due_date'] is None:
            todo.todo_due_date = None
        if 'todo_priority' in data:
            todo.todo_priority = data['todo_priority']
        if 'todo_importance' in data:
            todo.todo_importance = int(data['todo_importance'])
        if 'todo_status' in data:
            todo.todo_status = data['todo_status']
        # 案件・請求書連携フィールド更新
        if 'linked_project_id' in data:
            todo.linked_project_id = data['linked_project_id']
        if 'linked_invoice_id' in data:
            todo.linked_invoice_id = data['linked_invoice_id']

        # BerryWork連動フィールド更新
        if 'company_name' in data:
            todo.company_name = data['company_name']
        if 'project_name' in data:
            todo.project_name = data['project_name']
        if 'notes' in data:
            todo.notes = data['notes']
        
        todo.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(todo.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Todo更新エラー: {str(e)}'}), 400

@todos_bp.route('/<int:todo_id>', methods=['DELETE'])
@login_required
def delete_todo(todo_id):
    """Todo削除"""
    
    todo = Project.query.filter_by(
        id=todo_id, 
        user_id=current_user.id, 
        is_todo=True
    ).first()
    
    if not todo:
        return jsonify({'error': 'Todoが見つかりません'}), 404
    
    try:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'message': 'Todo削除成功'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Todo削除エラー: {str(e)}'}), 400

@todos_bp.route('/<int:todo_id>/complete', methods=['PUT'])
@login_required
def toggle_todo_complete(todo_id):
    """Todo完了状態切り替え（タップ操作用）"""
    
    todo = Project.query.filter_by(
        id=todo_id, 
        user_id=current_user.id, 
        is_todo=True
    ).first()
    
    if not todo:
        return jsonify({'error': 'Todoが見つかりません'}), 404
    
    try:
        # 完了状態切り替え
        new_status = 'completed' if todo.todo_status == 'pending' else 'pending'
        todo.todo_status = new_status
        todo.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': f'Todo{"完了" if new_status == "completed" else "未完了"}に変更',
            'new_status': new_status
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Todo状態変更エラー: {str(e)}'}), 400

@todos_bp.route('/stats', methods=['GET'])
@login_required
def get_todo_stats():
    """Todo統計（ダッシュボード用）"""
    
    todos = Project.query.filter_by(user_id=current_user.id, is_todo=True).all()
    
    # 統計計算
    total_todos = len(todos)
    pending_todos = len([t for t in todos if t.todo_status == 'pending'])
    completed_todos = len([t for t in todos if t.todo_status == 'completed'])
    
    # 今日・今週・今月の未完了タスク
    today = date.today()
    today_todos = len([t for t in todos if t.todo_due_date == today and t.todo_status == 'pending'])
    
    # 締切間近（3日以内）
    upcoming_todos = len([
        t for t in todos 
        if t.todo_due_date and t.todo_due_date <= today + timedelta(days=3) 
        and t.todo_due_date >= today and t.todo_status == 'pending'
    ])
    
    # 緊急度高タスク数
    high_priority_todos = len([
        t for t in todos 
        if t.todo_priority == 'high' and t.todo_status == 'pending'
    ])
    
    return jsonify({
        'pending_todos': pending_todos,
        'upcoming_todos': upcoming_todos
    })

def get_urgency_level(todo):
    """緊急度判定"""
    if not todo.todo_due_date:
        return 'low'
    
    days_left = (todo.todo_due_date - date.today()).days
    
    if days_left <= 1:
        return 'critical'
    elif days_left <= 3:
        return 'high'
    elif days_left <= 7:
        return 'medium'
    else:
        return 'low'

def get_importance_label(importance):
    """重要度ラベル"""
    labels = {
        1: '非常に低い',
        2: '低い', 
        3: '普通',
        4: '高い',
        5: '非常に高い'
    }
    return labels.get(importance, '普通')

@todos_bp.route('/project-options', methods=['GET'])
@login_required
def get_project_options():
    """ProjectApp（BerryWork）選択肢提供API"""
    
    projects = Project.query.filter_by(
        user_id=current_user.id, 
        is_todo=True
    ).order_by(Project.company_name.asc()).all()
    
    options = []
    for project in projects:
        options.append({
            'value': project.id,
            'company_name': project.company_name,
            'project_name': project.project_name or '',
            'amount': float(project.amount),
            'status': project.status,
            'label': f"{project.company_name} - {project.project_name or '案件名なし'}"
        })
    
    return jsonify({
        'project_options': options,
        'total': len(options)
    })

@todos_bp.route('/invoice-options', methods=['GET'])
@login_required  
def get_invoice_options():
    """InvoiceApp（BerryPay）選択肢提供API"""
    
    from app.models.invoice import Invoice
    
    invoices = Invoice.query.filter_by(
        user_id=current_user.id
    ).order_by(Invoice.client_company.asc()).all()
    
    options = []
    for invoice in invoices:
        options.append({
            'value': invoice.id,
            'client_company': invoice.client_company,
            'project_name': invoice.project_name or '',
            'subtotal': float(invoice.subtotal),
            'label': f"請求書: {invoice.client_company} - {invoice.project_name or '案件名なし'}"
        })
    
    return jsonify({
        'invoice_options': options,
        'total': len(options)
    })

# Blueprint登録用の関数
def register_todos_blueprint(app):
    """アプリケーションにTodos Blueprintを登録"""
    app.register_blueprint(todos_bp, url_prefix='/api/todos')