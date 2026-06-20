# -*- coding: utf-8 -*-
"""
Fusion one-shot : intègre dans la BIBLE (source de vérité) les exclusivités du
manuel public manuels-hub/kobra-s1/kobra-s1.json :
  1. les modèles du hub absents de data/models.json (dédup par URL) -> schéma riche
  2. le cours slicer pédagogique (unique au hub) -> data/slicer_course.json

Rejouable (idempotent sur les URLs déjà présentes). Lancer depuis la racine du repo bible :
    python tools/merge_manuels_hub.py
"""
import sys, io, json, os, re, unicodedata
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
MODELS = os.path.join(ROOT, "data", "models.json")
COURSE = os.path.join(ROOT, "data", "slicer_course.json")
HUB = os.path.join(ROOT, "..", "maurisson-manuels-hub", "kobra-s1", "kobra-s1.json")

bible = json.load(open(MODELS, encoding="utf-8"))
hub = json.load(open(HUB, encoding="utf-8"))

# ---- normalisation URL pour la dédup (ignore /en/, trailing slash, casse) ----
def norm(u):
    if not u:
        return ""
    u = u.strip().lower().rstrip("/")
    u = re.sub(r"^https?://(www\.)?", "", u)
    u = u.replace("/en/", "/")
    return u

bible_urls = {norm(m.get("url")) for m in bible["models"] if m.get("url")}
bible_ids = {m["id"] for m in bible["models"]}
calib = bible.setdefault("calibration_models", [])
calib_urls = {norm(m.get("url")) for m in calib if m.get("url")}
calib_ids = {m.get("id") for m in calib}

# ---- mapping thème hub -> catégories bible -------------------------------
def cats_for(theme):
    t = theme.lower()
    table = [
        ("multi-couleur", ["multicolor"]), ("multicouleur", ["multicolor"]),
        ("utile maison", ["home"]),
        ("musique", ["music"]),
        ("plantes", ["plants", "animals"]),
        ("cadeaux", ["gifts"]),
        ("jouets", ["toys"]),
        ("déco", ["deco_lighting"]),
        ("mécanique", ["mechanical"]),
        ("atelier", ["workshop_outdoor", "repairs"]),
        ("cuisine", ["kitchen"]),
        ("airbnb", ["airbnb"]),
        ("bug-a-salt", ["bugasalt"]),
        ("tuning kobra", ["workshop_outdoor"]),
        ("gaming", ["gaming", "cosplay"]),
        ("fêtes", ["seasonal"]), ("saisonnier", ["seasonal"]),
        ("électronique", ["electronics_maker"]), ("maker", ["electronics_maker"]),
        ("voyage", ["travel_edc"]), ("edc", ["travel_edc"]),
        ("enfance", ["kids_school"]), ("école", ["kids_school"]),
        ("auto", ["auto_moto"]),
        ("bar", ["bar", "coffee_tea"]),
        ("couture", ["sewing_creative"]),
        ("photo", ["photo_video"]),
        ("tests & calibration", []),
    ]
    for key, cats in table:
        if key in t:
            return list(cats)
    return []

def platform_for(url):
    d = norm(url)
    for needle, name in [("makerworld", "MakerWorld"), ("printables", "Printables"),
                         ("thingiverse", "Thingiverse"), ("cults3d", "Cults3D"),
                         ("myminifactory", "MyMiniFactory"), ("thangs", "Thangs")]:
        if needle in d:
            return name
    return "autre"

DIFF = {"très facile": "tres_facile", "tres facile": "tres_facile", "facile": "facile",
        "moyen": "moyen", "difficile": "difficile", "expert": "expert"}

def parse_meta(meta):
    """meta hub -> (time, difficulty, leftover_note)."""
    if not meta:
        return None, None, None
    low = meta.strip().lower()
    if low in DIFF:
        return None, DIFF[low], None
    if re.search(r"\d|min|\bh\b|heure|jour|semaine|pièce|/", low):
        return meta.strip(), None, None
    return None, None, meta.strip()

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s.lower())
    s = re.sub(r"[\s_-]+", "-", s).strip("-")
    return s or "modele"

def uniq_id(base, used):
    cand = base[:60]
    i = 2
    while cand in used:
        cand = f"{base[:56]}-{i}"
        i += 1
    used.add(cand)
    return cand

# ---- fusion des modèles --------------------------------------------------
added = 0
added_calib = 0
for theme in hub["models"]["themes"]:
    is_calib = "calibration" in theme["theme"].lower()
    cats = cats_for(theme["theme"])
    for it in theme["items"]:
        url = it.get("url")
        if not url:
            continue
        # les modèles de calibration vont dans calibration_models (pas dans models)
        if is_calib:
            if norm(url) in calib_urls or norm(url) in bible_urls:
                continue
            calib_urls.add(norm(url))
            time, _d, _l = parse_meta(it.get("meta"))
            cm = {"id": uniq_id(slugify(it["name"]), calib_ids | bible_ids),
                  "name": it["name"], "url": url, "why": it.get("desc", "")}
            if time:
                cm["time"] = time
            cm["order_hint"] = None
            calib.append(cm)
            added_calib += 1
            continue
        if norm(url) in bible_urls:
            continue
        bible_urls.add(norm(url))
        time, diff, leftover = parse_meta(it.get("meta"))
        m = {
            "id": uniq_id(slugify(it["name"]), bible_ids),
            "name": it["name"],
            "categories": cats,
            "url": url,
            "platform": platform_for(url),
            "why": it.get("desc", ""),
        }
        if diff:
            m["difficulty"] = diff
        if time:
            m["time"] = time
        m["multicolor"] = "multi" if it.get("multi") else "mono"
        m["tags"] = []
        notes = []
        if leftover:
            notes.append(leftover)
        if "tuning kobra" in theme["theme"].lower():
            notes.append("Mod machine Kobra S1.")
        if notes:
            m["notes"] = " ".join(notes)
        m["origin_files"] = ["manuels-hub:kobra-s1/index.html"]
        m["see_also"] = []
        bible["models"].append(m)
        added += 1

# maj du compteur _meta éventuel
if isinstance(bible.get("_meta"), dict):
    bible["_meta"]["merged_from_manuels_hub"] = True

json.dump(bible, open(MODELS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- extraction du cours slicer -----------------------------------------
WANT = ["réglages slicer optimaux", "où ça se règle", "slicer expliqué pour de vrai"]
course_secs = [s for s in hub["sections"]
               if any(w in s["title"].lower() for w in WANT)]
course = {
    "_meta": {
        "machine": "Anycubic Kobra S1 Combo + ACE Pro",
        "part": "slicer_course",
        "role": "Cours pédagogique du slicer (Anycubic Slicer Next), prose lisible + tables. "
                "Migré depuis le manuel public manuels.maurisson.com/kobra-s1/.",
        "source_url": hub["_meta"].get("source_url"),
        "lang": "fr",
    },
    "sections": course_secs,
}
json.dump(course, open(COURSE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"Modèles : +{added} ajoutés -> total {len(bible['models'])}")
print(f"Calibration : +{added_calib} ajoutés -> total {len(calib)}")
print(f"Cours slicer : {len(course_secs)} sections -> data/slicer_course.json "
      f"({os.path.getsize(COURSE)/1024:.0f} Ko)")
# sanity dédup
allids = [m["id"] for m in bible["models"]]
print("ids uniques :", len(set(allids)) == len(allids), "| total ids", len(allids))
