# /Users/kurinobu/projects/influberry_v2/app/utils/security_validators.py
"""
セキュリティバリデーション強化ヘルパー
入力検証・XSS対策・インジェクション対策のためのユーティリティ
"""

import re
import html
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from flask import request, jsonify
from functools import wraps


class InputValidator:
    """入力値バリデーションクラス"""
    
    # 安全な文字パターン
    SAFE_STRING_PATTERN = re.compile(r'^[a-zA-Z0-9\s\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF\-_.,!?()]*$')
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{3,20}$')
    
    @staticmethod
    def sanitize_string(input_str, max_length=255):
        """
        文字列の安全化処理
        """
        if not isinstance(input_str, str):
            return None
        
        # HTMLエスケープ
        escaped = html.escape(input_str.strip())
        
        # 長さ制限
        if len(escaped) > max_length:
            return None
        
        # 安全な文字パターンチェック
        if not InputValidator.SAFE_STRING_PATTERN.match(escaped):
            return None
        
        return escaped
    
    @staticmethod
    def validate_email(email):
        """
        メールアドレスバリデーション
        """
        if not isinstance(email, str) or len(email) > 255:
            return False
        
        return bool(InputValidator.EMAIL_PATTERN.match(email.strip().lower()))
    
    @staticmethod
    def validate_username(username):
        """
        ユーザー名バリデーション
        """
        if not isinstance(username, str):
            return False
        
        return bool(InputValidator.USERNAME_PATTERN.match(username.strip()))
    
    @staticmethod
    def validate_password(password):
        """
        パスワード強度バリデーション
        """
        if not isinstance(password, str):
            return False, "パスワードが正しくありません"
        
        if len(password) < 6:
            return False, "パスワードは6文字以上である必要があります"
        
        if len(password) > 128:
            return False, "パスワードは128文字以下である必要があります"
        
        # 基本的な強度チェック
        if password.isdigit() or password.isalpha():
            return False, "パスワードは英数字を組み合わせてください"
        
        return True, "OK"
    
    @staticmethod
    def validate_amount(amount_str):
        """
        金額バリデーション
        """
        try:
            amount = Decimal(str(amount_str))
            if amount <= 0:
                return None, "金額は0より大きい値である必要があります"
            if amount > Decimal('999999999.99'):
                return None, "金額が上限を超えています"
            return amount, None
        except (InvalidOperation, ValueError, TypeError):
            return None, "金額の形式が正しくありません"
    
    @staticmethod
    def validate_date(date_str):
        """
        日付バリデーション
        """
        try:
            parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # 過去の日付チェック（1年前まで許可）
            min_date = date.today().replace(year=date.today().year - 1)
            if parsed_date < min_date:
                return None, "日付が古すぎます"
            
            # 未来の日付チェック（10年後まで許可）
            max_date = date.today().replace(year=date.today().year + 10)
            if parsed_date > max_date:
                return None, "日付が未来すぎます"
            
            return parsed_date, None
        except ValueError:
            return None, "日付の形式が正しくありません（YYYY-MM-DD）"


class SecurityDecorator:
    """セキュリティデコレータークラス"""
    
    @staticmethod
    def validate_json_request(required_fields=None, optional_fields=None):
        """
        JSONリクエストバリデーションデコレータ
        """
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Content-Type チェック
                if not request.is_json:
                    return jsonify({'error': 'Content-Type must be application/json'}), 400
                
                try:
                    data = request.get_json()
                except Exception:
                    return jsonify({'error': 'Invalid JSON format'}), 400
                
                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400
                
                # 必須フィールドチェック
                if required_fields:
                    for field in required_fields:
                        if field not in data or not data[field]:
                            return jsonify({'error': f'{field}は必須です'}), 400
                
                # 不正なフィールドチェック
                allowed_fields = set(required_fields or []) | set(optional_fields or [])
                if allowed_fields:
                    for field in data.keys():
                        if field not in allowed_fields:
                            return jsonify({'error': f'不正なフィールド: {field}'}), 400
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    @staticmethod
    def rate_limit_basic(max_requests=60, window_seconds=60):
        """
        基本的なレート制限デコレータ（メモリベース）
        """
        requests_log = {}
        
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # 簡易的なレート制限（本番環境ではRedis推奨）
                client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
                current_time = datetime.now().timestamp()
                
                if client_ip not in requests_log:
                    requests_log[client_ip] = []
                
                # 古いリクエストを削除
                requests_log[client_ip] = [
                    req_time for req_time in requests_log[client_ip]
                    if current_time - req_time < window_seconds
                ]
                
                # レート制限チェック
                if len(requests_log[client_ip]) >= max_requests:
                    return jsonify({
                        'error': 'レート制限に達しました',
                        'message': f'{window_seconds}秒間に{max_requests}回まで',
                        'status': 429
                    }), 429
                
                # リクエスト記録
                requests_log[client_ip].append(current_time)
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator


