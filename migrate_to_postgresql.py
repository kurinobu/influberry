#!/usr/bin/env python3
"""
InfluBerry SQLite → PostgreSQL データ移行スクリプト
作成日: 2025年9月12日
対象: Week 4 PostgreSQL移行・本番環境構築
"""

import sqlite3
import psycopg2
import sys
from datetime import datetime
import os

# PostgreSQL接続情報
POSTGRESQL_URL = "postgresql://influberry_user:CdFLqrOp2VjYDGsULPCc8e1zTBOz8l1s@dpg-d31u8gbipnbc73cn3cag-a.singapore-postgres.render.com/influberry_prod"
SQLITE_PATH = "instance/influberry_dev.db"

def log_message(message):
    """ログメッセージ出力"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def connect_databases():
    """データベース接続"""
    try:
        # SQLite接続
        sqlite_conn = sqlite3.connect(SQLITE_PATH)
        sqlite_conn.row_factory = sqlite3.Row
        log_message("SQLite接続成功")
        
        # PostgreSQL接続
        pg_conn = psycopg2.connect(POSTGRESQL_URL)
        log_message("PostgreSQL接続成功")
        
        return sqlite_conn, pg_conn
    except Exception as e:
        log_message(f"データベース接続エラー: {e}")
        sys.exit(1)

def create_postgresql_tables(pg_conn):
    """PostgreSQLテーブル作成"""
    try:
        cursor = pg_conn.cursor()
        
        # Users テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                influencer_name VARCHAR(100),
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                plan_type VARCHAR(20) NOT NULL DEFAULT 'free',
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Projects テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                company_name VARCHAR(255) NOT NULL,
                project_name VARCHAR(255),
                amount DECIMAL(10, 2) NOT NULL,
                deadline DATE NOT NULL,
                description TEXT NOT NULL,
                notes TEXT,
                status VARCHAR(20) NOT NULL DEFAULT 'proposed'
                    CHECK (status IN ('proposed', 'contracted', 'completed')),
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Invoices テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                project_name VARCHAR(255),
                invoice_number VARCHAR(50) UNIQUE NOT NULL,
                invoice_date DATE NOT NULL,
                due_date DATE NOT NULL,
                subtotal DECIMAL(10, 2) NOT NULL,
                tax_rate DECIMAL(5, 2) NOT NULL,
                tax_amount DECIMAL(10, 2) NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                client_company VARCHAR(255) NOT NULL,
                client_address TEXT,
                client_contact VARCHAR(255),
                influencer_name VARCHAR(100) NOT NULL,
                influencer_address TEXT,
                influencer_email VARCHAR(255),
                status VARCHAR(20) NOT NULL,
                description TEXT NOT NULL,
                notes TEXT,
                payment_date DATE,
                payment_method VARCHAR(50),
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # インデックス作成
        indexes = [
            "CREATE INDEX IF NOT EXISTS ix_projects_user_id ON projects (user_id);",
            "CREATE INDEX IF NOT EXISTS ix_projects_status ON projects (status);",
            "CREATE INDEX IF NOT EXISTS ix_projects_deadline ON projects (deadline);",
            "CREATE INDEX IF NOT EXISTS ix_invoices_user_id ON invoices (user_id);",
            "CREATE INDEX IF NOT EXISTS ix_invoices_project_id ON invoices (project_id);",
            "CREATE INDEX IF NOT EXISTS ix_invoices_status ON invoices (status);",
            "CREATE INDEX IF NOT EXISTS ix_invoices_invoice_date ON invoices (invoice_date);"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        pg_conn.commit()
        log_message("PostgreSQLテーブル作成完了")
        
    except Exception as e:
        log_message(f"テーブル作成エラー: {e}")
        pg_conn.rollback()
        raise

def migrate_users(sqlite_conn, pg_conn):
    """Usersテーブル移行"""
    try:
        sqlite_cursor = sqlite_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        # SQLiteからデータ取得
        sqlite_cursor.execute("SELECT * FROM users")
        users = sqlite_cursor.fetchall()
        
        log_message(f"Users移行開始: {len(users)}件")
        
        # PostgreSQLにデータ挿入
        for user in users:
            pg_cursor.execute("""
                INSERT INTO users (id, username, email, password_hash, influencer_name, 
                                 is_active, plan_type, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                user['id'], user['username'], user['email'], user['password_hash'],
                user['influencer_name'], bool(user['is_active']), user['plan_type'],
                user['created_at'], user['updated_at']
            ))
        
        # シーケンス更新
        pg_cursor.execute("SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));")
        
        pg_conn.commit()
        log_message(f"Users移行完了: {len(users)}件")
        
    except Exception as e:
        log_message(f"Users移行エラー: {e}")
        pg_conn.rollback()
        raise

