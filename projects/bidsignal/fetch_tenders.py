import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
PROFILES = json.loads((ROOT / "profiles.json").read_text(encoding="utf-8"))

TED_SEARCH_URL = "https://api.ted.europa.eu/v3/notices/search"
MAX_LOOKBACK_DAYS = 7
PAGE_SIZE = 250
MAX_ITERATION_PAGES = 40

TED_FIELDS = [
    "publication-number",
    "notice-title",
    "buyer-name",
    "place-of-performance",
    "estimated-value-proc",
    "estimated-value-cur-proc",
    "deadline-receipt-tender-date-lot",
    "publication-date",
    "notice-type",
    "dispatch-date",
    "contract-nature",
    "description-proc",
    "description-lot",
    "classification-cpv",
    "sme-lot",
]


def post_json(url, payload):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "BidSignal/0.2 (+https://github.com/Frankieee-hub/project)",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:2000]
        raise RuntimeError(f"TED API HTTP {exc.code}: {detail}") from exc


def normalize_text(value):
    """Flatten multilingual/list/dict TED values into one searchable string."""
    if value is None:
        return ""
    if isinstance(value, dict):
        value = " ".join(normalize_text(v) for v in value.values())
    elif isinstance(value, (list, tuple, set)):
        value = " ".join(normalize_text(v) for v in value)
    return re.sub(r"\s+", " ", str(value)).strip()


def truthy(value):
    text = normalize_text(value).lower()
    return text in {"true", "yes", "1", "y"} or "true" in text


def first_link(links):
    if not links:
        return ""
    if isinstance(links, str):
        return links if links.startswith("http") else ""
    if isinstance(links, list):
        for value in links:
            link = first_link(value)
            if link:
                return link
        return ""
    if isinstance(links, dict):
        preferred_keys = ("html", "HTML", "en", "EN")
        for key in preferred_keys:
            if key in links:
                link = first_link(links[key])
                if link:
                    return link
        for value in links.values():
            link = first_link(value)
            if link:
                return link
    return ""


def ted_url(publication_number, links=None):
    direct = first_link(links)
    if direct:
        return direct
    safe = normalize_text(publication_number).replace("/", "-")
    return f"https://ted.europa.eu/en/notice/-/detail/{safe}" if safe else "https://ted.europa.eu/"


def flatten_notice(notice):
    title = normalize_text(notice.get("notice-title"))
    buyer = normalize_text(notice.get("buyer-name"))
    place = normalize_text(notice.get("place-of-performance"))
    nature = normalize_text(notice.get("contract-nature"))
    description = normalize_text([notice.get("description-proc"), notice.get("description-lot")])
    cpv = normalize_text(notice.get("classification-cpv"))
    search_text = " ".join([title, description, cpv, buyer, place, nature]).lower()

    publication_number = normalize_text(notice.get("publication-number"))
    return {
        "publication_number": publication_number,
        "title": title or "Untitled notice",
        "buyer": buyer,
        "place": place,
        "estimated_value": normalize_text(notice.get("estimated-value-proc")),
        "currency": normalize_text(notice.get("estimated-value-cur-proc")),
        "deadline": normalize_text(notice.get("deadline-receipt-tender-date-lot")),
        "publication_date": normalize_text(notice.get("publication-date")),
        "dispatch_date": normalize_text(notice.get("dispatch-date")),
        "notice_type": normalize_text(notice.get("notice-type")),
        "contract_nature": nature,
        "cpv": cpv,
        "sme_suitable": truthy(notice.get("sme-lot")),
        "url": ted_url(publication_number, notice.get("links")),
        "search_text": search_text,
    }


def score_notice(notice, profile):
    text = notice["search_text"]
    title = notice["title"].lower()
    score = 0
    hits = []

    for keyword in profile.get("include", []):
        kw = keyword.strip().lower()
        if not kw or kw not in text:
            continue
        score += 4 if kw in title else 2
        hits.append(keyword)

    for keyword in profile.get("exclude", []):
        kw = keyword.strip().lower()
        if kw and kw in text:
            score -= 6

    countries = [c.strip().lower() for c in profile.get("countries", []) if c.strip()]
    if countries:
        place = notice["place"].lower()
        score += 2 if any(c in place for c in countries) else -3

    if notice.get("sme_suitable"):
        score += 1

    return score, hits


def request_for_date(date_value, token=None):
    payload = {
        "query": f"publication-date = {date_value:%Y%m%d}",
        "fields": TED_FIELDS,
        "limit": PAGE_SIZE,
        "scope": "ACTIVE",
        "checkQuerySyntax": True,
        "paginationMode": "ITERATION",
        "onlyLatestVersions": True,
    }
    if token:
        payload["iterationNextToken"] = token
    return payload


