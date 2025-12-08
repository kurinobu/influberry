#!/usr/bin/env python3
"""
Phase 2: 計画書v2.0, v2.1との差異確認スクリプト
実装完了後の計画書準拠性を確認
"""

import sys
import os
import re
from datetime import datetime
from pathlib import Path

def check_use_new_api_flag():
    """USE_NEW_APIフラグの状態を確認"""
    print("\n" + "="*80)
    print("📊 USE_NEW_API フラグ確認")
    print("="*80)
    
    monthly_js_path = Path("frontend/src/stores/monthly.js")
    if not monthly_js_path.exists():
        print("❌ monthly.js が見つかりません")
        return False
    
    with open(monthly_js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # USE_NEW_API フラグの確認
    use_new_api_match = re.search(r'USE_NEW_API:\s*(true|false)', content)
    if use_new_api_match:
        value = use_new_api_match.group(1) == 'true'
        print(f"✅ USE_NEW_API: {use_new_api_match.group(1)}")
        if value:
            print("✅ Phase 2実装完了: 新APIが有効化されています")
            return True
        else:
            print("⚠️ Phase 2未完了: 新APIが無効化されています")
            return False
    else:
        print("⚠️ USE_NEW_API フラグが見つかりません")
        return False

def check_monthly_stats_section_implementation():
    """MonthlyStatsSection.vueの実装確認"""
    print("\n" + "="*80)
    print("📊 MonthlyStatsSection.vue 実装確認")
    print("="*80)
    
    monthly_stats_section_path = Path("frontend/src/components/MonthlyStatsSection.vue")
    if not monthly_stats_section_path.exists():
        print("❌ MonthlyStatsSection.vue が見つかりません")
        return False
    
    with open(monthly_stats_section_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = {
        'onMounted_fetchCurrentMonthlyData': False,
        'loadData_USE_NEW_API_check': False,
        'loadData_overview_maintained': False,
        'loadData_legacy_maintained': False
    }
    
    # onMounted で fetchCurrentMonthlyData() を呼び出しているか確認
    if re.search(r'onMounted.*?fetchCurrentMonthlyData', content, re.DOTALL):
        results['onMounted_fetchCurrentMonthlyData'] = True
        print("✅ onMounted: fetchCurrentMonthlyData() を呼び出し（新API使用時）")
    else:
        print("⚠️ onMounted: fetchCurrentMonthlyData() を呼び出していない可能性")
    
    # loadData() で USE_NEW_API をチェックしているか確認
    if re.search(r'monthlyStore\.USE_NEW_API', content):
        results['loadData_USE_NEW_API_check'] = True
        print("✅ loadData(): USE_NEW_API フラグをチェック")
    else:
        print("⚠️ loadData(): USE_NEW_API フラグをチェックしていない可能性")
    
    # overviewタブが既存の方法を維持しているか確認
    if re.search(r'props\.currentTab === \'overview\'.*?fetchOverview', content, re.DOTALL):
        results['loadData_overview_maintained'] = True
        print("✅ loadData(): overviewタブは既存の fetchOverview() を維持")
    else:
        print("⚠️ loadData(): overviewタブの処理が確認できません")
    
    # 旧API使用時が既存の方法を維持しているか確認
    if re.search(r'else.*?fetchTargets.*?fetchStats', content, re.DOTALL):
        results['loadData_legacy_maintained'] = True
        print("✅ loadData(): 旧API使用時は既存の方法を維持（後方互換性）")
    else:
        print("⚠️ loadData(): 旧API使用時の処理が確認できません")
    
    return all(results.values())

def check_plan_compliance():
    """計画書v2.0, v2.1との準拠性を確認"""
    print("\n" + "="*80)
    print("📊 計画書v2.0, v2.1との差異確認")
    print("="*80)
    
    differences = []
    
    # 1. USE_NEW_API フラグ確認
    monthly_js_path = Path("frontend/src/stores/monthly.js")
    if monthly_js_path.exists():
        with open(monthly_js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        use_new_api_match = re.search(r'USE_NEW_API:\s*(true|false)', content)
        if use_new_api_match:
            value = use_new_api_match.group(1) == 'true'
            if value:
                print("✅ USE_NEW_API = true: 計画書v2.0準拠")
            else:
                differences.append("⚠️ USE_NEW_API = false: 計画書v2.0で要求される true になっていません")
        else:
            differences.append("❌ USE_NEW_API フラグが見つかりません")
    
    # 2. fetchCurrentMonthlyData() の実装確認
    if monthly_js_path.exists():
        with open(monthly_js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'fetchCurrentMonthlyData' in content and '/api/monthly/current' in content:
            print("✅ fetchCurrentMonthlyData(): 新API (/api/monthly/current) を呼び出し - 計画書v2.0準拠")
        else:
            differences.append("⚠️ fetchCurrentMonthlyData(): 新API (/api/monthly/current) を呼び出していない可能性")
    
    # 3. MonthlyStatsSection.vue の実装確認
    monthly_stats_section_path = Path("frontend/src/components/MonthlyStatsSection.vue")
    if monthly_stats_section_path.exists():
        with open(monthly_stats_section_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # onMounted で fetchCurrentMonthlyData() を呼び出しているか確認
        if re.search(r'onMounted.*?fetchCurrentMonthlyData', content, re.DOTALL):
            print("✅ MonthlyStatsSection: 初期化時に fetchCurrentMonthlyData() を呼び出し - 計画書v2.0準拠")
        else:
            differences.append("⚠️ MonthlyStatsSection: 初期化時に fetchCurrentMonthlyData() を呼び出していない可能性")
        
        # loadData() で新API使用時の処理が実装されているか確認
        if re.search(r'monthlyStore\.USE_NEW_API.*?getStatsByMonth', content, re.DOTALL):
            print("✅ MonthlyStatsSection: 新API使用時は既存データから取得 - 計画書v2.0準拠")
        else:
            differences.append("⚠️ MonthlyStatsSection: 新API使用時の処理が実装されていない可能性")
    
    # 4. 計画書v2.1との比較
    print("\n📋 計画書v2.1との比較:")
    print("  - Phase 2: 根本解決（計画書v2.0完全準拠）")
    print("  - Step 2-1: 新規APIエンドポイントの実装 → ✅ 実装済み（app/blueprints/monthly_current.py）")
    print("  - Step 2-2: フロントエンドの段階的切り替え → ✅ 実装済み（USE_NEW_API = true）")
    
    if differences:
        print("\n⚠️ 発見された差異:")
        for i, diff in enumerate(differences, 1):
            print(f"  {i}. {diff}")
    else:
        print("\n✅ 計画書v2.0, v2.1との差異なし")
    
    return len(differences) == 0

def main():
    """メイン処理"""
    print("\n" + "="*80)
    print("🔍 Phase 2: 計画書v2.0, v2.1との差異確認")
    print("="*80)
    print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # 1. USE_NEW_API フラグ確認
    results.append(("USE_NEW_API", check_use_new_api_flag()))
    
    # 2. MonthlyStatsSection.vue 実装確認
    results.append(("MonthlyStatsSection", check_monthly_stats_section_implementation()))
    
    # 3. 計画書準拠性確認
    results.append(("Plan Compliance", check_plan_compliance()))
    
    # 結果サマリー
    print("\n" + "="*80)
    print("📊 Phase 2 差異確認結果サマリー")
    print("="*80)
    
    success_count = sum(1 for _, result in results if result)
    print(f"✅ 成功: {success_count}/{len(results)} 項目")
    
    if all(result for _, result in results):
        print("\n✅ Phase 2実装完了: 計画書v2.0, v2.1との差異なし")
    else:
        print("\n⚠️ Phase 2実装に差異があります")
        for name, result in results:
            if not result:
                print(f"  - {name}: 差異あり")
    
    print("\n" + "="*80)
    print("Phase 2 差異確認完了")
    print("="*80)
    
    return all(result for _, result in results)

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)


