# Source list for World Pulse automation

Reference list of information sources for expanding `monitor.py`'s feed
list and for manual sourcing. Split by what's actually usable for free,
automated, frequent polling vs. what's reference-only.

Checked reachability of each RSS URL directly on 2026-09-18. URLs change
without notice — re-check before wiring a new one into `monitor.py`.

## Currently wired into monitor.py

- BBC World — `https://feeds.bbci.co.uk/news/world/rss.xml`
- Al Jazeera — `https://www.aljazeera.com/xml/rss/all.xml`
- The Guardian World — `https://www.theguardian.com/world/rss`

## Verified working, good candidates to add next

**Wire services / major outlets**
- Wall Street Journal World — `https://feeds.a.dj.com/rss/RSSWorldNews.xml`
- New York Times World — `https://rss.nytimes.com/services/xml/rss/nyt/World.xml`
- France 24 English — `https://www.france24.com/en/rss`
- Deutsche Welle World — `https://rss.dw.com/xml/rss-en-world`
- NPR World — `https://feeds.npr.org/1004/rss.xml`
- Sky News World — `https://feeds.skynews.com/feeds/rss/world.xml`
- CBS News World — `https://www.cbsnews.com/latest/rss/world`
- Fox News World — `https://moxie.foxnews.com/google-publisher/world.xml`
- The Economist International — `https://www.economist.com/international/rss.xml`
- Financial Times World — `https://www.ft.com/world?format=rss`
- Politico — `https://www.politico.com/rss/politicopicks.xml`

**International organizations (official statements — high trust, direct source)**
- UN News (all) — `https://news.un.org/feed/subscribe/en/news/all/rss.xml`
- European Commission press corner — `https://ec.europa.eu/commission/presscorner/api/rss?language=en`

## Checked, not usable as-is (blocked, discontinued, or needs a workaround)

- Reuters — discontinued public RSS years ago; reuters.com itself blocks
  most bot traffic (401 on direct fetch in our tests). No good free feed.
- Washington Post — public RSS feeds appear discontinued (`feeds.washingtonpost.com` unreachable).
- CNBC, IMF, World Bank, US State Department, White House, NATO — all
  returned 403/404 on the URLs tried; either bot-blocked or the feed path
  has moved. Worth a fresh look individually if one of these matters a lot.

## Reference only — not realistically usable for free automated polling

**X / Twitter** — official API access for bulk/automated reading now
requires a paid tier; scraping the site directly breaks constantly and
violates its terms. Listing accounts here as manual-browsing references,
not as something `monitor.py` can pull from:
- @Reuters, @AP, @BBCWorld, @AJEnglish, @nytimes, @guardian
- @UN, @NATO, @EU_Commission, @WHO
- @StateDept, @Kremlin_Russia, @mfa_russia, @IsraeliPM, @IDF

**Reddit** — `old.reddit.com/r/<subreddit>.json` still works unauthenticated
for light, infrequent polling, but Reddit's 2023 API changes make heavy
automated use against their terms without a paid API key. Reference
subreddits if browsing manually: r/worldnews, r/geopolitics, r/europe,
r/UkrainianConflict, r/anime_titties (a long-running geopolitics-focused
sub despite the name).

**Telegram channels** — genuinely useful for fast, on-the-ground reporting
(especially Russia/Ukraine war coverage), but each channel needs its own
scraping setup (no unified RSS-like API), and reliability/bias varies a
lot channel to channel. Not wired into anything here; would need a
dedicated integration if this becomes a priority later.

## Recommendation

Add the WSJ, NYT, France 24, DW and UN News feeds to `monitor.py` next —
all verified working, no auth needed, and UN News in particular is a
direct-from-source feed rather than press coverage of a source, which
fits the site's attribution philosophy especially well. Everything else
here is reference for later, not urgent.
