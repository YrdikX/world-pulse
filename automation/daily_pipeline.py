"""
The "heavy" deep pass (runs every 6 hours): reads candidates the 30-minute
monitor collected,
fetches the actual article, asks Claude to extract a structured edge (or
reject the candidate), and writes anything accepted to pending_edges.jsonl
for a human glance before it's merged into the site. Nothing here writes
to world_pulse_template.html directly -- publishing new edges is still a
separate, reviewed step, on purpose (see README.md's "no fabrication" rule).

Scope for this first version, deliberately conservative:
- Only drafts an edge when BOTH the actor and the target already exist as
  tracked entities (automation/entities.json). Creating brand-new
  countries/people/orgs unattended is a separate, manual step.
- One Claude call per candidate. Costs stay bounded because the 30-minute
  monitor already filtered GDELT's firehose down to headlines that mention
  something we track -- this only ever sees that pre-filtered trickle.
"""
import json, os, re, sys, urllib.request
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTOMATION = os.path.join(BASE, "automation")
ENTITIES_FILE = os.path.join(AUTOMATION, "entities.json")
CANDIDATES_FILE = os.path.join(AUTOMATION, "candidates.jsonl")
PROCESSED_FILE = os.path.join(AUTOMATION, "processed_urls.json")
PENDING_FILE = os.path.join(AUTOMATION, "pending_edges.jsonl")

sys.path.insert(0, AUTOMATION)
from extract_text import fetch_article_text  # noqa: E402

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
# Haiku, not Sonnet: this is bounded structured extraction (accept/reject +
# fill a fixed JSON shape from article text already narrowed down by the
# entity-match filter upstream) -- not the kind of task that needs a bigger
# model, and running it on Sonnet every 6 hours was needlessly expensive.
MODEL = "claude-haiku-4-5-20251001"
API_URL = "https://api.anthropic.com/v1/messages"

SYSTEM_PROMPT = """You are a strict fact-extraction engine for World Pulse, a site whose entire premise is "facts, not framing" -- every claim must be a real, sourced, dated event, never invented.

You will be given one news article and a list of entity ids World Pulse already tracks. Your job:

1. Decide whether this article describes a genuine, distinct political/international-relations event (a country, person, or organization saying or doing something). Reject: sports, entertainment, markets-only stories, pure opinion columns, or cases where the entity name match is coincidental (e.g. "Turkey" the country vs. a Thanksgiving turkey).
2. If it qualifies, identify the ACTOR (whoever is speaking or acting -- not whoever the story is about) and the TARGET, using World Pulse's attribution rule: "Lithuania's president says X" belongs to Lithuania, because Lithuania is the one speaking.
3. Both actor and target MUST already exist in the provided entity list. If either one isn't a tracked entity, reject the candidate -- do not invent a new id.
4. Only use facts actually stated in the article. Never add a date, quote, or detail that isn't in the text.

Respond with ONLY a JSON object, no other text, in exactly this shape:

{"accept": true, "from": "<entity id>", "to": "<entity id>", "label": "<short lowercase-first clause, e.g. 'announced new tariffs on steel imports'>", "date": "YYYY-MM-DD", "scope": "international" or "domestic", "detail": "<1-2 sentence factual summary, present/past tense, no editorializing>"}

or, if it should be rejected:

{"accept": false, "reason": "<short reason>"}
"""


def load_json(path, default):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


def load_candidates():
    if not os.path.exists(CANDIDATES_FILE):
        return []
    with open(CANDIDATES_FILE, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def call_claude(system, user_content):
    body = json.dumps({
        "model": MODEL,
        "max_tokens": 500,
        "system": system,
        "messages": [{"role": "user", "content": user_content}],
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL, data=body, method="POST",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return "".join(block.get("text", "") for block in data.get("content", []))


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def main():
    if not ANTHROPIC_API_KEY:
        print("ANTHROPIC_API_KEY not set -- skipping daily pipeline.", file=sys.stderr)
        return

    entities = load_json(ENTITIES_FILE, [])
    valid_ids = {e["id"] for e in entities}
    entity_list_str = ", ".join(sorted(valid_ids))

    candidates = load_candidates()
    processed = set(load_json(PROCESSED_FILE, []))
    todo = [c for c in candidates if c["url"] not in processed]

    if not todo:
        print("No new candidates to process.")
        return

    print(f"Processing {len(todo)} candidate(s)...")
    accepted = []

    for c in todo:
        text, err = fetch_article_text(c["url"])
        if err:
            # A permanent characteristic of this URL (paywalled, JS-rendered,
            # dead link) -- retrying later won't change that, safe to mark done.
            processed.add(c["url"])
            print(f"  skip ({err}): {c['url']}")
            continue

        published_date = (c.get("published") or "")[:10] or None
        user_content = (
            f"TRACKED ENTITY IDS:\n{entity_list_str}\n\n"
            f"ARTICLE TITLE: {c['title']}\n"
            f"ARTICLE URL: {c['url']}\n"
            + (f"ARTICLE PUBLISHED: {published_date} (authoritative -- use this for relative dates like 'yesterday')\n" if published_date else "")
            + f"ARTICLE TEXT:\n{text}\n"
        )
        try:
            raw = call_claude(SYSTEM_PROMPT, user_content)
        except Exception as e:
            # Likely a systemic issue (bad/expired key, quota, network) rather
            # than anything about this specific candidate. Stop here instead
            # of burning through every remaining one with the same failure --
            # and leave this candidate (and the rest) unmarked so the next
            # run retries them once the underlying problem is fixed.
            print(f"  API error for {c['url']}: {e}", file=sys.stderr)
            print("  Stopping this run early; nothing processed so far will be lost.", file=sys.stderr)
            break

        # Only now, after an actual model response, is this candidate done.
        processed.add(c["url"])
        result = extract_json(raw)
        if not result:
            print(f"  unparseable model output for {c['url']}")
            continue

        if not result.get("accept"):
            print(f"  rejected: {result.get('reason', 'no reason given')}")
            continue

        if result.get("from") not in valid_ids or result.get("to") not in valid_ids:
            print(f"  rejected: from/to not both tracked entities ({result.get('from')} -> {result.get('to')})")
            continue

        edge = {
            "from": result["from"],
            "to": result["to"],
            "label": result["label"],
            "url": c["url"],
            # The article's own real timestamp (captured by monitor.py) is
            # authoritative when we have it -- the model's guess from article
            # text alone, our previous approach, turned out to fabricate
            # dates whenever the text didn't state one explicitly (Telegram
            # posts especially), sometimes off by years.
            "date": published_date or result["date"],
            "scope": result.get("scope", "international"),
            "detail": result.get("detail", ""),
            "source_title": c["title"],
            "extracted_at": datetime.now(timezone.utc).isoformat(),
        }
        accepted.append(edge)
        print(f"  accepted: {edge['from']} -> {edge['to']}: {edge['label']}")

    if accepted:
        with open(PENDING_FILE, "a", encoding="utf-8") as f:
            for e in accepted:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        print(f"Wrote {len(accepted)} candidate edge(s) to {PENDING_FILE} for review.")

    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(list(processed)[-8000:], f)

    # Prune candidates.jsonl down to just the still-unprocessed backlog, so
    # it doesn't grow forever now that everything in it has been handled.
    remaining = [c for c in candidates if c["url"] not in processed]
    with open(CANDIDATES_FILE, "w", encoding="utf-8") as f:
        for c in remaining:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
