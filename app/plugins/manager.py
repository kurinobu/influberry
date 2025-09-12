"""
PluginManager - プラグインシステム管理クラス
InfluBerry v2 - 動的Blueprint登録・プラグイン統合管理
設計書仕様準拠・既存システムとの統一・シンプル構造
"""

from typing import Dict, List, Optional
from flask import Flask
from .base import BasePlugin
import logging

class PluginManager:
    """プラグインシステム統合管理"""
    
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}
        self.blueprints: List = []
        self.logger = logging.getLogger(__name__)
    
    def register_plugin(self, plugin: BasePlugin) -> bool:
        """
        プラグイン登録とBlueprint作成
        
        Args:
            plugin (BasePlugin): 登録するプラグイン
            
        Returns:
            bool: 登録成功かどうか
        """
        try:
            if plugin.name in self.plugins:
                self.logger.warning(f"プラグイン '{plugin.name}' は既に登録されています")
                return False
            
            # プラグインをレジストリに追加
            self.plugins[plugin.name] = plugin
            
            # Blueprintを作成・登録
            blueprint = plugin.create_blueprint()
            if blueprint:
                self.blueprints.append({
                    'blueprint': blueprint,
                    'plugin_name': plugin.name,
                    'url_prefix': f'/api/plugins/{plugin.name}'
                })
                self.logger.info(f"プラグイン '{plugin.name}' のBlueprint登録完了")
            else:
                self.logger.info(f"プラグイン '{plugin.name}' はBlueprint不要")
                
            return True
            
        except Exception as e:
            self.logger.error(f"プラグイン '{plugin.name}' 登録エラー: {str(e)}")
            return False
    
    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """
        プラグイン取得
        
        Args:
            name (str): プラグイン名
            
        Returns:
            Optional[BasePlugin]: プラグインインスタンス
        """
        return self.plugins.get(name)
    
    def get_enabled_plugins(self, user_id: int) -> List[BasePlugin]:
        """
        ユーザーが利用可能なプラグイン一覧
        
        Args:
            user_id (int): ユーザーID
            
        Returns:
            List[BasePlugin]: 利用可能プラグイン一覧
        """
        enabled_plugins = []
        for plugin in self.plugins.values():
            if plugin.is_enabled_for_user(user_id):
                enabled_plugins.append(plugin)
        return enabled_plugins
    
    def get_all_plugins(self) -> List[BasePlugin]:
        """
        全プラグイン一覧取得
        
        Returns:
            List[BasePlugin]: 全プラグイン一覧
        """
        return list(self.plugins.values())
    
    def register_blueprints(self, app: Flask) -> None:
        """
        Flask アプリにBlueprint登録
        
        Args:
            app (Flask): Flaskアプリケーション
        """
        try:
            for blueprint_info in self.blueprints:
                app.register_blueprint(
                    blueprint_info['blueprint'],
                    url_prefix=blueprint_info['url_prefix']
                )
                self.logger.info(
                    f"Blueprint '{blueprint_info['plugin_name']}' を "
                    f"'{blueprint_info['url_prefix']}' で登録完了"
                )
        except Exception as e:
            self.logger.error(f"Blueprint登録エラー: {str(e)}")
            raise
    
    def get_plugin_info(self, user_id: int) -> List[Dict]:
        """
        フロントエンド用プラグイン情報
        
        Args:
            user_id (int): ユーザーID
            
        Returns:
            List[Dict]: プラグイン情報一覧
        """
        plugin_info = []
        for plugin in self.plugins.values():
            info = plugin.get_plugin_info()
            info['enabled_for_user'] = plugin.is_enabled_for_user(user_id)
            plugin_info.append(info)
        return plugin_info
    
    def get_plugin_usage_stats(self, user_id: int) -> Dict:
        """
        全プラグインの使用統計
        
        Args:
            user_id (int): ユーザーID
            
        Returns:
            Dict: 使用統計情報
        """
        stats = {}
        total_usage = 0
        
        for plugin_name, plugin in self.plugins.items():
            plugin_stats = plugin.get_usage_stats(user_id)
            stats[plugin_name] = plugin_stats
            total_usage += plugin_stats.get('total_usage', 0)
        
        return {
            'plugin_stats': stats,
            'total_usage': total_usage,
            'active_plugins': len(self.get_enabled_plugins(user_id)),
            'total_plugins': len(self.plugins)
        }
    
    def initialize_plugins(self) -> None:
        """
        起動時プラグイン初期化・自動登録
        """
        try:
            # Phase 1: sponsor_managementプラグインのみ登録
            from .sponsor_management import SponsorManagementPlugin
            
            sponsor_plugin = SponsorManagementPlugin()
            self.register_plugin(sponsor_plugin)
            
            self.logger.info(f"プラグイン初期化完了: {len(self.plugins)}個のプラグイン登録")
            
            # 将来のプラグイン追加（Phase 2以降）
            # from .pricing_calculator import PricingCalculatorPlugin
            # from .content_calendar import ContentCalendarPlugin
            # from .proposal_generator import ProposalGeneratorPlugin
            
        except ImportError as e:
            self.logger.warning(f"プラグイン初期化中にインポートエラー: {str(e)}")
        except Exception as e:
            self.logger.error(f"プラグイン初期化エラー: {str(e)}")
            raise
    
    def validate_plugin_compatibility(self, plugin: BasePlugin) -> bool:
        """
        プラグイン互換性チェック（将来機能）
        
        Args:
            plugin (BasePlugin): チェック対象プラグイン
            
        Returns:
            bool: 互換性があるかどうか
        """
        # 将来実装：バージョン互換性・依存関係チェック
        return True
    
    def get_system_status(self) -> Dict:
        """
        プラグインシステム状態取得
        
        Returns:
            Dict: システム状態情報
        """
        active_plugins = len([p for p in self.plugins.values() if p.is_active])
        
        return {
            'system_status': 'healthy',
            'total_plugins': len(self.plugins),
            'active_plugins': active_plugins,
            'registered_blueprints': len(self.blueprints),
            'plugin_list': [p.name for p in self.plugins.values()]
        }
    
    def __repr__(self):
        return f'<PluginManager {len(self.plugins)} plugins>'


# グローバルプラグインマネージャーインスタンス
plugin_manager = PluginManager()