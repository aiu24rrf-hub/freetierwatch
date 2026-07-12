# 今日やることシート(英語が読めなくてもできる版)

**最初に大事なコツ**: 英語のページが出たら、ページの上で右クリック →「日本語に翻訳」を選ぶと、画面全体が日本語になります。以下の作業は全部これでOKです。

---

## ① 使い終わったトークンを削除(1分)

1. https://github.com/settings/tokens を開く
2. 「freetierwatch setup」の右にある「Delete」(赤いボタン)を押す → 確認が出たらもう一度押す

## ② Ko-fi(投げ銭の受け皿)を作る(10分)

1. https://ko-fi.com を開く(右クリック→日本語に翻訳)
2. 「Sign up(登録)」→ **Googleアカウントで登録**が一番簡単
3. ページ名を聞かれたら: `FreeTierWatch`
4. URL用の名前(英数字)を聞かれたら: `freetierwatch`(使われていたら `aiu24rrf` など)
5. 登録後、自分のページのURLをメモする(例: `https://ko-fi.com/freetierwatch`)
6. お金の受け取り設定(PayPal連携)は「後で」でもOK。売上が出てからでも設定できます

## ③ Gumroad(PDF販売)に出品する(15分)

1. https://gumroad.com を開く(右クリック→日本語に翻訳)→ 登録(Googleで可)
2. 「New product(新しい商品)」を押す
3. 商品名にこれを貼り付け:
   ```
   The $0 AI Stack Playbook — Run always-on AI apps for free
   ```
4. 種類は「Digital product(デジタル商品)」、価格は `12`(ドル)
5. ファイルのアップロード欄に、チャットで受け取った `The-0-Dollar-AI-Stack-Playbook.pdf` をアップロード
6. 説明欄にこれを貼り付け:
   ```
   Free-tier quotas change. Subscriptions end. Your app shouldn't die with them.

   This playbook shows you the exact stack behind FreeTierWatch (a live site that re-verifies 15 AI API free tiers every morning, on $0/month): GitHub Actions as a free cron engine, free LLM API tiers as the brain, and static hosting as the face. Copy-paste templates included — the workflow YAML, a zero-dependency Gemini call, fail-soft design rules, and the honest monetization order that works at small scale (plus the verified dead-ends to skip).

   9 pages. No fluff. Fork the live repo and have your own always-on AI app running tonight.
   ```
7. 「Publish(公開)」を押す → 商品ページのURLをメモする

## ④ サイトに②③のリンクを埋め込む(5分)

1. https://github.com/aiu24rrf-hub/freetierwatch/edit/main/index.html を開く(編集画面に直接飛びます)
2. キーボードで Ctrl+F(Macは Cmd+F)を押し、`YOUR_KOFI_NAME` を検索
3. その行の `https://ko-fi.com/YOUR_KOFI_NAME` を、②でメモした自分のURLに書き換える
4. すぐ下の行の `https://YOURNAME.gumroad.com/l/ai-zero-stack` を、③でメモした商品URLに書き換える
5. 右上の緑「Commit changes...」→ もう一度緑ボタン

## ⑤ X(Twitter)で公開投稿(10分)

サイトを開いてスクリーンショットを1枚撮っておく → 下の2本をそのまま投稿(画像添付推奨)。

**日本語ポスト:**
```
AI APIの無料枠、いつの間にか変わってて焦ること多くないですか?

主要AI API(Gemini/OpenAI/Claude/Groq…)の無料枠と料金を毎日自動で再検証するサイトを作りました。日本語表示にも対応。

維持費は月0円(GitHub Actions+Gemini無料枠)で全自動運用です👇
https://aiu24rrf-hub.github.io/freetierwatch/
```

**英語ポスト(意味: 「無料枠は黙って変わるので、毎日自動検証するサイトを作った」):**
```
AI API free tiers keep changing silently. Gemini's quota, Groq's limits, OpenAI's prices — I got tired of re-checking pricing pages.

So I built FreeTierWatch: every major AI API free tier, re-verified automatically every day. Runs on $0/month infra.

https://aiu24rrf-hub.github.io/freetierwatch/
```

## ⑥(任意・今週中のどこかで)Hacker NewsとReddit

英語コミュニティへの投稿で、当たれば一番大きいやつです。文面はリポジトリ内の `LAUNCH_POSTS.md` にあります。やる場合は火〜木の日本時間22時以降に。アカウント作成が必要なので、無理せず「毎週火曜の自動レポート」に慣れてからでもOKです。

---

## これが終わったら

あとは何もしなくても回ります。**毎週火曜の朝、Claudeから週次レポートが自動で届きます**(投稿文のコピペ用テキスト付き・全部日本語)。それを見てXに貼るだけ、週5分です。
