# FreeTierWatch 完全運用手順書(Fable 5なしで回す版)

これは「AI APIの無料枠・料金を毎日自動追跡する収益サイト」を、**月0円**で公開・運用するための手順書です。プログラミング知識ゼロでも進められるように書いています。所要時間: 初回セットアップ約30〜40分。

---

## 全体像

```
[GitHub Pages(無料)] ← サイト本体(index.html)を世界に公開
        ↑
[data/services.json] ← 無料枠・料金データ
        ↑ 毎朝6:17(日本時間)に自動更新
[GitHub Actions(無料)] → 各社の公式料金ページを取得
        → [Gemini API 無料枠] が変更を検出 → データを自動書き換え
```

一度動き出せば、あなたが何もしなくても毎日データが検証・更新され続けます。

---

## STEP 1: GitHubアカウントを作る(5分)

1. https://github.com/signup を開く
2. メールアドレス・パスワード・ユーザー名を決めて登録(無料プランでOK)
3. ユーザー名は後でサイトのURLになります: `ユーザー名.github.io/freetierwatch`

## STEP 2: リポジトリを作ってファイルを上げる(10分)

1. GitHubにログイン → 右上の「+」→「New repository」
2. Repository name: `freetierwatch` / **Public** を選択(Publicだと Actions が完全無料)→「Create repository」
3. 「uploading an existing file」リンクをクリック
4. 納品zipを解凍してできた **フォルダの中身全部**(index.html、data、scripts、.github など)をドラッグ&ドロップ
   - ⚠️ `.github` フォルダは隠しフォルダです。見えない場合はOSの「隠しファイルを表示」をONに
   - ⚠️ アップロード画面に `.github` がドラッグできない場合: 「Add file → Create new file」でファイル名に `.github/workflows/update.yml` と入力し、中身をコピペしてもOK
5. 「Commit changes」を押す

## STEP 3: サイトを公開する — GitHub Pages(3分)

1. リポジトリ画面 → Settings → 左メニュー「Pages」
2. 「Source」を **Deploy from a branch** に、Branch を **main** / **(root)** にして Save
3. 1〜2分待つと `https://あなたのユーザー名.github.io/freetierwatch/` でサイトが世界公開されます

## STEP 4: Gemini APIキーを取る(5分・無料)

1. https://aistudio.google.com/apikey を開く(Googleアカウントでログイン)
2. 「Create API key」→ キーをコピー(`AIza...` で始まる文字列)
3. **お金は一切かかりません**(無料枠内で動くよう設計済み。1日15サービス×1回だけ呼ぶので余裕)

## STEP 5: APIキーをGitHubに登録する(3分)

1. リポジトリ → Settings → 左メニュー「Secrets and variables」→「Actions」
2. 「New repository secret」
3. Name: `GEMINI_API_KEY` / Secret: さっきのキーを貼り付け → Add secret

## STEP 6: 自動更新の動作確認(3分)

1. リポジトリ → 「Actions」タブ → 左の「Daily data verification」
2. 「Run workflow」ボタン → 実行
3. 緑のチェック✅が付けば成功。以後、**毎朝6:17(日本時間)に全自動で実行**されます
4. もし赤い✕になっても、サイトは壊れません(失敗時は前日データを保持する設計)

## STEP 7: 収益導線を設定する(15分)

`index.html` の上の方にこのブロックがあります:

```js
const LINKS = {
  kofi: "https://ko-fi.com/YOUR_KOFI_NAME",
  gumroad: "https://YOURNAME.gumroad.com/l/ai-zero-stack",
  repo: "https://github.com/YOUR_GITHUB/freetierwatch"
};
```

GitHub上で index.html を開き、鉛筆アイコン(Edit)で以下を書き換えて Commit:

### 7-1. Ko-fi(投げ銭・ドル建て・審査なし)
1. https://ko-fi.com で登録(無料)→ 自分のページURLをコピー
2. `kofi:` の値を差し替え
3. 受け取りはPayPal連携(PayPalも無料登録)

### 7-2. Gumroad(デジタル商品販売・ドル建て・審査なし)
1. https://gumroad.com で販売者登録(無料)
2. 同梱の `PLAYBOOK.md`(「The $0 AI Stack Playbook」)をPDF化して商品登録(推奨価格: $9〜$19)
3. 商品URLを `gumroad:` に差し替え

### 7-3. repo リンク
`repo:` を自分のリポジトリURLに差し替え(例: `https://github.com/stella/freetierwatch`)

### 7-4. (後日)アフィリエイト
- 表の各サービスへのリンクは、紹介プログラムのあるサービス(例: 一部のAIツールはreferralプログラムあり)に参加したら、`data/services.json` の `source_url` はそのままにして、別途紹介リンクを貼るコンテンツを追加するのが安全です(公式ドキュメントへのリンクを紹介リンクにすると信頼を損ないます)
- Google AdSenseはある程度アクセスが増えてから申請(審査に数週間)

## STEP 8: 集客(ここだけは自動化できない — 調査で判明した唯一のボトルネック)

**調査結果の核心: AIは「作る」を無料にしたが「売る」は人間の仕事。** 最低限これだけやってください:

1. **X(英語)で公開ポスト**: 「I built a site that tracks every AI API free tier daily, because quotas keep changing silently → URL」型。スクショ付き。#buildinpublic タグ
2. **Reddit**: r/SideProject、r/ArtificialIntelligence に「Show」投稿(宣伝臭を消し、「作った理由」を語る)
3. **Hacker News**: 「Show HN: FreeTierWatch – AI API free tiers, verified daily」で投稿(当たれば数万アクセス)
4. **日本語圏**: Xで日本語でも紹介(サイトは日本語表示切替対応済み)、Zennやnoteで「月0円でAIサイトを自動運用する構成」記事を書く → 記事内でGumroadガイドを紹介
5. 週1回でいいので「今週の無料枠変更まとめ」をXに投稿(サイトのRecent changesを見るだけ。これがコンテンツになる)

## 日々のメンテナンス(ほぼゼロ)

- **何もしない**: 毎日の更新は全自動
- **週1(5分)**: Actionsタブが緑か確認。Recent changesを見てXに投稿
- **サービス追加したいとき**: `data/services.json` に同じ形式で1ブロック追加するだけ
- **壊れたとき**: GitHubの無料AI(Copilot)や無料のGemini/ChatGPTに「このリポジトリのこのエラーを直して」とファイルを貼れば直せます。このリポジトリは全部で実質3ファイルの小さな構成なので、どのAIでも理解できます

## お金の流れ(現実的な期待値)

正直な見通し(2026年7月の調査に基づく):

- **最初の1〜2ヶ月**: ほぼ$0。集客の種まき期間
- **当たった場合**(HN/Redditでヒット): Ko-fi数十ドル+Gumroad販売+アクセス増
- **サイトの本当の価値**: 「毎日自動更新される一次データ」は時間とともに価値が増える希少資産。競合の手動サイトは必ず古くなる
- **かかるコスト**: 月0円(だから何ヶ月放置しても損しない。これが最大の強み)

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| サイトが404 | Settings→Pagesの設定を確認。反映に数分かかる |
| Actionsが失敗する | ログを開いてエラー行をコピーし、無料のAIに貼って質問 |
| Geminiの無料枠が変わった | `scripts/update_data.py` の `GEMINI_MODEL` を当時の無料モデル名に変える |
| データが古くなった | Actionsタブ→Run workflowで手動実行 |
