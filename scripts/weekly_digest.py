#!/usr/bin/env python3
"""
Weekly marketing digest generator.

Every Tuesday morning (JST) this script:
  1. Reads data/changelog.json for changes in the last 7 days.
  2. Builds ready-to-copy social posts (English + Japanese).
  3. Opens a GitHub Issue containing the drafts.

GitHub emails the repo owner about the new Issue automatically,
so the owner just copies the text into X — no writing needed.

Runs on the free GITHUB_TOKEN that Actions provides. No LLM needed
(deterministic templates = zero extra failure modes).
"""

import datetime
import json
import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANGELOG_PATH = os.path.join(ROOT, "data", "changelog.json")

REPO = os.environ.get("GITHUB_REPOSITORY", "")  # e.g. "stella/freetierwatch"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
SITE_URL = os.environ.get("SITE_URL", "")  # set in workflow env, e.g. https://user.github.io/freetierwatch/

TODAY = datetime.date.today()
WEEK_AGO = TODAY - datetime.timedelta(days=7)


def recent_changes():
    try:
        with open(CHANGELOG_PATH, encoding="utf-8") as f:
            changes = json.load(f).get("changes", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    out = []
    for c in changes:
        try:
            d = datetime.date.fromisoformat(c.get("date", ""))
        except ValueError:
            continue
        if d >= WEEK_AGO and c.get("service") != "FreeTierWatch":
            out.append(c)
    return out


def build_posts(changes):
    url = SITE_URL or f"https://github.com/{REPO}"
    if changes:
        lines_en = "\n".join(f"• {c['service']}: {c['change']}" for c in changes[:6])
        lines_ja = "\n".join(f"・{c['service']}: {c['change']}" for c in changes[:6])
        en = (f"📊 This week in AI API free tiers and pricing:\n\n{lines_en}\n\n"
              f"Everything else held steady. Tracked automatically every day:\n{url}")
        ja = (f"📊 今週のAI API無料枠・料金の変更まとめ:\n\n{lines_ja}\n\n"
              f"それ以外は変更なし。毎日自動追跡中:\n{url}")
    else:
        en = (f"📊 AI API free-tier check: no changes detected this week across "
              f"15 tracked providers (Gemini, OpenAI, Claude, Groq, Mistral...).\n\n"
              f"Quiet weeks are good weeks. Verified daily, automatically:\n{url}")
        ja = (f"📊 今週のAI API無料枠チェック: 追跡中の15サービス(Gemini/OpenAI/Claude/Groq/Mistral…)に変更はありませんでした。\n\n"
              f"変わってないことを毎日自動で確認しています:\n{url}")
    return en, ja


def create_issue(title, body):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/issues",
        data=json.dumps({"title": title, "body": body, "labels": ["weekly-post"]}).encode(),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        print("issue created:", json.loads(r.read()).get("html_url"))


def main():
    changes = recent_changes()
    en, ja = build_posts(changes)
    body = (
        "今週の投稿文が自動生成されました。下をそのままコピーしてXに投稿してください(所要5分)。\n\n"
        "## English (X / global)\n\n```\n" + en + "\n```\n\n"
        "## 日本語 (X / 国内)\n\n```\n" + ja + "\n```\n\n"
        "---\n"
        f"detected changes this week: {len(changes)} / "
        "posting tip: 日本時間22時前後(米国朝)に投稿すると英語圏に届きやすい。\n"
        "投稿したらこのIssueをCloseしてください。"
    )
    create_issue(f"📣 今週の投稿文 ({TODAY.isoformat()}) — コピペ用", body)


if __name__ == "__main__":
    main()
