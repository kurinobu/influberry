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
        <h1 class="text-4xl font-bold text-gray-800 mb-4">ご利用規約</h1>
        <p class="text-gray-600 text-lg">安心してInfluBerryをご利用いただくために</p>
        <p class="text-sm text-gray-500 mt-2">最終更新日: {{ lastUpdated }}</p>
      </div>

      <!-- 利用規約内容 -->
      <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg p-8 space-y-8">
        
        <!-- 1. はじめに -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">1. はじめに</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <p>本規約は、Air Edison（エアエジソン）（以下「当社」）が提供するInfluBerry（以下「本サービス」）の利用条件を定めるものです。</p>
            <p>本サービスをご利用になる場合には、本規約にご同意いただいたものとして取り扱わせていただきます。Z世代のインフルエンサーの皆様が安心してご利用いただけるよう、わかりやすい規約を心がけています。</p>
          </div>
        </section>

        <!-- 2. サービス内容 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">2. サービス内容</h2>
          <div class="text-gray-700 leading-relaxed">
            <p class="mb-3">InfluBerryは、インフルエンサー向けの案件管理ツールです。以下の機能を提供します：</p>
            <div class="bg-pink-50 p-4 rounded-lg">
              <ul class="list-disc list-inside space-y-2">
                <li>スポンサー案件の管理・追跡機能</li>
                <li>請求書の自動生成・管理機能</li>
                <li>収益・案件状況のダッシュボード表示</li>
                <li>ユーザーアカウント管理機能</li>
              </ul>
            </div>
            <p class="mt-3">当社は、事前の通知なくサービス内容を変更・追加・廃止する場合があります。</p>
          </div>
        </section>

        <!-- 3. アカウント登録・管理 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">3. アカウント登録・管理</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <div class="bg-yellow-50 p-4 rounded-lg">
              <h3 class="font-semibold text-gray-800 mb-2">登録条件</h3>
              <ul class="list-disc list-inside space-y-1 text-sm">
                <li>正確で最新の情報を登録すること</li>
                <li>他人になりすましてアカウントを作成しないこと</li>
                <li>一人につき一つのアカウントのみ作成すること</li>
                <li>未成年者は保護者の同意を得ること</li>
              </ul>
            </div>
            <p>ユーザーは、登録情報を正確かつ最新の状態に保つ責任があります。</p>
            <p>アカウントのセキュリティはユーザーの責任において管理してください。不正利用を発見した場合は、直ちに当社にご連絡ください。</p>
          </div>
        </section>

        <!-- 4. 利用料金・支払い -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">4. 利用料金・支払い</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <div class="bg-green-50 p-4 rounded-lg">
              <h3 class="font-semibold text-gray-800 mb-2">料金プラン</h3>
              <ul class="list-disc list-inside space-y-1 text-sm">
                <li>基本プラン：無料</li>
                <li>プレミアムプラン：月額1,280円（予定）</li>
                <li>初回1ヶ月間：全ユーザー無料提供</li>
              </ul>
            </div>
            <p>有料プランの料金は、毎月自動的に請求されます。支払い方法はクレジットカードまたは当社が指定する方法となります。</p>
            <p>料金の変更は、30日前までに通知いたします。</p>
          </div>
        </section>

        <!-- 5. 禁止事項 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">5. 禁止事項</h2>
          <div class="text-gray-700 leading-relaxed">
            <p class="mb-3">本サービスの利用に際し、以下の行為を禁止します：</p>
            <div class="bg-red-50 p-4 rounded-lg">
              <ul class="list-disc list-inside space-y-2 text-sm">
                <li>法令や公序良俗に反する行為</li>
                <li>他のユーザーまたは第三者の権利を侵害する行為</li>
                <li>本サービスの運営を妨害する行為</li>
                <li>不正アクセス、ハッキング等の行為</li>
                <li>虚偽の情報を登録・投稿する行為</li>
                <li>商用目的での無断利用</li>
                <li>その他、当社が不適切と判断する行為</li>
              </ul>
            </div>
          </div>
        </section>

        <!-- 6. 知的財産権 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">6. 知的財産権</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <p>本サービスに関する一切の知的財産権は、当社または正当な権利者に帰属します。</p>
            <p>ユーザーが本サービスに投稿したコンテンツの著作権は、ユーザーに帰属します。ただし、当社はサービス運営に必要な範囲で、これらのコンテンツを使用することができます。</p>
          </div>
        </section>

        <!-- 7. 免責事項・責任制限 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">7. 免責事項・責任制限</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <div class="bg-gray-50 p-4 rounded-lg">
              <h3 class="font-semibold text-gray-800 mb-2">当社の責任制限</h3>
              <ul class="list-disc list-inside space-y-1 text-sm">
                <li>本サービスの中断・停止による損害</li>
                <li>ユーザー同士のトラブル</li>
                <li>第三者による不正アクセス</li>
                <li>データの消失・破損</li>
              </ul>
            </div>
            <p>当社の故意または重大な過失による場合を除き、当社はユーザーに対していかなる損害の賠償責任も負わないものとします。</p>
            <p>損害賠償が認められる場合でも、その額はユーザーが過去12ヶ月間に支払った利用料金を上限とします。</p>
          </div>
        </section>

        <!-- 8. サービス利用の停止・終了 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">8. サービス利用の停止・終了</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <p>当社は、以下の場合にユーザーの利用を停止・終了することができます：</p>
            <ul class="list-disc list-inside space-y-2 ml-4">
              <li>本規約に違反した場合</li>
              <li>料金の支払いが遅滞した場合</li>
              <li>長期間サービスを利用しない場合</li>
              <li>その他、当社が適切でないと判断した場合</li>
            </ul>
            <p>ユーザーは、いつでもアカウントを削除してサービス利用を終了することができます。</p>
          </div>
        </section>

        <!-- 9. 規約の変更 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">9. 規約の変更</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <p>当社は、法令の改正やサービス内容の変更等により、本規約を変更する場合があります。</p>
            <p>重要な変更については、サービス内での通知または当ページでの告知を行い、30日の周知期間を設けます。</p>
            <p>変更後も継続してサービスをご利用いただいた場合、変更後の規約に同意いただいたものとします。</p>
          </div>
        </section>

        <!-- 10. 準拠法・管轄裁判所 -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">10. 準拠法・管轄裁判所</h2>
          <div class="text-gray-700 leading-relaxed space-y-3">
            <p>本規約は、日本法に準拠し、日本法に従って解釈されるものとします。</p>
            <p>本サービスに関連して発生した紛争については、神戸地方裁判所を第一審の専属的合意管轄裁判所とします。</p>
          </div>
        </section>

        <!-- 11. お問い合わせ -->
        <section>
          <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b border-pink-200 pb-2">11. お問い合わせ</h2>
          <div class="text-gray-700 leading-relaxed">
            <p class="mb-4">本規約に関するお問い合わせは、以下までご連絡ください：</p>
            <div class="bg-gray-50 p-4 rounded-lg">
              <div class="space-y-2 text-sm">
                <p><strong>運営者:</strong> Air Edison（エアエジソン）</p>
                <p><strong>運営責任者:</strong> 栗原伸行</p>
                <p><strong>所在地:</strong> 神戸市兵庫区西出町２−３−２３</p>
                <p><strong>お問い合わせ:</strong> <a href="https://air-edison.com/ask/" class="text-pink-600 hover:text-pink-800 underline" target="_blank" rel="noopener noreferrer">https://air-edison.com/ask/</a></p>
                <p><strong>ホームページ:</strong> <a href="https://air-edison.com" class="text-pink-600 hover:text-pink-800 underline" target="_blank" rel="noopener noreferrer">https://air-edison.com</a></p>
              </div>
            </div>
          </div>
        </section>

      </div>

      <!-- フッター -->
      <div class="text-center mt-12 py-8">
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
/* 利用規約専用スタイル */
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
}
</style>