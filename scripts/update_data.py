#!/usr/bin/env python3
"""
FreeTierWatch daily updater.

For each service in data/services.json:
  1. Fetch its official source_url.
  2. Ask Gemini (free tier) whether the free tier / pricing shown on the page
     differs from what we have stored.
  3. If it differs, update the entry and append to data/changelog.json.

Designed to run on GitHub Actions for $0/month:
  - Uses only the Gemini free tier (GEMINI_API_KEY secret).
  - Fails soft: any per-service error keeps the old data (never wipes data).
  - If GEMINI_API_KEY is missing, it only refreshes the "last_updated" stamp
    and checks that source URLs are still alive.
"""

import json
import os
import re
import sys
import time
import datetime
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICES_PATH = os.path.join(ROOT, "data", "services.json")
CHANGELOG_PATH = os.path.join(ROOT, "data", "changelog.json")

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent?key={GEMINI_KEY}"
)

TODAY = datetime.date.today().isoformat()
UA = "Mozilla/5.0 (compatible; FreeTierWatch/1.0; +https://github.com)"


def fetch_text(url: str, limit: int = 60000) -> str:
    """Fetch a URL and return crudely de-HTML'd text."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read(400000).decode("utf-8", errors="ignore")
    raw = re.sub(r"<script[\s\S]*?</script>", " ", raw, flags=re.I)
    raw = re.sub(r"<style[\s\S]*?</style>", " ", raw, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\s+", " ", text)
    return text[:limit]


def ask_gemini(prompt: str) -> str:
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 1024},
    }).encode()
    req = urllib.request.Request(
        GEMINI_URL, data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode())
    return data["candidates"][0]["content"]["parts"][0]["text"]


def extract_json(text: str):
    """Pull the first JSON object out of a model response."""
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


PROMPT_TEMPLATE = """You are a precise data checker for a website tracking AI API free tiers.

Here is the CURRENT stored entry (JSON):
{entry}

Here is TEXT scraped today from the official page ({url}):
---
{page}
---

Compare the stored entry with the page text. Respond with ONLY a JSON object:
{{
  "changed": true/false,
  "change_summary": "one short sentence describing what changed (empty string if nothing)",
  "free_tier": "updated short factual free-tier description with numbers",
  "free_tier_notes": "updated caveats",
  "paid_price": "updated short pricing string",
  "price_in_per_m": number or null,
  "price_out_per_m": number or null
}}

Rules:
- Set changed=true ONLY if a number/limit/price on the page clearly differs from the stored entry.
- If the page text is unclear, paywalled, or doesn't contain pricing info, set changed=false and repeat the stored values verbatim.
- Never invent numbers. Keep descriptions under 160 characters.
"""


def main() -> int:
    with open(SERVICES_PATH, encoding="utf-8") as f:
        data = json.load(f)
    try:
        with open(CHANGELOG_PATH, encoding="utf-8") as f:
            changelog = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        changelog = {"changes": []}

    n_checked = n_changed = n_errors = 0

    for svc in data.get("services", []):
        url = svc.get("source_url")
        if not url:
            continue
        try:
            page = fetch_text(url)
            n_checked += 1
        except Exception as e:  # noqa: BLE001
            print(f"[warn] fetch failed for {svc['name']}: {e}")
            n_errors += 1
            continue

        if not GEMINI_KEY:
            # No key: liveness check only.
            svc["last_verified"] = TODAY
            continue

        entry_view = {k: svc.get(k) for k in (
            "name", "free_tier", "free_tier_notes", "paid_price",
            "price_in_per_m", "price_out_per_m")}
        prompt = PROMPT_TEMPLATE.format(
            entry=json.dumps(entry_view, ensure_ascii=False),
            url=url, page=page)
        try:
            result = extract_json(ask_gemini(prompt))
            time.sleep(5)  # stay well inside free-tier rate limits
        except Exception as e:  # noqa: BLE001
            print(f"[warn] gemini failed for {svc['name']}: {e}")
            n_errors += 1
            continue
        if not result:
            print(f"[warn] unparseable response for {svc['name']}")
            n_errors += 1
            continue

        svc["last_verified"] = TODAY
        if result.get("changed"):
            summary = (result.get("change_summary") or "updated").strip()[:200]
            print(f"[change] {svc['name']}: {summary}")
            for k in ("free_tier", "free_tier_notes", "paid_price"):
                if result.get(k):
                    svc[k] = str(result[k])[:300]
            for k in ("price_in_per_m", "price_out_per_m"):
                if isinstance(result.get(k), (int, float)):
                    svc[k] = result[k]
            svc["confidence"] = "high"
            changelog["changes"].insert(0, {
                "date": TODAY, "service": svc["name"], "change": summary})
            n_changed += 1

    data.setdefault("meta", {})["last_updated"] = TODAY
    changelog["changes"] = changelog["changes"][:100]

    with open(SERVICES_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open(CHANGELOG_PATH, "w", encoding="utf-8") as f:
        json.dump(changelog, f, ensure_ascii=False, indent=2)

    print(f"done: checked={n_checked} changed={n_changed} errors={n_errors}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
