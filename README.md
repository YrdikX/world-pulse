# World Pulse

A prototype for tracking world political news as an objective fact-network — who said or did what, to whom, sourced — instead of comparing opinions or framing.

**Live artifact:** https://claude.ai/artifact/8R5UjCHkUgcg2bGViiyxnB

## What this is

A single self-contained HTML/CSS/JS page (no backend). Core parts:

- **Feed** — chronological, bucketed (Today / This week / This month / Archive)
- **Map** — all 221 countries, zoomable/pannable, colored by relative recent activity (quartile-based "pulse" tiers) or by alliance membership (EU/NATO/BRICS/Mercosur/ASEAN/Arab League/African Union — via the flag icon flyout on the map)
- **Chambers** — real, sourced statements from international organizations (UN, NATO, EU, G7, G20, WTO, BRICS, Mercosur, ASEAN, African Union, Arab League, OSCE, International IDEA)
- **Indices** — a catalog of real, existing world political indices (Global Peace Index, WGI Political Stability, Fragile States Index, Democracy Index, Freedom House, CPI, V-Dem, etc.) with explanations and links to official sources, plus World Pulse's own transparent activity-tier metric
- **Archive**, **About**, entity pages for every country/person/org/event, search

Attribution rule: a news item belongs to whoever is the **actor** (the one speaking or acting), not whoever it's about.

## Project layout

```
world_pulse_template.html   the editable source (has __PLACEHOLDER__ tokens for large data)
build.py                    injects cache/ data into the template -> build/world_pulse.html
cache/                      generated data the template depends on (see below)
build/world_pulse.html      the built, publish-ready file
```

### cache/ contents

- `world_geometry.json`, `world_centroids.json` — per-country SVG path data (Robinson projection), from the Guardian's open-source world-map repo, keyed by World Bank 3-letter country codes
- `wb_countries.json` — World Bank country list (names, codes), used to auto-generate the 205 "extra" countries beyond the 16 hand-built ones
- `extra_country_paths.js`, `extra_country_entities.js` — the 205 auto-generated country entities/paths built from the two files above
- `person_profiles.js` — Wikipedia bio/photo data for the 16 politician profiles (photos are embedded as base64 data URIs directly in this file — needed because Claude's artifact sandbox blocks hotlinking external images)

## Rebuilding

After editing `world_pulse_template.html`:

```bash
python3 build.py
```

This writes `build/world_pulse.html`, which is what gets published as the Artifact.

## Known limitations (as of this prototype)

- Not automated — no backend, no scheduler, no live news pipeline. Every edge in the dataset was hand-curated and sourced manually.
- Coverage is real but partial: 74 sourced edges so far, spanning Europe, the Americas, the Middle East, Asia-Pacific and Africa — most of the 221 countries on the map have no data yet (and say so honestly rather than faking coverage).
- Two future paths for real automation were discussed but not built: (A) a scheduled task doing periodic manual-style curation, or (B) a real pipeline (GDELT or similar source + Postgres + LLM extraction + human review queue).
