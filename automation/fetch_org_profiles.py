"""
One-off (re-runnable) fetch of Wikipedia summaries for organizations,
regions and key events -- same pattern already used for person profiles.
Not a person, so no photo requirement, but includes one if Wikipedia has
a thumbnail (a flag or logo, usually). Writes cache/org_profiles.js in the
same {id: {desc, extract, photo, wiki}} shape build.py already knows how
to inject.

Usage: python3 automation/fetch_org_profiles.py
"""
import json, os, time, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "cache", "org_profiles.js")

UA = "Mozilla/5.0 (WorldPulseBuild/1.0; contact: local-build)"

# entity id -> Wikipedia article title
TITLES = {
    "afd": "Alternative for Germany",
    "nato": "NATO",
    "idea": "International IDEA",
    "un": "United Nations",
    "wto": "World Trade Organization",
    "who": "World Health Organization",
    "eu": "European Union",
    "g7": "G7",
    "g20": "G20",
    "brics": "BRICS",
    "mercosur": "Mercosur",
    "asean": "ASEAN",
    "au": "African Union",
    "arab_league": "Arab League",
    "osce": "Organization for Security and Co-operation in Europe",
    "duma": "State Duma",
    "donbas": "Donbas",
    "europe": "Europe",
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
    for eid, title in TITLES.items():
        data = fetch_summary(title)
        if "error" in data or data.get("type") == "disambiguation":
            print(f"  FAILED {eid} ({title}): {data.get('error', 'disambiguation page')}")
            continue
        results[eid] = {
            "desc": data.get("description", ""),
            "extract": data.get("extract", ""),
            "photo": (data.get("thumbnail") or {}).get("source", ""),
            "wiki": data.get("content_urls", {}).get("desktop", {}).get("page", "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")),
        }
        print(f"  ok {eid} ({title})")
        time.sleep(0.3)

    lines = ["var ORG_PROFILES = {"]
    for eid, p in results.items():
        def esc(s):
            return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
        lines.append(
            '  %s: {desc:"%s", extract:"%s", photo:"%s", wiki:"%s"},'
            % (eid, esc(p["desc"]), esc(p["extract"]), p["photo"], p["wiki"])
        )
    lines.append("};")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nWrote {len(results)}/{len(TITLES)} profiles to {OUT}")


if __name__ == "__main__":
    main()
