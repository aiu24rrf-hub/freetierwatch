# FreeTierWatch 🟢

**Every AI API free tier — tracked and auto-verified daily.**

Free-tier limits and pricing for Gemini, OpenAI, Claude, Groq, Mistral and other AI APIs change without warning. FreeTierWatch re-verifies them every day, automatically, and publishes the results as a fast static page.

## How it works

- `index.html` — a single-file static site (no build step, no framework). Renders the tracker table, a cost calculator, and a change log from `data/*.json`.
- `data/services.json` — the dataset: free-tier limits, caveats, paid pricing, source URLs, confidence levels.
- `scripts/update_data.py` — the daily verifier. Fetches each provider's official pricing page, uses the Gemini API free tier to detect changes, updates the dataset, and appends to `data/changelog.json`.
- `.github/workflows/update.yml` — runs the verifier daily on GitHub Actions and commits any changes.

**Total running cost: $0/month** (GitHub Pages + GitHub Actions on a public repo + Gemini free tier).

## Suggest a service

Open an issue with the service name and its official pricing page URL.

## Disclaimer

Data is collected automatically from public sources and may lag or contain errors. Always verify on the provider's official page before making decisions.
