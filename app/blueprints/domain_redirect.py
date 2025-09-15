from flask import Blueprint, request, redirect

domain_redirect_bp = Blueprint('domain_redirect', __name__)

@domain_redirect_bp.before_app_request
def handle_domain_redirect():
    """旧ドメインから新ドメインへの301リダイレクト"""
    if request.host == 'influberry-app.onrender.com':
        new_url = request.url.replace(
            'influberry-app.onrender.com', 
            'influberry.jp'
        )
        return redirect(new_url, code=301)