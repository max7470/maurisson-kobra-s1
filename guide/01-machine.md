# Anycubic Kobra S1 Combo — La machine & le wiki officiel

> Digest du wiki officiel Anycubic (https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-Combo), exploré page par page le 2026-06-10, croisé avec les pages produit Anycubic et des reviews indépendantes. Tout ce qui suit est spécifique à la Kobra S1 Combo + ACE Pro.

---

## 1. La machine en bref

La Kobra S1 Combo = imprimante FDM **CoreXY fermée (caisson)** + module multi-filament **ACE Pro** (4 bobines, séchage actif, y compris pendant l'impression). Sortie début 2025, positionnée comme l'alternative budget à la Bambu Lab P1S Combo.

### Specs complètes (sources : FAQ wiki + pages produit Anycubic)

| Caractéristique | Valeur |
|---|---|
| Volume d'impression | **250 × 250 × 250 mm** |
| Structure | CoreXY caisson fermé (porte + capot en PC, pas en verre — choix sécurité assumé par Anycubic) |
| Axe Z | 3 vis trapézoïdales reliées au moteur Z par courroie |
| Vitesse | **300 mm/s recommandé**, 600 mm/s max, accél. 20 000 mm/s² (Benchy en 13 min à 0,2 mm) |
| Buse | 0,4 mm de série, **quick-release** (hotend démontable à la main via un levier). 0,2 mm supporté depuis firmware V2.5.8.6 |
| Hauteur de couche | 0,05 – 0,28 mm (buse 0,4) |
| Temp. buse max | **320 °C** (gorge en tube composite céramique résistant 350 °C — ce n'est PAS du PTFE) |
| Temp. plateau max | **120 °C** |
| Plateau | PEI acier ressort (spring steel), 250×250 mm |
| Matériaux | PLA, PETG, ABS, ASA, PET, PA, PC, HIPS, TPU 95A (en mode mono uniquement), fibre carbone/verre (en mono, PAS via ACE Pro) |
| Nivellement | Automatique (jauge de contrainte / strain gauge) + préchauffe plateau +5 °C avant leveling (depuis FW V2.4.8.3) |
| Reprise après coupure | Oui + détection fin de filament |
| Caméra | Intégrée, 720p, AI détection (spaghetti + objets étrangers), timelapse, pas de vision nocturne (bandeau LED latéral) |
| Écran | Tactile, orientable, sur le dessus du caisson |
| Alimentation | 100–240 V (tension large), **puissance nominale 1500 W** |
| Conso réelle mesurée (review Notebookcheck) | ~800 W en pic à la chauffe, **~300 W en impression avec ACE Pro**, ~250 W sans |
| Bruit | ~44 dB annoncé |
| Connexion | Wi-Fi **2,4 GHz uniquement** (pas de 5 GHz, pas de bande mixte), USB, adaptateur USB→Ethernet supporté (FW ≥ V2.5.8.6) |
| Dimensions / poids machine | 400 × 410 × 490 mm, **18 kg** |
| Slicer | **Anycubic Slicer Next** (fork d'OrcaSlicer) ; OrcaSlicer peut envoyer des fichiers depuis FW V2.5.9.9 ; .gcode et .3mf supportés |
| Open source | **Non** (Anycubic dit que c'est « dans le plan », rien de concret — à prendre avec des pincettes) |
| Filtration | Ventilateur filtre arrière + **sachet de charbon actif** dans une trappe interne (voir maintenance) |

Ventilateurs (5 au total) : refroidissement pièce (tête), refroidissement hotend, ventilateur auxiliaire dans le caisson (crée une « couche d'air » sur la pièce), ventilateur filtre arrière, ventilateur carte mère (⚠️ celui-ci **tourne même au repos**, c'est voulu — sécurité).

Sources : [FAQ wiki](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/faq) · [Introduction aux composants](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/introduction) · [Page produit](https://store.anycubic.com/products/kobra-s1-combo) · [Review Notebookcheck](https://www.notebookcheck.net/A-splash-of-color-on-your-desk-Reviewing-the-Anycubic-Kobra-S1-Combo-Ace-Pro.1010199.0.html)

---

## 2. L'ACE Pro — comment ça marche, ce que ça fait, ce que ça ne fait PAS

L'ACE Pro (Anycubic Color Engine) est le boîtier 4 bobines posé au-dessus/à côté de la machine. Câblage : câble signal **6 pins côté ACE Pro, 4 pins côté imprimante** + alim séparée. Une icône de connexion apparaît sur l'écran quand c'est bon.

### Fonctionnement
- **4 slots**, chargement automatique : on pousse le filament dans la goulotte, on lâche dès qu'on sent une traction, l'ACE avale tout seul. ⚠️ **Une bobine à la fois** — attendre la fin du chargement avant d'insérer la suivante (l'ACE ne reconnaît que le premier filament inséré).
- Couper la pointe du filament et la **redresser** avant insertion (si plié/noué → couper la partie tordue).
- **RFID** : les bobines officielles Anycubic avec puce sont reconnues automatiquement (type + couleur + matière restante). Filament tiers : régler **type + couleur à la main** sur l'écran (icône 1 = couleur, icône 2 = type), sinon pas d'impression. Le slicer synchronise les consommables depuis la machine.
- **Déchargement** : sélectionner le slot → « Reject » → attendre la fin → tirer la bobine.
- **Buffer mechanism** (le mécanisme tampon à l'arrière, où arrivent les 4 tubes PTFE) : absorbe les variations de tension. Bruits légers pendant l'impression = normal jusqu'à un certain point, le wiki a une page dédiée.
- **Détection d'enchevêtrement/blocage** intégrée : si une bobine coince, la machine met en pause et reprend après intervention manuelle.

### Séchage de filament
- Séchage actif **jusqu'à 55 °C max**, y compris **pendant l'impression** (gros différenciateur vs Bambu AMS).
- Exemple officiel TPU : **50–55 °C pendant 4–6 h** avant impression.
- ⚠️ La température mesurée à la goulotte d'entrée paraît plus basse que la consigne : c'est normal, la valeur affichée est une moyenne multi-points (entrée d'air, sortie, NFC, goulotte) — l'entrée d'air est la référence.
- ⚠️ L'ACE Pro **première génération n'a PAS de capteur d'humidité** ni de stockage étanche (ça, c'est l'ACE 2 Pro, qui sèche à 65 °C et est supporté depuis FW V2.7.0.7). L'ACE Pro sèche, mais ne stocke pas au sec : bobines hygroscopiques (PA, TPU) → boîte de séchage à part.

### Limites et interdits (officiels, page « ACE Pro Tips »)
- **NE PAS passer dans l'ACE Pro** : filaments trop durs, cassants ou chargés fibre (**PLA-CF/GF, carbone, verre**, PLA Silk non-officiel) → usure des canaux internes, casse, bouchons.
- **TPU 95A et HIPS** : séchage OK dans l'ACE, mais **impression via l'ACE interdite** → utiliser le porte-bobine mono-couleur à l'arrière (le wiki a un guide TPU complet : débrancher le câble signal ACE, retirer le module de détection de retour, imprimer en direct).
- TPU < 95A (85A et moins) : pas imprimable du tout sur la S1 (écrasé par la roue d'extrusion).
- **Bobines** : privilégier le **plastique**, 195–200 mm de diamètre, 60–68 mm de large, flasques 3–6 mm. **Bobines carton = risque de glisse + débris** → imprimer la bague d'adaptation officielle (fichiers 3mf dans le wiki : « ACE Pro Anti-Tangle Model 1 & 2 »).

### Filament Backup (relais automatique de bobines)
Si 2 slots contiennent **même matière + même couleur**, et que l'option « **auto refill** » est cochée dans la gestion des consommables, la machine bascule automatiquement sur la bobine de secours quand la première est vide — idéal pour les grosses pièces. Conditions strictes : même type ET même couleur (différent type + même couleur = refusé) ; filament tiers → configurer les 2 slots identiquement à la main.

### Extension 8 couleurs
On peut chaîner **2 ACE Pro** pour 8 couleurs (supporté depuis FW V2.4.8.3) — guide : [Eight-color Module Installation](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/color-module).

### Couleurs qui bavent en multi-couleur
Si mélange de couleurs sur petites pièces avec changements fréquents : augmenter le **coefficient de purge (flushing)** depuis l'interface d'impression. Page wiki dédiée : [Reduce waste](https://wiki.anycubic.com/en/home/knowledge-sharing/reduce-waste).

Sources : [ACE Pro Tips](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-3-combo/ace-pro-notes) · [Chargement & config ACE Pro](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/ace-pro-loading-steps-and-configuration-information) · [Filament Backup](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/automatic-feeding-guide) · [Guide TPU](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/tpu-printing-guide) · [Specs ACE Pro](https://store.anycubic.com/products/anycubic-ace-pro)

---

## 3. Calibrations importantes

### Auto-leveling
Automatique via jauge de contrainte. Depuis FW V2.4.8.3, le plateau préchauffe (+5 °C au-dessus de la cible) avant le leveling pour stabiliser thermiquement → ne pas lancer un leveling plateau froid si on imprime chaud.

### Flow Calibration (= Pressure Advance automatique)
La S1 a un **capteur de pression dans la buse** : la « Flow Calibration » cochable avant chaque impression calibre automatiquement le pressure advance (consomme ~127 mm de filament, ~2 min).
- **Priorité** : valeur auto-calibrée > valeur PA manuelle > valeur par défaut.
- ⚠️ Piège officiel : **si la calibration échoue, AUCUN message** — la machine continue avec la valeur par défaut. Indice : une calibration ratée finit nettement plus vite que 2 min.
- Causes d'échec : pas de filament, buse bouchée, vis d'extrudeur desserrées, filament emmêlé. Causes d'imprécision : buse tierce, **filament humide**.
- À relancer quand : changement de marque/type de filament, de diamètre de buse, de température, de vitesse, d'accélération, ou après réparation de l'extrudeur.
- Activable depuis l'écran machine, le slicer (≥ 1.3.5.4) ou l'app.

### Compensation de vibrations (input shaping)
Pas cochée par défaut ; à lancer **uniquement après avoir déplacé la machine ou touché à la mécanique** (courroies, etc.). Le bruit fort pendant le scan de résonance est normal.

### Premier layer imparfait → calibration manuelle du plateau
Le wiki l'admet : le leveling auto ne rattrape pas tout. Procédure officielle si zones « fantômes » sur le 1er layer :
1. Imprimer le [gcode de test premier layer officiel](https://wiki.anycubic.com/kobra-s1/xy240_pla_0.2_57m4s.gcode) ;
2. Vérifier que le hotend quick-release est bien clipsé ;
3. Nettoyer le plateau (eau + détergent) ;
4. Préchauffer le plateau 5–10 min à la température d'impression ;
5. **Tourner la vis du coin défaillant sous le plateau d'1/4 de tour anti-horaire** (clé Allen S2.0) — les 4 vis si les 4 coins sont creux ;
6. Re-leveler et réimprimer. Affiner par 1/4 de tours.

Source : [Flow Calibration](https://wiki.anycubic.com/en/home/knowledge-sharing/pressure-advance) · [First layer](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1/first-layer) · [FAQ](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/faq)

---

## 4. Plan de maintenance officiel

### Imprimante ([page Maintenance](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/maintenance-recommendations), avec [vidéo YouTube](https://www.youtube.com/embed/K6tdYtwVDas))

| Quoi | Fréquence | Comment |
|---|---|---|
| **Vis Z (lead screws ×3)** | ~tous les **3 mois** ou si bruit anormal | Chiffon non pelucheux, puis Z à zéro → appliquer **de la GRAISSE** (pas d'huile : elle coule) sur toute la hauteur, plateau en haut puis en bas. NB : bruit métallique > 350 mm/s = normal. |
| **Tiges lisses Y (linear rods)** | Contrôle **mensuel** | Souffler la poussière (soufflette douce), chiffon, puis **un peu de graisse** répartie en bougeant l'axe à la main. |
| **Tiges lisses X** | Quand sales | Chiffon + alcool UNIQUEMENT. ⚠️ **JAMAIS de graisse sur l'axe X** : paliers graphène autolubrifiants. |
| **Cutter (lame de coupe filament)** | Après **3–5 bobines** imprimées | Démonter (Allen S2.0), inspecter l'usure, remplacer si usé. |
| **Hotend / buse** | Si sous-extrusion ou buse sale | Retirer la chaussette silicone, chauffer à 200 °C, essuyer (gants !) ; chauffer à 230 °C et passer l'aiguille. |
| **Chaussette silicone buse** | Inspection régulière | Remplacer si usée ou encroûtée de filament. |
| **Ventilateurs** (hotend, façade, auxiliaire) | Régulièrement | Soufflette / pinceau / coton-tige ; alcool isopropylique pour taches tenaces. Démontage si très encrassé. |
| **Plateau spring steel** | Régulièrement | Alcool ou détergent ; **ne pas toucher la surface avec les doigts** (traces grasses = défauts d'adhérence). |
| **Caméra** | Si image floue | Chiffon non pelucheux + alcool isopropylique. |
| **Sachet charbon actif** | Régénérer ~1×/mois (3–5 jours à l'air libre), remplacer après ~1 an max (2–3 mois en usage odeurs fortes) | Dans la trappe interne du caisson. Recharges en boutique officielle. |

### ACE Pro ([page maintenance ACE Pro](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-3-max/ace-pro-maintenance-recommendations))

⚠️ Toujours **éteindre et débrancher l'ACE Pro** avant maintenance.

| Quoi | Fréquence | Comment |
|---|---|---|
| **Tubes PTFE (Teflon)** | **Remplacer tous les 2 mois** en usage normal ; **contrôle mensuel** si filaments abrasifs | Retirer le clip bleu, presser la bague noire du raccord pneumatique, tirer le tube. Contrôler l'usure interne ET côté buffer mechanism. Tube usé non remplacé = bourrage garanti. |
| **Goulottes d'entrée (feed channel)** | Contrôle régulier | Usure sévère = bourrage. Pièce de rechange en boutique ; 2 vis Allen S2.5. Modèles anti-usure DIY imprimables fournis par le wiki ([modèle 1](https://wiki.anycubic.com/k3-max/ace+guide+v2.3mf), [modèle 2](https://wiki.anycubic.com/k3-max/filament+roller+guide+v2.3mf)). |
| **Carte de détection + LED** | Si la LED clignote au chargement | Poussière sur le capteur → chiffon propre ; nettoyer aussi le photo-interrupteur ; vérifier câbles PCBA et la palette de détection (pas pliée). |
| **Rouleaux porte-bobines** | Contrôle régulier | Doivent tourner librement ; si rouillé/grippé → **huile** sur les roulements (ici oui, de l'huile). Ne pas perdre les roulements latéraux au démontage. |
| **Buffer mechanism** | Si bruits anormaux / contrôle | Démonter le capot (S2.5) puis le mécanisme (S2.0), vérifier que les **ressorts** des 4 buffers rebondissent normalement. |

---

## 5. Pannes & erreurs fréquentes (fixes officiels)

### Codes d'erreur
La machine affiche un code + QR code à scanner. Index complet : **[wiki.anycubic.com/en/error-codes](https://wiki.anycubic.com/en/error-codes)** (chercher le code dans la barre de recherche du wiki, puis cliquer la variante « Kobra S1/S1 Combo »). Les plus parlants :

| Code | Signification | Piste |
|---|---|---|
| 10105 / 10106 / 10113 / 10115 / 10116 | Téléchargement/parsing fichier, mémoire pleine, MD5, fichier corrompu, slicing anormal | Réseau, stockage interne, re-slicer |
| 10107 | Filament cassé / fin de filament | Capteur de rupture (extrudeur) ou détection ACE Pro |
| 10118 / 10119 / 10120 | Échec homing X / Y / Z | Moteurs, câblage, mécanique |
| 10121 / 10123 | Plateau : chauffe anormale / NTC HS | Plateau + câblage |
| 10122 / 10124 | Hotend : chauffe anormale / NTC HS | Cartouche chauffante, **câble hotend mal inséré** (piège connu, voir ci-dessous) |
| 10126 / 10127 / 10128 | Compensation vibration X/Y anormale | Tension de courroie, accéléromètre |
| 11801 / 11812 | **Spaghetti détecté** (IA) | Confirmer arrêt / vérifier la pièce |
| 11802 | **Objet étranger détecté** sur le plateau (IA) | Nettoyer le plateau |

### Buse bouchée ([guide nettoyage](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/cleaning-hotend-clogging) + [troubleshooting complet](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/troubleshooting-abnormal-print-head-clogging))
Escalade officielle : 1) chauffer à 250 °C et extruder pour chasser le bouchon → 2) déposer le hotend quick-release (gants/pince !), pousser un bout de filament à la main dans la gorge, ou une clé Allen S1.5 longue → 3) aiguille dans la buse à 230 °C → 4) si rien ne marche, **remplacer le hotend quick-release** (pas cher, conçu pour). La buse 0,2 mm se bouche beaucoup plus facilement.
Diagnostic amont (si bouchons à répétition) : vérifier buffer mechanism (rebond des 4 buffers) → extrudeur (test E+ à 250 °C, le filament doit traverser le radiateur) → cutter (corps étranger) → gorge (chauffer 150 °C, pousser au filament avec pince) → buse.
⚠️ **2 pièges officiels au remontage** : hotend mal clipsé = la buse racle le plateau ; **câble hotend pas inséré à fond = hotend qui ne chauffe plus**.

### Bourrage dans l'ACE Pro ([guide](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1/ace-pro-blocking))
Réflexe n°1 : **redémarrer l'ACE Pro** (remet les engrenages à zéro, libère un jeu pour tirer le filament). Sinon : ouvrir le capot (S2.5), tourner l'engrenage à la main en tirant. Bourrage dans le buffer : démonter le buffer (clip bleu → tube → capot S2.5 → mécanisme S2.0). Bourrage profond : démontage de la coque ACE Pro (procédure complète dans le guide).

### Autres soucis documentés
- **Buse qui racle le plateau** : [page dédiée](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/nozzle-scraping-hot-bed) (souvent hotend mal clipsé).
- **Layer shift** : [page dédiée](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/layer-shift).
- **Câble de tête qui frotte le capot** (bruit) : repositionner le tube PTFE/le faisceau ; Anycubic fournit un rehausseur de capot imprimable sur Makeronline.
- **Qualité d'impression médiocre** : [page dédiée](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/printing-effect-is-not-good).
- **Caméra ne s'affiche pas** : très dépendant réseau → tester en partage de connexion 4G, puis en mode LAN via le slicer ; si LAN OK mais cloud KO → support officiel avec compte + code CN.
- **Export des logs** pour le SAV : [Fault Log Export Guide](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/fault-log-export).
- **AI detection** : c'est un service **cloud via l'app** (délai de détection normal ; nécessite caméra + réseau + compte app + fonction activée). Tailles mini détectées (sensibilité moyenne) : spaghetti ~3×3×3,8 cm au loin ; objet étranger ~9,5×9,5×3 cm au loin. Faux positifs possibles sur plateaux non-standard, plateau sale, PLA noir/gris. [Page AI Detection](https://wiki.anycubic.com/en/home/knowledge-sharing/ai-detection).

---

## 6. Firmware : mise à jour

Procédure officielle ([guide](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/firmware-update-guide)) :
1. **Binder l'imprimante à l'app Anycubic** (scan QR). ⚠️ **Impossible de mettre à jour en mode LAN** — désactiver le LAN mode d'abord. ([Guide de binding](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1/printer-binding-guide))
2. Écran → **Settings → Device → Printer information** : une flèche sous le n° de version = MAJ dispo → cliquer, OK, puis **redémarrer**.
3. **L'ACE Pro a son propre firmware** : Settings → Device → **ACE 1 Information** → même principe (×2 si deux ACE).

Versions marquantes (changelog complet sur la page) : V2.4.8.3 (skip de pièce ratée, flow calibration, 8 couleurs, préchauffe leveling) · V2.5.6.0 (détection objets étrangers, sensibilité IA réglable) · V2.5.8.6 (buse 0,2 mm, USB→Ethernet) · V2.5.9.9 (envoi depuis OrcaSlicer, 3mf, M73) · V2.7.0.7+ (support ACE 2/V2, purge multi-couleur améliorée, PLA Silk) · **V2.7.2.1 (dernière vue au 2026-06)** : stabilité pause/reprise, reconnaissance ACE améliorée, IA et reprise-coupure optimisées.

💡 Réflexe : garder firmware machine + ACE + slicer à jour, Anycubic corrige beaucoup par logiciel (le premier-layer notamment).

---

## 7. Liens wiki à garder sous la main

**Hub principal** : https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-Combo

| Sujet | URL |
|---|---|
| Quick Start Guide | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/quick-start-guide |
| Déballage (vidéo) | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-x1-combo/assembly |
| **Manuel PDF FR** | https://wiki.anycubic.com/kobra-s1/anycubic_kobra_s1_combo_user_manual-fr-v1.0.pdf |
| FAQ | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/faq |
| Maintenance machine | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/maintenance-recommendations |
| Maintenance ACE Pro | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-3-max/ace-pro-maintenance-recommendations |
| ACE Pro tips (limites filaments/bobines) | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-3-combo/ace-pro-notes |
| Chargement/config ACE Pro | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/ace-pro-loading-steps-and-configuration-information |
| Filament backup (relais bobines) | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/automatic-feeding-guide |
| Buse bouchée (nettoyage) | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/cleaning-hotend-clogging |
| Buse bouchée (diagnostic complet) | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/troubleshooting-abnormal-print-head-clogging |
| Bourrage ACE Pro | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1/ace-pro-blocking |
| Premier layer | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1/first-layer |
| Flow calibration / pressure advance | https://wiki.anycubic.com/en/home/knowledge-sharing/pressure-advance |
| AI détection | https://wiki.anycubic.com/en/home/knowledge-sharing/ai-detection |
| Firmware | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/firmware-update-guide |
| Réseau (2,4 GHz !) + dépannage | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/network-connection-guide-and-troubleshooting |
| Connexion LAN | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1/lan-connection-guide |
| Guide TPU | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/tpu-printing-guide |
| Module 8 couleurs (2× ACE) | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/color-module |
| Timelapse | https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/timelapse-photography |
| **Index codes d'erreur** | https://wiki.anycubic.com/en/error-codes |
| Slicer (Anycubic Slicer Next) | https://wiki.anycubic.com/en/software-and-app/new-page-anycubic-slicer-beta(orca-version) |
| Vidéos SAV officielles | https://anycubic.com/SupportCenter/unboxingVideo/44 |

Le wiki contient aussi ~40 guides de remplacement de pièces (hotend, extrudeur, cutter, ventilos, courroies XY, moteurs, plateau, caméra, carte mère, écran, et toutes les pièces ACE Pro) — tous listés sur le hub principal, section « Part Replacement ».

---

## 8. Points d'incertitude / à vérifier soi-même

- **Puissance** : 1500 W = nominal (FAQ wiki) ; les mesures indépendantes donnent ~300 W en croisière — les deux chiffres sont « vrais » mais ne mesurent pas la même chose.
- **Open source** : promesse vague d'Anycubic, rien de livré à ce jour.
- Les pages ACE Pro du wiki sont partagées entre Kobra 3 / Kobra S1 (même module) — certaines captures montrent la K3, les procédures restent valables.
- L'app/IA dépend du **cloud Anycubic** (serveur mqtt-universe.anycubic.com:8883) : pas de cloud = pas d'IA ni de MAJ firmware OTA ; le mode LAN existe mais coupe la MAJ firmware.
- Manuel FR en v1.0 alors que l'EN est en v1.3 — en cas de doute, croiser avec la version EN.
