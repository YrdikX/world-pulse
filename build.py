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
