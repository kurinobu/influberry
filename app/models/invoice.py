# app/models/invoice.py
"""
InfluBerry Invoice モデル
自動請求書発行システム用データモデル
"""

from datetime import datetime, date, timedelta
from decimal import Decimal
from app import db


class Invoice(db.Model):
    """請求書モデル"""
    
    __tablename__ = 'invoices'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Invoice Information
    invoice_number = db.Column(db.String(50), unique=True, nullable=False, index=True)  # 請求書番号
    invoice_date = db.Column(db.Date, nullable=False, index=True)  # 請求日
    due_date = db.Column(db.Date, nullable=False, index=True)  # 支払期限
    
    # Amount Information
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)  # 小計
    tax_rate = db.Column(db.Numeric(5, 2), nullable=False, default=Decimal('10.0'))  # 消費税率
    tax_amount = db.Column(db.Numeric(10, 2), nullable=False)  # 消費税額
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)  # 合計額
    # Project Information ← 新規セクション追加
    project_name = db.Column(db.String(255), nullable=True)  # プロジェクト名
    # Client Information (from Project)
    client_company = db.Column(db.String(255), nullable=False)  # 請求先企業名
    client_address = db.Column(db.Text)  # 請求先住所
    client_contact = db.Column(db.String(255))  # 請求先担当者
    
    # Influencer Information
    influencer_name = db.Column(db.String(100), nullable=False)  # インフルエンサー名
    influencer_address = db.Column(db.Text)  # インフルエンサー住所
    influencer_email = db.Column(db.String(255))  # インフルエンサーメール
    
    # Invoice Status
    status = db.Column(
        db.String(20), 
        nullable=False, 
        default='draft',
        index=True
    )
    # Status options: 'draft', 'sent', 'paid', 'overdue', 'cancelled'
    
    # Description
    description = db.Column(db.Text, nullable=False)  # 案件内容
    notes = db.Column(db.Text)  # 備考
    
    # Payment Information
    payment_date = db.Column(db.Date)  # 支払日
    payment_method = db.Column(db.String(50))  # 支払方法
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    user = db.relationship('User', backref='invoices')
    project = db.relationship('Project', backref='invoices')
    
    def __init__(self, user_id, project_id, **kwargs):
        """コンストラクタ"""
        self.user_id = user_id
        self.project_id = project_id
        
        # デフォルト値設定
        self.invoice_date = kwargs.get('invoice_date', date.today())
        self.due_date = kwargs.get('due_date', date.today() + timedelta(days=30))
        self.tax_rate = kwargs.get('tax_rate', Decimal('10.0'))
        
        # その他の属性設定
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self):
        return f'<Invoice {self.invoice_number}: {self.client_company} - ¥{self.total_amount}>'
    
    def generate_invoice_number(self):
        """請求書番号自動生成"""
        today = date.today()
        year_month = today.strftime('%Y%m')
        
        # 同月の請求書数を取得
        count = Invoice.query.filter(
            Invoice.invoice_number.like(f'INV-{year_month}-%')
        ).count()
        
        # 請求書番号生成 (例: INV-202509-001)
        sequence = str(count + 1).zfill(3)
        self.invoice_number = f'INV-{year_month}-{sequence}'
        return self.invoice_number
    
    def calculate_amounts(self):
        """金額計算"""
        if self.subtotal:
            # 消費税計算
            self.tax_amount = self.subtotal * (self.tax_rate / Decimal('100'))
            # 合計額計算
            self.total_amount = self.subtotal + self.tax_amount
    
    def auto_populate_from_project(self, project):
        """プロジェクトデータから自動入力"""
        self.subtotal = project.amount
        self.client_company = project.company_name
        self.description = project.description
        self.project_name = project.project_name  # Task 5: プロジェクト名自動設定追加
        
        # 金額計算実行
        self.calculate_amounts()
        
        # ユーザー情報から自動入力
        user = project.user
        if user:
            self.influencer_name = user.influencer_name
            self.influencer_email = user.email
    
    @classmethod
    def create_from_project(cls, project):
        """プロジェクトから請求書自動生成"""
        invoice = cls(
            user_id=project.user_id,
            project_id=project.id
        )
        
        # プロジェクトデータから自動入力
        invoice.auto_populate_from_project(project)
        
        # 請求書番号生成
        invoice.generate_invoice_number()
        
        return invoice
    
    def to_dict(self):
        """辞書形式でデータ返却"""
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'invoice_date': self.invoice_date.isoformat() if self.invoice_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'subtotal': float(self.subtotal) if self.subtotal else 0,
            'tax_rate': float(self.tax_rate) if self.tax_rate else 0,
            'tax_amount': float(self.tax_amount) if self.tax_amount else 0,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'client_company': self.client_company,
            'client_address': self.client_address,
            'client_contact': self.client_contact,
            'influencer_name': self.influencer_name,
            'influencer_address': self.influencer_address,
            'influencer_email': self.influencer_email,
            'status': self.status,
            'description': self.description,
            'notes': self.notes,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_method': self.payment_method,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'project_id': self.project_id,
            'user_id': self.user_id,
            # プロジェクト新フィールド統合
            'project_name': self.project_name or '',
            'project_notes': self.project.notes if self.project and self.project.notes else ''
        }
    
    def get_status_display(self):
        """ステータス表示名取得"""
        status_map = {
            'draft': '下書き',
            'sent': '送信済み',
            'paid': '支払済み',
            'overdue': '支払期限超過',
            'cancelled': 'キャンセル'
        }
        return status_map.get(self.status, self.status)
    
    def is_overdue(self):
        """支払期限超過チェック"""
        if self.status in ['paid', 'cancelled']:
            return False
        return self.due_date < date.today()
    
    def format_amount(self, amount):
        """金額フォーマット"""
        if amount is None:
            return "¥0"
        return f"¥{amount:,.0f}"
    
    def format_total_amount(self):
        """合計額フォーマット"""
        return self.format_amount(self.total_amount)
    
    def format_subtotal(self):
        """小計フォーマット"""
        return self.format_amount(self.subtotal)
    
    def format_tax_amount(self):
        """消費税額フォーマット"""
        return self.format_amount(self.tax_amount)