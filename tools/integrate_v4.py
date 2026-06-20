# -*- coding: utf-8 -*-
"""Intègre les modèles de la vague 4 (sortie structurée du workflow) dans le HTML.
Usage : python integrate_v4.py <chemin_output_workflow.json>
- Catégories existantes : cartes insérées en tête de grille.
- Nouvelles catégories : sections créées avant le callout Matériaux.
- Dédup par URL contre le HTML existant.
"""
import json, re, sys, os, html as H

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(BASE, "Dossier-Kobra-S1-Combo.html")

EXISTING = {
    "jouets": "<h3>🧸 Jouets & jeux</h3>",
    "deco": "<h3>🏮 Déco & lumière</h3>",
    "mecanique": "<h3>⚙️ Mécanique fascinante — les prints « impossibles autrement »</h3>",
    "maison": "<h3>🍳 Cuisine & organisation</h3>",
    "jardin": "<h3>🔧 Atelier, garage & outdoor</h3>",
    "musique": "<h3>🎵 Musique (piano, harmonica, studio)</h3>",
    "airbnb": "<h3>🏡 Spécial Airbnb — « Chez Maurisson » édition boutique-hôtel</h3>",
}
NEW = {  # ordre d'insertion
    "gaming": "🎮 Gaming, JdR & cosplay",
    "fetes": "🎄 Fêtes & saisonnier",
    "animaux": "🐾 Animaux & jardin sauvage",
    "electronique": "🔌 Électronique & maker",
    "voyage": "🎒 Voyage & EDC",
    "enfants": "🧒 Petite enfance & école",
}
AIRBNB_KW = ("savon", "plateau", "serviette", "parapluie", "veilleuse", "chausson",
             "patère", "patere", "butoir", "verre", "accueil", "coaster", "dessous")

def card(m):
    name, url = H.escape(m["name"]), H.escape(m["url"], quote=True)
    why = H.escape(m["why"])
    diff = m.get("diff", "")
    pill = "med" if "moyen" in diff.lower() else "easy"
    label = H.escape(diff.split("·", 1)[-1].strip() if "·" in diff else diff)
    multi = '<span class="pill multi">multi</span>' if m.get("multi") else ""
    return (f'\n    <div class="model"><h4><a href="{url}">{name}</a></h4>'
            f'<p>{why}</p><div class="meta"><span class="pill {pill}">{label}</span>{multi}</div></div>')

def main():
    out = json.load(open(sys.argv[1], encoding="utf-8"))
    batches = out["result"]["batches"]
    doc = open(HTML, encoding="utf-8").read()

    # collecte + dédup URL (contre le doc ET entre agents)
    seen = set(re.findall(r'<div class="model">(?:<a [^>]+</a>)?<h4><a href="([^"]+)"', doc))
    groups, skipped = {}, 0
    for b in batches:
        key = b["theme"]
        for m in b["models"]:
            if m["url"] in seen:
                skipped += 1
                continue
            seen.add(m["url"])
            k = key
            if key == "musique_airbnb":
                blob = (m["name"] + " " + m["why"]).lower()
                k = "airbnb" if any(w in blob for w in AIRBNB_KW) else "musique"
            groups.setdefault(k, []).append(m)

    total = 0
    # catégories existantes : insérer en tête de grille
    for key, h3 in EXISTING.items():
        models = groups.pop(key, [])
        if not models:
            continue
        anchor = h3 + '\n  <div class="grid g3">'
        if anchor not in doc:
            print(f"ANCRE INTROUVABLE pour {key} !")
            continue
        doc = doc.replace(anchor, anchor + "".join(card(m) for m in models), 1)
        total += len(models)
        print(f"{key}: +{len(models)}")

    # nouvelles catégories : avant le callout Matériaux
    tail_anchor = '  <div class="callout yellow"><b>⚠️ Matériaux</b>'
    blocks = ""
    for key, title in NEW.items():
        models = groups.pop(key, [])
        if not models:
            continue
        blocks += (f'\n  <h3>{title}</h3>\n  <div class="grid g3">'
                   + "".join(card(m) for m in models) + "\n  </div>\n")
        total += len(models)
        print(f"{key} (nouvelle): +{len(models)}")
    if blocks:
        doc = doc.replace(tail_anchor, blocks + "\n" + tail_anchor, 1)

    for key, models in groups.items():
        print(f"THEME INATTENDU non intégré : {key} ({len(models)} modèles)")

    open(HTML, "w", encoding="utf-8").write(doc)
    print(f"FINI : {total} cartes ajoutées, {skipped} doublons URL écartés")

if __name__ == "__main__":
    main()
