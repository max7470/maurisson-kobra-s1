# 03 — Mods, firmware & upgrades — Anycubic Kobra S1 Combo

> Recherche : 2026-06-10. Sources croisées : GitHub Rinkhals (jbatonnet + rinkhals-community), doc officielle Rinkhals, MakerWorld, Printables, wiki Anycubic, forums (drucktipps3d, Reddit, OrcaSlicer discussions).

---

## 1. Rinkhals — LE firmware custom de la Kobra S1

### C'est quoi

[Rinkhals](https://github.com/jbatonnet/Rinkhals) (créé par **Jbatonnet**) n'est **pas un remplacement** du firmware Anycubic : c'est un **overlay** qui s'installe par-dessus le firmware stock (Kobra OS, basé sur une version fermée de Klipper appelée « gklib/GoKlipper »). Tu gardes **tout le stock** (écran tactile, calibrations, outils Anycubic, ACE Pro) et tu gagnes :

- **Mainsail + Fluidd** (interfaces web Klipper classiques) via **Moonraker** → contrôle complet depuis le navigateur, sur ton LAN, **sans cloud Anycubic**
- **Caméra intégrée de la S1 visible dans Mainsail/Fluidd** (flux webcam) + support caméra USB
- **Accès SSH** à la machine (c'est un Linux embarqué)
- **Système d'apps** : OctoEverywhere (accès distant + détection d'échec IA + notifs), **OctoApp** (app mobile), Tailscale, Cloudflare Tunnel, Spoolman (gestion bobines), SimplyPrint…
- **Mises à jour OTA** de Rinkhals depuis l'interface
- Envoi de prints depuis **OrcaSlicer en réseau local** (voir §3)

⚠️ **Gouvernance (important, juin 2026)** : le projet a changé de mains. Depuis avril 2026, le repo actif est **[rinkhals-community/Rinkhals](https://github.com/rinkhals-community/Rinkhals/)** (mainteneur : Martin Bogomolni), avec un cycle de release **mensuel**. Le repo `jbatonnet/Rinkhals` reste la référence historique/doc, mais télécharge les builds récents chez **rinkhals-community**. La première installation depuis le nouveau repo doit se faire manuellement en `.swu` ; ensuite les updates OTA repointent dessus.

### Compatibilité firmware (critique)

Rinkhals ne marche **que sur des versions précises** du firmware Anycubic, car il s'injecte dans l'UI stock :

| Firmware Anycubic Kobra S1 | Rinkhals |
|---|---|
| 2.6.0.0 / 2.7.0.7 / 2.7.0.9 | ✅ supporté (releases 2025–début 2026) |
| 2.7.2.1 | ✅ supporté (release 20260601_01, juin 2026) |
| 2.7.2.7 | ✅ hotfix dédié (release **20260606_02**, 7 juin 2026) |
| Toute version plus récente | ❓ vérifier les release notes AVANT d'updater |

**Règle d'or : ne JAMAIS accepter une mise à jour officielle Anycubic sans vérifier qu'une release Rinkhals la supporte.** Une MAJ Anycubic casse quasi systématiquement Rinkhals jusqu'à ce que l'équipe sorte un correctif ([issue #222](https://github.com/jbatonnet/Rinkhals/issues/222)). Procédure propre : MAJ officielle d'abord → réinstaller la version Rinkhals compatible ensuite.

### Compatibilité ACE Pro

**Oui, l'ACE Pro fonctionne avec Rinkhals**, y compris le multi-couleur. Détails :
- En multicolor depuis Orca, le slicer génère un fichier `.acm` à côté du gcode ; gklib le détecte et initialise l'ACE Pro.
- Les releases 2026 ont ajouté : sync du statut MMU, fix de la sélection de slot auto-feed pour les prints mono-couleur, **contrôle du flush ACE** (réduction du gaspillage de purge), intégration Happy Hare, fix des IDs en dual ACE Pro.
- Piège connu (hérité Kobra 3, à connaître) : imprimer **sans** ACE branché via Moonraker peut donner l'erreur 11503 « filament hub not exist » ([issue #433](https://github.com/jbatonnet/Rinkhals/issues/433)). Sur le Combo tu laisses l'ACE branché, donc peu concerné.

### Installation (résumé — doc complète : [jbatonnet.github.io/Rinkhals](https://jbatonnet.github.io/Rinkhals/))

1. Vérifier la version firmware de la S1 (Réglages → À propos) et qu'elle est dans la liste supportée.
2. Clé USB **FAT32, table de partition MBR** (GPT = échec silencieux).
3. Créer un dossier nommé exactement **`aGVscF9zb3Nf`** à la racine.
4. Y placer le fichier de la release renommé **`update.swu`**.
5. Brancher la clé, printer allumé → bip de détection → barre de progression (~20 s) → **barre verte + 2 bips = OK** ; barre rouge + 3 bips = échec (mauvaise version firmware, en général).
6. Une icône Rinkhals apparaît dans les réglages de l'écran tactile.

### Désinstallation propre

C'est un overlay, donc réversible facilement — gros avantage vs un vrai flash :
- **Désactiver** : via l'UI tactile Rinkhals, ou créer un fichier `.disable-rinkhals` (via SSH/USB) → reboot → la machine redémarre 100 % stock.
- **Supprimer complètement** : effacer ensuite le dossier `/useremain/rinkhals`.
- En cas de boot foireux : page [Boot Issues Recovery](https://jbatonnet.github.io/Rinkhals/printers/recover-boot-issues/) de la doc + les firmwares stock re-flashables sont mirrorés dans le repo.

### Risques & garantie — l'avis honnête

- **Brick** : risque réel mais **faible** vu l'architecture overlay + procédure de recovery documentée. Le dev annonce la couleur : « I'm not responsible if you brick your printer ». Les vrais bricks rapportés viennent surtout de bidouilles SSH dans la config Klipper, pas de l'install standard.
- **Garantie** : Anycubic peut refuser le support si Rinkhals est détecté. **MAIS** : (1) c'est désinstallable proprement avant un retour SAV, (2) en **droit européen** (directive 2019/771, applicable en Belgique), un vendeur ne peut refuser la garantie légale de 2 ans que s'il prouve que le défaut vient de la modification — un firmware overlay n'a aucun lien avec une panne mécanique. En pratique : désactive/retire Rinkhals avant tout contact SAV et n'en parle pas.
- **Stabilité** : chaque app/client web connecté ralentit la machine (CPU embarqué modeste) et peut crasher l'UI — la doc le dit explicitement. Installer Mainsail + caméra + OctoEverywhere + Spoolman + 3 onglets ouverts = mauvaise idée. Rester minimaliste.
- **Modifs Klipper directes** (printer.cfg via SSH) : non supportées, c'est là que les gens cassent des trucs. À éviter au début.

**Verdict** : sur la S1 c'est LE mod n°1, mature (releases mensuelles, communauté active), réversible. À faire une fois la machine apprivoisée en stock 2-3 semaines, pas le jour 1.

Sources : [repo jbatonnet](https://github.com/jbatonnet/Rinkhals) · [repo communautaire + releases](https://github.com/rinkhals-community/Rinkhals/releases) · [doc officielle](https://jbatonnet.github.io/Rinkhals/) · [guide OctoEverywhere](https://blog.octoeverywhere.com/how-to-install-klipper-on-your-anycubic-3d-printer/) · [issue MAJ Anycubic vs Rinkhals](https://github.com/jbatonnet/Rinkhals/issues/222)

---

## 2. Sortir du cloud Anycubic

Trois niveaux, du plus simple au plus complet :

1. **Mode LAN officiel Anycubic** (sans rien modder) : la S1 a un mode LAN qui cause **uniquement avec Anycubic Slicer Next** (envoi de prints, suivi, vidéo) en local, sans cloud. Limite : tu es enfermé dans le slicer Anycubic. [Guide réseau wiki Anycubic](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/network-connection-guide-and-troubleshooting).
2. **Rinkhals** : Moonraker expose l'API standard → Mainsail/Fluidd dans le navigateur, OrcaSlicer en direct, zéro dépendance cloud. C'est la vraie libération.
3. **Accès distant sans cloud** : via les apps Rinkhals — **Tailscale** (VPN mesh, le plus propre), Cloudflare Tunnel, ou OctoEverywhere (pratique mais c'est re-déléguer à un cloud tiers).

## 3. OrcaSlicer en réseau

- **Sans Rinkhals : impossible.** Orca ne sait pas parler au protocole LAN propriétaire de la S1 ([discussion OrcaSlicer #8568](https://github.com/OrcaSlicer/OrcaSlicer/discussions/8568)). Tu slices dans Orca → export gcode → clé USB ou re-import, pénible.
- **Avec Rinkhals :** tu déclares la S1 comme imprimante « Klipper/Moonraker » dans Orca (IP de la machine) → envoi direct, suivi, et le print lancé depuis Orca s'affiche normalement sur l'écran tactile. Guide officiel : [Orca slicer usage](https://jbatonnet.github.io/Rinkhals/guides/orca-slicer-usage/). Le multicolor ACE marche (fichier `.acm` auto).

## 4. Home Assistant

Deux voies :
- **Via Rinkhals (recommandé)** : Moonraker tourne sur la S1 → l'intégration HA **Moonraker** (HACS) remonte état, températures, progression, caméra, et permet pause/stop. C'est l'intégration Klipper standard, très mature. Quelques frictions historiques rapportées sur Kobra (socket gklib non standard, [issue #225](https://github.com/jbatonnet/Rinkhals/issues/225)), largement améliorées dans les releases 2026 (« Moonraker host control resilience »).
- **Sans Rinkhals** : composant HACS [Anycubic Cloud](https://community.home-assistant.io/t/anycubic-cloud-component-frontend-card/742295) (état + carte frontend) — mais ça passe par le cloud Anycubic, dépendant de leur API, support S1 à vérifier au cas par cas. ⚠️ Moins fiable, à considérer comme un dépannage.

---

## 5. Mods imprimables spécifiques S1 / ACE Pro (les populaires qui servent vraiment)

Collection de référence : [Anycubic Kobra S1 Upgrades sur MakerWorld](https://makerworld.com/en/collections/6659265-anycubic-kobra-s1-upgrades) + [collection S1 générale](https://makerworld.com/en/collections/6061654-anycubic-kobra-s1).

### ACE Pro (le poste n°1 des galères → des mods)

| Mod | Pourquoi | Lien |
|---|---|---|
| **ACE Pro Filament Saver & Alignment** (3Dwork.io) | LE mod ACE le plus connu. Guide de bobine + butée anti-mouvement → réduit les fausses alertes « filament feed » et les bourrages, surtout bobines carton ou presque vides | [Printables](https://www.printables.com/model/1140105-anycubic-ace-pro-filament-saver-alignment) · [MakerWorld](https://makerworld.com/en/models/967734-anycubic-ace-pro-filament-saver-alignment) |
| **ACE Pro Filament Guide (sans vis)** | Même but, se colle au double-face dans le couvercle — pour les ACE sans trous de vis | [MakerWorld](https://makerworld.com/en/models/1627161-anycubic-ace-pro-filament-guide-no-screws) |
| **Boîte à silica gel + hygromètre** | Le dessiccant en sachets libres dans l'ACE, c'est nul. Boîte dédiée + emplacement capteur temp/humidité → tu SAIS si tes bobines sont au sec | [MakerWorld silica box](https://makerworld.com/en/models/1222801-anycubic-kobra-s1-combo-ace-pro-silica-gel-box) · [Printables holder + capteur](https://www.printables.com/model/1317868-anycubic-kobra-s1-ace-pro-humidity-sensor-silica-g) · [support hygromètre visible](https://makerworld.com/en/models/1234091-hygrometer-display-stand-anycubic-kobra-s1-ace-pro) |
| **Plateau de séchage du dessiccant** | Pour régénérer le silica au four proprement | [MakerWorld](https://makerworld.com/en/models/1434976-anycubic-ace-pro-desiccant-drying-tray) |

### Chemin filament / PTFE

| Mod | Pourquoi | Lien |
|---|---|---|
| **PTFE Guide and Protection** | Améliore l'angle d'entrée du filament dans l'extrudeur + protège le PTFE du frottement contre le capot. Sans supports. Quasi indispensable | [MakerWorld](https://makerworld.com/en/models/1220595-anycubic-kobra-s1-ptfe-guide-and-protection) |
| **Hub 5-vers-1** (zpin) | Remplace le hub 4→1 stock : ajoute un **5ᵉ port pour une bobine manuelle** → tu peux imprimer **TPU et filaments exotiques que l'ACE Pro ne digère pas** sans rien débrancher. Mod malin n°1 du Combo | [Printables](https://www.printables.com/model/1291687-5-to-1-filament-hub-for-anycubic-kobra-s1-combo) · [Thingiverse](https://www.thingiverse.com/thing:7037079) |
| **Side spool holder** (porte-bobine latéral) | Bobine externe en direct (TPU notamment — **le TPU ne passe PAS par l'ACE Pro**, limitation officielle) avec déroulement fluide | [MakerWorld](https://makerworld.com/en/models/1330385-side-spool-holder-anycubic-kobra-s1) · [version avec riser](https://makerworld.com/en/models/2152469-anycubic-kobra-s1-side-spool-holder-with-riser) |
| **Improved Spool Holder** | Le porte-bobine arrière stock déroule mal ; celui-ci ajoute une vraie rotation fluide | [Printables](https://www.printables.com/model/1336673-improved-spool-holder-for-anycubic-kobra-s1-3d-pri) |

### Châssis / confort

| Mod | Pourquoi | Lien |
|---|---|---|
| **Pieds anti-vibration** (MisterTLX) | Moins de bruit transmis au meuble, meilleure stabilité, flux d'air sous la machine | [Printables](https://www.printables.com/model/1217694-anycubic-kobra-s1-anti-vibration-foot-pads) · [Thingiverse](https://www.thingiverse.com/thing:6964845) |
| **Pieds HULA v1.0** (Gwebster) | Variante « HULA » (découplage vibratoire inspiré Voron) — gros gain bruit | [Printables](https://www.printables.com/model/1425160-anycubic-kobra-s1-s1c-hula-v10-anti-vibration-feet/related) |
| **Riser** (rehausse) | Surélève la S1 (~15 cm) : tiroirs de rangement, support de plaques de build, meilleur accès. ⚠️ Gourmand : ~2 kg de filament | [Cults3D](https://cults3d.com/en/3d-model/tool/anycubic-kobra-s1-riser) · [riser D3P](https://cults3d.com/en/3d-model/tool/anycubic-kobra-s1-d3p-riser) |
| **Poignées / handle upgrade** | La S1 fait ~24 kg avec l'ACE dessus, zéro prise stock — poignées imprimées pour la déplacer sans se casser le dos | dans la [collection Upgrades MakerWorld](https://makerworld.com/en/collections/6659265-anycubic-kobra-s1-upgrades) |
| **Bracket capteur temp/humidité de chambre** | Monitorer la température de chambre (utile ABS/ASA, machine fermée) | [MakerWorld](https://makerworld.com/en/models/1395349-kobra-s1-chamber-temp-humidity-sensor-bracket) |

Fil de discussion utile (DE, traduisible) qui agrège les mods testés du Combo : [drucktipps3d — Nützliche Modifikationen für den Kobra S1 Combo](https://forum.drucktipps3d.de/forum/thread/42708-n%C3%BCtzliche-modifikationen-f%C3%BCr-den-kobra-s1-combo/).

---

## 6. Upgrades : ce qui vaut le coup vs gadgets

### ✅ Vaut le coup (ordre de priorité)

1. **Rinkhals** — gratuit, réversible, transforme la machine (Orca réseau + caméra + HA + plus de cloud). Le meilleur ratio bénéfice/risque de toute cette page.
2. **Mods anti-galère ACE Pro** (filament saver + guide PTFE) — 2 h d'impression, élimine les pannes les plus fréquentes du Combo rapportées par la communauté.
3. **Gestion dessiccant + hygromètre** (~10 € de capteur + un print) — le PETG/PA humide est la cause n°1 de prints moches ; l'ACE Pro sèche, mais sans mesure tu pilotes à l'aveugle.
4. **Hub 5-to-1 ou side spool + bypass** — dès que tu veux du TPU (l'ACE Pro ne le gère pas), c'est obligatoire de toute façon.
5. **Pieds anti-vibration** — si la machine est sur un meuble qui résonne. Gratuit (chutes de TPU).
6. **Buses de rechange officielles** (0.4 spare + une 0.6 pour les gros prints/filaments chargés) — consommable, pas vraiment un « upgrade », mais à avoir d'avance.

### ❌ Gadgets / à éviter

- **Riser à tiroirs** : joli sur Insta, ~2 kg de filament (~40 €) et des jours d'impression pour… des tiroirs. Surélever la machine peut aussi amplifier le wobble si le meuble n'est pas rigide. À faire seulement si tu manques vraiment de rangement.
- **Modifs Klipper profondes via SSH** (accélérations, input shaping custom…) : la S1 tourne sur un Klipper fermé (gklib) déjà tuné usine ; bidouiller = source n°1 de casse signalée sur le repo, gain marginal.
- **Caméras USB additionnelles** alors que la caméra intégrée suffit pour du monitoring — charge CPU en plus, crashs UI possibles.
- **Upgrades mécaniques** (rails, extrudeur tiers…) : inutiles, la S1 est une CoreXY récente et fermée — rien de prouvé côté communauté à ce jour, et là tu flingues vraiment la garantie.

---

## 7. Check-list de mise en œuvre proposée

1. [ ] Machine en stock 2-3 semaines, noter la version firmware exacte.
2. [ ] Imprimer en stock : filament saver ACE + guide PTFE + boîte silica/hygromètre + pieds.
3. [ ] Vérifier sur [rinkhals-community/releases](https://github.com/rinkhals-community/Rinkhals/releases) que la version firmware est supportée → installer Rinkhals (clé USB FAT32/MBR, dossier `aGVscF9zb3Nf`, `update.swu`).
4. [ ] Configurer Orca → imprimante Moonraker (IP locale) ; tester un print mono puis multicolor ACE.
5. [ ] Brancher HA via l'intégration Moonraker. Optionnel : Tailscale pour l'accès distant.
6. [ ] **Désactiver les MAJ auto Anycubic** / ne jamais updater sans vérifier la compat Rinkhals.
7. [ ] Plus tard, si TPU : hub 5-to-1 + side spool.

---

### Incertitudes / points à surveiller

- Les **versions firmware supportées évoluent chaque mois** — ce doc est daté du 10/06/2026, toujours re-vérifier les release notes rinkhals-community avant d'agir.
- La position officielle d'Anycubic sur la **garantie avec Rinkhals n'est documentée nulle part** publiquement ; le raisonnement « droit EU + désinstallation avant SAV » est pragmatique, pas une certitude juridique.
- Le **support S1 dans le composant HA Anycubic Cloud** (sans Rinkhals) n'est pas confirmé explicitement — testé surtout sur Kobra 3.
- Stats de fiabilité des mods : basées sur retours communautaires (likes/makes, forums), pas sur des tests contrôlés.
