# RivalBrief — MVP

RivalBrief is a lightweight competitor-intelligence product for small ecommerce teams.

## Positioning

**Stop checking competitor tabs. Get one brief telling you what actually changed.**

The product is intentionally narrower and cheaper than enterprise competitive-intelligence suites. The initial customer is a small DTC / Shopify merchant tracking 3–10 direct competitors.

### Signals in the MVP

- homepage / landing-page copy changes
- promotion language (sale, discount, bundle, free shipping, buy X get Y)
- visible price signals and JSON-LD product prices when present
- new or removed high-signal text
- a ranked Markdown brief instead of a raw diff

### Target price

- Beta: $19/month
- Standard target: $29/month for up to 10 competitors
- Goal: 11 Standard customers = $319 MRR, roughly the $10/day target before infrastructure/payment costs

## Files

- `site/index.html` — sellable landing page + interactive product demo
- `monitor.py` — fetches configured competitor pages, extracts signals and compares snapshots
- `config.json` — sites to monitor
- `data/state.json` — persisted snapshots
- `data/latest.json` — latest machine-readable result
- `data/latest-report.md` — generated human-readable brief
- `.github/workflows/rivalbrief-monitor.yml` — scheduled GitHub Actions job

## Run locally

```bash
python -m pip install -r requirements.txt
python monitor.py
```

Edit `config.json` and replace the example URLs with actual competitors.

## Current MVP limitations

This version deliberately uses no paid AI API and no billing provider. It proves the monitoring loop first. JavaScript-heavy sites, anti-bot protections, login-gated pages and marketplace pages may require browser rendering or a dedicated data provider later.

The next commercial milestone is: deploy the landing page, wire a lead-capture endpoint, recruit 5 design partners, then add AI summarization only after users prove they value the brief.
