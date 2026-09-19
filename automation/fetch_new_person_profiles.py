"""
One-off (re-runnable) fetch of Wikipedia summaries for world leaders who
appear constantly in event details (quoted, named as the real speaker) but
were never added as tracked entities -- their country was used as a stand-in
actor instead. Without a tracked entity, the automation pipeline is also
instructed to reject any extracted fact naming them directly, so they were
quietly falling through the extraction step too, not just missing a page.

Same fetch pattern as fetch_org_profiles.py, but using raw Wikipedia photo
URLs (not base64) since the site is served from GitHub Pages with no CSP
issue -- matches how org_profiles.js already does it.

Usage: python3 automation/fetch_new_person_profiles.py
"""
import json, os, time, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "cache", "new_person_profiles.js")

UA = "Mozilla/5.0 (WorldPulseBuild/1.0; contact: local-build)"

# entity id -> (Wikipedia article title, country entity id)
PEOPLE = {
    "trump": ("Donald Trump", "usa"),
    "netanyahu": ("Benjamin Netanyahu", "isr"),
    "xi": ("Xi Jinping", "china"),
    "modi": ("Narendra Modi", "india"),
    "milei": ("Javier Milei", "arg"),
    "ramaphosa": ("Cyril Ramaphosa", "zaf"),
    "tolam": ("Tô Lâm", "vnm"),
    "sisi": ("Abdel Fattah el-Sisi", "egy"),
    "tinubu": ("Bola Tinubu", "nga"),
    "pezeshkian": ("Masoud Pezeshkian", "irn"),
    "mkhamenei": ("Mojtaba Khamenei", "irn"),
    "sheinbaum": ("Claudia Sheinbaum", "mex"),
    "espriella": ("Abelardo de la Espriella", "col"),
    "anutin": ("Anutin Charnvirakul", "tha"),
    "jetten": ("Rob Jetten", "nld"),
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

    profile_lines = ["var NEW_PERSON_PROFILES = {"]
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
