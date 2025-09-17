<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// トップページに戻る
const goHome = () => {
  router.push('/')
}

// 最終更新日
const lastUpdated = '2025年9月17日'
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-pink-100">
    <!-- ヘッダー -->
    <div class="bg-white/80 backdrop-blur-sm border-b border-pink-200">
      <div class="max-w-4xl mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <span class="text-2xl">🍓</span>
            <h1 class="text-xl font-bold text-gray-800">InfluBerry</h1>
          </div>
          <button 
            @click="goHome"
            class="px-4 py-2 bg-pink-500 text-white rounded-full hover:bg-pink-600 transition-colors text-sm font-medium"
          >
            ログインに戻る
          </button>
        </div>
      </div>
    </div>

    <!-- メインコンテンツ -->
    <div class="max-w-4xl mx-auto px-4 py-8">
      <!-- タイトルセクション -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-800 mb-4">特定商取引法に基づく表記</h1>
        <p class="text-gray-600 text-lg">法律に基づく事業者情報の開示</p>
        <p class="text-sm text-gray-500 mt-2">最終更新日: {{ lastUpdated }}</p>
      </div>

      <!-- 特定商取引法表記内容 -->
      <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg p-8 space-y-8">
        
        <!-- 1. 事業者情報 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-6 border-b border-pink-200 pb-2">事業者情報</h2>
          <div class="bg-gray-50 p-6 rounded-lg">
            <div class="grid md:grid-cols-2 gap-6">
              <div class="space-y-4">
                <div>
                  <h3 class="font-semibold text-gray-800 mb-2 text-sm">販売事業者名</h3>
                  <p class="text-gray-700">Air Edison（エアエジソン）</p>
                </div>
                <div>
                  <h3 class="font-semibold text-gray-800 mb-2 text-sm">運営責任者</h3>
                  <p class="text-gray-700">栗原伸行</p>
                </div>
                <div>
                  <h3 class="font-semibold text-gray-800 mb-2 text-sm">所在地</h3>
                  <p class="text-gray-700">〒652-0804<br>神戸市兵庫区西出町２−３−２３</p>
                </div>
              </div>
              <div class="space-y-4">
                <div>
                  <h3 class="font-semibold text-gray-800 mb-2 text-sm">お問い合わせ先</h3>
                  <p class="text-gray-700">
                    <a href="https://air-edison.com/ask/" class="text-pink-600 hover:text-pink-800 underline" target="_blank" rel="noopener noreferrer">https://air-edison.com/ask/</a>
                  </p>
                </div>
                <div>
                  <h3 class="font-semibold text-gray-800 mb-2 text-sm">ホームページURL</h3>
                  <p class="text-gray-700">
                    <a href="https://air-edison.com" class="text-pink-600 hover:text-pink-800 underline" target="_blank" rel="noopener noreferrer">https://air-edison.com</a>
                  </p>
                </div>
                <div>
                  <h3 class="font-semibold text-gray-800 mb-2 text-sm">営業時間</h3>
                  <p class="text-gray-700">平日 9:00-18:00<br>（土日祝日を除く）</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 2. サービス・料金について -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-6 border-b border-pink-200 pb-2">サービス・料金について</h2>
          <div class="space-y-4">
            <div class="bg-green-50 p-6 rounded-lg">
              <h3 class="font-semibold text-gray-800 mb-3">提供サービス</h3>
              <ul class="list-disc list-inside space-y-1 text-sm text-gray-700">
                <li>InfluBerry - インフルエンサー向け案件管理Webアプリケーション</li>
                <li>スポンサー案件管理機能</li>
                <li>請求書自動生成機能</li>
                <li>ダッシュボード・統計機能</li>
                <li>カスタマーサポート</li>
              </ul>
            </div>
            
            <div class="bg-blue-50 p-6 rounded-lg">
              <h3 class="font-semibold text-gray-800 mb-3">料金体系</h3>
              <div class="grid md:grid-cols-2 gap-4">
                <div class="bg-white p-4 rounded-lg border">
                  <h4 class="font-medium text-gray-800 mb-2">基本プラン</h4>
                  <p class="text-2xl font-bold text-gray-800 mb-1">無料</p>
                  <p class="text-sm text-gray-600">基本的な案件管理機能をご利用いただけます</p>
                </div>
                <div class="bg-white p-4 rounded-lg border">
                  <h4 class="font-medium text-gray-800 mb-2">プレミアムプラン</h4>
                  <p class="text-2xl font-bold text-gray-800 mb-1">月額1,280円<span class="text-sm font-normal">（税込）</span></p>
                  <p class="text-sm text-gray-600">高度な機能とプレミアムサポートが利用可能（今後提供予定）</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 3. 支払い方法・時期 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-6 border-b border-pink-200 pb-2">支払い方法・時期</h2>
          <div class="bg-yellow-50 p-6 rounded-lg">
            <div class="grid md:grid-cols-2 gap-6">
              <div>
                <h3 class="font-semibold text-gray-800 mb-3">支払い方法</h3>
                <ul class="list-disc list-inside space-y-1 text-sm text-gray-700">
                  <li>クレジットカード決済（Stripe）</li>
                  <li>VISA, MasterCard, JCB, American Express対応</li>
                  <li>その他当社が指定する方法</li>
                </ul>
              </div>
              <div>
                <h3 class="font-semibold text-gray-800 mb-3">支払い時期</h3>
                <ul class="list-disc list-inside space-y-1 text-sm text-gray-700">
                  <li>基本プラン：料金発生なし</li>
                  <li>プレミアムプラン：毎月自動課金</li>
                  <li>課金日：プラン加入日と同日</li>
                  <li>初回1ヶ月無料キャンペーン実施中</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <!-- 4. 提供時期・方法 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-6 border-b border-pink-200 pb-2">提供時期・方法</h2>
          <div class="bg-purple-50 p-6 rounded-lg">
            <div class="space-y-4">
              <div>
                <h3 class="font-semibold text-gray-800 mb-2">サービス提供方法</h3>
                <p class="text-sm text-gray-700">Webブラウザを通じたオンライン提供（https://influberry.jp）</p>
              </div>
              <div>
                <h3 class="font-semibold text-gray-800 mb-2">提供時期</h3>
                <ul class="list-disc list-inside space-y-1 text-sm text-gray-700">
                  <li>基本プラン：アカウント登録後、即座にご利用開始可能</li>
                  <li>プレミアムプラン：決済完了後、即座にアップグレード</li>
                  <li>24時間365日アクセス可能（メンテナンス時間を除く）</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <!-- 5. 返品・キャンセル・解約について -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-6 border-b border-pink-200 pb-2">返品・キャンセル・解約について</h2>
          <div class="space-y-4">
            <div class="bg-red-50 p-6 rounded-lg">
              <h3 class="font-semibold text-gray-800 mb-3">返品について</h3>
              <p class="text-sm text-gray-700 mb-3">本サービスはデジタルコンテンツのため、以下を除き返品は承っておりません：</p>
              <ul class="list-disc list-inside space-y-1 text-sm text-gray-700">
                <li>当社のシステム障害によりサービスが利用できない場合</li>
                <li>当社の重大な過失によりサービス品質に問題がある場合</li>
                <li>その他、法律で定められた条件に該当する場合</li>
              </ul>
            </div>
            
            <div class="bg-green-50 p-6 rounded-lg">
              <h3 class="font-semibold text-gray-800 mb-3">解約について</h3>
              <div class="space-y-3 text-sm text-gray-700">
                <div>
                  <p class="font-medium mb-1">プレミアムプラン解約</p>
                  <ul class="list-disc list-inside space-y-1">
                    <li>いつでもアカウント設定から解約可能</li>
                    <li>解約手続き後、次回課金日より停止</li>
                    <li>解約まで既に利用いただいた期間の返金は原則として行いません</li>
                  </ul>
                </div>
                <div>
                  <p class="font-medium mb-1">アカウント削除</p>
                  <ul class="list-disc list-inside space-y-1">
                    <li>お問い合わせフォームよりご連絡ください</li>
                    <li>削除処理には営業日1-3日程度を要します</li>
                    <li>削除後のデータ復旧はできませんのでご注意ください</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 6. その他重要事項 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-6 border-b border-pink-200 pb-2">その他重要事項</h2>
          <div class="space-y-4">
            <div class="bg-gray-50 p-6 rounded-lg">
              <h3 class="font-semibold text-gray-800 mb-3">免責事項</h3>
              <ul class="list-disc list-inside space-y-1 text-sm text-gray-700">
                <li>天災地変、戦争、暴動、労働争議等の不可抗力により生じた損害</li>
                <li>お客様のコンピュータ環境、ネットワーク環境に起因する障害</li>
                <li>第三者による不正アクセス、サイバー攻撃等による損害</li>
                <li>当社の予見不可能な事象による一時的なサービス停止</li>
              </ul>
            </div>
            
            <div class="bg-blue-50 p-6 rounded-lg">
              <h3 class="font-semibold text-gray-800 mb-3">準拠法・管轄裁判所</h3>
              <div class="space-y-2 text-sm text-gray-700">
                <p><strong>準拠法：</strong>日本法</p>
                <p><strong>管轄裁判所：</strong>神戸地方裁判所を第一審の専属的合意管轄裁判所とします</p>
              </div>
            </div>
          </div>
        </section>

        <!-- 7. 表記の変更について -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-6 border-b border-pink-200 pb-2">表記の変更について</h2>
          <div class="bg-orange-50 p-6 rounded-lg">
            <p class="text-sm text-gray-700 leading-relaxed">
              本表記の内容は、法律の改正やサービス内容の変更に伴い、予告なく変更する場合があります。
              重要な変更につきましては、当サイト内での告知またはお客様への個別通知を行います。
              最新の情報は本ページをご確認ください。
            </p>
          </div>
        </section>

      </div>

      <!-- フッター -->
      <div class="text-center mt-12 py-8">
        <div class="mb-6">
          <p class="text-gray-600 text-sm mb-4">ご不明な点がございましたら、お気軽にお問い合わせください。</p>
          <a href="https://air-edison.com/ask/" 
             class="inline-flex items-center px-6 py-3 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors text-sm font-medium"
             target="_blank" rel="noopener noreferrer">
            <span class="mr-2">📧</span>
            お問い合わせフォーム
          </a>
        </div>
        
        <button 
          @click="goHome"
          class="px-8 py-3 bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-full hover:from-pink-600 hover:to-purple-700 transition-all duration-300 text-lg font-semibold shadow-lg hover:shadow-xl"
        >
          今すぐInfluBerryを始める
        </button>
        <p class="text-gray-500 text-sm mt-4">© 2025 InfluBerry - Air Edison. All rights reserved.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 特定商取引法表記専用スタイル */
section h2 {
  scroll-margin-top: 100px;
}

/* スムーススクロール */
html {
  scroll-behavior: smooth;
}

/* レスポンシブ対応 */
@media (max-width: 768px) {
  .max-w-4xl {
    max-width: 100%;
    margin: 0 auto;
  }
  
  .px-4 {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>