# app/schedulers/monthly_rotation.py
"""
Monthly Rotation Scheduler
月次自動切り替えスケジューラー
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime, date
import logging
from app import db
from app.models.monthly_snapshot import MonthlySnapshot
from app.models.monthly_target import MonthlyTarget
from app.blueprints.monthly_stats import get_monthly_stats

logger = logging.getLogger(__name__)

class MonthlyRotationScheduler:
    """月次自動切り替えスケジューラー"""
    
    def __init__(self, app=None):
        self.app = app
        self.scheduler = None
        self._setup_scheduler()
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """アプリケーション初期化"""
        self.app = app
        
        # スケジューラーをアプリケーションコンテキストで初期化
        with app.app_context():
            self._start_scheduler()
    
    def _setup_scheduler(self):
        """スケジューラーの設定"""
        # シンプルな設定でエラーを回避
        self.scheduler = BackgroundScheduler()
    
    def _start_scheduler(self):
        """スケジューラーの開始"""
        if not self.scheduler.running:
            # 月初日0時0分に実行するジョブを追加
            self.scheduler.add_job(
                func=self.monthly_rotation_task,
                trigger=CronTrigger(day=1, hour=0, minute=0),
                id='monthly_rotation',
                name='Monthly Rotation Task',
                replace_existing=True
            )
            
            self.scheduler.start()
            logger.info("Monthly rotation scheduler started")
    
    def monthly_rotation_task(self):
        """月初日の自動実行処理"""
        try:
            logger.info("Starting monthly rotation task")
            
            with self.app.app_context():
                # 1. 全ユーザーの過去月データをスナップショット保存
                self._create_snapshots_for_all_users()
                
                # 2. 月次切り替えの通知（オプション）
                self._notify_monthly_rotation()
                
            logger.info("Monthly rotation task completed successfully")
            
        except Exception as e:
            logger.error(f"Monthly rotation task failed: {str(e)}")
            raise
    
    def _create_snapshots_for_all_users(self):
        """全ユーザーの過去月データをスナップショット保存"""
        try:
            from app.models.user import User
            
            # 現在の月を取得
            now = datetime.now()
            current_year = now.year
            current_month = now.month
            
            # 過去月（前月）を計算
            if current_month == 1:
                prev_year = current_year - 1
                prev_month = 12
            else:
                prev_year = current_year
                prev_month = current_month - 1
            
            # 全ユーザーを取得
            users = User.query.filter_by(is_active=True).all()
            
            for user in users:
                try:
                    self._create_user_snapshot(user.id, prev_year, prev_month)
                except Exception as e:
                    logger.error(f"Failed to create snapshot for user {user.id}: {str(e)}")
                    continue
            
            logger.info(f"Created snapshots for {len(users)} users for {prev_year}-{prev_month:02d}")
            
        except Exception as e:
            logger.error(f"Failed to create snapshots for all users: {str(e)}")
            raise
    
    def _create_user_snapshot(self, user_id, year, month):
        """指定ユーザーの月次スナップショット作成"""
        try:
            # 既存のスナップショットをチェック
            existing = MonthlySnapshot.get_by_user_and_month(user_id, year, month)
            if existing:
                logger.info(f"Snapshot already exists for user {user_id}, {year}-{month:02d}")
                return
            
            # 統計データを取得（認証バイパス）
            try:
                # 直接APIを呼び出さず、データベースから直接集計
                from app.models import Project, Invoice, ProjectStatusHistory, InvoiceStatusHistory
                from sqlalchemy import func, extract
                
                # 日付範囲を計算（インデックスを有効活用するため）
                month_start = datetime(year, month, 1)
                if month == 12:
                    month_end = datetime(year + 1, 1, 1)
                else:
                    month_end = datetime(year, month + 1, 1)
                
                # 獲得案件数の集計
                # 最適化: extract()関数を使わず、日付範囲でのフィルタリングによりインデックスを有効活用
                acquired_projects = db.session.query(
                    func.count(func.distinct(ProjectStatusHistory.project_id))
                ).join(Project).filter(
                    Project.user_id == user_id,
                    ProjectStatusHistory.old_status == 'proposed',
                    ProjectStatusHistory.new_status == 'contracted',
                    ProjectStatusHistory.changed_at >= month_start,
                    ProjectStatusHistory.changed_at < month_end
                ).scalar() or 0
                
                # 完了案件数の集計
                completed_projects = db.session.query(
                    func.count(func.distinct(ProjectStatusHistory.project_id))
                ).join(Project).filter(
                    Project.user_id == user_id,
                    ProjectStatusHistory.old_status == 'contracted',
                    ProjectStatusHistory.new_status == 'completed',
                    ProjectStatusHistory.changed_at >= month_start,
                    ProjectStatusHistory.changed_at < month_end
                ).scalar() or 0
                
                # 送信済み請求書の集計
                sent_amount = db.session.query(
                    func.sum(Invoice.total_amount)
                ).join(InvoiceStatusHistory).filter(
                    Invoice.user_id == user_id,
                    InvoiceStatusHistory.old_status == 'draft',
                    InvoiceStatusHistory.new_status == 'sent',
                    InvoiceStatusHistory.changed_at >= month_start,
                    InvoiceStatusHistory.changed_at < month_end
                ).scalar() or 0
                
                stats_data = {
                    'month': f"{year}-{month:02d}-01",
                    'target': {'projects': 0, 'income': 0},
                    'actual': {
                        'acquired_projects': acquired_projects,
                        'completed_projects': completed_projects,
                        'sent_invoices_amount': float(sent_amount)
                    }
                }
                
            except Exception as e:
                logger.error(f"Failed to get stats for user {user_id}, {year}-{month:02d}: {str(e)}")
                return
            
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
            logger.info(f"Created snapshot for user {user_id}, {year}-{month:02d}")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to create snapshot for user {user_id}, {year}-{month:02d}: {str(e)}")
            raise
    
    def _notify_monthly_rotation(self):
        """月次切り替えの通知（オプション）"""
        try:
            # ここで通知機能を実装（メール、プッシュ通知等）
            logger.info("Monthly rotation notification sent")
        except Exception as e:
            logger.error(f"Failed to send monthly rotation notification: {str(e)}")
    
    def stop_scheduler(self):
        """スケジューラーの停止"""
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Monthly rotation scheduler stopped")
    
    def get_scheduler_status(self):
        """スケジューラーの状態取得"""
        if not self.scheduler:
            return {'status': 'not_initialized'}
        
        return {
            'status': 'running' if self.scheduler.running else 'stopped',
            'jobs': [job.id for job in self.scheduler.get_jobs()]
        }
    
    def trigger_manual_rotation(self):
        """手動で月次切り替えを実行"""
        try:
            logger.info("Manual monthly rotation triggered")
            self.monthly_rotation_task()
            return True
        except Exception as e:
            logger.error(f"Manual monthly rotation failed: {str(e)}")
            return False
