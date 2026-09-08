from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"
DATA_DIR = ROOT / "data"
STATE_PATH = DATA_DIR / "state.json"
LATEST_PATH = DATA_DIR / "latest.json"
REPORT_PATH = DATA_DIR / "latest-report.md"

USER_AGENT = (
    "Mozilla/5.0 (compatible; RivalBriefBot/0.1; +https://github.com/)"
)

PRICE_RE = re.compile(
    r"(?:[$€£¥]\s?\d{1,5}(?:[.,]\d{1,2})?|\d{1,5}(?:[.,]\d{1,2})?\s?(?:USD|EUR|GBP|JPY))",
    re.I,
)


@dataclass
class Snapshot:
    fetched_at: str
    url: str
    title: str
    text_hash: str
    text: str
    promotions: list[str]
    prices: list[str]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def unique_keep_order(items: Iterable[str], limit: int = 40) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        key = item.casefold()
        if item and key not in seen:
            seen.add(key)
            out.append(item)
            if len(out) >= limit:
                break
    return out


def fetch_snapshot(site: dict, keywords: list[str]) -> Snapshot:
    response = requests.get(
        site["url"],
        timeout=25,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"},
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    title = normalize_text(soup.title.get_text(" ", strip=True)) if soup.title else site["name"]
    visible_text = normalize_text(soup.get_text(" ", strip=True))
    compact_text = visible_text[:70000]

    lowered = compact_text.casefold()
    promotions = []
    sentences = re.split(r"(?<=[.!?])\s+|\s{2,}", compact_text)
    for sentence in sentences:
        clean = normalize_text(sentence)
        low = clean.casefold()
        if 4 <= len(clean) <= 220 and any(k.casefold() in low for k in keywords):
            promotions.append(clean)

    prices = unique_keep_order(PRICE_RE.findall(compact_text), limit=30)
    promotions = unique_keep_order(promotions, limit=25)

    return Snapshot(
        fetched_at=utc_now(),
        url=site["url"],
        title=title,
        text_hash=hashlib.sha256(compact_text.encode("utf-8")).hexdigest(),
        text=compact_text,
        promotions=promotions,
        prices=prices,
    )


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def diff_lists(old: list[str], new: list[str]) -> tuple[list[str], list[str]]:
    old_map = {x.casefold(): x for x in old}
    new_map = {x.casefold(): x for x in new}
    added = [new_map[k] for k in new_map.keys() - old_map.keys()]
    removed = [old_map[k] for k in old_map.keys() - new_map.keys()]
    return added, removed


def classify_change(previous: dict | None, current: Snapshot) -> dict:
    if previous is None:
        return {
            "status": "baseline",
            "score": 0,
            "summary": "Initial baseline captured.",
            "added_promotions": [],
            "removed_promotions": [],
            "added_prices": [],
            "removed_prices": [],
        }

    if previous.get("text_hash") == current.text_hash:
        return {
            "status": "unchanged",
            "score": 0,
            "summary": "No material page change detected.",
            "added_promotions": [],
            "removed_promotions": [],
            "added_prices": [],
            "removed_prices": [],
        }

    added_promos, removed_promos = diff_lists(previous.get("promotions", []), current.promotions)
    added_prices, removed_prices = diff_lists(previous.get("prices", []), current.prices)

    score = min(100, len(added_promos) * 18 + len(removed_promos) * 10 + len(added_prices) * 8 + len(removed_prices) * 5 + 10)
    pieces = []
    if added_promos:
        pieces.append(f"{len(added_promos)} new promo signal(s)")
    if removed_promos:
        pieces.append(f"{len(removed_promos)} promo signal(s) removed")
    if added_prices or removed_prices:
        pieces.append("visible pricing changed")
    if not pieces:
        pieces.append("page copy changed")

    return {
        "status": "changed",
        "score": score,
        "summary": "; ".join(pieces) + ".",
        "added_promotions": added_promos[:8],
        "removed_promotions": removed_promos[:8],
        "added_prices": added_prices[:12],
        "removed_prices": removed_prices[:12],
    }


def build_report(results: list[dict]) -> str:
    changed = sorted(
        [r for r in results if r["change"]["status"] == "changed"],
        key=lambda r: r["change"]["score"],
        reverse=True,
    )
    lines = [
        "# RivalBrief — Latest Competitor Brief",
        "",
        f"Generated: {utc_now()}",
        "",
    ]

    if not changed:
        lines += ["## Executive summary", "", "No material competitor changes detected in this run.", ""]
    else:
        top = changed[0]
        lines += [
            "## Executive summary",
            "",
            f"Most important move: **{top['name']}** — {top['change']['summary']}",
            "",
        ]

    for result in sorted(results, key=lambda r: r["change"]["score"], reverse=True):
        change = result["change"]
        lines += [
            f"## {result['name']}",
            "",
            f"- Status: **{change['status']}**",
            f"- Importance score: **{change['score']}/100**",
            f"- Summary: {change['summary']}",
            f"- URL: {result['url']}",
        ]
        for label, key in [
            ("New promo signals", "added_promotions"),
            ("Removed promo signals", "removed_promotions"),
            ("New visible prices", "added_prices"),
            ("Removed visible prices", "removed_prices"),
        ]:
            vals = change[key]
            if vals:
                lines.append(f"- {label}:")
                lines.extend([f"  - {v}" for v in vals])
        lines.append("")

    lines += [
        "---",
        "This is an automated signal brief. It highlights observed public-page changes and may miss JavaScript-rendered, geo-personalized or login-gated content.",
    ]
    return "\n".join(lines)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    config = load_json(CONFIG_PATH, {"sites": [], "keywords": []})
    state = load_json(STATE_PATH, {})
    results: list[dict] = []
    next_state = dict(state)

    for site in config.get("sites", []):
        name = site["name"]
        try:
            current = fetch_snapshot(site, config.get("keywords", []))
            previous = state.get(name)
            change = classify_change(previous, current)
            next_state[name] = asdict(current)
            results.append({
                "name": name,
                "url": site["url"],
                "fetched_at": current.fetched_at,
                "change": change,
            })
            print(f"[{change['status']}] {name}: {change['summary']}")
        except Exception as exc:
            results.append({
                "name": name,
                "url": site["url"],
                "fetched_at": utc_now(),
                "change": {
                    "status": "error",
                    "score": 0,
                    "summary": f"Fetch failed: {type(exc).__name__}: {exc}",
                    "added_promotions": [],
                    "removed_promotions": [],
                    "added_prices": [],
                    "removed_prices": [],
                },
            })
            print(f"[error] {name}: {exc}")

    STATE_PATH.write_text(json.dumps(next_state, ensure_ascii=False, indent=2), encoding="utf-8")
    latest = {"generated_at": utc_now(), "results": results}
    LATEST_PATH.write_text(json.dumps(latest, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_PATH.write_text(build_report(results), encoding="utf-8")


if __name__ == "__main__":
    main()
