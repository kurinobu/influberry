# app/blueprints/invoices.py
"""
InfluBerry Invoice Blueprint
自動請求書発行システム API
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from flask_wtf.csrf import CSRFProtect
from datetime import date, datetime, timedelta
from decimal import Decimal

from app import db
from app.models.invoice import Invoice
from app.models.project import Project
from flask import current_app

invoices_bp = Blueprint('invoices', __name__)
csrf = CSRFProtect()


@invoices_bp.route('/', methods=['GET'])
@login_required
def get_invoices():
    """ユーザーの請求書一覧取得"""
    try:
        # パラメーター取得
        status = request.args.get('status')
        
        # クエリ構築
        query = Invoice.query.filter_by(user_id=current_user.id)
        
        # ステータスフィルター
        if status:
            query = query.filter(Invoice.status == status)
        
        # 全件取得（ページネーション削除）
        invoices = query.order_by(Invoice.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'invoices': [invoice.to_dict() for invoice in invoices],
            'pagination': {
                'total': len(invoices)
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
                'message': '請求書は既に以前発行されてます。二度の発行はできません。',
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
@csrf.exempt
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
            'project_name', 'invoice_date', 'due_date'
        ]
        
        # ステータス変更履歴記録用の変数
        old_status = None
        status_changed = False
        
        # フィールド更新
        for field in updatable_fields:
            if field in data:
                if field == 'status':
                    # ステータス変更の場合は履歴記録用に保存
                    old_status = invoice.status
                    if old_status != data[field]:
                        status_changed = True
                    setattr(invoice, field, data[field])
                elif field in ['subtotal', 'tax_rate']:
                    setattr(invoice, field, Decimal(str(data[field])))
                elif field in ['payment_date', 'invoice_date', 'due_date'] and data[field]:
                    setattr(invoice, field, date.fromisoformat(data[field]))
                else:
                    setattr(invoice, field, data[field])
        
        # ステータス変更履歴記録
        if status_changed:
            from app.models.invoice_status_history import InvoiceStatusHistory
            history = InvoiceStatusHistory(
                invoice_id=invoice.id,
                old_status=old_status,
                new_status=data['status'],
                changed_by=current_user.id
            )
            db.session.add(history)
            
            # Phase 2: 事前集計テーブル更新
            try:
                from app.services.monthly_summary_updater import update_monthly_summary
                changed_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                update_monthly_summary(current_user.id, changed_month)
                print(f"✅ 請求書ステータス変更: 事前集計テーブル更新完了")
            except Exception as e:
                print(f"⚠️ 請求書ステータス変更: 事前集計テーブル更新エラー: {e}")
                # エラーでも処理は継続（既存機能を破壊しない）
        
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
    
@invoices_bp.route('/<int:invoice_id>/pdf', methods=['GET'])
@login_required
def generate_invoice_pdf(invoice_id):
    """請求書PDF生成"""
    try:
        # 請求書データ取得
        invoice = Invoice.query.filter_by(
            id=invoice_id, 
            user_id=current_user.id
        ).first()
        
        if not invoice:
            return jsonify({'error': '請求書が見つかりません'}), 404
        
        # プロジェクトデータ取得
        project = Project.query.filter_by(id=invoice.project_id).first()
        if not project:
            return jsonify({'error': 'プロジェクトデータが見つかりません'}), 404
        
        # HTMLテンプレート読み込み・レンダリング
        from flask import render_template
        html_content = render_template(
            'pdf/invoice.html',
            invoice=invoice,
            project=project,
            user=current_user
        )

        # 発行日の取得（PDF生成で使用）
        issue_date = invoice.invoice_date if hasattr(invoice, 'invoice_date') and invoice.invoice_date else invoice.created_at

        # ReportLab PDF生成（日本語対応）
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from io import BytesIO
        import os
        
        pdf_buffer = BytesIO()
        
        # 日本語フォント登録
        font_path = os.path.join(current_app.static_folder, 'fonts', 'ipaexg.ttf')
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('IPAexGothic', font_path))
        
        # ReportLab PDF生成（標準的な日本の請求書フォーマット）
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.colors import black
        from io import BytesIO
        import os
        
        pdf_buffer = BytesIO()
        
        # 日本語フォント登録
        font_path = os.path.join(current_app.static_folder, 'fonts', 'ipaexg.ttf')
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('IPAexGothic', font_path))
        
        # A4サイズ定義
        page_width, page_height = A4
        margin = 50
        
        # PDF Canvas作成（白背景・黒文字のみ）
        p = canvas.Canvas(pdf_buffer, pagesize=A4)
        p.setFillColor(black)
        p.setStrokeColor(black)
        
        # === 発行日・請求書番号（タイトル上右） ===
        y_position = page_height - margin - 20
        right_x = page_width - margin
        
        p.setFont('IPAexGothic', 9)
        p.drawRightString(right_x, y_position, f"発行日: {issue_date.strftime('%Y年%m月%d日')}")
        y_position -= 15
        p.drawRightString(right_x, y_position, f"請求書番号: {invoice.invoice_number}")

        # === 請求書タイトル ===
        y_position = page_height - margin - 60
        p.setFont('IPAexGothic', 20)
        title_text = "請　求　書"
        title_width = p.stringWidth(title_text, 'IPAexGothic', 20)
        p.drawString((page_width - title_width) / 2, y_position, title_text)
        
        # タイトル下線
        y_position -= 10
        p.setLineWidth(0.5)
        p.line(margin, y_position, page_width - margin, y_position)
        
        # === 請求先（左側） ===
        y_position -= 40
        p.setFont('IPAexGothic', 11)
        p.drawString(margin, y_position, f"{project.company_name}　御中")
        
        # === 請求元（右側・同じ高さ） ===
        p.setFont('IPAexGothic', 10)
        
        # オフィス所在地（任意）
        if current_user.office_address:
            p.drawRightString(page_width - margin, y_position, current_user.office_address)
            y_position -= 15
        
        # 請求者名（必須）
        issuer_name = current_user.issuer_name or current_user.influencer_name or current_user.username
        p.drawRightString(page_width - margin, y_position, issuer_name)
        y_position -= 15
        
        # 連絡先（任意）
        if current_user.contact_info:
            p.drawRightString(page_width - margin, y_position, current_user.contact_info)
            y_position -= 15
        
        # === 支払期限・件名 ===
        y_position -= 30
        
        # プロジェクト名表示
        project_name_display = invoice.project_name or project.project_name or ''
        if project_name_display:
            p.drawString(margin, y_position, f"件名: {project_name_display}")
            y_position -= 20
        
        due_date = invoice.due_date if hasattr(invoice, 'due_date') and invoice.due_date else None
        if due_date:
            p.drawString(margin, y_position, f"お支払期限: {due_date.strftime('%Y年%m月%d日')}")
            y_position -= 20
        
        # === 合計金額（大きく表示） ===
        y_position -= 40
        p.setFont('IPAexGothic', 14)
        total_amount = invoice.total_amount if hasattr(invoice, 'total_amount') and invoice.total_amount else invoice.subtotal
        p.drawString(margin, y_position, f"ご請求金額: ¥{int(total_amount):,}")
        
        # === 明細表 ===
        y_position -= 50
        p.setFont('IPAexGothic', 10)
        
        # 明細表ヘッダー
        table_y = y_position
        table_height = 25
        
        # 表の罫線（シンプル）
        p.setLineWidth(0.5)
        p.rect(margin, table_y - table_height, page_width - 2 * margin, table_height)
        
        # ヘッダーテキスト
        header_y = table_y - 15
        
        col1_x = margin + 10  # 項目名
        col2_x = page_width - margin - 120  # 数量
        col3_x = page_width - margin - 10   # 金額
        
        p.drawString(col1_x, header_y, "項目")
        p.drawRightString(col2_x, header_y, "数量")
        p.drawRightString(col3_x, header_y, "金額")
        
        # 明細行
        y_position = table_y - table_height - 20
        
        # 明細データ
        item_name = invoice.description or invoice.project_name or project.project_name or '案件作業'
        p.drawString(col1_x, y_position, item_name)
        p.drawRightString(col2_x, y_position, "1")
        p.drawRightString(col3_x, y_position, f"¥{int(invoice.subtotal):,}")
        
        # 明細行の罫線
        y_position -= 10
        p.line(margin, y_position, page_width - margin, y_position)
        
        # === 小計・消費税・合計 ===
        y_position -= 30
        
        # 右寄せで合計表示
        label_x = page_width - margin - 100
        amount_x = page_width - margin - 10
        
        p.setFont('IPAexGothic', 10)
        p.drawString(label_x, y_position, "小計")
        p.drawRightString(amount_x, y_position, f"¥{int(invoice.subtotal):,}")
        y_position -= 20
        
        if hasattr(invoice, 'tax_amount') and invoice.tax_amount:
            p.drawString(label_x, y_position, "消費税")
            p.drawRightString(amount_x, y_position, f"¥{int(invoice.tax_amount):,}")
            y_position -= 20
        
        # 合計（罫線付き）
        y_position -= 5
        p.setLineWidth(0.5)
        p.line(label_x - 10, y_position, amount_x + 10, y_position)
        y_position -= 20
        
        p.setFont('IPAexGothic', 11)
        p.drawString(label_x, y_position, "合計")
        p.drawRightString(amount_x, y_position, f"¥{int(total_amount):,}")

        # === 支払い情報 ===
        if current_user.bank_name or current_user.account_number:
            y_position -= 40
            p.setFont('IPAexGothic', 10)
            p.drawString(margin, y_position, "【お振込先】")
            
            y_position -= 20
            
            if current_user.payment_method:
                p.drawString(margin, y_position, f"支払方法: {current_user.payment_method}")
                y_position -= 18
            
            if current_user.bank_name:
                p.drawString(margin, y_position, f"銀行名: {current_user.bank_name}")
                y_position -= 18
            
            if current_user.branch_name:
                p.drawString(margin, y_position, f"支店名: {current_user.branch_name}")
                y_position -= 18
            
            if current_user.account_type:
                p.drawString(margin, y_position, f"口座種別: {current_user.account_type}")
                y_position -= 18
            
            if current_user.account_number:
                p.drawString(margin, y_position, f"口座番号: {current_user.account_number}")
                y_position -= 18
            
            if current_user.account_holder:
                p.drawString(margin, y_position, f"口座名義: {current_user.account_holder}")
        
        # PDF完成
        p.showPage()
        p.save()
        pdf_buffer.seek(0)
        
        # レスポンス生成
        from flask import send_file
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'invoice_{invoice.invoice_number}.pdf'
        )
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"PDF生成エラー詳細: {error_trace}")
        return jsonify({'error': f'PDF生成エラー: {str(e)}'}), 500