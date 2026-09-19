"""
Second batch: people named directly in event detail text (not just heads of
state of the biggest powers) that still weren't tracked entities -- found by
scanning all current edges' detail text for proper names and cross-checking
against automation/entities.json. Same fetch/merge pattern as
fetch_new_person_profiles.py.

Usage: python3 automation/fetch_new_person_profiles2.py
"""
import json, os, time, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "cache", "new_person_profiles2.js")

UA = "Mozilla/5.0 (WorldPulseBuild/1.0; contact: local-build)"

PEOPLE = {
    "macron": ("Emmanuel Macron", "france"),
    "merz": ("Friedrich Merz", "germany"),
    "rutte": ("Mark Rutte", "nato"),
    "costa": ("Ant\u00f3nio Costa", "eu"),
    "okonjo_iweala": ("Ngozi Okonjo-Iweala", "wto"),
    "anwar": ("Anwar Ibrahim", "mys"),
    "dissanayake": ("Anura Kumara Dissanayake", "lka"),
    "mahama": ("John Mahama", "gha"),
    "nawrocki": ("Karol Nawrocki", "poland"),
    "lula": ("Lula da Silva", "brazil"),
    "leejaemyung": ("Lee Jae-myung", "kor"),
    "mirziyoyev": ("Shavkat Mirziyoyev", "uzb"),
    "noboa": ("Daniel Noboa", "ecu"),
    "arevalo": ("Bernardo Ar\u00e9valo", "gtm"),
    "saied": ("Kais Saied", "tun"),
    "paz": ("Rodrigo Paz Pereira", "bol"),
    "andersson": ("Magdalena Andersson", "swe"),
    "kristersson": ("Ulf Kristersson", "swe"),
    "nauseda": ("Gitanas Naus\u0117da", "lithuania"),
    "kushner": ("Jared Kushner", "usa"),
    "witkoff": ("Steve Witkoff", "usa"),
    "lutnick": ("Howard Lutnick", "usa"),
    "banerjee": ("Mamata Banerjee", "india"),
    "norlen": ("Andreas Norl\u00e9n", "swe"),
    "burke": ("Tony Burke", "aus"),
    "crosetto": ("Guido Crosetto", "italy"),
}


def fetch_summary(title):
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(title.replace(" ", "_"))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}


def main():
    results = {}
    for eid, (title, country) in PEOPLE.items():
        data = fetch_summary(title)
        if "error" in data or data.get("type") == "disambiguation":
            print(f"  FAILED {eid} ({title}): {data.get('error', 'disambiguation page')}")
            continue
        results[eid] = {
            "country": country,
            "label": title.split(" (")[0],
            "desc": data.get("description", ""),
            "extract": data.get("extract", ""),
            "photo": (data.get("thumbnail") or {}).get("source", ""),
            "wiki": data.get("content_urls", {}).get("desktop", {}).get("page", "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")),
        }
        print(f"  ok {eid} ({title})")
        time.sleep(0.3)

    def esc(s):
        return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")

    profile_lines = ["var NEW_PERSON_PROFILES2 = {"]
    entity_lines = []
    for eid, p in results.items():
        profile_lines.append(
            '  %s: {desc:"%s", extract:"%s", photo:"%s", wiki:"%s"},'
            % (eid, esc(p["desc"]), esc(p["extract"]), p["photo"], p["wiki"])
        )
        entity_lines.append(
            "  {id:'%s', label:'%s', type:'person', country:'%s'}," % (eid, esc(p["label"]), p["country"])
        )
    profile_lines.append("};")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(profile_lines) + "\n\n// entity declarations for reference/copy-paste into world_pulse_template.html:\n")
        f.write("\n".join(entity_lines) + "\n")
    print(f"\nWrote {len(results)}/{len(PEOPLE)} profiles to {OUT}")


if __name__ == "__main__":
    main()
