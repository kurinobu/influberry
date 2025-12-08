#!/usr/bin/env python3
"""
Phase 1: APIエンドポイント動作確認スクリプト
実際のAPIエンドポイントをテストして動作を確認
"""

import sys
import os
import requests
import time
from datetime import datetime

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

def test_monthly_current_api(base_url, token=None):
    """新API (/api/monthly/current) の動作確認"""
    print("\n" + "="*80)
    print("🔌 新API (/api/monthly/current) 動作確認")
    print("="*80)
    
    url = f"{base_url}/api/monthly/current"
    
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        print(f"📡 リクエストURL: {url}")
        print(f"📋 ヘッダー: {headers}")
        
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=30)
        elapsed_time = (time.time() - start_time) * 1000  # ms
        
        print(f"\n⏱️ レスポンスタイム: {elapsed_time:.2f}ms")
        print(f"📊 HTTPステータス: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ レスポンス成功")
            print(f"📋 レスポンス形式:")
            print(f"  - success: {data.get('success')}")
            print(f"  - current_month: {data.get('current_month')}")
            print(f"  - data keys: {list(data.get('data', {}).keys())}")
            
            # 計画書v2.0との比較
            if data.get('success') and 'current_month' in data and 'data' in data:
                print("\n✅ レスポンス形式: 計画書v2.0準拠")
            else:
                print("\n⚠️ レスポンス形式: 計画書v2.0と異なる可能性")
                print(f"  実際のレスポンス: {data}")
        else:
            print(f"❌ レスポンス失敗: {response.status_code}")
            print(f"エラー内容: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API呼び出しエラー: {e}")
        return None
    
    return {
        'success': response.status_code == 200,
        'status_code': response.status_code,
        'response_time': elapsed_time,
        'data': response.json() if response.status_code == 200 else None
    }

def test_monthly_targets_api(base_url, token=None):
    """旧API (/api/monthly-targets/) の動作確認"""
    print("\n" + "="*80)
    print("🔌 旧API (/api/monthly-targets/) 動作確認")
    print("="*80)
    
    now = datetime.now()
    year = now.year
    month = now.month
    
    url = f"{base_url}/api/monthly-targets/"
    params = {
        'year': year,
        'months': f'{month},{month-1},{month+1}'
    }
    
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        print(f"📡 リクエストURL: {url}")
        print(f"📋 パラメータ: {params}")
        print(f"📋 ヘッダー: {headers}")
        
        start_time = time.time()
        response = requests.get(url, params=params, headers=headers, timeout=30)
        elapsed_time = (time.time() - start_time) * 1000  # ms
        
        print(f"\n⏱️ レスポンスタイム: {elapsed_time:.2f}ms")
        print(f"📊 HTTPステータス: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ レスポンス成功")
            print(f"📋 データ件数: {len(data.get('data', []))}")
        else:
            print(f"❌ レスポンス失敗: {response.status_code}")
            print(f"エラー内容: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API呼び出しエラー: {e}")
        return None
    
    return {
        'success': response.status_code == 200,
        'status_code': response.status_code,
        'response_time': elapsed_time,
        'data': response.json() if response.status_code == 200 else None
    }

def test_monthly_stats_api(base_url, token=None):
    """旧API (/api/monthly-stats/{year}/{month}) の動作確認"""
    print("\n" + "="*80)
    print("🔌 旧API (/api/monthly-stats/{year}/{month}) 動作確認")
    print("="*80)
    
    now = datetime.now()
    year = now.year
    month = now.month
    
    url = f"{base_url}/api/monthly-stats/{year}/{month}"
    
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        print(f"📡 リクエストURL: {url}")
        print(f"📋 ヘッダー: {headers}")
        
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=30)
        elapsed_time = (time.time() - start_time) * 1000  # ms
        
        print(f"\n⏱️ レスポンスタイム: {elapsed_time:.2f}ms")
        print(f"📊 HTTPステータス: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ レスポンス成功")
            print(f"📋 レスポンス形式:")
            print(f"  - success: {data.get('success')}")
            print(f"  - data.month: {data.get('data', {}).get('month')}")
        else:
            print(f"❌ レスポンス失敗: {response.status_code}")
            print(f"エラー内容: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API呼び出しエラー: {e}")
        return None
    
    return {
        'success': response.status_code == 200,
        'status_code': response.status_code,
        'response_time': elapsed_time,
        'data': response.json() if response.status_code == 200 else None
    }

