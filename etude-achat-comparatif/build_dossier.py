# -*- coding: utf-8 -*-
"""Dossier comparatif imprimantes 3D fermées multi-couleurs — bol.com BE, 10/06/2026."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable)

BASE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(BASE, "photos")
OUT = os.path.join(BASE, "Dossier-comparatif-imprimantes-3D-multicouleurs.pdf")

PAGE_W, PAGE_H = A4
M = 16 * mm

# Palette
INK = colors.HexColor("#1a2332")
ACCENT = colors.HexColor("#0f6f5c")
ACCENT_LIGHT = colors.HexColor("#e6f2ef")
GOLD = colors.HexColor("#b07a1e")
GOLD_LIGHT = colors.HexColor("#fdf3e0")
RED = colors.HexColor("#a33327")
RED_LIGHT = colors.HexColor("#fbeae7")
GREY = colors.HexColor("#5b6470")
LINE = colors.HexColor("#d7dce3")
ROW_ALT = colors.HexColor("#f4f6f8")

ss = getSampleStyleSheet()
def st(name, **kw):
    base = kw.pop("parent", ss["Normal"])
    return ParagraphStyle(name, parent=base, **kw)

S_TITLE   = st("t",  fontName="Helvetica-Bold", fontSize=26, leading=31, textColor=INK)
S_SUB     = st("sub", fontName="Helvetica", fontSize=12.5, leading=17, textColor=GREY)
S_H1      = st("h1", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=INK, spaceAfter=3*mm)
S_H2      = st("h2", fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=ACCENT, spaceBefore=2.5*mm, spaceAfter=1.5*mm)
S_BODY    = st("b",  fontName="Helvetica", fontSize=9.3, leading=13, textColor=INK)
S_BODY_S  = st("bs", fontName="Helvetica", fontSize=8.4, leading=11.4, textColor=INK)
S_CELL    = st("c",  fontName="Helvetica", fontSize=8.2, leading=10.6, textColor=INK)
S_CELL_B  = st("cb", fontName="Helvetica-Bold", fontSize=8.2, leading=10.6, textColor=INK)
S_CELL_W  = st("cw", fontName="Helvetica-Bold", fontSize=8.4, leading=10.8, textColor=colors.white)
S_SMALL   = st("sm", fontName="Helvetica", fontSize=7.4, leading=9.6, textColor=GREY)
S_BADGE   = st("bd", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=colors.white)
S_PRICE   = st("pr", fontName="Helvetica-Bold", fontSize=20, leading=23, textColor=ACCENT)
S_CAPT    = st("cp", fontName="Helvetica-Oblique", fontSize=7.6, leading=9.8, textColor=GREY, alignment=TA_CENTER)

def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFillColor(ACCENT)
        canvas.rect(0, PAGE_H - 8*mm, PAGE_W, 8*mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 7.5)
        canvas.drawString(M, PAGE_H - 5.6*mm, "DOSSIER COMPARATIF — IMPRIMANTES 3D FERMÉES MULTI-COULEURS")
        canvas.drawRightString(PAGE_W - M, PAGE_H - 5.6*mm, "bol.com BE · 10 juin 2026")
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 7)
    canvas.drawRightString(PAGE_W - M, 8*mm, f"Page {doc.page}")
    canvas.drawString(M, 8*mm, "Sources : bol.com, sites constructeurs, Tom's Hardware, How-To Geek, TechRadar, 3DWithUs, Notebookcheck, 3DTechValley")
    canvas.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=14*mm, bottomMargin=14*mm)
frame = Frame(M, 13*mm, PAGE_W - 2*M, PAGE_H - 28*mm, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=header_footer)])

E = []  # story

def badge_table(text, color):
    t = Table([[Paragraph(text, S_BADGE)]], colWidths=[None])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), color),
        ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    return t

def photo_row(img1, img2, cap1, cap2, h=62*mm):
    w = (PAGE_W - 2*M - 6*mm) / 2
    def cell(img, cap):
        i = Image(os.path.join(PHOTOS, img), width=w, height=h, kind="proportional")
        return [i, Spacer(1, 1.5*mm), Paragraph(cap, S_CAPT)]
    t = Table([[cell(img1, cap1), cell(img2, cap2)]], colWidths=[w + 3*mm, w + 3*mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"), ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 3*mm),
    ]))
    return t

def kv_table(rows, col1=42*mm):
    data = [[Paragraph(k, S_CELL_B), Paragraph(v, S_CELL)] for k, v in rows]
    t = Table(data, colWidths=[col1, PAGE_W - 2*M - col1])
    style = [
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 2.6), ("BOTTOMPADDING", (0,0), (-1,-1), 2.6),
        ("LINEBELOW", (0,0), (-1,-2), 0.4, LINE),
    ]
    for i in range(len(rows)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0,i), (-1,i), ROW_ALT))
    t.setStyle(TableStyle(style))
    return t

# ============================== PAGE 1 — COUVERTURE ==============================
E.append(Spacer(1, 10*mm))
E.append(Paragraph("Imprimantes 3D fermées<br/>&amp; multi-couleurs", S_TITLE))
E.append(Spacer(1, 3*mm))
E.append(Paragraph("Dossier comparatif — sélection bol.com Belgique · 10 juin 2026", S_SUB))
E.append(Spacer(1, 5*mm))
E.append(HRFlowable(width="100%", thickness=1.2, color=ACCENT))
E.append(Spacer(1, 6*mm))

E.append(Paragraph("Cahier des charges", S_H2))
E.append(Paragraph(
    "• Imprimante 3D <b>fermée</b> (enclosure complète) &nbsp;&nbsp;• <b>Multi-couleurs</b> de série (module type AMS inclus)<br/>"
    "• <b>Livrable demain</b> (stock affiché bol.com au 10/06/2026) &nbsp;&nbsp;• Modèle de référence : Anycubic Kobra S1 Combo",
    S_BODY))
E.append(Spacer(1, 5*mm))

E.append(Paragraph("Verdict en 30 secondes", S_H2))
verdict_data = [
    [Paragraph("<b>N°1 — RECOMMANDÉ : Anycubic Kobra S1 Combo · 429,99 €</b>", S_CELL_B),],
    [Paragraph("Fermée, 4 couleurs (extensible 8), module ACE Pro qui <b>sèche le filament</b> et se pose <b>à côté</b> de la machine, "
               "caméra incluse, la mécanique la plus fiable du lot selon la presse (Tom's Hardware : « comparable à une Bambu Lab »). "
               "Vendeur Vlotty 9,3/10 — <b>commande avant 15h00 → livrée demain</b>.", S_CELL)],
    [Paragraph("<b>N°2 — CHALLENGER SÉRIEUX : Elegoo Centauri Carbon 2 Combo · 429,95 €</b>", S_CELL_B)],
    [Paragraph("Même prix au centime, fermée, buse 350 °C, presse exceptionnelle (How-To Geek 9/10, Editor's Choice 2026). "
               "Mais : module CANVAS perché sur le capot (~74 cm de haut), 4 couleurs <b>non extensibles</b>, bobines à l'air libre (pas de séchage), "
               "zéro avis client bol.com (produit trop récent).", S_CELL)],
    [Paragraph("<b>N°3 — OPTION « TOUJOURS PLUS » : Creality K2 Combo · 540 €</b> (extensible 16 couleurs)", S_CELL_B)],
    [Paragraph("110 € de plus pour un écosystème slicer plus mûr (Creality Print) et un CFS chaînable jusqu'à 16 couleurs. "
               "Vlotty, avant 15h00 → demain. Le K2 <b>Pro</b> (650 €, chambre chauffée 60 °C, 300×300×300) est le seul vrai cran au-dessus "
               "techniquement, mais sans « livré demain » affiché.", S_CELL)],
]
vt = Table([[r[0]] for r in verdict_data], colWidths=[PAGE_W - 2*M])
vt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,1), GOLD_LIGHT),
    ("BACKGROUND", (0,2), (0,3), ACCENT_LIGHT),
    ("BACKGROUND", (0,4), (0,5), ROW_ALT),
    ("BOX", (0,0), (0,1), 0.8, GOLD), ("BOX", (0,2), (0,3), 0.8, ACCENT), ("BOX", (0,4), (0,5), 0.8, LINE),
    ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
E.append(vt)
E.append(Spacer(1, 5*mm))

E.append(Paragraph("Écrémage : éliminées d'office", S_H2))
elim = [
    ("Flashforge AD5X — 339 €", "Cadre OUVERT (enclosure en option à monter soi-même) → critère « fermée » non rempli. Dommage : meilleur prix multi-couleurs."),
    ("Creality K1 Max — 499/499,95 €", "Fermée mais MONO-couleur (kit CFS vendu à part, et le capot ne ferme plus avec)."),
    ("Creality K1C — 350 €", "Fermée mais MONO-couleur (même logique)."),
    ("3Dandprint Mini — 295,95 €", "Machine débutant Easythreed : minuscule, PLA seul, mono-couleur. Hors catégorie."),
    ("FlashForge Adventurer 3 + scanner — 105 €", "Vieille machine mono-couleur + scanner d'entrée de gamme. Hors sujet."),
    ("Lot 25 kg filament PLA+ — 270,99 €", "Ce n'est pas une imprimante — encart sponsorisé glissé dans la page."),
]
et = Table([[Paragraph(f"<b>{k}</b>", S_CELL), Paragraph(v, S_CELL)] for k, v in elim],
           colWidths=[58*mm, PAGE_W - 2*M - 58*mm])
et.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LINEBELOW", (0,0), (-1,-2), 0.4, LINE),
    ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 2.4), ("BOTTOMPADDING", (0,0), (-1,-1), 2.4),
    ("ROWBACKGROUNDS", (0,0), (-1,-1), [colors.white, ROW_ALT]),
]))
E.append(et)
E.append(PageBreak())

# ============================== FICHES MODÈLES ==============================
def fiche(num, titre, badge_txt, badge_col, prix, prix_note, photos, caps, infos, forces, faiblesses, presse):
    E.append(Paragraph(f"{num} · {titre}", S_H1))
    head = Table([[badge_table(badge_txt, badge_col), Paragraph(prix, S_PRICE), Paragraph(prix_note, S_SMALL)]],
                 colWidths=[78*mm, 38*mm, None])
    head.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                              ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 4)]))
    E.append(head)
    E.append(Spacer(1, 3*mm))
    E.append(photo_row(photos[0], photos[1], caps[0], caps[1]))
    E.append(Spacer(1, 3*mm))
    E.append(kv_table(infos))
    E.append(Spacer(1, 2.5*mm))
    ff = Table([[Paragraph("<b>POINTS FORTS</b><br/>" + forces, S_CELL),
                 Paragraph("<b>POINTS FAIBLES</b><br/>" + faiblesses, S_CELL)]],
               colWidths=[(PAGE_W - 2*M)/2 - 2*mm, (PAGE_W - 2*M)/2 - 2*mm])
    ff.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("BACKGROUND", (0,0), (0,0), ACCENT_LIGHT), ("BACKGROUND", (1,0), (1,0), RED_LIGHT),
        ("BOX", (0,0), (0,0), 0.6, ACCENT), ("BOX", (1,0), (1,0), 0.6, RED),
        ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    E.append(ff)
    E.append(Spacer(1, 2.5*mm))
    E.append(Paragraph("<b>Ce qu'en dit la presse :</b> " + presse, S_BODY_S))
    E.append(PageBreak())

# --- 1. KOBRA S1 ---
fiche(
    "1", "Anycubic Kobra S1 Combo", "LA RECOMMANDATION", GOLD,
    "429,99 €", "−33 % (prix conseillé 649 €) · Vlotty (9,3/10) · 4,4/5 — 22 avis bol",
    ("kobra-s1-1.jpg", "kobra-s1-2.jpg"),
    ("Machine fermée + ACE Pro (4 bobines) — lauréate Red Dot 2025",
     "Config 8 couleurs : 2 modules ACE Pro chaînés à côté de la machine"),
    [
        ("Disponibilité bol.com", "<b>En stock — commandé avant 15h00, livré demain.</b> Vendeur marketplace Vlotty (9,3/10), pas bol même."),
        ("Structure", "CoreXY <b>entièrement fermée</b> (1re CoreXY d'Anycubic) · 400 × 410 × 490 mm · 18 kg — l'ACE Pro se pose À CÔTÉ, la machine reste basse"),
        ("Volume d'impression", "250 × 250 × 250 mm"),
        ("Multi-couleurs", "ACE Pro 4 bobines inclus · <b>extensible à 8 couleurs</b> (2e ACE Pro ≈ 100-130 €) · <b>séchage actif du filament 55 °C, même en cours d'impression</b> — unique dans ce comparatif"),
        ("Vitesse / précision", "600 mm/s max (300 recommandé) · accél. 10 000 mm/s² · nivellement auto LeviQ 3.0 + compensation de résonance"),
        ("Buse / lit / chambre", "Buse 320 °C démontage rapide · lit PEI 120 °C · chambre fermée passive (pas de chauffage actif)"),
        ("Filaments", "PLA, PETG, TPU 95A, ABS, ASA (enclosure + 320 °C = ABS/ASA réalistes)"),
        ("Équipement", "Caméra HD incluse (timelapse + détection spaghetti) · écran tactile 4,3\" · WiFi + app · ≤ 44-46 dB · slicer Anycubic Slicer Next (base Orca)"),
    ],
    "Mécanique « set and forget » saluée après des centaines d'heures (Tom's Hardware) · qualité mono-couleur « parmi les meilleures jamais testées » (TechRadar) · ACE Pro = seul module qui sèche les bobines · caméra incluse · architecture basse (module à côté, pas sur le capot) · SAV Anycubic réactif (remplacement obtenu, Creative Bloq)",
    "Slicer en retrait : n'affiche pas le volume de purge, réglages purge sur la machine uniquement · changements de couleur lents (print multi-couleurs « plusieurs heures plus lent qu'une Bambu ») · purge gaspilleuse (un Benchy 11 g a généré 183 g de déchets en test extrême) · WiFi/app instables (avis bol + presse) · cas documentés de bourrage ACE Pro (wiki officiel dédié)",
    "Tom's Hardware « Good printer, bad slicer » — fiabilité comparable à une Bambu Lab P1P · Creative Bloq « excellente quand elle marche, frustrante quand elle ne marche pas » (panne capteur remplacée sous garantie) · consensus : le meilleur rapport prix/équipement de la catégorie, pas un « Bambu killer »."
)

# --- 2. ELEGOO CC2 ---
fiche(
    "2", "Elegoo Centauri Carbon 2 Combo", "CHALLENGER — PRESSE EN OR", ACCENT,
    "429,95 €", "Prix officiel 439 € · Vlotty (9,3/10) · aucun avis bol (sortie ~mars 2026)",
    ("cc2-1.jpg", "cc2-2.jpg"),
    ("CANVAS sur le capot + 4 bobines sur le flanc — l'ensemble culmine à ~74 cm",
     "De face : bobines latérales à l'air libre, écran déporté"),
    [
        ("Disponibilité bol.com", "<b>En stock — commandé avant 15h00, livré demain.</b> Vendeur Vlotty (9,3/10). Zéro avis client pour l'instant."),
        ("Structure", "CoreXY <b>fermée</b> (verre renforcé, filtration HEPA + charbon, grille d'échappement pilotée) · machine seule ~398 × 404 × 490 mm · <b>500 × 480 × 743 mm avec CANVAS sur le capot</b> · prévoir ~600 mm de large avec les 4 bobines · 19,35 kg"),
        ("Volume d'impression", "256 × 256 × 256 mm (le plus généreux à ce prix)"),
        ("Multi-couleurs", "Module CANVAS 4 bobines inclus, RFID, auto-refill, détection d'emmêlement · <b>NON extensible</b> (4 couleurs maxi, pas de chaînage) · bobines exposées (pas de caisson, pas de séchage)"),
        ("Vitesse / précision", "500 mm/s max · accél. 20 000 mm/s² · auto-calibration 1 clic (31 capteurs)"),
        ("Buse / lit / chambre", "<b>Buse acier trempé 350 °C</b> (la plus chaude du dossier) · lit 110 °C · chambre fermée passive"),
        ("Filaments", "PLA, PETG, TPU, ABS, ASA, PC, PLA-CF/PETG-CF (acier trempé = OK fibre carbone)"),
        ("Équipement", "Caméra (monitoring + timelapse) · très silencieuse · slicer ElegooSlicer (base Orca) + app Elegoo Matrix"),
    ],
    "Torture test How-To Geek : <b>1 100+ changements de filament en 30 h sans panne critique</b> · 91 % de réussite premier essai en multi-couleurs (3DTechValley) · buse 350 °C + acier trempé = matériaux techniques et carbone · volume légèrement supérieur · ~10 € sous le prix officiel",
    "CANVAS perché sur le capot : silhouette haute (~74 cm) et jugée « visuellement maladroite » (Tom's Hardware) · 4 couleurs sans extension possible · bobines à l'air libre = sensibles à l'humidité · purge gaspilleuse (print Gengar : presque autant de déchet que de pièce) · gestion des bobines plus manuelle que Bambu/Creality · conduit de purge qui peut se boucher · aucun retour client bol pour se rassurer",
    "How-To Geek <b>9/10, Editor's Choice 2026</b> · Tom's Hardware « délicieuse CoreXY budget » · 3DWithUs : transitions de couleurs propres · consensus : le meilleur rapport prix/features du multi-couleurs fermé sous 500 €, à condition d'accepter ses 4 couleurs fixes."
)

# --- 3. K2 COMBO ---
fiche(
    "3", "Creality K2 Combo (CFS)", "L'ÉVOLUTIVE — 16 COULEURS POSSIBLES", INK,
    "540,00 €", "Listing Vlotty (9,3/10), barré 559 € · le même produit existe à 599 € (Mi RobotHome, avant 23h) · 4,5/5 (2 avis) / 4/5 (10 avis)",
    ("k2-combo-1.jpg", "k2-combo-2.jpg"),
    ("K2 Combo avec CFS 4 bobines posé sur le capot",
     "K2 seule : cadre tout métal, chambre fermée, écran tactile"),
    [
        ("Disponibilité bol.com", "<b>540 € chez Vlotty : avant 15h00 → livré demain, port gratuit.</b> Variante 599 € (Mi RobotHome Store) : avant 23h00 → demain. Même machine — prendre la moins chère si l'horaire 15h convient."),
        ("Structure", "CoreXY <b>fermée</b>, cadre entièrement métallique · ~404 × 437 × 546 mm machine seule · CFS sur le capot (+ ~276 mm) → ~82 cm de haut · 18,3 kg"),
        ("Volume d'impression", "260 × 260 × 260 mm"),
        ("Multi-couleurs", "CFS 4 bobines inclus, RFID Creality, relais auto fin de bobine · <b>chaînable jusqu'à 4 unités = 16 couleurs</b> (record du dossier)"),
        ("Vitesse / précision", "600 mm/s · accél. 20 000 mm/s² · nivellement auto"),
        ("Buse / lit / chambre", "Buse 300 °C quick-swap · lit 110 °C · chambre fermée passive (PAS chauffée — c'est le K2 Pro qui l'a)"),
        ("Filaments", "PLA, PETG, PET, PLA-CF · ABS/ASA possibles mais déconseillés en grandes pièces sans chambre chauffée"),
        ("Équipement", "Caméra IA (détection erreurs/spaghetti) · écran tactile couleur · WiFi + app · slicer Creality Print 6 (écosystème le plus mûr du trio chinois)"),
    ],
    "CFS extensible 16 couleurs — aucune rivale du dossier ne suit · écosystème logiciel Creality Print plus abouti que les slicers Anycubic/Elegoo · RFID + relais de bobine automatique · cadre tout métal · caméra IA de série",
    "110 € de plus que Kobra S1/CC2 pour une buse 20 °C moins chaude (300 °C) · chambre passive comme les deux autres (le « Pro » à 650 € a la chambre chauffée) · un avis bol signale bruit et vibrations importants · seulement 2 avis sur le listing à 540 € · CFS sur le capot : ~82 cm de haut · purge multi-couleurs gaspilleuse (commun à tous les systèmes mono-buse)",
    "Tom's Hardware (sur la gamme K2) : machines « polies, très abouties » · The Gadgeteer : « plateformes riches en fonctionnalités » · la presse place la gamme K2 au niveau du duel Bambu, avec l'extensibilité 16 couleurs comme argument signature."
)

# --- 4. K2 PRO ---
fiche(
    "4", "Creality K2 Pro Combo (CFS)", "LA PLUS TECHNIQUE — MAIS PAS DEMAIN", GREY,
    "650,00 €", "−24 % (prix conseillé 859 €) · 3D4YouStore · 4/5 (10 avis) · ATTENTION : pas de « livré demain » affiché",
    ("k2-pro-1.jpg", "k2-pro-2.jpg"),
    ("K2 Pro Combo : CFS multicolore sur le capot",
     "K2 Pro seule — 300×300×300, double caméra IA, step-servo"),
    [
        ("Disponibilité bol.com", "650 € chez 3D4YouStore — <b>aucune mention « livré demain »</b> sur le listing au 10/06. Pièges repérés : le même vendeur a un 2e listing à 779,95 € (1-2 semaines), et H.Y. Cloud GmbH en demande 1 422 € — ignorer ces deux-là."),
        ("Structure", "CoreXY <b>fermée</b> · 445 × 505 × <b>850 mm avec CFS</b> · 23,7 kg (+ CFS 4,56 kg) · moteurs step-servo XY + extrudeur"),
        ("Volume d'impression", "<b>300 × 300 × 300 mm</b> (le plus grand du dossier)"),
        ("Multi-couleurs", "CFS 4 bobines, RFID, extensible <b>16 couleurs</b> (comme le K2)"),
        ("Vitesse / précision", "600 mm/s · accél. 20 000 mm/s² · débit 40 mm³/s"),
        ("Buse / lit / chambre", "Buse 300 °C · lit 110 °C · <b>chambre CHAUFFÉE ACTIVE jusqu'à 60 °C — la seule du dossier</b>"),
        ("Filaments", "PLA, PETG, PET, ABS, ASA, PLA-CF, PA-CF, PPA-CF — la chambre chauffée rend les filaments techniques réellement fiables"),
        ("Équipement", "<b>Double caméra IA</b> · écran tactile 4\" · WiFi + app · Creality Print 6"),
    ],
    "La seule machine du comparatif avec chambre chauffée active 60 °C : ABS/ASA/nylon-carbone en grandes pièces sans warping · volume 300³ · double caméra IA · step-servo (précision/fiabilité) · 16 couleurs possibles · −24 % sur le prix conseillé = vraie affaire pour ce niveau d'équipement",
    "<b>Ne remplit pas ton critère « demain »</b> (pas de promesse de livraison affichée) · 650 € = +220 € vs Kobra S1 · 85 cm de haut avec CFS · vendeur 3D4YouStore moins établi que Vlotty · buse 300 °C (vs 350 °C Elegoo) · surdimensionnée si tu restes sur PLA/PETG décoratif",
    "Tom's Hardware : « <b>A polished performer</b> » — speedster 4 couleurs très abouti, juste en dessous du K2 Plus · c'est l'achat « engineering » du dossier : pertinent seulement si ABS/ASA/CF en grand format font partie du plan."
)

# --- 5. AD5X ---
fiche(
    "5", "Flashforge Adventurer 5X (AD5X)", "ÉLIMINÉE — CADRE OUVERT", RED,
    "339,00 €", "Vlotty (9,3/10) · 4,3/5 — 30 avis bol · documentée par acquit de conscience",
    ("ad5x-1.jpg", "ad5x-2.jpg"),
    ("AD5X : cadre OUVERT, rack 4 bobines latéral (IFS)",
     "Trois-quarts : tubes PTFE et rack apparents — pas d'enclosure"),
    [
        ("Pourquoi éliminée", "<b>Cadre ouvert — pas d'enclosure d'origine.</b> Le wiki officiel Flashforge propose un kit enclosure optionnel à monter soi-même : preuve par l'absence. Critère « fermée » non rempli."),
        ("Disponibilité bol.com", "En stock, expédition le lendemain · Vlotty (9,3/10)"),
        ("L'essentiel", "CoreXY 600 mm/s · 220 × 220 × 220 mm · IFS 4 couleurs (gère même le TPU multi-couleurs, rare) · buse 300 °C quick-detach · pas de caméra · slicer Orca-Flashforge jugé buggé (Tom's Hardware)"),
        ("À retenir", "Ticket d'entrée multi-couleurs le moins cher du marché en CoreXY rapide — et purge plus efficace que la Kobra S1. Si un jour le critère « fermée » saute, elle redevient pertinente à 339 €."),
    ],
    "Prix imbattable · IFS fiable, auto-calibré, TPU multi-couleurs · transitions de couleurs nettes · setup 20 min",
    "OUVERTE (rédhibitoire ici) · pas de caméra · Z limité à 220 mm · slicer crashs/bugs · pas de manuel NL (avis bol) · porte-bobines durs avec filaments fragiles",
    "Tom's Hardware : « bonne imprimante, mauvaise expérience slicer » · Hoffman Engineering &amp; 3DWithUs : très bon rapport qualité-prix multi-couleurs — mais en cadre ouvert."
)

# ============================== TABLEAU COMPARATIF ==============================
E.append(Paragraph("Tableau comparatif synthétique", S_H1))
E.append(Spacer(1, 2*mm))

def C(txt, bold=False):
    return Paragraph(txt, S_CELL_B if bold else S_CELL)
def CW(txt):
    return Paragraph(txt, S_CELL_W)

comp = [
    [CW("Critère"), CW("Kobra S1 Combo"), CW("Centauri Carbon 2"), CW("K2 Combo"), CW("K2 Pro Combo")],
    [C("Prix bol.com", 1), C("<b>429,99 €</b> (−33 %)"), C("<b>429,95 €</b>"), C("540 € (ou 599 €)"), C("650 € (−24 %)")],
    [C("Livré demain ?", 1), C("<b>OUI</b> — avant 15h (Vlotty)"), C("<b>OUI</b> — avant 15h (Vlotty)"), C("<b>OUI</b> — avant 15h (540 €) / avant 23h (599 €)"), C("<b>NON affiché</b> (3D4YouStore)")],
    [C("Avis clients bol", 1), C("4,4/5 — 22 avis"), C("Aucun (trop récente)"), C("4,5/5 (2) · 4/5 (10)"), C("4/5 — 10 avis")],
    [C("Fermée", 1), C("Oui — CoreXY enclos"), C("Oui — verre + filtre HEPA"), C("Oui — cadre métal"), C("Oui")],
    [C("Chambre chauffée", 1), C("Non (passive)"), C("Non (passive)"), C("Non (passive)"), C("<b>OUI — 60 °C active</b>")],
    [C("Couleurs incluses / max", 1), C("4 / <b>8</b> (2e ACE Pro)"), C("4 / 4 (non extensible)"), C("4 / <b>16</b> (CFS chaînable)"), C("4 / <b>16</b>")],
    [C("Séchage filament", 1), C("<b>OUI — ACE Pro 55 °C</b>, même en imprimant"), C("Non — bobines à l'air libre"), C("Non (caisson CFS fermé, sans chauffe)"), C("Non (idem)")],
    [C("Position du module", 1), C("<b>À côté</b> — machine 49 cm de haut"), C("Sur le capot — ~74 cm"), C("Sur le capot — ~82 cm"), C("Sur le capot — 85 cm")],
    [C("Volume d'impression", 1), C("250 × 250 × 250"), C("256 × 256 × 256"), C("260 × 260 × 260"), C("<b>300 × 300 × 300</b>")],
    [C("Buse max", 1), C("320 °C"), C("<b>350 °C</b> acier trempé"), C("300 °C"), C("300 °C")],
    [C("Lit max", 1), C("<b>120 °C</b>"), C("110 °C"), C("110 °C"), C("110 °C")],
    [C("Vitesse / accél.", 1), C("600 mm/s · 10K"), C("500 mm/s · 20K"), C("600 mm/s · 20K"), C("600 mm/s · 20K")],
    [C("Caméra", 1), C("HD incluse"), C("Incluse"), C("1 caméra IA"), C("<b>2 caméras IA</b>")],
    [C("Filaments", 1), C("PLA PETG TPU ABS ASA"), C("PLA PETG TPU ABS ASA PC CF"), C("PLA PETG PET PLA-CF (ABS limité)"), C("PLA PETG ABS ASA PA-CF PPA-CF")],
    [C("Slicer / écosystème", 1), C("Anycubic Slicer Next — le point faible"), C("ElegooSlicer (Orca) — bugs mineurs"), C("Creality Print 6 — le plus mûr"), C("Creality Print 6")],
    [C("Presse", 1), C("Tom's HW : fiabilité type Bambu, slicer faible"), C("How-To Geek <b>9/10 EC 2026</b>"), C("Gamme saluée « polished »"), C("Tom's HW « polished performer »")],
]
cw = [30*mm, 37*mm, 37*mm, 37*mm, 37*mm]
ct = Table(comp, colWidths=cw, repeatRows=1)
ct.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), ACCENT),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("GRID", (0,0), (-1,-1), 0.4, LINE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, ROW_ALT]),
    ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING", (0,0), (-1,-1), 3), ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ("BACKGROUND", (1,0), (1,0), GOLD),
]))
E.append(ct)
E.append(Spacer(1, 4*mm))
E.append(Paragraph(
    "<b>Important — vérité utile sur le multi-couleurs (toutes marques) :</b> tous ces systèmes mono-buse purgent du filament à chaque "
    "changement de couleur. En usage extrême, la purge peut dépasser plusieurs fois le poids de la pièce (Benchy 11 g → 183 g de purge "
    "sur Kobra S1 ; ratio ~2:1 mesuré sur Elegoo et Flashforge) et rallonger fortement les temps d'impression. C'est structurel, "
    "pas un défaut d'une marque — Bambu Lab a le même problème. À intégrer dans le budget filament.", S_BODY_S))
E.append(PageBreak())

# ============================== RECO FINALE ==============================
E.append(Paragraph("Recommandation finale", S_H1))
E.append(Spacer(1, 2*mm))
E.append(Paragraph(
    "<b>Prends l'Anycubic Kobra S1 Combo à 429,99 € — et commande avant 15h00 pour l'avoir demain.</b>",
    st("reco", fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=GOLD)))
E.append(Spacer(1, 3*mm))
E.append(Paragraph(
    "Ta préférence initiale sort confirmée par les faits, pas par sentiment. À prix strictement égal avec l'Elegoo (4 centimes d'écart), "
    "elle gagne sur quatre points concrets : <b>(1)</b> l'ACE Pro est le seul module du marché à ce prix qui <b>sèche le filament à 55 °C même "
    "pendant l'impression</b> — en Belgique, l'humidité est l'ennemi n°1 du PLA/PETG, et l'Elegoo laisse ses bobines à l'air libre ; "
    "<b>(2)</b> elle est <b>extensible à 8 couleurs</b> quand l'Elegoo est verrouillée à 4 ; <b>(3)</b> le module se pose à côté — silhouette basse, "
    "architecture plus saine que les modules perchés sur le capot qu'il faut déposer à chaque intervention ; <b>(4)</b> elle a <b>22 avis clients "
    "réels sur bol.com (4,4/5)</b> et des centaines d'heures de recul presse, là où l'Elegoo n'a encore aucun retour client. "
    "Son vrai défaut — le slicer — se contourne : la communauté imprime via OrcaSlicer, et Anycubic pousse des mises à jour.", S_BODY))
E.append(Spacer(1, 4*mm))

E.append(Paragraph("Change d'avis seulement si…", S_H2))
cases = [
    ("… tu veux imprimer du carbone/PC dès maintenant", "→ <b>Elegoo CC2 Combo (429,95 €)</b> : buse acier trempé 350 °C, prête pour PLA-CF/PETG-CF/PC sans changer de buse. Accepte en échange : 4 couleurs à vie, pas de séchage, zéro recul client."),
    ("… tu vises plus de 8 couleurs ou l'écosystème le plus mûr", "→ <b>Creality K2 Combo (540 €, Vlotty avant 15h)</b> : CFS chaînable jusqu'à 16 couleurs, Creality Print 6 plus abouti. +110 € pour de l'évolutivité."),
    ("… l'ABS/ASA/nylon en grandes pièces est ton vrai objectif", "→ <b>Creality K2 Pro Combo (650 €)</b> : seule chambre chauffée active (60 °C) du dossier + volume 300³. Mais pas de « livré demain » affiché — ton critère saute."),
    ("… le critère « fermée » saute un jour", "→ <b>Flashforge AD5X (339 €)</b> redevient le meilleur rapport prix/multi-couleurs."),
]
ctab = Table([[Paragraph(f"<b>{k}</b>", S_CELL), Paragraph(v, S_CELL)] for k, v in cases],
             colWidths=[62*mm, PAGE_W - 2*M - 62*mm])
ctab.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LINEBELOW", (0,0), (-1,-2), 0.4, LINE),
    ("ROWBACKGROUNDS", (0,0), (-1,-1), [colors.white, ROW_ALT]),
    ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 3), ("BOTTOMPADDING", (0,0), (-1,-1), 3),
]))
E.append(ctab)
E.append(Spacer(1, 5*mm))

E.append(Paragraph("Check-list avant de cliquer « Commander »", S_H2))
E.append(Paragraph(
    "1. <b>Horaire</b> : commande avant <b>15h00</b> (deadline Vlotty) pour la livraison demain — vérifie que la promesse « livré demain » "
    "est toujours affichée au moment de l'achat, le stock marketplace bouge vite.<br/>"
    "2. <b>Vendeur</b> : c'est Vlotty (marketplace, 9,3/10) qui vend et expédie, pas bol — retours 30 jours + garantie légale via le vendeur, "
    "avec le Service Clients bol en filet de sécurité.<br/>"
    "3. <b>Le titre bol dit « 8 couleurs »</b> : le carton contient 1 ACE Pro = <b>4 couleurs</b>. Les 8 couleurs supposent un 2e ACE Pro "
    "(≈ 100-130 € chez Anycubic) — à savoir avant de rêver en huit teintes.<br/>"
    "4. <b>Premier achat filament</b> : prévois 2-3 bobines de PLA de plus que prévu — la purge multi-couleurs consomme. "
    "Et un bac de capture pour les déchets de purge (« poop bucket », imprimable… en premier print).<br/>"
    "5. <b>À l'installation</b> : mise à jour firmware immédiate + test du WiFi (point faible connu) ; en cas de souci, "
    "l'impression par USB/carte marche toujours.", S_BODY))

doc.build(E)
print("OK:", OUT)
