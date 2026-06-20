# -*- coding: utf-8 -*-
"""Intègre la vague 6 (3 fichiers JSON theme/models) dans les catégories EXISTANTES.
Cartes sans photo (la photo sera ajoutée ensuite par fetch_photos.py). Dédup par URL."""
import json, re, os, html as H

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(BASE, "Dossier-Kobra-S1-Combo.html")
EXTRAS = os.path.join(BASE, "extras")

# theme du JSON -> sous-chaîne du <h3> de la catégorie cible
TARGET = {
    "bugasalt": "Bug-A-Salt",
    "musique": "Musique (piano",
    "mecanique": "Mécanique fascinante",
}
FILES = {
    "bugasalt": "vague6-bugasalt.json",
    "musique": "vague6-musique.json",
    "mecanique": "vague6-mecanique.json",
}

def card(m):
    name = H.escape(m["name"]); url = H.escape(m["url"], quote=True)
    why = H.escape(m["why"]); diff = m.get("diff", "")
    pill = "med" if ("moyen" in diff.lower() or "diffic" in diff.lower()) else "easy"
    label = H.escape(diff.split("·", 1)[-1].strip() if "·" in diff else diff)
    multi = '<span class="pill multi">multi</span>' if m.get("multi") else ""
    return (f'\n    <div class="model"><h4><a href="{url}">{name}</a></h4>'
            f'<p>{why}</p><div class="meta"><span class="pill {pill}">{label}</span>{multi}</div></div>')

def main():
    doc = open(HTML, encoding="utf-8").read()
    seen = set(re.findall(r'<h4><a href="([^"]+)"', doc))
    added = skipped = 0
    for theme, fname in FILES.items():
        data = json.load(open(os.path.join(EXTRAS, fname), encoding="utf-8"))
        models = data["models"]
        # localiser le grid de la catégorie cible
        h3_sub = TARGET[theme]
        m = re.search(r'<h3>[^<]*' + re.escape(h3_sub) + r'.*?<div class="grid g3">', doc, re.S)
        if not m:
            print(f"ANCRE INTROUVABLE : {theme} ({h3_sub})"); continue
        # fin du grid = premier '\n  </div>' après l'ouverture
        start = m.end()
        close = doc.index("\n  </div>", start)
        cards = ""
        for mod in models:
            if mod["url"] in seen:
                skipped += 1; continue
            seen.add(mod["url"]); cards += card(mod); added += 1
        doc = doc[:close] + cards + doc[close:]
        print(f"{theme}: +{sum(1 for mod in models if mod['url'] in seen)} (cumulé)")
    open(HTML, "w", encoding="utf-8").write(doc)
    print(f"FINI : {added} ajoutées, {skipped} doublons écartés")

if __name__ == "__main__":
    main()
