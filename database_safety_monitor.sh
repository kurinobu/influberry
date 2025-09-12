#!/bin/bash
# InfluBerry Database Safety Monitor
# 再発防止・自動検知・修復スクリプト

PROJECT_ROOT="/Users/kurinobu/projects/influberry_v2"
INSTANCE_DB="$PROJECT_ROOT/instance/influberry_dev.db"
LOG_FILE="$PROJECT_ROOT/db_safety.log"

# ログ関数
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# プロジェクトルートの不正DBファイル検出
check_root_db_files() {
    local found_files=0
    
    # 具体的なファイル名チェック
    for db_file in "influberry_dev.db" "app.db" "database.db" "test.db"; do
        if [ -f "$PROJECT_ROOT/$db_file" ]; then
            found_files=1
            local file_size=$(stat -f%z "$PROJECT_ROOT/$db_file" 2>/dev/null || echo "0")
            
            log_message "WARNING: Database file detected in project root: $db_file (${file_size} bytes)"
            
            if [ "$file_size" -eq 0 ]; then
                log_message "Empty database file detected - removing automatically"
                rm "$PROJECT_ROOT/$db_file"
                log_message "Removed empty database file: $db_file"
            else
                log_message "CRITICAL: Non-empty database file in project root: $db_file"
                log_message "Manual intervention required - file preserved for investigation"
            fi
        fi
    done
    
    # パターンマッチによるチェック
    for pattern in "*.db" "*.sqlite" "*.sqlite3"; do
        if ls "$PROJECT_ROOT"/$pattern >/dev/null 2>&1; then
            for file in "$PROJECT_ROOT"/$pattern; do
                if [ -f "$file" ] && [[ "$(basename "$file")" != "influberry_dev.db" ]]; then
                    found_files=1
                    log_message "WARNING: Unexpected database file detected: $(basename "$file")"
                fi
            done
        fi
    done
    
    return $found_files
}

# instance/ディレクトリの健全性チェック
check_instance_db() {
    if [ ! -f "$INSTANCE_DB" ]; then
        log_message "CRITICAL: Main database missing: $INSTANCE_DB"
        return 1
    fi
    
    local file_size=$(stat -f%z "$INSTANCE_DB" 2>/dev/null || echo "0")
    if [ "$file_size" -eq 0 ]; then
        log_message "CRITICAL: Main database is empty: $INSTANCE_DB"
        return 1
    fi
    
    # SQLite整合性チェック
    if command -v sqlite3 >/dev/null 2>&1; then
        if ! sqlite3 "$INSTANCE_DB" "PRAGMA integrity_check;" >/dev/null 2>&1; then
            log_message "CRITICAL: Database integrity check failed: $INSTANCE_DB"
            return 1
        fi
    fi
    
    log_message "Database health check: OK (${file_size} bytes)"
    return 0
}

# Flask設定検証
verify_flask_config() {
    cd "$PROJECT_ROOT" || return 1
    
    python3 -c "
import os
import sys
sys.path.insert(0, '.')

try:
    from app import create_app
    app = create_app()
    
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    instance_path = app.instance_path
    
    with app.app_context():
        from app import db
        actual_path = str(db.engine.url)
    
    print(f'Config URI: {db_uri}')
    print(f'Instance Path: {instance_path}')
    print(f'Actual Engine: {actual_path}')
    
    # instance/ディレクトリ使用の確認
    if 'instance/influberry_dev.db' not in actual_path:
        print('ERROR: Flask not using instance directory')
        sys.exit(1)
    else:
        print('Flask configuration: OK')
        
except Exception as e:
    print(f'Flask config error: {e}')
    sys.exit(1)
" 2>/dev/null || {
        log_message "ERROR: Flask configuration verification failed"
        return 1
    }
    
    log_message "Flask configuration verification: OK"
    return 0
}

# メイン処理
main() {
    log_message "=== Database Safety Monitor Start ==="
    
    local exit_code=0
    
    # プロジェクトルートDBファイルチェック
    if check_root_db_files; then
        log_message "No unauthorized database files in project root"
    else
        exit_code=1
    fi
    
    # instance/データベース健全性チェック
    if ! check_instance_db; then
        exit_code=1
    fi
    
    # Flask設定検証
    if ! verify_flask_config; then
        exit_code=1
    fi
    
    if [ $exit_code -eq 0 ]; then
        log_message "All safety checks passed"
    else
        log_message "Safety checks detected issues"
    fi
    
    log_message "=== Database Safety Monitor End ==="
    return $exit_code
}

# スクリプト実行
main "$@"