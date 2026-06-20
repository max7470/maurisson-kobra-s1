# Kobra S1 Combo — Conseils & pièges (retours forums, reviews long-terme)

> Compilé le 2026-06-10 à partir de reviews long-terme (Tom's Hardware, VoxelMatters, Creative Bloq, 3DWork, 3DWithUs, Maker Hacks), du wiki officiel Anycubic, de GitHub (Rinkhals, profils OrcaSlicer communautaires), de Printables/MakerWorld et de retours utilisateurs (blog Le Ngoc « 50+ hours », groupes FB Kobra S1). Les recherches Reddit directes étaient peu accessibles — la communauté la plus active est en réalité sur les **groupes Facebook « Kobra S1 Series »** et le **forum drucktipps3d.de** (germanophone), plus le wiki Anycubic qui est étonnamment complet.

**Verdict global de la communauté** : machine CoreXY fiable et rapide en mono-couleur (« set it and forget it » — Tom's Hardware après des centaines d'heures), mais le multi-couleur via ACE Pro est **lent** (~2 min par changement) et **très gaspilleur** par défaut, et le slicer Anycubic est le maillon faible. Le SAV Anycubic est unanimement salué (remplacements rapides, y compris machine complète chez Creative Bloq).

---

## ✅ À faire dès le déballage / le début

1. **Retirer les 6 vis de transport** marquées de flèches rouges/orange **AVANT** la première mise sous tension, couper les zip-ties de la tête et retirer le carton/mousse autour du lit. Oublier une vis = bruit horrible, voire casse moteur. C'est LE piège n°1 du déballage.
2. **Installer le filtre à charbon actif** dans son compartiment (fourni, souvent oublié dans le sachet d'accessoires).
3. **Mettre à jour le firmware immédiatement** — les premières versions avaient des faux positifs de détection spaghetti IA et des bugs ACE Pro corrigés depuis. ⚠️ La mise à jour OTA **ne fonctionne pas en mode LAN** : il faut d'abord désactiver le mode LAN et lier l'imprimante au cloud Anycubic, faire la MAJ, puis repasser en LAN si souhaité ([guide officiel](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/firmware-update-guide)).
4. **Laver la plaque PEI au savon + eau chaude** avant le premier print (le film de fabrication ruine l'adhérence), puis ne plus la toucher avec les doigts. Nettoyage régulier ensuite.
5. **Lancer l'auto-nivellement (LeviQ 3.0) lit CHAUD**, à la température d'impression, après 5-10 min de chauffe — le lit se dilate et change de géométrie. Niveler à froid = première couche ratée. Relancer le nivellement avant les prints importants : le Z n'a que 2 moteurs, il dérive.
6. **Wifi : 2,4 GHz uniquement.** Si le routeur n'expose que du 5 GHz, la connexion échoue. Éviter les caractères spéciaux dans le mot de passe wifi. Le **mode LAN** (Réglages → Réseau → LAN Mode, puis IP entrée à la main dans le slicer) est plus fiable que le cloud/app pour envoyer les prints ([troubleshooting officiel](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/network-connection-guide-and-troubleshooting)).
7. **Couper le bout plié du filament** à chaque chargement d'une bobine dans l'ACE Pro (l'extrémité écrasée/coudée est une cause classique de bourrage au hub).
8. **Bobines plastiques uniquement dans l'ACE Pro** — les bobines carton perdent des fibres et déchirent le bord, ça bloque la rotation et bourre le système. Pour une bobine carton : adaptateur imprimable ou porte-bobine externe arrière (fourni) pour le mono-couleur.
9. **Faire les premiers prints en mono-couleur** (fichiers de test SD) pour valider la mécanique avant de brancher la complexité ACE Pro.
10. **Calibrer flux + température par filament** (tours de température, test de flux) avant les gros prints — recommandé par 3DWork, la machine est rapide donc punit les profils approximatifs.

---

## ⚠️ Pièges connus

### ACE Pro / multi-couleur
- **Le gaspillage est énorme par défaut** : VoxelMatters a mesuré un Benchy 4 couleurs de 10,9 g qui a généré **183 g de purge** (17× le poids du modèle), et un print 1 h passé à **9 h** à cause des swaps. Un masque multicolore = 73 h chez 3DWithUs. → Réduire le flush (voir 🔧) et accepter que le multi-couleur est pour les pièces qui en valent la peine.
- **Chaque changement de couleur ≈ 2 minutes.** Multiplier mentalement avant de lancer.
- **Décharge/recharge inutile des 4 bobines au démarrage** de certains prints (comportement firmware signalé par Creative Bloq) — agaçant mais normal, amélioré par les MAJ.
- **Filaments interdits dans l'ACE Pro** : TPU souple (85A et moins = bourrage garanti), filaments chargés fibre (PLA-CF/GF — ça use les canaux internes), filaments cassants (PLA vieux/humide qui casse DANS les tubes), Silk fragiles. Le TPU s'imprime en direct via le porte-bobine arrière.
- **Le slicer Anycubic (Slicer Next) est le point faible** de l'écosystème : Tom's Hardware le démonte (n'affiche même pas le filament qui sera gaspillé avant de lancer). C'est un fork d'OrcaSlicer — OrcaSlicer vanilla marche, mais son profil S1 par défaut **n'a pas le G-code de changement de filament** : le copier depuis Slicer Next ou utiliser les [profils communautaires MPC561](https://github.com/MPC561/Anycubic-Kobra-S1-Orcaslicer-Profiles) (PETG, ABS, hauteurs de couche 0,08→0,24, start-code amélioré).
- **L'ACE Pro est bruyant quand le séchage chauffe** (ventilos PTC) — prévoir son emplacement en conséquence. Machine elle-même : ~46 dB standard / ~44 dB silencieux.

### Enceinte fermée + matières basse température
- **PLA : porte ouverte ou capot enlevé** sur les longs prints. Enceinte fermée + lit chaud = heat creep (le filament ramollit au-dessus de la zone de fusion → clic d'extrudeur, sous-extrusion, bouchon). Consigne officielle Anycubic : PETG lit ≥ ~70 °C → ouvrir porte et/ou capot ; TPU lit ≥ 45 °C → idem. Enceinte fermée = réservée ABS/ASA/PC.
- **ABS/ASA** : le filtre charbon aide mais ne fait pas tout — pièce ventilée.

### App / connectivité / caméra
- **L'app mobile Anycubic est jugée « boguée et capricieuse »** (Creative Bloq) ; la caméra devient parfois inaccessible → un simple redémarrage de la machine la récupère (3DWork). Ne pas compter sur l'app comme canal principal : mode LAN + slicer, ou Rinkhals (voir 🔧).
- **La détection spaghetti IA fait des faux positifs** qui mettent le print en pause (2 fausses alertes pendant les tests 3DWithUs). Les firmwares récents ont amélioré ça ; on peut la désactiver sur un print critique de nuit si elle se déclenche à tort.
- **Pas d'accès système / SSH en stock** — machine fermée façon Bambu. Pour bidouiller : Rinkhals.

### Mécanique / qualité
- **Capteur de fin de filament (runout) capricieux** : c'est la panne hardware documentée chez Creative Bloq (capteur qui ne détecte pas le filament inséré → erreurs en boucle). Si erreurs de détection persistantes dès le début → SAV direct, ils remplacent sans discuter.
- **Vitesse max 600 mm/s = marketing** ; la vitesse de croisière réelle et propre est ~300 mm/s. Ne pas pousser les profils au max pour gagner 10 min.
- **Première couche inégale selon les coins** : le lit se règle avec 4 vis sous le plateau (voir 🔧) — beaucoup de gens l'ignorent et se battent uniquement avec le z-offset.

---

## 🔧 Fixes des problèmes fréquents

### Bourrage / clog ACE Pro (CODE 11518 et autres)
- **Redémarrer l'ACE Pro** : à la relance, les engrenages reviennent en position zéro et libèrent un jeu qui permet de tirer le filament coincé.
- Si toujours bloqué : **clé Allen 2,5 → 2 vis du capot du mécanisme de buffer**, remettre les 4 buffers dans une position cohérente, refermer. Procédure officielle illustrée : [ACE Pro abnormal filament clogging](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1/ace-pro-blocking) et [CODE 11518](https://wiki.anycubic.com/en/error-codes/11518-code/s1).
- Cause fréquente : **filament trop fin / de mauvaise qualité** (les engrenages patinent) ou bout de filament coudé non coupé. Filament humide cassé dans le tube = démonter le capot et pousser/retirer le segment.
- Anycubic a une **série vidéo officielle de troubleshooting** ACE Pro & chemin filament : [YouTube — Guide Part 2](https://www.youtube.com/watch?v=e1LnZcfdUEs).

### Première couche ratée / adhérence
- Diagnostic par coin ([wiki first layer](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1/first-layer)) : couche ratée **dans un coin** → ce coin est trop loin de la buse → vis de ce coin **1/4 tour anti-horaire** (Allen 2,0). Ratée **aux 4 coins** → buse globalement trop haute → 4 vis 1/4 tour anti-horaire. Toujours re-niveler ensuite, lit chaud.
- PETG/TPU : **bâton de colle sur la plaque** — recommandation officielle, double rôle : adhérence ET couche sacrificielle qui protège le PEI (le PETG nu peut arracher le revêtement en refroidissant).
- Décollement en cours de print : 9 fois sur 10 c'est une plaque grasse → savon + eau, pas juste l'alcool.

### Extrusion irrégulière / clics
- Astuce communautaire (blog Le Ngoc, 50 h de tests) : **serrer à fond la vis droite de l'extrudeur puis la desserrer d'1,5 à 2 tours** pour retrouver une tension de pignon correcte.
- Clic + sous-extrusion en cours de long print PLA enceinte fermée = heat creep → ouvrir la porte, vérifier que le ventilateur du heatbreak n'est pas encrassé.
- Bouchon installé : apprendre le **cold pull**, ou profiter du **hotend quick-release** (levier sur le côté, changement en ~10 s sans outil) — c'est l'un des gros atouts de cette machine, en abuser plutôt que de gratter une buse en place.

### Purge multi-couleur excessive
- **Flush volume : passer le multiplicateur de 1.0 → ~0.4** : testé OK par la communauté ([vidéo « This printer poops too much »](https://www.youtube.com/watch?v=i5ce2Ow3F3M)). Garder plus haut pour les transitions critiques (noir → blanc).
- Activer **« flush into infill »** (purge dans le remplissage) et/ou purger dans des objets sacrificiels : réduit drastiquement la tour de purge sur les modèles à fort infill.
- Optimiser **l'ordre des couleurs** (du foncé vers le clair coûte plus cher en purge que l'inverse).

### Pour aller plus loin : firmware Rinkhals
- [Rinkhals](https://github.com/jbatonnet/Rinkhals) = firmware custom **non destructif** (garde toutes les fonctions stock) qui ajoute Klipper complet, Moonraker, **Mainsail/Fluidd**, et débloque l'accès réseau local propre (+ OctoEverywhere, SimplyPrint). Installeur avec interface sur l'écran tactile. C'est LE mod logiciel de référence de la communauté S1. À considérer une fois la machine maîtrisée en stock — pas le jour 1.

### Mods imprimables plébiscités (gratuits)
- **[PTFE Guide & Protection](https://www.printables.com/model/1233238-anycubic-kobra-s1-ptfe-guide-and-protection)** (entrée extrudeur) et **[ACE Pro Filament Saver & Alignment](https://www.printables.com/model/1140105-anycubic-ace-pro-filament-saver-alignment)** (par 3Dwork) : corrigent l'angle d'attaque du filament, réduisent l'usure et les frottements — les deux mods les plus recommandés.
- Anti-tangle / guides de bobine ACE Pro, **lid-stop** (maintient le capot entrouvert pour le PLA), relocalisation du capteur runout : collection [MakerWorld Kobra S1 Upgrades](https://makerworld.com/en/collections/6659265-anycubic-kobra-s1-upgrades).
- Possesseurs d'un **ancien ACE Pro** (Kobra 3) : [kit d'upgrade vers les guides version S1](https://www.printables.com/model/1237589-20-anycubic-ace-pro-upgrade-kit-to-new-s1-version).

### Maintenance périodique (wiki Anycubic + retours)
- **Tige filetée Z : lubrifier ~tous les 3 mois** ou dès qu'un bruit anormal apparaît (graisse, pas de WD-40).
- **Tiges/rails Y : inspection mensuelle**, propres et sans débris.
- Vider le bac à purge ACE Pro régulièrement, dépoussiérer les ventilos, vérifier la tension des courroies (capteur intégré côté machine).

---

## 🛒 Consommables et pièces à avoir en stock

| Pièce | Pourquoi | Note |
|---|---|---|
| **Buses 0,4 mm** (hotend quick-release Kobra S1, laiton) | Usure normale + bouchons ; le swap prend 10 s | Prendre le **hotend complet pré-assemblé** Anycubic, c'est le format prévu. 1-2 d'avance. Une **0,6 mm** en plus pour les gros prints rapides |
| **Manchons silicone de buse** | Consommable officiel, se déchire avec le temps | [Guide remplacement](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/nozzle-silicone-replacement-guide) |
| **Module wiper / brosse silicone de nettoyage buse** | Pièce d'usure désignée comme telle par Anycubic | Dispo boutique Anycubic / 3DJake |
| **Tube PTFE + coupleurs** | Le chemin ACE Pro→tête use le PTFE ; un tube ovalisé = frottements et bourrages | Quelques mètres de PTFE 1,75 mm de qualité (type Capricorn) |
| **Filtre à charbon actif** | À remplacer périodiquement (ABS/ASA surtout) | Boutique Anycubic |
| **Bâtons de colle** (PVP type Magigoo/UHU) | Obligatoire PETG/TPU pour protéger la plaque | Conso rapide |
| **Plaque PEI de rechange** | Le PEI finit toujours par s'user/s'arracher | Pas urgent jour 1, mais à prévoir |
| **Dessicant rechargeable + hygromètre** | L'ACE Pro sèche (45-55 °C) mais ne stocke pas hermétiquement parfaitement ; filament humide = cassures dans les tubes = pire panne ACE Pro | Sachets silica gel à recharger au four |
| **Clés Allen 2,0 et 2,5** | Fournies, mais ce sont les 2 tailles de toutes les interventions (vis de lit, capot buffer ACE) | Les garder près de la machine |

Sources pièces : [boutique officielle Kobra S1](https://store.anycubic.com/collections/accessories-for-kobra-s1-combo), [3DJake](https://www.3djake.com/spareparts/ersatzteile-fuer-anycubic-kobra-s1) (livre en Belgique), Amazon.

---

## Sources principales

- [Tom's Hardware — Anycubic Kobra S1 Review](https://www.tomshardware.com/3d-printing/anycubic-kobra-s1-review) (long-terme, critique du slicer)
- [VoxelMatters — review](https://www.voxelmatters.com/anycubic-kobra-s1-review-no-fuss-corexy-for-speed-and-reliability/) (mesures de gaspillage purge)
- [Creative Bloq — review](https://www.creativebloq.com/3d/anycubic-kobra-s1-combo-review-excellent-when-it-works-frustrating-when-it-doesnt) (capteur runout défectueux, app boguée, SAV)
- [3DWithUs — review, tests, tips & settings](https://3dwithus.com/anycubic-kobra-s1-combo-review-3d-printer-tests-tips-and-settings)
- [3DWork — review enclosed multicolor](https://3dwork.io/en/anycubic-kobra-s1-combo-review/) (bruit, caméra, mods)
- [Maker Hacks — review](https://www.makerhacks.com/anycubic-kobra-s1-combo-review/) · [The Gadgeteer — review](https://the-gadgeteer.com/2025/07/16/anycubic-kobra-s1-3d-printer-combo-review-punching-above-its-price-point/)
- [Blog Le Ngoc — Fixing Common Issues, 50+ hours](https://blog.lengoc.me/fixing-common-issues-with-the-kobra-s1-my-first-50-hours-experience/)
- Wiki officiel Anycubic : [hub Kobra S1 Combo](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo) · [first layer](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1/first-layer) · [clog ACE Pro](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1/ace-pro-blocking) · [maintenance](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/maintenance-recommendations) · [réseau](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/network-connection-guide-and-troubleshooting) · [compatibilité filaments](https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-max-combo/filament-compatibility-guide)
- GitHub : [Rinkhals](https://github.com/jbatonnet/Rinkhals) · [profils OrcaSlicer MPC561](https://github.com/MPC561/Anycubic-Kobra-S1-Orcaslicer-Profiles) · [issue G-code filament change OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer/issues/11632)
- Mods : [Printables PTFE Guide](https://www.printables.com/model/1233238-anycubic-kobra-s1-ptfe-guide-and-protection) · [Filament Saver 3Dwork](https://www.printables.com/model/1140105-anycubic-ace-pro-filament-saver-alignment) · [collection MakerWorld](https://makerworld.com/en/collections/6659265-anycubic-kobra-s1-upgrades) · [forum drucktipps3d](https://forum.drucktipps3d.de/forum/thread/42708-n%C3%BCtzliche-modifikationen-f%C3%BCr-den-kobra-s1-combo/)
- Vidéo flush : [Optimizing flush amounts on the Kobra S1](https://www.youtube.com/watch?v=i5ce2Ow3F3M) · [Troubleshooting officiel ACE Pro](https://www.youtube.com/watch?v=e1LnZcfdUEs)

> **Incertitudes** : les retours Reddit bruts étaient peu indexables (communauté surtout sur Facebook « Kobra S1 Series ») ; les valeurs de flush (0.4) et le réglage de vis d'extrudeur (1,5-2 tours) sont des recettes communautaires, pas des specs officielles — à valider sur ta machine. Le firmware évolue vite : certains défauts cités (faux positifs IA, recharge inutile des bobines) ont pu être corrigés depuis les reviews (début-mi 2025).
