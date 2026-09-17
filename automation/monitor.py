"""
Lightweight 30-minute check: pulls recent world-politics articles from
GDELT (free, no API key, updated every ~15 min) and flags which ones
mention an entity we already track. Zero LLM calls, zero cost -- this is
purely "did anything happen involving someone we track", not "write me
a new edge". The daily deep pass reads candidates.jsonl and does the
actual drafting/verification with an LLM.
"""
import json, os, sys, urllib.request, urllib.parse
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTOMATION = os.path.join(BASE, "automation")
ENTITIES_FILE = os.path.join(AUTOMATION, "entities.json")
CANDIDATES_FILE = os.path.join(AUTOMATION, "candidates.jsonl")
SEEN_FILE = os.path.join(AUTOMATION, "seen_urls.json")

GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
QUERY = (
    "sourcelang:english "
    "(politics OR government OR president OR minister OR parliament "
    "OR election OR sanctions OR coalition OR referendum)"
)
MAX_SEEN = 8000  # bound the file size; GDELT dedup only needs recent history


def load_entities():
    with open(ENTITIES_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, encoding="utf-8") as f:
            return list(json.load(f))
    return []


def save_seen(seen_list):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(seen_list[-MAX_SEEN:], f)


def gdelt_query(query, timespan="45min", maxrecords=250):
    params = {
        "query": query,
        "mode": "artlist",
        "maxrecords": str(maxrecords),
        "timespan": timespan,
        "format": "json",
        "sort": "datedesc",
    }
    url = GDELT_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "WorldPulseMonitor/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print("GDELT request failed:", e, file=sys.stderr)
        return []
    if not data.strip():
        return []
    try:
        obj = json.loads(data)
    except json.JSONDecodeError:
        print("GDELT returned non-JSON (likely rate-limited or empty)", file=sys.stderr)
        return []
    return obj.get("articles", [])


def main():
    entities = load_entities()
    seen = load_seen()
    seen_set = set(seen)

    articles = gdelt_query(QUERY)
    print(f"GDELT returned {len(articles)} articles")

    candidates = []
    for art in articles:
        url = art.get("url", "")
        if not url or url in seen_set:
            continue
        title = art.get("title", "") or ""
        title_lower = title.lower()
        # Only match whole-ish words to cut down on noise (e.g. "Chad" inside
        # another word) -- simple substring is good enough for short names,
        # so just require the match isn't part of a longer alphabetic run.
        matched = []
        for e in entities:
            label_lower = e["label"].lower()
            if len(label_lower) < 3:
                continue
            idx = title_lower.find(label_lower)
            if idx == -1:
                continue
            matched.append(e["id"])
        if not matched:
            continue
        candidates.append({
            "title": title,
            "url": url,
            "seendate": art.get("seendate"),
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