def migrate_projects(sqlite_conn, pg_conn):
    """Projectsテーブル移行"""
    try:
        sqlite_cursor = sqlite_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        # SQLiteからデータ取得
        sqlite_cursor.execute("SELECT * FROM projects")
        projects = sqlite_cursor.fetchall()
        
        log_message(f"Projects移行開始: {len(projects)}件")
        
        # PostgreSQLにデータ挿入
        for project in projects:
            pg_cursor.execute("""
                INSERT INTO projects (id, user_id, company_name, project_name, amount,
                                    deadline, description, notes, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                project['id'], project['user_id'], project['company_name'],
                project['project_name'] if 'project_name' in project.keys() else None,
                project['amount'], project['deadline'],
                project['description'], 
                project['notes'] if 'notes' in project.keys() else None,
                project['status'],
                project['created_at'], project['updated_at']
            ))
        
        # シーケンス更新
        pg_cursor.execute("SELECT setval('projects_id_seq', (SELECT MAX(id) FROM projects));")
        
        pg_conn.commit()
        log_message(f"Projects移行完了: {len(projects)}件")
        
    except Exception as e:
        log_message(f"Projects移行エラー: {e}")
        pg_conn.rollback()
        raise

def migrate_invoices(sqlite_conn, pg_conn):
    """Invoicesテーブル移行"""
    try:
        sqlite_cursor = sqlite_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        # SQLiteからデータ取得
        sqlite_cursor.execute("SELECT * FROM invoices")
        invoices = sqlite_cursor.fetchall()
        
        log_message(f"Invoices移行開始: {len(invoices)}件")
        
        # PostgreSQLにデータ挿入
        for invoice in invoices:
            pg_cursor.execute("""
                INSERT INTO invoices (id, user_id, project_id, project_name, invoice_number,
                                    invoice_date, due_date, subtotal, tax_rate, tax_amount,
                                    total_amount, client_company, client_address, client_contact,
                                    influencer_name, influencer_address, influencer_email,
                                    status, description, notes, payment_date, payment_method,
                                    created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (invoice_number) DO NOTHING
            """, (
                invoice['id'], invoice['user_id'], invoice['project_id'],
                invoice['project_name'] if 'project_name' in invoice.keys() else None,
                invoice['invoice_number'],
                invoice['invoice_date'], invoice['due_date'], invoice['subtotal'],
                invoice['tax_rate'], invoice['tax_amount'], invoice['total_amount'],
                invoice['client_company'], invoice['client_address'], invoice['client_contact'],
                invoice['influencer_name'], invoice['influencer_address'], invoice['influencer_email'],
                invoice['status'], invoice['description'], invoice['notes'],
                invoice['payment_date'], invoice['payment_method'],
                invoice['created_at'], invoice['updated_at']
            ))
        
        # シーケンス更新
        pg_cursor.execute("SELECT setval('invoices_id_seq', (SELECT MAX(id) FROM invoices));")
        
        pg_conn.commit()
        log_message(f"Invoices移行完了: {len(invoices)}件")
        
    except Exception as e:
        log_message(f"Invoices移行エラー: {e}")
        pg_conn.rollback()
        raise

def verify_migration(pg_conn):
    """データ移行検証"""
    try:
        cursor = pg_conn.cursor()
        
        # レコード数確認
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM projects")
        projects_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM invoices")
        invoices_count = cursor.fetchone()[0]
        
        log_message("=== 移行結果検証 ===")
        log_message(f"Users: {users_count}件")
        log_message(f"Projects: {projects_count}件")
        log_message(f"Invoices: {invoices_count}件")
        
        # データ整合性確認
        cursor.execute("""
            SELECT u.username, COUNT(p.id) as project_count, COUNT(i.id) as invoice_count
            FROM users u
            LEFT JOIN projects p ON u.id = p.user_id
            LEFT JOIN invoices i ON u.id = i.user_id
            GROUP BY u.id, u.username
            ORDER BY u.id
        """)
        
        log_message("=== ユーザー別データ確認 ===")
        for row in cursor.fetchall():
            log_message(f"User: {row[0]}, Projects: {row[1]}, Invoices: {row[2]}")
        
        return users_count, projects_count, invoices_count
        
    except Exception as e:
        log_message(f"検証エラー: {e}")
        raise

def main():
    """メイン処理"""
    log_message("=== InfluBerry SQLite→PostgreSQL 移行開始 ===")
    
    try:
        # データベース接続
        sqlite_conn, pg_conn = connect_databases()
        
        # PostgreSQLテーブル作成
        create_postgresql_tables(pg_conn)
        
        # データ移行実行
        migrate_users(sqlite_conn, pg_conn)
        migrate_projects(sqlite_conn, pg_conn)
        migrate_invoices(sqlite_conn, pg_conn)
        
        # 移行検証
        users_count, projects_count, invoices_count = verify_migration(pg_conn)
        
        # 接続クローズ
        sqlite_conn.close()
        pg_conn.close()
        
        log_message("=== 移行完了 ===")
        log_message(f"移行完了: Users {users_count}件, Projects {projects_count}件, Invoices {invoices_count}件")
        log_message("PostgreSQL本番環境準備完了")
        
    except Exception as e:
        log_message(f"移行失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()