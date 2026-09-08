# BidSignal

BidSignal is a low-cost tender opportunity radar for small businesses, agencies and independent consultants.

## Core promise

**Tell us what you sell. We scan public procurement notices and send only the opportunities worth opening.**

The first data source is TED (Tenders Electronic Daily), the EU's official public procurement database. Published-notice search is openly accessible and does not require an API key.

## Pricing hypothesis

- Free: weekly digest, 1 profile, top 5 matches
- Pro: $7.90/month, daily digest, up to 5 profiles, top 20 matches
- Annual: $59/year

Target: roughly 39 monthly Pro users = $308.10 MRR before payment/infrastructure costs.

## MVP

- Fetches fresh TED notices
- Scores every notice against configurable business profiles
- Filters noisy low-relevance results
- Generates JSON and HTML digest files
- Runs without an AI API or paid data provider
- Designed to run daily through GitHub Actions

## Structure

- `fetch_tenders.py` — collector, normalizer, scorer and digest generator
- `profiles.json` — sample business profiles
- `site/index.html` — public product page/demo
- `data/latest.json` — machine-readable matches
- `data/latest.html` — latest digest
- `.github/workflows/bidsignal-daily.yml` — daily automation (repository root)

## Run

```bash
cd projects/bidsignal
python fetch_tenders.py
```

No third-party Python packages are required.

## Product strategy

Do not add paid AI until people subscribe. The initial ranking is deterministic and explainable. AI can later summarize long tender notices, classify eligibility and draft a first-response checklist once demand is proven.
