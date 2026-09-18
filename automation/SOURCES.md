# Source list for World Pulse automation

Reference list of information sources for expanding `monitor.py`'s feed
list and for manual sourcing. Split by what's actually usable for free,
automated, frequent polling vs. what's reference-only.

Checked reachability of each RSS URL directly on 2026-09-18. URLs change
without notice — re-check before wiring a new one into `monitor.py`.

## Currently wired into monitor.py

**RSS**
- BBC World — `https://feeds.bbci.co.uk/news/world/rss.xml`
- Al Jazeera — `https://www.aljazeera.com/xml/rss/all.xml`
- The Guardian World — `https://www.theguardian.com/world/rss`
- Wall Street Journal World — `https://feeds.a.dj.com/rss/RSSWorldNews.xml`
- New York Times World — `https://rss.nytimes.com/services/xml/rss/nyt/World.xml`
- France 24 English — `https://www.france24.com/en/rss`
- Deutsche Welle World — `https://rss.dw.com/xml/rss-en-world`
- UN News (all) — `https://news.un.org/feed/subscribe/en/news/all/rss.xml`

**Telegram** (via `t.me/s/<channel>`, no login needed — see below)
- Топор Live (`toporlive`) — user-picked, general incident/news channel
- CNN Breaking News (`cnnbrk`), The Guardian (`guardian`), France 24 English (`france24_en`), AP (`apnews`), CBS News (`cbsnews`), Politico (`politico`), Bloomberg (`bloomberg`), BBC News World (`bbcworld`), Sky News (`skynews`), The Times (`thetimes`), Al Jazeera English (`aljazeeraenglish`)
- The Kyiv Independent (`kyivindependent`), Ukrainska Pravda (`ukrpravda_news`)
- SCMP (`scmpnews`), NHK World (`nhkworld`), TRT World (`trtworld`), Straits Times (`straitstimes`)
- Times of Israel (`timesofisrael`), Al Mayadeen (`almayadeen`) — note: Al Mayadeen is a Lebanese outlet with a well-known pro-Hezbollah/Iran-axis editorial lean; kept for the "who said what" record (their own stated position is itself a fact), not as a neutral source

### Telegram channels — a real, workable source after all

Public Telegram channels expose a login-free HTML preview at
`t.me/s/<channel_name>`, built for embedding posts on other sites. No
account, no API key, no Telegram app needed — a plain HTTP GET returns
recent posts with their text and timestamps. `monitor.py`'s
`fetch_telegram()` parses this directly.

This means Telegram is NOT reference-only the way X/Reddit are — any
public channel can be added to `TELEGRAM_CHANNELS` in `monitor.py` right
now, for free, with no extra setup. We aren't vetting channels for bias
ourselves; whoever picks a channel to add is vouching for it, and the
LLM-extraction + human-review steps downstream are the actual safety net
against anything inaccurate reaching the site — same as for any source.

Send more channel @usernames (Russian, Ukrainian, or any language/region)
and they can be added the same way.

## Verified working, good candidates to add next

- NPR World — `https://feeds.npr.org/1004/rss.xml`
- Sky News World — `https://feeds.skynews.com/feeds/rss/world.xml`
- CBS News World — `https://www.cbsnews.com/latest/rss/world`
- Fox News World — `https://moxie.foxnews.com/google-publisher/world.xml`
- The Economist International — `https://www.economist.com/international/rss.xml`
- Financial Times World — `https://www.ft.com/world?format=rss`
- Politico — `https://www.politico.com/rss/politicopicks.xml`
- European Commission press corner (official statements, direct source) — `https://ec.europa.eu/commission/presscorner/api/rss?language=en`

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

## Recommendation

Send more Telegram channel handles — that's the highest-leverage source
we found: free, no auth, works today, good for on-the-ground/local
coverage RSS misses entirely. Everything else in "verified working" is a
reasonable next batch to wire in, not urgent.