def compare_old_and_new_api(base_url, token=None):
    """旧APIと新APIの比較"""
    print("\n" + "="*80)
    print("📊 旧APIと新APIの比較")
    print("="*80)
    
    # 旧API: 2回の呼び出しをシミュレート
    print("\n📊 旧API呼び出し（2回）:")
    targets_result = test_monthly_targets_api(base_url, token)
    stats_result = test_monthly_stats_api(base_url, token)
    
    old_total_time = (targets_result['response_time'] if targets_result else 0) + \
                     (stats_result['response_time'] if stats_result else 0)
    
    print(f"\n⏱️ 旧API合計時間: {old_total_time:.2f}ms (2回の呼び出し)")
    
    # 新API: 1回の呼び出し
    print("\n📊 新API呼び出し（1回）:")
    new_result = test_monthly_current_api(base_url, token)
    
    new_total_time = new_result['response_time'] if new_result else 0
    print(f"\n⏱️ 新API合計時間: {new_total_time:.2f}ms (1回の呼び出し)")
    
    # 比較
    if old_total_time > 0 and new_total_time > 0:
        improvement = ((old_total_time - new_total_time) / old_total_time * 100)
        print(f"\n📊 比較結果:")
        print(f"  - 旧API: {old_total_time:.2f}ms (2回の呼び出し)")
        print(f"  - 新API: {new_total_time:.2f}ms (1回の呼び出し)")
        print(f"  - 改善率: {improvement:.1f}%")
        
        if new_total_time < old_total_time:
            print("  ✅ 新APIの方が高速")
        else:
            print("  ⚠️ 新APIの方が遅い（キャッシュやネットワーク状態の影響の可能性）")
    
    return {
        'old_total_time': old_total_time,
        'new_total_time': new_total_time,
        'improvement': improvement if old_total_time > 0 else 0
    }

def main():
    """メイン処理"""
    print("\n" + "="*80)
    print("🔍 Phase 1: APIエンドポイント動作確認")
    print("="*80)
    print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 環境設定
    base_url = os.environ.get('API_BASE_URL', 'http://127.0.0.1:5000')
    token = os.environ.get('API_TOKEN', None)
    
    print(f"\n📋 テスト環境:")
    print(f"  - Base URL: {base_url}")
    print(f"  - Token: {'設定済み' if token else '未設定（認証エラーの可能性あり）'}")
    
    if not token:
        print("\n⚠️ 認証トークンが設定されていません")
        print("環境変数 API_TOKEN を設定してください")
        print("例: export API_TOKEN='your_jwt_token'")
    
    # 各APIの動作確認
    print("\n" + "="*80)
    print("📊 各APIエンドポイントの動作確認")
    print("="*80)
    
    results = {}
    
    # 新API動作確認
    results['new_api'] = test_monthly_current_api(base_url, token)
    
    # 旧API動作確認
    results['old_targets'] = test_monthly_targets_api(base_url, token)
    results['old_stats'] = test_monthly_stats_api(base_url, token)
    
    # 比較
    if results['old_targets'] and results['old_stats'] and results['new_api']:
        comparison = compare_old_and_new_api(base_url, token)
        results['comparison'] = comparison
    
    # 結果サマリー
    print("\n" + "="*80)
    print("📊 Phase 1 API動作確認結果サマリー")
    print("="*80)
    
    if results.get('new_api') and results['new_api']['success']:
        print("✅ 新API (/api/monthly/current): 動作確認済み")
        print(f"   - レスポンスタイム: {results['new_api']['response_time']:.2f}ms")
        if results['new_api']['response_time'] < 500:
            print("   ✅ 目標達成: レスポンスタイム < 500ms")
        else:
            print(f"   ⚠️ 目標未達成: レスポンスタイム = {results['new_api']['response_time']:.2f}ms（目標: < 500ms）")
    else:
        print("❌ 新API (/api/monthly/current): 動作確認失敗")
        if results.get('new_api'):
            print(f"   - ステータスコード: {results['new_api']['status_code']}")
    
    if results.get('old_targets') and results['old_targets']['success']:
        print("✅ 旧API (/api/monthly-targets/): 動作確認済み")
        print(f"   - レスポンスタイム: {results['old_targets']['response_time']:.2f}ms")
    else:
        print("❌ 旧API (/api/monthly-targets/): 動作確認失敗")
    
    if results.get('old_stats') and results['old_stats']['success']:
        print("✅ 旧API (/api/monthly-stats/{year}/{month}): 動作確認済み")
        print(f"   - レスポンスタイム: {results['old_stats']['response_time']:.2f}ms")
    else:
        print("❌ 旧API (/api/monthly-stats/{year}/{month}): 動作確認失敗")
    
    if results.get('comparison'):
        comp = results['comparison']
        print(f"\n📊 比較結果:")
        print(f"  - 旧API合計: {comp['old_total_time']:.2f}ms")
        print(f"  - 新API合計: {comp['new_total_time']:.2f}ms")
        print(f"  - 改善率: {comp['improvement']:.1f}%")
    
    print("\n" + "="*80)
    print("Phase 1 API動作確認完了")
    print("="*80)
    
    return results

if __name__ == '__main__':
    main()


