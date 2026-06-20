# -*- coding: utf-8 -*-
"""Fusionne des catégories doublons dans la section #imprimer.
Pour chaque (src, dst, new_title) : déplace les cartes de src à la fin du grid de dst,
renomme le h3 de dst, supprime le bloc src. Idempotent-ish (à lancer une fois)."""
import re, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(BASE, "Dossier-Kobra-S1-Combo.html")

# (sous-chaîne d'identification du h3 source, idem destination, nouveau titre destination complet)
MERGES = [
    ("Réparations & right-to-repair", "Atelier, garage & outdoor",
     "🔧 Atelier, garage, outdoor & réparations"),
    ("Café & thé", "Bar, apéro & œnologie",
     "🍷 Bar, café, thé & apéro"),
    ("Animaux & jardin sauvage", "Plantes",
     "🌱 Plantes, jardin & animaux"),
]

def main():
    doc = open(HTML, encoding="utf-8").read()
    head = doc[:doc.index('<section id="imprimer">')]
    pan = doc.index('<section id="pannes">')
    sec = doc[len(head):pan]
    tail = doc[pan:]
    lines = sec.split("\n")

    def find_h3(sub):
        for i, l in enumerate(lines):
            if "<h3>" in l and sub in l:
                return i
        return -1

    def grid_close_after(h3_idx):
        # première ligne == '  </div>' (grid g3) après le h3
        for j in range(h3_idx + 1, len(lines)):
            if lines[j].strip() == "</div>":
                return j
        return -1

    def block_end(h3_idx):
        # fin du bloc catégorie = ligne avant le prochain <h3> (ou avant </section>)
        for j in range(h3_idx + 1, len(lines)):
            if "<h3>" in lines[j]:
                return j  # exclusif
        return len(lines)

    for src_sub, dst_sub, new_title in MERGES:
        si = find_h3(src_sub)
        di = find_h3(dst_sub)
        if si < 0 or di < 0:
            print(f"SKIP (introuvable) : {src_sub!r} / {dst_sub!r}")
            continue
        # cartes du bloc source
        s_end = block_end(si)
        cards = [l for l in lines[si:s_end] if 'class="model"' in l]
        # renommer dst
        lines[di] = re.sub(r"<h3>.*?</h3>", f"<h3>{new_title}</h3>", lines[di])
        # insérer les cartes avant le grid-close de dst
        gc = grid_close_after(di)
        lines[gc:gc] = cards
        # recalcul des indices du bloc source (décalés par l'insertion si src après dst)
        si = find_h3(src_sub)
        s_end = block_end(si)
        # absorber d'éventuelles lignes vides juste avant le h3 source
        start = si
        while start > 0 and lines[start-1].strip() == "":
            start -= 1
        del lines[start:s_end]
        print(f"Fusionné : {src_sub} ({len(cards)} cartes) -> {new_title}")

    out = head + "\n".join(lines) + tail
    open(HTML, "w", encoding="utf-8").write(out)
    print("OK écrit")

if __name__ == "__main__":
    main()