class ProjectValidator:
    """プロジェクト専用バリデーター"""
    
    VALID_STATUSES = ['proposed', 'contracted', 'completed']
    
    @staticmethod
    def validate_project_data(data):
        """
        プロジェクトデータの包括的バリデーション
        """
        errors = []
        validated_data = {}
        
        # 企業名バリデーション
        company_name = InputValidator.sanitize_string(
            data.get('company_name', ''), max_length=255
        )
        if not company_name:
            errors.append('企業名が正しくありません')
        else:
            validated_data['company_name'] = company_name
        
        # 金額バリデーション
        amount, amount_error = InputValidator.validate_amount(data.get('amount'))
        if amount_error:
            errors.append(amount_error)
        else:
            validated_data['amount'] = amount
        
        # 納期バリデーション
        deadline, deadline_error = InputValidator.validate_date(data.get('deadline'))
        if deadline_error:
            errors.append(deadline_error)
        else:
            validated_data['deadline'] = deadline
        
        # 案件概要バリデーション
        description = InputValidator.sanitize_string(
            data.get('description', ''), max_length=1000
        )
        if not description:
            errors.append('案件概要が正しくありません')
        else:
            validated_data['description'] = description
        
        # プロジェクト名バリデーション（任意フィールド）
        project_name = InputValidator.sanitize_string(
            data.get('project_name', ''), max_length=255
        )
        validated_data['project_name'] = project_name
        
        # 備考・メモバリデーション（任意フィールド）
        notes = InputValidator.sanitize_string(
            data.get('notes', ''), max_length=2000
        )
        validated_data['notes'] = notes
        
        # ステータスバリデーション（更新時）
        if 'status' in data:
            status = data.get('status')
            if status not in ProjectValidator.VALID_STATUSES:
                errors.append(f'ステータスは{ProjectValidator.VALID_STATUSES}のいずれかである必要があります')
            else:
                validated_data['status'] = status
        
        return validated_data if not errors else None, errors


class UserValidator:
    """ユーザー専用バリデーター"""
    
    @staticmethod
    def validate_user_data(data):
        """
        ユーザーデータの包括的バリデーション
        """
        errors = []
        validated_data = {}
        
        # ユーザー名バリデーション
        if 'username' in data:
            if not InputValidator.validate_username(data['username']):
                errors.append('ユーザー名は3-20文字の英数字とアンダースコアのみ使用可能です')
            else:
                validated_data['username'] = data['username'].strip()
        
        # メールアドレスバリデーション
        if 'email' in data:
            if not InputValidator.validate_email(data['email']):
                errors.append('メールアドレスの形式が正しくありません')
            else:
                validated_data['email'] = data['email'].strip().lower()
        
        # インフルエンサー名バリデーション
        if 'influencer_name' in data:
            influencer_name = InputValidator.sanitize_string(
                data['influencer_name'], max_length=100
            )
            if not influencer_name:
                errors.append('インフルエンサー名が正しくありません')
            else:
                validated_data['influencer_name'] = influencer_name
        
        return validated_data if not errors else None, errors