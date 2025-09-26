# app/blueprints/invoices.py
"""
InfluBerry Invoice Blueprint
自動請求書発行システム API
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import date, timedelta
from decimal import Decimal

from app import db
from app.models.invoice import Invoice
from app.models.project import Project

invoices_bp = Blueprint('invoices', __name__)


@invoices_bp.route('/', methods=['GET'])
@login_required
def get_invoices():
    """ユーザーの請求書一覧取得"""
    try:
        # パラメーター取得
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        status = request.args.get('status')
        
        # クエリ構築
        query = Invoice.query.filter_by(user_id=current_user.id)
        
        # ステータスフィルター
        if status:
            query = query.filter(Invoice.status == status)
        
        # ページネーション
        invoices = query.order_by(Invoice.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'invoices': [invoice.to_dict() for invoice in invoices.items],
            'pagination': {
                'page': page,
                'pages': invoices.pages,
                'per_page': per_page,
                'total': invoices.total,
                'has_next': invoices.has_next,
                'has_prev': invoices.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'請求書一覧取得エラー: {str(e)}'
        }), 500


@invoices_bp.route('/<int:invoice_id>', methods=['GET'])
@login_required
def get_invoice(invoice_id):
    """請求書詳細取得"""
    try:
        invoice = Invoice.query.filter_by(
            id=invoice_id, 
            user_id=current_user.id
        ).first()
        
        if not invoice:
            return jsonify({
                'success': False,
                'message': '請求書が見つかりません'
            }), 404
        
        return jsonify({
            'success': True,
            'invoice': invoice.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'請求書取得エラー: {str(e)}'
        }), 500

@invoices_bp.route('/<invoice_number>', methods=['GET'])
@login_required
def get_invoice_by_number(invoice_number):
    """請求書詳細取得（請求書番号指定）- フロントエンド統合対応"""
    try:
        invoice = Invoice.query.filter_by(
            invoice_number=invoice_number, 
            user_id=current_user.id
        ).first()
        
        if not invoice:
            return jsonify({
                'success': False,
                'message': '請求書が見つかりません'
            }), 404
        
        # フロントエンド用データマッピング統一
        invoice_data = {
            'id': invoice.id,
            'invoice_number': invoice.invoice_number,
            'customer_name': invoice.client_company,  # マッピング統一
            'amount': float(invoice.subtotal),        # マッピング統一  
            'tax_rate': float(invoice.tax_rate) if invoice.tax_rate else 10.0,
            'status': invoice.status,
            'description': invoice.description,
            'due_date': invoice.due_date.isoformat() if invoice.due_date else None,
            'payment_date': invoice.payment_date.isoformat() if invoice.payment_date else None,
            'payment_method': invoice.payment_method
        }
        
        return jsonify({
            'success': True,
            'invoice': invoice_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'請求書取得エラー: {str(e)}'
        }), 500
@invoices_bp.route('/create-from-project/<int:project_id>', methods=['POST'])
@login_required
def create_invoice_from_project(project_id):
    """プロジェクトから請求書自動生成"""
    try:
        # プロジェクト確認
        project = Project.query.filter_by(
            id=project_id, 
            user_id=current_user.id
        ).first()
        
        if not project:
            return jsonify({
                'success': False,
                'message': 'プロジェクトが見つかりません'
            }), 404
        
        # 既存請求書チェック
        existing_invoice = Invoice.query.filter_by(project_id=project_id).first()
        if existing_invoice:
            return jsonify({
                'success': False,
                'message': 'このプロジェクトの請求書は既に作成されています',
                'existing_invoice_id': existing_invoice.id
            }), 400
        
        # 請求書自動生成
        invoice = Invoice.create_from_project(project)
        
        # データベース保存
        db.session.add(invoice)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '請求書を自動生成しました',
            'invoice': invoice.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'請求書生成エラー: {str(e)}'
        }), 500


@invoices_bp.route('/', methods=['POST'])
@login_required
def create_invoice():
    """手動請求書作成"""
    try:
        data = request.get_json()
        
        # 必須フィールド検証
        required_fields = ['project_id', 'client_company', 'subtotal', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'必須フィールドが不足しています: {field}'
                }), 400
        
        # プロジェクト確認
        project = Project.query.filter_by(
            id=data['project_id'], 
            user_id=current_user.id
        ).first()
        
        if not project:
            return jsonify({
                'success': False,
                'message': 'プロジェクトが見つかりません'
            }), 404
        
        # 請求書作成
        invoice = Invoice(
            user_id=current_user.id,
            project_id=data['project_id'],
            client_company=data['client_company'],
            subtotal=Decimal(str(data['subtotal'])),
            description=data['description'],
            client_address=data.get('client_address'),
            client_contact=data.get('client_contact'),
            influencer_address=data.get('influencer_address'),
            notes=data.get('notes'),
            tax_rate=Decimal(str(data.get('tax_rate', 10.0))),
            invoice_date=date.fromisoformat(data.get('invoice_date', date.today().isoformat())),
            due_date=date.fromisoformat(data.get('due_date', (date.today() + timedelta(days=30)).isoformat()))
        )
        
        # ユーザー情報自動設定
        invoice.influencer_name = current_user.influencer_name
        invoice.influencer_email = current_user.email
        
        # 金額計算
        invoice.calculate_amounts()
        
        # 請求書番号生成
        invoice.generate_invoice_number()
        
        # データベース保存
        db.session.add(invoice)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '請求書を作成しました',
            'invoice': invoice.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'請求書作成エラー: {str(e)}'
        }), 500


@invoices_bp.route('/<int:invoice_id>', methods=['PUT'])
@login_required
def update_invoice(invoice_id):
    """請求書更新"""
    try:
        invoice = Invoice.query.filter_by(
            id=invoice_id, 
            user_id=current_user.id
        ).first()
        
        if not invoice:
            return jsonify({
                'success': False,
                'message': '請求書が見つかりません'
            }), 404
        
        data = request.get_json()
        
        # 更新可能フィールド
        updatable_fields = [
            'client_company', 'client_address', 'client_contact',
            'influencer_address', 'description', 'notes',
            'subtotal', 'tax_rate', 'status', 'payment_date', 'payment_method',
            'project_name'
        ]
        
        # フィールド更新
        for field in updatable_fields:
            if field in data:
                if field in ['subtotal', 'tax_rate']:
                    setattr(invoice, field, Decimal(str(data[field])))
                elif field == 'payment_date' and data[field]:
                    setattr(invoice, field, date.fromisoformat(data[field]))
                else:
                    setattr(invoice, field, data[field])
        
        # 金額再計算
        if 'subtotal' in data or 'tax_rate' in data:
            invoice.calculate_amounts()
        
        # データベース保存
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '請求書を更新しました',
            'invoice': invoice.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'請求書更新エラー: {str(e)}'
        }), 500


@invoices_bp.route('/<int:invoice_id>', methods=['DELETE'])
@login_required
def delete_invoice(invoice_id):
    """請求書削除"""
    try:
        invoice = Invoice.query.filter_by(
            id=invoice_id, 
            user_id=current_user.id
        ).first()
        
        if not invoice:
            return jsonify({
                'success': False,
                'message': '請求書が見つかりません'
            }), 404
        
        # 削除制限チェック
        if invoice.status == 'paid':
            return jsonify({
                'success': False,
                'message': '支払済み請求書は削除できません'
            }), 400
        
        # データベースから削除
        db.session.delete(invoice)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '請求書を削除しました'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'請求書削除エラー: {str(e)}'
        }), 500


@invoices_bp.route('/stats', methods=['GET'])
@login_required
def get_invoice_stats():
    """請求書統計情報取得"""
    try:
        # 基本統計
        total_invoices = Invoice.query.filter_by(user_id=current_user.id).count()
        
        # ステータス別統計
        stats_by_status = {}
        statuses = ['draft', 'sent', 'paid', 'overdue', 'cancelled']
        
        for status in statuses:
            count = Invoice.query.filter_by(
                user_id=current_user.id, 
                status=status
            ).count()
            stats_by_status[status] = count
        
        # 金額統計
        paid_invoices = Invoice.query.filter_by(
            user_id=current_user.id, 
            status='paid'
        ).all()
        
        total_paid = sum(float(inv.total_amount) for inv in paid_invoices)
        
        # 今月の統計
        from datetime import datetime
        this_month = datetime.now().replace(day=1).date()
        
        monthly_invoices = Invoice.query.filter(
            Invoice.user_id == current_user.id,
            Invoice.invoice_date >= this_month
        ).count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_invoices': total_invoices,
                'by_status': stats_by_status,
                'total_paid_amount': total_paid,
                'this_month_invoices': monthly_invoices
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'統計取得エラー: {str(e)}'
        }), 500


@invoices_bp.route('/overdue', methods=['GET'])
@login_required
def get_overdue_invoices():
    """期限超過請求書取得"""
    try:
        overdue_invoices = Invoice.query.filter(
            Invoice.user_id == current_user.id,
            Invoice.due_date < date.today(),
            Invoice.status.in_(['sent', 'overdue'])
        ).order_by(Invoice.due_date.asc()).all()
        
        return jsonify({
            'success': True,
            'overdue_invoices': [inv.to_dict() for inv in overdue_invoices],
            'count': len(overdue_invoices)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'期限超過請求書取得エラー: {str(e)}'
        }), 500
    
@invoices_bp.route('/options', methods=['GET'])
@login_required
def get_invoice_options():
    """Todo連動用請求書選択肢取得"""
    try:
        invoices = Invoice.query.filter_by(
            user_id=current_user.id
        ).order_by(Invoice.created_at.desc()).all()
        
        return jsonify([invoice.to_dict() for invoice in invoices]), 200
        
    except Exception as e:
        return jsonify({'error': '請求書選択肢取得エラー'}), 500