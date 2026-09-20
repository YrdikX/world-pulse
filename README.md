# World Pulse

A political fact-network — who said or did what, to whom, sourced — instead of comparing opinions or framing.

**Live site:** https://getworldpulse.com

## What this is

A real multi-page static site (GitHub Pages, no backend server). Every country, person, organization and event gets its own real URL (`/entity/<id>.html`, `/event/<id>.html`), not a hash-routed single page — one shared `app.js`/`style.css` bundle keeps the ~1,000-edge dataset from being duplicated per page.

Core parts:

- **Feed** — chronological, bucketed (Today / This week / This month / Archive), with "Trending now" chips at the top
- **Map** — all 221 countries, zoomable/pannable, colored by relative recent activity (quartile-based "pulse" tiers) or by alliance membership (EU/NATO/BRICS/Mercosur/ASEAN/Arab League/African Union — via the flag icon flyout on the map)
- **Chambers** — real, sourced statements from international organizations (UN, NATO, EU, G7, G20, WTO, BRICS, Mercosur, ASEAN, African Union, Arab League, OSCE, International IDEA)
- **Trends** — recurring themes (Russia–Ukraine war, Middle East tensions, elections & coalitions, trade/tariffs, energy & fuel, Greenland/Arctic) computed live by keyword-matching each event's own text, not hand-picked — so new automation-collected events get bucketed with no manual maintenance
- **Connections** — on every entity's page, a ranked list of which other entities it shares the most documented events with; clicking one opens their joint timeline (`#/entity/<id>/with/<otherId>`, deep-linkable)
- Entity pages for every country/person/org/event, full-text search, **Archive**, **About**

Two editorial rules run through all of it:
- **Attribution belongs to the actor**, not whoever the action is about — "Lithuania's president says the drone was Russian" is Lithuania's news, not Russia's.
- **Every name mentioned anywhere in an event's text is auto-linked** to that entity's own profile if we track it (`autoLinkText()` + a combined regex over every tracked label) — not just the two actors on the edge itself. An entity's `aliases` list (e.g. `Zelensky` / `Zelenskyy`, `Lee Jae-myung` / `Lee Jae Myung`) covers the same name spelled differently across sources.

## Automation pipeline

```
RSS + Telegram feeds (30 min)  →  candidates.jsonl
                                        ↓
        LLM extraction pass, Haiku (every 6 hours)
                                        ↓
                          automation/pending_edges.jsonl
                                        ↓
                    human review (dedup, verify, merge)
                                        ↓
                world_pulse_template.html  →  python3 build.py
                                        ↓
                    push to main  →  GitHub Actions  →  deploy
```

Nothing goes live without a human reviewing it first — the LLM pass only proposes candidate edges into a queue, it never merges into the template directly. See `automation/SOURCES.md` for the current feed list and `.github/workflows/` for the three scheduled jobs (30-minute monitor, 6-hourly deep pass, deploy-on-push).

## Project layout

```
world_pulse_template.html   the editable source (has __PLACEHOLDER__ tokens for large data)
build.py                    injects cache/ data into the template, then generates:
                               build/style.css, build/app.js       (shared bundle)
                               build/index.html                    (Feed/Map/Chambers/Trends/Archive/About)
                               build/entity/<id>.html               (one per tracked entity)
                               build/event/<id>.html                (one per edge)
                               build/sitemap.xml                    (generated, not hand-written)
                               build/world_pulse.html               (single-file copy, local sanity checks only)
automation/                 monitor.py (RSS/Telegram polling), daily_pipeline.py (LLM extraction),
                             fetch_*_profiles*.py (Wikipedia summary fetches), pending_edges.jsonl (review queue)
cache/                      generated data the template depends on (see below)
.github/workflows/          monitor.yml, deep_pass.yml, deploy.yml
```

### cache/ contents

- `world_geometry.json`, `world_centroids.json` — per-country SVG path data (Robinson projection), from the Guardian's open-source world-map repo, keyed by World Bank 3-letter country codes
- `wb_countries.json` — World Bank country list (names, codes), used to auto-generate the ~205 "extra" countries beyond the 16 hand-built ones
- `extra_country_paths.js`, `extra_country_entities.js` — the auto-generated country entities/paths built from the two files above
- `person_profiles.js` — Wikipedia bio/photo data for tracked people (fetched via the Wikipedia REST summary API, never hand-written)
- `org_profiles.js` — same, for tracked organizations

## Rebuilding

After editing `world_pulse_template.html`:

```bash
python3 build.py
```

The real deploy target is the multi-page output under `build/` (`index.html`, `style.css`, `app.js`, `entity/`, `event/`, `sitemap.xml`) — regenerated fresh by the `deploy.yml` workflow on every push to `main` and never committed to git. `build/world_pulse.html` is kept as a single-file copy for quick local sanity checks only (entity/event links won't resolve from it standalone).

## Known limitations

- It's a static site with one shared data bundle, not a database — fine at the current scale (a few hundred events), but a real backend (API + DB) would eventually be needed if the dataset grows by an order of magnitude or more.
- Coverage is real but partial: most of the 221 countries on the map have no data yet, and say so honestly rather than faking coverage.
- Trends are keyword-matched, not a real clustering/NLP model — good enough while the topic list is short and hand-maintained, but won't scale to discovering *new* topics on its own.
- Every profile's biographical description is Wikipedia's own text (CC BY-SA), fetched via API and never edited or written by World Pulse — only the "Activity" sections below it are original sourced reporting.
