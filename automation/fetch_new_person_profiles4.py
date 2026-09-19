"""
Fourth batch: a systematic name-mining sweep of all 212 edges' label+detail
text (regex for multi-word capitalized sequences, cross-checked against the
existing entity list) turned up more real, named political/official figures
that were never tracked. Same fetch/merge pattern as the previous batches.

Usage: python3 automation/fetch_new_person_profiles4.py
"""
import json, os, time, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "cache", "new_person_profiles4.js")

UA = "Mozilla/5.0 (WorldPulseBuild/1.0; contact: local-build)"

# entity id -> (Wikipedia title, display label, country entity id)
PEOPLE = {
    "graham": ("Lindsey Graham", "Graham", "usa"),
    "minaunghlaing": ("Min Aung Hlaing", "Min Aung Hlaing", "mmr"),
    "maduro": ("Nicol\u00e1s Maduro", "Maduro", "ven"),
    "vance": ("JD Vance", "Vance", "usa"),
    "najib": ("Najib Razak", "Najib", "mys"),
    "bago": ("Mohammed Umar Bago", "Bago", "nga"),
    "yoon": ("Yoon Suk Yeol", "Yoon Suk-yeol", "kor"),
    "pistorius": ("Boris Pistorius", "Pistorius", "germany"),
    "babis": ("Andrej Babi\u0161", "Babi\u0161", "cze"),
    "linchialung": ("Lin Chia-lung", "Lin Chia-lung", "twn"),
    "olabi": ("Ibrahim Olabi", "Olabi", "syr"),
    "fbolsonaro": ("Fl\u00e1vio Bolsonaro", "Fl\u00e1vio Bolsonaro", "brazil"),
    "johal": ("Jagtar Singh Johal", "Jagtar Singh Johal", "uk"),
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

    profile_lines = ["var NEW_PERSON_PROFILES4 = {"]
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
