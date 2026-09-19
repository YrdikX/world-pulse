"""
Third batch: comprehensive sweep of event detail text for any remaining
named individual not yet a tracked entity. Same fetch/merge pattern as the
previous two batches.

Usage: python3 automation/fetch_new_person_profiles3.py
"""
import json, os, time, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "cache", "new_person_profiles3.js")

UA = "Mozilla/5.0 (WorldPulseBuild/1.0; contact: local-build)"

# entity id -> (Wikipedia title, display label, country entity id)
PEOPLE = {
    "erdogan": ("Recep Tayyip Erdo\u011fan", "Erdogan", "tur"),
    "lecornu": ("S\u00e9bastien Lecornu", "Lecornu", "france"),
    "vturk": ("Volker T\u00fcrk", "Türk", "un"),
    "kimyojong": ("Kim Yo-jong", "Kim Yo Jong", "prk"),
    "johnlee": ("John Lee Ka-chiu", "John Lee", "hkg"),
    "frederiksen": ("Mette Frederiksen", "Frederiksen", "dnk"),
    "abbas": ("Mahmoud Abbas", "Abbas", "wbg"),
    "kravchenko": ("Ruslan Kravchenko", "Kravchenko", "ukraine"),
    "coale": ("John Coale", "Coale", "usa"),
    "velasco": ("Roberto Velasco Alvarado", "Velasco", "mex"),
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
    for eid, (title, label, country) in PEOPLE.items():
        data = fetch_summary(title)
        if "error" in data or data.get("type") == "disambiguation":
            print(f"  FAILED {eid} ({title}): {data.get('error', 'disambiguation page')}")
            continue
        results[eid] = {
            "country": country,
            "label": label,
            "desc": data.get("description", ""),
            "extract": data.get("extract", ""),
            "photo": (data.get("thumbnail") or {}).get("source", ""),
            "wiki": data.get("content_urls", {}).get("desktop", {}).get("page", "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")),
        }
        print(f"  ok {eid} ({title})")
        time.sleep(0.3)

    def esc(s):
        return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")

    profile_lines = ["var NEW_PERSON_PROFILES3 = {"]
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
