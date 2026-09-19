import json, re, os

BASE = os.path.dirname(__file__)
TEMPLATE = os.path.join(BASE, "world_pulse_template.html")
CACHE = os.path.join(BASE, "cache")
OUT = os.path.join(BASE, "build", "world_pulse.html")

geo = json.load(open(os.path.join(CACHE, "world_geometry.json")))

CORE = {
    "RUS": "rus", "UKR": "ukr", "LTU": "ltu", "BLR": "blr", "POL": "pol", "MDA": "mda",
    "USA": "usa", "CHN": "chn", "DEU": "deu", "FRA": "fra", "GBR": "gbr", "JPN": "jpn",
    "IND": "ind", "CAN": "can", "ITA": "ita", "BRA": "bra",
}

html = open(TEMPLATE, encoding="utf-8").read()

leftover_before = set(re.findall(r"__[A-Z_]+__", html))

for code in CORE:
    placeholder = "__%s_PATH__" % code
    d = geo[code]
    html = html.replace(placeholder, d)

extra_paths = open(os.path.join(CACHE, "extra_country_paths.js"), encoding="utf-8").read()
extra_entities = open(os.path.join(CACHE, "extra_country_entities.js"), encoding="utf-8").read()
person_profiles = open(os.path.join(CACHE, "person_profiles.js"), encoding="utf-8").read()
org_profiles = open(os.path.join(CACHE, "org_profiles.js"), encoding="utf-8").read()

html = html.replace("__EXTRA_COUNTRY_PATHS__", extra_paths)
html = html.replace("__EXTRA_COUNTRY_ENTITIES__", extra_entities)
html = html.replace("__PERSON_PROFILES__", person_profiles)
html = html.replace("__ORG_PROFILES__", org_profiles)

leftover_after = set(re.findall(r"__[A-Z_]+__", html))
print("leftover placeholders:", sorted(leftover_after))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("wrote", OUT, "size:", os.path.getsize(OUT))

# Also refresh the root-level copy used for a quick single-file sanity check
# (Feed/Map/Chambers/About all work standalone here) -- entity/event links
# won't resolve from this copy since those are only generated as part of the
# real multi-page build below (build/entity/*.html, build/event/*.html);
# serve the build/ directory itself to test those.
ROOT_COPY = os.path.join(BASE, "world_pulse.html")
with open(ROOT_COPY, "w", encoding="utf-8") as f:
    f.write(html)

# Extract a plain {id, label, type} index of every entity for the automation
# scripts (monitor.py etc.) to use, so it never drifts out of sync with the
# actual dataset -- it's regenerated from the built page every time.
#
# The label alternation is quote-delimiter-aware (single vs double) rather
# than excluding both quote characters from the content -- a label like
# "Cote d'Ivoire" (double-quoted, containing an apostrophe) was silently
# dropped by the old single-pattern version, since it excluded ' from the
# content class even though ' wasn't the string's actual delimiter.
entity_re = re.compile(
    r"\{id:\s*['\"]([^'\"]+)['\"],\s*label:\s*(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"),\s*type:\s*['\"]([^'\"]+)['\"]"
)
seen_ids = set()
entities_index = []
for m in entity_re.finditer(html):
    eid = m.group(1)
    label = m.group(2) if m.group(2) is not None else m.group(3)
    etype = m.group(4)
    if eid in seen_ids:
        continue
    seen_ids.add(eid)
    label = label.replace("\\'", "'").replace('\\"', '"')
    entities_index.append({"id": eid, "label": label, "type": etype})

AUTOMATION = os.path.join(BASE, "automation")
os.makedirs(AUTOMATION, exist_ok=True)
with open(os.path.join(AUTOMATION, "entities.json"), "w", encoding="utf-8") as f:
    json.dump(entities_index, f, ensure_ascii=False, indent=1)
print("wrote entities index:", len(entities_index), "entities")

# --- Multi-page site: real, separate, crawlable pages for every entity and
# event, instead of one single-page app where "navigating" just swaps DOM
# content under one URL. Every page shares the same style.css/app.js bundle
# (so the browser caches the ~1MB dataset+logic once, not once per page) --
# only the tiny per-page HTML shell (meta tags + a one-line bootstrap call)
# differs.
HEAD_END = html.index("<style>")
STYLE_START = html.index("<style>") + len("<style>")
STYLE_END = html.index("</style>")
BODY_START = html.index("</style>") + len("</style>")
SCRIPT_START = html.index("<script>", BODY_START) + len("<script>")
SCRIPT_END = html.rindex("</script>")

head_meta = html[:HEAD_END]
style_block = html[STYLE_START:STYLE_END]
body_html = html[BODY_START:html.index("<script>", BODY_START)]
script_block = html[SCRIPT_START:SCRIPT_END]

BUILD_DIR = os.path.dirname(OUT)
with open(os.path.join(BUILD_DIR, "style.css"), "w", encoding="utf-8") as f:
    f.write(style_block)
