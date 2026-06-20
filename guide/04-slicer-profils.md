# 05 — Slicer et profils (Kobra S1 Combo + ACE Pro)

> Dossier projet Kobra S1 Combo — recherche du 2026-06-10. Sources croisées : wiki Anycubic, GitHub OrcaSlicer/Rinkhals, reviews (Tom's Hardware, VoxelMatters, 3DWithUs, Creative Bloq), profils communautaires.

---

## 1. TL;DR — quelle stratégie slicer

| Besoin | Outil |
|---|---|
| Démarrer vite, multi-couleur ACE Pro sans prise de tête, envoi LAN/cloud | **Anycubic Slicer Next (ASN)** — c'est un fork d'OrcaSlicer, donc l'interface est quasi identique |
| Calibrations poussées (PA, flow, temp tower), profils communautaires, contrôle total | **OrcaSlicer** (profils Kobra S1 inclus dans les versions récentes) |
| OrcaSlicer **avec envoi réseau direct + interface web Fluidd/Mainsail** | OrcaSlicer + firmware custom **Rinkhals** (overlay, réversible) |

Stratégie recommandée par la communauté : **commencer sur ASN** (le multi-couleur ACE Pro y est natif et le calcul de purge automatique), puis **passer à Orca** quand on veut optimiser — soit en exportant le G-code sur clé USB, soit en installant Rinkhals pour l'envoi LAN direct.

⚠️ Les reviewers sont durs avec ASN : Tom's Hardware titre carrément que « son slicer nous fait pleurer » (bugs, lourdeur, dépendance au cloud Anycubic). Il fait le job, mais Orca reste la référence pour la qualité.

Sources : [Tom's Hardware — review Kobra S1](https://www.tomshardware.com/3d-printing/anycubic-kobra-s1-review) · [Anycubic Slicer Next (wiki)](https://wiki.anycubic.com/en/software-and-app/new-page-anycubic-slicer-beta(orca-version)) · [Creative Bloq — review S1 Combo](https://www.creativebloq.com/3d/anycubic-kobra-s1-combo-review-excellent-when-it-works-frustrating-when-it-doesnt)

---

## 2. Anycubic Slicer Next vs OrcaSlicer — le détail

**ASN = fork open-source d'OrcaSlicer** optimisé pour les machines Anycubic. Il ajoute par rapport à Orca :
- Compte Anycubic + **impression à distance via cloud**, monitoring vidéo, contrôle machine, gestion de fichiers cloud.
- **Mode LAN** : officiellement, *seul ASN* supporte l'envoi en réseau local vers la S1 en firmware stock ([guide LAN Anycubic](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1/lan-connection-guide)).
- Calcul **automatique des volumes de purge** entre couleurs (algorithme basé sur couleur + type des deux filaments).
- Outils maison : « Adaptive Pressure Advance », « YOLO Flow Calibration ».

**Ce qu'Orca fait mieux** : calibrations plus complètes et éprouvées (PA tower, flow rate pass 1/2, temp tower, retraction test, VFA), profils pour des centaines de machines, intégration Klipper, mises à jour plus fréquentes, pas de dépendance cloud.

Sources : [wiki ASN](https://wiki.anycubic.com/en/software-and-app/new-page-anycubic-slicer-beta(orca-version)) · [update record ASN](https://wiki.anycubic.com/en/software-and-app/new-page-anycubic-slicer-beta(orca-version)/anycubic-slicer-next-(orca-version)-update-record) · [Obico — Orca Slicer overview](https://www.obico.io/blog/orca-slicer-download/)

---

## 3. Connecter la S1 à OrcaSlicer — 3 options

### Option A — Firmware stock, sans réseau (la plus simple)
1. Dans Orca : ajouter l'imprimante **Anycubic Kobra S1** (présente dans les versions récentes d'Orca ; sinon profils communautaires, voir §4).
2. Slicer dans Orca → **exporter le G-code** → clé USB → imprimer.
3. Variante : importer le G-code dans ASN et l'envoyer en LAN/cloud depuis là.

⚠️ Point de vigilance multi-couleur en firmware stock : le **G-code de changement de filament** du profil Orca par défaut ne collait pas exactement à celui d'ASN — vérifier/mettre à jour le « machine change filament G-code » (issue ouverte : [OrcaSlicer #11632](https://github.com/OrcaSlicer/OrcaSlicer/issues/11632)).

### Option B — Firmware custom Rinkhals (la voie royale, choix de la communauté)
[Rinkhals](https://github.com/jbatonnet/Rinkhals) est un **overlay** sur le firmware Anycubic (Kobra S1 supporté, firmwares testés 2.7.0.9 et 2.7.2.7) : il garde l'écran tactile et les fonctions stock, et ajoute **Moonraker + Mainsail/Fluidd + caméra USB (mjpg-streamer) + VNC + mDNS**.

Procédure Orca + Rinkhals (d'après la [doc officielle Rinkhals/Orca](https://github.com/jbatonnet/Rinkhals/blob/master/docs/docs/guides/orca-slicer-usage.md)) :
1. Télécharger Orca depuis le **GitHub officiel** (éviter les sites miroirs type orcaslicer.net).
2. Sélectionner le preset **Kobra S1 (Combo)** — seuls Kobra 3 et Kobra S1 ont des presets dédiés côté Rinkhals.
3. Bouton **Connexion** (icône WiFi dans la section imprimante) → entrer **uniquement l'IP locale** de la S1, laisser le reste vide → Test.
4. Mettre une **IP statique** sur le routeur (sinon déconnexions).
5. Fluidd ou Mainsail doit tourner sur l'imprimante (apps activées dans Rinkhals).
6. Envoi direct depuis Orca ; l'écran d'impression s'affiche sur la machine. L'onglet « Device » d'Orca donne accès à Mainsail/Fluidd.

Bonus Rinkhals + ACE Pro : un driver communautaire publie l'inventaire des 4 slots (type + couleur) vers Moonraker (`lane_data`), et les builds récents d'Orca peuvent **pré-remplir automatiquement les filaments** ([Kobra-S1/ACEPRO](https://github.com/Kobra-S1/ACEPRO)). Encore jeune — à considérer comme expérimental.

⚠️ Rinkhals = firmware non officiel : risque théorique pour la garantie, mais overlay désinstallable. Très largement adopté par les possesseurs de S1.

### Option C — Rester 100 % ASN
LAN + cloud + multi-couleur natifs, zéro bidouille. C'est l'option « ça marche tout de suite », au prix d'un slicer moins abouti.

Sources : [Rinkhals docs](https://jbatonnet.github.io/Rinkhals/) · [guide réseau S1 (2,4 GHz uniquement, pas de 5 GHz)](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/network-connection-guide-and-troubleshooting) · [OrcaSlicer #7961 — demande de profil S1](https://github.com/OrcaSlicer/OrcaSlicer/issues/7961)

---

## 4. Profils Orca recommandés

- **Profil officiel Orca** : « Anycubic Kobra S1 » est inclus dans les versions récentes (2.3+). Bon point de départ, mais G-code de changement de filament à vérifier (cf. §3A).
- **[MPC561/Anycubic-Kobra-S1-Orcaslicer-Profiles](https://github.com/MPC561/Anycubic-Kobra-S1-Orcaslicer-Profiles)** — le plus complet côté communauté :
  - Profil imprimante avec **start G-code amélioré** (nettoyage buse avant probe + « bubble » de pré-extrusion → meilleur Z-offset et première couche).
  - Process en 0.08 / 0.12 / 0.16 / 0.20 / 0.24 mm, chacun en 3 niveaux (Standard rapide / Medium / Structural précis).
  - Filaments : PLA, PETG (generic, Jayo, Deeply), ABS (generic, eSun), ASA (generic, Eryone), PETG-CF.
  - Débits volumétriques relevés : **PETG jusqu'à 23 mm³/s, ABS 28 mm³/s** (vs 12–15 mm³/s sur les profils Anycubic, jugés très conservateurs).
  - **Rétraction réduite à ~1,5 mm → valeurs plus basses** pour limiter les défauts (au prix d'un peu plus de stringing).
- **[ditschi/OrcaSlicer-user-profiles](https://github.com/ditschi/OrcaSlicer-user-profiles)** — autre set Kobra S1 Combo, plus simple.

---

## 5. Vitesses : marketing vs réalité

Les **600 mm/s** (et 20 000 mm/s² d'accélération) annoncés sont atteignables en pointe sur des segments courts, mais toutes les reviews convergent :

| Situation | Vitesse réaliste |
|---|---|
| PLA qualité correcte, usage courant | **200–300 mm/s** |
| Pièces où la qualité prime | 150–250 mm/s |
| Pousser la machine (pièces simples) | 300–400 mm/s |
| **Multi-couleur ACE Pro** | **150–200 mm/s** effectifs (les changements de filament dominent le temps d'impression de toute façon) |

À retenir : sur un print multi-couleur, le goulot n'est pas la vitesse de dépose mais les **changements de filament (~1 min 30 à 2 min par swap)**. Optimiser la purge (§6) rapporte plus que monter la vitesse.

Sources : [VoxelMatters](https://www.voxelmatters.com/anycubic-kobra-s1-review-no-fuss-corexy-for-speed-and-reliability/) · [Ryan Mercer — review Combo](https://www.ryanmercer.com/ryansthoughts/2025/10/29/anycubic-kobra-s1-combo-review-the-budget-multi-color-beast) · [LinuxNiche](https://blog.linuxniche.com/2025/03/anycubic-kobra-s1-review/) · [3DWithUs](https://3dwithus.com/anycubic-kobra-s1-combo-review-3d-printer-tests-tips-and-settings)

---

## 6. Multi-couleur : purge, tour, regroupement

### Comment marche la purge (flush)
À chaque changement de couleur, l'ancienne couleur est chassée de la buse → déchet (« poop » éjecté à l'arrière + tour de purge). ASN/Orca calculent un **volume de purge automatique** par paire de couleurs (matrice N×N) : foncé → clair = beaucoup de purge, clair → foncé = peu.

### Réduire le gaspillage — leviers concrets (Orca et ASN)
1. **Flush multiplier** : la matrice auto est volontairement large. Descendre le multiplicateur à **0,4–0,6** et tester ; remonter si du bleeding apparaît. (Réglage aussi accessible *pendant* l'impression dans les paramètres ACE Pro de la machine, à doser prudemment.)
2. **Matrice manuelle** : plafonner les pires paires (ex. noir→blanc) plutôt que tout baisser uniformément. ASN recommande de rester **≤ 900 mm³** par paire ([wiki Anycubic — reduce waste](https://wiki.anycubic.com/en/home/knowledge-sharing/reduce-waste)).
3. **« Flush into objects' infill »** et **« flush into objects »** (Orca, onglet Others) : purger dans le remplissage / les supports au lieu de jeter — gratuit, à activer quasi systématiquement quand l'infill est invisible.
4. **Tour de purge (prime tower)** : réduire sa largeur (35 → 25 mm) et activer « purge dans l'infill » d'abord ; la tour ne sert qu'au reliquat.
5. **Ordonner les couleurs** : peindre le modèle pour que les transitions claires→foncées dominent (le sens foncé→clair coûte cher).
6. **Regrouper par couleur / par hauteur** : quand c'est possible, séparer les zones de couleur en hauteur (logo bicolore : changement à la couche N = 1 seul swap) plutôt qu'en damier (swaps à chaque couche). Pour des objets distincts monocouleurs : imprimer **« one by one »** ou par plaques séparées plutôt qu'un print multi-couleur.
7. Imprimer un **bac à poop grand volume** ([modèle Printables dédié S1](https://www.printables.com/model/1290304-anycubic-kobra-s1-large-volume-filament-waste-purg)) — ne réduit pas le déchet mais évite le débordement.

Vidéo de référence sur l'optimisation des flush amounts S1 : [« This printer poops too much »](https://www.youtube.com/watch?v=i5ce2Ow3F3M).

⚠️ Incertitude : il n'existe pas de « bonne valeur » universelle de flush multiplier — 0,4–0,6 est le point de départ communautaire courant, mais ça dépend des marques de filament et des paires de couleurs. Tester sur un print 2 couleurs sacrificiel.

Sources : [wiki Anycubic reduce-waste](https://wiki.anycubic.com/en/home/knowledge-sharing/reduce-waste) · [Tom's Hardware](https://www.tomshardware.com/3d-printing/anycubic-kobra-s1-review) · [Creative Bloq](https://www.creativebloq.com/3d/anycubic-kobra-s1-combo-review-excellent-when-it-works-frustrating-when-it-doesnt)

---

## 7. TPU et ACE Pro : ils ne font PAS bon ménage (confirmé)

C'est officiel, pas une rumeur — wiki Anycubic :

- **Ne jamais alimenter du TPU via l'ACE Pro** : le filament souple flambe/se coince dans les canaux de l'ACE → échec d'alimentation. (Même restriction sur l'ACE 2 Pro.)
- **TPU ≥ 95A uniquement** sur la S1. TPU ≤ 85A : interdit (écrasé par la roue d'extrusion → bouchon).
- Procédure : bobine TPU sur le **support arrière**, retirer le tube bowden du hub de filament et de la tête, **insérer le filament en direct** par le tube PTFE arrière jusqu'à l'extrudeur.
- Réglages TPU S1 : buse **220–230 °C**, **vitesse basse** (rester ≤ 100 mm/s, le wiki insiste : vitesse élevée = bourrage), imprimer les modèles **un par un** plutôt qu'en plein plateau, rétraction faible.
- **Sécher le TPU avant** : 50–55 °C pendant 4–6 h dans l'ACE Pro (le séchage dans l'ACE est OK, c'est juste l'*alimentation* qui ne l'est pas).
- L'ACE Pro reste donc une station 4 couleurs **PLA/PETG** ; le TPU = mono-couleur en direct. Il existe un hub 5-en-1 communautaire pour garder une voie manuelle permanente ([Printables](https://www.printables.com/model/1291687-5-to-1-filament-hub-for-anycubic-kobra-s1-combo)).

Sources : [wiki Anycubic — TPU Printing Guide S1](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/tpu-printing-guide) · [TPU printing (knowledge sharing)](https://wiki.anycubic.com/en/home/knowledge-sharing/tpu-printing-recommendations) · [page produit ACE 2 Pro (même restriction TPU)](https://store.anycubic.com/products/ace-2-pro)

---

## 8. Séchage filament avec l'ACE Pro

L'ACE Pro (celui du S1 Combo) sèche **jusqu'à 55 °C max** — y compris **pendant l'impression**. C'est suffisant pour PLA/TPU/PETG ; insuffisant pour vraiment *sécher* ABS/ASA/Nylon/PC (mais OK pour les *maintenir* secs s'ils sont déjà en bon état). L'ACE 2 Pro monte à 65–70 °C, pas l'ACE Pro v1.

| Matériau | Température ACE Pro | Durée | Note |
|---|---|---|---|
| PLA | **45–50 °C** | 4–6 h | au-delà de 50 °C, risque de ramollir le PLA |
| PETG | **55 °C** (max machine) | 6–7 h | l'idéal serait 65 °C — l'ACE Pro plafonne, prévoir plus long |
| TPU | **50–55 °C** | 4–6 h | recommandation officielle Anycubic avant tout print TPU |
| ABS/ASA | 55 °C (max) | maintien seulement | vrai séchage = 75–80 °C → dryer externe nécessaire |

Réflexe pratique : activer le séchage à 50–55 °C **pendant** les longs prints PETG — gros gain de qualité (moins de stringing/bulles), surtout en Belgique humide.

⚠️ Incertitude : durées PLA/PETG = consensus général (Overture, Bambu, Sovol convergent), Anycubic ne publie de durée officielle que pour le TPU (4–6 h).

Sources : [Tom's Hardware (55 °C max, séchage en cours d'impression)](https://www.tomshardware.com/3d-printing/anycubic-kobra-s1-review) · [ACE Pro Dryer Guide (wiki)](https://wiki.anycubic.com/en/fdm-3d-printer/ace-pro/ace-pro-dryerguide) · [TPU guide S1](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/tpu-printing-guide) · [Overture — How to dry filament](https://overture3d.com/blogs/overture-blogs/how-to-dry-3d-printer-filament) · [Bambu Lab — drying recommendations](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)

---

## 9. Premiers réglages — checklist calibration

### Ordre recommandé (dans Orca, menu Calibration)
1. **Temperature tower** par bobine → choisir la temp la plus basse qui garde une bonne adhésion inter-couches.
2. **Pressure Advance (PA tower)** — *avant* le flow. La S1 est direct drive : valeurs typiquement **0,02–0,05 pour le PLA** (point de départ ; le test Orca donne la valeur exacte). PETG un peu plus haut, TPU beaucoup plus haut. ASN propose en plus un « Adaptive Pressure Advance ».
3. **Flow rate (pass 1 puis pass 2)** — une fois par *type* de matériau (PLA/PETG/TPU), pas par bobine. Modèle de test dédié Kobra : [Flow Rate Cube MakerWorld](https://makerworld.com/en/models/470614-anycubic-flow-rate-cube-calibration-kobra-series).
4. **Retraction test** si stringing (rappel : profils MPC561 = rétraction réduite vs 1,5 mm d'origine).
5. Avant les prints importants : **bed mesh** complet (5×5 voire 7×7 — recommandé par MPC561 avec son start G-code amélioré).

Référence : [wiki OrcaSlicer — pressure advance calib](https://github.com/OrcaSlicer/OrcaSlicer/wiki/pressure-advance-calib) · [adaptive PA](https://github.com/OrcaSlicer/OrcaSlicer/wiki/adaptive-pressure-advance-calib) · [wiki Anycubic — Flow/PA](https://wiki.anycubic.com/en/home/knowledge-sharing/pressure-advance)

### Plaque et températures plateau
La S1 est livrée avec une **plaque PEI texturée flexible** (machine fermée → ABS/ASA possibles).

| Matériau | Plateau | Buse | Notes |
|---|---|---|---|
| PLA | **60 °C** | 200–210 °C | 200 °C lent/propre, 210 °C pièces fonctionnelles ; ventilation 100 % dès couche 2 ; **ouvrir la porte/le capot** sur les longs prints PLA (machine fermée = heat creep) |
| PETG | **70–80 °C** (75 °C bon compromis sur PEI) | 230–250 °C | PEI texturé : pas de colle nécessaire ; première couche lente (~15–20 mm/s) ; ne PAS dépasser 80 °C (pièce quasi indécollable) |
| TPU | 30–40 °C | 220–230 °C | alimentation directe uniquement (§7) |
| ABS/ASA | 90–100 °C | 240–260 °C | porte fermée, profils MPC561 dispo |

Sources : [3D Printed Decor — Kobra S1 PLA settings](https://3dprinteddecor.com/anycubic-kobra-s1-pla-settings/) · [Overture — PETG bed temperature](https://overture3d.com/blogs/blogs/petg-bed-temperature) · [Wevolver — PETG settings](https://www.wevolver.com/article/petg-print-settings) · [MPC561 profiles](https://github.com/MPC561/Anycubic-Kobra-S1-Orcaslicer-Profiles)

### Divers premiers jours
- WiFi : **2,4 GHz uniquement** (pas de 5 GHz) — [guide réseau](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/network-connection-guide-and-troubleshooting).
- Garder le firmware imprimante à jour via l'écran (les fixes ACE Pro sont fréquents).
- Premier print multi-couleur : modèle 2 couleurs simple, flush multiplier 1,0 → puis re-slicer à 0,5 et comparer (bleeding ?). C'est le test le plus rentable du dossier.

---

*Fichier généré le 2026-06-10 — recherches web croisées, liens vérifiés à cette date. Les pages wiki.anycubic.com bloquent parfois le fetch direct (403) mais sont accessibles en navigateur.*
