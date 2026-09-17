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

html = html.replace("__EXTRA_COUNTRY_PATHS__", extra_paths)
html = html.replace("__EXTRA_COUNTRY_ENTITIES__", extra_entities)
html = html.replace("__PERSON_PROFILES__", person_profiles)

leftover_after = set(re.findall(r"__[A-Z_]+__", html))
print("leftover placeholders:", sorted(leftover_after))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("wrote", OUT, "size:", os.path.getsize(OUT))
