"""
Flask application factory
InfluBerry v2 - シンプル構成版（Flask-Login認証）
"""

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from config import config


# Extension instances
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='development'):
    """Flask application factory"""
    
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # CORS Configuration
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # Flask-Login Configuration for JSON API
    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({'error': '認証が必要です', 'code': 'UNAUTHORIZED'}), 401
        
    # Remove HTML redirect configuration for JSON API compatibility
    
    # User loader for Flask-Login
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register Blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.projects import projects_bp
    from app.blueprints.users import users_bp
    from app.blueprints.plugins import plugins_bp
    from app.blueprints.main import main_bp
    from app.blueprints.invoices import invoices_bp
    from app.blueprints.domain_redirect import domain_redirect_bp
    from app.plugins.manager import plugin_manager
    
    # Static file serving for Vue.js frontend
    from flask import send_from_directory
    @app.route('/')
    def serve_frontend():
        return send_from_directory('static', 'index.html')
    
    @app.route('/<path:filename>')
    def serve_static_files(filename):
        # Root files (favicon.ico, robots.txt, etc.)
        if '.' in filename and '/' not in filename:
            try:
                return send_from_directory('static', filename)
            except FileNotFoundError:
                pass
        
        # Assets directory (CSS, JS, images)
        if filename.startswith('assets/'):
            try:
                return send_from_directory('static', filename)
            except FileNotFoundError:
                pass
        
        # Everything else -> SPA (Vue Router handles it)
        return send_from_directory('static', 'index.html')

    app.register_blueprint(domain_redirect_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(plugins_bp, url_prefix='/api/plugins')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(invoices_bp, url_prefix='/api/invoices')
    # Plugin System Integration
    try:
        plugin_manager.initialize_plugins()
        plugin_manager.register_blueprints(app)
    except Exception as e:
        print(f"Plugin system initialization error: {e}")
        # プラグインエラーでもアプリは起動継続
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'ok', 'message': 'InfluBerry v2 API is running'}, 200
    # === エラーハンドリング・ログ設定追加 ===
    import logging
    from logging.handlers import RotatingFileHandler
    import os
    
    # ログ設定
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/influberry.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('InfluBerry startup')
    
    # 統一エラーハンドラー
    @app.errorhandler(400)
    def bad_request(error):
        """400 Bad Request エラーハンドラー"""
        return jsonify({
            'error': 'リクエストが正しくありません',
            'message': str(error.description) if error.description else 'Bad Request',
            'status': 400
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """401 Unauthorized エラーハンドラー"""
        return jsonify({
            'error': '認証が必要です',
            'message': 'ログインしてください',
            'status': 401
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """403 Forbidden エラーハンドラー"""
        return jsonify({
            'error': 'アクセス権限がありません',
            'message': str(error.description) if error.description else 'Forbidden',
            'status': 403
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """404 Not Found エラーハンドラー"""
        return jsonify({
            'error': 'リソースが見つかりません',
            'message': 'The requested URL was not found on the server',
            'status': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500 Internal Server Error エラーハンドラー"""
        app.logger.error(f'Server Error: {error}')
        return jsonify({
            'error': 'サーバー内部エラーが発生しました',
            'message': 'Internal Server Error',
            'status': 500
        }), 500
    
    # データベースエラーハンドラー
    from sqlalchemy.exc import SQLAlchemyError
    @app.errorhandler(SQLAlchemyError)
    def database_error(error):
        """データベースエラーハンドラー"""
        db.session.rollback()
        app.logger.error(f'Database Error: {error}')
        return jsonify({
            'error': 'データベースエラーが発生しました',
            'message': 'Database operation failed',
            'status': 500
        }), 500
    return app
# Database safety check
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    unsafe_db_files = ['influberry_dev.db', 'app.db', 'database.db']
    
    for db_file in unsafe_db_files:
        unsafe_path = os.path.join(project_root, db_file)
        if os.path.exists(unsafe_path):
            file_size = os.path.getsize(unsafe_path)
            if file_size == 0:
                os.remove(unsafe_path)
                print(f"WARNING: Removed empty database file from project root: {db_file}")
            else:
                print(f"CRITICAL: Non-empty database file detected in project root: {db_file}")