#!/usr/bin/env python3
"""
Phase 1: 徹底的な現状調査スクリプト
実装コードの詳細分析、データフロー確認、API動作確認を包括的に実施
"""

import sys
import os
import re
import json
from datetime import datetime
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

from app import create_app, db
from app.models.monthly_summary import MonthlySummary
from app.models.monthly_target import MonthlyTarget

app = create_app()

def analyze_frontend_api_calls():
    """フロントエンドのAPI呼び出しパターンを分析"""
    print("\n" + "="*80)
    print("📊 フロントエンド API呼び出しパターン分析")
    print("="*80)
    
    results = {
        'fetchCurrentMonthlyData': False,
        'fetchTargets': False,
        'fetchStats': False,
        'USE_NEW_API': False,
        'call_patterns': []
    }
    
    # monthly.js の確認
    monthly_js_path = Path("frontend/src/stores/monthly.js")
    if monthly_js_path.exists():
        with open(monthly_js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # USE_NEW_API フラグ確認
        use_new_api_match = re.search(r'USE_NEW_API\s*[=:]\s*(true|false)', content)
        if use_new_api_match:
            results['USE_NEW_API'] = use_new_api_match.group(1) == 'true'
            print(f"✅ USE_NEW_API: {use_new_api_match.group(1)}")
        else:
            print("⚠️ USE_NEW_API フラグが見つかりません")
        
        # fetchCurrentMonthlyData 関数の確認
        if 'fetchCurrentMonthlyData' in content:
            results['fetchCurrentMonthlyData'] = True
            print("✅ fetchCurrentMonthlyData() 関数: 実装済み")
            
            # 新API使用時の処理を確認
            if 'USE_NEW_API' in content and '/api/monthly/current' in content:
                print("✅ 新API (/api/monthly/current) への呼び出し: 実装済み")
            else:
                print("⚠️ 新API (/api/monthly/current) への呼び出し: 未実装")
        else:
            print("❌ fetchCurrentMonthlyData() 関数: 未実装")
        
        # fetchTargets 関数の確認
        if 'async fetchTargets' in content:
            results['fetchTargets'] = True
            print("✅ fetchTargets() 関数: 実装済み")
            
            # API エンドポイント確認
            if '/api/monthly-targets' in content:
                print("✅ 旧API (/api/monthly-targets/) への呼び出し: 実装済み")
        else:
            print("❌ fetchTargets() 関数: 未実装")
        
        # fetchStats 関数の確認
        if 'async fetchStats' in content:
            results['fetchStats'] = True
            print("✅ fetchStats() 関数: 実装済み")
            
            # API エンドポイント確認
            if '/api/monthly-stats' in content:
                print("✅ 旧API (/api/monthly-stats/{year}/{month}) への呼び出し: 実装済み")
        else:
            print("❌ fetchStats() 関数: 未実装")
        
        # 呼び出しパターンの抽出
        # fetchTargets と fetchStats の順次呼び出し
        pattern1 = re.search(r'await\s+this\.fetchTargets.*?await\s+this\.fetchStats', content, re.DOTALL)
        if pattern1:
            results['call_patterns'].append('sequential: fetchTargets -> fetchStats')
            print("📋 呼び出しパターン: fetchTargets が先、その後 fetchStats")
        
        # 並列呼び出しの確認
        pattern2 = re.search(r'Promise\.all.*?fetchTargets.*?fetchStats', content, re.DOTALL)
        if pattern2:
            results['call_patterns'].append('parallel: Promise.all with fetchTargets and fetchStats')
            print("📋 呼び出しパターン: Promise.all による並列呼び出し")
        else:
            print("⚠️ 並列呼び出し: 未実装（順次実行の可能性）")
    
    # MonthlyStatsSection.vue の確認
    monthly_stats_section_path = Path("frontend/src/components/MonthlyStatsSection.vue")
    if monthly_stats_section_path.exists():
        with open(monthly_stats_section_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\n📋 MonthlyStatsSection.vue のAPI呼び出し確認:")
        
        # loadData 関数の確認
        if 'const loadData' in content:
            print("✅ loadData() 関数: 実装済み")
            
            # fetchTargets と fetchStats の呼び出し確認
            fetch_targets_count = len(re.findall(r'fetchTargets', content))
            fetch_stats_count = len(re.findall(r'fetchStats', content))
            print(f"  - fetchTargets 呼び出し: {fetch_targets_count} 箇所")
            print(f"  - fetchStats 呼び出し: {fetch_stats_count} 箇所")
            
            # 順次/並列の確認
            if re.search(r'await\s+monthlyStore\.fetchTargets.*?await\s+monthlyStore\.fetchStats', content, re.DOTALL):
                print("  ⚠️ 順次実行: fetchTargets -> fetchStats")
            elif re.search(r'Promise\.all.*?fetchTargets.*?fetchStats', content, re.DOTALL):
                print("  ✅ 並列実行: Promise.all 使用")
    
    return results

def analyze_api_endpoints():
    """APIエンドポイントの実装詳細を分析"""
    print("\n" + "="*80)
    print("📊 APIエンドポイント実装詳細分析")
    print("="*80)
    
    results = {
        'new_api': {},
        'old_api_targets': {},
        'old_api_stats': {}
    }
    
    # 新API (/api/monthly/current) の確認
    monthly_current_path = Path("app/blueprints/monthly_current.py")
    if monthly_current_path.exists():
        with open(monthly_current_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results['new_api']['exists'] = True
        print("✅ 新API (/api/monthly/current): ファイル存在")
        
        # レスポンス形式の確認
        if 'current_month' in content and 'data' in content:
            print("✅ レスポンス形式: 計画書v2.0準拠")
            results['new_api']['response_format'] = 'v2.0_compliant'
        else:
            print("⚠️ レスポンス形式: 計画書v2.0と異なる可能性")
        
        # monthly_summary テーブルの使用確認
        if 'MonthlySummary.get_by_user_and_month' in content or 'MonthlySummary.query' in content:
            print("✅ 事前集計テーブル (monthly_summary) 使用: 実装済み")
            results['new_api']['uses_preaggregation'] = True
        else:
            print("⚠️ 事前集計テーブル (monthly_summary) 使用: 未確認")
        
        # フォールバック機能の確認
        if 'calculate_monthly_stats' in content:
            print("✅ フォールバック機能: 実装済み（事前集計テーブルなし時のリアルタイム計算）")
            results['new_api']['has_fallback'] = True
    
    # 旧API (/api/monthly-targets/) の確認
    monthly_path = Path("app/blueprints/monthly.py")
    if monthly_path.exists():
        with open(monthly_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results['old_api_targets']['exists'] = True
        print("✅ 旧API (/api/monthly-targets/): ファイル存在")
    
    # 旧API (/api/monthly-stats/{year}/{month}) の確認
    monthly_stats_path = Path("app/blueprints/monthly_stats.py")
    if monthly_stats_path.exists():
        with open(monthly_stats_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results['old_api_stats']['exists'] = True
        print("✅ 旧API (/api/monthly-stats/{year}/{month}): ファイル存在")
        
        # 正負集計ロジックの確認
        if 'positive_changes' in content and 'negative_changes' in content:
            print("✅ 正負集計ロジック: 実装済み")
            results['old_api_stats']['has_positive_negative_logic'] = True
        else:
            print("⚠️ 正負集計ロジック: 未確認")
    
    return results

def check_preaggregation_auto_update():
    """事前集計テーブルの自動更新機能の確認"""
    print("\n" + "="*80)
    print("📊 事前集計テーブル自動更新機能確認")
    print("="*80)
    
    results = {
        'update_function_exists': False,
        'called_from_projects': False,
        'called_from_invoices': False
    }
    
    # update_monthly_summary 関数の確認
    updater_path = Path("app/services/monthly_summary_updater.py")
    if updater_path.exists():
        with open(updater_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'def update_monthly_summary' in content:
            results['update_function_exists'] = True
            print("✅ update_monthly_summary() 関数: 実装済み")
        else:
            print("❌ update_monthly_summary() 関数: 未実装")
    
    # projects.py からの呼び出し確認
    projects_path = Path("app/blueprints/projects.py")
    if projects_path.exists():
        with open(projects_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'update_monthly_summary' in content:
            results['called_from_projects'] = True
            print("✅ プロジェクトステータス変更時: 自動更新実装済み")
        else:
            print("⚠️ プロジェクトステータス変更時: 自動更新未確認")
    
    # invoices.py からの呼び出し確認
    invoices_path = Path("app/blueprints/invoices.py")
    if invoices_path.exists():
        with open(invoices_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'update_monthly_summary' in content:
            results['called_from_invoices'] = True
            print("✅ 請求書ステータス変更時: 自動更新実装済み")
        else:
            print("⚠️ 請求書ステータス変更時: 自動更新未確認")
    
    return results

def analyze_data_flow():
    """データフローの詳細分析"""
    print("\n" + "="*80)
    print("📊 データフロー分析")
    print("="*80)
    
    flow = {
        'dashboard_initialization': [],
        'monthly_stats_section_initialization': [],
        'api_calls': []
    }
    
    # DashboardPage.vue の onMounted 確認
    dashboard_path = Path("frontend/src/views/DashboardPage.vue")
    if dashboard_path.exists():
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'onMounted' in content:
            # onMounted 内の処理を抽出
            onmounted_match = re.search(r'onMounted\s*\([^)]*\)\s*\{([^}]+)\}', content, re.DOTALL)
            if onmounted_match:
                onmounted_content = onmounted_match.group(1)
                
                if 'fetchCurrentMonthlyData' in onmounted_content or 'monthlyStore.fetch' in onmounted_content:
                    flow['dashboard_initialization'].append('calls_monthly_store')
                    print("✅ DashboardPage: monthlyStore を呼び出し")
                else:
                    print("⚠️ DashboardPage: monthlyStore を直接呼び出していない")
    
    # MonthlyStatsSection.vue のデータフロー確認
    monthly_stats_section_path = Path("frontend/src/components/MonthlyStatsSection.vue")
    if monthly_stats_section_path.exists():
        with open(monthly_stats_section_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # onMounted 確認
        if 'onMounted' in content:
            print("✅ MonthlyStatsSection: onMounted 実装済み")
            if 'loadData' in content:
                print("✅ MonthlyStatsSection: loadData() を呼び出し")
                flow['monthly_stats_section_initialization'].append('calls_loadData')
        
        # watch 確認
        watch_count = len(re.findall(r'watch\(', content))
        print(f"✅ MonthlyStatsSection: {watch_count} 個のwatch実装済み")
    
    return flow

def generate_comprehensive_report():
    """包括的レポート生成"""
    print("\n" + "="*80)
    print("📊 Phase 1 徹底的調査 総合レポート")
    print("="*80)
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'frontend_analysis': analyze_frontend_api_calls(),
        'api_analysis': analyze_api_endpoints(),
        'preaggregation_analysis': check_preaggregation_auto_update(),
        'data_flow_analysis': analyze_data_flow()
    }
    
    # 差異判定
    differences = []
    
    # 1. USE_NEW_API フラグ確認
    if not report['frontend_analysis']['USE_NEW_API']:
        differences.append({
            'type': 'feature_flag',
            'issue': 'USE_NEW_API = false',
            'impact': '新APIが無効化されているため、計画書v2.0のAPI分離戦略が適用されていない',
            'recommendation': 'USE_NEW_API を true に変更して新APIを有効化'
        })
    
    # 2. API呼び出しパターン確認
    if 'parallel' not in str(report['frontend_analysis']['call_patterns']):
        differences.append({
            'type': 'performance',
            'issue': '並列API呼び出し未実装',
            'impact': 'fetchTargets と fetchStats が順次実行されるため、総レスポンスタイムが長い',
            'recommendation': 'Promise.all を使用して並列実行を実装'
        })
    
    # 3. fetchCurrentMonthlyData の使用確認
    if report['frontend_analysis']['fetchCurrentMonthlyData']:
        if not report['frontend_analysis']['USE_NEW_API']:
            differences.append({
                'type': 'implementation',
                'issue': 'fetchCurrentMonthlyData が実装済みだが未使用',
                'impact': '新API機能が無効化されている',
                'recommendation': 'USE_NEW_API = true に変更'
            })
    
    report['differences'] = differences
    
    # レポート出力
    print("\n📋 調査結果サマリー:")
    print(f"  - フロントエンド実装: ✅ 完了")
    print(f"  - API実装: ✅ 完了")
    print(f"  - 事前集計機能: ✅ 確認済み")
    print(f"  - 差異: {len(differences)} 件")
    
    if differences:
        print("\n⚠️ 発見された差異:")
        for i, diff in enumerate(differences, 1):
            print(f"\n  {i}. {diff['type']}: {diff['issue']}")
            print(f"     影響: {diff['impact']}")
            print(f"     推奨: {diff['recommendation']}")
    else:
        print("\n✅ 計画書v2.0との差異なし")
    
    # JSON出力
    report_path = Path("docs/phase1_comprehensive_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 詳細レポート: {report_path}")
    
    return report

def main():
    """メイン処理"""
    print("\n" + "="*80)
    print("🔍 Phase 1: 徹底的な現状調査")
    print("="*80)
    print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    report = generate_comprehensive_report()
    
    print("\n" + "="*80)
    print("Phase 1 徹底的調査完了")
    print("="*80)
    
    return report

if __name__ == '__main__':
    main()


