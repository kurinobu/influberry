# /Users/kurinobu/projects/influberry_v2/app/utils/db_optimizations.py
"""
データベースクエリ最適化ヘルパー関数
パフォーマンス向上とクエリ統一化のためのユーティリティ
"""

from sqlalchemy import func
from app.models.project import Project
from app.models.user import User
from app import db


class ProjectQueryOptimizer:
    """Project関連クエリの最適化ヘルパー"""
    
    @staticmethod
    def get_user_projects_optimized(user_id, status=None, page=1, per_page=10):
        """
        ユーザーのプロジェクト一覧を最適化されたクエリで取得
        """
        query = Project.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        # インデックスを活用した並び順指定
        query = query.order_by(
            Project.deadline.asc(),
            Project.created_at.desc()
        )
        
        # ページネーション適用
        return query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
    
    @staticmethod
    def get_user_stats_optimized(user_id):
        """
        ユーザー統計情報を単一クエリで効率的に取得
        """
        # 単一クエリで全ての統計を取得
        stats_query = db.session.query(
            func.count(Project.id).label('total'),
            func.count(func.nullif(Project.status != 'proposed', True)).label('proposed'),
            func.count(func.nullif(Project.status != 'contracted', True)).label('contracted'),
            func.count(func.nullif(Project.status != 'completed', True)).label('completed'),
            func.coalesce(func.sum(
                func.case(
                    (Project.status == 'completed', Project.amount),
                    else_=0
                )
            ), 0).label('total_earnings'),
            func.coalesce(func.sum(Project.amount), 0).label('total_potential')
        ).filter_by(user_id=user_id).first()
        
        return {
            'total_projects': stats_query.total,
            'projects_by_status': {
                'proposed': stats_query.proposed,
                'contracted': stats_query.contracted, 
                'completed': stats_query.completed
            },
            'total_earnings': float(stats_query.total_earnings),
            'total_potential_earnings': float(stats_query.total_potential)
        }
    
    @staticmethod
    def get_recent_projects_optimized(user_id, limit=5):
        """
        最近のプロジェクトを効率的に取得
        """
        return Project.query.filter_by(user_id=user_id)\
            .order_by(Project.created_at.desc())\
            .limit(limit)\
            .all()


class UserQueryOptimizer:
    """User関連クエリの最適化ヘルパー"""
    
    @staticmethod
    def get_user_with_stats_optimized(user_id):
        """
        ユーザー情報と統計を結合クエリで効率的に取得
        """
        user_query = db.session.query(
            User.id,
            User.username,
            User.email,
            User.influencer_name,
            User.plan_type,
            User.is_active,
            User.created_at,
            func.count(Project.id).label('project_count'),
            func.count(
                func.case(
                    (Project.status == 'completed', 1),
                    else_=None
                )
            ).label('completed_count'),
            func.coalesce(
                func.sum(
                    func.case(
                        (Project.status == 'completed', Project.amount),
                        else_=0
                    )
                ), 0
            ).label('total_earnings')
        ).outerjoin(Project, User.id == Project.user_id)\
         .filter(User.id == user_id)\
         .group_by(User.id)\
         .first()
        
        if user_query:
            return {
                'id': user_query.id,
                'username': user_query.username,
                'email': user_query.email,
                'influencer_name': user_query.influencer_name,
                'plan_type': user_query.plan_type,
                'is_active': user_query.is_active,
                'created_at': user_query.created_at.isoformat(),
                'stats': {
                    'total_projects': user_query.project_count,
                    'completed_projects': user_query.completed_count,
                    'total_earnings': float(user_query.total_earnings)
                }
            }
        return None


class CacheHelper:
    """キャッシュ関連ヘルパー（将来実装用）"""
    
    @staticmethod
    def cache_key_generator(prefix, user_id, **kwargs):
        """
        キャッシュキー生成（Redis導入時に使用）
        """
        key_parts = [prefix, str(user_id)]
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
        return ":".join(key_parts)
    
    @staticmethod
    def invalidate_user_cache(user_id):
        """
        ユーザー関連キャッシュ無効化（将来実装）
        """
        # TODO: Redis実装時にキャッシュクリア処理を追加
        pass