def fetch_publication_day(date_value):
    notices = []
    token = None
    timed_out = False

    for _ in range(MAX_ITERATION_PAGES):
        response = post_json(TED_SEARCH_URL, request_for_date(date_value, token))
        timed_out = timed_out or bool(response.get("timedOut"))
        batch = response.get("notices") or response.get("results") or []
        notices.extend(batch)

        next_token = response.get("iterationNextToken")
        if not next_token or next_token == token or not batch:
            break
        token = next_token

    deduped = {}
    for notice in notices:
        key = normalize_text(notice.get("publication-number"))
        if key:
            deduped[key] = notice

    return list(deduped.values()), timed_out


def fetch_latest_publication_day(now=None):
    now = now or datetime.now(timezone.utc)
    for days_back in range(MAX_LOOKBACK_DAYS + 1):
        candidate = (now - timedelta(days=days_back)).date()
        notices, timed_out = fetch_publication_day(candidate)
        if notices:
            return candidate.isoformat(), notices, timed_out
    return None, [], False


def rank_profiles(notices):
    normalized = [flatten_notice(n) for n in notices]
    output_profiles = []

    for profile in PROFILES:
        matches = []
        for notice in normalized:
            score, hits = score_notice(notice, profile)
            if score < 3:
                continue
            matches.append(
                {
                    **{k: v for k, v in notice.items() if k != "search_text"},
                    "score": score,
                    "hits": hits,
                }
            )

        matches.sort(key=lambda item: (item["score"], item["publication_date"]), reverse=True)
        output_profiles.append({"name": profile["name"], "matches": matches[:20]})

    return normalized, output_profiles


def render_html(payload):
    blocks = []
    for profile in payload["profiles"]:
        rows = []
        for item in profile["matches"]:
            value = ""
            if item["estimated_value"]:
                value = f" · Est. {escape(item['estimated_value'])} {escape(item['currency'])}".rstrip()
            sme = " · SME-friendly" if item.get("sme_suitable") else ""
            rows.append(
                f"""
                <article class='card'>
                  <div class='score'>{item['score']}</div>
                  <div>
                    <h3><a href='{escape(item['url'])}' target='_blank' rel='noopener'>{escape(item['title'])}</a></h3>
                    <p>{escape(item['buyer'] or 'Buyer not listed')} · {escape(item['place'] or 'Location not listed')}</p>
                    <p class='meta'>Published {escape(item['publication_date'] or '—')} · Deadline {escape(item['deadline'] or '—')}{value}{sme}</p>
                    <p class='hits'>Matched: {escape(', '.join(item['hits']) or 'general profile fit')}</p>
                  </div>
                </article>
                """
            )
        empty = "<p>No strong matches on the latest publication day.</p>"
        blocks.append(f"<section><h2>{escape(profile['name'])}</h2>{''.join(rows) or empty}</section>")

    warning = "<p class='warning'>TED reported a partial/timed-out search; this digest may be incomplete.</p>" if payload["timed_out"] else ""
    return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>BidSignal Daily Digest</title>
<style>
body{{font-family:Inter,system-ui,sans-serif;background:#f7f7f5;color:#171717;max-width:920px;margin:auto;padding:32px}}
h1{{font-size:40px;margin-bottom:4px}} .sub{{color:#666;margin-bottom:12px}} .warning{{padding:12px;background:#fff3cd;border-radius:10px}}
section{{margin:34px 0}} .card{{display:grid;grid-template-columns:56px 1fr;gap:16px;background:#fff;border:1px solid #e7e7e2;border-radius:16px;padding:18px;margin:12px 0}}
.score{{width:44px;height:44px;border-radius:12px;background:#171717;color:#fff;display:grid;place-items:center;font-weight:700}}
a{{color:inherit}} h3{{margin:0 0 8px}} p{{margin:5px 0;color:#555}} .meta,.hits{{font-size:14px;color:#777}}
</style></head><body>
<h1>BidSignal</h1>
<p class='sub'>Source day {escape(payload['source_date'] or 'unavailable')} · {payload['notice_count']} notices scanned · generated {escape(payload['generated_at'])}</p>
{warning}{''.join(blocks)}</body></html>"""


def main():
    source_date, notices, timed_out = fetch_latest_publication_day()
    if not notices:
        raise RuntimeError(f"No TED notices found in the last {MAX_LOOKBACK_DAYS + 1} calendar days")

    normalized, profiles = rank_profiles(notices)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "TED",
        "source_date": source_date,
        "notice_count": len(normalized),
        "timed_out": timed_out,
        "profiles": profiles,
    }

    (DATA_DIR / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA_DIR / "latest.html").write_text(render_html(payload), encoding="utf-8")

    match_count = sum(len(profile["matches"]) for profile in profiles)
    print(f"TED {source_date}: scanned {len(normalized)} notices, emitted {match_count} profile matches")


if __name__ == "__main__":
    main()
