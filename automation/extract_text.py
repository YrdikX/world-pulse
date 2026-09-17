"""
Minimal, dependency-free article text extraction: fetch a URL and strip
HTML down to plain-ish text. Not as good as a real readability parser, but
good enough to give the model real article content instead of just a
headline, with zero extra pip installs in CI.
"""
import re
import urllib.request

UA = "Mozilla/5.0 (WorldPulseBot/1.0; +https://getworldpulse.com)"


def fetch_article_text(url, max_chars=6000, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            ctype = resp.headers.get_content_charset() or "utf-8"
    except Exception as e:
        return None, f"fetch failed: {e}"

    try:
        html = raw.decode(ctype, errors="replace")
    except LookupError:
        html = raw.decode("utf-8", errors="replace")

    # Drop script/style/nav/footer blocks entirely, then strip remaining tags.
    html = re.sub(r"(?is)<(script|style|nav|footer|header|form|noscript)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    text = re.sub(r"&nbsp;|&amp;|&#8217;|&#8216;|&#8220;|&#8221;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) < 200:
        return None, "extracted text too short (likely paywalled or JS-rendered)"

    return text[:max_chars], None
