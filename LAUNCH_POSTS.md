# 集客用・投稿文テンプレ(コピペ用)

URLを自分のものに差し替えてから使ってください。

---

## X(英語)— 公開初日

> AI API free tiers keep changing silently. Gemini's quota, Groq's limits, OpenAI's prices — I got tired of re-checking pricing pages.
>
> So I built FreeTierWatch: every major AI API free tier, re-verified automatically every day.
>
> Runs on $0/month infra. Link below 👇

(リプライにURL+スクリーンショット。#buildinpublic #indiehacker)

## X(日本語)

> AI APIの無料枠、いつの間にか変わってて焦ること多くないですか?
>
> 主要AI API(Gemini/OpenAI/Claude/Groq…)の無料枠と料金を毎日自動で再検証するサイトを作りました。日本語表示にも対応。
>
> 維持費は月0円(GitHub Actions+Gemini無料枠)。仕組みも全部公開してます👇

## Hacker News(Show HN)

タイトル:
> Show HN: FreeTierWatch – AI API free tiers, auto-verified daily

本文:
> Free-tier quotas for LLM APIs change without notice (Gemini's free tier has shifted multiple times). I built a static site that re-verifies every provider's official pricing page daily using GitHub Actions + the Gemini free tier itself, and publishes a diff log.
>
> The whole thing runs at $0/month: the repo is the database (JSON), Pages is the host, Actions is the cron. Happy to answer questions about the fail-soft design for free-tier rate limits.

(HNは謙虚で技術的な語り口が一番伸びます。宣伝臭NG)

## Reddit r/SideProject

> I built a site that tracks every AI API free tier (because they keep changing silently)
>
> Last month a free quota I relied on quietly dropped. So I built FreeTierWatch — it fetches each provider's official pricing page every day, uses a free-tier LLM to detect changes, and publishes the current limits + a changelog. Total running cost: $0/month (GitHub Actions cron + Pages hosting + Gemini free tier). Would love feedback on what services to add.

## 週次投稿テンプレ(サイトのRecent changesを見て埋めるだけ)

> 📊 This week in AI API free tiers:
> - {サービス名}: {変更内容}
> - {サービス名}: {変更内容}
> Nothing else changed. Tracked daily at {URL}

## Zenn/note記事ネタ(Gumroad導線用)

タイトル案: 「月0円でAIサイトを毎日自動運用する構成(GitHub Actions+Gemini無料枠)」
構成: 困りごと → アーキテクチャ図 → ハマりどころ(cron遅延、60日停止、無料枠変動) → コード解説 → 「テンプレ・詳細ガイドはこちら(Gumroad)」
