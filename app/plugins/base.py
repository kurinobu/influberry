"""
BasePlugin - プラグインシステム基盤クラス
InfluBerry v2 - 動的Blueprint登録・統一インターフェース実装
設計書仕様準拠・シンプル構造・拡張性確保
"""

from abc import ABC, abstractmethod
from flask import Blueprint
from typing import List, Dict, Optional

class BasePlugin(ABC):
    """プラグインベースクラス - 全プラグインの統一インターフェース"""
    
    def __init__(self, name: str, display_name: str, version: str = "1.0.0"):
        self.name = name
        self.display_name = display_name
        self.version = version
        self.blueprint = None
        self.is_active = True
        self.description = ""
    
    @abstractmethod
    def create_blueprint(self) -> Optional[Blueprint]:
        """
        プラグイン専用のBlueprint作成
        
        Returns:
            Blueprint: プラグイン専用Blueprint（Noneの場合はBlueprint不要）
        """
        pass
    
    @abstractmethod
    def get_api_endpoints(self) -> List[str]:
        """
        APIエンドポイント一覧取得
        
        Returns:
            List[str]: エンドポイントパス一覧
        """
        pass
    
    def get_plugin_info(self) -> Dict:
        """
        フロントエンド用プラグイン情報
        
        Returns:
            Dict: プラグイン基本情報
        """
        return {
            'name': self.name,
            'display_name': self.display_name,
            'version': self.version,
            'description': self.description,
            'is_active': self.is_active,
            'endpoints': self.get_api_endpoints()
        }
    
    def is_enabled_for_user(self, user_id: int) -> bool:
        """
        ユーザーがプラグインを利用可能かチェック
        
        Args:
            user_id (int): ユーザーID
            
        Returns:
            bool: 利用可能かどうか
        """
        from app.models.user import User
        user = User.query.get(user_id)
        
        if not user or not user.is_active:
            return False
            
        # プラグインが非アクティブな場合
        if not self.is_active:
            return False
            
        # フリープランの制限チェック
        if user.plan_type == 'free':
            return self._check_free_plan_limits(user_id)
        
        return True
    
    def _check_free_plan_limits(self, user_id: int) -> bool:
        """
        フリープラン制限チェック（各プラグインで実装）
        
        Args:
            user_id (int): ユーザーID
            
        Returns:
            bool: 制限内かどうか
        """
        # Phase 1-3は全機能無料のため、常にTrue
        # Phase 4以降は各プラグインで制限実装
        return True
    
    def get_usage_stats(self, user_id: int) -> Dict:
        """
        プラグイン使用統計（各プラグインで実装）
        
        Args:
            user_id (int): ユーザーID
            
        Returns:
            Dict: 使用統計情報
        """
        return {
            'plugin_name': self.name,
            'total_usage': 0,
            'this_month_usage': 0,
            'last_used': None
        }
    
    def validate_plugin_settings(self, settings: Dict) -> bool:
        """
        プラグイン設定バリデーション（各プラグインで実装）
        
        Args:
            settings (Dict): プラグイン設定
            
        Returns:
            bool: バリデーション成功かどうか
        """
        return True
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name} v{self.version}>'