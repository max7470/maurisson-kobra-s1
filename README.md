# 🖨️ Bible machine — Anycubic Kobra S1 Combo + ACE Pro

> La référence complète de l'imprimante 3D de Maxime. Deux étages :
> - **`data/*.json`** → couche **machine-readable** : tout le savoir éclaté en JSON autoportants et requêtables, pour que n'importe quelle IA consulte précisément ce dont elle a besoin, à la demande.
> - **`guide/`** → la même chose en **prose lisible** (markdown), pour l'humain.
>
> 🔗 À rattacher au **Labo 3D de Maurisson** (skill `maurisson-3d`).
> 📅 Recherche source : **2026-06-10** · Compilation/refonte JSON : **2026-06-20**.

## 🌐 En ligne (GitHub)

- **Repo** : https://github.com/max7470/maurisson-kobra-s1
- **Tableau de bord** (GitHub Pages) : **https://max7470.github.io/maurisson-kobra-s1/**
- **Base raw pour les IA** : `https://raw.githubusercontent.com/max7470/maurisson-kobra-s1/main/`
  - Manifest d'entrée : `…/main/kobra-s1.json`
  - Données : `…/main/data/<fichier>.json` (ex. `…/main/data/models.json`)

> Sync multi-machine = **git** (`git pull --ff-only` en début de session, `git add -A && git commit && git push` en fin). Le clone vit en local **hors Drive** (Drive corromprait le `.git`).

---

## 🧭 Comment l'utiliser

**Tu es une IA ?** Commence par **[`kobra-s1.json`](kobra-s1.json)** (le manifest) : il contient les `quick_facts`, les `golden_rules`, et la carte de tous les fichiers `data/` avec « quand charger quoi ». Charge ensuite uniquement le JSON pertinent.

**Tu es humain ?** Le tableau ci-dessous, ou plonge dans `guide/`.

---

## 📂 Structure

```
Imprimante Kobra S1 Combo/
├── README.md                ← tu es ici
├── kobra-s1.json            ← MANIFEST : index d'entrée pour les IA (quick facts, règles d'or, carte des fichiers)
├── data/                    ← SOURCE DE VÉRITÉ machine-readable (9 JSON)
│   ├── printer.json         ← specs machine + ACE Pro
│   ├── calibration.json     ← leveling, flow/PA, input shaping, 1re couche, temps par matériau
│   ├── maintenance.json     ← entretien machine + ACE Pro
│   ├── troubleshooting.json ← codes d'erreur + pannes + fixes + MAJ firmware
│   ├── consumables.json     ← pièces & consommables à stocker
│   ├── materials.json       ← guide des 10 filaments (temps, prix EU, marques, pièges)
│   ├── slicer.json          ← slicer, profils, vitesses, purge multicouleur, séchage
│   ├── slicer_course.json   ← COURS slicer pédagogique (chaque réglage expliqué) — migré du manuel public
│   ├── mods.json            ← Rinkhals, sortie du cloud, Home Assistant, mods imprimables, upgrades
│   └── models.json          ← CATALOGUE de modèles à imprimer (737 + systèmes + calibration), dédupliqué
├── guide/                   ← prose lisible (markdown)
│   ├── 01-machine.md
│   ├── 02-demarrage-pieges.md
│   ├── 03-mods-firmware.md
│   ├── 04-slicer-profils.md
│   ├── 05-filaments.md
│   └── modeles/             ← sources prose des modèles (vagues 1 à 6 + tuning + bug-a-salt)
├── etude-achat-comparatif/  ← 3 PDF d'étude d'achat + scripts + photos
├── photos-modeles/          ← vignettes des modèles
└── tools/                   ← scripts utilitaires
```

---

## 📊 Carte des données

| Domaine | JSON | Prose | Pour quoi |
|---|---|---|---|
| Specs machine + ACE Pro | [`data/printer.json`](data/printer.json) | [guide/01](guide/01-machine.md) | Capacités, fonctionnement ACE Pro, ventilos, connectivité |
| Calibrations | [`data/calibration.json`](data/calibration.json) | [guide/01](guide/01-machine.md) | Leveling, flow/PA, 1re couche, temps par matériau |
| Maintenance | [`data/maintenance.json`](data/maintenance.json) | [guide/01](guide/01-machine.md) | Entretien périodique machine + ACE Pro |
| Pannes & erreurs | [`data/troubleshooting.json`](data/troubleshooting.json) | [guide/01](guide/01-machine.md) | Codes d'erreur, bouchons, bourrages, fixes, firmware |
| Consommables | [`data/consumables.json`](data/consumables.json) | [guide/02](guide/02-demarrage-pieges.md) | Quoi stocker, où acheter |
| Filaments | [`data/materials.json`](data/materials.json) | [guide/05](guide/05-filaments.md) | 10 matériaux, prix EU/Belgique, marques, kit de démarrage |
| Slicer & profils | [`data/slicer.json`](data/slicer.json) | [guide/04](guide/04-slicer-profils.md) | ASN vs Orca, purge, vitesses, séchage |
| Cours slicer | [`data/slicer_course.json`](data/slicer_course.json) | — | **Chaque réglage expliqué** (layer height, vitesse, parois, infill, T°, rétraction, supports, purge…) + où ça se règle dans ASN |
| Mods & firmware | [`data/mods.json`](data/mods.json) | [guide/03](guide/03-mods-firmware.md) | Rinkhals, cloud, Home Assistant, upgrades, 15 mods machine S1 |
| Modèles à imprimer | [`data/models.json`](data/models.json) | [guide/modeles/](guide/modeles/) | **737 modèles** dédupliqués (vagues 1-6 + Bug-A-Salt + manuel public) + 11 systèmes + 9 calibration, 26 catégories |

---

## ⚡ Les règles d'or (résumé)

1. **Déballage** : retirer les **6 vis de transport** avant la 1re mise sous tension.
2. **TPU & fibrés (CF/GF)** : **jamais via l'ACE Pro** → tube arrière. TPU ≥ 95A. (Le TPU se *sèche* dans l'ACE, puis se sort.)
3. **PLA / PETG** : **porte/capot ouverts** sur les longs prints (heat creep en enceinte fermée). Enceinte fermée = ABS/ASA/PC.
4. **Plateau PEI** : laver au savon, ne jamais toucher avec les doigts. Colle (voile) pour PETG/PC/PA.
5. **Axe X** : jamais de graisse (alcool seulement). Vis Z : graisse, pas d'huile.
6. **Multicouleur** : mono-buse → purge à chaque changement. Flush 0,4-0,6, « flush into infill », couleurs par zone/hauteur, batcher.
7. **Firmware** : ne jamais MAJ sans vérifier la compat **Rinkhals** ; MAJ impossible en mode LAN.
8. **Wi-Fi** : **2,4 GHz uniquement**.

> Détail complet et nuancé : `kobra-s1.json` → `golden_rules`, et chaque `data/*.json`.

---

## 🗂️ Provenance

Cette bible a été compilée à partir du wiki officiel Anycubic, de reviews long-terme (Tom's Hardware, VoxelMatters, Creative Bloq, 3DWithUs, 3DWork…), de GitHub (Rinkhals, profils OrcaSlicer), des groupes communautaires, et de MakerWorld / Printables / Thingiverse / Cults3D pour les modèles. Tous les liens sources sont conservés dans les champs `sources` de chaque JSON. Les incertitudes assumées sont signalées dans les champs `uncertainties` / `uncertainty`.
