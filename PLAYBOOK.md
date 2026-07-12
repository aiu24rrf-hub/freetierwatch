# The $0 AI Stack Playbook

**Run real, always-on AI apps without paying for anything.**

This is the exact stack behind FreeTierWatch — a website that fetches, analyzes and republishes data every single day, with an LLM in the loop, for a total infrastructure cost of $0.00/month. Everything here is copy-paste ready.

---

## Part 1: The Stack

Three free building blocks cover 90% of what indie AI projects need:

### 1. The cron engine — GitHub Actions (public repos: free, unlimited)

GitHub Actions on a **public** repository gives you free scheduled compute. A workflow file in `.github/workflows/` turns your repo into a machine that wakes up on a schedule, runs your script, and commits the results.

```yaml
name: Daily job
on:
  schedule:
    - cron: "17 6 * * *"    # every day 06:17 UTC — pick odd minutes, :00 is congested
  workflow_dispatch: {}      # adds a manual "Run" button
permissions:
  contents: write
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: python job.py
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
      - run: |
          git config user.name "bot"
          git config user.email "actions@github.com"
          git add -A
          git diff --cached --quiet || git commit -m "auto: $(date -u +%F)"
          git push
```

**Gotchas learned the hard way:**
- Scheduled runs can be delayed 5–30 min at busy times. Never build anything time-critical on them.
- GitHub disables schedules on repos with no activity for 60 days. The trick above (committing a data change daily) keeps it alive automatically.
- Always add `workflow_dispatch` so you can test manually.

### 2. The brain — free LLM API tiers

| Provider | Free tier (verify before relying — these shift) | Best use |
|---|---|---|
| Google Gemini (Flash class) | ~1,000+ requests/day class quota via AI Studio key | Default choice: summarize, extract, classify |
| Groq | Generous free requests, extremely fast open models | High-volume, low-stakes calls |
| Mistral La Plateforme | Free tier on small models | Backup / EU option |
| OpenRouter | Rotating `:free` models | Experiments, model variety |

**Design rules for free tiers:**
1. **Treat quotas as weather, not contracts.** They change without notice. Your code must fail soft: on API error, keep yesterday's output, never crash the pipeline.
2. **One call per item per day is plenty.** Batch and sleep (`time.sleep(5)`) between calls — you'll never hit rate limits.
3. **Force JSON out of the model** with an explicit schema in the prompt, then parse defensively (regex out the first `{...}` block; on parse failure, skip and keep old data).

Minimal Gemini call with zero dependencies (Python stdlib only — nothing to install):

```python
import json, os, re, urllib.request

def ask_gemini(prompt: str) -> str:
    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           "gemini-2.5-flash:generateContent?key=" + os.environ["GEMINI_API_KEY"])
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                       "generationConfig": {"temperature": 0.1}}).encode()
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]

def extract_json(text: str):
    m = re.search(r"\{[\s\S]*\}", text)
    return json.loads(m.group(0)) if m else None
```

### 3. The face — free static hosting

- **GitHub Pages**: zero config, serves your repo's `index.html` at `username.github.io/repo`. Perfect partner for Actions: the workflow commits new JSON, Pages serves it instantly. This is the magic loop: **cron writes data → the same repo IS the website.**
- **Cloudflare Pages**: custom domains, faster, still free.
- Architecture rule: **no backend, no database.** Your "database" is a JSON file in the repo. Git history is your free audit log and backup. The frontend `fetch()`es the JSON. This eliminates every hostable, billable, hackable component.

---

## Part 2: The Pattern — "Fetch → Think → Publish"

Almost every useful $0 AI app is the same three-step loop:

```
[FETCH]  urllib gets a public page / RSS feed / API
[THINK]  a free-tier LLM extracts, compares, summarizes → JSON
[PUBLISH] commit JSON → static site re-renders → (optional) notify
```

Concrete apps you can build with this exact loop by changing ~20 lines:

1. **A change tracker** (this site): watch pricing pages, changelogs, terms-of-service, government announcements. LLM diffs against stored state. *Value: freshness — humans can't compete.*
2. **A niche daily digest**: fetch 5 RSS feeds, LLM picks and summarizes the top items, publish as a page + RSS. *Value: curation of a niche too small for media.*
3. **A monitoring alarm**: watch a price / stock status / keyword; when the LLM detects the condition, the workflow opens a GitHub Issue — which emails you for free. (No email service needed: `gh issue create` inside the workflow.)
4. **A dataset that appreciates**: every daily run appends a row. After a year you own a unique time-series nobody else has — that's sellable content by itself.

**The "diff log" trick:** always store a changelog of what changed and when (see `data/changelog.json` in this repo). The changelog *is* your marketing: every week, post "what changed this week" to X/Reddit. Your site generates its own content.

---

## Part 3: Monetization that actually works at small scale

Honest expectations, based on documented cases rather than hype: traffic is the bottleneck, not the tech. Plan monetization in this order:

1. **Ko-fi / Buy Me a Coffee (day 1)** — no approval, no traffic threshold, paid in USD. Put it on the site from the start; it converts once the site saves people time.
2. **A Gumroad product (week 1)** — package your knowledge (like this playbook), $9–19. No approval process. Digital products convert far better from "builder" audiences (X/HN/Reddit) than ads ever will.
3. **Referral programs of tools you list (month 1+)** — many AI/dev tools pay recurring referral commissions. Rule: keep official-docs links honest; put referral links in separate "review/guide" content.
4. **AdSense (only after real traffic)** — needs review and volume; do it last, or never.

**What NOT to do** (all verified dead-ends in 2025-26): mass AI content sites (Google penalizes), AI books on KDP (Amazon caps + disclosure), AI templates on Etsy (policy crackdown), autonomous trading bots (documented capital losses).

---

## Part 4: Distribution (the part AI can't do for you)

A famous 2026 experiment let an AI agent work 72 hours straight: it produced 7 products and 150 posts — and earned $0. Supply is free now; demand is not. Budget human time for exactly this:

- **Launch once, properly:** "Show HN: ..." on Hacker News + r/SideProject on Reddit + a screenshot thread on X. One good launch beats 100 automated posts.
- **Let the machine feed you content:** your daily diff log = a weekly "what changed" post. 5 minutes/week.
- **Answer questions where your users already are** (Reddit/Discord/Stack Overflow) with a genuinely helpful answer + link. Slow, compounding, and the only channel that never gets platform-banned.

---

## Part 5: Keep it alive with zero budget

- Everything is 3 files: one HTML, one Python script, one YAML. Any free AI assistant (Gemini, ChatGPT free, Copilot) can fix or extend it — paste the file and the error.
- Fail-soft design means the worst case is "data is one day stale," never "site is down."
- Cost of abandoning it for 6 months: $0. Cost of restarting: one manual workflow run. **A $0 asset never expires — you can't lose; you can only not-yet-win.**

---

*Built with the stack it describes. Fork it, change the FETCH target, and you have your own always-on AI app by tonight.*
