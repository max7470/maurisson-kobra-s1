# -*- coding: utf-8 -*-
"""Le duel — Anycubic Kobra S1 Combo vs Elegoo Centauri Carbon 2 Combo. 10/06/2026."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, Image, PageBreak, HRFlowable)

BASE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(BASE, "photos")
OUT = os.path.join(BASE, "Duel-Kobra-S1-vs-Centauri-Carbon-2.pdf")

PAGE_W, PAGE_H = A4
M = 16 * mm

INK = colors.HexColor("#1a2332")
KOBRA = colors.HexColor("#b07a1e")      # or
KOBRA_L = colors.HexColor("#fdf3e0")
CC2 = colors.HexColor("#0f6f5c")        # vert
CC2_L = colors.HexColor("#e6f2ef")
NUL = colors.HexColor("#5b6470")
NUL_L = colors.HexColor("#eef0f3")
GREY = colors.HexColor("#5b6470")
LINE = colors.HexColor("#d7dce3")
ROW_ALT = colors.HexColor("#f4f6f8")
RED = colors.HexColor("#a33327")
RED_L = colors.HexColor("#fbeae7")

ss = getSampleStyleSheet()
def st(name, **kw):
    base = kw.pop("parent", ss["Normal"])
    return ParagraphStyle(name, parent=base, **kw)

S_TITLE = st("t", fontName="Helvetica-Bold", fontSize=22, leading=27, textColor=INK)
S_SUB   = st("sub", fontName="Helvetica", fontSize=11.5, leading=15, textColor=GREY)
S_H1    = st("h1", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=INK, spaceBefore=4*mm, spaceAfter=2.5*mm)
S_H2    = st("h2", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=INK, spaceBefore=2.8*mm, spaceAfter=1.4*mm)
S_BODY  = st("b", fontName="Helvetica", fontSize=9.2, leading=12.8, textColor=INK)
S_CELL  = st("c", fontName="Helvetica", fontSize=8.0, leading=10.4, textColor=INK)
S_CELL_B= st("cb", fontName="Helvetica-Bold", fontSize=8.0, leading=10.4, textColor=INK)
S_CELL_W= st("cw", fontName="Helvetica-Bold", fontSize=8.4, leading=10.8, textColor=colors.white)
S_WIN   = st("w", fontName="Helvetica-Bold", fontSize=7.6, leading=9.8, textColor=colors.white, alignment=TA_CENTER)
S_CAPT  = st("cp", fontName="Helvetica-Oblique", fontSize=7.6, leading=9.8, textColor=GREY, alignment=TA_CENTER)
S_SMALL = st("sm", fontName="Helvetica", fontSize=7.4, leading=9.6, textColor=GREY)

def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        half = PAGE_W / 2
        canvas.setFillColor(KOBRA); canvas.rect(0, PAGE_H - 8*mm, half, 8*mm, stroke=0, fill=1)
        canvas.setFillColor(CC2);   canvas.rect(half, PAGE_H - 8*mm, half, 8*mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 7.5)
        canvas.drawString(M, PAGE_H - 5.6*mm, "ANYCUBIC KOBRA S1 COMBO")
        canvas.drawRightString(PAGE_W - M, PAGE_H - 5.6*mm, "ELEGOO CENTAURI CARBON 2 COMBO")
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawCentredString(half, PAGE_H - 5.8*mm, "VS")
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 7)
    canvas.drawRightString(PAGE_W - M, 8*mm, f"Page {doc.page}")
    canvas.drawString(M, 8*mm, "Duel détaillé · 10 juin 2026 · sources : Notebookcheck (les 2 testées, même protocole), How-To Geek, Tom's Hardware, TechRadar, forums, wikis officiels")
    canvas.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=14*mm, bottomMargin=14*mm)
frame = Frame(M, 13*mm, PAGE_W - 2*M, PAGE_H - 28*mm, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=header_footer)])
E = []

def winner_chip(who):
    if who == "K":
        return Table([[Paragraph("KOBRA", S_WIN)]], colWidths=[16*mm], style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), KOBRA), ("TOPPADDING", (0,0), (-1,-1), 2.5), ("BOTTOMPADDING", (0,0), (-1,-1), 2.5)]))
    if who == "E":
        return Table([[Paragraph("ELEGOO", S_WIN)]], colWidths=[16*mm], style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), CC2), ("TOPPADDING", (0,0), (-1,-1), 2.5), ("BOTTOMPADDING", (0,0), (-1,-1), 2.5)]))
    return Table([[Paragraph("NUL", S_WIN)]], colWidths=[16*mm], style=TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NUL), ("TOPPADDING", (0,0), (-1,-1), 2.5), ("BOTTOMPADDING", (0,0), (-1,-1), 2.5)]))

# ================= PAGE 1 — COUVERTURE =================
E.append(Spacer(1, 4*mm))
E.append(Paragraph("Le duel final", S_TITLE))
E.append(Paragraph("Anycubic Kobra S1 Combo (429,99 €) vs Elegoo Centauri Carbon 2 Combo (429,95 €) — toutes deux fermées, multi-couleurs, livrées demain (Vlotty, commande avant 15h)", S_SUB))
E.append(Spacer(1, 3*mm))
E.append(HRFlowable(width="100%", thickness=1.2, color=INK))
E.append(Spacer(1, 4*mm))

w = (PAGE_W - 2*M - 6*mm) / 2
img_row = Table([[
    [Image(os.path.join(PHOTOS, "kobra-s1-1.jpg"), width=w, height=54*mm, kind="proportional"),
     Spacer(1, 1.5*mm), Paragraph("Kobra S1 Combo — ACE Pro à côté, sécheur intégré", S_CAPT)],
    [Image(os.path.join(PHOTOS, "cc2-1.jpg"), width=w, height=54*mm, kind="proportional"),
     Spacer(1, 1.5*mm), Paragraph("Centauri Carbon 2 Combo — CANVAS sur le capot, bobines latérales", S_CAPT)],
]], colWidths=[w + 3*mm, w + 3*mm])
img_row.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("ALIGN", (0,0), (-1,-1), "CENTER"),
                             ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 3*mm)]))
E.append(img_row)
E.append(Spacer(1, 4*mm))

E.append(Paragraph("Le verdict en 30 secondes", S_H2))
E.append(Paragraph(
    "C'est serré, et il faut être honnête : <b>à prix égal, la presse spécialisée penche pour l'Elegoo</b> (TechRadar a détrôné la "
    "Kobra S1 au profit de la CC2, How-To Geek lui a donné 9/10 Editor's Choice). Son système multi-couleurs est objectivement plus "
    "efficace : changements ~40 % plus rapides, purge mieux maîtrisée. <b>Mais pour TON profil précis, la Kobra S1 garde l'avantage</b> "
    "sur quatre points que la presse pondère peu : le séchage de filament intégré (déterminant en Belgique), un firmware libérable "
    "(Rinkhals : SSH, Mainsail, Home Assistant — la CC2 est verrouillée SANS alternative et impose un compte cloud), un an de maturité "
    "terrain (la CC2 a des bugs de jeunesse), et 15 minutes de montage contre 1 à 2 heures. Score sur 15 rounds : "
    "<b>Kobra 6 — Elegoo 5 — Nuls 4</b>. Détail rond par rond en page 2, analyse des 5 différences qui comptent en page 3.", S_BODY))
E.append(Spacer(1, 3*mm))
sc = Table([[
    Paragraph("<b>KOBRA S1 : 6 rounds</b><br/>Montage · Séchage · Extensibilité couleurs · Firmware/bidouille · Maturité · Indépendance cloud", S_CELL),
    Paragraph("<b>NULS : 4 rounds</b><br/>Prix · Livraison · Bruit · Slicer", S_CELL),
    Paragraph("<b>ELEGOO CC2 : 5 rounds</b><br/>Vitesse des swaps · Purge · Buse/matériaux · Pièces standard · Verdict presse", S_CELL),
]], colWidths=[(PAGE_W-2*M)*0.37, (PAGE_W-2*M)*0.26, (PAGE_W-2*M)*0.37])
sc.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,0), KOBRA_L), ("BACKGROUND", (1,0), (1,0), NUL_L), ("BACKGROUND", (2,0), (2,0), CC2_L),
    ("BOX", (0,0), (0,0), 0.8, KOBRA), ("BOX", (1,0), (1,0), 0.8, NUL), ("BOX", (2,0), (2,0), 0.8, CC2),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5)]))
E.append(sc)
E.append(PageBreak())

# ================= PAGE 2 — ROND PAR ROND =================
E.append(Paragraph("Rond par rond — 15 critères", S_H1))
rounds = [
    ("Prix bol.com", "429,99 € (-33 %)", "429,95 € (-2 %, prix officiel 439 €)", "N",
     "4 centimes d'écart. Égalité parfaite."),
    ("Livraison demain", "Vlotty, avant 15h", "Vlotty, avant 15h", "N", "Même vendeur, même promesse."),
    ("Montage initial", "Prémontée ~95 % : 10-20 min de débridage fléché, écran préinstallé", "CANVAS livré démonté : hub, 4 supports bobine, hotte thermique, flash firmware. 30 min à 2 h (42 étapes sur la version CC1), nappe écran fragile (scotch)", "K",
     "Premier contact sans appel : la Kobra imprime dans l'heure, l'Elegoo demande une vraie session de montage + calibration de 26 min."),
    ("Vitesse des changements de couleur", "~2 min par swap", "~1 min 10 par swap (Notebookcheck, même protocole)", "E",
     "~40 % plus rapide. Sur un print à 100 swaps : ~1 h 20 d'écart."),
    ("Purge / déchets", "Jusqu'à 17x le poids de la pièce en cas extrême ; contrôle de purge limité côté slicer (réglages sur la machine)", "5-15 % de filament en plus ; purge-to-infill natif dans ElegooSlicer (déchet recyclé dans le remplissage)", "E",
     "L'argument déchets le plus concret publié est chez Elegoo. Attention : sa goulotte d'éjection de purge peut se boucher (prints perdus documentés)."),
    ("Séchage du filament", "ACE Pro = sécheur actif 55 °C, même en cours d'impression", "Aucun. 4 bobines à l'air libre sur le flanc — LA critique design récurrente ; la communauté imprime des dryboxes", "K",
     "En Belgique, c'est un point lourd : le PLA/PETG humide = stringing, bulles, prints ratés. La Kobra intègre la solution, l'Elegoo a le problème."),
    ("Extensibilité couleurs", "4 de série, 8 possibles (2e ACE Pro 249 € + hub 8 voies)", "4, point final — pas de chaînage", "K",
     "Option chère mais elle existe."),
    ("Buse / matériaux", "320 °C, hotend PROPRIÉTAIRE (bloc complet 13-16 €), laiton de série ; ABS excellent (caisson)", "350 °C acier trempé DE SÉRIE, format standard Centauri, Microswiss FlowTech compatible, buse de rechange FOURNIE", "E",
     "30 °C de marge en plus, carbone-ready d'origine, écosystème de buses standard. Beau round Elegoo."),
    ("Pièces détachées", "Dispo UE (3DJake...) mais hotend propriétaire ; pas de buse de rechange dans le carton", "Dispo UE (3DJake, Elegoo France stock 24/48 h), buses standard moins chères, rechange incluse", "E",
     "Les deux sont bien servies en Europe, l'Elegoo est plus standard."),
    ("Firmware / bidouille", "Kobra OS (fork Klipper) verrouillé MAIS Rinkhals (mod communautaire mature) : SSH, Mainsail/Fluidd, OrcaSlicer direct, Home Assistant, OctoEverywhere", "Firmware propriétaire verrouillé SANS alternative : OpenCentauri ne couvre PAS la CC2 (officiel : « support not available at this time »)", "K",
     "Pour un bidouilleur self-hosted, c'est un gouffre : la Kobra se libère complètement, l'Elegoo est une boîte noire aujourd'hui."),
    ("Indépendance cloud", "Compte Anycubic NON obligatoire (USB/LAN sans compte) ; mode LAN 100 % local", "Compte Elegoo OBLIGATOIRE pour la connectivité réseau (binding machine-compte)", "K",
     "La CC1 était saluée pour son absence de cloud ; la CC2 a fait marche arrière."),
    ("Slicer", "Slicer Next (base Orca) : largement rattrapé en 2026 + profils S1 intégrés dans OrcaSlicer vanilla", "ElegooSlicer (base Orca) : très bon en multicouleur (purge-to-infill) mais connectivité Windows instable, et CC2 PAS encore dans OrcaSlicer vanilla (issue ouverte)", "N",
     "Deux forks d'Orca avec des défauts différents. Égalité avec nuances."),
    ("Fiabilité / recul terrain", "1 an de terrain : pannes connues, documentées, corrigées (firmware) ; loterie QC à réception ; bourrages ACE Pro = point faible identifié", "3 mois de recul : 91 % de réussite premier essai, 4,2/5 sur 628 avis Amazon, mais bugs de jeunesse actifs (goulotte purge, Error 1220, connectivité, app Matrix)", "K",
     "La Kobra a déjà mangé son pain noir ; l'Elegoo est encore en rodage logiciel. Round serré — la CC2 part bien, mais le recul manque."),
    ("Bruit", "44 dB(A) machine seule, ~55 dB sécheur ACE actif", "44-47 dB moyens, pics 54 dB, bip idle agaçant signalé", "N", "Kif-kif."),
    ("Verdict presse à prix égal", "« Good printer, bad slicer », fiabilité saluée — mais plus challengée", "9/10 Editor's Choice How-To Geek ; TechRadar a explicitement basculé S1 vers CC2 ; aucune source ne recommande la S1 plutôt que la CC2 à prix égal", "E",
     "À l'applaudimètre éditorial 2026, l'Elegoo gagne — en pondérant peu le séchage, le cloud et la bidouille."),
]
rows = [[Paragraph("<b>Round</b>", S_CELL_W), Paragraph("<b>Kobra S1 Combo</b>", S_CELL_W),
         Paragraph("<b>Centauri Carbon 2</b>", S_CELL_W), Paragraph("<b>Gagnant</b>", S_CELL_W)]]
notes = []
for i, (crit, k, e, who, note) in enumerate(rounds):
    rows.append([Paragraph(f"<b>{crit}</b>", S_CELL_B), Paragraph(k, S_CELL), Paragraph(e, S_CELL), winner_chip(who)])
tbl = Table(rows, colWidths=[30*mm, 62*mm, 62*mm, 24*mm], repeatRows=1)
sty = [
    ("BACKGROUND", (0,0), (-1,0), INK),
    ("VALIGN", (0,0), (-1,-1), "TOP"), ("ALIGN", (3,1), (3,-1), "CENTER"),
    ("GRID", (0,0), (-1,-1), 0.4, LINE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, ROW_ALT]),
    ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING", (0,0), (-1,-1), 3), ("BOTTOMPADDING", (0,0), (-1,-1), 3)]
tbl.setStyle(TableStyle(sty))
E.append(tbl)
E.append(Spacer(1, 2*mm))
E.append(Paragraph("Score final : Kobra S1 — 6 rounds · Centauri Carbon 2 — 5 rounds · 4 nuls. Un duel, un vrai.", S_CELL_B))
E.append(PageBreak())

# ================= PAGE 3 — LES 5 DIFFÉRENCES QUI COMPTENT =================
E.append(Paragraph("Les 5 différences qui compteront VRAIMENT au quotidien", S_H1))
diffs = [
    ("1. Le séchage — l'argument belge", KOBRA_L, KOBRA,
     "Tu vis en Belgique : 80 %+ d'humidité relative une bonne partie de l'année. Une bobine entamée laissée à l'air absorbe l'eau en "
     "quelques jours ; résultat : fils, bulles, surfaces granuleuses, adhérence en berne. L'ACE Pro de la Kobra sèche en continu à 55 °C "
     "pendant que tu imprimes — c'est un sécheur de 60-70 € intégré. Sur la CC2, les 4 bobines pendent à l'air libre sur le flanc, et "
     "c'est la critique design n°1 de la presse ET des utilisateurs (la communauté imprime déjà des caissons de fortune). Si tu prends "
     "l'Elegoo, ajoute mentalement un drybox au budget."),
    ("2. Le multi-couleurs — l'Elegoo fait mieux le métier que tu achètes", CC2_L, CC2,
     "Paradoxe assumé : sur la fonction multi-couleurs elle-même, la CC2 est meilleure. Swaps ~1 min 10 contre ~2 min, purge recyclable "
     "dans le remplissage (purge-to-infill), 91 % de réussite premier essai mesurée sur 34 jobs. Si ton usage principal est d'imprimer "
     "beaucoup d'objets multicolores, ce round pèse lourd : sur un print à 200 changements, la Kobra te coûte ~2 h 45 de plus. "
     "Contre-point : la goulotte d'éjection de purge de la CC2 se bouche parfois (prints perdus documentés — à surveiller manuellement)."),
    ("3. Firmware et cloud — la Kobra se libère, l'Elegoo t'enferme", KOBRA_L, KOBRA,
     "C'est LE point taillé pour ton profil. Kobra : compte facultatif, mode LAN 100 % local, et Rinkhals (mod mature, install USB "
     "réversible) t'ouvre SSH, Mainsail/Fluidd, l'envoi direct depuis OrcaSlicer, OctoEverywhere, et l'intégration Home Assistant via "
     "Moonraker. Elegoo CC2 : compte cloud OBLIGATOIRE pour le réseau, firmware verrouillé, et le projet communautaire OpenCentauri "
     "ne supporte pas la CC2 (confirmé par leur doc officielle). Avec ton infra self-hosted, tu sentirais la différence dès la semaine 2."),
    ("4. La buse — l'Elegoo est mieux née", CC2_L, CC2,
     "350 °C acier trempé de série (carbone-ready immédiatement, buse de rechange fournie), format standard avec écosystème tiers "
     "(Microswiss). La Kobra : 320 °C, laiton de série, hotend propriétaire à remplacer en bloc (13-16 €) et AUCUNE rechange dans le "
     "carton. Pour l'ABS les deux font très bien (caisson fermé) ; pour le PLA-CF/PETG-CF, l'Elegoo est prête d'origine, la Kobra "
     "demande ~16 € de hotend acier."),
    ("5. La maturité — un an de terrain, ça compte", KOBRA_L, KOBRA,
     "La Kobra S1 a 16 mois de production : ses défauts sont connus, documentés (wiki officiel fourni), corrigés par firmware, et la "
     "communauté a des réponses à tout. La CC2 a 3 mois : excellents débuts (4,2/5 sur 628 avis Amazon), mais Error 1220, connectivité "
     "slicer Windows capricieuse, app Matrix instable, estimations de temps fausses de +17 % — du rodage logiciel classique de v1, "
     "probablement corrigé d'ici 6 mois… que tu vivrais en attendant."),
]
for title, bg, border, body in diffs:
    t = Table([[Paragraph(f"<b>{title}</b><br/>{body}", S_CELL)]], colWidths=[PAGE_W - 2*M])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg), ("BOX", (0,0), (-1,-1), 0.8, border),
        ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5)]))
    E.append(t)
    E.append(Spacer(1, 2.2*mm))
E.append(PageBreak())

# ================= PAGE 4 — VERDICT =================
E.append(Paragraph("Verdict", S_H1))
E.append(Paragraph(
    "<b>Si tu devais être n'importe qui : l'Elegoo.</b> C'est le verdict de la presse à prix égal, et il est défendable — multi-couleurs "
    "plus efficace, buse mieux née, machine légèrement plus volumineuse (256³ vs 250³).", S_BODY))
E.append(Spacer(1, 2*mm))
E.append(Paragraph(
    "<b>Mais tu n'es pas n'importe qui, et pour TOI je maintiens la Kobra S1 Combo, d'une courte tête.</b> Trois raisons décisives "
    "à ton profil : <b>(1)</b> le séchage intégré — en Belgique c'est structurel, pas du confort, et c'est le seul point que l'Elegoo ne "
    "peut PAS rattraper sans accessoire ; <b>(2)</b> le firmware libérable + pas de compte obligatoire — avec ton écosystème self-hosted "
    "(Coolify, Home Assistant-style), une machine verrouillée au cloud te frustrera, et OpenCentauri ne couvre pas la CC2 ; <b>(3)</b> la "
    "maturité — la Kobra a fini son rodage, la CC2 est en plein dedans. En face, ce que tu concèdes est réel mais gérable : des swaps "
    "plus lents (tu ne feras pas du multicolore intensif tous les jours) et une purge moins fine (mitigeable : Flush Volume 0.4 + purge "
    "dans l'infill, dispo aussi côté Anycubic via OrcaSlicer).", S_BODY))
E.append(Spacer(1, 3*mm))
E.append(Paragraph("La question qui tranche tout", S_H2))
q = Table([[Paragraph(
    "<b>« Est-ce que le multi-couleurs sera mon usage PRINCIPAL, oui ou non ? »</b><br/><br/>"
    "<b>NON, c'est un bonus (ton cas probable, cf. ta question d'hier)</b> : prends la <b>Kobra S1 Combo</b>. Tu imprimeras à 90 % en "
    "mono-couleur avec des bobines toujours sèches, une machine mûre, et un firmware que tu peux t'approprier. Les défauts du multi-couleurs "
    "Anycubic ne te toucheront presque jamais.<br/><br/>"
    "<b>OUI, je veux produire du multicolore régulièrement</b> (figurines, objets déco à vendre, cadeaux en série) : prends la "
    "<b>Centauri Carbon 2 Combo</b> — et commande un drybox avec. Les 50 min gagnées par tranche de 50 swaps et la purge maîtrisée "
    "rembourseront ses défauts de jeunesse.", S_CELL)]], colWidths=[PAGE_W - 2*M])
q.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), NUL_L), ("BOX", (0,0), (-1,-1), 1, INK),
    ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6)]))
E.append(q)
E.append(Spacer(1, 3*mm))
E.append(Paragraph("Rappels pratiques (valables pour les deux)", S_H2))
E.append(Paragraph(
    "Commande avant <b>15h00 chez Vlotty</b> pour la livraison demain — vérifie que la promesse est toujours affichée au moment de payer. "
    "Vendeur marketplace (9,3/10) : retours 30 jours + garantie légale 2 ans via le vendeur, Service Clients bol en filet. Les deux machines "
    "purgent du filament en multi-couleurs : prévois 2-3 bobines de PLA en plus quel que soit ton choix. Et dans les deux cas, le TPU ne "
    "passe pas par le module multi-couleurs (alimentation directe).", S_BODY))
E.append(Spacer(1, 3*mm))
E.append(Paragraph(
    "<i>Méthodologie : duel construit sur 6 rapports de recherche (presse spécialisée — Notebookcheck ayant testé les deux machines avec "
    "le même protocole —, forums et communautés via index de recherche, wikis officiels Anycubic/Elegoo, GitHub Rinkhals/OpenCentauri, "
    "Trustpilot). La CC2 ayant 3 mois de vie commerciale, son recul utilisateur est structurellement plus faible que celui de la S1 — "
    "biais signalé partout où il joue.</i>", S_SMALL))

doc.build(E)
print("OK:", OUT)
