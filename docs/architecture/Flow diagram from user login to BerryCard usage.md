

\#\# ユーザーログインからBerryCard利用までのフロー

\#\#\# 1\. 全体フロー図

\`\`\`  
┌─────────────────────────────────────────────────────────┐  
│                    1\. ログイン                           │  
└─────────────────────────────────────────────────────────┘  
                            │  
                    ユーザーがログイン  
                            │  
                    /auth でログインフォーム入力  
                            │  
                    POST /api/auth/login  
                            │  
                    Flask-Login Cookie認証  
                            │  
┌─────────────────────────────────────────────────────────┐  
│              2\. AppIndexPage（アプリ一覧）               │  
└─────────────────────────────────────────────────────────┘  
                            │  
              ログイン成功 → /app-index へリダイレクト  
                            │  
              ┌─────────────┴─────────────┐  
              │                           │  
    ┌─────────▼─────────┐     ┌──────────▼──────────┐  
    │  BerryManagement  │     │     BerryCard       │  
    │  （案件管理系）    │     │  （デジタル名刺）    │  
    └─────────┬─────────┘     └──────────┬──────────┘  
              │                           │  
              │ クリック                   │ クリック  
              │                           │  
┌─────────────▼─────────────┐ ┌──────────▼──────────┐  
│    3-A. /dashboard        │ │   3-B. /card        │  
│  （案件系ダッシュボード）   │ │ （BerryCardアプリ）  │  
└───────────────────────────┘ └─────────────────────┘  
\`\`\`

\---

\#\#\# 2\. 詳細フロー（BerryCard利用の場合）

\#\#\#\# Step 1: ログイン（/auth）

\*\*画面\*\*: \`AuthPage.vue\`

\*\*ユーザー操作\*\*:  
1\. ブラウザで \`https://influberry.jp/auth\` にアクセス  
2\. ログインフォームに入力  
   \- ユーザー名（またはメールアドレス）  
   \- パスワード  
3\. 「ログイン」ボタンクリック

\*\*フロントエンド処理\*\*:  
\`\`\`javascript  
// stores/auth.js  
async login(credentials) {  
  const response \= await axios.post(  
    \`${API\_BASE\_URL}/api/auth/login\`,  
    credentials,  
    { withCredentials: true }  
  )  
    
  this.isAuthenticated \= true  
  this.user \= response.data.user  
    
  // ★ 重要: ログイン後は /app-index へリダイレクト  
  this.router.push('/app-index')  
}  
\`\`\`

\*\*バックエンド処理\*\*:  
\`\`\`python  
\# app/blueprints/auth.py

@auth\_bp.route('/api/auth/login', methods=\['POST'\])  
def login():  
    data \= request.get\_json()  
    user \= User.query.filter\_by(username=data\['username'\]).first()  
      
    if user and user.check\_password(data\['password'\]):  
        login\_user(user)  \# Flask-Login Cookie設定  
        return jsonify({  
            'success': True,  
            'user': {  
                'id': user.id,  
                'username': user.username,  
                'email': user.email,  
                'plan\_type': user.plan\_type  
            }  
        })  
      
    return jsonify({'success': False, 'message': 'ログイン失敗'}), 401  
\`\`\`

\*\*結果\*\*:   
\- Flask-Login Cookie設定完了  
\- \`/app-index\` へ自動リダイレクト

\---

\#\#\#\# Step 2: AppIndexPage（アプリ一覧）

\*\*画面\*\*: \`AppIndexPage.vue\`

\*\*URL\*\*: \`https://influberry.jp/app-index\`

\*\*表示内容\*\*:  
\`\`\`  
┌──────────────────────────────────────────┐  
│  InfluBerry アプリ一覧             \[設定\] │  
├──────────────────────────────────────────┤  
│                                          │  
│  ┌────────────────────────────────────┐  │  
│  │  📊 BerryManagement               │  │  
│  │  案件・請求書・タスク管理          │  │  
│  │                            \[→\]    │  │  
│  └────────────────────────────────────┘  │  
│                                          │  
│  ┌────────────────────────────────────┐  │  
│  │  🎫 BerryCard                     │  │  
│  │  デジタル名刺・QRコード            │  │  
│  │                            \[→\]    │  │  
│  └────────────────────────────────────┘  │  
│                                          │  
└──────────────────────────────────────────┘  
\`\`\`

\*\*ユーザー操作\*\*:  
\- 「BerryCard」カードをクリック

\*\*フロントエンド処理\*\*:  
\`\`\`javascript  
// AppIndexPage.vue

const navigateTo \= (path) \=\> {  
  router.push(path)  
}

// BerryCardカードクリック時  
navigateTo('/card')  
\`\`\`

\*\*結果\*\*: \`/card\` へ遷移

\---

\#\#\#\# Step 3: CardApp（BerryCardメインページ）

\*\*画面\*\*: \`CardApp.vue\`

\*\*URL\*\*: \`https://influberry.jp/card\`

\*\*レイアウト\*\*:  
\`\`\`  
┌──────────────────────────────────────────────────────────────┐  
│  \[← アプリ一覧へ\]  BerryCard \- デジタル名刺                   │  
├──────────────────────────────────────────────────────────────┤  
│                                                              │  
│  ┌───────────────────────┐  ┌─────────────────────────────┐ │  
│  │  編集パネル           │  │  プレビューパネル            │ │  
│  ├───────────────────────┤  ├─────────────────────────────┤ │  
│  │                       │  │                             │ │  
│  │  \[プロフィール編集\]   │  │  ┌─────────────────────┐   │ │  
│  │  ・アイコン画像       │  │  │   \[プレビュー\]      │   │ │  
│  │  ・名前              │  │  │                     │   │ │  
│  │  ・自己紹介          │  │  │   リアルタイム      │   │ │  
│  │  ・SNSリンク         │  │  │   プレビュー表示    │   │ │  
│  │                       │  │  │                     │   │ │  
│  │  \[デザイン設定\]       │  │  └─────────────────────┘   │ │  
│  │  ・カラー選択        │  │                             │ │  
│  │  ・フォント選択      │  │                             │ │  
│  │  ・レイアウト選択    │  │                             │ │  
│  │                       │  │                             │ │  
│  │  \[QRコード\]           │  │                             │ │  
│  │  ・PNG ダウンロード  │  │                             │ │  
│  │  ・SVG ダウンロード  │  │                             │ │  
│  │  ・vCard ダウンロード│  │                             │ │  
│  │                       │  │                             │ │  
│  │  \[保存\]              │  │                             │ │  
│  └───────────────────────┘  └─────────────────────────────┘ │  
│                                                              │  
└──────────────────────────────────────────────────────────────┘  
\`\`\`

\*\*初回アクセス時の処理\*\*:

1\. \*\*プロフィールデータ取得\*\*:  
\`\`\`javascript  
// stores/profiles.js

// CardApp.vue マウント時  
onMounted(async () \=\> {  
  await profileStore.fetchProfile()  
})

// Pinia Store  
async fetchProfile() {  
  const response \= await axios.get(  
    \`${API\_BASE\_URL}/api/profiles/me\`,  
    { withCredentials: true }  
  )  
  this.profile \= response.data  
}  
\`\`\`

2\. \*\*Flask API処理\*\*:  
\`\`\`python  
\# app/blueprints/profiles.py

@profiles\_bp.route('/api/profiles/me', methods=\['GET'\])  
@login\_required  
def get\_profile():  
    user \= current\_user  
    return jsonify({  
        'id': user.id,  
        'username': user.username,  
        'influencer\_name': user.influencer\_name,  
        'bio': user.bio,  
        'icon\_url': f'/static/uploads/icons/{user.icon\_filename}' if user.icon\_filename else None,  
        \# ... 全フィールド  
    })  
\`\`\`

3\. \*\*プレビュー表示\*\*:  
\`\`\`javascript  
// ProfilePreview.vue

// computed で自動更新  
const previewProfile \= computed(() \=\> profileStore.profile)  
\`\`\`

\---

\#\#\#\# Step 4: プロフィール編集

\*\*ユーザー操作\*\*:  
1\. 名前を入力: 「さくら」  
2\. 自己紹介を入力: 「Z世代インフルエンサーです！」  
3\. アイコン画像をアップロード

\*\*フロントエンド処理（リアルタイムプレビュー）\*\*:  
\`\`\`javascript  
// ProfileEditForm.vue

const localProfile \= reactive({  
  influencerName: '',  
  bio: '',  
  iconUrl: null  
})

// 入力イベント  
const emitUpdate \= () \=\> {  
  emit('update', localProfile)  
}

// CardApp.vue  
const handleProfileUpdate \= (updatedData) \=\> {  
  // Storeローカル更新（サーバー送信なし）  
  profileStore.updateProfileLocal(updatedData)  
}  
\`\`\`

\*\*結果\*\*:   
\- プレビューがリアルタイム更新  
\- サーバーには未送信（保存ボタンクリック時に送信）

\---

\#\#\#\# Step 5: プロフィール保存

\*\*ユーザー操作\*\*:  
\- 「プロフィールを保存」ボタンクリック

\*\*フロントエンド処理\*\*:  
\`\`\`javascript  
// ProfileEditForm.vue

const saveProfile \= async () \=\> {  
  saving.value \= true  
  try {  
    await profileStore.updateProfile(localProfile)  
    alert('プロフィールを保存しました')  
  } catch (error) {  
    alert('保存に失敗しました')  
  } finally {  
    saving.value \= false  
  }  
}  
\`\`\`

\*\*バックエンド処理\*\*:  
\`\`\`python  
\# app/blueprints/profiles.py

@profiles\_bp.route('/api/profiles/me', methods=\['PUT'\])  
@login\_required  
def update\_profile():  
    data \= request.get\_json()  
    user \= current\_user  
      
    \# 更新  
    user.influencer\_name \= data.get('influencer\_name')  
    user.bio \= data.get('bio')  
    \# ...  
      
    db.session.commit()  
      
    \# QRコード自動再生成  
    generate\_qr\_code\_file(user)  
      
    return jsonify({  
        'success': True,  
        'profile': { /\* 更新後データ \*/ }  
    })  
\`\`\`

\*\*結果\*\*:  
\- データベース更新  
\- QRコード自動生成  
\- プロフィールページURL有効化: \`https://influberry.jp/@さくら\`

\---

\#\#\#\# Step 6: QRコードダウンロード

\*\*ユーザー操作\*\*:  
1\. 「PNG ダウンロード」ボタンクリック

\*\*フロントエンド処理\*\*:  
\`\`\`javascript  
// QRCodeDownload.vue

const downloadQR \= async (format) \=\> {  
  await profileStore.downloadQrCode(format)  
}

// stores/profiles.js  
async downloadQrCode(format \= 'png') {  
  const response \= await axios.get(  
    \`${API\_BASE\_URL}/api/profiles/me/download-qr?format=${format}\`,  
    {  
      withCredentials: true,  
      responseType: 'blob'  
    }  
  )

  // ダウンロード処理  
  const url \= window.URL.createObjectURL(new Blob(\[response.data\]))  
  const link \= document.createElement('a')  
  link.href \= url  
  link.setAttribute('download', \`${this.profile.username}\_qr.${format}\`)  
  document.body.appendChild(link)  
  link.click()  
  link.remove()  
}  
\`\`\`

\*\*結果\*\*:  
\- \`さくら\_qr.png\` がダウンロード  
\- QRコードスキャンで \`https://influberry.jp/@さくら\` へアクセス可能

\---

\#\#\#\# Step 7: 公開プロフィールページ確認

\*\*ユーザー操作\*\*:  
1\. ブラウザで \`https://influberry.jp/@さくら\` にアクセス  
2\. または QRコードをスキャン

\*\*バックエンド処理\*\*:  
\`\`\`python  
\# app/blueprints/profiles.py

@profiles\_bp.route('/@\<username\>')  
def public\_profile\_username(username):  
    \# クローラーブロック  
    user\_agent \= request.headers.get('User-Agent', '').lower()  
    if is\_crawler(user\_agent):  
        abort(403)  
      
    user \= User.query.filter\_by(username=username).first\_or\_404()  
      
    if not user.profile\_public:  
        abort(404)  
      
    return render\_template('profiles/public\_profile.html', user=user)  
\`\`\`

\*\*表示内容\*\*:  
\`\`\`html  
\<\!-- public\_profile.html \--\>  
\<\!DOCTYPE html\>  
\<html\>  
\<head\>  
    \<meta charset="UTF-8"\>  
    \<meta name="robots" content="noindex, nofollow"\>  
    \<title\>さくら \- InfluBerry\</title\>  
    \<link href="https://fonts.googleapis.com/css2?family=Nunito" rel="stylesheet"\>  
\</head\>  
\<body style="background-color: \#FFD4C4; font-family: Nunito;"\>  
    \<div class="profile-card layout-simple"\>  
        \<img src="/static/uploads/icons/user\_123\_icon.jpg" alt="アイコン"\>  
        \<h1\>さくら\</h1\>  
        \<p\>Z世代インフルエンサーです！\</p\>  
          
        \<\!-- SNSリンク \--\>  
        \<div class="sns-links"\>  
            \<a href="https://tiktok.com/@sakura"\>\<img src="/icons/tiktok.svg"\>\</a\>  
            \<a href="https://instagram.com/sakura"\>\<img src="/icons/instagram.svg"\>\</a\>  
        \</div\>  
          
        \<\!-- LINE QRコード \--\>  
        \<div class="line-qr-section"\>  
            \<p\>LINEで友だち追加\</p\>  
            \<img src="/static/uploads/line\_qrcodes/user\_123\_line\_qr.png"\>  
        \</div\>  
    \</div\>  
\</body\>  
\</html\>  
\`\`\`

\*\*結果\*\*:  
\- 公開プロフィールページ表示  
\- ユーザー設定したデザイン反映  
\- SNSリンク・LINE QRコード表示

\---

\#\#\# 3\. フロー全体のシーケンス図

\`\`\`  
ユーザー    AuthPage    auth.js    Flask    DB    AppIndexPage    CardApp    profiles.js    Flask    ProfilePreview  
  │           │           │         │       │         │            │           │            │           │  
  │──ログイン──→│           │         │       │         │            │           │            │           │  
  │           │─login()──→│         │       │         │            │           │            │           │  
  │           │           │─POST───→│       │         │            │           │            │           │  
  │           │           │         │─認証──→│         │            │           │            │           │  
  │           │           │         │←─OK──│         │            │           │            │           │  
  │           │           │←Cookie─│       │         │            │           │            │           │  
  │           │           │─push──────────────────→│            │           │            │           │  
  │           │           │         │       │         │            │           │            │           │  
  │←──────────────────────────────────────AppIndex表示│            │           │            │           │  
  │                       │         │       │         │            │           │            │           │  
  │─BerryCardクリック──────────────────────────────→│            │           │            │           │  
  │                       │         │       │         │            │           │            │           │  
  │←────────────────────────────────────────────CardApp表示────────│            │           │  
  │                       │         │       │         │            │           │            │           │  
  │                       │         │       │         │            │─fetch────→│            │           │  
  │                       │         │       │         │            │           │─GET───────→│           │  
  │                       │         │       │         │            │           │            │─SELECT──→│  
  │                       │         │       │         │            │           │            │←─data───│  
  │                       │         │       │         │            │           │←─profile──│           │  
  │                       │         │       │         │            │←─profile──│            │           │  
  │                       │         │       │         │            │           │            │           │  
  │←──────────────────────────────────────────────初期表示─────────────────────────────────────────→│  
  │                       │         │       │         │            │           │            │           │  
  │─入力──────────────────────────────────────────→│            │           │            │           │  
  │                       │         │       │         │            │─update────→│            │           │  
  │                       │         │       │         │            │           │─local更新──│           │  
  │←──────────────────────────────────────────────プレビュー更新─────────────────────────────────────→│  
  │                       │         │       │         │            │           │            │           │  
  │─保存クリック───────────────────────────────────→│            │           │            │           │  
  │                       │         │       │         │            │─save─────→│            │           │  
  │                       │         │       │         │            │           │─PUT───────→│           │  
  │                       │         │       │         │            │           │            │─UPDATE──→│  
  │                       │         │       │         │            │           │            │←─OK─────│  
  │                       │         │       │         │            │           │            │─QR生成──→│  
  │                       │         │       │         │            │           │←─success──│           │  
  │←──────────────────────────────────────────────保存完了通知─────────────────────────────────────────│  
\`\`\`

\---

\#\#\# 4\. 認証状態の維持

\*\*Flask-Login Cookie認証の仕組み\*\*:

1\. \*\*ログイン時\*\*:  
\`\`\`python  
login\_user(user)  \# Flask-Loginがセッション作成  
\# Cookie: session=xxxxx (HttpOnly, Secure)  
\`\`\`

2\. \*\*以降のリクエスト\*\*:  
\`\`\`python  
@login\_required  \# デコレータで自動認証チェック  
def get\_profile():  
    user \= current\_user  \# Flask-Loginが自動取得  
\`\`\`

3\. \*\*フロントエンド\*\*:  
\`\`\`javascript  
// 全リクエストでCookie送信  
axios.get(url, { withCredentials: true })  
\`\`\`

\*\*セッション有効期限\*\*:  
\- デフォルト: ブラウザ閉じるまで  
\- 「ログイン状態を保持」: 30日間

\---

\#\#\# 5\. エラーハンドリング

\*\*認証エラー時\*\*:  
\`\`\`javascript  
// router/index.js

router.beforeEach(async (to, from, next) \=\> {  
  if (to.meta.requiresAuth) {  
    if (\!authStore.isAuthenticated) {  
      // 認証チェック  
      try {  
        await authStore.checkAuth()  
        next()  
      } catch (error) {  
        // 認証失敗 → /auth へリダイレクト  
        next('/auth')  
      }  
    } else {  
      next()  
    }  
  } else {  
    next()  
  }  
})  
\`\`\`

\*\*API エラー時\*\*:  
\`\`\`javascript  
// stores/profiles.js

async fetchProfile() {  
  try {  
    const response \= await axios.get(...)  
    this.profile \= response.data  
  } catch (error) {  
    if (error.response?.status \=== 401\) {  
      // 認証切れ → ログインページへ  
      router.push('/auth')  
    } else {  
      // その他エラー表示  
      alert('プロフィールの取得に失敗しました')  
    }  
  }  
}  
\`\`\`

\---

\#\# まとめ

\#\#\# フロー要約

1\. \*\*ログイン\*\*: \`/auth\` → Cookie認証  
2\. \*\*アプリ一覧\*\*: \`/app-index\` → BerryCardカード選択  
3\. \*\*BerryCard\*\*: \`/card\` → プロフィール編集  
4\. \*\*保存\*\*: データベース更新 → QRコード生成  
5\. \*\*公開\*\*: \`/@username\` でプロフィール表示

\#\#\# 重要ポイント

\- ✅ ログイン後は必ず \`/app-index\` へリダイレクト  
\- ✅ Flask-Login Cookie認証で全API保護  
\- ✅ リアルタイムプレビューはローカル更新（サーバー非送信）  
\- ✅ 保存時にQRコード自動生成  
\- ✅ 公開プロフィールページはクローラーブロック

\---

\*\*以上がユーザーログインからBerryCard利用までの完全なフローです。\*\*

