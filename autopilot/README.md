# Leads on Autopilot ⚙️ (free · decentralized)

An always-on lead engine that runs **in GitHub's cloud on a cron — off your machine — for $0**.
It implements the six GTM shifts from the video with zero paid tools:

| Shift | How we do it, free |
|---|---|
| 1 · Company sourcing | **OpenStreetMap Overpass** — the free "Google Maps" for local businesses (no key) |
| 2 · Contact finding | Fetch the site → **HTML→text** (BeautifulSoup) → extract a **verified public email** + owner name |
| 3 · Agentic cron | **GitHub Actions `schedule:`** — decentralized, runs daily in the cloud |
| 4 · Goal mode | Loops until it finds *N* new **qualified** leads (weak/no site + a real email) |
| 5 · Auto research | **Groq (free LLM)** writes a truthful hook + first-touch email + a daily run digest (`logs/`) |
| 6 · Open-source tech | `requests` + `BeautifulSoup` + tech-signature detection — no BuiltWith, no ZenRows |

## What it does each run
Picks a rotating **city × niche** slice (see `config.json`), sources local businesses, keeps only
those with a **weak or missing website AND a verified public email** (never a guessed address), writes
a warm, truthful first-touch email in the lead's language, and **appends them straight into the cockpit**
(`_clients.json` → the outreach console). New leads appear on the console within ~20 min (the Pages cron redeploys).

## Run it
- **Automatically:** daily at 06:30 UTC (edit the cron in `.github/workflows/autopilot.yml`).
- **Now:** Actions tab → "Leads on Autopilot" → **Run workflow**.

## Config (`config.json`)
- `target_new_per_run` — how many new leads per run (default 6)
- `areas` / `niches` — the rotation pool; add your own cities and business types
- `groq_model` — the free Groq model used for the copy

## Requirements
- **`GROQ_API_KEY`** repo secret (free at console.groq.com). Without it, the engine still runs and uses
  clean template emails — you just lose the AI-personalised hook.
- Nothing else. No paid APIs, no server, no cost.

## Guardrails
- **Verified public emails only** — found on the business's own site or its OSM listing; never invented.
- **Truthful copy** — no "we visited your site" fabrications, no em-dashes, warm human B2B.
- **Never re-adds a lead** — dedupes against the whole cockpit + `_seen.json` history.