with open(os.path.join(BUILD_DIR, "app.js"), "w", encoding="utf-8") as f:
    f.write(script_block)
print("wrote style.css, app.js")


def simple_hash(s):
    h = 0
    for ch in s:
        h = (31 * h + ord(ch)) & 0xFFFFFFFF
    if h == 0:
        return "0"
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    n = h
    while n:
        n, r = divmod(n, 36)
        out = digits[r] + out
    return out


def edge_id(frm, to, date, label):
    return simple_hash(frm + "|" + to + "|" + date + "|" + label)


def page_head(title, description, canonical):
    return (
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta charset="utf-8">\n'
        f"<title>{title}</title>\n"
        f'<meta name="description" content="{description}">\n'
        f'<link rel="canonical" href="{canonical}">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:site_name" content="World Pulse">\n'
        f'<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{description}">\n'
        f'<meta property="og:url" content="{canonical}">\n'
        '<meta name="twitter:card" content="summary">\n'
        f'<meta name="twitter:title" content="{title}">\n'
        f'<meta name="twitter:description" content="{description}">\n'
        '<link rel="stylesheet" href="/style.css">\n'
    )


def html_escape_attr(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def write_page(path, title, description, canonical, boot_js):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    page = (
        page_head(html_escape_attr(title), html_escape_attr(description), canonical)
        + body_html
        + '<script src="/app.js"></script>\n'
        + (f"<script>{boot_js}</script>\n" if boot_js else "")
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)


# index.html: the main app (Feed/Map/Chambers/Trends/Archive/About), same
# default behavior as always -- no bootstrap override needed.
write_page(
    os.path.join(BUILD_DIR, "index.html"),
    "World Pulse — Global Political Events, Connected",
    "World Pulse tracks world politics as a network of sourced facts — who said or did what, to whom, and when — instead of comparing opinions. Every claim links to its original source.",
    "https://getworldpulse.com/",
    None,
)

TYPE_NOUN = {"person": "person", "country": "country", "org": "organization", "event": "event", "region": "region / bloc"}
for e in entities_index:
    label = e["label"]
    etype = e["type"]
    desc = f"{label} on World Pulse — real, sourced facts about who said or did what, involving this {TYPE_NOUN.get(etype, 'entity')}. Every claim links to its original source."
    write_page(
        os.path.join(BUILD_DIR, "entity", e["id"] + ".html"),
        f"{label} — World Pulse",
        desc,
        f"https://getworldpulse.com/entity/{e['id']}.html",
        f"openEntityPage('{e['id']}', true);",
    )
print("wrote", len(entities_index), "entity pages")

edge_re2 = re.compile(
    r"\{from:'([^']+)', to:'([^']+)', label:'((?:[^'\\]|\\.)*)', url:'([^']*)', date:'([^']*)', scope:'([^']*)'(?:, country:'([^']*)')?,\n"
    r"   detail:'((?:[^'\\]|\\.)*)'\}"
)
edges_index = []
for m in edge_re2.finditer(html):
    frm, to, label, url, date, scope, country, detail = m.groups()
    unesc = lambda s: s.replace("\\'", "'").replace("\\\\", "\\") if s else s
    edges_index.append({
        "from": frm, "to": to, "label": unesc(label), "url": url, "date": date,
        "scope": scope, "detail": unesc(detail),
    })

label_by_id = {e["id"]: e["label"] for e in entities_index}
seen_edge_ids = set()
for x in edges_index:
    eid = edge_id(x["from"], x["to"], x["date"], x["label"])
    if eid in seen_edge_ids:
        continue
    seen_edge_ids.add(eid)
    from_label = label_by_id.get(x["from"], x["from"])
    to_label = label_by_id.get(x["to"], x["to"])
    title = f"{from_label} {x['label']} → {to_label} — World Pulse"
    desc = x["detail"] or f"{from_label} {x['label']} {to_label}."
    write_page(
        os.path.join(BUILD_DIR, "event", eid + ".html"),
        title,
        desc,
        f"https://getworldpulse.com/event/{eid}.html",
        f"openEventPage('{eid}', true);",
    )
print("wrote", len(seen_edge_ids), "event pages")

# Sitemap now generated, not hand-maintained -- it needs one <url> per
# entity/event page and would silently go stale otherwise as those grow.
sitemap_urls = ["https://getworldpulse.com/"]
sitemap_urls += [f"https://getworldpulse.com/entity/{e['id']}.html" for e in entities_index]
sitemap_urls += [f"https://getworldpulse.com/event/{eid}.html" for eid in seen_edge_ids]
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for i, u in enumerate(sitemap_urls):
    freq = "hourly" if i == 0 else "daily"
    prio = "1.0" if i == 0 else "0.6"
    sitemap.append(f"  <url><loc>{u}</loc><changefreq>{freq}</changefreq><priority>{prio}</priority></url>")
sitemap.append("</urlset>")
with open(os.path.join(BUILD_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(sitemap) + "\n")
print("wrote sitemap.xml:", len(sitemap_urls), "urls")
