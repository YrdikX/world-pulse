"""
Lightweight 30-minute check: pulls recent world-news headlines and flags
which ones mention an entity we already track. Zero LLM calls, zero cost --
this is purely "did anything happen involving someone we track", not
"write me a new edge". The deep pass reads candidates.jsonl and does the
actual drafting/verification with an LLM.

Primary source is a handful of major outlets' public RSS feeds -- these
are meant for frequent automated polling and don't rate-limit a request
every 30 minutes. Public Telegram channels (t.me/s/<name>, no login
needed) are a second source, useful for faster/local coverage RSS misses.
GDELT is kept as a best-effort supplementary source for its much broader
outlet coverage, but GitHub Actions runners share IP ranges with
countless other projects, and GDELT's free API rate-limits by IP -- so a
429 from it is expected sometimes, not an error to fix, just something to
not depend on exclusively.
"""
import json, os, re, sys, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTOMATION = os.path.join(BASE, "automation")
ENTITIES_FILE = os.path.join(AUTOMATION, "entities.json")
CANDIDATES_FILE = os.path.join(AUTOMATION, "candidates.jsonl")
SEEN_FILE = os.path.join(AUTOMATION, "seen_urls.json")

UA = "Mozilla/5.0 (WorldPulseMonitor/1.0; +https://getworldpulse.com)"
MAX_SEEN = 8000  # bound the file size; only recent history is needed for dedup

RSS_FEEDS = [
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.theguardian.com/world/rss",
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://www.france24.com/en/rss",
    "https://rss.dw.com/xml/rss-en-world",
    "https://news.un.org/feed/subscribe/en/news/all/rss.xml",
]

# Public Telegram channels expose a login-free HTML preview at t.me/s/<name>,
# meant for embedding -- no account, no API key, no Telegram app needed.
# User-picked, not vetted by us for bias; the LLM step and human review are
# what keep bad extractions off the site, same as for any other source.
TELEGRAM_CHANNELS = [
    "toporlive",
    "cnnbrk", "guardian", "france24_en", "apnews", "cbsnews", "politico",
    "bloomberg", "bbcworld", "skynews", "thetimes", "aljazeeraenglish",
    "kyivindependent", "scmpnews", "nhkworld", "trtworld", "timesofisrael",
    "straitstimes", "ukrpravda_news", "almayadeen",
]

GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
GDELT_QUERY = (
    "sourcelang:english "
    "(politics OR government OR president OR minister OR parliament "
    "OR election OR sanctions OR coalition OR referendum)"
)


def load_entities():
    with open(ENTITIES_FILE, encoding="utf-8") as f:
        entities = json.load(f)
    # Word-boundary regex per entity, precompiled once -- plain substring
    # matching let "Oman" match inside "woman" and similar noise.
    for e in entities:
        if len(e["label"]) >= 3:
            e["_re"] = re.compile(r"\b" + re.escape(e["label"]) + r"\b", re.IGNORECASE)
    return entities


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, encoding="utf-8") as f:
            return list(json.load(f))
    return []


def save_seen(seen_list):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(seen_list[-MAX_SEEN:], f)


def fetch_rss(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
    except Exception as e:
        print(f"RSS fetch failed ({url}): {e}", file=sys.stderr)
        return []
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        print(f"RSS parse failed ({url}): {e}", file=sys.stderr)
        return []
    items = []
    for item in root.iter("item"):
        title_el = item.find("title")
        link_el = item.find("link")
        if title_el is None or link_el is None or not title_el.text or not link_el.text:
            continue
        items.append({"title": title_el.text.strip(), "url": link_el.text.strip(), "domain": urllib.parse.urlparse(url).netloc})
    return items


def fetch_telegram(channel, limit=40):
    url = f"https://t.me/s/{channel}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Telegram fetch failed ({channel}): {e}", file=sys.stderr)
        return []
    items = []
    # Each message's own wrapper starts a new "tgme_widget_message " block
    # (note the trailing space, to not also match message_text/message_date).
    parts = re.split(r'(?=<div class="tgme_widget_message[^a-zA-Z][^"]*" data-post=)', html)
    for part in parts[1:]:
        post_m = re.search(r'data-post="([^"]+)"', part)
        text_m = re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', part, re.S)
        if not post_m or not text_m:
            continue
        text = re.sub(r"<br\s*/?>", " ", text_m.group(1))
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        items.append({"title": text[:300], "url": f"https://t.me/{post_m.group(1)}", "domain": f"t.me/{channel}"})
    return items[-limit:]


def gdelt_query(query, timespan="45min", maxrecords=250):
    params = {
        "query": query, "mode": "artlist", "maxrecords": str(maxrecords),
        "timespan": timespan, "format": "json", "sort": "datedesc",
    }
    url = GDELT_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print("GDELT request failed (non-fatal, RSS is primary):", e, file=sys.stderr)
        return []
    if not data.strip():
        return []
    try:
        obj = json.loads(data)
    except json.JSONDecodeError:
        print("GDELT returned non-JSON (likely rate-limited -- fine, RSS is primary)", file=sys.stderr)
        return []
    return [{"title": a.get("title", ""), "url": a.get("url", ""), "domain": a.get("domain", "")}
            for a in obj.get("articles", [])]


def main():
    entities = load_entities()
    seen = load_seen()
    seen_set = set(seen)

    raw_items = []
    for feed in RSS_FEEDS:
        items = fetch_rss(feed)
        print(f"{feed}: {len(items)} items")
        raw_items.extend(items)
    for channel in TELEGRAM_CHANNELS:
        items = fetch_telegram(channel)
        print(f"t.me/{channel}: {len(items)} items")
        raw_items.extend(items)
    gdelt_items = gdelt_query(GDELT_QUERY)
    print(f"GDELT: {len(gdelt_items)} items")
    raw_items.extend(gdelt_items)

    candidates = []
    for art in raw_items:
        url = art.get("url", "")
        title = art.get("title", "") or ""
        if not url or not title or url in seen_set:
            continue
        matched = [e["id"] for e in entities if "_re" in e and e["_re"].search(title)]
        if not matched:
            seen.append(url)  # still mark seen so a later run doesn't re-check it forever
            continue
        candidates.append({
            "title": title,
            "url": url,
            "domain": art.get("domain"),
            "matched_entities": matched,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        })
        seen.append(url)

    if candidates:
        with open(CANDIDATES_FILE, "a", encoding="utf-8") as f:
            for c in candidates:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        print(f"Appended {len(candidates)} new candidate(s) to {CANDIDATES_FILE}")
    else:
        print("No new candidates this run")

    save_seen(seen)


if __name__ == "__main__":
    main()
